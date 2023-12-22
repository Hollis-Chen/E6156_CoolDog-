from synchronous_Asynchronous.resources.student_resource import StudentResource
import json
import asyncio


async def t1():
    it = StudentResource()

    result = await it.get_student()
    if result:
        print("t1: result = \n", json.dumps(result, indent=2))
    else:
        print("Did not get a result.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(t1())
