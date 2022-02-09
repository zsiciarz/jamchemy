import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from graphql_api.schema import schema
from models.user import User


@pytest.mark.asyncio
async def test_query_async(session: AsyncSession) -> None:
    async with session.begin():
        user = User(name="Mike", email="mike@example.com")
        session.add(user)
    query = """query Users {
        users {
            name
            email
        }
    }
    """
    response = await schema.execute(query)
    assert response.data is not None
    assert response.data["users"][0]["name"] == user.name
