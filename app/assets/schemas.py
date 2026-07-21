# app/assets/schemas.py

from pydantic import BaseModel
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
