from asyncio import Queue

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from graphql_api.schema import schema
from models.idea import Idea, IdeaRepository
from models.user import User, UserRepository


@pytest.mark.asyncio
async def test_query_ideas(session: AsyncSession, queue: Queue[int]) -> None:
    idea_repo = IdeaRepository(session)
    async with session.begin():
        user = User(name="Mike", email="mike@example.com")
        session.add(user)
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
        user = User(name="Mike", email="mike@example.com")
        session.add(user)
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


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, queue: Queue[int]) -> None:
    name = "Zed"
    email = "zed@example.com"
    query = """mutation CreateUser($name: String!, $email: String!) {
        createUser(name: $name, email: $email) {
            ... on CreateUserSuccess {
                user {
                    name
                    email
                }
            }
        }
    }
    """
    response = await schema.execute(
        query,
        variable_values={"name": name, "email": email},
        context_value={"session": session, "queue": queue},
    )
    assert response.data is not None
    assert response.data["createUser"]["user"]["name"] == name
    assert not queue.empty()
    user_id = await queue.get()
    assert user_id is not None
    queue.task_done()


@pytest.mark.asyncio
async def test_create_user_email_already_exists(
    session: AsyncSession, queue: Queue[int]
) -> None:
    async with session.begin():
        user = User(name="Bob", email="bob@example.com")
        session.add(user)
    query = """mutation CreateUser($name: String!, $email: String!) {
        createUser(name: $name, email: $email) {
            ... on CreateUserSuccess {
                user {
                    name
                    email
                }
            }
            ... on CreateUserError {
                cause
            }
        }
    }
    """
    response = await schema.execute(
        query,
        variable_values={"name": "Bobbb", "email": user.email},
        context_value={"session": session, "queue": queue},
    )
    assert response.data is not None
    assert "user" not in response.data["createUser"]
    assert response.data["createUser"]["cause"] == "Email already exists"
    assert queue.empty()
