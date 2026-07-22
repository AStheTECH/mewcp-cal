"""MewCP Cal tool registration."""

from fastmcp import FastMCP

from .availability_tools import register_availability_tools
from .bookings_tools import register_bookings_tools
from .event_types_tools import register_event_types_tools
from .organizations_tools import register_organizations_tools
from .profile_tools import register_profile_tools
from .schedules_tools import register_schedules_tools


def register_tools(mcp: FastMCP) -> None:
    register_profile_tools(mcp)
    register_event_types_tools(mcp)
    register_bookings_tools(mcp)
    register_schedules_tools(mcp)
    register_availability_tools(mcp)
    register_organizations_tools(mcp)
