import { render, screen } from "@testing-library/react";
import { expect, test, vi } from "vitest";

import { FileUploader } from "./FileUploader";

test("exposes upload as a keyboard-accessible button", () => {
  render(<FileUploader disabled={false} onFileSelected={vi.fn()} />);

  expect(screen.getByRole("button", { name: "上传乐谱" })).toBeTruthy();
});
