from sqlalchemy.orm import configure_mappers

from .idea import Idea  # noqa
from .user import User  # noqa

configure_mappers()
