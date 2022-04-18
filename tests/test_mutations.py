import pytest

from graphql_api.schema import schema
from graphql_api.types import Context


@pytest.mark.asyncio
async def test_create_user(execution_context: Context) -> None:
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
        context_value=execution_context,
    )
    assert response.data is not None
    assert response.data["createUser"]["user"]["name"] == name


@pytest.mark.asyncio
async def test_create_user_email_already_exists(execution_context: Context) -> None:
    user_repo = execution_context.user_repo
    session = execution_context.session
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
        context_value=execution_context,
    )
    assert response.data is not None
    assert "user" not in response.data["createUser"]
    assert response.data["createUser"]["cause"] == "Email already exists"
