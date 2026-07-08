from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

from fastapi import APIRouter, HTTPException, UploadFile

from app.conversion.service import ConversionResult, convert_melody_events
from app.omr.config import load_omr_settings
from app.omr.errors import OMRError
from app.omr.service import OMRTranscriptionResult, transcribe_score_to_musicxml
from app.omr.validation import OMR_SUFFIXES
from app.parsing.musicxml_parser import parse_musicxml

router = APIRouter()

MUSICXML_SUFFIXES = {".musicxml", ".xml", ".mxl"}
SUPPORTED_SUFFIXES = MUSICXML_SUFFIXES | OMR_SUFFIXES


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/convert")
async def convert(file: UploadFile) -> dict[str, object]:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    content = await file.read()
    tmp_path: Path | None = None
    try:
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = Path(tmp.name)
            tmp.write(content)

        if suffix in OMR_SUFFIXES:
            return _convert_omr_upload(tmp_path, suffix)
        return _convert_musicxml_path(tmp_path, source_type="musicxml", omr=None)
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)


def _convert_omr_upload(path: Path, suffix: str) -> dict[str, object]:
    try:
        settings = load_omr_settings()
        with TemporaryDirectory() as output_dir:
            omr_result = transcribe_score_to_musicxml(
                input_path=path,
                suffix=suffix,
                output_dir=Path(output_dir),
                settings=settings,
            )
            return _convert_musicxml_path(
                omr_result.musicxml_path,
                source_type="omr",
                omr=omr_result,
            )
    except OMRError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


def _convert_musicxml_path(
    path: Path,
    source_type: str,
    omr: OMRTranscriptionResult | None,
) -> dict[str, object]:
    try:
        melody = parse_musicxml(path)
        result = convert_melody_events(melody)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return _serialize_conversion_result(result, source_type, omr)


def _serialize_conversion_result(
    result: ConversionResult,
    source_type: str,
    omr: OMRTranscriptionResult | None,
) -> dict[str, object]:
    response: dict[str, object] = {
        "sourceType": source_type,
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

    if omr is not None:
        response["omr"] = {
            "engine": omr.engine,
            "generatedMusicXml": True,
            "message": omr.message,
        }

    return response
