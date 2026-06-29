# app/treasury/managers.py

from app.treasury.schemas import (
    InvoiceBase,
    RevenueBase,
    ReceivableBase
)
from datetime import date
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
    update_revenue_by_invoice_db
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
