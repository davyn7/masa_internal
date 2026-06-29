from app.connection import supabase
from app.tests.schemas import (
    TestBase
)
from uuid import UUID

async def get_tests_db():
    response = supabase.table("tests").select("*").execute()
    return response.data

async def get_test_db(test_id: int):
    response = supabase.table("tests").select("*").eq("id", test_id).execute()
    return response.data

async def add_test_db(test: TestBase):
    test_data = test.model_dump(mode="json")
    response = supabase.table("tests").insert(test_data).execute()
    return response.data
    branch_data = branch.model_dump(exclude_unset=True, mode="json")
    response = supabase.table("tests").update(test_data).eq("id", test_id).execute()
    return response.data

async def delete_test_db(test_id: int):
    response = supabase.table("tests").delete().eq("id", test_id).execute()
    return response.data

async def delete_tests_db():
    response = supabase.table("tests").delete().neq("id", 0).execute()
    return response.data