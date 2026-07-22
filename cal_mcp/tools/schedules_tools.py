"""Schedules group: get_schedules, get_schedule, get_default_schedule, create_schedule."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.schedules import (
    ScheduleCreateResult,
    ScheduleData,
    ScheduleDefaultResult,
    ScheduleListData,
    ScheduleListResult,
    ScheduleResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("cal-mcp.tools.schedules")


def register_schedules_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_schedules",
        description="Get all schedules for the user",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_schedules() -> ScheduleListResult:
        tlog = ToolLogger(logger, "get_schedules")

        try:
            data, status, retry_after = service.api_request(
                "GET", "/schedules",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                payload = data.get("data") if isinstance(data, dict) else data
                items = payload if isinstance(payload, list) else []
                schedules = [ScheduleData(**item) for item in items if isinstance(item, dict)]
                tlog.success()
                return ScheduleListResult(
                    success=True, statusCode=status,
                    data=ScheduleListData(count=len(schedules), schedules=schedules),
                )
            return _upstream_err(ScheduleListResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ScheduleListResult, tlog, exc)

    @mcp.tool(
        name="get_schedule",
        description="Get a specific schedule by ID",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_schedule(
        schedule_id: str = Field(description="The schedule ID"),
    ) -> ScheduleResult:
        tlog = ToolLogger(logger, "get_schedule")

        if not schedule_id or not str(schedule_id).strip():
            return _err(ScheduleResult, tlog, "VALIDATION_ERROR", "schedule_id is required", 400)

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/schedules/{schedule_id}",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                payload = data.get("data") if isinstance(data, dict) else None
                tlog.success()
                return ScheduleResult(
                    success=True, statusCode=status,
                    data=ScheduleData(**payload) if isinstance(payload, dict) else None,
                )
            return _upstream_err(ScheduleResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ScheduleResult, tlog, exc)

    @mcp.tool(
        name="get_default_schedule",
        description="Get default schedule",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_default_schedule() -> ScheduleDefaultResult:
        tlog = ToolLogger(logger, "get_default_schedule")

        try:
            data, status, retry_after = service.api_request(
                "GET", "/schedules/default",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                payload = data.get("data") if isinstance(data, dict) else None
                tlog.success()
                return ScheduleDefaultResult(
                    success=True, statusCode=status,
                    data=ScheduleData(**payload) if isinstance(payload, dict) else None,
                )
            return _upstream_err(ScheduleDefaultResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ScheduleDefaultResult, tlog, exc)

    @mcp.tool(
        name="create_schedule",
        description="Create a new schedule",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_schedule(
        name: str = Field(description="Name of the schedule to create"),
    ) -> ScheduleCreateResult:
        tlog = ToolLogger(logger, "create_schedule")

        if not name or not str(name).strip():
            return _err(ScheduleCreateResult, tlog, "VALIDATION_ERROR", "name is required", 400)

        try:
            data, status, retry_after = service.api_request(
                "POST", "/schedules", body={"name": name},
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                payload = data.get("data") if isinstance(data, dict) else None
                tlog.success()
                return ScheduleCreateResult(
                    success=True, statusCode=status,
                    data=ScheduleData(**payload) if isinstance(payload, dict) else None,
                )
            return _upstream_err(ScheduleCreateResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ScheduleCreateResult, tlog, exc)
