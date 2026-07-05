export type HarmonicaPosition = {
  hole: number;
  breath: "blow" | "draw";
  slide: boolean;
  label: string;
};

export type JianpuEvent = {
  measure: number;
  beat: number;
  durationQuarter: number;
  symbol: string;
  octave: number;
  isRest: boolean;
  harmonica: HarmonicaPosition | null;
};

export type ConversionResponse = {
  events: JianpuEvent[];
  warnings: string[];
};
