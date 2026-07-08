from dataclasses import dataclass
import os

from app.omr.errors import OMRConfigurationError


@dataclass(frozen=True)
class OMRSettings:
    audiveris_cmd: str = "audiveris"
    max_file_mb: float = 15
    max_pdf_pages: int = 3
    timeout_seconds: int = 120


def load_omr_settings() -> OMRSettings:
    try:
        return OMRSettings(
            audiveris_cmd=os.getenv("AUDIVERIS_CMD", "audiveris"),
            max_file_mb=float(os.getenv("OMR_MAX_FILE_MB", "15")),
            max_pdf_pages=int(os.getenv("OMR_MAX_PDF_PAGES", "3")),
            timeout_seconds=int(os.getenv("OMR_TIMEOUT_SECONDS", "120")),
        )
    except ValueError as exc:
        raise OMRConfigurationError(
            "OMR 配置无效，请检查 OMR_MAX_FILE_MB、OMR_MAX_PDF_PAGES 和 OMR_TIMEOUT_SECONDS。"
        ) from exc
