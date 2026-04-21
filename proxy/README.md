# LLM proxy — Cloudflare Worker

Tiny proxy that hides your `ANTHROPIC_API_KEY` from the browser. The web app
POSTs to `<worker-url>/v1/messages`, the worker forwards to Anthropic with
the key attached, streams the SSE response back verbatim.

~70 lines of JS. Free tier: 100k requests/day.

## Deploy

```bash
npm install -g wrangler
cd proxy
wrangler secret put ANTHROPIC_API_KEY     # paste your key when prompted
wrangler deploy
```

Wrangler prints the live URL (e.g. `https://a2ui-llm-proxy.<you>.workers.dev`).

## Point the web app at it

In your fork/deploy of `/web/index.html`, edit the `<head>` to add:

```html
<script>window.A2UI_PROXY_URL = 'https://a2ui-llm-proxy.<you>.workers.dev';</script>
```

Or set it at the beginning of the main module script. If `A2UI_PROXY_URL` is
unset, the app falls back to asking the user to paste an API key that gets
stored in `localStorage` — useful for purely local dev, but not shippable.

## Alternative hosts

This same file deploys with minor changes to:

- **Fly.io** / **Railway** — as a Node/Deno server; change the `default.fetch`
  signature to a standard `http.createServer` handler
- **Vercel Functions** — as `api/v1/messages.js`, export `export default async function handler(req, res)`
- **AWS Lambda + API Gateway** — similar handler shape

The Cloudflare Worker variant is shortest + fastest cold-start.

## Security notes

- **Lock `ALLOWED_ORIGINS`** in `llm-proxy.js` to your GitHub Pages URL before
  deploying. The default `'*'` is for local dev; it means anyone can use your
  proxy (and burn your API quota).
- The worker has no rate limiting. Add a `fetch` rate limiter via
  Cloudflare's built-in bindings (`env.RATE_LIMITER`) for production.
- Consider requiring a shared secret header to prevent anonymous abuse.
