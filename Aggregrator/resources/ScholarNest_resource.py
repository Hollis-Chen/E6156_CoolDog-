from pydantic import BaseModel
import asyncio
import aiohttp
import json
import time
from pydantic import BaseModel
import asyncio
import aiohttp
import json
import time
import requests
from aiohttp import ClientSession



#####################################
#########  my testbench
#########################################
class user(BaseModel):
    name: str




class scholarResource:
    #
    # These endpoints are on SwaggerHub mock APIs
    #

    resources = [
        {
            "resource": "activities",
            "url": 'https://virtserver.swaggerhub.com/YC4140/scholarnest_activities/1.0.0'
        },
        {
            "resource": "users",
            "url": 'https://virtserver.swaggerhub.com/YC4140/scholarnest_user/1.0.0'
        },
        {
            "resource": "papers",
            "url": 'https://virtserver.swaggerhub.com/YC4140/Scholarnest_papers/1.0.0'
        }
    ]


    async def get_item(self, item: user = None, sleep=5) -> str:
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

    # async def fetch(self, url):
    #     async with ClientSession() as session:
    #         async with session.get(url) as response:
    #             if response.headers.get('Content-Type') == 'application/json':
    #                 return await response.json()
    #             else:
    #                 content = await response.text()
    #                 print(f"Non-JSON response: {content}")
    #                 return {"error": "Non-JSON response received"}

    # async def fetch(cls, session, resource):
    #     url = resource["url"]
    #     async with session.get(url) as response:
    #         if response.headers.get('Content-Type') == 'application/json':
    #             return await response.json()
    #         else:
    #             # Handle non-JSON responses
    #             content = await response.text()
    #             print(f"Non-JSON response: {content}")
    #             return {"error": "Non-JSON response received"}
    #



    # async def get_scholarnest_async(self):
    #     full_result = None
    #     start_time = time.time()
    #     async with aiohttp.ClientSession() as session:
    #         tasks = [asyncio.ensure_future(Resource.fetch(session, res)) for res in Resource.resources]
    #         responses = await asyncio.gather(*tasks)
    #         full_result = {}
    #         for response in responses:
    #             full_result[response["resource"]] = response["data"]
    #         end_time = time.time()
    #         full_result["elapsed_time"] = end_time - start_time
    #
    #         return full_result
    #     print("\nFull Result = ", json.dumps(full_result, indent=2))

    async def get_scholarnest_async(self):
        full_result = {}
        start_time = time.time()

        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(self.fetch_async(session, res)) for res in self.resources]
            responses = await asyncio.gather(*tasks)

            for res, response in zip(self.resources, responses):
                if response.headers.get('Content-Type') == 'application/json':
                    try:
                        full_result[res["resource"]] = await response.json()
                    except ValueError as e:
                        # Handle the case where JSON parsing fails
                        full_result[res["resource"]] = {"error": str(e)}
                else:
                    # Handle non-JSON responses
                    text = await response.text()
                    full_result[res["resource"]] = {"content": text}

        end_time = time.time()
        full_result["elapsed_time"] = end_time - start_time
        return full_result

    async def fetch_async(self, session, resource):
        async with session.get(resource["url"]) as response:
            return response

# ########
#     ####old code for testing
#     #####
#
#     async def get_scholarnest_async(self):
#         full_result = None
#         start_time = time.time()
#         async with aiohttp.ClientSession() as session:
#             tasks = [asyncio.ensure_future(
#                 scholarResource.fetch(session, res)) for res in scholarResource.resources]
#             responses = await asyncio.gather(*tasks)
#             full_result = {}
#             for response in responses:
#                 full_result[response["resource"]] = response["data"]
#             end_time = time.time()
#             full_result["elapsed_time"] = end_time - start_time
#
#             return full_result
#
#     async def get_scholarnest_sync(self):
#         full_result = None
#         start_time = time.time()
#
#         full_result = {}
#
#         for r in scholarResource.resources:
#             response = requests.get(r["url"])
#             full_result[r["resource"]] = response.json()
#         end_time = time.time()
#         full_result["elapsed_time"] = end_time - start_time
#
#         return full_result
#     #################################

    #######
    ## working code
    ########
    async def get_scholarnest_sync(self):
        full_result = None
        start_time = time.time()

        full_result = {}
        for r in self.resources:
            response = requests.get(r["url"])
            if response.headers.get('Content-Type') == 'application/json':
                try:
                    full_result[r["resource"]] = response.json()
                except ValueError as e:
                    # Handle the case where JSON parsing fails
                    full_result[r["resource"]] = {"error": str(e)}
            else:
                # Handle non-JSON responses
                full_result[r["resource"]] = {"content": response.text}

        return full_result

#######################################################

############################
########## simple example
#################################

#
#
# class ScholarNestResource:
#     resources = [
#         {
#             "resource": "users",
#             "url": 'https://virtserver.swaggerhub.com/YC4140/scholarnest_users/1.0.0/api/users'
#         },
#         {
#             "resource": "papers",
#             "url": 'https://virtserver.swaggerhub.com/YC4140/Scholarnest_papers/1.0.0/api/papers'
#         },
#         {
#             "resource": "groups",
#             "url": 'https://virtserver.swaggerhub.com/YC4140/Scholarnest_groups/1.0.0/api/groups'
#         }
#     ]
#
#     @classmethod
#     async def fetch_async(cls, session, resource):
#         url = resource["url"]
#         async with session.get(url) as response:
#             data = await response.json()
#             return {"resource": resource["resource"], "data": data}
#
#     async def aggregate_data_async(self):
#         async with aiohttp.ClientSession() as session:
#             tasks = [asyncio.ensure_future(self.fetch_async(session, res)) for res in self.resources]
#             responses = await asyncio.gather(*tasks)
#             return {res["resource"]: res["data"] for res in responses}
#
#     def fetch_sync(self, resource):
#         response = requests.get(resource["url"])
#         return {"resource": resource["resource"], "data": response.json()}
#
#     def aggregate_data_sync(self):
#         return {res["resource"]: self.fetch_sync(res)["data"] for res in self.resources}
#
# ##############################################################



