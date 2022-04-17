import asyncio
from typing import Any, Optional, Union

from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL
from strawberry.schema import BaseSchema

from graphql_api.types import Context
from models.base import Session
from models.idea import IdeaRepository
from models.user import UserRepository


class JamchemyGraphQL(GraphQL):
    def __init__(self, schema: BaseSchema, queue: asyncio.Queue[int], **kwargs: Any):
        super().__init__(schema, **kwargs)
        self.queue = queue

    async def get_context(
        self,
        request: Union[Request, WebSocket],
        response: Optional[Response] = None,
    ) -> Context:
        async with Session() as session:
            # TODO: Should we call session.begin() here? Should the entire
            # request be atomic with regard to database transactions?
            return {
                "queue": self.queue,
                "request": request,
                "response": response,
                "session": session,
                "idea_repo": IdeaRepository(session),
                "user_repo": UserRepository(session),
            }
