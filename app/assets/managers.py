# app/assets/managers.py

from typing import Optional
from fastapi import HTTPException
from app.assets.schemas import MakeBase, ModelBase, AssetBase
from app.assets.db import (
    get_makes_db,
    get_make_db,
    get_make_by_name_db,
    add_make_db,
    update_make_db,
    delete_make_db,
    delete_makes_db,
    get_models_db,
    get_all_models_db,
    get_model_db,
    get_model_by_make_and_name_db,
    add_model_db,
    update_model_db,
    delete_model_db,
    delete_models_db,
    get_assets_db,
    get_asset_db,
    add_asset_db,
    update_asset_db,
    delete_asset_db,
    delete_assets_db,
)

def _validate_device_on_site(
    is_on_site: Optional[bool],
    device_installed: Optional[bool],
    existing: Optional[dict] = None,
):
    resolved_on_site = (
        is_on_site
        if is_on_site is not None
        else existing.get("is_on_site", True) if existing else True
    )
    resolved_installed = (
        device_installed
        if device_installed is not None
        else existing.get("device_installed", False) if existing else False
    )
    if resolved_installed and not resolved_on_site:
        raise HTTPException(
            status_code=400,
            detail="device_installed requires is_on_site to be true",
        )

class MakeManager:
    def __init__(self, make: MakeBase):
        self.make = make

    async def get_makes(self):
        return await get_makes_db()

    async def get_make(self, make_id: int):
        return await get_make_db(make_id)

    async def add_make(self):
        if self.make.name:
            existing = await get_make_by_name_db(self.make.name)
            if existing:
                raise HTTPException(
                    status_code=409,
                    detail=f"Make '{self.make.name}' already exists",
                )
        return await add_make_db(self.make)

    async def update_make(self, make_id: int):
        return await update_make_db(self.make, make_id)

    async def delete_make(self, make_id: int):
        return await delete_make_db(make_id)

    async def delete_makes(self):
        return await delete_makes_db()

class ModelManager:
    def __init__(self, model: ModelBase):
        self.model = model

    async def get_models(self, make_id: Optional[int] = None):
        return await get_models_db(make_id)

    async def get_all_models(self):
        return await get_all_models_db()

    async def get_model(self, model_id: int):
        return await get_model_db(model_id)

    async def add_model(self):
        if self.model.name and self.model.make_id is not None:
            existing = await get_model_by_make_and_name_db(
                self.model.make_id, self.model.name
            )
            if existing:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"Model '{self.model.name}' already exists "
                        f"for make {self.model.make_id}"
                    ),
                )
        return await add_model_db(self.model)

    async def update_model(self, model_id: int):
        return await update_model_db(self.model, model_id)

    async def delete_model(self, model_id: int):
        return await delete_model_db(model_id)

    async def delete_models(self):
        return await delete_models_db()

class AssetManager:
    def __init__(self, asset: AssetBase):
        self.asset = asset

    async def get_assets(self, customer_id: Optional[int] = None):
        return await get_assets_db(customer_id)

    async def get_asset(self, asset_id: int):
        return await get_asset_db(asset_id)

    async def add_asset(self):
        _validate_device_on_site(self.asset.is_on_site, self.asset.device_installed)
        return await add_asset_db(self.asset)

    async def update_asset(self, asset_id: int):
        existing_result = await get_asset_db(asset_id)
        existing = existing_result[0] if existing_result else None
        _validate_device_on_site(
            self.asset.is_on_site,
            self.asset.device_installed,
            existing,
        )
        return await update_asset_db(self.asset, asset_id)

    async def delete_asset(self, asset_id: int):
        return await delete_asset_db(asset_id)

    async def delete_assets(self):
        return await delete_assets_db()
