# app/treasury/managers.py

from app.treasury.schemas import (
    InvoiceBase
)
from app.treasury.db import (
    get_invoices_db,
    get_invoice_db,
    add_invoice_db,
    update_invoice_db,
    delete_invoice_db,
    delete_invoices_db
)

class InvoiceManager:
    def __init__(self, invoice: InvoiceBase):
        self.invoice = invoice

    async def get_invoices(self):
        return await get_invoices_db()

    async def get_invoice(self, invoice_id: int):
        return await get_invoice_db(invoice_id)

    async def add_invoice(self):
        return await add_invoice_db(self.invoice)

    async def update_invoice(self, invoice_id: int):
        return await update_invoice_db(self.invoice, invoice_id)

    async def delete_invoice(self, invoice_id: int):
        return await delete_invoice_db(invoice_id)

    async def delete_invoices(self):
        return await delete_invoices_db()
