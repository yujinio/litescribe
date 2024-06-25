import logging
from time import perf_counter

from faster_whisper.transcribe import WhisperModel


class Transcriber:
    model: WhisperModel
    beam_size: int
    audio_max_duration_seconds: int

    def __init__(
        self,
        model_size_or_path: str,
        device: str,
        compute_type: str,
        cpu_threads: int,
        num_workers: int,
        download_root: str,
        beam_size: int,
        audio_max_duration_seconds: int,
    ) -> None:
        self.beam_size = beam_size
        self.audio_max_duration_seconds = audio_max_duration_seconds

        start = perf_counter()
        self.model = WhisperModel(
            model_size_or_path=model_size_or_path,
            device=device,
            compute_type=compute_type,
            cpu_threads=cpu_threads,
            num_workers=num_workers,
            download_root=download_root,
        )
        logging.debug(f"WhisperModel initialization ({model_size_or_path}) took {perf_counter() - start:.2f} seconds.")

    def transcribe_to_string(self, fp: str) -> str:
        segments, info = self.model.transcribe(audio=fp, beam_size=self.beam_size)

        if info.duration > self.audio_max_duration_seconds:
            raise ValueError(
                f"Audio duration of {info.duration} exceeds maximum allowed duration of {self.audio_max_duration_seconds} seconds."
            )

        start = perf_counter()
        text = "".join(segment.text for segment in segments)
        logging.debug(
            f"Transcription of audio with duration {info.duration} took {perf_counter() - start:.2f} seconds."
        )

        return text
