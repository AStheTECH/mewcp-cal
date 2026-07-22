"""Configuration for MewCP Cal MCP Server."""

import logging
import os

SERVER_NAME = "MewCP Cal MCP Server"
SERVER_VERSION = "v1.1.0"
BREAKING_CHANGES: list[dict] = []

CAL_API_BASE = "https://api.cal.com/v2"
CAL_API_VERSION = "2024-06-11"  # sent as the `cal-api-version` request header
CONNECT_TIMEOUT = 5  # TCP connection — fixed across all servers
READ_TIMEOUT = 30    # Cal.com REST calls are synchronous CRUD reads/writes with no async
                     # job endpoints; 30s covers the slowest list endpoints with headroom.


def configure_logging() -> None:
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        from pythonjsonlogger import jsonlogger
        handler = logging.StreamHandler()
        handler.setFormatter(
            jsonlogger.JsonFormatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s")
        )
    except ImportError:
        handler = logging.StreamHandler()
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(log_level)
