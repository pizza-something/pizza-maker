import asyncio

from pizza_maker.entrypoint.faststream.app import app


async def amain() -> None:
    await app.run()


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()
