// Bunny Edge Script (standalone) entry point. Deploy on its own pull zone, e.g. mcp.janbrennenstuhl.eu/mcp;
// scripts/mcp_script.py bundles it with handler.ts and the publish job deploys it (docs/DELIVERY.md).
import * as BunnySDK from "https://esm.sh/@bunny.net/edgescript-sdk@0.11.2";
import { defaultLoader, handle } from "./handler.ts";

const load = defaultLoader();
BunnySDK.net.http.serve(async (request: Request) => {
  const path = new URL(request.url).pathname;
  if (path !== "/mcp") return new Response("Not found. The MCP endpoint is /mcp.", { status: 404 });
  return handle(request, load);
});
