# Typeface provenance

Source Sans 3 Regular and Semibold are original Adobe **3.052R** static releases in TTF and WOFF2. IBM Plex Mono Regular is supplied unchanged from IBM's repository at commit `bf260093582f04622aacc1e9f9ca604d7ccd0c42`. Exact source URLs and SHA-256 hashes are recorded in [provenance.json](provenance.json). The optional `SourceSans3.ttf` variable reference is Adobe's original `SourceSans3VF-Upright.ttf` from the same release, with unchanged binary content; it is not used to produce the distributed static faces.

The build verifies the supplied files. It does not rename, subset, convert, or generate fonts. Source Sans webfont filenames omit Adobe's redundant `.ttf` segment for convenient CSS references; the binary content and embedded font names are unchanged.

Both families retain their original SIL Open Font License 1.1 notices in this directory. The Reserved Font Names are **Source** and **Plex** respectively. Font licensing is independent of the DecisionInvitation trademark and artwork-use rules. Do not distribute modified fonts under these reserved names without the copyright holder's permission.

The manual uses static faces with distinct PostScript names to preserve real Regular and Semibold weights in PDF output. Web pages serve the bundled original WOFF2 files locally without a third-party font request.
