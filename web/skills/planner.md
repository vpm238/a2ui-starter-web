---
name: planner
description: Breaks goals into 3 concrete first steps. Triggered when the user wants structured action.
triggers:
  - want_plan
first_turn_skeleton:
  components:
    - id: intro
      component: Text
      variant: h2
      text: { path: "/reply/intro" }
    - id: opts
      component: OptionsGrid
      prompt: "Take it step by step:"
      options:
        - id: s1
          label: { path: "/reply/step1_label" }
          rationale: { path: "/reply/step1_rationale" }
          emoji: "1️⃣"
          action: { event: { name: step_1_detail, context: {} } }
        - id: s2
          label: { path: "/reply/step2_label" }
          rationale: { path: "/reply/step2_rationale" }
          emoji: "2️⃣"
          action: { event: { name: step_2_detail, context: {} } }
        - id: s3
          label: { path: "/reply/step3_label" }
          rationale: { path: "/reply/step3_rationale" }
          emoji: "3️⃣"
          action: { event: { name: step_3_detail, context: {} } }
    - id: root
      component: Column
      children: [intro, opts]
      gap: 14
first_turn_fill_fields:
  intro:
    description: ONE sentence framing the plan. Ends with period.
  step1_label:
    description: The first step. Imperative verb phrase (≤7 words).
  step1_rationale:
    description: ONE sentence explaining why this is step 1.
  step2_label:
    description: The second step.
  step2_rationale:
    description: ONE sentence — why this follows step 1.
  step3_label:
    description: The third step.
  step3_rationale:
    description: ONE sentence — why this seals the early effort.
---

# Planner skill

Turn any goal into 3 specific, ordered first steps. No generic "plan your day"
advice — real steps a person can take today.

## Voice
Direct, specific, imperative. If the user's goal is fuzzy, pick a reasonable
concrete interpretation and go.
