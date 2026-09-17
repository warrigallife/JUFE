
**Document ID:** JUFE-V3-EDITORIAL-README
**Version:** 0.1.0
Status: ACTIVE SPECIFICATION DRAFT

# JUFE Editorial Toolkit v0.1.0

This starter package provides the first report-only JUFE Markdown validator.

## Install

Copy `docs`, `tools`, and `.vscode` into the root of the JUFE repository. Keep the specification chapters inside a folder named `specification`.

## Run in VS Code Terminal

```bash
python3 tools/jufe_lint.py specification
```

The tool is read-only and does not modify any chapter.

## Run as a VS Code Task

Open **Terminal → Run Task → Run JUFE Validation**.

## First Review

Run it before editing. Save the first report, then review each reported rule against Chapter 1 before changing authoritative files.
