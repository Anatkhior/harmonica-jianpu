from app.conversion.jianpu import midi_to_jianpu


def test_c_major_scale_maps_to_numbers():
    result = [midi_to_jianpu(pitch).symbol for pitch in [60, 62, 64, 65, 67, 69, 71]]

    assert result == ["1", "2", "3", "4", "5", "6", "7"]


def test_accidentals_use_sharp_only():
    result = [midi_to_jianpu(pitch).symbol for pitch in [61, 63, 66, 68, 70]]

    assert result == ["#1", "#2", "#4", "#5", "#6"]


def test_octave_relative_to_middle_c():
    assert midi_to_jianpu(48).octave == -1
    assert midi_to_jianpu(60).octave == 0
    assert midi_to_jianpu(72).octave == 1
