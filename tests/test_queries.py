import pytest

from graphql_api.schema import schema
from graphql_api.types import Context


@pytest.mark.asyncio
async def test_query_ideas(execution_context: Context) -> None:
    idea_repo = execution_context.idea_repo
    user_repo = execution_context.user_repo
    session = execution_context.session
    async with session.begin():
        user = await user_repo.create(name="Mike", email="mike@example.com")
        idea = await idea_repo.create(
            author=user, summary="A cool idea", description="just kidding"
        )
    query = """query Ideas {
        ideas {
            author {
                name
            }
            summary
        }
    }
    """
    response = await schema.execute(query, context_value=execution_context)
    assert response.data is not None
    assert response.data["ideas"][0]["author"]["name"] == user.name
    assert response.data["ideas"][0]["summary"] == idea.summary


@pytest.mark.asyncio
async def test_query_users(execution_context: Context) -> None:
    user_repo = execution_context.user_repo
    session = execution_context.session
    async with session.begin():
        user = await user_repo.create(name="Mike", email="mike@example.com")
    query = """query Users {
        users {
            name
            email
        }
    }
    """
    response = await schema.execute(query, context_value=execution_context)
    assert response.data is not None
    assert response.data["users"][0]["name"] == user.name
