from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from app.omr.audiveris import AudiverisResult, run_audiveris
from app.omr.config import OMRSettings
from app.omr.validation import validate_omr_upload


@dataclass(frozen=True)
class OMRTranscriptionResult:
    musicxml_path: Path
    engine: str
    message: str


AudiverisRunner = Callable[[Path, Path, OMRSettings], AudiverisResult]


def transcribe_score_to_musicxml(
    input_path: Path,
    suffix: str,
    output_dir: Path,
    settings: OMRSettings,
    audiveris_runner: AudiverisRunner = run_audiveris,
) -> OMRTranscriptionResult:
    validate_omr_upload(input_path, suffix, settings)
    result = audiveris_runner(input_path, output_dir, settings)
    return OMRTranscriptionResult(
        musicxml_path=result.musicxml_path,
        engine="audiveris",
        message="OMR 识别完成，请人工核对结果。",
    )
