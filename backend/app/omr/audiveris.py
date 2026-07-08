from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Callable

from app.omr.config import OMRSettings
from app.omr.errors import OMRConfigurationError, OMREngineError, OMRTimeoutError


CompletedRunner = Callable[..., subprocess.CompletedProcess[str]]

MUSICXML_SUFFIX_PRIORITY = {
    ".musicxml": 0,
    ".xml": 1,
    ".mxl": 2,
}


@dataclass(frozen=True)
class AudiverisResult:
    musicxml_path: Path
    stdout: str
    stderr: str


def build_audiveris_command(input_path: Path, output_dir: Path, settings: OMRSettings) -> list[str]:
    return [
        settings.audiveris_cmd,
        "-batch",
        "-transcribe",
        "-export",
        "-output",
        str(output_dir),
        str(input_path),
    ]


def format_engine_detail(stdout: str, stderr: str, max_length: int = 500) -> str:
    for detail in (stderr, stdout, "unknown error"):
        detail = detail.strip()
        if detail:
            break

    if len(detail) > max_length:
        return f"{detail[:max_length]}..."
    return detail


def run_audiveris(
    input_path: Path,
    output_dir: Path,
    settings: OMRSettings,
    runner: CompletedRunner = subprocess.run,
) -> AudiverisResult:
    command = build_audiveris_command(input_path, output_dir, settings)

    try:
        completed = runner(
            command,
            timeout=settings.timeout_seconds,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise OMRConfigurationError(
            "当前环境未配置 Audiveris，请安装后设置 AUDIVERIS_CMD，或上传 MusicXML/MXL。"
        ) from exc
    except OSError as exc:
        raise OMRConfigurationError(
            "当前环境无法启动 Audiveris，请检查 AUDIVERIS_CMD 是否可执行，或上传 MusicXML/MXL。"
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise OMRTimeoutError("OMR 识别超时，请尝试更清晰或页数更少的谱面。") from exc

    stdout = completed.stdout or ""
    stderr = completed.stderr or ""

    if completed.returncode != 0:
        detail = format_engine_detail(stdout, stderr)
        raise OMREngineError(f"Audiveris 识别失败: {detail}")

    musicxml_path = find_generated_musicxml(output_dir)
    if musicxml_path is None:
        raise OMREngineError("Audiveris 未生成 MusicXML，请尝试先用 Audiveris GUI 校对并导出。")

    return AudiverisResult(musicxml_path=musicxml_path, stdout=stdout, stderr=stderr)


def find_generated_musicxml(output_dir: Path) -> Path | None:
    candidates = [
        path
        for path in output_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in MUSICXML_SUFFIX_PRIORITY
    ]
    if not candidates:
        return None

    return sorted(candidates, key=lambda path: (suffix_priority(path.suffix), str(path)))[0]


def suffix_priority(suffix: str) -> int:
    return MUSICXML_SUFFIX_PRIORITY.get(suffix.lower(), len(MUSICXML_SUFFIX_PRIORITY))
