import logging
from pathlib import Path

from environs import Env


def get_secret(env: Env, name: str, default: object = None) -> str:
    if value := env.str(name, None):
        logging.warning(f"{name} is set in the environment. Consider using a file secret.")
        return value

    if value := env.str(f"{name}_FILE", None):
        fp = Path(value)
        if not fp.is_file():
            raise FileNotFoundError(f"File not found: {fp}.")
        return fp.read_text()

    if default:
        return default

    raise ValueError(f"Secret {name} not found in environment or file.")
