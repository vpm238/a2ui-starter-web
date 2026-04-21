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
    - id: choice
      component: OptionsGrid
      prompt: "I'm here to…"
      options:
        - id: plan
          label: "Make a plan"
          rationale: "You know roughly what you want; you need structure to move forward."
          emoji: "🗺️"
          action: { event: { name: want_plan, context: {} } }
        - id: decide
          label: "Decide between options"
          rationale: "Two or three paths; you want a blunt second opinion."
          emoji: "⚖️"
          action: { event: { name: want_decision, context: {} } }
        - id: feedback
          label: "Get honest feedback"
          rationale: "Draft, idea, or situation you want someone to cut through."
          emoji: "🎯"
          action: { event: { name: want_feedback, context: {} } }
    - id: root
      component: Column
      children: [hdr, sub, choice]
      gap: 16
---

# Greeting skill

Static intake. No LLM call. Routes to three different skills based on the option tapped.
