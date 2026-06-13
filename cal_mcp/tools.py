from pydantic import Field

from cal_mcp import service


def register_tools(mcp):

    @mcp.tool(
        name="get_my_profile",
        description="Get authenticated user profile from Cal.com"
    )
    def get_my_profile():
        return service.get_my_profile()

    @mcp.tool(
        name="get_event_types",
        description="List all event types for the user"
    )
    def get_event_types():
        return service.get_event_types()

    @mcp.tool(
        name="get_schedules",
        description="Get all schedules for the user"
    )
    def get_schedules():
        return service.get_schedules()

    @mcp.tool(
        name="get_bookings",
        description="Get all bookings for the user"
    )
    def get_bookings():
        return service.get_bookings()

    # ---------------- BOOKINGS ----------------

    @mcp.tool(
        name="get_booking",
        description="Get a specific booking by ID"
    )
    def get_booking(
        booking_id: str = Field(
            ...,
            description="The booking ID to retrieve"
        )
    ):
        return service.get_booking(booking_id)

    @mcp.tool(
        name="cancel_booking",
        description="Cancel a booking"
    )
    def cancel_booking(
        booking_id: str = Field(
            ...,
            description="The booking ID to cancel"
        )
    ):
        return service.cancel_booking(booking_id)

    @mcp.tool(
        name="reschedule_booking",
        description="Reschedule an existing booking"
    )
    def reschedule_booking(
        booking_id: str = Field(
            ...,
            description="The booking ID to reschedule"
        ),
        start: str = Field(
            ...,
            description="New start time"
        ),
        end: str = Field(
            ...,
            description="New end time"
        )
    ):
        return service.reschedule_booking(booking_id, start, end)

    # ---------------- SCHEDULES ----------------

    @mcp.tool(
        name="get_schedule",
        description="Get a specific schedule by ID"
    )
    def get_schedule(
        schedule_id: str = Field(
            ...,
            description="The schedule ID"
        )
    ):
        return service.get_schedule(schedule_id)

    @mcp.tool(
        name="get_default_schedule",
        description="Get default schedule"
    )
    def get_default_schedule():
        return service.get_default_schedule()

    @mcp.tool(
        name="create_schedule",
        description="Create a new schedule"
    )
    def create_schedule(
        name: str = Field(
            ...,
            description="Name of the schedule to create"
        )
    ):
        return service.create_schedule(name)

    # ---------------- AVAILABILITY ----------------

    @mcp.tool(
        name="get_availability",
        description="Get available time slots"
    )
    def get_availability(
        date: str = Field(
            ...,
            description="Date in YYYY-MM-DD format"
        )
    ):
        return service.get_availability(date)

    @mcp.tool(
        name="get_busy_times",
        description="Get busy times from calendars"
    )
    def get_busy_times():
        return service.get_busy_times()

    # ---------------- ORGANIZATION ----------------

    @mcp.tool(
        name="get_org_memberships",
        description="Get organization memberships"
    )
    def get_org_memberships():
        return service.get_org_memberships()

    @mcp.tool(
        name="get_org_routing_forms",
        description="Get organization routing forms"
    )
    def get_org_routing_forms():
        return service.get_org_routing_forms()
        # ---------------- EVENT TYPES ----------------

    @mcp.tool(
        name="get_event_type",
        description="Get a specific event type by ID"
    )
    def get_event_type(
        event_type_id: int = Field(
            ...,
            description="The event type ID"
        )
    ):
        return service.get_event_type(event_type_id)

    @mcp.tool(
        name="create_event_type",
        description="Create a new event type"
    )
    def create_event_type(
        title: str = Field(
            ...,
            description="Title of the event type"
        )
    ):
        return service.create_event_type(title)

    # ---------------- BOOKINGS ----------------

    @mcp.tool(
        name="create_booking",
        description="Create a new booking"
    )
    def create_booking(
        event_type_id: int = Field(
            ...,
            description="Event type ID"
        ),
        start: str = Field(
            ...,
            description="Booking start datetime"
        ),
        attendee_name: str = Field(
            ...,
            description="Attendee full name"
        ),
        attendee_email: str = Field(
            ...,
            description="Attendee email address"
        )
    ):
        return service.create_booking(
            event_type_id,
            start,
            attendee_name,
            attendee_email
        )

    @mcp.tool(
        name="confirm_booking",
        description="Confirm a pending booking"
    )
    def confirm_booking(
        booking_id: str = Field(
            ...,
            description="Booking ID"
        )
    ):
        return service.confirm_booking(booking_id)

    @mcp.tool(
        name="mark_booking_absent",
        description="Mark a booking as absent"
    )
    def mark_booking_absent(
        booking_id: str = Field(
            ...,
            description="Booking ID"
        )
    ):
        return service.mark_booking_absent(booking_id)