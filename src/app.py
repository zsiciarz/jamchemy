import asyncio

from graphql_api.asgi import JamchemyGraphQL
from graphql_api.schema import schema

# mutation puts User IDs on queue, subscription consumes the ID
# note: this assumes running in a single process
queue: asyncio.Queue[int] = asyncio.Queue()


app = JamchemyGraphQL(schema, queue=queue)
