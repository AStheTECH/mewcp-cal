"""Organizations group: get_org_memberships, get_org_routing_forms."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.organizations import (
    OrgMembershipData,
    OrgMembershipListData,
    OrgMembershipListResult,
    OrgRoutingFormData,
    OrgRoutingFormListData,
    OrgRoutingFormListResult,
)
from ._helpers import _handle_request_exc, _upstream_err

logger = logging.getLogger("cal-mcp.tools.organizations")


def _items(data) -> list[dict]:
    """Unwrap the Cal.com `{status, data: [...]}` envelope into a list of dicts."""
    payload = data.get("data") if isinstance(data, dict) else data
    if isinstance(payload, dict):
        payload = next(
            (value for value in payload.values() if isinstance(value, list)), []
        )
    items = payload if isinstance(payload, list) else []
    return [item for item in items if isinstance(item, dict)]


def register_organizations_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_org_memberships",
        description="Get organization memberships",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_org_memberships() -> OrgMembershipListResult:
        tlog = ToolLogger(logger, "get_org_memberships")

        # Only the upstream call and its response normaliser belong in the try:
        # keeping result construction out of it means tlog.success() can never
        # be emitted alongside a later status=error for the same call.
        try:
            data, status, retry_after = service.api_request(
                "GET", "/organizations/memberships",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            items = _items(data) if 200 <= status < 300 else []
        except Exception as exc:
            return _handle_request_exc(OrgMembershipListResult, tlog, exc)

        if not (200 <= status < 300):
            return _upstream_err(OrgMembershipListResult, tlog, status, data, retry_after)

        try:
            memberships = [OrgMembershipData(**item) for item in items]
            result = OrgMembershipListResult(
                success=True, statusCode=status,
                data=OrgMembershipListData(
                    count=len(memberships), memberships=memberships
                ),
            )
        except Exception as exc:
            return _handle_request_exc(OrgMembershipListResult, tlog, exc)

        tlog.success()
        return result

    @mcp.tool(
        name="get_org_routing_forms",
        description="Get organization routing forms",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_org_routing_forms() -> OrgRoutingFormListResult:
        tlog = ToolLogger(logger, "get_org_routing_forms")

        # Only the upstream call and its response normaliser belong in the try:
        # keeping result construction out of it means tlog.success() can never
        # be emitted alongside a later status=error for the same call.
        try:
            data, status, retry_after = service.api_request(
                "GET", "/organizations/routing-forms",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            items = _items(data) if 200 <= status < 300 else []
        except Exception as exc:
            return _handle_request_exc(OrgRoutingFormListResult, tlog, exc)

        if not (200 <= status < 300):
            return _upstream_err(OrgRoutingFormListResult, tlog, status, data, retry_after)

        try:
            forms = [OrgRoutingFormData(**item) for item in items]
            result = OrgRoutingFormListResult(
                success=True, statusCode=status,
                data=OrgRoutingFormListData(
                    count=len(forms), routing_forms=forms
                ),
            )
        except Exception as exc:
            return _handle_request_exc(OrgRoutingFormListResult, tlog, exc)

        tlog.success()
        return result
