import logging
from pathlib import Path

from ctranslate2.specs.model_spec import ACCEPTED_MODEL_TYPES as ctranslate2_supported_compute_types
from environs import Env
from faster_whisper.utils import available_models
from marshmallow import validate

from litescriber_shared.config_utils import get_secret

APP_DIR = Path(__file__).resolve().parent
SRC_DIR = APP_DIR.parent
WORKER_DIR = SRC_DIR.parent
BACKEND_DIR = WORKER_DIR.parent
PROJECT_DIR = BACKEND_DIR.parent
env = Env()


# optionally load .env file
if env.bool("LITESCRIBER_READ_DOT_ENV_FILE", default=False):
    DOT_ENV_FILE_PATH: str = env.str("LITESCRIBER_DOT_ENV_FILE_PATH", default=BACKEND_DIR / ".env")
    env.read_env(DOT_ENV_FILE_PATH)

# Logging settings
# ---------------------------------------------------------------------------------------------------------------------
LOGGING_LEVEL: str = env.str("LITESCRIBER_LOGGING_LEVEL", default="INFO")
LOGGING_FORMAT: str = env.str(
    "LITESCRIBER_LOGGING_FORMAT",
    default="%(levelname)s %(asctime)s %(module)s:%(lineno)d %(process)d %(thread)d %(message)s",
)
logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT)


# RabbitMQ configuration
# ---------------------------------------------------------------------------------------------------------------------
RABBITMQ_URL: str | None = env.str("LITESCRIBER_RABBITMQ_URL", default=None)
RABBITMQ_API_BASE_URL: str | None = env.str("LITESCRIBER_RABBITMQ_API_BASE_URL", default=None)
RABBITMQ_DEFAULT_QUEUE: str | None = env.str("LITESCRIBER_RABBITMQ_DEFAULT_QUEUE", default=None)
RABBITMQ_AVAILABLE_QUEUES: list[str] = env.list(
    "LITESCRIBER_RABBITMQ_AVAILABLE_QUEUES", default=["tiny", "small", "base", "medium", "large"], subcast=str
)
RABBITMQ_USER: str | None = env.str("LITESCRIBER_RABBITMQ_USER", default=None)
RABBITMQ_PASSWORD: str | None = get_secret(env, "LITESCRIBER_RABBITMQ_PASSWORD", default=None)

# Whisper configuration
# ---------------------------------------------------------------------------------------------------------------------
WHISPER_AVAILABLE_MODELS: list[str] = available_models()
WHISPER_AVAILBLE_DEVICES: list[str] = ["cpu", "gpu", "cuda"]
WHISPER_MODEL_PATH: str | None = env.str("LITESCRIBER_WHISPER_MODEL_PATH", default=None)
WHISPER_DEFAULT_MODEL_SIZE: str = env.str(
    "LITESCRIBER_WHISPER_DEFAULT_MODEL_SIZE", default="base", validate=validate.OneOf(WHISPER_AVAILABLE_MODELS)
)
WHISPER_DEFAULT_DEVICE: str = env.str(
    "LITESCRIBER_WHISPER_DEFAULT_DEVICE", default="cpu", validate=validate.OneOf(WHISPER_AVAILBLE_DEVICES)
)
WHISPER_DEFAULT_COMPUTE_TYPE: str = env.str(
    "LITESCRIBER_WHISPER_DEFAULT_COMPUTE_TYPE",
    default="int8",
    validate=validate.OneOf(ctranslate2_supported_compute_types),
)
WHISPER_DEFAULT_BEAM_SIZE: int = env.int("LITESCRIBER_WHISPER_DEFAULT_BEAM_SIZE", default=5)
WHISPER_DEFAULT_CPU_THREADS: int = env.int("LITESCRIBER_WHISPER_DEFAULT_CPU_THREADS", default=0)
WHISPER_DEFAULT_NUM_WORKERS: int = env.int("LITESCRIBER_WHISPER_DEFAULT_NUM_WORKERS", default=1)
WHISPER_DEFAULT_DOWNLOAD_ROOT: str = env.str("LITESCRIBER_WHISPER_DEFAULT_DOWNLOAD_ROOT", default=None)
WHISPER_AUDIO_MAX_DURATION_LIMIT_SECONDS: int = env.int(
    "LITESCRIBER_WHISPER_AUDIO_MAX_DURATION_LIMIT_SECONDS", default=60 * 60 * 10
)

# Gateway configuration
# ---------------------------------------------------------------------------------------------------------------------
GATEWAY_API_BASE_URL: str | None = env.str("LITESCRIBER_GATEWAY_API_BASE_URL", default=None)
GATEWAY_API_TOKEN: str | None = get_secret(env, "LITESCRIBER_GATEWAY_API_TOKEN", default=None)
