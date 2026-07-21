# app/assets/router.py

from typing import Optional
from fastapi import APIRouter, Query
from app.assets.managers import MakeManager, ModelManager
from app.assets.schemas import MakeBase, ModelBase

router = APIRouter(prefix="/assets")

# Make Routers

@router.get("/makes", tags=["Basic Makes"])
async def get_makes():
    try:
        manager = MakeManager(None)
        return await manager.get_makes()
    except Exception as e:
        raise e

@router.get("/makes/{make_id}", tags=["Basic Makes"])
async def get_make(make_id: int):
    try:
        manager = MakeManager(None)
        return await manager.get_make(make_id)
    except Exception as e:
        raise e

@router.post("/add_make", tags=["Basic Makes"])
async def add_make(make: MakeBase):
    try:
        manager = MakeManager(make)
        return await manager.add_make()
    except Exception as e:
        raise e

@router.patch("/update_make/{make_id}", tags=["Basic Makes"])
async def update_make(make_id: int, make: MakeBase):
    try:
        manager = MakeManager(make)
        return await manager.update_make(make_id)
    except Exception as e:
        raise e

@router.delete("/delete_make/{make_id}", tags=["Basic Makes"])
async def delete_make(make_id: int):
    try:
        manager = MakeManager(None)
        return await manager.delete_make(make_id)
    except Exception as e:
        raise e

@router.delete("/delete_makes", tags=["Basic Makes"])
async def delete_makes():
    try:
        manager = MakeManager(None)
        return await manager.delete_makes()
    except Exception as e:
        raise e

# Model Routers

@router.get("/models", tags=["Basic Models"])
async def get_models(make_id: Optional[int] = Query(None)):
    try:
        manager = ModelManager(None)
        return await manager.get_models(make_id)
    except Exception as e:
        raise e

@router.get("/models/{model_id}", tags=["Basic Models"])
async def get_model(model_id: int):
    try:
        manager = ModelManager(None)
        return await manager.get_model(model_id)
    except Exception as e:
        raise e

@router.post("/add_model", tags=["Basic Models"])
async def add_model(model: ModelBase):
    try:
        manager = ModelManager(model)
        return await manager.add_model()
    except Exception as e:
        raise e

@router.patch("/update_model/{model_id}", tags=["Basic Models"])
async def update_model(model_id: int, model: ModelBase):
    try:
        manager = ModelManager(model)
        return await manager.update_model(model_id)
    except Exception as e:
        raise e

@router.delete("/delete_model/{model_id}", tags=["Basic Models"])
async def delete_model(model_id: int):
    try:
        manager = ModelManager(None)
        return await manager.delete_model(model_id)
    except Exception as e:
        raise e

@router.delete("/delete_models", tags=["Basic Models"])
async def delete_models():
    try:
        manager = ModelManager(None)
        return await manager.delete_models()
    except Exception as e:
        raise e
