# app/assets/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional, Literal

VehicleType = Literal[
    "dt",
    "exca",
    "lv",
    "dozer",
    "grader",
    "water_truck",
    "fuel_truck",
    "manhauler",
]

class MakeBase(BaseModel):
    name: Optional[str] = None

class ModelBase(BaseModel):
    make_id: Optional[int] = None
    name: Optional[str] = None
    vehicle_type: Optional[VehicleType] = None

class AssetBase(BaseModel):
    customer_id: Optional[int] = None
    model_id: Optional[int] = None
    unit_identifier: Optional[str] = None
    is_on_site: Optional[bool] = True
    device_installed: Optional[bool] = False
    installed_at: Optional[date] = None
    removed_at: Optional[date] = None
    notes: Optional[str] = None
