import aiohttp
import asyncio


async def post_json(session, url):
    """
    Sends a POST request with a JSON body
    :param session:
    :param url:
    :return:
    """
    json = {"receiver": "+79170000000", "type": "text", "body": "Hello, World!"}
    async with session.post(url, json=json) as response:
        print('Post result:\n', await response.text())
        return await response.text()


async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:

        while True:
            posts = (post_json(session, 'http://0.0.0.0:8080/webhook/33') for _ in range(100))
            await asyncio.gather(*posts)
            await asyncio.sleep(5)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass  # Press Ctrl+C to stop
    finally:
        loop.close()
