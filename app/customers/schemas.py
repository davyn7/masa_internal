# app/customers/schemas.py

from pydantic import BaseModel
from decimal import Decimal
from enum import Enum
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

class ContractBase(BaseModel):
    customer_id: Optional[int] = None
    contract_number: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    currency: Optional[str] = None
    price_dt: Optional[Decimal] = None
    price_exca: Optional[Decimal] = None
    price_lv: Optional[Decimal] = None
    price_dozer: Optional[Decimal] = None
    price_grader: Optional[Decimal] = None
    price_water_truck: Optional[Decimal] = None
    price_fuel_truck: Optional[Decimal] = None
    price_manhauler: Optional[Decimal] = None

class AggregateBase(BaseModel):
    customer_id: Optional[int] = None
    dt: Optional[int] = None
    exca: Optional[int] = None
    lv: Optional[int] = None
    dozer: Optional[int] = None
    grader: Optional[int] = None
    water_truck: Optional[int] = None
    fuel_truck: Optional[int] = None
    manhauler: Optional[int] = None