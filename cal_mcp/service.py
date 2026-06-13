import requests
from fastmcp_credentials import get_credentials

from cal_mcp.config import (
    CAL_API_BASE,
    CAL_API_VERSION,
    API_TIMEOUT
)


def get_headers():
    try:
        cred = get_credentials()
        api_key = cred.fields["api_key"]

        return {
            "Authorization": f"Bearer {api_key}",
            "cal-api-version": CAL_API_VERSION
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def get_event_types():
    try:
        response = requests.get(
            f"{CAL_API_BASE}/event-types",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def get_my_profile():
    try:
        response = requests.get(
            f"{CAL_API_BASE}/me",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def get_schedules():
    try:
        response = requests.get(
            f"{CAL_API_BASE}/schedules",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def get_bookings():
    try:
        response = requests.get(
            f"{CAL_API_BASE}/bookings",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    # ---------------- BOOKINGS ----------------

def get_booking(booking_id: str):
    try:
        response = requests.get(
            f"{CAL_API_BASE}/bookings/{booking_id}",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def cancel_booking(booking_id: str):
    try:
        response = requests.post(
            f"{CAL_API_BASE}/bookings/{booking_id}/cancel",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def reschedule_booking(
    booking_id: str,
    start: str,
    end: str
):
    try:
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

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ---------------- SCHEDULES ----------------

def get_schedule(schedule_id: str):
    try:
        response = requests.get(
            f"{CAL_API_BASE}/schedules/{schedule_id}",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def get_default_schedule():
    try:
        response = requests.get(
            f"{CAL_API_BASE}/schedules/default",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def create_schedule(name: str):
    try:
        response = requests.post(
            f"{CAL_API_BASE}/schedules",
            headers=get_headers(),
            json={
                "name": name
            },
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ---------------- AVAILABILITY ----------------

def get_availability(date: str):
    try:
        response = requests.get(
            f"{CAL_API_BASE}/availability",
            headers=get_headers(),
            params={
                "date": date
            },
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def get_busy_times():
    try:
        response = requests.get(
            f"{CAL_API_BASE}/busy-times",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ---------------- ORGANIZATIONS ----------------

def get_org_memberships():
    try:
        response = requests.get(
            f"{CAL_API_BASE}/organizations/memberships",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def get_org_routing_forms():
    try:
        response = requests.get(
            f"{CAL_API_BASE}/organizations/routing-forms",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    # ---------------- EVENT TYPES ----------------

def get_event_type(event_type_id: int):
    try:
        response = requests.get(
            f"{CAL_API_BASE}/event-types/{event_type_id}",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def create_event_type(title: str):
    try:
        response = requests.post(
            f"{CAL_API_BASE}/event-types",
            headers=get_headers(),
            json={
                "title": title
            },
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ---------------- BOOKINGS ----------------

def create_booking(
    event_type_id: int,
    start: str,
    attendee_name: str,
    attendee_email: str
):
    try:
        response = requests.post(
            f"{CAL_API_BASE}/bookings",
            headers=get_headers(),
            json={
                "eventTypeId": event_type_id,
                "start": start,
                "attendee": {
                    "name": attendee_name,
                    "email": attendee_email
                }
            },
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def confirm_booking(booking_id: str):
    try:
        response = requests.post(
            f"{CAL_API_BASE}/bookings/{booking_id}/confirm",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def mark_booking_absent(booking_id: str):
    try:
        response = requests.post(
            f"{CAL_API_BASE}/bookings/{booking_id}/absence",
            headers=get_headers(),
            timeout=API_TIMEOUT
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }