# app/customers/db.py

from app.connection import supabase
from app.customers.schemas import (
    CustomerBase
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
