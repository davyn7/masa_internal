# app/treasury/db.py

from datetime import date
from app.connection import supabase
from app.treasury.schemas import (
    InvoiceBase
)

async def get_invoices_db():
    response = supabase.table("INVOICES").select("*").execute()
    return response.data

async def get_invoice_db(invoice_id: int):
    response = supabase.table("INVOICES").select("*").eq("id", invoice_id).execute()
    return response.data

async def add_invoice_db(invoice: InvoiceBase):
    invoice_data = invoice.model_dump(mode="json")
    response = supabase.table("INVOICES").insert(invoice_data).execute()
    return response.data

async def update_invoice_db(invoice: InvoiceBase, invoice_id: int):
    invoice_data = invoice.model_dump(exclude_unset=True, mode="json")
    response = supabase.table("INVOICES").update(invoice_data).eq("id", invoice_id).execute()
    return response.data

async def delete_invoice_db(invoice_id: int):
    response = supabase.table("INVOICES").delete().eq("id", invoice_id).execute()
    return response.data

async def delete_invoices_db():
    response = supabase.table("INVOICES").delete().neq("id", 0).execute()
    return response.data

async def mark_invoice_paid_db(invoice_id: int, payment_date: date):
    invoice_data = {"is_paid": True, "payment_date": payment_date.isoformat()}
    response = supabase.table("INVOICES").update(invoice_data).eq("id", invoice_id).execute()
    return response.data
