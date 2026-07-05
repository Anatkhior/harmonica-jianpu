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
