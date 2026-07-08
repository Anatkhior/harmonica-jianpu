from pathlib import Path
import subprocess

import pytest

from app.omr.audiveris import (
    AudiverisResult,
    build_audiveris_command,
    find_generated_musicxml,
    run_audiveris,
)
from app.omr.config import OMRSettings
from app.omr.errors import OMRConfigurationError, OMREngineError, OMRTimeoutError


def test_build_audiveris_command():
    input_path = Path("uploads/score.png")
    output_dir = Path("tmp/omr-output")
    settings = OMRSettings(audiveris_cmd="audiveris-cli")

    assert build_audiveris_command(input_path, output_dir, settings) == [
        "audiveris-cli",
        "-batch",
        "-transcribe",
        "-export",
        "-output",
        str(output_dir),
        str(input_path),
    ]


def test_find_generated_musicxml_recursively_finds_musicxml(tmp_path: Path):
    nested = tmp_path / "book" / "movement"
    nested.mkdir(parents=True)
    expected = nested / "score.musicxml"
    expected.write_text("<score-partwise />")

    assert find_generated_musicxml(tmp_path) == expected


def test_find_generated_musicxml_prefers_musicxml_then_xml_then_mxl(tmp_path: Path):
    mxl = tmp_path / "score.mxl"
    xml = tmp_path / "score.xml"
    musicxml = tmp_path / "score.musicxml"
    mxl.write_text("mxl")
    xml.write_text("xml")
    musicxml.write_text("musicxml")

    assert find_generated_musicxml(tmp_path) == musicxml

    musicxml.unlink()

    assert find_generated_musicxml(tmp_path) == xml

    xml.unlink()

    assert find_generated_musicxml(tmp_path) == mxl


def test_run_audiveris_returns_result_when_runner_generates_musicxml(tmp_path: Path):
    input_path = tmp_path / "score.png"
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    settings = OMRSettings(audiveris_cmd="audiveris-cli", timeout_seconds=7)

    def fake_runner(command: list[str], **kwargs):
        (output_dir / "score.musicxml").write_text("<score-partwise />")
        assert command == build_audiveris_command(input_path, output_dir, settings)
        assert kwargs == {
            "timeout": 7,
            "capture_output": True,
            "text": True,
            "check": False,
        }
        return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

    result = run_audiveris(input_path, output_dir, settings, runner=fake_runner)

    assert result == AudiverisResult(output_dir / "score.musicxml", "ok", "")


def test_run_audiveris_raises_configuration_error_for_missing_binary(tmp_path: Path):
    def fake_runner(*_args, **_kwargs):
        raise FileNotFoundError

    with pytest.raises(OMRConfigurationError, match="当前环境未配置 Audiveris"):
        run_audiveris(tmp_path / "score.png", tmp_path / "out", OMRSettings(), runner=fake_runner)


def test_run_audiveris_raises_timeout_error(tmp_path: Path):
    def fake_runner(command: list[str], **_kwargs):
        raise subprocess.TimeoutExpired(command, timeout=1)

    with pytest.raises(OMRTimeoutError, match="OMR 识别超时"):
        run_audiveris(tmp_path / "score.png", tmp_path / "out", OMRSettings(), runner=fake_runner)


def test_run_audiveris_raises_engine_error_for_non_zero_returncode(tmp_path: Path):
    def fake_runner(command: list[str], **_kwargs):
        return subprocess.CompletedProcess(command, 1, stdout="fallback", stderr="cannot read score")

    with pytest.raises(OMREngineError, match="Audiveris 识别失败: cannot read score"):
        run_audiveris(tmp_path / "score.png", tmp_path / "out", OMRSettings(), runner=fake_runner)


def test_run_audiveris_raises_engine_error_when_musicxml_is_missing(tmp_path: Path):
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    def fake_runner(command: list[str], **_kwargs):
        return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

    with pytest.raises(OMREngineError, match="Audiveris 未生成 MusicXML"):
        run_audiveris(tmp_path / "score.png", output_dir, OMRSettings(), runner=fake_runner)
