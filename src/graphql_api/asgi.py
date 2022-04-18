from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL

from events import EventManager
from graphql_api.types import Context
from models.base import Session
from models.idea import IdeaRepository
from models.user import UserRepository

event_manager = EventManager()


class JamchemyGraphQL(GraphQL):
    async def get_context(
        self,
        request: Request | WebSocket,
        response: Response | None = None,
    ) -> Context:
        async with Session() as session:
            # TODO: Should we call session.begin() here? Should the entire
            # request be atomic with regard to database transactions?
            return Context(
                request=request,
                response=response,
                event_manager=event_manager,
                session=session,
                idea_repo=IdeaRepository(session),
                user_repo=UserRepository(session),
            )
