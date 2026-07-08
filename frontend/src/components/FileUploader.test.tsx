import { render, screen } from "@testing-library/react";
import { expect, test, vi } from "vitest";

import { FileUploader } from "./FileUploader";

test("exposes upload as a keyboard-accessible button", () => {
  render(<FileUploader disabled={false} onFileSelected={vi.fn()} />);

  expect(screen.getByRole("button", { name: "上传乐谱" })).toBeTruthy();
});

test("accepts MusicXML, MXL, PDF, and image score files", () => {
  const { container } = render(<FileUploader disabled={false} onFileSelected={vi.fn()} />);

  const input = container.querySelector('input[type="file"]') as HTMLInputElement;

  expect(input.accept).toBe(".musicxml,.xml,.mxl,.pdf,.jpg,.jpeg,.png");
});
