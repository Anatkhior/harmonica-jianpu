import pytest

from app.conversion.harmonica import map_midi_to_harmonica


def test_maps_basic_low_octave_positions():
    assert map_midi_to_harmonica(60).label == "1吹"
    assert map_midi_to_harmonica(61).label == "1吹按键"
    assert map_midi_to_harmonica(62).label == "1吸"
    assert map_midi_to_harmonica(63).label == "1吸按键"
    assert map_midi_to_harmonica(65).label == "2吸"
    assert map_midi_to_harmonica(66).label == "2吸按键"


def test_maps_hole_12_top_note():
    assert map_midi_to_harmonica(95).label == "12吸"
    assert map_midi_to_harmonica(96).label == "12吹"
    assert map_midi_to_harmonica(97).label == "12吹按键"


def test_rejects_out_of_range_pitch():
    with pytest.raises(ValueError, match="outside 12-hole C chromatic harmonica range"):
        map_midi_to_harmonica(59)
