from app.models import HarmonicaPosition, JianpuEvent, MelodyEvent


def test_melody_event_keeps_pitch_and_duration():
    event = MelodyEvent(
        measure=1,
        beat=1.0,
        duration_quarter=1.0,
        midi_pitch=60,
        source_name="C4",
        is_rest=False,
    )

    assert event.midi_pitch == 60
    assert event.duration_quarter == 1.0


def test_jianpu_event_can_include_harmonica_position():
    position = HarmonicaPosition(hole=1, breath="blow", slide=False, label="1吹")
    event = JianpuEvent(
        measure=1,
        beat=1.0,
        duration_quarter=1.0,
        symbol="1",
        octave=0,
        harmonica=position,
    )

    assert event.symbol == "1"
    assert event.harmonica.label == "1吹"
