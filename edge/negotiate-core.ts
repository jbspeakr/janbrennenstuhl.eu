// Content negotiation rule shared by the edge script and its tests.
export function prefersMarkdown(accept: string | null): boolean {
  if (!accept) return false;
  const q = new Map<string, number>();
  for (const part of accept.split(",")) {
    const [media, ...params] = part.trim().split(";").map((s) => s.trim());
    const weight = params.find((p) => p.startsWith("q="));
    q.set(media.toLowerCase(), weight ? Number(weight.slice(2)) : 1);
  }
  const md = q.get("text/markdown") ?? 0;
  return md > 0 && md >= (q.get("text/html") ?? 0);
}

export function markdownPath(request: Request): string | null {
  if (request.method !== "GET" && request.method !== "HEAD") return null;
  const path = new URL(request.url).pathname;
  if (!path.endsWith("/") || !prefersMarkdown(request.headers.get("Accept"))) return null;
  return `${path}index.md`;
}
