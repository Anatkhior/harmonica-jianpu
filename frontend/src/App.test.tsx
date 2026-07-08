import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, expect, test, vi } from "vitest";

import App from "./App";
import { convertScore } from "./api";

vi.mock("./api", () => ({
  convertScore: vi.fn(),
}));

vi.mock("./components/ScorePreview", () => ({
  ScorePreview: ({ message, musicXml }: { message?: string; musicXml: string }) => (
    <div data-musicxml={musicXml} data-testid="score-preview">
      {message}
    </div>
  ),
}));

beforeEach(() => {
  vi.mocked(convertScore).mockReset();
});

function deferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason?: unknown) => void;
  const promise = new Promise<T>((promiseResolve, promiseReject) => {
    resolve = promiseResolve;
    reject = promiseReject;
  });
  return { promise, reject, resolve };
}

test("allows mxl conversion while showing preview unsupported notice", async () => {
  vi.mocked(convertScore).mockResolvedValue({ events: [], warnings: [] });
  const { container } = render(<App />);
  const input = container.querySelector('input[type="file"]') as HTMLInputElement;
  const file = new File(["PK compressed score"], "song.mxl", {
    type: "application/vnd.recordare.musicxml",
  });

  fireEvent.change(input, { target: { files: [file] } });

  await waitFor(() => expect(convertScore).toHaveBeenCalledWith(file));
  expect(screen.getByText(/MXL 文件可以转换/)).toBeTruthy();
  expect(screen.getByTestId("score-preview").dataset.musicxml).toBe("");
});

test("shows OMR recognition preview while converting a PDF score", async () => {
  const conversion = deferred<Awaited<ReturnType<typeof convertScore>>>();
  vi.mocked(convertScore).mockReturnValue(conversion.promise);
  const response = {
    events: [],
    warnings: [],
    sourceType: "omr",
    omr: {
      engine: "audiveris",
      generatedMusicXml: true,
      message: "OMR 识别完成，请人工核对结果。",
    },
  } satisfies Awaited<ReturnType<typeof convertScore>>;
  const { container } = render(<App />);
  const input = container.querySelector('input[type="file"]') as HTMLInputElement;
  const file = new File(["%PDF-1.7"], "song.pdf", { type: "application/pdf" });

  fireEvent.change(input, { target: { files: [file] } });

  expect(screen.getByText("正在进行 OMR 识别，可能需要几十秒。")).toBeTruthy();
  expect(screen.getByText("正在识别...")).toBeTruthy();
  expect(screen.getByTestId("score-preview").dataset.musicxml).toBe("");
  conversion.resolve(response);
  await waitFor(() => expect(convertScore).toHaveBeenCalledWith(file));
  expect(await screen.findByText("0 个音符/休止符")).toBeTruthy();
  expect(screen.queryByText("正在进行 OMR 识别，可能需要几十秒。")).toBeNull();
  expect(screen.getByText("OMR 识别完成，请在右侧核对转换结果。")).toBeTruthy();
});

test("replaces OMR recognition preview when PDF conversion fails", async () => {
  vi.mocked(convertScore).mockRejectedValue(new Error("OMR engine failed"));
  const { container } = render(<App />);
  const input = container.querySelector('input[type="file"]') as HTMLInputElement;
  const file = new File(["%PDF-1.7"], "song.pdf", { type: "application/pdf" });

  fireEvent.change(input, { target: { files: [file] } });

  expect(await screen.findByText("OMR engine failed")).toBeTruthy();
  expect(screen.queryByText("正在进行 OMR 识别，可能需要几十秒。")).toBeNull();
  expect(screen.getByText("OMR 识别失败，请检查错误信息后重试。")).toBeTruthy();
});
