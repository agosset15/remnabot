import re


def to_snake_case(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def event_to_key(class_name: str) -> str:
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()
    formatted_key = snake.replace("_", "-")
    return f"event-{formatted_key}"
