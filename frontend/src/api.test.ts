import { afterEach, expect, test, vi } from "vitest";

import { convertScore } from "./api";

afterEach(() => {
  vi.restoreAllMocks();
});

test("falls back when api error detail is not a string", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ detail: [{ msg: "Invalid upload" }] }), {
        headers: { "Content-Type": "application/json" },
        status: 422,
      }),
    ),
  );

  await expect(convertScore(new File(["bad"], "bad.xml"))).rejects.toThrow("转换失败");
});
