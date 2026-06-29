from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client
from app.tests.router import router as tests_router
from app.customers.router import router as customers_router

load_dotenv()

app = FastAPI()

app.include_router(tests_router)
app.include_router(customers_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}