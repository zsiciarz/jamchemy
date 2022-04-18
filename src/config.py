import logging
import os

DATABASE_URI = os.environ.get(
    "DATABASE_URI",
    "sqlite+aiosqlite:///jamchemy.db",
)

logging.basicConfig(level=logging.INFO)
