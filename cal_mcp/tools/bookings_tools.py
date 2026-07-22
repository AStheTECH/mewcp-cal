"""Bookings group: get_bookings, get_booking, create_booking, cancel_booking,
reschedule_booking, confirm_booking, mark_booking_absent."""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.bookings import (
    BookingAbsentResult,
    BookingCancelData,
    BookingCancelResult,
    BookingConfirmResult,
    BookingCreateResult,
    BookingData,
    BookingListData,
    BookingListResult,
    BookingRescheduleResult,
    BookingResult,
    BookingUpdateData,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("cal-mcp.tools.bookings")

TIMEOUT = (CONNECT_TIMEOUT, READ_TIMEOUT)


def _unwrap(payload: Any) -> Any:
    """Cal.com v2 wraps every response as {"status": ..., "data": ...}."""
    if isinstance(payload, dict) and "data" in payload:
        return payload["data"]
    return payload


def register_bookings_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_bookings",
        description="Get all bookings for the user",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                                    openWorldHint=True),
    )
    def get_bookings() -> BookingListResult:
        tlog = ToolLogger(logger, "get_bookings")
        try:
            data, status, retry_after = service.api_request(
                "GET", "/bookings", timeout=TIMEOUT,
            )
            if not 200 <= status < 300:
                return _upstream_err(BookingListResult, tlog, status, data, retry_after)
            items = _unwrap(data)
            if not isinstance(items, list):
                items = [items] if items else []
        except Exception as exc:
            return _handle_request_exc(BookingListResult, tlog, exc)

        bookings = [BookingData(**b) for b in items if isinstance(b, dict)]
        result = BookingListResult(
            success=True, statusCode=status,
            data=BookingListData(count=len(bookings), bookings=bookings),
        )
        tlog.success()
        return result

    @mcp.tool(
        name="get_booking",
        description="Get a specific booking by ID",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                                    openWorldHint=True),
    )
    def get_booking(
        booking_id: str = Field(
            description="The booking ID to retrieve, as a plain string "
                        "(e.g. '12345'). Required."
        ),
    ) -> BookingResult:
        tlog = ToolLogger(logger, "get_booking")

        if not booking_id or not booking_id.strip():
            return _err(BookingResult, tlog, "VALIDATION_ERROR",
                        "booking_id must not be empty", 400)

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/bookings/{booking_id}", timeout=TIMEOUT,
            )
            if not 200 <= status < 300:
                return _upstream_err(BookingResult, tlog, status, data, retry_after)
            payload = _unwrap(data)
        except Exception as exc:
            return _handle_request_exc(BookingResult, tlog, exc)

        result = BookingResult(
            success=True, statusCode=status, data=BookingData(**payload),
        )
        tlog.success()
        return result

    @mcp.tool(
        name="create_booking",
        description="Create a new booking",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False,
                                    openWorldHint=True),
    )
    def create_booking(
        event_type_id: int = Field(
            description="Event type ID to book, as an integer (e.g. 42). Required."
        ),
        start: str = Field(
            description="Booking start datetime in ISO 8601 / RFC 3339 UTC format "
                        "(e.g. '2024-08-13T09:00:00Z'). Required."
        ),
        attendee_name: str = Field(
            description="Attendee full name as a plain string "
                        "(e.g. 'Ada Lovelace'). Required."
        ),
        attendee_email: str = Field(
            description="Attendee email address as a plain string "
                        "(e.g. 'ada@example.com'). Required."
        ),
    ) -> BookingCreateResult:
        tlog = ToolLogger(logger, "create_booking")

        if not start or not start.strip():
            return _err(BookingCreateResult, tlog, "VALIDATION_ERROR",
                        "start must not be empty", 400)
        if not attendee_name or not attendee_name.strip():
            return _err(BookingCreateResult, tlog, "VALIDATION_ERROR",
                        "attendee_name must not be empty", 400)
        if not attendee_email or "@" not in attendee_email:
            return _err(BookingCreateResult, tlog, "VALIDATION_ERROR",
                        "attendee_email must be a valid email address", 400)

        try:
            data, status, retry_after = service.api_request(
                "POST", "/bookings",
                body={
                    "eventTypeId": event_type_id,
                    "start": start,
                    "attendee": {"name": attendee_name, "email": attendee_email},
                },
                timeout=TIMEOUT,
            )
            if not 200 <= status < 300:
                return _upstream_err(BookingCreateResult, tlog, status, data, retry_after)
            payload = _unwrap(data)
        except Exception as exc:
            return _handle_request_exc(BookingCreateResult, tlog, exc)

        result = BookingCreateResult(
            success=True, statusCode=status, data=BookingData(**payload),
        )
        tlog.success()
        return result

    @mcp.tool(
        name="cancel_booking",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Cancel a booking. Permanently cancels the booking identified by `booking_id`, "
            "releasing its time slot and notifying the host and every attendee. "
            "This action is irreversible — the cancelled booking and its confirmed slot "
            "cannot be recovered. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly which booking will be cancelled and that "
            "it is permanent, and wait for their explicit written confirmation before "
            "proceeding. The response includes the booking's state before cancellation."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True,
                                    openWorldHint=True),
    )
    def cancel_booking(
        booking_id: str = Field(
            description="The booking ID to cancel, as a plain string "
                        "(e.g. '12345'). Required."
        ),
    ) -> BookingCancelResult:
        tlog = ToolLogger(logger, "cancel_booking")

        if not booking_id or not booking_id.strip():
            return _err(BookingCancelResult, tlog, "VALIDATION_ERROR",
                        "booking_id must not be empty", 400)

        try:
            before_data, before_status, before_retry = service.api_request(
                "GET", f"/bookings/{booking_id}", timeout=TIMEOUT,
            )
            if not 200 <= before_status < 300:
                return _upstream_err(BookingCancelResult, tlog, before_status,
                                     before_data, before_retry)
            before_payload = _unwrap(before_data)

            data, status, retry_after = service.api_request(
                "POST", f"/bookings/{booking_id}/cancel", timeout=TIMEOUT,
            )
            if not 200 <= status < 300:
                return _upstream_err(BookingCancelResult, tlog, status, data, retry_after)
            after_payload = _unwrap(data)
        except Exception as exc:
            return _handle_request_exc(BookingCancelResult, tlog, exc)

        before = BookingData(**before_payload)
        after = BookingData(**after_payload) if isinstance(after_payload, dict) else None
        result = BookingCancelResult(
            success=True, statusCode=status,
            data=BookingCancelData(before=before, after=after),
        )
        tlog.success()
        return result

    @mcp.tool(
        name="reschedule_booking",
        description=(
            "Reschedule an existing booking. Only the fields you provide are changed — "
            "others keep their current value. "
            "NOTE: this overwrites the current start and end times — the original state is "
            "not stored after the call. "
            "The response includes both the before and after state so you have a full "
            "record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False,
                                    openWorldHint=True),
    )
    def reschedule_booking(
        booking_id: str = Field(
            description="The booking ID to reschedule, as a plain string "
                        "(e.g. '12345'). Required."
        ),
        start: str = Field(
            description="New start time in ISO 8601 / RFC 3339 UTC format "
                        "(e.g. '2024-08-13T09:00:00Z'). Required."
        ),
        end: str = Field(
            description="New end time in ISO 8601 / RFC 3339 UTC format "
                        "(e.g. '2024-08-13T09:30:00Z'). Required."
        ),
    ) -> BookingRescheduleResult:
        tlog = ToolLogger(logger, "reschedule_booking")

        if not booking_id or not booking_id.strip():
            return _err(BookingRescheduleResult, tlog, "VALIDATION_ERROR",
                        "booking_id must not be empty", 400)
        if not start or not start.strip():
            return _err(BookingRescheduleResult, tlog, "VALIDATION_ERROR",
                        "start must not be empty", 400)
        if not end or not end.strip():
            return _err(BookingRescheduleResult, tlog, "VALIDATION_ERROR",
                        "end must not be empty", 400)

        try:
            before_data, before_status, before_retry = service.api_request(
                "GET", f"/bookings/{booking_id}", timeout=TIMEOUT,
            )
            if not 200 <= before_status < 300:
                return _upstream_err(BookingRescheduleResult, tlog, before_status,
                                     before_data, before_retry)
            before_payload = _unwrap(before_data)

            data, status, retry_after = service.api_request(
                "POST", f"/bookings/{booking_id}/reschedule",
                body={"start": start, "end": end},
                timeout=TIMEOUT,
            )
            if not 200 <= status < 300:
                return _upstream_err(BookingRescheduleResult, tlog, status, data,
                                     retry_after)
            after_payload = _unwrap(data)
        except Exception as exc:
            return _handle_request_exc(BookingRescheduleResult, tlog, exc)

        before = BookingData(**before_payload)
        after = BookingData(**after_payload) if isinstance(after_payload, dict) else None
        result = BookingRescheduleResult(
            success=True, statusCode=status,
            data=BookingUpdateData(before=before, after=after),
        )
        tlog.success()
        return result

    @mcp.tool(
        name="confirm_booking",
        description=(
            "Confirm a pending booking. Only the fields you provide are changed — others "
            "keep their current value. "
            "NOTE: this overwrites the booking's current status — the original state is not "
            "stored after the call. "
            "The response includes both the before and after state so you have a full "
            "record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False,
                                    openWorldHint=True),
    )
    def confirm_booking(
        booking_id: str = Field(
            description="ID of the pending booking to confirm, as a plain string "
                        "(e.g. '12345'). Required."
        ),
    ) -> BookingConfirmResult:
        tlog = ToolLogger(logger, "confirm_booking")

        if not booking_id or not booking_id.strip():
            return _err(BookingConfirmResult, tlog, "VALIDATION_ERROR",
                        "booking_id must not be empty", 400)

        try:
            before_data, before_status, before_retry = service.api_request(
                "GET", f"/bookings/{booking_id}", timeout=TIMEOUT,
            )
            if not 200 <= before_status < 300:
                return _upstream_err(BookingConfirmResult, tlog, before_status,
                                     before_data, before_retry)
            before_payload = _unwrap(before_data)

            data, status, retry_after = service.api_request(
                "POST", f"/bookings/{booking_id}/confirm", timeout=TIMEOUT,
            )
            if not 200 <= status < 300:
                return _upstream_err(BookingConfirmResult, tlog, status, data, retry_after)
            after_payload = _unwrap(data)
        except Exception as exc:
            return _handle_request_exc(BookingConfirmResult, tlog, exc)

        before = BookingData(**before_payload)
        after = BookingData(**after_payload) if isinstance(after_payload, dict) else None
        result = BookingConfirmResult(
            success=True, statusCode=status,
            data=BookingUpdateData(before=before, after=after),
        )
        tlog.success()
        return result

    @mcp.tool(
        name="mark_booking_absent",
        description=(
            "Mark a booking as absent. Only the fields you provide are changed — others "
            "keep their current value. "
            "NOTE: this overwrites the booking's current attendance state — the original "
            "state is not stored after the call. "
            "The response includes both the before and after state so you have a full "
            "record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False,
                                    openWorldHint=True),
    )
    def mark_booking_absent(
        booking_id: str = Field(
            description="ID of the booking to mark as absent, as a plain string "
                        "(e.g. '12345'). Required."
        ),
    ) -> BookingAbsentResult:
        tlog = ToolLogger(logger, "mark_booking_absent")

        if not booking_id or not booking_id.strip():
            return _err(BookingAbsentResult, tlog, "VALIDATION_ERROR",
                        "booking_id must not be empty", 400)

        try:
            before_data, before_status, before_retry = service.api_request(
                "GET", f"/bookings/{booking_id}", timeout=TIMEOUT,
            )
            if not 200 <= before_status < 300:
                return _upstream_err(BookingAbsentResult, tlog, before_status,
                                     before_data, before_retry)
            before_payload = _unwrap(before_data)

            data, status, retry_after = service.api_request(
                "POST", f"/bookings/{booking_id}/absence", timeout=TIMEOUT,
            )
            if not 200 <= status < 300:
                return _upstream_err(BookingAbsentResult, tlog, status, data, retry_after)
            after_payload = _unwrap(data)
        except Exception as exc:
            return _handle_request_exc(BookingAbsentResult, tlog, exc)

        before = BookingData(**before_payload)
        after = BookingData(**after_payload) if isinstance(after_payload, dict) else None
        result = BookingAbsentResult(
            success=True, statusCode=status,
            data=BookingUpdateData(before=before, after=after),
        )
        tlog.success()
        return result
