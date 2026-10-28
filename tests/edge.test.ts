// Unit tests for the edge scripts. Run: npm run test:edge (Node 22.18+/23.6+ strips TypeScript types).
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { handle } from "../edge/mcp/handler.ts";
import { markdownPath, prefersMarkdown } from "../edge/negotiate-core.ts";

const fixtures: Record<string, unknown> = {
  "/search/index.json": [
    { id: "jb-guide-token-exchange", title: "How does OAuth 2.0 Token Exchange keep provider tokens away from agents?", description: "RFC 8693", url: "/knowledge-base/agent-identity/token-exchange/", kind: "guide", topics: ["agentic-engineering"], published: "2026-10-13", content: "token exchange gateway broker", sections: [{ id: "how-it-works", title: "How it works", text: "the gateway exchanges" }] },
    { id: "jb-jwks", title: "Mastering JWKS", description: "keys", url: "/jwks/", kind: "essay", topics: ["tokens-jwt"], published: "2023-06-02", content: "json web key set", sections: [] },
  ],
  "/catalog.json": { topics: [{ id: "tokens-jwt", title: "Tokens & JWT" }], items: [{ id: "jb-jwks", canonical_url: "https://www.janbrennenstuhl.eu/jwks/", markdown_url: "https://www.janbrennenstuhl.eu/jwks/index.md", topics: ["tokens-jwt"] }] },
  "/findings.json": { items: [{ id: "f-x", text: "Reuse is common", article: "Reuse", article_id: "jb-a", url: "https://www.janbrennenstuhl.eu/a/#f-x" }] },
  "/jwks/index.md": "---\nid: jb-jwks\n---\n# Mastering JWKS\n",
};
const load = async (path: string) => { if (!(path in fixtures)) throw new Error("missing " + path); return fixtures[path]; };

const MODERN = "2026-07-28";
function modern(method: string, params: Record<string, unknown> = {}, headers: Record<string, string> = {}) {
  const body = { jsonrpc: "2.0", id: 1, method, params: { ...params, _meta: { "io.modelcontextprotocol/protocolVersion": MODERN, "io.modelcontextprotocol/clientCapabilities": {} } } };
  const h: Record<string, string> = { "Content-Type": "application/json", "MCP-Protocol-Version": MODERN, "Mcp-Method": method, ...headers };
  if (method === "tools/call" && !("Mcp-Name" in headers)) h["Mcp-Name"] = String(params.name);
  return new Request("https://mcp.example/mcp", { method: "POST", headers: h, body: JSON.stringify(body) });
}

test("server/discover lists versions, tools capability and server info", async () => {
  const res = await handle(modern("server/discover"), load);
  assert.equal(res.status, 200);
  const { result } = await res.json();
  assert.equal(result.resultType, "complete");
  assert.ok(result.supportedVersions.includes(MODERN));
  assert.deepEqual(result.capabilities, { tools: {} });
});

test("modern tools/call search returns the best match with its section URL", async () => {
  const res = await handle(modern("tools/call", { name: "search_site", arguments: { query: "token exchange" } }), load);
  const { result } = await res.json();
  assert.equal(result.structuredContent.results[0].id, "jb-guide-token-exchange");
  assert.equal(result.structuredContent.results[0].section.url, "https://www.janbrennenstuhl.eu/knowledge-base/agent-identity/token-exchange/#how-it-works");
});

test("get_entry resolves catalog ids only, never arbitrary URLs", async () => {
  const ok = await (await handle(modern("tools/call", { name: "get_entry", arguments: { id: "jb-jwks" } }), load)).json();
  assert.match(ok.result.content[0].text, /# Mastering JWKS/);
  const bad = await (await handle(modern("tools/call", { name: "get_entry", arguments: { id: "https://evil.example/" } }), load)).json();
  assert.equal(bad.result.isError, true);
});

test("header mismatches are rejected with HeaderMismatch", async () => {
  const res = await handle(modern("tools/call", { name: "list_topics", arguments: {} }, { "Mcp-Name": "search_site" }), load);
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error.code, -32020);
  const missing = await handle(modern("tools/list", {}, { "Mcp-Method": "tools/call" }), load);
  assert.equal((await missing.json()).error.code, -32020);
});

