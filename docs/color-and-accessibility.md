# Color and accessibility

**Status:** proposed palette. Measurements below are computed from the specified sRGB colors, at full opacity. They are reproduction guidance, not a claim that an entire product is accessible.

## Palette

| Name | Hex | RGB | Role |
| --- | --- | --- | --- |
| Decision Ink | `#182B33` | 24, 43, 51 | Primary text, signature, major dark field, primary action |
| Paper | `#F5F4EF` | 245, 244, 239 | Primary editorial and document surface |
| Mist | `#E4ECEA` | 228, 236, 234 | Secondary field, image surround, considered contrast |
| Field Green | `#52766D` | 82, 118, 109 | Secondary field and limited supporting text |
| Signal Orange | `#D54B1E` | 213, 75, 30 | Signature point and sparse large editorial punctuation |
| White | `#FFFFFF` | 255, 255, 255 | Uncoated output approximation, neutral screens, reverse text |

The warm paper/mineral-green environment belongs to DecisionInvitation. Orange is the exact family accent. Color alone must never indicate whose response is visible, whether a response was recorded, or whether a decision is complete.

## Measured pairings

The same ratio applies in either foreground/background direction. “Large text” means at least 24 CSS px regular or approximately 18.67 CSS px bold. Use the actual rendered size and weight when assessing it.

| Pair | Contrast | Normal text | Large text / essential graphic |
| --- | ---: | --- | --- |
| Ink / White | 14.66:1 | Yes | Yes |
| Ink / Paper | 13.31:1 | Yes | Yes |
| Ink / Mist | 12.21:1 | Yes | Yes |
| Green / White | 5.03:1 | Yes | Yes |
| Green / Paper | 4.57:1 | Yes, full opacity only | Yes |
| Green / Mist | 4.19:1 | No | Yes |
| Orange / White | 4.33:1 | No | Yes |
| Orange / Paper | 3.93:1 | No | Yes |
| Orange / Mist | 3.60:1 | No | Yes |
| Orange / Ink | 3.39:1 | No | Yes |
| Green / Ink | 2.91:1 | No | No |

## Applying the palette

Use Ink for routine text on a light surface. Green supporting text is permitted on White or Paper at full opacity; do not fade it or put it on Mist. Use Paper or White text on Ink. Use White text on Green when normal-size copy is needed.

Signal Orange cannot be a normal-size text color on the proposed fields. A standard button with orange fill and a small white label also fails the 4.5:1 target. The primary action is therefore Ink with Paper text. Orange can remain in the logo, a large headline word that meets the large-text threshold, or a structural accent that does not carry the sole meaning.

Do not darken or tint the logo dot to fix a surrounding interface. Choose a documented one-color signature or change its background. Functional color additions require semantic naming and an accessibility check; they do not expand the corporate palette by accident.

## Status and focus

“Recorded,” “Needs attention,” and “Closed” require text or a recognizable symbol with an accessible label. Success does not default to Field Green, and Orange does not automatically mean an error. The orange signature point never pulses to signal activity.

On light backgrounds, Ink is the dependable focus outline. On Ink, use Paper. A two-layer outline can survive mixed surfaces. Essential component edges need at least 3:1 against the adjacent field; decorative rules can be lighter only when they carry no necessary boundary or state.

Keep body text at least 16 CSS px on the web, 18 px where room allows. Reflow at narrow viewports and 200% zoom. Maintain visible keyboard focus, real labels, descriptive link text, error messages tied to fields, and motion-independent state. Touch targets should be at least 44 by 44 CSS px in the product's own design guidance; do not equate that single rule with full conformance.

## Print and material reproduction

Hex is the sRGB master, not a universal print recipe. Convert through the printer's specified output profile and proof on the actual stock. Do not publish unverified Pantone numbers or treat an arithmetic CMYK conversion as a press match. On uncoated paper, protect the negative space in the monogram and evaluate dot spread at final size.

One-color Ink or black is the first option for low-cost forms, stamps, embossing, and office printing. Use the one-color master instead of relying on uncontrolled grayscale conversion.

## Verification method

The measurements use relative sRGB luminance: linearize each channel; combine with coefficients 0.2126, 0.7152, and 0.0722; compute `(lighter + 0.05) / (darker + 0.05)`. Round for display only. A result printed as 4.50 must be assessed from the unrounded value. Recompute after any token, opacity, image, or background change.
