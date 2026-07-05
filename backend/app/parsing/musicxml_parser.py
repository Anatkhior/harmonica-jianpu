from pathlib import Path

from music21 import converter, note

from app.models import MelodyEvent


def parse_musicxml(path: Path) -> list[MelodyEvent]:
    score = converter.parse(path)
    flat_notes = score.flatten().notesAndRests
    events: list[MelodyEvent] = []

    for item in flat_notes:
        measure_number = item.measureNumber or 0
        beat = float(getattr(item, "beat", 0.0) or 0.0)
        duration = float(item.duration.quarterLength)

        if isinstance(item, note.Rest):
            events.append(
                MelodyEvent(
                    measure=measure_number,
                    beat=beat,
                    duration_quarter=duration,
                    midi_pitch=None,
                    source_name=None,
                    is_rest=True,
                )
            )
            continue

        if isinstance(item, note.Note):
            events.append(
                MelodyEvent(
                    measure=measure_number,
                    beat=beat,
                    duration_quarter=duration,
                    midi_pitch=item.pitch.midi,
                    source_name=item.pitch.nameWithOctave,
                    is_rest=False,
                    tie_type=item.tie.type if item.tie else None,
                )
            )

    return events
