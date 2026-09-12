# Application review proofs

Reviewed locally on 2026-09-12 for the 0.3.2 identity proposal. These 21 PNGs record source-layout review; they are not approved artwork, platform-ready social exports, delivered communications, or press proofs.

## Scope

- All eight HTML sources loaded in locally installed Chrome through Playwright, with the repository's bundled fonts and canonical logos.
- Desktop viewport: 1440 × 1200 CSS px, device scale factor 1. Every card, document page, slide, product moment, and social artboard was captured and visually inspected. The application index and signature page were reviewed as full-page captures.
- Narrow viewport: 390 × 844 CSS px. All eight pages were checked for page-level horizontal overflow, broken images, and truncated preview or responsive-content containers. The index, product moments, and signature also have full-page narrow-screen proofs.
- Print-media emulation: card, letterhead, brief, presentation, product moments, and social files were checked for the intended named page and dimensions, hidden review chrome/guides, and artboard overflow. This is a computed-layout check, not a PDF pagination or physical printer test.

## Observed result

- No browser JavaScript errors or missing images in the eight source pages.
- Main and utility fonts loaded; semibold loaded in the templates that use it.
- No artboard content overflow in the supplied specimens. Fixed-size artwork remains at its native dimensions; keyboard-focusable horizontal preview regions make it accessible on narrow screens.
- No page-level horizontal overflow at 390 px. Responsive product specimens, preview copy, and signature content remained in bounds.
- Card canvases measured 360 × 216 CSS px, corresponding to 3.75 × 2.25 in including bleed at 96 CSS px/in. The finished trim is 3.5 × 2 in.
- A4 pages measured approximately 793.69 × 1122.52 CSS px; presentation masters measured 1280 × 720 px. Social artboards measured 1080 × 1080, 1200 × 630, and 1080 × 1350 px.
- Dense brief and presentation interiors were inspected for footer collisions, cramped hierarchy, clipped text, and unusable reference space. No collision was observed with the supplied content.

## File conventions

`business-card-1.png` is the front and `-2` the contact side. `decision-brief-1.png` is the cover and `-2` the interior. The four presentation images follow cover, section, content, and closing order. Product moments follow invitation, receipt, deadline, and owner brief order. Social images follow square, wide, and portrait order. Files ending in `-mobile.png` show the narrow viewport.

Dashed trim/safe-area guides in screen proofs are intentional review aids. Hide them for final artboard exports. Full-page images include preview notes that do not belong in printed artwork or an email signature.

## Remaining production gates

Replace all bracketed fields, recheck long real-world copy, and regenerate proofs after any source or canonical asset change. Validate actual exported page dimensions and pagination separately. No PDF was generated in this task. Physical stock, color conversion, bleed/trim boxes, duplex orientation, and press approval require supplier preflight and physical proof. The signature still requires an approved hosted HTTPS image and testing in the intended email clients. Social destination dimensions/overlays require a fresh destination-specific check before upload. No messages were sent and no product workflow was activated by these fixtures.
