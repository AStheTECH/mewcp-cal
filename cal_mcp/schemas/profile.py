"""Profile group schemas: get_my_profile."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class ProfileData(BaseModel):
    """Authenticated user profile as returned by Cal.com v2 `GET /me`."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    username: str | None = None
    email: str | None = None
    name: str | None = None
    timeZone: str | None = None
    weekStart: str | None = None
    locale: str | None = None
    timeFormat: int | None = None
    defaultScheduleId: int | None = None
    organizationId: int | None = None
    organization: dict | None = None
    avatarUrl: str | None = None
    bio: str | None = None


class ProfileGetResult(ToolResult):
    data: ProfileData | None = None
