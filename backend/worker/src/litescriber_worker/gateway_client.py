import httpx

from litescriber_shared.dto import TranscripionResult
from litescriber_shared.serialization import serialize_transcription_request


class GatewayClient:
    gateway_api_base_url: str
    gateway_api_token: str

    def __init__(self, gateway_api_base_url: str, gateway_api_token: str) -> None:
        self.gateway_api_base_url = gateway_api_base_url
        self.gateway_api_token = gateway_api_token

    def post_transcription_result(self, request_id: str, text: str) -> None:
        result = TranscripionResult(request_id=request_id, transcription=text)
        payload = serialize_transcription_request(result)
        response = httpx.post(
            f"{self.gateway_api_base_url}/results",
            headers={"Authorization": f"Bearer {self.gateway_api_token}", "Content-Type": "application/msgpack"},
            data=payload,
        )
        response.raise_for_status()
