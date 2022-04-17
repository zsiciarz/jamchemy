from asyncio import Queue

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from graphql_api.schema import schema
from models.user import UserRepository


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, queue: Queue[int]) -> None:
    user_repo = UserRepository(session)
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
        context_value={"session": session, "queue": queue, "user_repo": user_repo},
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
    user_repo = UserRepository(session)
    async with session.begin():
        user = await user_repo.create(name="Bob", email="bob@example.com")
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
        context_value={"session": session, "queue": queue, "user_repo": user_repo},
    )
    assert response.data is not None
    assert "user" not in response.data["createUser"]
    assert response.data["createUser"]["cause"] == "Email already exists"
    assert queue.empty()
