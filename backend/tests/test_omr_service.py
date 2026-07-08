from pathlib import Path

import pytest

from app.omr.audiveris import AudiverisResult
from app.omr.config import OMRSettings
from app.omr.errors import OMRValidationError
from app.omr.service import transcribe_score_to_musicxml


def test_transcribe_score_validates_then_runs_audiveris(tmp_path: Path):
    input_path = tmp_path / "score.jpg"
    input_path.write_bytes(b"fake image")
    output_dir = tmp_path / "omr-output"
    output_dir.mkdir()
    settings = OMRSettings()
    calls = []

    def fake_run_audiveris(path: Path, output: Path, received_settings: OMRSettings) -> AudiverisResult:
        calls.append((path, output, received_settings))
        musicxml_path = output / "score.musicxml"
        musicxml_path.write_text("<score-partwise />", encoding="utf-8")
        return AudiverisResult(musicxml_path=musicxml_path, stdout="", stderr="")

    result = transcribe_score_to_musicxml(
        input_path=input_path,
        suffix=".jpg",
        output_dir=output_dir,
        settings=settings,
        audiveris_runner=fake_run_audiveris,
    )

    assert calls == [(input_path, output_dir, settings)]
    assert result.musicxml_path == output_dir / "score.musicxml"
    assert result.engine == "audiveris"
    assert result.message == "OMR 识别完成，请人工核对结果。"


def test_transcribe_score_validation_failure_does_not_run_audiveris(tmp_path: Path):
    input_path = tmp_path / "score.txt"
    input_path.write_text("not an omr file", encoding="utf-8")
    settings = OMRSettings()
    called = False

    def fake_run_audiveris(path: Path, output: Path, received_settings: OMRSettings) -> AudiverisResult:
        nonlocal called
        called = True
        raise AssertionError("runner should not be called")

    with pytest.raises(OMRValidationError):
        transcribe_score_to_musicxml(
            input_path=input_path,
            suffix=".txt",
            output_dir=tmp_path,
            settings=settings,
            audiveris_runner=fake_run_audiveris,
        )

    assert called is False
