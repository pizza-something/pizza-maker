from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from pizza_maker.application.create_pizza import CreatePizza
from pizza_maker.application.on_account_created import OnAccountCreated
from pizza_maker.application.ports.decoded_access_token import (
    DecodedAccessTokenWhen,
)
from pizza_maker.infrastructure.adapters.clock import LocalHostClock
from pizza_maker.infrastructure.adapters.decoded_access_token import (
    DecodedAccessTokenFromHS256JWTWhen,
)
from pizza_maker.infrastructure.adapters.map import MapToPostgres
from pizza_maker.infrastructure.adapters.pizzas import InPostgresPizzas
from pizza_maker.infrastructure.adapters.transaction import (
    InPostgresTransactionOf,
)
from pizza_maker.infrastructure.adapters.users import InPostgresUsers
from pizza_maker.infrastructure.typenv.envs import RuntimeEnvs
from pizza_maker.infrastructure.types import JWT
from pizza_maker.presentation.faststream.routes.on_account_created import (
    on_account_created_route,
)


type PostgresEngine = AsyncEngine
type PostgresSession = AsyncSession


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    provide_runtime_envs = provide(source=RuntimeEnvs.load, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def provide_postgres_engine(
        self, envs: RuntimeEnvs
    ) -> PostgresEngine:
        return create_async_engine(envs.postgres_url)

    @provide(scope=Scope.APP)
    async def provide_kafka_broker(
        self, envs: RuntimeEnvs
    ) -> KafkaBroker:
        broker = KafkaBroker(envs.kafka_url)
        broker.include_routers(
            on_account_created_route
        )

        return broker

    @provide
    async def provide_postgres_esion(
        self, engine: PostgresEngine
    ) -> AsyncIterator[PostgresSession]:
        session = AsyncSession(engine, autoflush=False, autobegin=False)
        async with session:
            yield session

    @provide
    def provide_clock(self) -> LocalHostClock:
        return LocalHostClock()

    @provide
    def provide_decoded_access_token_when(
        self, envs: RuntimeEnvs
    ) -> DecodedAccessTokenWhen[JWT]:
        return DecodedAccessTokenFromHS256JWTWhen(secret=envs.jwt_secret)

    @provide
    def provide_users(self, session: PostgresSession) -> InPostgresUsers:
        return InPostgresUsers(session=session)

    @provide
    def provide_pizzas(self, session: PostgresSession) -> InPostgresPizzas:
        return InPostgresPizzas(session=session)

    @provide(scope=Scope.APP)
    def provide_in_postgres_transaction_of(
        self
    ) -> InPostgresTransactionOf:
        return InPostgresTransactionOf()

    @provide(scope=Scope.APP)
    def provide_map_to(
        self
    ) -> MapToPostgres:
        return MapToPostgres()

    provide_on_account_created = provide(
        OnAccountCreated[InPostgresUsers],
        provides=OnAccountCreated,
    )

    provide_create_pizza = provide(
        CreatePizza[JWT, InPostgresUsers, InPostgresPizzas],
        provides=CreatePizza[str],
    )
