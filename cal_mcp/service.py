"""Upstream API client for MewCP Cal MCP Server."""

import logging
from typing import Any

import requests
from fastmcp_credentials import get_credentials

from .config import CAL_API_BASE, CAL_API_VERSION, CONNECT_TIMEOUT, READ_TIMEOUT

logger = logging.getLogger("cal-mcp.service")


def _get_credential() -> str:
    cred = get_credentials()
    value = cred.fields.get("api_key") if cred.fields else None
    if not value:
        raise ValueError("Missing api_key credential")
    return value


def _auth_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_get_credential()}",
        "cal-api-version": CAL_API_VERSION,
        "Content-Type": "application/json",
    }


def _parse_retry_after(header: str | None) -> int | None:
    if not header:
        return None
    try:
        return int(header)
    except ValueError:
        return None


def api_request(
    method: str,
    endpoint: str,
    body: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    timeout: tuple[int, int] | None = None,
) -> tuple[dict[str, Any], int, int | None]:
    if timeout is None:
        timeout = (CONNECT_TIMEOUT, READ_TIMEOUT)
    url = f"{CAL_API_BASE}{endpoint}"
    resp = requests.request(method=method, url=url, headers=_auth_headers(),
                            json=body, params=params, timeout=timeout)
    try:
        data = resp.json()
    except Exception:
        data = {"error": resp.text or "Empty response body"}
    return data, resp.status_code, _parse_retry_after(resp.headers.get("Retry-After"))
