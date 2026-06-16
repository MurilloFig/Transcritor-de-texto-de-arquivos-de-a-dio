\
from pathlib import Path
from datetime import datetime
from faster_whisper import WhisperModel


MODEL_SIZE = "medium"

SUPPORTED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".ogg",
    ".flac",
    ".mp4",
    ".webm",
}

BASE_DIR = Path(__file__).resolve().parent.parent
TRANSCRIPTION_DIR = BASE_DIR / "transcriptions"
TRANSCRIPTION_DIR.mkdir(exist_ok=True)


class AudioTranscriber:
    def __init__(self) -> None:
        self.model = WhisperModel(
            MODEL_SIZE,
            device="cpu",
            compute_type="int8"
        )

    def validate_file(self, file_path: str) -> None:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError("Arquivo não encontrado.")

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Formato não suportado: {path.suffix}. "
                f"Formatos aceitos: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )

    def transcribe(self, file_path: str, language: str = "auto") -> dict:
        self.validate_file(file_path)

        selected_language = None if language == "auto" else language

        segments, info = self.model.transcribe(
            file_path,
            language=selected_language,
            beam_size=5,
            vad_filter=True,
            vad_parameters={
                "min_silence_duration_ms": 500
            }
        )

        full_text_parts = []
        detailed_segments = []

        for segment in segments:
            text = segment.text.strip()

            if not text:
                continue

            full_text_parts.append(text)

            detailed_segments.append({
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": text
            })

        final_text = " ".join(full_text_parts).strip()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = Path(file_path).stem.replace(" ", "_")
        output_file = TRANSCRIPTION_DIR / f"{original_name}_{timestamp}.txt"

        output_file.write_text(final_text, encoding="utf-8")

        return {
            "text": final_text,
            "detected_language": info.language,
            "language_probability": round(info.language_probability, 4),
            "duration": round(info.duration, 2),
            "segments": detailed_segments,
            "output_file": str(output_file)
        }
