# Docs site (MkDocs + GitHub Pages)

This vault is published as a read-only website so people without Obsidian
can browse the requirements, scope, backlog, specs, and traceability matrix.

## How it works

1. `scripts/build_docs_site.py` copies the vault's markdown into
   `docs_build/` (git-ignored, rebuilt every run), skipping pipeline
   internals (`00-pipeline-skills/`, `scripts/`, `github-sync/`, `.obsidian/`,
   `README.md`, `README-vault-qa.md`, `CLAUDE.md`).
2. While copying, it converts Obsidian `[[wikilinks]]` into plain relative
   Markdown links, since MkDocs doesn't understand wikilink syntax natively.
   The original `.md` files are never modified — Obsidian and the pipeline
   skills keep working exactly as before.
3. `mkdocs build` (configured by `mkdocs.yml` at the repo root) turns
   `docs_build/` into a static site using the Material theme.
4. The `awesome-pages` plugin reads `nav-root.pages` / `nav-speckit-specs.pages`
   (copied into `docs_build/.pages` and `docs_build/04-speckit-specs/.pages`)
   to order the navigation. New files the pipeline creates (new versions,
   new specs) show up automatically via the `...` catch-all entry — nothing
   here needs to be touched when the pipeline runs.
5. `.github/workflows/deploy-docs.yml` runs this on every push to `main`
   and publishes the result to GitHub Pages.

## One-time setup (do this once, in the GitHub repo settings)

Settings → Pages → Source: **GitHub Actions**.

Without this, the workflow will build the site but GitHub won't serve it.

## Running it locally

```bash
pip install mkdocs mkdocs-material mkdocs-awesome-pages-plugin
python scripts/build_docs_site.py
mkdocs serve
```

Then open http://127.0.0.1:8000.

## If a wikilink doesn't resolve

The build script prints a warning (file + broken link) instead of failing
the build. The unresolved link renders as bold plain text on the site
instead of a link. Check the Action logs, or the terminal output when
running locally, for the list.
