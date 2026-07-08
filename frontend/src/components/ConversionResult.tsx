import type { ConversionResponse, JianpuEvent } from "../types";

type ConversionResultProps = {
  result: ConversionResponse | null;
};

function octaveMarks(octave: number) {
  if (octave === 0) {
    return "";
  }

  const mark = octave > 0 ? "·" : ".";
  return mark.repeat(Math.abs(octave));
}

function groupByMeasure(events: JianpuEvent[]) {
  return events.reduce<Record<number, JianpuEvent[]>>((groups, event) => {
    groups[event.measure] = groups[event.measure] ?? [];
    groups[event.measure].push(event);
    return groups;
  }, {});
}

export function ConversionResult({ result }: ConversionResultProps) {
  if (!result) {
    return <div className="empty-state">上传 MusicXML 后显示转换结果</div>;
  }

  const grouped = groupByMeasure(result.events);

  return (
    <>
      {result.omr ? <p className="omr-notice">{result.omr.message}</p> : null}

      {result.warnings.length > 0 ? (
        <ul className="warnings">
          {result.warnings.map((warning, index) => (
            <li key={`${warning}-${index}`}>{warning}</li>
          ))}
        </ul>
      ) : null}

      <div className="measure-list">
        {Object.entries(grouped).map(([measure, events]) => (
          <div className="measure" key={measure}>
            <span className="measure-number">第 {measure} 小节</span>
            {events.map((event, index) => (
              <span className="note-cell" key={`${measure}-${event.beat}-${index}`}>
                <span className="jianpu-symbol">
                  {event.symbol}
                  {octaveMarks(event.octave)}
                </span>
                <span className="harmonica-label">{event.harmonica?.label ?? "-"}</span>
              </span>
            ))}
          </div>
        ))}
      </div>
    </>
  );
}
