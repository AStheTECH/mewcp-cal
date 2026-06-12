import requests
from fastmcp_credentials import get_credentials

from cal_mcp.config import (
    CAL_API_BASE,
    CAL_API_VERSION,
    API_TIMEOUT
)


def get_headers():

    cred = get_credentials()
    api_key = cred.fields["api_key"]

    return {
        "Authorization": f"Bearer {api_key}",
        "cal-api-version": CAL_API_VERSION
    }


def get_event_types():

    response = requests.get(
        f"{CAL_API_BASE}/event-types",
        headers=get_headers(),
        timeout=API_TIMEOUT
    )

    return response.json()


def get_my_profile():

    response = requests.get(
        f"{CAL_API_BASE}/me",
        headers=get_headers(),
        timeout=API_TIMEOUT
    )

    return response.json()


def get_schedules():

    response = requests.get(
        f"{CAL_API_BASE}/schedules",
        headers=get_headers(),
        timeout=API_TIMEOUT
    )

    return response.json()


def get_bookings():

    response = requests.get(
        f"{CAL_API_BASE}/bookings",
        headers=get_headers(),
        timeout=API_TIMEOUT
    )

    return response.json()