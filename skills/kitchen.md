---
name: kitchen
description: "Kitchen sink: one surface showcasing every basicCatalog primitive + the two starter extensions."
triggers:
  - show_kitchen_sink
first_turn_skeleton:
  components:
    # ---- Header ---------------------------------------------------------
    - id: title
      component: Text
      variant: h1
      text: "A2UI Kitchen Sink"
    - id: subtitle
      component: Text
      variant: body
      text: "Every component shipped by @a2ui/lit's basicCatalog, plus the two starter extensions (OptionsGrid, RichMessageCard). Rendered by the official renderer, served from this page."
    - id: divider_top
      component: Divider

    # ---- Text variants --------------------------------------------------
    - id: s_text
      component: Text
      variant: h2
      text: "Text variants"
    - id: t_h1
      component: Text
      variant: h1
      text: "Heading h1"
    - id: t_h2
      component: Text
      variant: h2
      text: "Heading h2"
    - id: t_h3
      component: Text
      variant: h3
      text: "Heading h3"
    - id: t_body
      component: Text
      variant: body
      text: "Body text — the default. Line height should be readable."
    - id: t_caption
      component: Text
      variant: caption
      text: "Caption text — smaller, muted."
    - id: g_text
      component: Column
      children: [s_text, t_h1, t_h2, t_h3, t_body, t_caption]

    # ---- Row + Buttons --------------------------------------------------
    - id: s_btn
      component: Text
      variant: h2
      text: "Row + Button variants"
    - id: btn_p_label
      component: Text
      text: "Primary"
    - id: btn_p
      component: Button
      variant: primary
      child: btn_p_label
      action: { event: { name: kitchen_click, context: { which: primary } } }
    - id: btn_d_label
      component: Text
      text: "Default"
    - id: btn_d
      component: Button
      variant: default
      child: btn_d_label
      action: { event: { name: kitchen_click, context: { which: default } } }
    - id: btn_b_label
      component: Text
      text: "Borderless"
    - id: btn_b
      component: Button
      variant: borderless
      child: btn_b_label
      action: { event: { name: kitchen_click, context: { which: borderless } } }
    - id: g_btn_row
      component: Row
      children: [btn_p, btn_d, btn_b]
    - id: g_btn
      component: Column
      children: [s_btn, g_btn_row]

    # ---- Card wrapping inner content ------------------------------------
    - id: s_card
      component: Text
      variant: h2
      text: "Card"
    - id: card_inner_title
      component: Text
      variant: h3
      text: "Card headline"
    - id: card_inner_body
      component: Text
      variant: body
      text: "basicCatalog Cards hold one child, so pack title + body into an inner Column."
    - id: card_inner
      component: Column
      children: [card_inner_title, card_inner_body]
    - id: card_one
      component: Card
      child: card_inner
    - id: g_card
      component: Column
      children: [s_card, card_one]

    # ---- Divider (horizontal) -------------------------------------------
    - id: s_div
      component: Text
      variant: h2
      text: "Divider"
    - id: div_h
      component: Divider
    - id: g_div
      component: Column
      children: [s_div, div_h]

    # ---- Image ----------------------------------------------------------
    - id: s_img
      component: Text
      variant: h2
      text: "Image"
    - id: img
      component: Image
      url: "https://picsum.photos/seed/a2ui/480/200"
    - id: g_img
      component: Column
      children: [s_img, img]

    # ---- TextField ------------------------------------------------------
    - id: s_tf
      component: Text
      variant: h2
      text: "TextField (two-way bound to /form/name)"
    - id: tf_name
      component: TextField
      label: "Your name"
      value: { path: "/form/name" }
    - id: tf_echo
      component: Text
      variant: caption
      text: { path: "/form/name" }
    - id: g_tf
      component: Column
      children: [s_tf, tf_name, tf_echo]

    # ---- CheckBox -------------------------------------------------------
    - id: s_cb
      component: Text
      variant: h2
      text: "CheckBox (bound to /form/subscribed)"
    - id: cb_sub
      component: CheckBox
      label: "Subscribe to updates"
      value: { path: "/form/subscribed" }
    - id: g_cb
      component: Column
      children: [s_cb, cb_sub]

    # ---- Slider ---------------------------------------------------------
    - id: s_sl
      component: Text
      variant: h2
      text: "Slider (bound to /form/volume)"
    - id: sl_vol
      component: Slider
      min: 0
      max: 100
      value: { path: "/form/volume" }
    - id: sl_echo
      component: Text
      variant: caption
      text: { path: "/form/volume" }
    - id: g_sl
      component: Column
      children: [s_sl, sl_vol, sl_echo]

    # ---- ChoicePicker ---------------------------------------------------
    - id: s_cp
      component: Text
      variant: h2
      text: "ChoicePicker (chips, mutually exclusive)"
    - id: cp
      component: ChoicePicker
      label: "Pick a flavor"
      displayStyle: chips
      variant: mutuallyExclusive
      options:
        - { value: "vanilla",    label: "Vanilla" }
        - { value: "chocolate",  label: "Chocolate" }
        - { value: "strawberry", label: "Strawberry" }
      value: { path: "/form/flavor" }
    - id: g_cp
      component: Column
      children: [s_cp, cp]

    # ---- Extension: OptionsGrid ----------------------------------------
    - id: s_og
      component: Text
      variant: h2
      text: "Extension · OptionsGrid (tap-to-fire)"
    - id: og
      component: OptionsGrid
      prompt: "Tap an option to fire an A2UI event:"
      options:
        - id: one
          label: "Option A"
          rationale: "Fires event `kitchen_option` with context.id = one."
          emoji: "🅰️"
          action: { event: { name: kitchen_option, context: { id: one } } }
        - id: two
          label: "Option B"
          rationale: "Fires the same event with id = two."
          emoji: "🅱️"
          action: { event: { name: kitchen_option, context: { id: two } } }
    - id: g_og
      component: Column
      children: [s_og, og]

    # ---- Extension: RichMessageCard ------------------------------------
    - id: s_rc
      component: Text
      variant: h2
      text: "Extension · RichMessageCard"
    - id: rc
      component: RichMessageCard
      recommendationType: strong
      confidence: high
      headline: "This is a strong take."
      rationale: "Two-sentence rationale that explains the take. Ships with confirm and dismiss actions wired up."
      confirmAction:
        label: "I'm in"
        event: { name: kitchen_confirm, context: {} }
      dismissAction:
        label: "Show alternatives"
        event: { name: kitchen_dismiss, context: {} }
    - id: g_rc
      component: Column
      children: [s_rc, rc]

    # ---- Back button ---------------------------------------------------
    - id: back_label
      component: Text
      text: "← Back to chat"
    - id: back
      component: Button
      variant: default
      child: back_label
      action: { event: { name: restart, context: {} } }

    # ---- Root layout ----------------------------------------------------
    - id: root
      component: Column
      children:
        - title
        - subtitle
        - divider_top
        - g_text
        - g_btn
        - g_card
        - g_div
        - g_img
        - g_tf
        - g_cb
        - g_sl
        - g_cp
        - g_og
        - g_rc
        - back
---

# Kitchen sink skill

Static surface. Renders every component in the starter catalog so you can
eyeball that the renderer picks them all up and that our extensions
(OptionsGrid, RichMessageCard) register alongside the basicCatalog primitives.

No LLM call. Accessed via the "Kitchen sink" button in the header.
