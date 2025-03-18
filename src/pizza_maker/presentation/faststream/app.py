from faststream import FastStream
from faststream.kafka import KafkaBroker


def app_with(broker: KafkaBroker) -> FastStream:
    return FastStream(broker)
