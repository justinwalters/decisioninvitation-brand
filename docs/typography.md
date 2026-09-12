# Typography

**Status:** proposed roles using typefaces already present in the parent inventory. No new font family is introduced.

## Typeface inventory

| Role | Face | Weight | Fallback |
| --- | --- | --- | --- |
| Large statement | Source Sans 3 | 400 | Arial, sans-serif |
| Heading and title | Source Sans 3 | 600 | Arial, sans-serif |
| Body and interface | Source Sans 3 | 400; 600 for emphasis and controls | Arial, sans-serif |
| Utility, date, identifier | IBM Plex Mono | 400 | ui-monospace, SFMono-Regular, Menlo, monospace |
| Native or unsupported channel | System UI or Arial | Platform-appropriate | sans-serif |

Source Sans 3 is promoted from the parent's reading role to the full DecisionInvitation voice. Its open forms and lighter large statements make the product feel distinct from Suki's Lexend display. IBM Plex Mono is a shared tool for precision, used sparingly.

## Scale

| Role | Desktop | Narrow screen | Leading | Notes |
| --- | ---: | ---: | ---: | --- |
| Hero | 88–120 px | 48–64 px | 0.96–1.04 | Weight 400; one primary statement |
| Section | 48–64 px | 32–40 px | 1.08 | Weight 400 or 600 according to density |
| Title | 28–36 px | 24–28 px | 1.15 | Weight 600 |
| Lead | 22–26 px | 20–22 px | 1.4 | Weight 400 |
| Body | 18–20 px | 16–18 px | 1.5–1.6 | Reading measure 55–75 characters |
| Control | 16–18 px | 16–18 px | 1.25 | Weight 600; never condensed to fit |
| Utility | 11–13 px | 12–13 px | 1.45 | IBM Plex Mono; short labels only |

These are design roles, not a requirement to shrink content to a size. Long headlines may need more lines. Use restrained negative tracking for large display, around -0.03em, and normal tracking for body copy. Metadata may use up to 0.06em. Never tightly track a small caption to imitate the logo.

## Typesetting the primary line

Preferred two-line setting:

> Catalyst of  
> analysis.

“Catalyst” and “analysis” should remain legible as ordinary words. A line break may change with format; do not alter the phrase. Set it in Source Sans 3 regular at generous scale. An orange point can finish the composition, but the headline does not need an orange character every time the mark already carries one.

The supporting line “Ask separately. Decide clearly.” belongs at a smaller scale and should not compete with the primary brand idea.

## Name rendering

Use the vector signature in a masthead, identity lockup, or cover. Use ordinary `DecisionInvitation` text in a sentence. Do not construct the monogram from two typed letters or recolor all the i-dots in the product name. The engineered monogram is the primary orange-point treatment.

Accessible labels remain `DecisionInvitation`. Decorative vectors use no duplicate accessible name when adjacent text already provides it. Preserve searchable text in public pages and accessible text alternatives for outlined wordmarks.

## Font delivery

Use the packaged font files and their included license notices when the target supports embedding. Load only the roles and weights used by the page. Web fonts use `font-display: swap`; measure fallback and final line wrapping. Avoid remote font requests on private invitation pages unless the product's privacy and network policy allows them.

The repository's packaged font files are resources, not a new license grant. Preserve their original notices in redistributed packages. Use the supplied original upstream static font files; do not substitute regenerated or renamed instances without a separate provenance and license review. For documents sent outside the organization, embed the fonts when permitted or use the approved fallback. The wordmark's source geometry must not change when a recipient lacks the font.

## Accessibility checks

At 200% zoom, the title, nav, form labels, and metadata remain readable and no essential content is clipped. Do not use light gray text, all-caps paragraphs, italic instructions, or visual ordering that differs from reading order. Set dates and IDs in mono only where their aligned structure helps comprehension.
