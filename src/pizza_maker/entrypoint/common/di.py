from collections.abc import AsyncIterator

from dishka import AnyOf, Provider, Scope, provide
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from pizza_maker.application.create_pizza import CreatePizza
from pizza_maker.application.on_account_created import OnAccountCreated
from pizza_maker.application.ports.clock import Clock
from pizza_maker.application.ports.decoded_access_token import (
    DecodedAccessTokenWhen,
)
from pizza_maker.application.ports.event_queue import EventQueue
from pizza_maker.application.ports.map import MapTo
from pizza_maker.application.ports.pizzas import Pizzas
from pizza_maker.application.ports.transaction import TransactionOf
from pizza_maker.application.ports.users import Users
from pizza_maker.infrastructure.adapters.clock import LocalHostClock
from pizza_maker.infrastructure.adapters.decoded_access_token import (
    DecodedAccessTokenFromHS256JWTWhen,
)
from pizza_maker.infrastructure.adapters.event_queue import KafkaEventQueue
from pizza_maker.infrastructure.adapters.map import MapToPostgres
from pizza_maker.infrastructure.adapters.pizzas import InPostgresPizzas
from pizza_maker.infrastructure.adapters.transaction import (
    InPostgresTransactionOf,
)
from pizza_maker.infrastructure.adapters.users import InPostgresUsers
from pizza_maker.infrastructure.faststream.publisher_regitry import (
    KafkaPublisherRegistry,
)
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

    provide_kafka_publisher_registry = provide(
        KafkaPublisherRegistry, scope=Scope.APP
    )

    provide_event_queue = provide(
        KafkaEventQueue,
        provides=AnyOf[KafkaEventQueue, EventQueue],
        scope=Scope.APP,
    )

    @provide
    async def provide_postgres_esion(
        self, engine: PostgresEngine
    ) -> AsyncIterator[PostgresSession]:
        session = AsyncSession(engine, autoflush=False, autobegin=False)
        async with session:
            yield session

    @provide
    def provide_clock(self) -> AnyOf[LocalHostClock, Clock]:
        return LocalHostClock()

    @provide
    def provide_decoded_access_token_when(
        self, envs: RuntimeEnvs
    ) -> AnyOf[DecodedAccessTokenFromHS256JWTWhen, DecodedAccessTokenWhen[JWT]]:
        return DecodedAccessTokenFromHS256JWTWhen(secret=envs.jwt_secret)

    @provide
    def provide_users(
        self, session: PostgresSession
    ) -> AnyOf[InPostgresUsers, Users]:
        return InPostgresUsers(session=session)

    @provide
    def provide_pizzas(
        self, session: PostgresSession
    ) -> AnyOf[InPostgresPizzas, Pizzas]:
        return InPostgresPizzas(session=session)

    @provide(scope=Scope.APP)
    def provide_in_postgres_transaction_of(
        self
    ) -> AnyOf[
        InPostgresTransactionOf,
        TransactionOf[tuple[InPostgresPizzas, InPostgresUsers]],
        TransactionOf[tuple[InPostgresUsers]],
    ]:
        return InPostgresTransactionOf()

    @provide(scope=Scope.APP)
    def provide_map_to(
        self
    ) -> AnyOf[
        MapToPostgres,
        MapTo[tuple[InPostgresUsers]],
        MapTo[tuple[InPostgresPizzas]],
    ]:
        return MapToPostgres()

    provide_on_account_created = provide(
        OnAccountCreated[InPostgresUsers],
        provides=OnAccountCreated,
    )

    provide_create_pizza = provide(
        CreatePizza[JWT, InPostgresUsers, InPostgresPizzas],
        provides=CreatePizza[str],
    )
