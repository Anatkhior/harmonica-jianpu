import { render, screen } from "@testing-library/react";
import { afterEach, expect, test, vi } from "vitest";

import { ConversionResult } from "./ConversionResult";

afterEach(() => {
  vi.restoreAllMocks();
});

test("renders duplicate warning text without duplicate key warnings", () => {
  const consoleError = vi.spyOn(console, "error").mockImplementation(() => undefined);

  render(<ConversionResult result={{ events: [], warnings: ["同一个提示", "同一个提示"] }} />);

  expect(consoleError).not.toHaveBeenCalled();
});

test("renders OMR review notice from conversion metadata", () => {
  render(
    <ConversionResult
      result={{
        events: [],
        warnings: [],
        sourceType: "omr",
        omr: {
          engine: "audiveris",
          generatedMusicXml: true,
          message: "OMR 识别完成，请人工核对结果。",
        },
      }}
    />,
  );

  expect(screen.getByText("OMR 识别完成，请人工核对结果。")).toBeTruthy();
});
