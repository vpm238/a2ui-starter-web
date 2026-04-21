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
    - id: step1_label
      component: Text
      variant: body
      text: { path: "/reply/step1_label" }
    - id: step1_btn
      component: Button
      child: step1_label
      variant: default
      action: { event: { name: step_1_detail, context: {} } }
    - id: step1_rationale
      component: Text
      variant: caption
      text: { path: "/reply/step1_rationale" }
    - id: step2_label
      component: Text
      variant: body
      text: { path: "/reply/step2_label" }
    - id: step2_btn
      component: Button
      child: step2_label
      variant: default
      action: { event: { name: step_2_detail, context: {} } }
    - id: step2_rationale
      component: Text
      variant: caption
      text: { path: "/reply/step2_rationale" }
    - id: step3_label
      component: Text
      variant: body
      text: { path: "/reply/step3_label" }
    - id: step3_btn
      component: Button
      child: step3_label
      variant: default
      action: { event: { name: step_3_detail, context: {} } }
    - id: step3_rationale
      component: Text
      variant: caption
      text: { path: "/reply/step3_rationale" }
    - id: root
      component: Column
      children: [intro, step1_btn, step1_rationale, step2_btn, step2_rationale, step3_btn, step3_rationale]
first_turn_fill_fields:
  intro:
    description: ONE sentence framing the plan. Begins with an emoji like 🗺️ or 1️⃣. Ends with period.
  step1_label:
    description: "1️⃣ — The first step. Imperative verb phrase (≤7 words). Start with an emoji then the action."
  step1_rationale:
    description: ONE sentence explaining why this is step 1.
  step2_label:
    description: "2️⃣ — The second step. Same style."
  step2_rationale:
    description: ONE sentence — why this follows step 1.
  step3_label:
    description: "3️⃣ — The third step. Same style."
  step3_rationale:
    description: ONE sentence — why this seals the early effort.
---

# Planner skill

Turn any goal into 3 specific, ordered first steps. No generic "plan your day"
advice — real steps a person can take today. Emojis in step labels give them visual anchors.

## Voice
Direct, specific, imperative. If the user's goal is fuzzy, pick a reasonable
concrete interpretation and go.
