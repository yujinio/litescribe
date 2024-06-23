from dataclasses import dataclass


@dataclass
class TranscriptionRequest:
    request_id: str
    fp: str


@dataclass
class TranscripionResult:
    request_id: str
    transcription: str
