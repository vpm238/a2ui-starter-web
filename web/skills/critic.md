---
name: critic
description: One strong opinionated piece of feedback. Triggered when the user wants someone to cut through on a draft, idea, or situation.
triggers:
  - want_feedback
first_turn_skeleton:
  components:
    - id: rec
      component: RichMessageCard
      recommendationType: strong
      confidence: medium
      headline: { path: "/reply/headline" }
      rationale: { path: "/reply/rationale" }
      confirmAction:
        label: { path: "/reply/confirm_label" }
        event: { name: { path: "/reply/confirm_event" }, context: {} }
      dismissAction:
        label: { path: "/reply/dismiss_label" }
        event: { name: { path: "/reply/dismiss_event" }, context: {} }
    - id: root
      component: Column
      children: [rec]
      gap: 12
first_turn_fill_fields:
  headline:
    description: ONE direct sentence — your take. No hedging.
  rationale:
    description: 2-3 sentences explaining the take.
  confirm_label:
    description: Short action button text (≤5 words).
  confirm_event:
    description: "Event name snake_case: concrete_fix, show_example, tradeoffs."
  dismiss_label:
    description: Short dismiss text (≤5 words).
  dismiss_event:
    description: "Event name snake_case. Usually `restart`."
---

# Critic skill

Give one honest piece of feedback. No hedging sandwich.

## Voice
First person. Direct. If it has a real problem, say so. If it's good, say that.
