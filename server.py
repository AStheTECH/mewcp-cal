from fastmcp import FastMCP
import requests
from dotenv import load_dotenv
import os

mcp = FastMCP("Cal.com MCP")
load_dotenv()

API_KEY = os.getenv("CAL_API_KEY")
if not API_KEY:
    raise ValueError("CAL_API_KEY not found in .env")

@mcp.tool
def get_event_types():

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "cal-api-version": "2024-06-11"
    }

    response = requests.get(
        "https://api.cal.com/v2/event-types",
        headers=headers
    )

    return response.json()
@mcp.tool
def get_my_profile():

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "cal-api-version": "2024-06-11"
    }

    response = requests.get(
        "https://api.cal.com/v2/me",
        headers=headers
    )

    return response.json()
@mcp.tool
def get_schedules():

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "cal-api-version": "2024-06-11"
    }

    response = requests.get(
        "https://api.cal.com/v2/schedules",
        headers=headers
    )

    return response.json()
@mcp.tool
def get_bookings():

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "cal-api-version": "2024-06-11"
    }

    response = requests.get(
        "https://api.cal.com/v2/bookings",
        headers=headers
    )

    return response.json()

if __name__ == "__main__":
    mcp.run()