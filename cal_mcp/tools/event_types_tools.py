"""Event types group: get_event_types, get_event_type, create_event_type."""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.event_types import (
    EventTypeCreateResult,
    EventTypeData,
    EventTypeGetResult,
    EventTypeListData,
    EventTypeListResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("cal-mcp.tools.event_types")


def _extract_event_types(payload: Any) -> list[dict]:
    """Normalise the /event-types payload into a flat list of event type objects.

    Cal.com returns either a bare list of event types or, for some account
    shapes, an object holding `eventTypeGroups`, each with its own `eventTypes`.
    """
    body = payload.get("data", payload) if isinstance(payload, dict) else payload
    if isinstance(body, list):
        return [item for item in body if isinstance(item, dict)]
    if isinstance(body, dict):
        groups = body.get("eventTypeGroups")
        if isinstance(groups, list):
            collected: list[dict] = []
            for group in groups:
                if isinstance(group, dict) and isinstance(group.get("eventTypes"), list):
                    collected.extend(e for e in group["eventTypes"] if isinstance(e, dict))
            return collected
        event_types = body.get("eventTypes")
        if isinstance(event_types, list):
            return [item for item in event_types if isinstance(item, dict)]
    return []


def _extract_event_type(payload: Any) -> dict | None:
    """Normalise a single event type payload into a plain dict."""
    body = payload.get("data", payload) if isinstance(payload, dict) else payload
    if isinstance(body, dict):
        inner = body.get("eventType")
        if isinstance(inner, dict):
            return inner
        return body
    return None


def register_event_types_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_event_types",
        description="List all event types for the user",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                                    openWorldHint=True),
    )
    def get_event_types() -> EventTypeListResult:
        tlog = ToolLogger(logger, "get_event_types")

        try:
            data, status, retry_after = service.api_request(
                "GET", "/event-types",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if not (200 <= status < 300):
                return _upstream_err(EventTypeListResult, tlog, status, data, retry_after)
            items = _extract_event_types(data)
        except Exception as exc:
            return _handle_request_exc(EventTypeListResult, tlog, exc)

        result = EventTypeListResult(
            success=True,
            statusCode=status,
            data=EventTypeListData(
                count=len(items),
                event_types=[EventTypeData(**item) for item in items],
            ),
        )
        tlog.success()
        return result

    @mcp.tool(
        name="get_event_type",
        description="Get a specific event type by ID",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                                    openWorldHint=True),
    )
    def get_event_type(
        event_type_id: int = Field(
            description=(
                "The event type ID: the numeric Cal.com identifier of the event type "
                "to retrieve, as an integer (e.g. 123456). Required — the call fails "
                "with a validation error if omitted."
            ),
        ),
    ) -> EventTypeGetResult:
        tlog = ToolLogger(logger, "get_event_type")

        if event_type_id is None:
            return _err(
                EventTypeGetResult, tlog, "VALIDATION_ERROR",
                "event_type_id is required", 400,
            )

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/event-types/{event_type_id}",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if not (200 <= status < 300):
                return _upstream_err(EventTypeGetResult, tlog, status, data, retry_after)
            event_type = _extract_event_type(data)
        except Exception as exc:
            return _handle_request_exc(EventTypeGetResult, tlog, exc)

        if event_type is None:
            return _err(
                EventTypeGetResult, tlog, "UPSTREAM_ERROR",
                f"HTTP {status}", status,
            )

        result = EventTypeGetResult(
            success=True, statusCode=status, data=EventTypeData(**event_type),
        )
        tlog.success()
        return result

    @mcp.tool(
        name="create_event_type",
        description="Create a new event type",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False,
                                    openWorldHint=True),
    )
    def create_event_type(
        title: str = Field(
            description=(
                "Title of the event type: the display name for the new event type, "
                "as a plain non-empty string (e.g. '30 Minute Meeting'). Required — "
                "the call fails with a validation error if omitted or blank."
            ),
        ),
    ) -> EventTypeCreateResult:
        tlog = ToolLogger(logger, "create_event_type")

        if not title or not str(title).strip():
            return _err(
                EventTypeCreateResult, tlog, "VALIDATION_ERROR",
                "title must be a non-empty string", 400,
            )

        try:
            data, status, retry_after = service.api_request(
                "POST", "/event-types", body={"title": title},
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if not (200 <= status < 300):
                return _upstream_err(EventTypeCreateResult, tlog, status, data, retry_after)
            event_type = _extract_event_type(data)
        except Exception as exc:
            return _handle_request_exc(EventTypeCreateResult, tlog, exc)

        if event_type is None:
            return _err(
                EventTypeCreateResult, tlog, "UPSTREAM_ERROR",
                f"HTTP {status}", status,
            )

        result = EventTypeCreateResult(
            success=True, statusCode=status, data=EventTypeData(**event_type),
        )
        tlog.success()
        return result
