# Signature system

Status: visual proposal, pending owner review. Measurements below describe the supplied 0.2.0 masters; they are not permission to redraw them.

## One name, a compact sign

The wordmark is `DecisionInvitation`, with both capital letters intact. The bespoke `Di` is an identifying sign, not an abbreviation for running copy. Use the full lockup at the first point of contact. Use the mark alone where the name is already visible, in an app icon, or within a clearly identified profile.

The open D gives the product its own shape and suggests a held question with a way forward. The orange point completes the i. It is a small aSUKIra family trace, not a status light or a Suki symbol. The dot belongs to the supplied monogram; do not color every i in prose or the outlined wordmark.

## Master construction

Canonical geometry lives in `assets/source/identity.json`. Master SVGs are in `production/01-logo/svg/` and contain outlined wordmarks, not live font dependencies.

| Property | Master specification |
| --- | --- |
| Coordinate field | 256 × 256 units |
| D extent | x 24–178; y 40–224 |
| Main D wall | nominal 34 units; optically shaped curve |
| Left aperture | y 113–147, 34 units high |
| i stem | x 198–230; y 110–224 |
| i point | center 214, 69; radius 18 |
| Clear-space unit x | 36 units, the point's diameter |
| Main master minimum | 24 CSS pixels high or 8 mm square field |
| Micro master minimum | 16 CSS pixels high; digital-only |

The micro master closes the D's left aperture and strengthens the i stem to preserve reading. Prefer it for 16–32 CSS pixel fields and test favicon exports at their actual display size. Do not substitute a scaled-down main master at 16 pixels. The open master is permitted from 24 pixels where inspection confirms its aperture remains clear; above 32 pixels it is the default. Size is measured on the square viewBox, not just the visible shape.

Maintain x of clear space beyond the **visible artwork bounds** on each side. This is an exclusion area: no text, photograph edge, border, badge, or other logo. A supplied SVG viewBox may include internal padding; add whatever external margin is needed to reach the full clear space. For lockups, x is the dot diameter at the lockup's actual scale. For a wordmark-only asset, x is one half of its outlined capital D height. App-icon masks are the deliberate exception: use the supplied icon composition and its safe area.

## Responsive use

| Context | Asset | Working minimum |
| --- | --- | --- |
| First-contact website navigation | `di-lockup-primary.svg` | 180 px wide, inspect full-name legibility |
| Narrow signed-in header with adjacent product name | `di-mark-primary.svg` | 24 px square field |
| Small browser tab | `di-micro-primary.svg` / favicon export | 16 px square field |
| Print horizontal signature | `di-lockup-ink.svg` | 48 mm wide, physical proof required |
| Print mark only | `di-mark-ink.svg` | 8 mm square field |
| Editorial name with mark elsewhere | `di-wordmark-ink.svg` | 140 px / 38 mm wide |
| Square title sheet | `di-stacked-primary.svg` | 120 px / 32 mm wide |

The lockup and print working minima are proposed operational guardrails, not measured universal reproduction guarantees. If the substrate or display cannot hold the name or aperture, enlarge the asset. Do not reduce below these values to solve a layout problem.

## Color versions

- **Primary:** Ink body and Orange point on Paper, White, or Mist.
- **Reverse:** Paper body and Orange point on Ink.
- **Ink:** all-Ink, including point, for single-color reproduction.
- **White:** all-White, including point, on a sufficiently dark background.

Use the matching `primary`, `reverse`, `ink`, or `white` file for mark, micro, wordmark, lockup, and stacked formats. The wordmark has no isolated orange glyph. Orange carries no information by itself; the all-one-color versions remain the same brand.

## Background and misuse

Prefer a flat quiet field. On photography, place the signature on an opaque Paper or Ink panel with full clear space. Do not place it over faces, fine texture, or a fluctuating video frame. No gradients, shadows, outlines, rotation, stretching, component rearrangement, parent-logo fusion, orange body, replacement dot, decorative duplication, or glyph substitution. Do not animate the point to communicate AI activity, urgency, unread status, or consent.

Use SVG for browser and vector-capable design tools; PNG for systems that do not preserve SVG. A white background is not part of a transparent PNG unless the application master explicitly includes it. Do not reuse a contact-sheet tile as a logo file. Describe linked logos with `DecisionInvitation`; decorative repetitions use empty alternative text.
