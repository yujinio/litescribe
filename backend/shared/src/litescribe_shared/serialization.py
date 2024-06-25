from dataclasses import asdict

import msgpack

from litescribe_shared.dto import TranscripionResult, TranscriptionRequest


def serialize_transcription_request(request: TranscriptionRequest) -> bytes:
    return serialize_dict(asdict(request))


def deserialize_transcription_request(data: bytes) -> TranscriptionRequest:
    unpacked_data = deserialize_dict(data)
    return TranscriptionRequest(**unpacked_data)


def serialize_transcription_result(result: TranscripionResult) -> bytes:
    return serialize_dict(asdict(result))


def deserialize_transcription_result(data: bytes) -> TranscripionResult:
    unpacked_data = deserialize_dict(data)
    return TranscripionResult(**unpacked_data)


def serialize_dict(data: dict) -> bytes:
    return msgpack.packb(data)


def deserialize_dict(data: bytes) -> dict:
    return msgpack.unpackb(data)
