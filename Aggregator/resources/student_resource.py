from pydantic import BaseModel
import asyncio
import aiohttp
import json
import time
import requests


class Student(BaseModel):
    name: str


class StudentResource:
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

    async def get_item(self, item: Student = None, sleep=5) -> str:
        # Simulate an asynchronous operation
        if item and item.name:
            n = item.name
        else:
            n = "Item with no name."
        await asyncio.sleep(sleep)
        return f"Hello, {n}! This is an asynchronous response."

    @classmethod
    async def fetch(cls, session, resource):
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

    async def get_student_async(self):
        full_result = None
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(
                StudentResource.fetch(session, res)) for res in StudentResource.resources]
            responses = await asyncio.gather(*tasks)
            full_result = {}
            for response in responses:
                full_result[response["resource"]] = response["data"]
            end_time = time.time()
            full_result["elapsed_time"] = end_time - start_time

            return full_result

            # print("\nFull Result = ", json.dumps(full_result, indent=2))

    async def get_student_sync(self):
        full_result = None
        start_time = time.time()

        full_result = {}

        for r in StudentResource.resources:
            response = requests.get(r["url"])
            full_result[r["resource"]] = response.json()
        end_time = time.time()
        full_result["elapsed_time"] = end_time - start_time

        return full_result

