from asyncio import Queue

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from graphql_api.schema import schema
from models.idea import Idea, IdeaRepository
from models.user import UserRepository


@pytest.mark.asyncio
async def test_query_ideas(session: AsyncSession, queue: Queue[int]) -> None:
    user_repo = UserRepository(session)
    idea_repo = IdeaRepository(session)
    async with session.begin():
        user = await user_repo.create(name="Mike", email="mike@example.com")
        idea = Idea(author=user, summary="A cool idea", description="just kidding")
        session.add(idea)
    query = """query Ideas {
        ideas {
            author {
                name
            }
            summary
        }
    }
    """
    response = await schema.execute(
        query,
        context_value={"session": session, "queue": queue, "idea_repo": idea_repo},
    )
    assert response.data is not None
    assert response.data["ideas"][0]["author"]["name"] == user.name
    assert response.data["ideas"][0]["summary"] == idea.summary


@pytest.mark.asyncio
async def test_query_users(session: AsyncSession, queue: Queue[int]) -> None:
    user_repo = UserRepository(session)
    async with session.begin():
        user = await user_repo.create(name="Mike", email="mike@example.com")
    query = """query Users {
        users {
            name
            email
        }
    }
    """
    response = await schema.execute(
        query,
        context_value={"session": session, "queue": queue, "user_repo": user_repo},
    )
    assert response.data is not None
    assert response.data["users"][0]["name"] == user.name
