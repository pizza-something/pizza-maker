import asyncio

from pizza_maker.entrypoint.faststream.di import container
from pizza_maker.presentation.faststream.app import app_from


app = asyncio.run(app_from(container))

