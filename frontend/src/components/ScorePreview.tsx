import { useEffect, useRef, useState } from "react";
import { OpenSheetMusicDisplay } from "opensheetmusicdisplay";

type ScorePreviewProps = {
  message?: string;
  musicXml: string;
};

export function ScorePreview({ message = "", musicXml }: ScorePreviewProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [previewError, setPreviewError] = useState("");

  useEffect(() => {
    const container = containerRef.current;
    let active = true;

    setPreviewError("");

    if (!container || !musicXml) {
      return;
    }

    const osmd = new OpenSheetMusicDisplay(container, {
      autoResize: true,
      drawTitle: false,
    });

    container.innerHTML = "";
    osmd
      .load(musicXml)
      .then(() => {
        if (active) {
          osmd.render();
        }
      })
      .catch(() => {
        if (active) {
          container.innerHTML = "";
          setPreviewError("原谱预览失败，请确认文件是有效的 MusicXML。");
        }
      });

    return () => {
      active = false;
      container.innerHTML = "";
    };
  }, [musicXml]);

  if (message) {
    return <div className="empty-state">{message}</div>;
  }

  if (previewError) {
    return <div className="empty-state">{previewError}</div>;
  }

  if (!musicXml) {
    return <div className="empty-state">上传 MusicXML 后显示原谱</div>;
  }

  return <div className="score-preview" ref={containerRef} />;
}
