// Read-only MCP server for janbrennenstuhl.eu: search, read and cite the site's content.
// Dual-era: serves MCP 2026-07-28 statelessly (per-request _meta) and answers the legacy
// initialize handshake for 2025-03-26 to 2025-11-25 clients. It only ever fetches the site's
// own public JSON and Markdown files; arbitrary URLs are never fetched.

export const SITE = "https://www.janbrennenstuhl.eu";
export const MODERN = ["2026-07-28"];
export const LEGACY = ["2025-11-25", "2025-06-18", "2025-03-26"];
const SERVER_INFO = { name: "janbrennenstuhl.eu", version: "1.0.0" };
const INSTRUCTIONS =
  "Read-only access to Jan Brennenstuhl's essays and field guide on application security, identity and agent identity. " +
  "Use search_site to find entries, get_entry for the full Markdown, and get_findings for quotable claims with anchor URLs. " +
  "Cite canonical URLs. Content is CC BY 4.0 unless an entry says otherwise, AI training included; attribution is the condition. Reuse policy: https://www.janbrennenstuhl.eu/agents/";
const ALLOWED_ORIGINS = new Set([SITE]);

type Json = Record<string, unknown>;
type Loader = (path: string, kind: "json" | "text") => Promise<unknown>;

const TOOLS = [
  {
    name: "search_site",
    title: "Search the site",
    description: "Full-text search over essays, field-guide entries, talks and projects. Returns titles, canonical URLs and the best matching section.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Words to search for" },
        kind: { type: "string", enum: ["essay", "guide", "talk", "project"], description: "Optional content type" },
        topic: { type: "string", description: "Optional topic id, see list_topics" },
        limit: { type: "integer", minimum: 1, maximum: 20, description: "Maximum results, default 8" },
      },
      required: ["query"],
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: "get_entry",
    title: "Read an entry",
    description: "Returns the full Markdown of one entry, with front matter (dates, review status, license). Accepts a catalog id such as jb-jwks or a canonical URL.",
    inputSchema: { type: "object", properties: { id: { type: "string", description: "Catalog id or canonical URL" } }, required: ["id"] },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: "get_findings",
    title: "Get quotable findings",
    description: "Lists findings with their anchor URL, source and review status. Filter by entry id or by words in the finding.",
    inputSchema: {
      type: "object",
      properties: { article_id: { type: "string" }, query: { type: "string" }, limit: { type: "integer", minimum: 1, maximum: 50 } },
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: "list_topics",
    title: "List topics",
    description: "The site's six topics with descriptions, URLs and entry counts.",
    inputSchema: { type: "object", properties: {} },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
];

const norm = (s: unknown) => String(s ?? "").normalize("NFKC").toLocaleLowerCase("en");

export function defaultLoader(fetchImpl: typeof fetch = fetch, ttlMs = 300_000): Loader {
  const cache = new Map<string, { at: number; value: unknown }>();
  return async (path, kind) => {
    const hit = cache.get(path);
    if (hit && Date.now() - hit.at < ttlMs) return hit.value;
    const response = await fetchImpl(SITE + path, { headers: { Accept: kind === "json" ? "application/json" : "text/markdown" } });
    if (!response.ok) throw new Error(`Upstream ${response.status} for ${path}`);
    const value = kind === "json" ? await response.json() : await response.text();
    cache.set(path, { at: Date.now(), value });
    return value;
  };
}

async function callTool(name: string, args: Json, load: Loader): Promise<Json> {
  const text = (value: unknown) => ({ content: [{ type: "text", text: typeof value === "string" ? value : JSON.stringify(value, null, 2) }] });
  if (name === "search_site") {
    const query = String(args.query ?? "").trim();
    if (!query) return { ...text("query is required"), isError: true };
    const words = norm(query).split(/\s+/).filter(Boolean);
    const index = (await load("/search/index.json", "json")) as Json[];
    const limit = Math.min(20, Math.max(1, Number(args.limit) || 8));
    const hits = index
      .filter((e) => (!args.kind || e.kind === args.kind) && (!args.topic || (e.topics as string[]).includes(String(args.topic))))
      .map((e) => {
        const hay = norm(`${e.title} ${e.description} ${e.content}`);
        if (!words.every((w) => hay.includes(w))) return null;
        const score = words.reduce((n, w) => n + (norm(e.title).includes(w) ? 12 : 0) + (norm(e.description).includes(w) ? 4 : 0), 0);
        const section = (e.sections as Json[]).find((s) => words.some((w) => norm(`${s.title} ${s.text}`).includes(w)));
        return { score, e, section };
      })
      .filter((h): h is NonNullable<typeof h> => h !== null)
      .sort((a, b) => b.score - a.score || String(b.e.published).localeCompare(String(a.e.published)))
      .slice(0, limit)
      .map(({ e, section }) => ({
        id: e.id, title: e.title, kind: e.kind, topics: e.topics, published: e.published,
        url: SITE + e.url, markdown_url: `${SITE}${e.url}index.md`,
        section: section ? { title: section.title, url: `${SITE}${e.url}#${section.id}` } : null,
        summary: e.description,
      }));
    return { ...text(hits), structuredContent: { results: hits } };
  }
  if (name === "get_entry") {
    const wanted = String(args.id ?? "").trim();
    const catalog = (await load("/catalog.json", "json")) as { items: Json[] };
    const item = catalog.items.find((i) => i.id === wanted || i.canonical_url === wanted || i.canonical_url === `${SITE}${wanted.startsWith("/") ? wanted : `/${wanted}`}`);
    if (!item) return { ...text(`No entry with id or URL "${wanted}". Use search_site first.`), isError: true };
    const path = new URL(String(item.markdown_url)).pathname;
    return text(await load(path, "text"));
  }
  if (name === "get_findings") {
    const data = (await load("/findings.json", "json")) as { items: Json[] };
    const words = norm(args.query).split(/\s+/).filter(Boolean);
    const limit = Math.min(50, Math.max(1, Number(args.limit) || 20));
    const items = data.items
      .filter((f) => !args.article_id || f.article_id === args.article_id)
      .filter((f) => words.every((w) => norm(`${f.text} ${f.article}`).includes(w)))
      .slice(0, limit);
    return { ...text(items), structuredContent: { findings: items } };
  }
  if (name === "list_topics") {
    const catalog = (await load("/catalog.json", "json")) as { topics: Json[]; items: Json[] };
    const topics = catalog.topics.map((t) => ({ ...t, entries: catalog.items.filter((i) => (i.topics as string[]).includes(String(t.id))).length }));
    return { ...text(topics), structuredContent: { topics } };
  }
  return { ...text(`Unknown tool ${name}`), isError: true };
}

