from pathlib import Path

import pytest

from app.omr.config import OMRSettings
from app.omr.errors import OMRValidationError
from app.omr.validation import OMR_SUFFIXES, validate_omr_upload


def test_omr_suffixes_include_pdf_and_images():
    assert OMR_SUFFIXES == {".pdf", ".jpg", ".jpeg", ".png"}


def test_rejects_unsupported_omr_suffix(tmp_path: Path):
    path = tmp_path / "score.gif"
    path.write_bytes(b"fake")

    with pytest.raises(OMRValidationError, match="不支持的 OMR 文件类型"):
        validate_omr_upload(path, ".gif", OMRSettings())


def test_rejects_files_larger_than_limit(tmp_path: Path):
    path = tmp_path / "large.jpg"
    path.write_bytes(b"x" * 11)
    settings = OMRSettings(max_file_mb=0.000001)

    with pytest.raises(OMRValidationError, match="文件大小超过限制"):
        validate_omr_upload(path, ".jpg", settings)


def test_accepts_image_under_limit(tmp_path: Path):
    path = tmp_path / "score.jpg"
    path.write_bytes(b"fake image")

    validate_omr_upload(path, ".jpg", OMRSettings(max_file_mb=1))


def test_rejects_pdf_with_too_many_pages(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    path = tmp_path / "score.pdf"
    path.write_bytes(b"%PDF fake")

    monkeypatch.setattr("app.omr.validation.count_pdf_pages", lambda _: 4)

    with pytest.raises(OMRValidationError, match="PDF 页数超过限制"):
        validate_omr_upload(path, ".pdf", OMRSettings(max_pdf_pages=3))


def test_accepts_pdf_within_page_limit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    path = tmp_path / "score.pdf"
    path.write_bytes(b"%PDF fake")

    monkeypatch.setattr("app.omr.validation.count_pdf_pages", lambda _: 3)

    validate_omr_upload(path, ".pdf", OMRSettings(max_pdf_pages=3))


def test_rejects_unreadable_pdf(tmp_path: Path):
    path = tmp_path / "broken.pdf"
    path.write_bytes(b"not a real pdf")

    with pytest.raises(OMRValidationError, match="无法读取 PDF 页数"):
        validate_omr_upload(path, ".pdf", OMRSettings(max_pdf_pages=3))
