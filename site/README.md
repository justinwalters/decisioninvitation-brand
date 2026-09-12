# Public identity center source

This folder implements the intended **decisioninvitation.com/brand** center for identity version **0.3.0**, visibly labeled as a proposal pending owner review. Its existence does not establish deployment or final visual approval. This is a separate brand page; preserve the product's original homepage and real invitation routes.

## Files and behavior

| File | Responsibility |
| --- | --- |
| `index.html` | Semantic identity story, standards, specimens, applications, and download links |
| `brand.css` | Responsive layout, local font loading, print and reduced-motion treatment |
| `brand.js` | Logo variant selection/download target, color-copy feedback, editable type specimen, and resource filtering |
| `brand-assets/` | Generated public mirror; do not edit or include recursively in release archives |

The static HTML delivers the main content and download links without JavaScript. Optional controls enhance the experience. No third-party font request, analytics, or product participant data is required by the page source.

Sections cover the central idea; independent identity and subtle family relationship; logo and optical small-size rules; palette and contrast; typography; applications; voice and truthful privacy language; and versioned resources. The primary idea is **Catalyst of analysis.** The product language “Better input. Clearer decisions.” and “Ask separately. Decide clearly.” is preserved.

## Prepare the preview

From the repository root, install dependencies and build assets/manual using the [main instructions](../README.md). Package last so every download exists and the checksums represent the final source.

```sh
.venv/bin/python tools/package_release.py
.venv/bin/python tools/validate.py
.venv/bin/python tools/sync_site.py
.venv/bin/python tools/validate.py --public-mirror
.venv/bin/python -m http.server 3000 --bind 127.0.0.1 --directory site
```

Visit `http://127.0.0.1:3000/`. The simple preview serves this source at `/`; production must map it to `/brand`. Root-relative `/brand.css`, `/brand.js`, and `/brand-assets/…` paths intentionally survive the product route. The home links still point to the actual product root in deployment.

`sync_site.py` copies only public allowlisted resources. It excludes the operational adoption ledger, browser/review renders, and private evidence. The public blank register is a reusable template, not an internal release receipt. Releases never include this generated mirror or nested ZIPs.

## Integrate with the product

The product checkout, hostname, and hosting workflow are separate from this repository. Only after resolving the intended checkout, an authorized integration can run:

```sh
.venv/bin/python tools/sync_site.py --product /absolute/path/to/decisioninvitation-product
```

The tool requires the product's `PRODUCT.md` marker and copies this page to `brand.html`, plus `brand.css`, `brand.js`, and `brand-assets/`. It does not intentionally change the homepage or invitation handlers. Inspect the resulting product diff and its route configuration. This step prepares files; it does not upload, change DNS, or prove the host accepted them.

## Acceptance gates

- **Source:** version/palette consistency, outlined vectors, transparent logo PNGs, all local HTML/CSS asset references, and release integrity pass.
- **Browser:** check desktop and narrow widths, 200% zoom, keyboard focus, readable fallback fonts, motion reduction, meaningful alt text, and functioning logo/copy/type/filter controls. JavaScript failure must leave content and downloads usable.
- **Downloads:** open the manual, test all four ZIPs, compare hashes, preserve font licenses, and verify filenames on the deployed host—not only the source checkout.
- **Review:** retain visible proposal status until the owner approves the visual identity. Print, legal, and product claims reviews remain separate.
- **Publication:** repository push, host upload/acceptance, DNS/origin/SSL, `/brand` status/content, resource MIME types, mobile rendering, and the unchanged product homepage/invitation routes each need current evidence.

The automated browser test can target the local preview:

```sh
BRAND_URL=http://127.0.0.1:3000/ node --test tests/brand-page.test.cjs
```

Install Playwright Chromium first, or supply `CHROMIUM_PATH` for a compatible installed browser. Automated checks are not a substitute for the visual and live acceptance gates above.
