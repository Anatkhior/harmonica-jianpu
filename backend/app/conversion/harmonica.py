from app.models import HarmonicaPosition

BREATH_LABEL = {
    "blow": "吹",
    "draw": "吸",
}

KEY_OUT_LAYOUT = [
    (1, 60, "blow"),
    (1, 62, "draw"),
    (2, 64, "blow"),
    (2, 65, "draw"),
    (3, 67, "blow"),
    (3, 69, "draw"),
    (4, 72, "blow"),
    (4, 71, "draw"),
    (5, 72, "blow"),
    (5, 74, "draw"),
    (6, 76, "blow"),
    (6, 77, "draw"),
    (7, 79, "blow"),
    (7, 81, "draw"),
    (8, 84, "blow"),
    (8, 83, "draw"),
    (9, 84, "blow"),
    (9, 86, "draw"),
    (10, 88, "blow"),
    (10, 89, "draw"),
    (11, 91, "blow"),
    (11, 93, "draw"),
    (12, 96, "blow"),
    (12, 95, "draw"),
]


def _build_solo_tuning_map() -> dict[int, HarmonicaPosition]:
    mapping: dict[int, HarmonicaPosition] = {}

    for hole, midi_pitch, breath in KEY_OUT_LAYOUT:
        mapping.setdefault(
            midi_pitch,
            HarmonicaPosition(
                hole=hole,
                breath=breath,
                slide=False,
                label=f"{hole}{BREATH_LABEL[breath]}",
            ),
        )

    for hole, midi_pitch, breath in KEY_OUT_LAYOUT:
        slide_pitch = midi_pitch + 1
        mapping.setdefault(
            slide_pitch,
            HarmonicaPosition(
                hole=hole,
                breath=breath,
                slide=True,
                label=f"{hole}{BREATH_LABEL[breath]}按键",
            ),
        )

    return mapping


HARMONICA_MAP = _build_solo_tuning_map()


def map_midi_to_harmonica(midi_pitch: int) -> HarmonicaPosition:
    try:
        return HARMONICA_MAP[midi_pitch]
    except KeyError as exc:
        raise ValueError("pitch outside 12-hole C chromatic harmonica range") from exc
