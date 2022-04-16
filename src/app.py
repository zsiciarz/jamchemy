from typing import Optional, Union

from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL

from graphql_api.schema import schema
from graphql_api.types import Context
from models.base import Session


class JamchemyGraphQL(GraphQL):
    async def get_context(
        self,
        request: Union[Request, WebSocket],
        response: Optional[Response] = None,
    ) -> Context:
        async with Session() as session:
            # TODO: Should we call session.begin() here? Should the entire
            # request be atomic with regard to database transactions?
            return {"request": request, "response": response, "session": session}


app = JamchemyGraphQL(schema)
