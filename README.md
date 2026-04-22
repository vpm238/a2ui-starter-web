# a2ui-starter-web

**Reference client-side [A2UI](https://a2ui.org/) starter for the browser.** Uses Google's official [`@a2ui/web_core`](https://www.npmjs.com/package/@a2ui/web_core) state machine + [`@a2ui/lit`](https://www.npmjs.com/package/@a2ui/lit) renderer, extended with a custom catalog. No bundler, no backend state. Claude via a tiny proxy.

### 👉 [Try it live: vpm238.github.io/a2ui-starter-web](https://vpm238.github.io/a2ui-starter-web/)

No install. Tap an option or type something — Claude streams replies into A2UI surfaces in real time. Top-right *Show A2UI wire log* to watch every v0.9 message go by. Top-right *Kitchen sink* to see every component in the catalog render at once.

Companion to [`a2ui-starter-swiftui`](https://github.com/vpm238/a2ui-starter-swiftui) — same four skills, same skeleton-first streaming pattern, same [progressive-rendering RFC primitives](https://github.com/vpm238/a2ui-progressive-rendering-rfc).

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│ index.html  (self-contained, no build step)                  │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐    │
│   │  A2UIStarter  (Lit element — chat shell)             │    │
│   └─────────────────────────────────────────────────────┘    │
│                          │                                    │
│   ┌─────────────────────────────────────────────────────┐    │
│   │  SkillRuntime  — routes user events to skills,       │    │
│   │  streams Claude's reply, emits v0.9 messages          │    │
│   └─────────────────────────────────────────────────────┘    │
│                          │ processMessages([...])             │
│   ┌─────────────────────────────────────────────────────┐    │
│   │  @a2ui/web_core  MessageProcessor                    │    │
│   │  ─ validates every message against starterCatalog    │    │
│   │  ─ owns all surface state (SurfaceModel per turn)    │    │
│   └─────────────────────────────────────────────────────┘    │
│                          │ renders via                        │
│   ┌─────────────────────────────────────────────────────┐    │
│   │  @a2ui/lit  <a2ui-surface>                           │    │
│   │  + basicCatalog  (18 components)                     │    │
│   │  + OptionsGrid   (extension — Lit + zod)             │    │
│   │  + RichMessageCard (extension — Lit + zod)           │    │
│   └─────────────────────────────────────────────────────┘    │
└──────────────────────────────┬───────────────────────────────┘
                               │ fetch()  POST /v1/messages  (SSE)
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ proxy/llm-proxy.js  (Cloudflare Worker, ~70 lines)           │
│  ─ holds ANTHROPIC_API_KEY as a Worker secret                │
│  ─ forwards to api.anthropic.com, streams SSE back           │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
                  https://api.anthropic.com/v1/messages
```

Three packages load from `esm.sh` via an importmap — no bundler, no `npm install`:
`@a2ui/web_core@0.9.2`, `@a2ui/lit@0.9.3`, `zod@3.25.76`, plus `lit` and `js-yaml`.

## What makes this "A2UI"

Every user-visible turn flows through Google's `MessageProcessor`. Each agent reply is a sequence of v0.9 wire messages:

```json
{"version":"v0.9", "createSurface":{"surfaceId":"msg_1","catalogId":"a2ui-starter/core@0.1"}}
{"version":"v0.9", "updateDataModel":{"surfaceId":"msg_1","value":{"reply":{}}}}
{"version":"v0.9", "updateComponents":{"surfaceId":"msg_1","components":[...]}}
{"version":"v0.9", "updateDataModel":{"surfaceId":"msg_1","path":"/reply/intro","value":"..."}}
```

Click **"Show A2UI wire log"** in the running app (top-right button) to watch these fly by in real time.

## Quick run (local, recommended for demos)

```bash
git clone https://github.com/vpm238/a2ui-starter-web
cd a2ui-starter-web

# Terminal 1 — Anthropic proxy on :8787 (keeps your API key off the browser)
export ANTHROPIC_API_KEY="sk-ant-..."
python3 proxy/local-proxy.py

# Terminal 2 — static server on :5173
python3 -m http.server 5173
# Open http://localhost:5173
```

The app auto-detects localhost and routes LLM calls through `http://localhost:8787`. Override with `?proxy=https://...` if you want.

## Quick run (no proxy, direct Anthropic)

```bash
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

2. **Point the web app at the proxy.** At the top of `index.html`, inside `<head>`, add:
   ```html
   <script>window.A2UI_PROXY_URL = 'https://a2ui-llm-proxy.you.workers.dev';</script>
   ```

3. **Enable GitHub Pages** at `Settings → Pages`:
   - Source: **Deploy from a branch**
   - Branch: `main`, folder: `/` (root)
   - Save

~60 seconds later, your starter is live at `https://<you>.github.io/a2ui-starter-web/`.

## The starter catalog

```js
starterCatalog = new Catalog('a2ui-starter/core@0.1', [
  ...basicCatalog.components,   // 18 official components
  A2uiOptionsGrid,              // extension — tap-to-fire options
  A2uiRichMessageCard,          // extension — opinionated recommendation
])
```

basicCatalog ships: `Text`, `Button`, `TextField`, `Row`, `Column`, `List`, `Image`, `Icon`, `Video`, `AudioPlayer`, `Card`, `Divider`, `CheckBox`, `Slider`, `DateTimeInput`, `ChoicePicker`, `Tabs`, `Modal`.

Our two extensions add UX patterns the basic set doesn't cover: a stacked list where each row fires an event (common for agent intake) and a strong-take recommendation card. Both are full-fidelity A2UI components — schema-validated, data-bound, action-dispatching — defined inline in `index.html` (sections 1 & 2, ~110 lines each).

See the **Kitchen sink** button in the running app for a live render of all 20 components.

## Skills

Four LLM-backed skills + one static kitchen sink, all in [`skills/`](./skills/) as SKILL.md files (YAML frontmatter + markdown body):

| Skill | Trigger | What it does |
|---|---|---|
| `greeting` | (default) | Static intake — routes to one of the three below |
| `planner` | `want_plan` | Breaks a goal into 3 concrete first steps |
| `decider` | `want_decision` | Weighs two options. Takes a position |
| `critic` | `want_feedback` | One strong opinionated piece of feedback |
| `kitchen` | `show_kitchen_sink` | Renders every component in the catalog |

The frontmatter's `first_turn_skeleton.components` is the initial A2UI component tree. `first_turn_fill_fields` names the data-model paths Claude streams into. The markdown body below the fence is the skill's system prompt.

See [`skills/README.md`](./skills/README.md) for the format spec.

## Streaming strategy

Anthropic SSE → `FieldParser` → per-field deltas → `updateDataModel` with `set` (accumulated value). Client-side typewriter smoothing splits chunks into char-paced updates so the rendering feels like typing instead of popping. Override the pace via `?smooth=N` (chars/sec; default 220; `?smooth=0` disables).

RFC Proposal 3's `append` patch op would be more efficient on the wire — the official `MessageProcessor` only supports `set` in v0.9, so we send growing accumulated values. When `append` lands, swap `_setSmoothly` for an append-op emitter and the wire traffic drops by ~90%.

## Project layout

```
a2ui-starter-web/              # repo root is also GH Pages root
├── README.md                  # you are here
├── LICENSE                    # MIT
├── index.html                 # the whole app (~930 lines)
├── official-test.html         # standalone 5-step renderer sanity check
├── skill.manifest.json        # experimental host manifest
├── skills/                    # SKILL.md per skill, loaded at runtime
│   ├── README.md              # SKILL.md format
│   ├── greeting.md            # intake — no LLM call
│   ├── planner.md             # → 3 ordered steps
│   ├── decider.md             # → two-option comparison
│   ├── critic.md              # → strong-take card
│   └── kitchen.md             # static kitchen sink
├── catalog/
│   └── catalog.json           # reference schema for the extension components
└── proxy/                     # Anthropic proxy
    ├── README.md
    ├── llm-proxy.js           # Cloudflare Worker (deploy with wrangler)
    ├── local-proxy.py         # zero-dep local dev
    └── wrangler.toml
```

## Compared to the SwiftUI starter

| | [SwiftUI starter](https://github.com/vpm238/a2ui-starter-swiftui) | Web starter (this) |
|---|---|---|
| Platform | macOS / iOS / visionOS | Any modern browser |
| Build step | `swift run` | None — open `index.html` |
| Renderer | [`a2ui-swiftui`](https://github.com/vpm238/a2ui-swiftui) (own) | `@a2ui/lit` (Google official) + 2 extensions |
| Skill runtime | [`a2ui-skills-swiftui`](https://github.com/vpm238/a2ui-skills-swiftui) (own) | Inline `SkillRuntime` + `FieldParser` |
| LLM provider | Direct via `AnthropicLLMProvider` | Cloudflare Worker proxy (key stays server-side) |
| Catalog | 13 components (all inline) | 18 from `basicCatalog` + 2 extensions |

Same protocol. Same skill shapes. Same streaming UX.

## Requirements

- A modern browser (Chrome/Safari/Firefox 2024+)
- An Anthropic API key
- For shipping: a Cloudflare account (free tier covers this)

## License

MIT. See [LICENSE](LICENSE).

## Related

- [`a2ui-swiftui`](https://github.com/vpm238/a2ui-swiftui) — Swift/SwiftUI renderer library
- [`a2ui-skills-swiftui`](https://github.com/vpm238/a2ui-skills-swiftui) — Swift skill runtime
- [`a2ui-starter-swiftui`](https://github.com/vpm238/a2ui-starter-swiftui) — Swift reference app
- [`a2ui-progressive-rendering-rfc`](https://github.com/vpm238/a2ui-progressive-rendering-rfc) — RFC + demo for streaming primitives
- [Google A2UI spec](https://a2ui.org/) — the protocol
