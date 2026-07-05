import type { ConversionResponse } from "./types";

export async function convertScore(file: File): Promise<ConversionResponse> {
  const body = new FormData();
  body.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/api/convert", {
    method: "POST",
    body,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "转换失败" }));
    throw new Error(error.detail ?? "转换失败");
  }

  return response.json();
}
