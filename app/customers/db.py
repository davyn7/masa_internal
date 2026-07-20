# app/customers/db.py

from datetime import date
from app.connection import supabase
from app.customers.schemas import (
    CustomerBase,
    ContractBase,
    AggregateBase,
    EquipmentBase
)

async def get_customers_db():
    response = supabase.table("CUSTOMERS").select("*").execute()
    return response.data

async def get_customer_db(customer_id: int):
    response = supabase.table("CUSTOMERS").select("*").eq("id", customer_id).execute()
    return response.data

async def add_customer_db(customer: CustomerBase):
    customer_data = customer.model_dump(mode="json")
    response = supabase.table("CUSTOMERS").insert(customer_data).execute()
    return response.data

async def update_customer_db(customer: CustomerBase, customer_id: int):
    customer_data = customer.model_dump(exclude_unset=True, mode="json")
    response = supabase.table("CUSTOMERS").update(customer_data).eq("id", customer_id).execute()
    return response.data

async def delete_customer_db(customer_id: int):
    response = supabase.table("CUSTOMERS").delete().eq("id", customer_id).execute()
    return response.data

async def delete_customers_db():
    response = supabase.table("CUSTOMERS").delete().neq("id", 0).execute()
    return response.data

async def get_contracts_db():
    response = supabase.table("CONTRACTS").select("*").execute()
    return response.data

async def get_contract_db(contract_id: int):
    response = supabase.table("CONTRACTS").select("*").eq("id", contract_id).execute()
    return response.data

async def get_contract_by_customer_db(customer_id: int):
    response = supabase.table("CONTRACTS").select("*").eq("customer_id", customer_id).execute()
    return response.data

async def add_contract_db(contract: ContractBase):
    contract_data = contract.model_dump(mode="json")
    response = supabase.table("CONTRACTS").insert(contract_data).execute()
    return response.data

async def update_contract_db(contract: ContractBase, contract_id: int):
    contract_data = contract.model_dump(exclude_unset=True, mode="json")
    response = supabase.table("CONTRACTS").update(contract_data).eq("id", contract_id).execute()
    return response.data

async def delete_contract_db(contract_id: int):
    response = supabase.table("CONTRACTS").delete().eq("id", contract_id).execute()
    return response.data

async def delete_contracts_db():
    response = supabase.table("CONTRACTS").delete().neq("id", 0).execute()
    return response.data

async def get_aggregates_db():
    response = supabase.table("AGGREGATES").select("*").execute()
    return response.data

async def get_aggregate_db(aggregate_id: int):
    response = supabase.table("AGGREGATES").select("*").eq("id", aggregate_id).execute()
    return response.data

async def get_aggregates_by_customer_db(customer_id: int):
    response = (
        supabase.table("AGGREGATES")
        .select("*")
        .eq("customer_id", customer_id)
        .order("updated_at", desc=False)
        .execute()
    )
    return response.data

async def get_latest_aggregate_by_customer_db(customer_id: int, before_date: date):
    response = (
        supabase.table("AGGREGATES")
        .select("*")
        .eq("customer_id", customer_id)
        .lte("updated_at", before_date.isoformat())
        .order("updated_at", desc=True)
        .limit(1)
        .execute()
    )
    return response.data

async def add_aggregate_db(aggregate: AggregateBase):
    aggregate_data = aggregate.model_dump(mode="json")
    response = supabase.table("AGGREGATES").insert(aggregate_data).execute()
    return response.data

async def update_aggregate_db(aggregate: AggregateBase, aggregate_id: int):
    aggregate_data = aggregate.model_dump(exclude_unset=True, mode="json")
    response = supabase.table("AGGREGATES").update(aggregate_data).eq("id", aggregate_id).execute()
    return response.data

async def delete_aggregate_db(aggregate_id: int):
    response = supabase.table("AGGREGATES").delete().eq("id", aggregate_id).execute()
    return response.data

async def delete_aggregates_db():
    response = supabase.table("AGGREGATES").delete().neq("id", 0).execute()
    return response.data

async def get_equipments_db():
    response = supabase.table("EQUIPMENTS").select("*").execute()
    return response.data

async def get_equipment_db(equipment_id: int):
    response = supabase.table("EQUIPMENTS").select("*").eq("id", equipment_id).execute()
    return response.data

async def add_equipment_db(equipment: EquipmentBase):
    equipment_data = equipment.model_dump(mode="json")
    response = supabase.table("EQUIPMENTS").insert(equipment_data).execute()
    return response.data

async def update_equipment_db(equipment: EquipmentBase, equipment_id: int):
    equipment_data = equipment.model_dump(exclude_unset=True, mode="json")
    response = supabase.table("EQUIPMENTS").update(equipment_data).eq("id", equipment_id).execute()
    return response.data

async def delete_equipment_db(equipment_id: int):
    response = supabase.table("EQUIPMENTS").delete().eq("id", equipment_id).execute()
    return response.data

async def delete_equipments_db():
    response = supabase.table("EQUIPMENTS").delete().neq("id", 0).execute()
    return response.data
