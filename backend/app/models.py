from dataclasses import dataclass


@dataclass(frozen=True)
class MelodyEvent:
    measure: int
    beat: float
    duration_quarter: float
    midi_pitch: int | None
    source_name: str | None
    is_rest: bool
    tie_type: str | None = None
    voice: str | None = None


@dataclass(frozen=True)
class HarmonicaPosition:
    hole: int
    breath: str
    slide: bool
    label: str


@dataclass(frozen=True)
class JianpuEvent:
    measure: int
    beat: float
    duration_quarter: float
    symbol: str
    octave: int
    harmonica: HarmonicaPosition | None = None
    is_rest: bool = False
