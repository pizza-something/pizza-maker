from pizza_maker.entrypoint.common.uvicorn import run_dev


def main() -> None:
    run_dev("pizza_maker.entrypoint.fastapi.asgi:app")


if __name__ == "__main__":
    main()
