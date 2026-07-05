from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, HTTPException, UploadFile

from app.conversion.service import convert_melody_events
from app.parsing.musicxml_parser import parse_musicxml

router = APIRouter()

SUPPORTED_SUFFIXES = {".musicxml", ".xml", ".mxl"}


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/convert")
async def convert(file: UploadFile) -> dict[str, object]:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    content = await file.read()
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        melody = parse_musicxml(tmp_path)
        result = convert_melody_events(melody)
    finally:
        tmp_path.unlink(missing_ok=True)

    return {
        "events": [
            {
                "measure": event.measure,
                "beat": event.beat,
                "durationQuarter": event.duration_quarter,
                "symbol": event.symbol,
                "octave": event.octave,
                "isRest": event.is_rest,
                "harmonica": None
                if event.harmonica is None
                else {
                    "hole": event.harmonica.hole,
                    "breath": event.harmonica.breath,
                    "slide": event.harmonica.slide,
                    "label": event.harmonica.label,
                },
            }
            for event in result.events
        ],
        "warnings": result.warnings,
    }
