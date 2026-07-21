import logging
from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client
from app.customers.router import router as customers_router
from app.assets.router import router as assets_router
from app.treasury.router import router as treasury_router

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(customers_router)
app.include_router(assets_router)
app.include_router(treasury_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}