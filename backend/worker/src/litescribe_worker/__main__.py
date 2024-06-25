import logging

import click
from ctranslate2.specs.model_spec import ACCEPTED_MODEL_TYPES as ctranslate2_supported_compute_types

from litescribe_worker import config, consumer, gateway_client, transcriber
from litescribe_worker.rabbitmq_helper import get_consumer_count


@click.command()
@click.option(
    "--queue",
    type=click.Choice(config.RABBITMQ_AVAILABLE_QUEUES),
    default=config.RABBITMQ_DEFAULT_QUEUE,
    help="Queue name.",
)
@click.option("--model-path", type=str, default=config.WHISPER_MODEL_PATH, help="Path to the model.")
@click.option(
    "--model-size",
    type=click.Choice(config.WHISPER_AVAILABLE_MODELS),
    default=config.WHISPER_DEFAULT_MODEL_SIZE,
    help="Model size.",
)
@click.option(
    "--device",
    type=click.Choice(config.WHISPER_AVAILBLE_DEVICES),
    default=config.WHISPER_DEFAULT_DEVICE,
    help="Device.",
)
@click.option(
    "--compute-type",
    type=click.Choice(ctranslate2_supported_compute_types),
    default=config.WHISPER_DEFAULT_COMPUTE_TYPE,
    help="Compute type.",
)
@click.option("--beam-size", type=int, default=config.WHISPER_DEFAULT_BEAM_SIZE, help="Beam size.")
@click.option("--cpu-threads", type=int, default=config.WHISPER_DEFAULT_CPU_THREADS, help="CPU threads.")
@click.option("--num-workers", type=int, default=config.WHISPER_DEFAULT_NUM_WORKERS, help="Number of workers.")
@click.option("--download-root", type=str, default=config.WHISPER_DEFAULT_DOWNLOAD_ROOT, help="Download root.")
@click.option(
    "--audio-max-duration-seconds",
    type=int,
    default=config.WHISPER_DEFAULT_AUDIO_MAX_DURATION_SECONDS,
    help="Maximum allowed audio duration in seconds.",
)
@click.option("--log-level", type=str, default=None, help="Logging level.")
@click.option("--rabbitmq-url", type=str, default=config.RABBITMQ_URL, help="RabbitMQ URL.")
@click.option("--rabbitmq-api-base_url", type=str, default=config.RABBITMQ_API_BASE_URL, help="RabbitMQ API URL.")
@click.option("--rabbitmq-user", type=str, default=config.RABBITMQ_USER, help="RabbitMQ user.")
@click.option("--rabbitmq-password", type=str, default=config.RABBITMQ_PASSWORD, help="RabbitMQ password.")
@click.option("--gateway-api-base-url", type=str, default=config.GATEWAY_API_BASE_URL, help="Gateway API base URL.")
@click.option("--gateway-api-token", type=str, default=config.GATEWAY_API_TOKEN, help="Gateway API token.")
@click.option("--storage-dir", type=str, default=config.FILE_STORAGE_DIR, help="Storage directory.")
def run(
    queue: str | None,
    model_path: str | None,
    model_size: str,
    device: str,
    compute_type: str,
    beam_size: int,
    cpu_threads: int,
    num_workers: int,
    download_root: str,
    audio_max_duration_seconds: int,
    log_level: str | None,
    rabbitmq_url: str | None,
    rabbitmq_api_base_url: str | None,
    rabbitmq_user: str | None,
    rabbitmq_password: str | None,
    gateway_api_base_url: str | None,
    gateway_api_token: str | None,
) -> None:
    if log_level:
        logging.basicConfig(level=log_level, format=config.LOGGING_FORMAT)

    if queue is None:
        raise ValueError("Queue is required.")
    if rabbitmq_url is None:
        raise ValueError("RabbitMQ URL is required.")
    if rabbitmq_api_base_url is None:
        raise ValueError("RabbitMQ API BASE URL is required.")
    if rabbitmq_user is None:
        raise ValueError("RabbitMQ user is required.")
    if rabbitmq_password is None:
        raise ValueError("RabbitMQ password is required.")
    if gateway_api_base_url is None:
        raise ValueError("Gateway API base URL is required.")
    if gateway_api_token is None:
        raise ValueError("Gateway API token is required.")

    click.echo("Starting with the following parameters:")
    click.echo(f"Queue: {queue}")
    click.echo(f"Model path: {model_path}")
    click.echo(f"Model size: {model_size}")
    click.echo(f"Device: {device}")
    click.echo(f"Compute type: {compute_type}")
    click.echo(f"Beam size: {beam_size}")
    click.echo(f"CPU threads: {cpu_threads}")
    click.echo(f"Number of workers: {num_workers}")
    click.echo(f"Download root: {download_root}")
    click.echo(f"Audio max duration seconds: {audio_max_duration_seconds}")
    click.echo(f"Log level: {log_level}")
    click.echo(f"RabbitMQ URL: {rabbitmq_url}")
    click.echo(f"RabbitMQ API BASE URL: {rabbitmq_api_base_url}")
    click.echo(f"RabbitMQ user: {rabbitmq_user}")
    click.echo("RabbitMQ password: ********")
    click.echo(f"Gateway API base URL: {gateway_api_base_url}")
    click.echo("Gateway API token: ********")

    transcriber_instance = transcriber.Transcriber(
        model_size_or_path=model_path or model_size,
        device=device,
        compute_type=compute_type,
        cpu_threads=cpu_threads,
        num_workers=num_workers,
        download_root=download_root,
        beam_size=beam_size,
        audio_max_duration_seconds=audio_max_duration_seconds,
    )

    consumer_count = get_consumer_count(
        rabbitmq_api_base_url=rabbitmq_api_base_url,
        rabbitmq_user=rabbitmq_user,
        rabbitmq_password=rabbitmq_password,
        queue_name=queue,
    )

    consumer_id = f"litescribe-{queue}-{consumer_count + 1}"

    click.echo(f"Consumer ID: {consumer_id}")

    gateway_client_instance = gateway_client.GatewayClient(
        gateway_api_base_url=gateway_api_base_url, gateway_api_token=gateway_api_token
    )

    consumer_instance = consumer.TranscribeConsumer(
        rabbitmq_url=rabbitmq_url,
        queue_name=queue,
        consumer_id=consumer_id,
        transcriber=transcriber_instance,
        gateway_client=gateway_client_instance,
    )

    try:
        consumer_instance.consume()
    except KeyboardInterrupt:
        raise  # FIXME


if __name__ == "__main__":
    run()
