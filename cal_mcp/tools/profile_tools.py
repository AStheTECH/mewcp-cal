"""Profile group: get_my_profile."""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.profile import ProfileData, ProfileGetResult
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("cal-mcp.tools.profile")


def _extract_profile(payload: Any) -> dict | None:
    """Normalise the /me payload into a plain profile dict.

    Cal.com v2 wraps the profile in `{"status": "success", "data": {...}}`,
    but tolerate a bare profile object too.
    """
    body = payload.get("data", payload) if isinstance(payload, dict) else payload
    if isinstance(body, dict):
        inner = body.get("user")
        if isinstance(inner, dict):
            return inner
        return body
    return None


def register_profile_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_my_profile",
        description="Get authenticated user profile from Cal.com",
        annotations=ToolAnnotations(
            readOnlyHint=True, destructiveHint=False, openWorldHint=True
        ),
    )
    def get_my_profile() -> ProfileGetResult:
        tlog = ToolLogger(logger, "get_my_profile")

        # Only the upstream call and its response normaliser belong in the try:
        # keeping result construction out of it means tlog.success() can never
        # fire ahead of a ValidationError raised while building the model.
        try:
            data, status, retry_after = service.api_request(
                "GET", "/me",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            profile = _extract_profile(data) if 200 <= status < 300 else None
        except Exception as exc:
            return _handle_request_exc(ProfileGetResult, tlog, exc)

        if not (200 <= status < 300):
            return _upstream_err(ProfileGetResult, tlog, status, data, retry_after)
        if profile is None:
            return _err(
                ProfileGetResult, tlog, "UPSTREAM_ERROR",
                f"HTTP {status}", 502,
            )

        try:
            result = ProfileGetResult(
                success=True,
                statusCode=status,
                data=ProfileData(**profile),
            )
        except Exception as exc:
            return _handle_request_exc(ProfileGetResult, tlog, exc)

        tlog.success()
        return result
