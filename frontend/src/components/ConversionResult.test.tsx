import { render } from "@testing-library/react";
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
