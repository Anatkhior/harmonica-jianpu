from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.omr.errors import OMRConfigurationError
from app.omr.service import OMRTranscriptionResult
from app.omr.validation import OMR_SUFFIXES

FIXTURES = Path(__file__).parent / "fixtures"


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_convert_musicxml_endpoint():
    client = TestClient(app)
    path = FIXTURES / "c_major_scale.musicxml"

    with path.open("rb") as file:
        response = client.post(
            "/api/convert",
            files={"file": ("c_major_scale.musicxml", file, "application/xml")},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["sourceType"] == "musicxml"
    assert "omr" not in body
    assert body["warnings"] == []
    assert [event["symbol"] for event in body["events"][:4]] == ["1", "2", "3", "4"]
    assert body["events"][0]["durationQuarter"] == 1.0
    assert body["events"][0]["isRest"] is False
    assert body["events"][0]["harmonica"]["label"] == "1吹"


def test_rejects_unsupported_file_type():
    client = TestClient(app)

    response = client.post(
        "/api/convert",
        files={"file": ("melody.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported file type"


def test_convert_pdf_uses_omr_then_existing_conversion(monkeypatch):
    client = TestClient(app)
    calls = []

    def fake_transcribe_score_to_musicxml(input_path, suffix, output_dir, settings):
        calls.append(
            {
                "input_path": input_path,
                "input_exists": input_path.exists(),
                "suffix": suffix,
                "output_dir": output_dir,
                "settings": settings,
            }
        )
        return OMRTranscriptionResult(
            musicxml_path=FIXTURES / "c_major_scale.musicxml",
            engine="audiveris",
            message="OMR 识别完成，请人工核对结果。",
        )

    monkeypatch.setattr(
        "app.api.routes.transcribe_score_to_musicxml",
        fake_transcribe_score_to_musicxml,
    )

    response = client.post(
        "/api/convert",
        files={"file": ("melody.pdf", b"%PDF fake", "application/pdf")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["sourceType"] == "omr"
    assert body["omr"] == {
        "engine": "audiveris",
        "generatedMusicXml": True,
        "message": "OMR 识别完成，请人工核对结果。",
    }
    assert [event["symbol"] for event in body["events"][:4]] == ["1", "2", "3", "4"]
    assert len(calls) == 1
    assert calls[0]["suffix"] == ".pdf"
    assert calls[0]["input_exists"] is True


def test_convert_pdf_reports_omr_configuration_error(monkeypatch):
    client = TestClient(app)
    message = "当前环境未配置 Audiveris，请安装后设置 AUDIVERIS_CMD。"

    def fake_transcribe_score_to_musicxml(input_path, suffix, output_dir, settings):
        raise OMRConfigurationError(message)

    monkeypatch.setattr(
        "app.api.routes.transcribe_score_to_musicxml",
        fake_transcribe_score_to_musicxml,
    )

    response = client.post(
        "/api/convert",
        files={"file": ("melody.jpg", b"fake image", "image/jpeg")},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == message


def test_supported_suffixes_include_omr_suffixes():
    from app.api.routes import SUPPORTED_SUFFIXES

    assert OMR_SUFFIXES <= SUPPORTED_SUFFIXES
