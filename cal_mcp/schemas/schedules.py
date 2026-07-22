"""Schemas for the schedules tool group (Cal.com v2 /schedules endpoints)."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class ScheduleAvailabilityData(BaseModel):
    """One availability window inside a schedule."""

    model_config = ConfigDict(extra="allow")

    days: list[str] | None = None
    startTime: str | None = None
    endTime: str | None = None


class ScheduleData(BaseModel):
    """A single Cal.com schedule. `id` is what every other schedule endpoint takes."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    ownerId: int | None = None
    name: str | None = None
    timeZone: str | None = None
    isDefault: bool | None = None
    availability: list[ScheduleAvailabilityData] | None = None
    overrides: list[dict] | None = None


class ScheduleListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    schedules: list[ScheduleData]


class ScheduleListResult(ToolResult):
    data: ScheduleListData | None = None


class ScheduleResult(ToolResult):
    data: ScheduleData | None = None


class ScheduleDefaultResult(ToolResult):
    data: ScheduleData | None = None


class ScheduleCreateResult(ToolResult):
    data: ScheduleData | None = None
