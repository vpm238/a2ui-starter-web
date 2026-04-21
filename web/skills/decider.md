---
name: decider
description: Weighs two options. Takes a position. Triggered when the user wants a second opinion.
triggers:
  - want_decision
first_turn_skeleton:
  components:
    - id: hdr
      component: Text
      variant: h2
      text: { path: "/reply/headline" }
    - id: o1_name
      component: Text
      variant: h3
      text: { path: "/reply/option1_name" }
    - id: o1_take
      component: Text
      variant: body
      text: { path: "/reply/option1_take" }
    - id: o1_body
      component: Column
      children: [o1_name, o1_take]
    - id: o1_card
      component: Card
      child: o1_body
    - id: o2_name
      component: Text
      variant: h3
      text: { path: "/reply/option2_name" }
    - id: o2_take
      component: Text
      variant: body
      text: { path: "/reply/option2_take" }
    - id: o2_body
      component: Column
      children: [o2_name, o2_take]
    - id: o2_card
      component: Card
      child: o2_body
    - id: lean
      component: Text
      variant: body
      text: { path: "/reply/lean" }
    - id: root
      component: Column
      children: [hdr, o1_card, o2_card, lean]
first_turn_fill_fields:
  headline:
    description: ONE sentence introducing the comparison.
  option1_name:
    description: Short name for the first option (≤6 words).
  option1_take:
    description: 1-2 sentences — honest take on option 1.
  option2_name:
    description: Short name for the second option.
  option2_take:
    description: 1-2 sentences — honest take on option 2.
  lean:
    description: ONE sentence starting "My lean:" — commit to a direction.
---

# Decider skill

Weigh two options. Name each. Take a position. Don't hedge.

## Voice
Blunt. The whole value is a second opinion that commits.
