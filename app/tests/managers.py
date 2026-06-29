# app/managers.py

from app.tests.schemas import (
    TestBase
)
from app.tests.db import (
    get_tests_db,
    get_test_db,
    add_test_db,
    update_test_db,
    delete_test_db,
    delete_tests_db
)
from uuid import UUID

class TestManager:
    def __init__(self, test: TestBase):
        self.test = test

    async def get_tests(self):
        return await get_tests_db()

    async def get_test(self, test_id: int):
        return await get_test_db(test_id)

    async def add_test(self):
        return await add_test_db(self.test)

    async def update_test(self, test_id: int):
        return await update_test_db(self.test, test_id)

    async def delete_test(self, test_id: int):
        return await delete_test_db(test_id)

    async def delete_tests(self):
        return await delete_tests_db()