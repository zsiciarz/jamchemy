import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from graphql_api.schema import schema
from models.user import User


@pytest.mark.asyncio
async def test_query_users(session: AsyncSession) -> None:
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


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession) -> None:
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
        query, variable_values={"name": name, "email": email}
    )
    assert response.data is not None
    assert response.data["createUser"]["user"]["name"] == name


@pytest.mark.asyncio
async def test_create_user_email_already_exists(session: AsyncSession) -> None:
    async with session.begin():
        user = User(name="Zed", email="zed@example.com")
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
        query, variable_values={"name": "Zedddd", "email": user.email}
    )
    assert response.data is not None
    assert "user" not in response.data["createUser"]
    assert response.data["createUser"]["cause"] == "Email already exists"
