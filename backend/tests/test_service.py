from app.conversion.service import convert_melody_events
from app.models import MelodyEvent


def test_converts_events_to_jianpu_and_harmonica():
    events = [
        MelodyEvent(1, 1.0, 1.0, 60, "C4", False),
        MelodyEvent(1, 2.0, 1.0, 61, "Db4", False),
        MelodyEvent(1, 3.0, 1.0, None, None, True),
    ]

    result = convert_melody_events(events)

    assert result.warnings == []
    assert [event.symbol for event in result.events] == ["1", "#1", "0"]
    assert [event.measure for event in result.events] == [1, 1, 1]
    assert [event.beat for event in result.events] == [1.0, 2.0, 3.0]
    assert [event.duration_quarter for event in result.events] == [1.0, 1.0, 1.0]
    assert result.events[0].harmonica.label == "1吹"
    assert result.events[1].harmonica.label == "1吹按键"
    assert result.events[2].octave == 0
    assert result.events[2].harmonica is None
    assert result.events[2].is_rest is True


def test_reports_out_of_range_notes():
    events = [MelodyEvent(1, 1.0, 1.0, 59, "B3", False)]

    result = convert_melody_events(events)

    assert result.events[0].harmonica is None
    assert result.warnings == ["第 1 小节第 1.0 拍的音 B3 超出 12 孔 C 调半音阶口琴范围"]


def test_reports_missing_pitch_information():
    events = [MelodyEvent(1, 2.0, 1.0, None, None, False)]

    result = convert_melody_events(events)

    assert result.events == []
    assert result.warnings == ["第 1 小节第 2.0 拍缺少音高信息"]
