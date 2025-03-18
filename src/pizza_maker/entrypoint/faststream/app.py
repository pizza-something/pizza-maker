import asyncio

from faststream import FastStream

from pizza_maker.entrypoint.faststream.di import container


async def get_app() -> FastStream:
    return await container.get(FastStream)


app = asyncio.run(get_app())
