#
# This example is a modification (slight) of
# https://martinxpn.medium.com/making-requests-with-asyncio-in-python-78-100-days-of-python-eb1570b3f986
#
import asyncio
import aiohttp

urls = [
    'http://www.google.com',
    'http://www.facebook.com',
    'http://www.twitter.com'
]


async def fetch(session, url):
    print("Calling URL = ", url)
    async with session.get(url) as response:
        t = await response.text()
        print("URL ", url, "returned", len(t), "bytes")
        result = t
    return t


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch(session, url)) for url in urls]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            print("Length = ", len(response))


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

asyncio.run(main())
