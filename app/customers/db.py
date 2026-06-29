# app/customers/db.py

from app.connection import supabase
from app.customers.schemas import (
    CustomerBase,
    ContractBase,
    AggregateBase,
    InvoiceBase
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

async def get_invoices_db():
    response = supabase.table("INVOICES").select("*").execute()
    return response.data

async def get_invoice_db(invoice_id: int):
    response = supabase.table("INVOICES").select("*").eq("id", invoice_id).execute()
    return response.data

async def add_invoice_db(invoice: InvoiceBase):
    invoice_data = invoice.model_dump(mode="json")
    response = supabase.table("INVOICES").insert(invoice_data).execute()
    return response.data

async def update_invoice_db(invoice: InvoiceBase, invoice_id: int):
    invoice_data = invoice.model_dump(exclude_unset=True, mode="json")
    response = supabase.table("INVOICES").update(invoice_data).eq("id", invoice_id).execute()
    return response.data

async def delete_invoice_db(invoice_id: int):
    response = supabase.table("INVOICES").delete().eq("id", invoice_id).execute()
    return response.data

async def delete_invoices_db():
    response = supabase.table("INVOICES").delete().neq("id", 0).execute()
    return response.data
