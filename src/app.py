from graphql_api.asgi import JamchemyGraphQL
from graphql_api.schema import schema

app = JamchemyGraphQL(schema)
