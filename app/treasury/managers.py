# app/treasury/managers.py

from app.treasury.schemas import (
    InvoiceBase,
    RevenueBase,
    ReceivableBase,
    FXRateBase
)
import asyncio
import bisect
import calendar
import logging
from datetime import date, timedelta
from decimal import Decimal
from typing import Optional
from fastapi import HTTPException
from app.customers.db import (
    get_customers_db,
    get_customer_db,
    get_contract_db,
    get_contracts_db,
    get_contract_by_customer_db,
    get_latest_aggregate_by_customer_db,
    get_aggregates_by_customer_db,
    get_aggregates_db
)
from app.treasury.db import (
    get_invoices_db,
    get_invoice_db,
    count_invoices_for_year_db,
    add_invoice_db,
    update_invoice_db,
    delete_invoice_db,
    delete_invoices_db,
    mark_invoice_paid_db,
    add_receivable_db,
    delete_receivable_by_invoice_db,
    delete_receivables_db,
    add_revenue_db,
    delete_revenue_by_invoice_db,
    delete_revenues_db,
    update_receivable_by_invoice_db,
    update_revenue_by_invoice_db,
    get_fxrates_db,
    get_fxrate_db,
    add_fxrate_db,
    update_fxrate_db,
    delete_fxrate_db,
    delete_fxrates_db
)

logger = logging.getLogger(__name__)

# Maps INVOICES fields to their RECEIVABLES/REVENUES counterparts so shared
# values stay in sync. booking_date is sourced differently per ledger:
# invoicing_date for receivables, payment_date for revenues.
RECEIVABLE_FIELD_MAP = {
    "invoicing_date": "booking_date",
    "due_date": "due_date",
    "currency": "currency",
    "fx_rate": "fx_rate",
    "total_usd": "amount_usd",
    "total_idr": "amount_idr",
}
REVENUE_FIELD_MAP = {
    "payment_date": "booking_date",
    "due_date": "due_date",
    "currency": "currency",
    "fx_rate": "fx_rate",
    "total_usd": "amount_usd",
    "total_idr": "amount_idr",
}

# Vehicle types whose aggregate counts are multiplied by their matching
# CONTRACTS price_<type> column to compute an invoice's pretax amount.
VEHICLE_TYPES = [
    "dt",
    "exca",
    "lv",
    "dozer",
    "grader",
    "water_truck",
    "fuel_truck",
    "manhauler",
]
VAT_RATE = Decimal("0.11")
DEFAULT_RATE = Decimal("17500")
MONTHS_PER_YEAR = 12


def _to_date(value):
    if value is None or isinstance(value, date):
        return value
    return date.fromisoformat(value)


def _add_months(d: date, months: int) -> date:
    month_index = d.month - 1 + months
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)

