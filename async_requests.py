import aiohttp
import asyncio


async def send(session):
    data = aiohttp.FormData()
    data.add_field(
        'report_file',
        open('sample_data/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.csv', 'rb'),
        content_type='text/tab-separated-values'
    )
    url = 'http://0.0.0.0:8000/api/v1/create_report/'
    await session.post(url, data=data)


async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[send(session) for x in range(100)])

if __name__ == "__main__":
    asyncio.run(main())
