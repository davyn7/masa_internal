# app/customers/router.py

from fastapi import APIRouter
from app.customers.managers import (
    CustomerManager,
    ContractManager,
    AggregateManager,
    InvoiceManager
)
from app.customers.schemas import (
    CustomerBase,
    ContractBase,
    AggregateBase,
    InvoiceBase
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

# Invoice Routers

@router.get("/invoices", tags=["Basic Invoices"])
async def get_invoices():
    try:
        manager = InvoiceManager(None)
        return await manager.get_invoices()
    except Exception as e:
        raise e

@router.get("/invoices/{invoice_id}", tags=["Basic Invoices"])
async def get_invoice(invoice_id: int):
    try:
        manager = InvoiceManager(None)
        return await manager.get_invoice(invoice_id)
    except Exception as e:
        raise e

@router.post("/add_invoice", tags=["Basic Invoices"])
async def add_invoice(invoice: InvoiceBase):
    try:
        manager = InvoiceManager(invoice)
        return await manager.add_invoice()
    except Exception as e:
        raise e

@router.patch("/update_invoice/{invoice_id}", tags=["Basic Invoices"])
async def update_invoice(invoice_id: int, invoice: InvoiceBase):
    try:
        manager = InvoiceManager(invoice)
        return await manager.update_invoice(invoice_id)
    except Exception as e:
        raise e

@router.delete("/delete_invoice/{invoice_id}", tags=["Basic Invoices"])
async def delete_invoice(invoice_id: int):
    try:
        manager = InvoiceManager(None)
        return await manager.delete_invoice(invoice_id)
    except Exception as e:
        raise e

@router.delete("/delete_invoices", tags=["Basic Invoices"])
async def delete_invoices():
    try:
        manager = InvoiceManager(None)
        return await manager.delete_invoices()
    except Exception as e:
        raise e
