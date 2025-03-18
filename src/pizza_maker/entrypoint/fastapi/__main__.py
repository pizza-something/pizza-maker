from pizza_maker.entrypoint.common.uvicorn import run_dev


def main() -> None:
    run_dev("pizza_maker.entrypoint.web_service.asgi:app")


if __name__ == "__main__":
    main()
