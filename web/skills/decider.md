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
    - id: o1_txt
      component: Text
      variant: body
      text: { path: "/reply/option1_take" }
    - id: o1
      component: Card
      title: { path: "/reply/option1_name" }
      child: o1_txt
    - id: o2_txt
      component: Text
      variant: body
      text: { path: "/reply/option2_take" }
    - id: o2
      component: Card
      title: { path: "/reply/option2_name" }
      child: o2_txt
    - id: lean
      component: Text
      variant: body
      text: { path: "/reply/lean" }
    - id: root
      component: Column
      children: [hdr, o1, o2, lean]
      gap: 14
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
