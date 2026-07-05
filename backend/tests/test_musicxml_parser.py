from pathlib import Path

from app.parsing.musicxml_parser import parse_musicxml

FIXTURES = Path(__file__).parent / "fixtures"


def test_parses_single_line_musicxml():
    events = parse_musicxml(FIXTURES / "c_major_scale.musicxml")

    assert [event.midi_pitch for event in events] == [60, 62, 64, 65]
    assert [event.measure for event in events] == [1, 1, 1, 1]
    assert [event.beat for event in events] == [1.0, 2.0, 3.0, 4.0]
    assert [event.duration_quarter for event in events] == [1.0, 1.0, 1.0, 1.0]


def test_parses_flat_input_as_pitch_notation():
    events = parse_musicxml(FIXTURES / "accidental_flat_input.musicxml")

    assert events[0].midi_pitch == 61
    assert events[0].source_name == "D-4"
