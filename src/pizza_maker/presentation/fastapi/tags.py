from enum import Enum


class Tag(Enum):
    user = "User"
    pizza = "Pizza"
    monitoring = "Monitoring"


tags_metadata = [
    {
        "name": Tag.user.value,
        "description": "Current user endpoints.",
    },
    {
        "name": Tag.pizza.value,
        "description": "Pizza endpoints.",
    },
    {
        "name": Tag.monitoring.value,
        "description": "Endpoints for monitoring.",
    },
]
