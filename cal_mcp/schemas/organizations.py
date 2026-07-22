"""Schemas for the organizations tool group (Cal.com v2 /organizations endpoints)."""

from typing import Any

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class OrgMembershipUserData(BaseModel):
    """The user attached to an organization membership."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    email: str | None = None
    username: str | None = None
    name: str | None = None


class OrgMembershipData(BaseModel):
    """A single organization membership.

    `id` is the membership id used by membership-scoped endpoints; `teamId` is the
    organization/team the membership belongs to and `userId` the member it grants access to.
    """

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    userId: int | None = None
    teamId: int | None = None
    organizationId: int | None = None
    role: str | None = None
    accepted: bool | None = None
    disableImpersonation: bool | None = None
    user: OrgMembershipUserData | None = None


class OrgMembershipListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    memberships: list[OrgMembershipData]


class OrgMembershipListResult(ToolResult):
    data: OrgMembershipListData | None = None


class OrgRoutingFormData(BaseModel):
    """A single organization routing form. `id` is what routing-form endpoints take."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    description: str | None = None
    disabled: bool | None = None
    position: int | None = None
    userId: int | None = None
    teamId: int | None = None
    routes: Any = None
    fields: Any = None
    createdAt: str | None = None
    updatedAt: str | None = None


class OrgRoutingFormListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    count: int
    routing_forms: list[OrgRoutingFormData]


class OrgRoutingFormListResult(ToolResult):
    data: OrgRoutingFormListData | None = None
