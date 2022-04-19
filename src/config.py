import logging.config
import os

import structlog
from structlog.types import Processor

DATABASE_URI = os.environ.get(
    "DATABASE_URI",
    "sqlite+aiosqlite:///jamchemy.db",
)

pre_chain: list[Processor] = [
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "structlog": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
            "foreign_pre_chain": pre_chain,
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "structlog",
        },
    },
    "loggers": {
        "events": {"handlers": ["console"], "level": "INFO"},
        "strawberry": {"handlers": ["console"], "level": "WARNING"},
        "sqlalchemy.engine": {"handlers": ["console"], "level": "INFO"},
        "uvicorn": {"handlers": ["console"], "level": "WARNING"},
    },
}
logging.config.dictConfig(LOGGING)

structlog.configure(
    processors=pre_chain
    + [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
