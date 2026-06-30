# app/treasury/managers.py

from app.treasury.schemas import (
    InvoiceBase,
    RevenueBase,
    ReceivableBase,
    FXRateBase
)
import calendar
from datetime import date
from decimal import Decimal
from fastapi import HTTPException
from app.customers.db import (
    get_contract_db,
    get_contract_by_customer_db,
    get_latest_aggregate_by_customer_db,
    get_aggregates_by_customer_db
)
from app.treasury.db import (
    get_invoices_db,
    get_invoice_db,
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
    get_fxrate_for_date_db,
    add_fxrate_db,
    update_fxrate_db,
    delete_fxrate_db,
    delete_fxrates_db
)

# Maps INVOICES fields to their RECEIVABLES/REVENUES counterparts so shared
# values stay in sync. booking_date is sourced differently per ledger:
# invoicing_date for receivables, payment_date for revenues.
RECEIVABLE_FIELD_MAP = {
    "invoicing_date": "booking_date",
    "currency": "currency",
    "fx_rate": "fx_rate",
    "total_usd": "amount_usd",
    "total_idr": "amount_idr",
}
REVENUE_FIELD_MAP = {
    "payment_date": "booking_date",
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
            currency=invoice.get("currency"),
            amount_usd=invoice.get("total_usd"),
            fx_rate=invoice.get("fx_rate"),
            amount_idr=invoice.get("total_idr"),
        )

    def _build_revenue(self, invoice: dict) -> RevenueBase:
        return RevenueBase(
            invoice_id=invoice.get("id"),
            booking_date=invoice.get("payment_date"),
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
        contract_result = await get_contract_db(contract_id)
        if not contract_result:
            raise HTTPException(status_code=404, detail=f"Contract {contract_id} not found")
        contract = contract_result[0]

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
            invoicing_date=invoicing_date,
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

    async def get_mrr_by_customer(self, customer_id: int):
        contract_result = await get_contract_by_customer_db(customer_id)
        if not contract_result:
            raise HTTPException(status_code=404, detail=f"No contract found for customer {customer_id}")
        contract = contract_result[0]

        start_date = _to_date(contract.get("start_date"))
        end_date = _to_date(contract.get("end_date"))
        if not start_date or not end_date:
            raise HTTPException(
                status_code=400,
                detail=f"Contract for customer {customer_id} is missing start_date or end_date",
            )

        aggregate_result = await get_aggregates_by_customer_db(customer_id)
        if not aggregate_result:
            raise HTTPException(status_code=404, detail=f"No aggregates found for customer {customer_id}")
        aggregates = sorted(aggregate_result, key=lambda a: _to_date(a.get("updated_at")))

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

            rate_result = await get_fxrate_for_date_db(month)
            if rate_result and rate_result[0].get("rate"):
                rate = Decimal(str(rate_result[0]["rate"]))
            else:
                rate = DEFAULT_RATE

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
            "currency": currency,
            "monthly": monthly,
            "total_usd": total_usd,
            "total_idr": total_idr,
        }

    async def get_arr_by_customer(self, customer_id: int):
        mrr = await self.get_mrr_by_customer(customer_id)

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
            "currency": mrr["currency"],
            "monthly": monthly,
            "total_usd": mrr["total_usd"] * MONTHS_PER_YEAR,
            "total_idr": mrr["total_idr"] * MONTHS_PER_YEAR,
        }


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
