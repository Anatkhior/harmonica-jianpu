import { useEffect, useRef } from "react";
import { OpenSheetMusicDisplay } from "opensheetmusicdisplay";

type ScorePreviewProps = {
  musicXml: string;
};

export function ScorePreview({ musicXml }: ScorePreviewProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!containerRef.current || !musicXml) {
      return;
    }

    const osmd = new OpenSheetMusicDisplay(containerRef.current, {
      autoResize: true,
      drawTitle: false,
    });

    containerRef.current.innerHTML = "";
    osmd.load(musicXml).then(() => osmd.render());

    return () => {
      if (containerRef.current) {
        containerRef.current.innerHTML = "";
      }
    };
  }, [musicXml]);

  if (!musicXml) {
    return <div className="empty-state">上传 MusicXML 后显示原谱</div>;
  }

  return <div className="score-preview" ref={containerRef} />;
}
