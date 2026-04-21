---
name: greeting
description: Static intake surface shown on connect. Routes to one of three specialized skills based on the option tapped.
triggers: []
first_turn_skeleton:
  components:
    - id: hdr
      component: Text
      variant: h1
      text: "What can I help you think through?"
    - id: sub
      component: Text
      variant: body
      text: "A few honest starting points. Pick whichever is closest to what you need."
    - id: o1_label
      component: Text
      variant: body
      text: "🗺️ Make a plan — structured action for something you already want to do"
    - id: o1_btn
      component: Button
      child: o1_label
      variant: primary
      action: { event: { name: want_plan, context: {} } }
    - id: o2_label
      component: Text
      variant: body
      text: "⚖️ Decide between options — blunt second opinion on two paths"
    - id: o2_btn
      component: Button
      child: o2_label
      variant: default
      action: { event: { name: want_decision, context: {} } }
    - id: o3_label
      component: Text
      variant: body
      text: "🎯 Get honest feedback — cut through on a draft, idea, or situation"
    - id: o3_btn
      component: Button
      child: o3_label
      variant: default
      action: { event: { name: want_feedback, context: {} } }
    - id: root
      component: Column
      children: [hdr, sub, o1_btn, o2_btn, o3_btn]
---

# Greeting skill

Static intake. No LLM call. Routes to three different skills based on the option tapped.
