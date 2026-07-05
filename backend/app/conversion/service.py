from dataclasses import dataclass

from app.conversion.harmonica import map_midi_to_harmonica
from app.conversion.jianpu import midi_to_jianpu
from app.models import HarmonicaPosition, JianpuEvent, MelodyEvent


@dataclass(frozen=True)
class ConversionResult:
    events: list[JianpuEvent]
    warnings: list[str]


def convert_melody_events(events: list[MelodyEvent]) -> ConversionResult:
    converted: list[JianpuEvent] = []
    warnings: list[str] = []

    for event in events:
        if event.is_rest:
            converted.append(
                JianpuEvent(
                    measure=event.measure,
                    beat=event.beat,
                    duration_quarter=event.duration_quarter,
                    symbol="0",
                    octave=0,
                    harmonica=None,
                    is_rest=True,
                )
            )
            continue

        if event.midi_pitch is None:
            warnings.append(f"第 {event.measure} 小节第 {event.beat} 拍缺少音高信息")
            continue

        jianpu = midi_to_jianpu(event.midi_pitch)
        harmonica = _map_harmonica_or_warn(event, warnings)

        converted.append(
            JianpuEvent(
                measure=event.measure,
                beat=event.beat,
                duration_quarter=event.duration_quarter,
                symbol=jianpu.symbol,
                octave=jianpu.octave,
                harmonica=harmonica,
                is_rest=False,
            )
        )

    return ConversionResult(events=converted, warnings=warnings)


def _map_harmonica_or_warn(
    event: MelodyEvent, warnings: list[str]
) -> HarmonicaPosition | None:
    try:
        return map_midi_to_harmonica(event.midi_pitch)
    except ValueError:
        warnings.append(
            f"第 {event.measure} 小节第 {event.beat} 拍的音 "
            f"{event.source_name or event.midi_pitch} 超出 12 孔 C 调半音阶口琴范围"
        )
        return None
