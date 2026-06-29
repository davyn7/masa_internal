# app/customers/managers.py

from app.customers.schemas import (
    CustomerBase
)
from app.customers.db import (
    get_customers_db,
    get_customer_db,
    add_customer_db,
    update_customer_db,
    delete_customer_db,
    delete_customers_db
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
