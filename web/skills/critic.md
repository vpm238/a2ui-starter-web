---
name: critic
description: One strong opinionated piece of feedback. Triggered when the user wants someone to cut through on a draft, idea, or situation.
triggers:
  - want_feedback
first_turn_skeleton:
  components:
    - id: tag
      component: Text
      variant: caption
      text: "🎯 STRONG TAKE · MEDIUM CONFIDENCE"
    - id: headline
      component: Text
      variant: h2
      text: { path: "/reply/headline" }
    - id: rationale
      component: Text
      variant: body
      text: { path: "/reply/rationale" }
    - id: confirm_label
      component: Text
      variant: body
      text: { path: "/reply/confirm_label" }
    - id: confirm_btn
      component: Button
      child: confirm_label
      variant: primary
      action: { event: { name: { path: "/reply/confirm_event" }, context: {} } }
    - id: dismiss_label
      component: Text
      variant: body
      text: { path: "/reply/dismiss_label" }
    - id: dismiss_btn
      component: Button
      child: dismiss_label
      variant: borderless
      action: { event: { name: { path: "/reply/dismiss_event" }, context: {} } }
    - id: actions
      component: Row
      children: [confirm_btn, dismiss_btn]
    - id: card_body
      component: Column
      children: [tag, headline, rationale, actions]
    - id: card
      component: Card
      child: card_body
    - id: root
      component: Column
      children: [card]
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
