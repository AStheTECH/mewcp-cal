"""Schemas for the bookings tool group (Cal.com v2 /bookings endpoints)."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class BookingAttendeeData(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    email: str | None = None
    timeZone: str | None = None
    phoneNumber: str | None = None
    language: str | None = None
    absent: bool | None = None


class BookingData(BaseModel):
    """A single Cal.com booking. `uid` is what every other booking endpoint takes."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    uid: str | None = None
    title: str | None = None
    description: str | None = None
    status: str | None = None
    start: str | None = None
    end: str | None = None
    duration: int | None = None
    eventTypeId: int | None = None
    meetingUrl: str | None = None
    location: str | None = None
    absentHost: bool | None = None
    cancellationReason: str | None = None
    rescheduledFromUid: str | None = None
    rescheduledToUid: str | None = None
    attendees: list[BookingAttendeeData] | None = None
    hosts: list[dict] | None = None


class BookingListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    bookings: list[BookingData]


class BookingListResult(ToolResult):
    data: BookingListData | None = None


class BookingResult(ToolResult):
    data: BookingData | None = None


class BookingCreateResult(ToolResult):
    data: BookingData | None = None


class BookingCancelData(BaseModel):
    """State of the booking immediately before the cancel call, and after it."""

    model_config = ConfigDict(extra="allow")

    before: BookingData | None = None
    after: BookingData | None = None


class BookingCancelResult(ToolResult):
    data: BookingCancelData | None = None


class BookingUpdateData(BaseModel):
    """Before/after state for a single-booking mutation."""

    model_config = ConfigDict(extra="allow")

    before: BookingData | None = None
    after: BookingData | None = None


class BookingRescheduleResult(ToolResult):
    data: BookingUpdateData | None = None


class BookingConfirmResult(ToolResult):
    data: BookingUpdateData | None = None


class BookingAbsentResult(ToolResult):
    data: BookingUpdateData | None = None
