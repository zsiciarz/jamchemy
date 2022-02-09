import pytest

from graphql_api.schema import schema


@pytest.mark.asyncio
async def test_query_async():
    query = """query Users {
        users {
            name
            email
        }
    }
    """
    response = await schema.execute(query)
    assert len(response.data["users"]) == 1
