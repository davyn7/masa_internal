# app/treasury/schemas.py

from pydantic import BaseModel
from decimal import Decimal
from enum import Enum
from datetime import date
from typing import Optional, List

class InvoiceBase(BaseModel):
    contract_id: Optional[int] = None
    invoice_number: Optional[str] = None
    invoicing_date: Optional[date] = None
    due_date: Optional[date] = None
    is_paid: Optional[bool] = False
    payment_date: Optional[date] = None
    currency: Optional[str] = None
    fx_rate: Optional[Decimal] = None
    pretax_usd: Optional[Decimal] = None
    vat_usd: Optional[Decimal] = None
    total_usd: Optional[Decimal] = None
    pretax_idr: Optional[Decimal] = None
    vat_idr: Optional[Decimal] = None
    total_idr: Optional[Decimal] = None
