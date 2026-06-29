# app/treasury/db.py

from datetime import date
from app.connection import supabase
from app.treasury.schemas import (
    InvoiceBase,
    RevenueBase,
    ReceivableBase
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

async def add_receivable_db(receivable: ReceivableBase):
    receivable_data = receivable.model_dump(mode="json")
    response = supabase.table("RECEIVABLES").insert(receivable_data).execute()
    return response.data

async def delete_receivable_by_invoice_db(invoice_id: int):
    response = supabase.table("RECEIVABLES").delete().eq("invoice_id", invoice_id).execute()
    return response.data

async def delete_receivables_db():
    response = supabase.table("RECEIVABLES").delete().neq("id", 0).execute()
    return response.data

async def add_revenue_db(revenue: RevenueBase):
    revenue_data = revenue.model_dump(mode="json")
    response = supabase.table("REVENUES").insert(revenue_data).execute()
    return response.data

async def delete_revenue_by_invoice_db(invoice_id: int):
    response = supabase.table("REVENUES").delete().eq("invoice_id", invoice_id).execute()
    return response.data

async def delete_revenues_db():
    response = supabase.table("REVENUES").delete().neq("id", 0).execute()
    return response.data

async def update_receivable_by_invoice_db(invoice_id: int, receivable_data: dict):
    response = supabase.table("RECEIVABLES").update(receivable_data).eq("invoice_id", invoice_id).execute()
    return response.data

async def update_revenue_by_invoice_db(invoice_id: int, revenue_data: dict):
    response = supabase.table("REVENUES").update(revenue_data).eq("invoice_id", invoice_id).execute()
    return response.data
