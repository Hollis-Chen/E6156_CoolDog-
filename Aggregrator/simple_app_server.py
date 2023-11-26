from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import asyncio
import uvicorn
# from resources.student_resource import StudentResource, Student

# from resources.ScholarNest_resource import Resource, user
from resources.ScholarNest_resource import scholarResource,user


app = FastAPI()

# ##########################
#### my testbench
######################################

# example_instance = StudentResource()
# example_instance = Resource()
example_instance = scholarResource()



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


@app.get("/get_item")
async def async_call(item_name: str = None):
    result = await example_instance.get_item(item_name)
    return JSONResponse(content={"message": result})


# @app.get("/get_student_async")
@app.get("/get_scholarnest_async")
async def async_call():
    result = await example_instance.get_scholarnest_async()
    return JSONResponse(content={"result": result})


# @app.get("/get_student_sync")
@app.get("/get_scholarnestnest_sync")
async def async_call():
    result_sync = await example_instance.get_scholarnest_sync()
    return JSONResponse(content={"result_sync": result_sync})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
##########################################################################



# ###################################################
#
# ##########   simple example
# #############################################
#
# app = FastAPI()
# scholarNest_instance = ScholarNestResource()
#
# @app.get("/")
# async def home_page():
#     home_page_content = """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>ScholarNest Aggregator Service</title>
#     </head>
#     <body>
#         <header>
#             <h1>Welcome to ScholarNest Aggregator Service</h1>
#         </header>
#         <section>
#             <h2>Usage</h2>
#             <p>Please go to <a href="/docs">the OpenAPI docs page for this app.</a>
#         </section>
#         <footer>
#             <p>&copy; 2023 ScholarNest. All rights reserved.</p>
#         </footer>
#     </body>
#     </html>
#     """
#     return HTMLResponse(home_page_content)
#
# @app.get("/aggregate_async")
# async def aggregate_data_async():
#     result = await scholarNest_instance.aggregate_data_async()
#     return JSONResponse(content=result)
#
# @app.get("/aggregate_sync")
# def aggregate_data_sync():
#     result = scholarNest_instance.aggregate_data_sync()
#     return JSONResponse(content=result)
#
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
#
# # ###################################################################




# ############################
########## working class example
###################################
# from fastapi import FastAPI
# from fastapi.responses import JSONResponse, HTMLResponse
# from pydantic import BaseModel
# import asyncio
# import uvicorn
# from resources.student_resource import StudentResource, Student
#
# app = FastAPI()
#
# example_instance = StudentResource()
#
#
# @app.get("/")
# async def home_page():
#     home_page = \
#         """
#         <!DOCTYPE html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>Simple Composite Service Example</title>
#         </head>
#         <body>
#
#             <header>
#                 <h1>Welcome to Simple Composite Example</h1>
#             </header>
#
#             <section>
#                 <h2>Usage</h2>
#                 <p>Please go to <a href="/docs">the OpenAPI docs page for this app.</a>
#             </section>
#
#             <footer>
#                 <p>&copy; 2023 Donald Ferguson. All rights reserved.</p>
#             </footer>
#
#         </body>
#         </html>
#         """
#     return HTMLResponse(home_page)
#
#
# @app.get("/get_item")
# async def async_call(item_name: str = None):
#     result = await example_instance.get_item(item_name)
#     return JSONResponse(content={"message": result})
#
#
# @app.get("/get_student_async")
# async def async_call():
#     result = await example_instance.get_student_async()
#     return JSONResponse(content={"students": result})
#
#
# @app.get("/get_student_sync")
# async def async_call():
#     result = await example_instance.get_student_sync()
#     return JSONResponse(content={"students": result})
#
#
# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
#
##########################################################
