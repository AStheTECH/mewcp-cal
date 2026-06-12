from cal_mcp import service


def register_tools(mcp):

    @mcp.tool
    def get_event_types():
        return service.get_event_types()

    @mcp.tool
    def get_my_profile():
        return service.get_my_profile()

    @mcp.tool
    def get_schedules():
        return service.get_schedules()

    @mcp.tool
    def get_bookings():
        return service.get_bookings()