# DecisionInvitation release kits

**0.3.1 · Multipath D identity proposal, pending owner review.** These kits distribute exact, usable files; they do not establish owner approval, trademark clearance, print approval, deployment, or downstream adoption.

## Choose a kit

| Filename | Intended use |
| --- | --- |
| `decisioninvitation-brand-0.3.1.zip` | Complete public identity: standards, manual, fonts/notices, production assets, editable applications, source, tools, tests, and public page source |
| `decisioninvitation-logos-0.3.1.zip` | Five Multipath D forms in four modes: outlined SVG, transparent PNG, and vector PDF; logo/color standards and asset terms |
| `decisioninvitation-templates-0.3.1.zip` | Editable HTML/CSS applications and briefs with referenced logos, tokens, licensed fonts, and channel guidance |
| `decisioninvitation-webfonts-0.3.1.zip` | Supplied Sora Regular and SemiBold files, original OFL notice, typography guidance |

Extract into a new folder and preserve the hierarchy. Paths start at the repository root (`assets/`, `production/`, `templates/`, etc.); there is no additional enclosing directory. Open `templates/applications/index.html` for the application gallery. The small kits intentionally contain only their relevant resources; the full README and complete manual are in the complete identity kit.

## Inventory and integrity

`manifest.json` lists every public payload file's repository-relative path, role, byte count, and SHA-256 hash. PNG/ICO records include pixel dimensions and whether actual transparent pixels exist; SVG dimensions are viewBox units. The `kits` object identifies the subset carried by each archive.

Each ZIP embeds the same `releases/manifest.json`. An extracted small kit does not contain every file in the global inventory: use its `kits.<kind>.files` membership list. File-level hashes cover payload files; the manifest cannot include its own hash without a circular dependency.

`checksums.json`, distributed beside the archives, records the exact byte count and SHA-256 of all four ZIPs and the manifest. It is deliberately not embedded in the ZIPs, because an archive cannot contain its own final checksum. Checksums detect byte changes; they are not a cryptographic signature or evidence of legal approval.

From a complete source checkout with Python dependencies installed:

```sh
.venv/bin/python tools/validate.py
```

The validator compares the current canonical files, manifest metadata, kit memberships, embedded payloads, ZIP CRCs, stable timestamps, and archive hashes. It fails when a distributed source file changes after packaging. To compare a downloaded archive manually, calculate its SHA-256 and compare the corresponding entry in `checksums.json` obtained from the intended release source.

## Rebuild contract

Build the production assets and manual first, then run `tools/package_release.py` from the complete source tree. A missing manual, standards index, font license, dependency lockfile, or logo export family refuses packaging. The packager uses fixed ZIP timestamps, sorted paths, fixed file permissions, and deterministic compression for unchanged inputs. Re-run after the final public-source edit.

The complete kit excludes private operational ledgers, review/screenshots, rendered PDF page proofs, generated `site/brand-assets`, dependencies and caches, retired material, and all nested ZIP archives. The reusable blank adoption register remains public. The static identity overview is intentional artwork, not a browser proof.

Use [asset usage terms](../ASSET-LICENSE.md) and retain the font notices. The brand page and release owner must report local verification, visual review, owner approval, repository publication, host acceptance, live routes/downloads, and consumer adoption as separate gates.