class InvoiceManager:
    def __init__(self, invoice: InvoiceBase):
        self.invoice = invoice

    def _build_receivable(self, invoice: dict) -> ReceivableBase:
        return ReceivableBase(
            invoice_id=invoice.get("id"),
            booking_date=invoice.get("invoicing_date"),
            due_date=invoice.get("due_date"),
            currency=invoice.get("currency"),
            amount_usd=invoice.get("total_usd"),
            fx_rate=invoice.get("fx_rate"),
            amount_idr=invoice.get("total_idr"),
        )

    def _build_revenue(self, invoice: dict) -> RevenueBase:
        return RevenueBase(
            invoice_id=invoice.get("id"),
            booking_date=invoice.get("payment_date"),
            due_date=invoice.get("due_date"),
            currency=invoice.get("currency"),
            amount_usd=invoice.get("total_usd"),
            fx_rate=invoice.get("fx_rate"),
            amount_idr=invoice.get("total_idr"),
        )

    async def get_invoices(self):
        return await get_invoices_db()

    async def get_invoice(self, invoice_id: int):
        return await get_invoice_db(invoice_id)

    async def add_invoice(self):
        invoice_result = await add_invoice_db(self.invoice)
        await add_receivable_db(self._build_receivable(invoice_result[0]))
        return invoice_result

    async def update_invoice(self, invoice_id: int):
        updated_fields = self.invoice.model_dump(exclude_unset=True, mode="json")

        before = await get_invoice_db(invoice_id)
        was_paid = before[0].get("is_paid") if before else False

        invoice_result = await update_invoice_db(self.invoice, invoice_id)

        after = await get_invoice_db(invoice_id)
        invoice = after[0] if after else {}
        is_paid = invoice.get("is_paid", False)

        if was_paid != is_paid:
            if is_paid:
                await delete_receivable_by_invoice_db(invoice_id)
                await add_revenue_db(self._build_revenue(invoice))
            else:
                await delete_revenue_by_invoice_db(invoice_id)
                await add_receivable_db(self._build_receivable(invoice))
        else:
            field_map = REVENUE_FIELD_MAP if is_paid else RECEIVABLE_FIELD_MAP
            ledger_data = {
                field_map[field]: value
                for field, value in updated_fields.items()
                if field in field_map
            }
            if ledger_data:
                if is_paid:
                    await update_revenue_by_invoice_db(invoice_id, ledger_data)
                else:
                    await update_receivable_by_invoice_db(invoice_id, ledger_data)

        return invoice_result

    async def delete_invoice(self, invoice_id: int):
        existing = await get_invoice_db(invoice_id)
        is_paid = existing[0].get("is_paid") if existing else False
        invoice_result = await delete_invoice_db(invoice_id)
        if is_paid:
            await delete_revenue_by_invoice_db(invoice_id)
        else:
            await delete_receivable_by_invoice_db(invoice_id)
        return invoice_result

    async def delete_invoices(self):
        invoice_result = await delete_invoices_db()
        await delete_receivables_db()
        await delete_revenues_db()
        return invoice_result

    async def mark_invoice_paid(self, invoice_id: int, payment_date: date):
        paid_result = await mark_invoice_paid_db(invoice_id, payment_date)
        invoice_result = await get_invoice_db(invoice_id)
        await delete_receivable_by_invoice_db(invoice_id)
        await add_revenue_db(self._build_revenue(invoice_result[0]))
        return paid_result

    async def generate_invoice(self, contract_id: int, fx_rate: Decimal, invoicing_date: date):
        contract_result, invoice_count = await asyncio.gather(
            get_contract_db(contract_id),
            count_invoices_for_year_db(invoicing_date.year),
        )
        if not contract_result:
            raise HTTPException(status_code=404, detail=f"Contract {contract_id} not found")
        contract = contract_result[0]

        invoice_number = (
            f"{invoicing_date:%y/%d/%m}/{invoice_count + 1:04d}"
        )

        aggregate_result = await get_latest_aggregate_by_customer_db(contract["customer_id"], invoicing_date)
        if not aggregate_result:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"No aggregate found for customer {contract['customer_id']} "
                    f"on or before invoicing date {invoicing_date.isoformat()}"
                ),
            )
        aggregate = aggregate_result[0]

        pretax = Decimal("0")
        for vehicle in VEHICLE_TYPES:
            quantity = Decimal(str(aggregate.get(vehicle) or 0))
            price = Decimal(str(contract.get(f"price_{vehicle}") or 0))
            pretax += quantity * price

        vat = pretax * VAT_RATE
        total = pretax + vat

        currency = contract.get("currency")
        pretax_usd = vat_usd = total_usd = None
        pretax_idr = vat_idr = total_idr = None

        if currency == "IDR":
            pretax_idr, vat_idr, total_idr = pretax, vat, total
            if fx_rate:
                pretax_usd = pretax / fx_rate
                vat_usd = vat / fx_rate
                total_usd = total / fx_rate
        elif currency == "USD":
            pretax_usd, vat_usd, total_usd = pretax, vat, total
            if fx_rate:
                pretax_idr = pretax * fx_rate
                vat_idr = vat * fx_rate
                total_idr = total * fx_rate

        self.invoice = InvoiceBase(
            contract_id=contract_id,
            invoice_number=invoice_number,
            invoicing_date=invoicing_date,
            due_date=invoicing_date + timedelta(days=14),
            is_paid=False,
            currency=currency,
            fx_rate=fx_rate,
            pretax_usd=pretax_usd,
            vat_usd=vat_usd,
            total_usd=total_usd,
            pretax_idr=pretax_idr,
            vat_idr=vat_idr,
            total_idr=total_idr,
        )
        return await self.add_invoice()


