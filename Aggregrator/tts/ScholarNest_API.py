

from fastapi import FastAPI

app = FastAPI()
#
from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/aggregate-data")
async def aggregate_data():
    async with httpx.AsyncClient() as client:
        student_response = await client.get("https://virtserver.swaggerhub.com/donald-f-ferguson/E6156Student/1.0.0/students/bb2101")
        sections_response = await client.get("https://virtserver.swaggerhub.com/Columbia-Classes/Sections/1.0.0/sections?uni=bb2101")
        projects_response = await client.get("https://virtserver.swaggerhub.com/Columbia-Classes/ProjectInfo/1.0.0/projects?uni=bb2021")

        student_data = student_response.json()
        sections_data = sections_response.json()
        projects_data = projects_response.json()

        full_result = {
            "student": student_data,
            "sections": sections_data,
            "projects": projects_data
        }

        return full_result


##############
# async def fetch_data(url: str):
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url)
#         return response.json()
#
# @app.get("/aggregate-data/")
# async def aggregate_data():
#     urls = [
#         # "https://virtserver.swaggerhub.com/donald-f-ferguson/E6156Student/1.0.0/students/bb2101",
#         # "https://virtserver.swaggerhub.com/Columbia-Classes/Sections/1.0.0/sections?uni=bb2101",
#         # "https://virtserver.swaggerhub.com/Columbia-Classes/ProjectInfo/1.0.0/projects?uni=bb2021"
#         'https://virtserver.swaggerhub.com/YC4140/scholarnest_activities/1.0.0'
#         'https://virtserver.swaggerhub.com/YC4140/scholarnest_user/1.0.0'
#         'https://virtserver.swaggerhub.com/YC4140/Scholarnest_papers/1.0.0'
#
#     ]
#
#     responses = await asyncio.gather(*(fetch_data(url) for url in urls))
#
#     result = {
#         "activities": responses[0],
#         "users": responses[1],
#         "papers": responses[2]
#     }
#
#     return result
