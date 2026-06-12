# To get the WHOLE json formatted file use this
# import asyncio
# from fastmcp import Client

# async def main():

#     async with Client("server.py") as client:

#         print("EVENT TYPES")
#         print(
#             await client.call_tool(
#                 "get_event_types",
#                 {}
#             )
#         )

#         print("\nPROFILE")
#         print(
#             await client.call_tool(
#                 "get_my_profile",
#                 {}
#             )
#         )

#         print("\nSCHEDULES")
#         print(
#             await client.call_tool(
#                 "get_schedules",
#                 {}
#             )
#         )

# asyncio.run(main())
#To get just the data from the json
import asyncio
from fastmcp import Client

async def main():

    async with Client("server.py") as client:

        # EVENT TYPES
        event_result = await client.call_tool(
            "get_event_types",
            {}
        )

        print("EVENT TYPES")

        events = event_result.data["data"]["eventTypeGroups"][0]["eventTypes"]

        for event in events:
            print(f"- {event['title']} ({event['length']} min)")

        # PROFILE
        profile_result = await client.call_tool(
            "get_my_profile",
            {}
        )

        profile = profile_result.data["data"]

        print("\nPROFILE")
        print(f"Name: {profile['name']}")
        print(f"Email: {profile['email']}")
        print(f"Timezone: {profile['timeZone']}")

        # SCHEDULES
        schedule_result = await client.call_tool(
            "get_schedules",
            {}
        )

        print("\nSCHEDULES")

        if schedule_result.data.get("data"):
            print("Schedules retrieved successfully")
        else:
            print("No schedules found")

        # BOOKINGS
        booking_result = await client.call_tool(
            "get_bookings",
            {}
        )

        print("\nBOOKINGS")

        if booking_result.data.get("data"):
            print("Bookings retrieved successfully")
        else:
            print("No bookings found")

asyncio.run(main())