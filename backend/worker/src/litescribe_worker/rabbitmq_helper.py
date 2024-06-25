import httpx


def get_consumer_count(rabbitmq_api_base_url: str, rabbitmq_user: str, rabbitmq_password: str, queue_name: str) -> int:
    response = httpx.get(f"{rabbitmq_api_base_url}/api/queues/{queue_name}/", auth=(rabbitmq_user, rabbitmq_password))
    response.raise_for_status()
    queue_info = response.json()
    return queue_info.get("consumers", 0)
