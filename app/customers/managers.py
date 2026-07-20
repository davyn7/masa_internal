# app/customers/managers.py

from app.customers.schemas import (
    CustomerBase,
    ContractBase,
    AggregateBase,
    EquipmentBase
)
from app.customers.db import (
    get_customers_db,
    get_customer_db,
    add_customer_db,
    update_customer_db,
    delete_customer_db,
    delete_customers_db,
    get_contracts_db,
    get_contract_db,
    add_contract_db,
    update_contract_db,
    delete_contract_db,
    delete_contracts_db,
    get_aggregates_db,
    get_aggregate_db,
    add_aggregate_db,
    update_aggregate_db,
    delete_aggregate_db,
    delete_aggregates_db,
    get_equipments_db,
    get_equipment_db,
    add_equipment_db,
    update_equipment_db,
    delete_equipment_db,
    delete_equipments_db
)

class CustomerManager:
    def __init__(self, customer: CustomerBase):
        self.customer = customer

    async def get_customers(self):
        return await get_customers_db()

    async def get_customer(self, customer_id: int):
        return await get_customer_db(customer_id)

    async def add_customer(self):
        return await add_customer_db(self.customer)

    async def update_customer(self, customer_id: int):
        return await update_customer_db(self.customer, customer_id)

    async def delete_customer(self, customer_id: int):
        return await delete_customer_db(customer_id)

    async def delete_customers(self):
        return await delete_customers_db()

class ContractManager:
    def __init__(self, contract: ContractBase):
        self.contract = contract

    async def get_contracts(self):
        return await get_contracts_db()

    async def get_contract(self, contract_id: int):
        return await get_contract_db(contract_id)

    async def add_contract(self):
        return await add_contract_db(self.contract)

    async def update_contract(self, contract_id: int):
        return await update_contract_db(self.contract, contract_id)

    async def delete_contract(self, contract_id: int):
        return await delete_contract_db(contract_id)

    async def delete_contracts(self):
        return await delete_contracts_db()

class AggregateManager:
    def __init__(self, aggregate: AggregateBase):
        self.aggregate = aggregate

    async def get_aggregates(self):
        return await get_aggregates_db()

    async def get_aggregate(self, aggregate_id: int):
        return await get_aggregate_db(aggregate_id)

    async def add_aggregate(self):
        return await add_aggregate_db(self.aggregate)

    async def update_aggregate(self, aggregate_id: int):
        return await update_aggregate_db(self.aggregate, aggregate_id)

    async def delete_aggregate(self, aggregate_id: int):
        return await delete_aggregate_db(aggregate_id)

    async def delete_aggregates(self):
        return await delete_aggregates_db()

class EquipmentManager:
    def __init__(self, equipment: EquipmentBase):
        self.equipment = equipment

    async def get_equipments(self):
        return await get_equipments_db()

    async def get_equipment(self, equipment_id: int):
        return await get_equipment_db(equipment_id)

    async def add_equipment(self):
        return await add_equipment_db(self.equipment)

    async def update_equipment(self, equipment_id: int):
        return await update_equipment_db(self.equipment, equipment_id)

    async def delete_equipment(self, equipment_id: int):
        return await delete_equipment_db(equipment_id)

    async def delete_equipments(self):
        return await delete_equipments_db()
