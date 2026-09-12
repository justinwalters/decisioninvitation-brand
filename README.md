# DecisionInvitation — corporate identity

**Catalyst of analysis.**  
Ask separately. Decide clearly.

Version **0.2.0 · proposed visual identity, pending owner review**. The central idea is user-directed; the Open frame mark, visual system, and applications are proposed. This repository is the identity source, not the product runtime. It does not replace the existing product homepage or establish that a website is deployed.

DecisionInvitation is designed to stand independently within the aSUKIra family. A small Suki Orange signature supplies a quiet relationship cue. The identity does not claim an acquisition history, trademark clearance, certified security, anonymous responses, or automatic decision-making.

## Start with the right artifact

| Need | Start here |
| --- | --- |
| Understand the complete identity | [16-page identity manual](output/pdf/decisioninvitation-identity-manual.pdf) |
| Find a specific standard | [Detailed standards index](docs/README.md) |
| Use an original logo | [Outlined SVG masters](production/01-logo/svg/), [transparent PNGs](production/01-logo/png/), [vector PDFs](production/01-logo/pdf/) |
| Make a document or communication | [Editable application gallery](templates/applications/index.html) and [instructions](templates/applications/README.md) |
| Build a compatible interface | [Token JSON](assets/tokens/decisioninvitation.tokens.json), [CSS](assets/tokens/decisioninvitation.tokens.css), [website standards](docs/website-guidelines.md) |
| Publish the public identity page | [Page source and integration instructions](site/README.md) |
| Download or verify a release | [Kits and verification notes](releases/README.md), [inventory](releases/manifest.json), [archive checksums](releases/checksums.json) |
| Know what may be used | [Asset usage terms](ASSET-LICENSE.md) and the original [font license notices](assets/fonts/) |

## What the package contains

- **Strategy and stewardship:** positioning, architecture, voice, claims/privacy boundaries, channel rules, governance, decision record, contributor and AI handoff guidance, and reusable creative/release briefs.
- **Logo production:** five forms—symbol, micro symbol, wordmark, horizontal signature, stacked signature—in primary, reverse, Ink, and white. Twenty outlined SVGs, twenty vector PDFs, and forty transparent PNGs. SVG wordmarks do not depend on installed fonts.
- **Digital identity:** app/icon masters at 16, 32, 48, 180, 192, 512, and 1024 pixels; ICO favicon; light and dark avatars; social/share, square, portrait, story, header, and presentation artwork. These are aspect-ratio masters, not assertions of current platform upload limits.
- **Type and tokens:** Source Sans 3 Regular/Semibold and IBM Plex Mono Regular, local upstream WOFF2/TTF resources with original OFL notices and provenance records, and primitive → semantic → component tokens.
- **Editable HTML/CSS applications:** front/back business card with trim and bleed, A4 letterhead, two-page decision brief, four presentation layouts, email signature, four fictional product moments, and three social layout specifications. No PowerPoint or native Word files are implied.
- **Manual and public center:** a 16-page, searchable-text PDF manual; a responsive public page with logo variants, color copying, type specimen, resource filtering, and real versioned downloads.
- **Production infrastructure:** canonical geometry, generators, pinned dependencies, regression tests, a deterministic ZIP packager, file-level inventory, archive SHA-256 checksums, and local validation.

Review screenshots, local operational ledgers, dependencies/caches, and generated website mirrors are not part of public kits. The editable templates include fictional copy and clearly marked contact placeholders. Printed pieces are design proofs, not approved press files.

## Four release kits

| Kit | Contents |
| --- | --- |
| [Complete identity](releases/decisioninvitation-brand-0.2.0.zip) | Public standards, manual, editable applications, all production assets, licensed fonts, source, build tools, tests, and public-page source |
| [Logo production](releases/decisioninvitation-logos-0.2.0.zip) | SVG/PNG/PDF logo family, logo and color standards, usage terms |
| [Application templates](releases/decisioninvitation-templates-0.2.0.zip) | Editable HTML/CSS and briefs, referenced production logos, tokens, fonts and license notices, relevant channel standards |
| [Webfonts](releases/decisioninvitation-webfonts-0.2.0.zip) | Supplied WOFF2/TTF resources, font license notices and typography standard |

Every archive preserves repository-relative paths and embeds `releases/manifest.json`. Keep its folder hierarchy when opening templates so relative font and logo references work. The manifest carries file-level hashes and kit membership; the external `checksums.json` carries ZIP hashes. A checksum proves byte integrity, not approval or authorship.

## Build and verify

Use Python 3.11+ and a supported Node.js release (Node 22 is a suitable baseline). The supplied upstream fonts are local inputs. Installing build dependencies requires network access; asset generation itself does not fetch fonts or call external design services.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm ci
.venv/bin/python tools/build.py
.venv/bin/python tools/build_manual.py
.venv/bin/python tools/package_release.py
.venv/bin/python tools/validate.py
.venv/bin/python -m unittest discover -s tests -v
```

`tools/build.py` validates the supplied upstream fonts and produces vectors, rasters, icons, tokens, and logo PDFs. `tools/build_manual.py` produces the manual from local sources. The packager refuses a missing manual, standards index, font licenses, dependency lockfile, or SVG/PNG/PDF logo family. Run packaging **after the last edit** to any distributed source file; stale source hashes deliberately fail validation.

For fixed input files, ZIP ordering, permissions, timestamps, and compression are deterministic. Rebuilding assets on a different rendering stack is a separate reproducibility question; compare the resulting manifest rather than assuming cross-platform pixels are identical.

After packaging, prepare the local public mirror and validate its actual references:

```sh
.venv/bin/python tools/sync_site.py
.venv/bin/python tools/validate.py --public-mirror
.venv/bin/python -m http.server 3000 --bind 127.0.0.1 --directory site
```

Open `http://127.0.0.1:3000/`. This simple preview serves the brand source at `/`; it does not simulate the product's `/brand` routing. In another terminal, install a supported browser for the interaction test if needed, then run:

```sh
npx playwright install chromium
BRAND_URL=http://127.0.0.1:3000/ node --test tests/brand-page.test.cjs
```

`CHROMIUM_PATH` may point to an existing compatible Chromium executable. Browser interaction tests cover logo preview/download changes, filtering, live type, and narrow-screen overflow; they do not replace visual, keyboard, zoom, reduced-motion, assistive-technology, or print proof review.

## Source and approval boundaries

1. Explicit owner decisions establish direction and approval.
2. [brand-system.json](brand-system.json) maps the system; [identity.json](assets/source/identity.json) owns geometry, palette, and font roles.
3. Detailed standards explain use. Generators produce assets and tokens; do not hand-edit an export as a new master.
4. Release inventory and checksums record exact files. The public page and downstream product are consumers of this system.

Local generation, automated verification, visual review, owner approval, repository publication, host acceptance, live `/brand` and download checks, and product adoption are **separate gates**. See [governance](docs/governance-and-release.md) and the [blank adoption register](docs/adoption-register-template.md). A local pass or public download is not evidence that every gate passed. Real invitation routes and the original homepage remain outside this identity repository's authority.
