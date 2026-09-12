# DecisionInvitation Corporate Identity

The source of truth for the DecisionInvitation identity: strategy, standards, production artwork, editable applications, public brand-center source, validation, and deterministic release kits.

## The idea

**Catalyst of analysis.** DecisionInvitation turns considered input into a clear next move without manufacturing consensus or taking responsibility from the decision owner.

The visual system is a **Decision Instrument**. Its Multipath D mark, Sora typography, cool instrument palette, ruled lanes, and hard thresholds stand apart from aSUKIra. A tiny Suki Orange dot over the lowercase i is a provenance signal only.

## Start here

- `output/pdf/decisioninvitation-identity-manual.pdf` — 16-page executive identity manual
- `docs/README.md` — complete standards index
- `production/01-logo/` — outlined SVG, transparent PNG, and PDF masters
- `templates/applications/` — editable communication specimens
- `site/` — `/brand` page source
- `releases/` — checksummed public kits

## Status

Version 0.3.1 is a design proposal pending owner review. Local validation proves file integrity, not trademark clearance, owner approval, production print quality, deployment, or live-route acceptance.

## Rebuild

```sh
npm run build
.venv/bin/python tools/build_manual.py
npm run release
npm test
npm run validate
```
