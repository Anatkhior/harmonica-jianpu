from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

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
