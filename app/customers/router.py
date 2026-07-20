# app/customers/router.py

from fastapi import APIRouter
from app.customers.managers import (
    CustomerManager,
    ContractManager,
    AggregateManager,
    EquipmentManager
)
from app.customers.schemas import (
    CustomerBase,
    ContractBase,
    AggregateBase,
    EquipmentBase
)

router = APIRouter(prefix="/customers")

# Customer Routers

@router.get("/customers", tags=["Basic Customers"])
async def get_customers():
    try:
        manager = CustomerManager(None)
        return await manager.get_customers()
    except Exception as e:
        raise e

@router.get("/customers/{customer_id}", tags=["Basic Customers"])
async def get_customer(customer_id: int):
    try:
        manager = CustomerManager(None)
        return await manager.get_customer(customer_id)
    except Exception as e:
        raise e

@router.post("/add_customer", tags=["Basic Customers"])
async def add_customer(customer: CustomerBase):
    try:
        manager = CustomerManager(customer)
        return await manager.add_customer()
    except Exception as e:
        raise e

@router.patch("/update_customer/{customer_id}", tags=["Basic Customers"])
async def update_customer(customer_id: int, customer: CustomerBase):
    try:
        manager = CustomerManager(customer)
        return await manager.update_customer(customer_id)
    except Exception as e:
        raise e

@router.delete("/delete_customer/{customer_id}", tags=["Basic Customers"])
async def delete_customer(customer_id: int):
    try:
        manager = CustomerManager(None)
        return await manager.delete_customer(customer_id)
    except Exception as e:
        raise e

@router.delete("/delete_customers", tags=["Basic Customers"])
async def delete_customers():
    try:
        manager = CustomerManager(None)
        return await manager.delete_customers()
    except Exception as e:
        raise e

# Contract Routers

@router.get("/contracts", tags=["Basic Contracts"])
async def get_contracts():
    try:
        manager = ContractManager(None)
        return await manager.get_contracts()
    except Exception as e:
        raise e

@router.get("/contracts/{contract_id}", tags=["Basic Contracts"])
async def get_contract(contract_id: int):
    try:
        manager = ContractManager(None)
        return await manager.get_contract(contract_id)
    except Exception as e:
        raise e

@router.post("/add_contract", tags=["Basic Contracts"])
async def add_contract(contract: ContractBase):
    try:
        manager = ContractManager(contract)
        return await manager.add_contract()
    except Exception as e:
        raise e

@router.patch("/update_contract/{contract_id}", tags=["Basic Contracts"])
async def update_contract(contract_id: int, contract: ContractBase):
    try:
        manager = ContractManager(contract)
        return await manager.update_contract(contract_id)
    except Exception as e:
        raise e

@router.delete("/delete_contract/{contract_id}", tags=["Basic Contracts"])
async def delete_contract(contract_id: int):
    try:
        manager = ContractManager(None)
        return await manager.delete_contract(contract_id)
    except Exception as e:
        raise e

@router.delete("/delete_contracts", tags=["Basic Contracts"])
async def delete_contracts():
    try:
        manager = ContractManager(None)
        return await manager.delete_contracts()
    except Exception as e:
        raise e

# Aggregate Routers

@router.get("/aggregates", tags=["Basic Aggregates"])
async def get_aggregates():
    try:
        manager = AggregateManager(None)
        return await manager.get_aggregates()
    except Exception as e:
        raise e

@router.get("/aggregates/{aggregate_id}", tags=["Basic Aggregates"])
async def get_aggregate(aggregate_id: int):
    try:
        manager = AggregateManager(None)
        return await manager.get_aggregate(aggregate_id)
    except Exception as e:
        raise e

@router.post("/add_aggregate", tags=["Basic Aggregates"])
async def add_aggregate(aggregate: AggregateBase):
    try:
        manager = AggregateManager(aggregate)
        return await manager.add_aggregate()
    except Exception as e:
        raise e

@router.patch("/update_aggregate/{aggregate_id}", tags=["Basic Aggregates"])
async def update_aggregate(aggregate_id: int, aggregate: AggregateBase):
    try:
        manager = AggregateManager(aggregate)
        return await manager.update_aggregate(aggregate_id)
    except Exception as e:
        raise e

@router.delete("/delete_aggregate/{aggregate_id}", tags=["Basic Aggregates"])
async def delete_aggregate(aggregate_id: int):
    try:
        manager = AggregateManager(None)
        return await manager.delete_aggregate(aggregate_id)
    except Exception as e:
        raise e

@router.delete("/delete_aggregates", tags=["Basic Aggregates"])
async def delete_aggregates():
    try:
        manager = AggregateManager(None)
        return await manager.delete_aggregates()
    except Exception as e:
        raise e

# Equipment Routers

@router.get("/equipments", tags=["Basic Equipments"])
async def get_equipments():
    try:
        manager = EquipmentManager(None)
        return await manager.get_equipments()
    except Exception as e:
        raise e

@router.get("/equipments/{equipment_id}", tags=["Basic Equipments"])
async def get_equipment(equipment_id: int):
    try:
        manager = EquipmentManager(None)
        return await manager.get_equipment(equipment_id)
    except Exception as e:
        raise e

@router.post("/add_equipment", tags=["Basic Equipments"])
async def add_equipment(equipment: EquipmentBase):
    try:
        manager = EquipmentManager(equipment)
        return await manager.add_equipment()
    except Exception as e:
        raise e

@router.patch("/update_equipment/{equipment_id}", tags=["Basic Equipments"])
async def update_equipment(equipment_id: int, equipment: EquipmentBase):
    try:
        manager = EquipmentManager(equipment)
        return await manager.update_equipment(equipment_id)
    except Exception as e:
        raise e

@router.delete("/delete_equipment/{equipment_id}", tags=["Basic Equipments"])
async def delete_equipment(equipment_id: int):
    try:
        manager = EquipmentManager(None)
        return await manager.delete_equipment(equipment_id)
    except Exception as e:
        raise e

@router.delete("/delete_equipments", tags=["Basic Equipments"])
async def delete_equipments():
    try:
        manager = EquipmentManager(None)
        return await manager.delete_equipments()
    except Exception as e:
        raise e
