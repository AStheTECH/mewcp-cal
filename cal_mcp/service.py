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


# ---------------- BOOKINGS ----------------

def get_booking(booking_id: str):

    response = requests.get(
        f"{CAL_API_BASE}/bookings/{booking_id}",
        headers=get_headers(),
        timeout=API_TIMEOUT
    )

    return response.json()


def cancel_booking(booking_id: str):

    response = requests.post(
        f"{CAL_API_BASE}/bookings/{booking_id}/cancel",
        headers=get_headers(),
        timeout=API_TIMEOUT
    )

    return response.json()


def reschedule_booking(
    booking_id: str,
    start: str,
    end: str
):

    response = requests.post(
        f"{CAL_API_BASE}/bookings/{booking_id}/reschedule",
        headers=get_headers(),
        json={
            "start": start,
            "end": end
        },
        timeout=API_TIMEOUT
    )

    return response.json()


# ---------------- SCHEDULES ----------------

def get_schedule(schedule_id: str):

    response = requests.get(
        f"{CAL_API_BASE}/schedules/{schedule_id}",
        headers=get_headers(),
        timeout=API_TIMEOUT
    )

    return response.json()


def get_default_schedule():

    response = requests.get(
        f"{CAL_API_BASE}/schedules/default",
        headers=get_headers(),
        timeout=API_TIMEOUT
    )

    return response.json()


def create_schedule(name: str):

    response = requests.post(
        f"{CAL_API_BASE}/schedules",
        headers=get_headers(),
        json={
            "name": name
        },
        timeout=API_TIMEOUT
    )

    return response.json()


# ---------------- AVAILABILITY ----------------

def get_availability(date: str):

    response = requests.get(
        f"{CAL_API_BASE}/availability",
        headers=get_headers(),
        params={
            "date": date
        },
        timeout=API_TIMEOUT
    )

    return response.json()


def get_busy_times():

    response = requests.get(
        f"{CAL_API_BASE}/busy-times",
        headers=get_headers(),
        timeout=API_TIMEOUT
    )

    return response.json()


# ---------------- ORGANIZATIONS ----------------

def get_org_memberships():

    response = requests.get(
        f"{CAL_API_BASE}/organizations/memberships",
        headers=get_headers(),
        timeout=API_TIMEOUT
    )

    return response.json()


def get_org_routing_forms():

    response = requests.get(
        f"{CAL_API_BASE}/organizations/routing-forms",
        headers=get_headers(),
        timeout=API_TIMEOUT
    )

    return response.json()