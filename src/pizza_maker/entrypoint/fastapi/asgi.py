from pizza_maker.entrypoint.common.asgi import LazyASGIApp
from pizza_maker.entrypoint.fastapi.di import container
from pizza_maker.presentation.fastapi.app import app_from


app = LazyASGIApp(app_factory=lambda: app_from(container))
