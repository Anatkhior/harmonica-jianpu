import { useState } from "react";

import { convertScore } from "./api";
import { ConversionResult } from "./components/ConversionResult";
import { ErrorNotice } from "./components/ErrorNotice";
import { FileUploader } from "./components/FileUploader";
import { ScorePreview } from "./components/ScorePreview";
import type { ConversionResponse } from "./types";

export default function App() {
  const [fileText, setFileText] = useState("");
  const [fileName, setFileName] = useState("");
  const [previewMessage, setPreviewMessage] = useState("");
  const [result, setResult] = useState<ConversionResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleFileSelected(file: File) {
    setLoading(true);
    setError("");
    setResult(null);
    setFileName(file.name);
    setPreviewMessage("");

    try {
      if (file.name.toLowerCase().endsWith(".mxl")) {
        setFileText("");
        setPreviewMessage("MXL 文件可以转换，但当前版本暂不支持前端原谱预览。");
      } else {
        setFileText(await file.text());
      }
      setResult(await convertScore(file));
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "转换失败");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="workspace">
        <header className="topbar">
          <div>
            <h1>Harmonica Jianpu</h1>
            <p>单旋律五线谱转 12 孔 C 调半音阶口琴简谱</p>
          </div>
          <FileUploader disabled={loading} onFileSelected={handleFileSelected} />
        </header>

        <ErrorNotice message={error} />

        <div className="split-view">
          <section className="pane" aria-label="原谱预览">
            <div className="pane-heading">
              <h2>原谱</h2>
              {fileName ? <span>{fileName}</span> : null}
            </div>
            <ScorePreview message={previewMessage} musicXml={fileText} />
          </section>
          <section className="pane" aria-label="转换结果">
            <div className="pane-heading">
              <h2>简谱与口琴提示</h2>
              {result ? <span>{result.events.length} 个音符/休止符</span> : null}
            </div>
            {loading ? <p className="muted">转换中...</p> : <ConversionResult result={result} />}
          </section>
        </div>
      </section>
    </main>
  );
}
