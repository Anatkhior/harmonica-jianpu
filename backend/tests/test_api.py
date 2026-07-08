from pathlib import Path
from shutil import copyfile

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


def test_convert_cleans_upload_temp_file_when_write_fails(monkeypatch, tmp_path):
    client = TestClient(app, raise_server_exceptions=False)
    leaked_path = tmp_path / "upload.musicxml"

    class FailingTempFile:
        name = str(leaked_path)

        def __enter__(self):
            leaked_path.touch()
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def write(self, content):
            raise OSError("disk full")

    def fake_named_temporary_file(delete, suffix):
        assert delete is False
        assert suffix == ".musicxml"
        return FailingTempFile()

    monkeypatch.setattr("app.api.routes.NamedTemporaryFile", fake_named_temporary_file)

    response = client.post(
        "/api/convert",
        files={"file": ("melody.musicxml", b"<score-partwise />", "application/xml")},
    )

    assert response.status_code == 500
    assert leaked_path.exists() is False


def test_convert_pdf_uses_omr_then_existing_conversion(monkeypatch):
    client = TestClient(app)
    calls = []
    output_dirs = []

    def fake_transcribe_score_to_musicxml(input_path, suffix, output_dir, settings):
        musicxml_path = output_dir / "c_major_scale.musicxml"
        copyfile(FIXTURES / "c_major_scale.musicxml", musicxml_path)
        calls.append(
            {
                "input_path": input_path,
                "input_exists": input_path.exists(),
                "suffix": suffix,
                "output_dir": output_dir,
                "settings": settings,
            }
        )
        output_dirs.append(output_dir)
        return OMRTranscriptionResult(
            musicxml_path=musicxml_path,
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
    assert output_dirs
    assert output_dirs[0].exists() is False


def test_convert_pdf_reports_omr_transcription_configuration_error(monkeypatch):
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


def test_convert_image_reports_invalid_omr_settings(monkeypatch):
    client = TestClient(app)
    monkeypatch.setenv("OMR_TIMEOUT_SECONDS", "abc")

    response = client.post(
        "/api/convert",
        files={"file": ("melody.jpg", b"fake image", "image/jpeg")},
    )

    assert response.status_code == 503
    assert "OMR 配置无效" in response.json()["detail"]


def test_convert_omr_generated_chord_musicxml_reports_unprocessable(monkeypatch):
    client = TestClient(app)

    def fake_transcribe_score_to_musicxml(input_path, suffix, output_dir, settings):
        musicxml_path = output_dir / "chord_input.musicxml"
        copyfile(FIXTURES / "chord_input.musicxml", musicxml_path)
        return OMRTranscriptionResult(
            musicxml_path=musicxml_path,
            engine="audiveris",
            message="OMR 识别完成，请人工核对结果。",
        )

    monkeypatch.setattr(
        "app.api.routes.transcribe_score_to_musicxml",
        fake_transcribe_score_to_musicxml,
    )

    response = client.post(
        "/api/convert",
        files={"file": ("melody.jpg", b"fake image", "image/jpeg")},
    )

    assert response.status_code == 422
    assert "Only single-line melody MusicXML is supported" in response.json()["detail"]


def test_supported_suffixes_include_omr_suffixes():
    from app.api.routes import SUPPORTED_SUFFIXES

    assert OMR_SUFFIXES <= SUPPORTED_SUFFIXES
