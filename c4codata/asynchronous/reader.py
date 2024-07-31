import requests

import asyncio
import aiohttp


async def fetch(session: aiohttp.ClientSession, url) -> None:
    print(f"Query {url}")
    async with session.get(url) as resp:
        body = await resp.json()
        return body


async def aget(auth, url) -> dict:
    async with aiohttp.ClientSession(
        auth=aiohttp.BasicAuth(*auth)
    ) as session:
        session.headers.update({'x-csrf-token': 'fetch', 'Accept': 'application/json'})
        data = await fetch(session, url)
        return data


def read_from_odata(auth, url_list):
    
    urls = [asyncio.ensure_future(aget(auth, url)) for url in url_list]

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*urls))
    loop.close()
    return results

