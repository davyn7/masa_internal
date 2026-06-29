# app/router.py

from fastapi import APIRouter
from app.managers import (
    TestManager
)
from app.schemas import (
    TestBase
)
from uuid import UUID

router = APIRouter(prefix="/tests", tags=["Tests"])

# Initialize DB Testing

@router.post("/populate")
async def populate():
    pass

@router.delete("/clear")
async def clear():
    pass

# Test Routers

@router.get("/tests")
async def get_tests():
    try:
        manager = TestManager(None)
        return await manager.get_tests()
    except Exception as e:
        raise e

@router.get("/tests/{test_id}")
async def get_test(test_id: int):
    try:
        manager = TestManager(None)
        return await manager.get_test(test_id)
    except Exception as e:
        raise e

@router.post("/add_test")
async def add_test(test: TestBase):
    try:
        manager = TestManager(test)
        return await manager.add_test()
    except Exception as e:
        raise e

@router.put("/update_test/{test_id}")
async def update_test(test_id: int, test: TestBase):
    try:
        manager = TestManager(test)
        return await manager.update_test(test_id)
    except Exception as e:
        raise e

@router.delete("/delete_test/{test_id}")
async def delete_test(test_id: int):
    try:
        manager = TestManager(None)
        return await manager.delete_test(test_id)
    except Exception as e:
        raise e

@router.delete("/delete_tests")
async def delete_tests():
    try:
        manager = TestManager(None)
        return await manager.delete_tests()
    except Exception as e:
        raise e

