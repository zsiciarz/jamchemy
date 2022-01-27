import strawberry


@strawberry.type
class User:
    name: str
    email: str


me = User(name="Zbigniew", email="zbigniew@example.com")


@strawberry.type
class Query:
    users: list[User] = strawberry.field(resolver=lambda: [me])


schema = strawberry.Schema(query=Query)
