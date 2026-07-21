# app/assets/managers.py

from typing import Optional
from fastapi import HTTPException
from app.assets.schemas import MakeBase, ModelBase
from app.assets.db import (
    get_makes_db,
    get_make_db,
    get_make_by_name_db,
    add_make_db,
    update_make_db,
    delete_make_db,
    delete_makes_db,
    get_models_db,
    get_model_db,
    get_model_by_make_and_name_db,
    add_model_db,
    update_model_db,
    delete_model_db,
    delete_models_db,
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
