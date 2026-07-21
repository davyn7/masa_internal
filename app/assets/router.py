# app/assets/router.py

from typing import Optional
from fastapi import APIRouter, Query
from app.assets.managers import MakeManager, ModelManager, AssetManager
from app.assets.schemas import MakeBase, ModelBase, AssetBase

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

@router.get("/all_models", tags=["Basic Models"])
async def get_all_models():
    try:
        manager = ModelManager(None)
        return await manager.get_all_models()
    except Exception as e:
        raise e

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

# Asset Routers

@router.get("/assets", tags=["Basic Assets"])
async def get_assets(customer_id: Optional[int] = Query(None)):
    try:
        manager = AssetManager(None)
        return await manager.get_assets(customer_id)
    except Exception as e:
        raise e

@router.get("/assets/{asset_id}", tags=["Basic Assets"])
async def get_asset(asset_id: int):
    try:
        manager = AssetManager(None)
        return await manager.get_asset(asset_id)
    except Exception as e:
        raise e

@router.post("/add_asset", tags=["Basic Assets"])
async def add_asset(asset: AssetBase):
    try:
        manager = AssetManager(asset)
        return await manager.add_asset()
    except Exception as e:
        raise e

@router.patch("/update_asset/{asset_id}", tags=["Basic Assets"])
async def update_asset(asset_id: int, asset: AssetBase):
    try:
        manager = AssetManager(asset)
        return await manager.update_asset(asset_id)
    except Exception as e:
        raise e

@router.delete("/delete_asset/{asset_id}", tags=["Basic Assets"])
async def delete_asset(asset_id: int):
    try:
        manager = AssetManager(None)
        return await manager.delete_asset(asset_id)
    except Exception as e:
        raise e

@router.delete("/delete_assets", tags=["Basic Assets"])
async def delete_assets():
    try:
        manager = AssetManager(None)
        return await manager.delete_assets()
    except Exception as e:
        raise e
