# app/treasury/router.py

from datetime import date
from typing import Optional
from decimal import Decimal
from fastapi import APIRouter
from app.treasury.managers import (
    InvoiceManager
)
from app.treasury.schemas import (
    InvoiceBase
)

router = APIRouter(prefix="/treasury")

# Financial KPI Routers

@router.get("/financial_kpis", tags=["Financial KPIs"])
async def get_financial_kpis():
    pass

# Invoice Routers

@router.patch("/mark_invoice_paid/{invoice_id}", tags=["Extended Invoices"])
async def mark_invoice_paid(invoice_id: int, payment_date: Optional[date] = None):
    try:
        manager = InvoiceManager(None)
        return await manager.mark_invoice_paid(invoice_id, payment_date or date.today())
    except Exception as e:
        raise e

@router.post("/generate_invoice", tags=["Extended Invoices"])
async def generate_invoice(contract_id: int, fx_rate: Optional[Decimal] = None, invoicing_date: Optional[date] = None):
    try:
        manager = InvoiceManager(None)
        return await manager.generate_invoice(contract_id, fx_rate, invoicing_date or date.today())
    except Exception as e:
        raise e

@router.get("/invoices", tags=["Basic Invoices"])
async def get_invoices():
    try:
        manager = InvoiceManager(None)
        return await manager.get_invoices()
    except Exception as e:
        raise e

@router.get("/invoices/{invoice_id}", tags=["Basic Invoices"])
async def get_invoice(invoice_id: int):
    try:
        manager = InvoiceManager(None)
        return await manager.get_invoice(invoice_id)
    except Exception as e:
        raise e

@router.post("/add_invoice", tags=["Basic Invoices"])
async def add_invoice(invoice: InvoiceBase):
    try:
        manager = InvoiceManager(invoice)
        return await manager.add_invoice()
    except Exception as e:
        raise e

@router.patch("/update_invoice/{invoice_id}", tags=["Basic Invoices"])
async def update_invoice(invoice_id: int, invoice: InvoiceBase):
    try:
        manager = InvoiceManager(invoice)
        return await manager.update_invoice(invoice_id)
    except Exception as e:
        raise e

@router.delete("/delete_invoice/{invoice_id}", tags=["Basic Invoices"])
async def delete_invoice(invoice_id: int):
    try:
        manager = InvoiceManager(None)
        return await manager.delete_invoice(invoice_id)
    except Exception as e:
        raise e

@router.delete("/delete_invoices", tags=["Basic Invoices"])
async def delete_invoices():
    try:
        manager = InvoiceManager(None)
        return await manager.delete_invoices()
    except Exception as e:
        raise e
