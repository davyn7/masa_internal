# app/assets/db.py

from typing import Optional
from app.connection import supabase
from app.assets.schemas import MakeBase, ModelBase

async def get_makes_db():
    response = supabase.table("MAKES").select("*").execute()
    return response.data

async def get_make_db(make_id: int):
    response = supabase.table("MAKES").select("*").eq("id", make_id).execute()
    return response.data

async def get_make_by_name_db(name: str):
    response = supabase.table("MAKES").select("*").eq("name", name).execute()
    return response.data

async def add_make_db(make: MakeBase):
    make_data = make.model_dump(mode="json")
    response = supabase.table("MAKES").insert(make_data).execute()
    return response.data

async def update_make_db(make: MakeBase, make_id: int):
    make_data = make.model_dump(exclude_unset=True, mode="json")
    response = supabase.table("MAKES").update(make_data).eq("id", make_id).execute()
    return response.data

async def delete_make_db(make_id: int):
    response = supabase.table("MAKES").delete().eq("id", make_id).execute()
    return response.data

async def delete_makes_db():
    response = supabase.table("MAKES").delete().neq("id", 0).execute()
    return response.data

async def get_models_db(make_id: Optional[int] = None):
    query = supabase.table("MODELS").select("*")
    if make_id is not None:
        query = query.eq("make_id", make_id)
    response = query.execute()
    return response.data

async def get_model_db(model_id: int):
    response = supabase.table("MODELS").select("*").eq("id", model_id).execute()
    return response.data

async def get_model_by_make_and_name_db(make_id: int, name: str):
    response = (
        supabase.table("MODELS")
        .select("*")
        .eq("make_id", make_id)
        .eq("name", name)
        .execute()
    )
    return response.data

async def add_model_db(model: ModelBase):
    model_data = model.model_dump(mode="json")
    response = supabase.table("MODELS").insert(model_data).execute()
    return response.data

async def update_model_db(model: ModelBase, model_id: int):
    model_data = model.model_dump(exclude_unset=True, mode="json")
    response = supabase.table("MODELS").update(model_data).eq("id", model_id).execute()
    return response.data

async def delete_model_db(model_id: int):
    response = supabase.table("MODELS").delete().eq("id", model_id).execute()
    return response.data

async def delete_models_db():
    response = supabase.table("MODELS").delete().neq("id", 0).execute()
    return response.data
