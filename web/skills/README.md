# Skills

Each `.md` file in this directory is a skill — a unit of agent behavior
the runtime can route a user event to. The format follows Anthropic's
[SKILL.md open standard](https://github.com/anthropics/claude-code/blob/main/packages/skills/README.md):
YAML frontmatter for the machine-readable parts, markdown body for the
system prompt.

Every skill file is loaded at app start by `loadSkillBundles()` in
`web/index.html` (section 5). Add a new skill by dropping a new `.md`
file here and adding its id to the `loadSkillBundles([...])` call.

## Frontmatter schema

```yaml
---
name: planner                          # required — maps to the runtime's skill id
description: "..."                     # optional — shown in dev tools
triggers:                              # event names that route here
  - want_plan                          # empty array = default/fallback skill
first_turn_skeleton:                   # initial A2UI component tree for this skill
  components:
    - id: root
      component: Column
      children: [intro, opts]
    - id: intro
      component: Text
      variant: h2
      text: { path: "/reply/intro" }   # path binding to the surface's data model
    - id: opts
      component: OptionsGrid
      options:
        - id: s1
          label: { path: "/reply/step1_label" }
          action: { event: { name: step_1_detail, context: {} } }
first_turn_fill_fields:                # the paths Claude streams into
  intro:
    description: "ONE sentence framing the plan. Ends with period."
  step1_label:
    description: "First step — imperative verb phrase (≤7 words)."
---

# Skill system prompt

Everything below the second `---` is the skill's system prompt. It's
passed verbatim to Claude when this skill is active.

## Voice
Direct. Specific. Imperative.
```

## How a turn runs

1. User taps an option or types a message.
2. `SkillRuntime` checks if the event matches any skill's `triggers`.
3. It sends to `MessageProcessor`:
   - `createSurface` with a new surfaceId
   - `updateDataModel` initializing `/reply` to `{}`
   - `updateComponents` with the skill's `skeleton` — UI renders
     immediately with shimmer placeholders where path-bound text is
     still empty
4. The runtime calls Claude with:
   - `system` = the skill's markdown body + the XML-tag response format
   - `messages` = conversation history + the current user message
5. Claude streams `<intro>...</intro><step1_label>...</step1_label>...`.
6. `FieldParser` emits a delta for each tag; the runtime sends
   `updateDataModel` with the growing accumulated value at `/reply/<tag>`.
7. The official renderer reacts to each update; bound text fields refresh.

The whole flow is visible in the wire-log panel (top-right "Show A2UI
wire log" button).

## Component shapes

Skills can use any of the 20 components in `starterCatalog`:

**basicCatalog (18):** `Text`, `Button`, `TextField`, `Row`, `Column`,
`List`, `Image`, `Icon`, `Video`, `AudioPlayer`, `Card`, `Divider`,
`CheckBox`, `Slider`, `DateTimeInput`, `ChoicePicker`, `Tabs`, `Modal`.

**Extensions (2):**
- `OptionsGrid` — `{prompt?, options: [{id, label, rationale?, emoji?, action}]}`
- `RichMessageCard` — `{recommendationType?, confidence?, headline?, rationale?, confirmAction?, dismissAction?}`

All fields that accept a string also accept `{path: "/..."}` to bind to
the surface's data model. All `action.event.name` must be a string at
dispatch time; it can be streamed in as a path binding too.

The full zod schemas live inline at the top of `web/index.html` (Section 1).
Invalid shapes are rejected by the `MessageProcessor` at `processMessages`
time with a detailed zod error.

## Adding a new skill

1. Create `web/skills/my-skill.md` with frontmatter + body.
2. Register it in the `loadSkillBundles([...])` call in `web/index.html`.
3. Add an option in `greeting.md` (or elsewhere) whose `action.event.name`
   matches your skill's `triggers`.
4. Reload — no build step.