test("base64 sentinel Mcp-Name values are decoded before comparison", async () => {
  const encoded = "=?base64?" + Buffer.from("list_topics").toString("base64") + "?=";
  const res = await handle(modern("tools/call", { name: "list_topics", arguments: {} }, { "Mcp-Name": encoded }), load);
  assert.equal(res.status, 200);
  assert.equal((await res.json()).result.structuredContent.topics[0].entries, 1);
});

test("unsupported modern version lists supported versions", async () => {
  const req = new Request("https://mcp.example/mcp", { method: "POST", headers: { "MCP-Protocol-Version": "1900-01-01", "Mcp-Method": "tools/list" }, body: JSON.stringify({ jsonrpc: "2.0", id: 7, method: "tools/list", params: { _meta: { "io.modelcontextprotocol/protocolVersion": "1900-01-01" } } }) });
  const res = await handle(req, load);
  assert.equal(res.status, 400);
  const body = await res.json();
  assert.equal(body.error.code, -32022);
  assert.ok(body.error.data.supported.includes(MODERN));
});

test("legacy clients can initialize and list tools", async () => {
  const init = await handle(new Request("https://mcp.example/mcp", { method: "POST", body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "initialize", params: { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "t", version: "1" } } }) }), load);
  const initResult = (await init.json()).result;
  assert.equal(initResult.protocolVersion, "2025-06-18");
  // The licence policy agents read must match docs/DECISIONS.md: CC BY 4.0, training permitted.
  assert.match(initResult.instructions, /CC BY 4\.0/);
  assert.doesNotMatch(initResult.instructions, /reserved/i);
  const note = await handle(new Request("https://mcp.example/mcp", { method: "POST", body: JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized" }) }), load);
  assert.equal(note.status, 202);
  const list = await handle(new Request("https://mcp.example/mcp", { method: "POST", headers: { "MCP-Protocol-Version": "2025-06-18" }, body: JSON.stringify({ jsonrpc: "2.0", id: 2, method: "tools/list" }) }), load);
  const tools = (await list.json()).result.tools.map((t: { name: string }) => t.name);
  assert.deepEqual(tools, ["search_site", "get_entry", "get_findings", "list_topics"]);
});

test("GET is not allowed and foreign browser origins are refused", async () => {
  assert.equal((await handle(new Request("https://mcp.example/mcp"), load)).status, 405);
  const foreign = await handle(new Request("https://mcp.example/mcp", { method: "POST", headers: { Origin: "https://evil.example" }, body: "{}" }), load);
  assert.equal(foreign.status, 403);
});

test("content negotiation prefers Markdown only when asked for it", () => {
  assert.equal(prefersMarkdown("text/markdown"), true);
  assert.equal(prefersMarkdown("text/markdown, text/html;q=0.8"), true);
  assert.equal(prefersMarkdown("text/html,application/xhtml+xml,*/*;q=0.8"), false);
  assert.equal(prefersMarkdown("text/html, text/markdown;q=0.5"), false);
  assert.equal(markdownPath(new Request("https://x/jwks/", { headers: { Accept: "text/markdown" } })), "/jwks/index.md");
  assert.equal(markdownPath(new Request("https://x/feed.json", { headers: { Accept: "text/markdown" } })), null);
});

test("the built catalog carries topics for list_topics", { skip: !safeExists("public/catalog.json") }, () => {
  const catalog = JSON.parse(readFileSync("public/catalog.json", "utf8"));
  assert.equal(catalog.topics.length, 6);
});
function safeExists(p: string) { try { readFileSync(p); return true; } catch { return false; } }
