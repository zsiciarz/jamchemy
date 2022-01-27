from strawberry.asgi import GraphQL

from graphql_api.schema import schema

app = GraphQL(schema)
