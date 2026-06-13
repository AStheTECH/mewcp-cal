from cal_mcp import service


def register_tools(mcp):

    @mcp.tool(description="Get authenticated user profile from Cal.com")
    def get_my_profile():
        return service.get_my_profile()

    @mcp.tool(description="List all event types for the user")
    def get_event_types():
        return service.get_event_types()

    @mcp.tool(description="Get all schedules for the user")
    def get_schedules():
        return service.get_schedules()

    @mcp.tool(description="Get all bookings for the user")
    def get_bookings():
        return service.get_bookings()

    # ---------------- BOOKINGS EXPANSION ----------------

    @mcp.tool(description="Get a specific booking by ID")
    def get_booking(booking_id: str):
        return service.get_booking(booking_id)

    @mcp.tool(description="Cancel a booking")
    def cancel_booking(booking_id: str):
        return service.cancel_booking(booking_id)

    @mcp.tool(description="Reschedule an existing booking")
    def reschedule_booking(booking_id: str, start: str, end: str):
        return service.reschedule_booking(booking_id, start, end)

    # ---------------- SCHEDULE EXPANSION ----------------

    @mcp.tool(description="Get a specific schedule by ID")
    def get_schedule(schedule_id: str):
        return service.get_schedule(schedule_id)

    @mcp.tool(description="Get default schedule")
    def get_default_schedule():
        return service.get_default_schedule()

    @mcp.tool(description="Create a new schedule")
    def create_schedule(name: str):
        return service.create_schedule(name)

    # ---------------- AVAILABILITY ----------------

    @mcp.tool(description="Get available time slots")
    def get_availability(date: str):
        return service.get_availability(date)

    @mcp.tool(description="Get busy times from calendars")
    def get_busy_times(date: str):
        return service.get_busy_times()

    # ---------------- ORGANIZATION ----------------

    @mcp.tool(description="Get organization memberships")
    def get_org_memberships():
        return service.get_org_memberships()

    @mcp.tool(description="Get organization routing forms")
    def get_org_routing_forms():
        return service.get_org_routing_forms()