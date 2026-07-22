"""Availability group: get_availability, get_busy_times."""

import logging
import re
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.availability import (
    AvailabilityData,
    AvailabilityResult,
    BusyTimeData,
    BusyTimeListData,
    BusyTimeListResult,
    SlotData,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("cal-mcp.tools.availability")

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _unwrap(payload: Any) -> Any:
    """Cal.com v2 wraps successful payloads in a top-level `data` envelope."""
    if isinstance(payload, dict) and "data" in payload:
        return payload["data"]
    return payload


def _extract_slots(payload: Any) -> list[dict]:
    """Normalise an availability payload into a flat list of slot objects.

    Cal.com returns either a bare list of slots, an object with a `slots` list,
    or an object mapping each date to its own list of slots.
    """
    body = _unwrap(payload)
    if isinstance(body, list):
        return [item for item in body if isinstance(item, dict)]
    if isinstance(body, dict):
        slots = body.get("slots")
        if isinstance(slots, list):
            return [item for item in slots if isinstance(item, dict)]
        if isinstance(slots, dict):
            collected: list[dict] = []
            for day_slots in slots.values():
                if isinstance(day_slots, list):
                    collected.extend(s for s in day_slots if isinstance(s, dict))
            return collected
    return []


def _extract_busy_times(payload: Any) -> list[dict]:
    """Normalise a busy-times payload into a flat list of busy intervals."""
    body = _unwrap(payload)
    if isinstance(body, list):
        return [item for item in body if isinstance(item, dict)]
    if isinstance(body, dict):
        for key in ("busy", "busyTimes", "busy_times"):
            value = body.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def register_availability_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_availability",
        description="Get available time slots",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                                    openWorldHint=True),
    )
    def get_availability(
        date: str = Field(
            ...,
            description=(
                "Calendar day to look up available slots for, as a plain string "
                "in YYYY-MM-DD format (ISO 8601 calendar date). Required — there "
                "is no default, and the call fails with VALIDATION_ERROR if it is "
                "omitted or not in YYYY-MM-DD format."
            )
        )
    ) -> AvailabilityResult:
        tlog = ToolLogger(logger, "get_availability")

        if not isinstance(date, str) or not _DATE_RE.match(date.strip()):
            return _err(AvailabilityResult, tlog, "VALIDATION_ERROR",
                        "date must be in YYYY-MM-DD format", 400)

        try:
            data, status, retry_after = service.api_request(
                "GET", "/availability", params={"date": date},
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if not 200 <= status < 300:
                return _upstream_err(AvailabilityResult, tlog, status, data,
                                     retry_after)
            raw_slots = _extract_slots(data)
            body = _unwrap(data)
        except Exception as exc:
            return _handle_request_exc(AvailabilityResult, tlog, exc)

        slots = [SlotData(**slot) for slot in raw_slots]
        time_zone = body.get("timeZone") if isinstance(body, dict) else None
        result = AvailabilityResult(
            success=True, statusCode=status,
            data=AvailabilityData(
                date=date, timeZone=time_zone,
                count=len(slots), slots=slots,
            ),
        )
        tlog.success()
        return result

    @mcp.tool(
        name="get_busy_times",
        description="Get busy times from calendars",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                                    openWorldHint=True),
    )
    def get_busy_times() -> BusyTimeListResult:
        tlog = ToolLogger(logger, "get_busy_times")

        try:
            data, status, retry_after = service.api_request(
                "GET", "/busy-times",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if not 200 <= status < 300:
                return _upstream_err(BusyTimeListResult, tlog, status, data,
                                     retry_after)
            raw_busy = _extract_busy_times(data)
        except Exception as exc:
            return _handle_request_exc(BusyTimeListResult, tlog, exc)

        busy = [BusyTimeData(**item) for item in raw_busy]
        result = BusyTimeListResult(
            success=True, statusCode=status,
            data=BusyTimeListData(count=len(busy), busy_times=busy),
        )
        tlog.success()
        return result
