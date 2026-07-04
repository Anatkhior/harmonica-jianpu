from app.models import JianpuEvent

PITCH_CLASS_TO_SYMBOL = {
    0: "1",
    1: "#1",
    2: "2",
    3: "#2",
    4: "3",
    5: "4",
    6: "#4",
    7: "5",
    8: "#5",
    9: "6",
    10: "#6",
    11: "7",
}


def midi_to_jianpu(midi_pitch: int) -> JianpuEvent:
    pitch_class = midi_pitch % 12
    octave = (midi_pitch - 60) // 12
    return JianpuEvent(
        measure=0,
        beat=0.0,
        duration_quarter=0.0,
        symbol=PITCH_CLASS_TO_SYMBOL[pitch_class],
        octave=octave,
    )
