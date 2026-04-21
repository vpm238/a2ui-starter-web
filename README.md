# a2ui-starter-web

**Reference client-side [A2UI](https://a2ui.org/) starter for the browser.** Lit + client-side skills + Anthropic Claude via a tiny proxy. Zero bundler, zero backend state.

Companion to [`a2ui-starter-swiftui`](https://github.com/vpm238/a2ui-starter-swiftui) — same four skills (`greeting`, `planner`, `decider`, `critic`), same skeleton-first streaming pattern, same [progressive-rendering RFC primitives 1–3](https://github.com/vpm238/a2ui-progressive-rendering-rfc). Runs in any modern browser; hostable on GitHub Pages.

## Architecture

```
   ┌──────────────────────────────────┐
   │ web/index.html                    │
   │                                   │ lit-html renderer, inline
   │ <a2ui-starter> Lit element        │ JSON Pointer + data-binding
   │   ├── SurfaceState (per turn)     │ FieldParser + SkillRuntime
   │   ├── SkillRuntime                │ (all in ~650 lines of JS)
   │   └── renderComponent(…)          │
   │                                   │
   │ GH Pages deployable as-is         │
   └────────────────┬─────────────────┘
                    │ fetch()  POST /v1/messages  (streaming)
                    ▼
   ┌──────────────────────────────────┐
   │ proxy/llm-proxy.js (CF Worker)    │
   │                                   │ forwards to api.anthropic.com
   │ Hides ANTHROPIC_API_KEY in        │ with key from a Worker secret;
   │ Cloudflare Worker secrets         │ streams SSE response back
   └──────────────────────────────────┘
                    │
                    ▼
         https://api.anthropic.com/v1/messages
```

## Quick run (local, with local proxy — recommended for demos)

Two terminals. First, the local proxy (keeps your API key off the browser):

```bash
git clone https://github.com/vpm238/a2ui-starter-web
cd a2ui-starter-web
export ANTHROPIC_API_KEY="sk-ant-..."
python3 proxy/local-proxy.py      # listens on http://localhost:8787
```

Second terminal — serve the web app and point it at the proxy:

```bash
cd web
# Add one line to point the app at the local proxy before the main script:
printf '%s\n' "<script>window.A2UI_PROXY_URL='http://localhost:8787';</script>" > /tmp/pr.html
sed -i.bak '/<script type="module">/i\
'"$(cat /tmp/pr.html)" index.html   # one-time local patch (don't commit)
python3 -m http.server 5173
# Open http://localhost:5173
```

Or simpler — open `web/index.html` directly and accept the API-key prompt. That keeps the key in localStorage, no proxy required, but exposes it to any page with DevTools access. Fine for dev, never for a public demo.

## Quick run (no proxy, direct Anthropic)

```bash
cd a2ui-starter-web/web
python3 -m http.server 5173
# Open http://localhost:5173
# First load: prompt for API key → stored in localStorage
# Clear with `localStorage.clear()` in DevTools when done
```

## Ship it (Pages + Worker)

1. **Deploy the proxy** (see [proxy/README.md](./proxy/README.md)):
   ```bash
   cd proxy
   npm install -g wrangler
   wrangler secret put ANTHROPIC_API_KEY
   wrangler deploy
   # Copy the printed URL, e.g. https://a2ui-llm-proxy.you.workers.dev
   ```

2. **Point the web app at the proxy.** In `web/index.html`, add before the module script:
   ```html
   <script>window.A2UI_PROXY_URL = 'https://a2ui-llm-proxy.you.workers.dev';</script>
   ```

3. **Enable GitHub Pages** at `Settings → Pages`:
   - Source: **Deploy from a branch**
   - Branch: `main`, folder: `/web`
   - Save

~60 seconds later, your starter is live at `https://vpm238.github.io/a2ui-starter-web/`.

## What it demonstrates

Exactly what [`a2ui-starter-swiftui`](https://github.com/vpm238/a2ui-starter-swiftui) does, but in a browser:

- **Client-side skills.** Four skills as JS objects: greeting's static intake, planner's numbered OptionsGrid, decider's stacked Cards, critic's RichMessageCard.
- **Skeleton-first streaming.** Skeleton renders in <100ms; Claude streams only the text values.
- **RFC Proposal 1** (pending state): shimmer placeholders while fields haven't arrived.
- **RFC Proposal 2** (streaming flag): typewriter caret on bound text during streaming.
- **RFC Proposal 3** (append patch op): each chunk is appended rather than re-sent whole.
- **Direct Anthropic streaming:** SSE parsed in-browser, fed to `FieldParser`, pushed to `SurfaceState`, re-renders incrementally.

## Project structure

```
a2ui-starter-web/
├── README.md
├── LICENSE
├── skill.manifest.json     # experimental host manifest
├── web/                    # GH Pages root
│   ├── index.html          # self-contained — Lit from esm.sh, ~650 lines
│   └── (no build step)
├── proxy/                  # Cloudflare Worker
│   ├── llm-proxy.js
│   ├── wrangler.toml
│   └── README.md
```

## Compared to the SwiftUI starter

| | SwiftUI starter | Web starter (this) |
|---|---|---|
| Platform | macOS / iOS / visionOS | Any modern browser |
| Build step | `swift run` | None — open `index.html` |
| Bundler | SPM | None |
| Renderer library | `a2ui-swiftui` SPM package | Inline JS (~650 lines, Lit from CDN) |
| Skill runtime | `a2ui-skills-swiftui` SPM package | Inline JS (`SkillRuntime`, `FieldParser`) |
| LLM provider | Direct via `AnthropicLLMProvider` | Via Cloudflare Worker proxy (key stays server-side) |
| SKILL.md source | Bundled Swift strings, parsed with Yams | JS objects (no YAML parser) |

Same protocol, same skill shapes, same streaming UX.

## Requirements

- A modern browser (Chrome/Safari/Firefox 2024+)
- An Anthropic API key (runtime-prompt for local dev, Worker secret for deploy)
- For shipping: a Cloudflare account (free tier) + 5 minutes

## License

MIT. See [LICENSE](LICENSE).

## Related

- [`a2ui-swiftui`](https://github.com/vpm238/a2ui-swiftui) — Swift/SwiftUI renderer library
- [`a2ui-skills-swiftui`](https://github.com/vpm238/a2ui-skills-swiftui) — Swift skill runtime
- [`a2ui-starter-swiftui`](https://github.com/vpm238/a2ui-starter-swiftui) — Swift reference app (same 4 skills)
- [`a2ui-progressive-rendering-rfc`](https://github.com/vpm238/a2ui-progressive-rendering-rfc) — RFC + demo for streaming primitives