class KpiManager:
    def _aggregate_amount(self, contract: dict, aggregate: dict) -> Decimal:
        amount = Decimal("0")
        for vehicle in VEHICLE_TYPES:
            quantity = Decimal(str(aggregate.get(vehicle) or 0))
            price = Decimal(str(contract.get(f"price_{vehicle}") or 0))
            amount += quantity * price
        return amount

    def _prepare_fxrates(self, fxrates: list):
        # Pre-sort rates once so monthly lookups become in-memory binary searches
        # instead of one DB round-trip per month.
        parsed = []
        for entry in fxrates or []:
            fx_date = _to_date(entry.get("fx_date"))
            if fx_date is None:
                continue
            rate = entry.get("rate")
            parsed.append((fx_date, Decimal(str(rate)) if rate else None))
        parsed.sort(key=lambda item: item[0])
        dates = [item[0] for item in parsed]
        rates = [item[1] for item in parsed]
        return dates, rates

    def _select_rate(self, prepared_rates, month: date) -> Decimal:
        dates, rates = prepared_rates
        idx = bisect.bisect_right(dates, month) - 1
        if idx >= 0 and rates[idx] is not None:
            return rates[idx]
        return DEFAULT_RATE

    def _compute_mrr(self, customer: dict, contract: dict, aggregates: list, prepared_rates) -> dict:
        customer_id = customer.get("id")
        if not contract:
            raise HTTPException(status_code=404, detail=f"No contract found for customer {customer_id}")

        start_date = _to_date(contract.get("start_date"))
        end_date = _to_date(contract.get("end_date"))
        if not start_date or not end_date:
            raise HTTPException(
                status_code=400,
                detail=f"Contract for customer {customer_id} is missing start_date or end_date",
            )

        if not aggregates:
            raise HTTPException(status_code=404, detail=f"No aggregates found for customer {customer_id}")
        aggregates = sorted(aggregates, key=lambda a: _to_date(a.get("updated_at")))

        currency = contract.get("currency")
        monthly = []
        total_usd = Decimal("0")
        total_idr = Decimal("0")

        month = _add_months(start_date, 1)
        while month <= end_date:
            active = None
            for aggregate in aggregates:
                if _to_date(aggregate.get("updated_at")) <= month:
                    active = aggregate
                else:
                    break

            amount = self._aggregate_amount(contract, active) if active else Decimal("0")
            rate = self._select_rate(prepared_rates, month)

            amount_usd = None
            amount_idr = None
            if currency == "USD":
                amount_usd = amount
                amount_idr = amount * rate
            elif currency == "IDR":
                amount_idr = amount
                amount_usd = amount / rate

            monthly.append({
                "month": month.isoformat(),
                "currency": currency,
                "amount_usd": amount_usd,
                "amount_idr": amount_idr,
            })
            total_usd += amount_usd or Decimal("0")
            total_idr += amount_idr or Decimal("0")
            month = _add_months(month, 1)

        return {
            "customer_id": customer_id,
            "name": customer.get("name"),
            "legal_name": customer.get("legal_name"),
            "site_name": customer.get("site_name"),
            "site_legal_name": customer.get("site_legal_name"),
            "currency": currency,
            "monthly": monthly,
            "total_usd": total_usd,
            "total_idr": total_idr,
        }

    def _scale_arr(self, mrr: dict) -> dict:
        monthly = [
            {
                "month": entry["month"],
                "currency": entry["currency"],
                "amount_usd": entry["amount_usd"] * MONTHS_PER_YEAR if entry["amount_usd"] is not None else None,
                "amount_idr": entry["amount_idr"] * MONTHS_PER_YEAR if entry["amount_idr"] is not None else None,
            }
            for entry in mrr["monthly"]
        ]

        return {
            "customer_id": mrr["customer_id"],
            "name": mrr["name"],
            "legal_name": mrr["legal_name"],
            "site_name": mrr["site_name"],
            "site_legal_name": mrr["site_legal_name"],
            "currency": mrr["currency"],
            "monthly": monthly,
            "total_usd": mrr["total_usd"] * MONTHS_PER_YEAR,
            "total_idr": mrr["total_idr"] * MONTHS_PER_YEAR,
        }

    async def get_mrr_by_customer(self, customer_id: int):
        customer_result, contract_result, aggregate_result, fxrates = await asyncio.gather(
            get_customer_db(customer_id),
            get_contract_by_customer_db(customer_id),
            get_aggregates_by_customer_db(customer_id),
            get_fxrates_db(),
        )

        if not customer_result:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")

        contract = contract_result[0] if contract_result else None
        prepared_rates = self._prepare_fxrates(fxrates)
        return self._compute_mrr(customer_result[0], contract, aggregate_result, prepared_rates)

    def _build_mrrs(self, customers: list, contracts: list, aggregates: list, fxrates: list) -> list:
        contracts_by_customer = {}
        for contract in contracts or []:
            contracts_by_customer.setdefault(contract.get("customer_id"), []).append(contract)

        aggregates_by_customer = {}
        for aggregate in aggregates or []:
            aggregates_by_customer.setdefault(aggregate.get("customer_id"), []).append(aggregate)

        prepared_rates = self._prepare_fxrates(fxrates)

        results = []
        for customer in customers or []:
            customer_contracts = contracts_by_customer.get(customer.get("id"))
            contract = customer_contracts[0] if customer_contracts else None
            try:
                results.append(
                    self._compute_mrr(
                        customer,
                        contract,
                        aggregates_by_customer.get(customer.get("id"), []),
                        prepared_rates,
                    )
                )
            except HTTPException:
                # Skip customers without the contract/aggregate data needed for MRR.
                continue
        return results

    async def get_mrr_all_customers(self):
        customers, contracts, aggregates, fxrates = await asyncio.gather(
            get_customers_db(),
            get_contracts_db(),
            get_aggregates_db(),
            get_fxrates_db(),
        )
        if not customers:
            return []
        return self._build_mrrs(customers, contracts, aggregates, fxrates)

    async def get_mrr_by_customer_entity(self, legal_name: str):
        logger.info("Computing MRR for customer entity legal_name=%r", legal_name)
        customers, contracts, aggregates, fxrates = await asyncio.gather(
            get_customers_db(),
            get_contracts_db(),
            get_aggregates_db(),
            get_fxrates_db(),
        )

        entity_customers = [
            customer for customer in (customers or [])
            if customer.get("legal_name") == legal_name
        ]
        if not entity_customers:
            logger.warning("No customers found for legal_name=%r", legal_name)
            raise HTTPException(status_code=404, detail=f"No customers found for legal name '{legal_name}'")

        logger.info(
            "Found %d site(s) for legal_name=%r: %s",
            len(entity_customers),
            legal_name,
            [customer.get("id") for customer in entity_customers],
        )

        results = self._build_mrrs(entity_customers, contracts, aggregates, fxrates)
        logger.info(
            "Computed MRR for %d of %d site(s) for legal_name=%r",
            len(results),
            len(entity_customers),
            legal_name,
        )
        return results

    async def get_mrr_by_site(self, site_legal_name: str):
        logger.info("Computing MRR for site site_legal_name=%r", site_legal_name)
        customers, contracts, aggregates, fxrates = await asyncio.gather(
            get_customers_db(),
            get_contracts_db(),
            get_aggregates_db(),
            get_fxrates_db(),
        )

        site_customers = [
            customer for customer in (customers or [])
            if customer.get("site_legal_name") == site_legal_name
        ]
        if not site_customers:
            logger.warning("No customers found for site_legal_name=%r", site_legal_name)
            raise HTTPException(status_code=404, detail=f"No customers found for site legal name '{site_legal_name}'")

        logger.info(
            "Found %d customer(s) for site_legal_name=%r: %s",
            len(site_customers),
            site_legal_name,
            [customer.get("id") for customer in site_customers],
        )

        results = self._build_mrrs(site_customers, contracts, aggregates, fxrates)
        logger.info(
            "Computed MRR for %d of %d customer(s) for site_legal_name=%r",
            len(results),
            len(site_customers),
            site_legal_name,
        )
        return results

    async def get_arr_by_customer(self, customer_id: int):
        mrr = await self.get_mrr_by_customer(customer_id)
        return self._scale_arr(mrr)

    async def get_arr_all_customers(self):
        return [self._scale_arr(mrr) for mrr in await self.get_mrr_all_customers()]

    async def get_arr_by_customer_entity(self, legal_name: str):
        return [self._scale_arr(mrr) for mrr in await self.get_mrr_by_customer_entity(legal_name)]

    async def get_arr_by_site(self, site_legal_name: str):
        return [self._scale_arr(mrr) for mrr in await self.get_mrr_by_site(site_legal_name)]

    def _empty_monthly_totals(self) -> dict:
        zero = Decimal("0")
        return {
            "mrr_idr_original": zero,
            "mrr_usd_original": zero,
            "mrr_total_idr": zero,
            "mrr_total_usd": zero,
            "mrr_usd_converted_idr": zero,
            "arr_idr_original": zero,
            "arr_usd_original": zero,
            "arr_total_idr": zero,
            "arr_total_usd": zero,
            "arr_usd_converted_idr": zero,
        }

    def _usd_percentage(self, usd_converted_idr: Decimal, total_idr: Decimal) -> Decimal:
        if total_idr == 0:
            return Decimal("0")
        return (usd_converted_idr / total_idr) * Decimal("100")

    def _finalize_monthly_entry(self, month: date, totals: dict) -> dict:
        return {
            "year": month.year,
            "month": month.month,
            "mrr_idr_original": totals["mrr_idr_original"],
            "mrr_usd_original": totals["mrr_usd_original"],
            "mrr_total_idr": totals["mrr_total_idr"],
            "mrr_total_usd": totals["mrr_total_usd"],
            "mrr_usd_percentage": self._usd_percentage(
                totals["mrr_usd_converted_idr"], totals["mrr_total_idr"]
            ),
            "arr_idr_original": totals["arr_idr_original"],
            "arr_usd_original": totals["arr_usd_original"],
            "arr_total_idr": totals["arr_total_idr"],
            "arr_total_usd": totals["arr_total_usd"],
            "arr_usd_percentage": self._usd_percentage(
                totals["arr_usd_converted_idr"], totals["arr_total_idr"]
            ),
        }

    def _aggregate_mrr_arr_monthly(self, mrrs: list, target_month: Optional[date] = None) -> list:
        monthly_totals = {}

        for mrr in mrrs or []:
            currency = mrr.get("currency")
            for entry in mrr.get("monthly") or []:
                month = _to_date(entry.get("month"))
                if month is None:
                    continue
                if target_month is not None and (
                    month.year != target_month.year or month.month != target_month.month
                ):
                    continue

                month_key = month.isoformat()
                totals = monthly_totals.setdefault(month_key, self._empty_monthly_totals())

                amount_idr = entry.get("amount_idr") or Decimal("0")
                amount_usd = entry.get("amount_usd") or Decimal("0")

                if currency == "IDR":
                    totals["mrr_idr_original"] += amount_idr
                elif currency == "USD":
                    totals["mrr_usd_original"] += amount_usd
                    totals["mrr_usd_converted_idr"] += amount_idr

                totals["mrr_total_idr"] += amount_idr
                totals["mrr_total_usd"] += amount_usd

                totals["arr_idr_original"] += amount_idr * MONTHS_PER_YEAR
                totals["arr_usd_original"] += amount_usd * MONTHS_PER_YEAR
                totals["arr_total_idr"] += amount_idr * MONTHS_PER_YEAR
                totals["arr_total_usd"] += amount_usd * MONTHS_PER_YEAR
                if currency == "USD":
                    totals["arr_usd_converted_idr"] += amount_idr * MONTHS_PER_YEAR

        return [
            self._finalize_monthly_entry(_to_date(month_key), totals)
            for month_key, totals in sorted(monthly_totals.items())
        ]

    async def get_mrr_arr_monthly(self):
        mrrs = await self.get_mrr_all_customers()
        return self._aggregate_mrr_arr_monthly(mrrs)

    async def get_mrr_arr_current(self):
        mrrs = await self.get_mrr_all_customers()
        today = date.today()
        results = self._aggregate_mrr_arr_monthly(mrrs, target_month=today)
        if results:
            return results[0]
        return self._finalize_monthly_entry(today, self._empty_monthly_totals())


class FXRateManager:
    def __init__(self, fxrate: FXRateBase):
        self.fxrate = fxrate

    async def get_fxrates(self):
        return await get_fxrates_db()

    async def get_fxrate(self, fxrate_id: int):
        return await get_fxrate_db(fxrate_id)

    async def add_fxrate(self):
        return await add_fxrate_db(self.fxrate)

    async def update_fxrate(self, fxrate_id: int):
        return await update_fxrate_db(self.fxrate, fxrate_id)

    async def delete_fxrate(self, fxrate_id: int):
        return await delete_fxrate_db(fxrate_id)

    async def delete_fxrates(self):
        return await delete_fxrates_db()
