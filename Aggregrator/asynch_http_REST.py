#
# This example is a modification (slight) of
# https://martinxpn.medium.com/making-requests-with-asyncio-in-python-78-100-days-of-python-eb1570b3f986
#
import asyncio
import aiohttp
import json

#
# These endpoints are on Prof. Ferguson's SwaggerHub mock APIs

resources = [
    {
        "resource": "student",
        "url": 'https://virtserver.swaggerhub.com/donald-f-ferguson/E6156Student/1.0.0/students/bb2101'
    },
    {
        "resource": "sections",
        "url": 'https://virtserver.swaggerhub.com/Columbia-Classes/Sections/1.0.0/sections?uni=bb2101'
    },
    {
        "resource": "projects",
        "url": 'https://virtserver.swaggerhub.com/Columbia-Classes/ProjectInfo/1.0.0/projects?uni=bb2021'
    }
]

# resources = [
#     {
#         "resource": "activities",
#         "url": 'https://virtserver.swaggerhub.com/YC4140/scholarnest_activities/1.0.0'
#     },
#     {
#         "resource": "users",
#         "url": 'https://virtserver.swaggerhub.com/YC4140/scholarnest_user/1.0.0'
#     },
#     {
#         "resource": "papers",
#         "url": 'https://virtserver.swaggerhub.com/YC4140/Scholarnest_papers/1.0.0'
#     }
# ]

async def fetch(session, resource):
    url = resource["url"]
    print("Calling URL = ", url)
    async with session.get(url) as response:
        t = await response.json()
        print("URL ", url, "returned", str(t))
        result = {
            "resource": resource["resource"],
            "data": t
        }
    return result


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch(session, res)) for res in resources]
        responses = await asyncio.gather(*tasks)
        full_result = {}
        for response in responses:
            full_result[response["resource"]] = response["data"]

        print("\nFull Result = ", json.dumps(full_result, indent=2))


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

asyncio.run(main())
