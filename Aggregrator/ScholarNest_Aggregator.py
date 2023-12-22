from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import asyncio
import uvicorn
import aiohttp

# from resources.student_resource import StudentResource, Student

# from resources.ScholarNest_resource import Resource, user
from resources.ScholarNest_resource import ScholarResource,User

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Set up CORS middleware - replace 'your-flask-app-domain.com' with your actual domain
origins = [
    "http://3.210.123.50.nip.io:5000",
    "http://3.210.123.50:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins (domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)





#
# #################
# #####ScholarResouece:
# ######################
scholar_resource_instance = ScholarResource()



@app.get("/")
async def home_page():
    home_page = \
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ScholarNest Aggrator Service Example</title>
        </head>
        <body>

            <header>
                <h1>Welcome to ScholarNest Aggrator Example</h1>
            </header>

            <section>
                <h2>Usage</h2>
                <p>Please go to <a href="/docs">the OpenAPI docs page for this app.</a>
            </section>

            <footer>
                <p>&copy; 2023 Team CoolDog. All rights reserved.</p>
            </footer>

        </body>
        </html>
        """
    return HTMLResponse(home_page)
#     return "welcome";



@app.post("/aggregate_data")
async def aggregate_data(user_id: str):
    try:
        user_group = await scholar_resource_instance.allocate_group(user_id)
        async with aiohttp.ClientSession() as session:
            papers = await scholar_resource_instance.fetch_papers(session, user_group["id"])
        return {"group": user_group, "papers": papers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/user_info/{user_id}")
async def get_user_info(user_id: str):
    try:
        user_group = await scholar_resource_instance.id_check(user_id)
        print(user_group)

        # Check if the user is not grouped
        if "message" in user_group and user_group["message"] == "User not grouped":
            return user_group

        async with aiohttp.ClientSession() as session:
            papers = await scholar_resource_instance.fetch_papers(session, user_group["id"])
        return {"group": user_group, "papers": papers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/user_papers/{user_id}")
async def get_user_paper_info(user_id: str):
    try:


        async with aiohttp.ClientSession() as session:
            papers = await scholar_resource_instance.fetch_personal_papers(session)
        return {"papers": papers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
#########################################################################


