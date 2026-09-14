# Governance, release, and adoption

## Authority and status

The brand owner approves the identity. A brand steward maintains the source system. Product, security/privacy, and legal reviewers validate claims in their scopes. These are roles to assign, not people or approvals invented by this repository.

The release is `0.4.0-proposal`: the user's strategic idea is explicit, while the Decision Instrument identity, Multipath D mark, layout, applications, and neuroinclusive design position await final review. Exported does not mean approved. Publicly reachable does not mean approved. Asset counts do not establish quality.

## Decision rights

| Change | Minimum review |
| --- | --- |
| Spelling, broken link, descriptive accessibility fix | Steward; product review if meaning changes |
| New composition using established assets | Steward + channel owner |
| New campaign or new product claim | Brand owner + product/claim owner |
| Palette, type, mark, name, architecture, primary idea | Brand owner; record a decision and affected consumers |
| Privacy/access/security/legal/certification wording | Relevant accountable reviewer and current evidence |
| Co-branding or endorsement | Brand owner + permission holder |

## Source-to-release workflow

1. **Brief.** Identify audience, action, channel, constraints, evidence, owner, and status. Use `templates/briefs/`.
2. **Design.** Edit canonical sources, not exported files. Keep rationale and rejected alternatives concise. Check that the product is distinct with the orange removed.
3. **Synchronize.** Update docs, `brand-system.json`, tokens, affected generators/assets, and `CHANGELOG.md`. Record significant decisions in `docs/decisions/`.
4. **Build.** Run `python3 tools/build.py`, `python3 tools/build_manual.py`, and `python3 tools/build_case_study.py` with the repository's configured dependencies; the local `.venv/bin/python` may be used. Do not treat generation as approval.
5. **Validate.** Run `python3 tools/validate.py`. Inspect logo at actual small sizes, desktop/narrow public page, print/export samples, PDF pages, contrast, links, and font fallback. Keep screenshots as evidence, not source.
6. **Review.** Resolve intentional choices separately from defects. Obtain the required approvals. Do not rename status to approved without an explicit owner decision.
7. **Package.** Include version, status, source/license references, standards, consumer assets, checksums/manifest when generated, and release notes. Keep private evidence and historical rejects out of public downloads.
8. **Deliver and adopt.** Record repository publication, public route, downstream consumer updates, and live acceptance as separate gates in a private ledger based on `docs/adoption-register-template.md`. The public template contains no completion evidence; do not publish the completed operational ledger by default.

## Version policy

Major: identity-level incompatibility such as mark, name, or architecture. Minor: compatible additions such as a new application family. Patch: correction preserving intent. During proposals, retain an explicit proposal status even as version numbers advance. Never silently replace an already approved release; supersede it with a version and migration note.

## Acceptance rubric

- **Distinctive:** full product recognition without a parent badge; no borrowed Suki UI shorthand.
- **Meaningful:** structure creates a next move, without suggesting speed or coercion.
- **Coherent:** assets, page, document, tokens, and copy express the same hierarchy.
- **Reproducible:** clean generation uses sources and included licensed fonts; no manual tracing or hidden font dependency.
- **Usable:** minimum sizes, contrast, real viewport crops, fallback, keyboard and reduced motion hold.
- **Truthful:** claims and action states match evidence; fictional specimens are obvious.
- **Governed:** owner review status, limitations, version, provenance, and adoption gates are visible.

## Exceptions and retirement

An exception records the rule, business reason, affected surface, approving role, expiry, and return path. “It looked better” does not authorize a new permanent logo. Remove expired exceptions from current templates. Keep retired assets in version history or a clearly labeled archive outside public downloads; do not leave alternate “final” folders competing with current masters.

## Handoff receipt

Report: version/status; changed files and artifacts; generation/validation commands and results; visual QA completed; licenses/provenance; known limits; owner decisions required; publication and live verification status. Never compress all of these into “done.” The next person should know exactly what they may use and what still needs a decision.
