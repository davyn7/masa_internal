# app/customers/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class CustomerBase(BaseModel):
    name: Optional[str] = None
    legal_name: Optional[str] = None
    npwp: Optional[str] = None
    address: Optional[str] = None
    customer_type: Optional[str] = None
    site_name: Optional[str] = None
    site_legal_name: Optional[str] = None
    site_address: Optional[str] = None
    resource: Optional[str] = None
    pic_id: Optional[int] = None