const json = (status: number, body: unknown, extra: Record<string, string> = {}) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store", ...extra } });
const rpcError = (id: unknown, code: number, message: string, data?: unknown) => ({ jsonrpc: "2.0", id: id ?? null, error: { code, message, ...(data ? { data } : {}) } });

function decodeHeader(value: string | null): string | null {
  if (value === null) return null;
  const m = /^=\?base64\?(.*)\?=$/.exec(value);
  return m ? new TextDecoder().decode(Uint8Array.from(atob(m[1]), (c) => c.charCodeAt(0))) : value;
}

export async function handle(request: Request, load: Loader): Promise<Response> {
  const origin = request.headers.get("Origin");
  if (origin && !ALLOWED_ORIGINS.has(origin)) return json(403, rpcError(null, -32600, "Origin not allowed"));
  if (request.method !== "POST") return new Response(null, { status: 405, headers: { Allow: "POST" } });

  let body: Json;
  try { body = await request.json(); } catch { return json(400, rpcError(null, -32700, "Parse error")); }
  if (!body || body.jsonrpc !== "2.0" || typeof body.method !== "string") return json(400, rpcError(body?.id, -32600, "Invalid request"));
  const { id, method } = body;
  const params = (body.params ?? {}) as Json;
  if (id === undefined) return new Response(null, { status: 202 }); // Notifications need no reply.

  const meta = (params._meta ?? {}) as Json;
  const modernVersion = meta["io.modelcontextprotocol/protocolVersion"] as string | undefined;
  const headerVersion = request.headers.get("MCP-Protocol-Version");

  // Legacy era: initialize handshake and initialize-era requests (no per-request _meta).
  if (method === "initialize") {
    const requested = String(params.protocolVersion ?? "");
    return json(200, {
      jsonrpc: "2.0", id,
      result: {
        protocolVersion: LEGACY.includes(requested) ? requested : LEGACY[0],
        capabilities: { tools: { listChanged: false } },
        serverInfo: SERVER_INFO,
        instructions: `${INSTRUCTIONS} This server also speaks MCP ${MODERN.join(", ")} without initialize.`,
      },
    });
  }
  let modern = false;
  if (modernVersion !== undefined) {
    modern = true;
    if (!MODERN.includes(modernVersion)) return json(400, rpcError(id, -32022, "Unsupported protocol version", { supported: [...MODERN, ...LEGACY], requested: modernVersion }));
    const mismatch = headerVersion !== modernVersion ? "MCP-Protocol-Version"
      : request.headers.get("Mcp-Method") !== method ? "Mcp-Method"
      : ["tools/call", "resources/read", "prompts/get"].includes(String(method)) && decodeHeader(request.headers.get("Mcp-Name")) !== String(params.name ?? params.uri) ? "Mcp-Name"
      : null;
    if (mismatch) return json(400, rpcError(id, -32020, `Header mismatch: ${mismatch} is missing or does not match the request body`));
  } else {
    const version = headerVersion ?? "2025-03-26";
    if (!LEGACY.includes(version)) return json(400, rpcError(id, -32022, "Unsupported protocol version", { supported: [...MODERN, ...LEGACY], requested: version }));
  }
  const ok = (result: Json) => json(200, { jsonrpc: "2.0", id, result: modern ? { resultType: "complete", ...result } : result });

  try {
    switch (method) {
      case "server/discover":
        return ok({ supportedVersions: [...MODERN, ...LEGACY], capabilities: { tools: {} }, _meta: { "io.modelcontextprotocol/serverInfo": SERVER_INFO }, instructions: INSTRUCTIONS });
      case "ping":
        return ok({});
      case "tools/list":
        return ok({ tools: TOOLS });
      case "tools/call": {
        const name = String(params.name ?? "");
        if (!TOOLS.some((t) => t.name === name)) return json(200, rpcError(id, -32602, `Unknown tool: ${name}`));
        return ok(await callTool(name, (params.arguments ?? {}) as Json, load));
      }
      default:
        return json(404, rpcError(id, -32601, "Method not found"));
    }
  } catch (error) {
    return json(502, rpcError(id, -32603, `Upstream content unavailable: ${(error as Error).message}`));
  }
}
