"""Schemas for the availability tool group."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class SlotData(BaseModel):
    """A single bookable time slot returned by Cal.com."""

    model_config = ConfigDict(extra="allow")

    start: str | None = None
    end: str | None = None
    time: str | None = None
    attendees: int | None = None
    bookingUid: str | None = None


class AvailabilityData(BaseModel):
    """Available time slots for a single date."""

    model_config = ConfigDict(extra="allow")

    date: str | None = None
    timeZone: str | None = None
    count: int
    slots: list[SlotData] = []


class AvailabilityResult(ToolResult):
    data: AvailabilityData | None = None


class BusyTimeData(BaseModel):
    """A single busy interval pulled from a connected calendar."""

    model_config = ConfigDict(extra="allow")

    start: str | None = None
    end: str | None = None
    source: str | None = None
    title: str | None = None


class BusyTimeListData(BaseModel):
    """All busy intervals across the user's connected calendars."""

    model_config = ConfigDict(extra="allow")

    count: int
    busy_times: list[BusyTimeData] = []


class BusyTimeListResult(ToolResult):
    data: BusyTimeListData | None = None
