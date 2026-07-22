"""Schemas for the event_types tool group."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class EventTypeData(BaseModel):
    """A single Cal.com event type."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    title: str | None = None
    slug: str | None = None
    lengthInMinutes: int | None = None
    length: int | None = None
    description: str | None = None
    hidden: bool | None = None
    ownerId: int | None = None


class EventTypeListData(BaseModel):
    """List of event types available to the authenticated user."""

    model_config = ConfigDict(extra="allow")

    count: int
    event_types: list[EventTypeData] = []


class EventTypeListResult(ToolResult):
    data: EventTypeListData | None = None


class EventTypeGetResult(ToolResult):
    data: EventTypeData | None = None


class EventTypeCreateResult(ToolResult):
    data: EventTypeData | None = None
