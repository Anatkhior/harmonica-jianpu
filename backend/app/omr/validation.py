from pathlib import Path

from pypdf import PdfReader

from app.omr.config import OMRSettings
from app.omr.errors import OMRValidationError


OMR_SUFFIXES = {".pdf", ".jpg", ".jpeg", ".png"}


def validate_omr_upload(path: Path, suffix: str, settings: OMRSettings) -> None:
    normalized_suffix = suffix.lower()
    if normalized_suffix not in OMR_SUFFIXES:
        raise OMRValidationError("不支持的 OMR 文件类型，请上传 PDF、JPG、JPEG 或 PNG。")

    max_bytes = settings.max_file_mb * 1024 * 1024
    if path.stat().st_size > max_bytes:
        raise OMRValidationError(f"文件大小超过限制，请上传不超过 {settings.max_file_mb} MB 的文件。")

    if normalized_suffix == ".pdf":
        page_count = count_pdf_pages(path)
        if page_count > settings.max_pdf_pages:
            raise OMRValidationError(f"PDF 页数超过限制，请上传不超过 {settings.max_pdf_pages} 页的文件。")


def count_pdf_pages(path: Path) -> int:
    try:
        reader = PdfReader(path)
        return len(reader.pages)
    except Exception as exc:
        raise OMRValidationError("无法读取 PDF 页数，请确认文件是有效 PDF。") from exc
