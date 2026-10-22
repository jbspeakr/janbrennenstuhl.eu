// Bunny Edge Script (middleware) for the www pull zone: requests that prefer text/markdown get the
// page's Markdown twin. Pair it with an edge rule that bypasses the cache when the Accept header
// contains "text/markdown" (docs/DELIVERY.md), or the twin could be cached under the HTML URL.
import * as BunnySDK from "https://esm.sh/@bunny.net/edgescript-sdk@0.11.2";
import { markdownPath } from "./negotiate-core.ts";

BunnySDK.net.http.servePullZone({ url: "https://www.janbrennenstuhl.eu" })
  .onOriginRequest((ctx) => {
    const target = markdownPath(ctx.request);
    if (!target) return Promise.resolve(ctx.request);
    const url = new URL(ctx.request.url);
    url.pathname = target;
    return Promise.resolve(new Request(url.toString(), ctx.request));
  })
  .onOriginResponse((ctx) => {
    const path = new URL(ctx.request.url).pathname;
    if (path.endsWith("/") || path.endsWith("/index.md")) ctx.response.headers.append("Vary", "Accept");
    return Promise.resolve(ctx.response);
  });
