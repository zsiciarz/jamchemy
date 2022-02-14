import os

DATABASE_URI = os.environ.get(
    "DATABASE_URI",
    "sqlite+aiosqlite:///jamchemy.db",
)
