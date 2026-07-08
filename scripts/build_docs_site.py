#!/usr/bin/env python3
"""
Stage vault markdown into docs_build/ for the MkDocs site, converting
Obsidian-style [[wikilinks]] into plain relative Markdown links.

The source .md files are never touched: Obsidian and the pipeline skills
need the [[wikilink]] syntax to keep working, so this script only writes
converted copies into docs_build/, which is git-ignored and rebuilt fresh
on every run (locally or in CI).

Usage (from repo root):
    python scripts/build_docs_site.py
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / "docs_build"

# Directories that are pipeline internals / tooling, not vault content.
EXCLUDE_DIRS = {
    ".git", ".github", ".obsidian", "00-pipeline-skills",
    "scripts", "github-sync", "docs-site", "docs_build", "site",
}
# Root-level files that aren't vault content meant for the published site.
# 00-how-to-use.md is about running/maintaining the Obsidian vault and the
# Claude pipeline itself, not about the project, so it's kept out of the
# public site (still in the repo for the team).
EXCLUDE_FILES = {
    "README.md", "README-vault-qa.md", "CLAUDE.md", "00-how-to-use.md",
    ".gitignore", ".DS_Store", "mkdocs.yml",
}

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

# MkDocs only generates a site root ("/") page from a file literally named
# index.md. 00-project-home.md is the vault's designated navigation hub
# (per CLAUDE.md), so it becomes the site's index.md at build time. Any
# wikilink pointing at "00-project-home" is aliased to resolve there too.
HOMEPAGE_SRC = Path("00-project-home.md")
HOMEPAGE_DST = Path("index.md")

# Where to send links that point at a real file which was deliberately kept
# off the published site (e.g. 00-how-to-use.md, 00-pipeline-skills/*),
# instead of leaving them as dead, unclickable text.
GITHUB_BLOB_BASE = "https://github.com/XploreBe/community-cpr-RequirementsVault/blob/main/"


def slugify(text: str) -> str:
    """Approximate the slug that python-markdown's toc extension generates
    for headings, so [[#Some Heading]] anchors resolve correctly."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


def collect_markdown_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*.md"):
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDE_DIRS for part in rel.parts[:-1]):
            continue
        if rel.name in EXCLUDE_FILES:
            continue
        files.append(rel)
    return files


def build_indexes(rel_paths: list[Path]):
    """Index files two ways, mirroring how Obsidian resolves [[links]]:
    by full relative path, and by bare basename (for links that don't
    include a folder prefix)."""
    path_index: dict[str, Path] = {}
    basename_index: dict[str, list[Path]] = {}
    for rel in rel_paths:
        effective = HOMEPAGE_DST if rel == HOMEPAGE_SRC else rel
        path_index[rel.with_suffix("").as_posix().lower()] = effective
        basename_index.setdefault(rel.stem.lower(), []).append(effective)
    return path_index, basename_index


def build_repo_wide_indexes():
    """Every markdown file in the repo (except .git), included or not.
    Used only as a fallback so links to intentionally-excluded files (e.g.
    00-how-to-use.md, 00-pipeline-skills/*) can point to GitHub instead of
    rendering as dead text."""
    path_index: dict[str, Path] = {}
    basename_index: dict[str, list[Path]] = {}
    for path in ROOT.rglob("*.md"):
        rel = path.relative_to(ROOT)
        if ".git" in rel.parts[:-1]:
            continue
        path_index[rel.with_suffix("").as_posix().lower()] = rel
        basename_index.setdefault(rel.stem.lower(), []).append(rel)
    return path_index, basename_index


def resolve_target(target, current_rel, path_index, basename_index, repo_path_index, repo_basename_index, warnings):
    target = target.strip().lstrip("/")
    if target.lower().endswith(".md"):
        target = target[:-3]
    key = target.lower()

    hit = path_index.get(key)
    if hit is None and "/" not in target:
        candidates = basename_index.get(key, [])
        if len(candidates) == 1:
            hit = candidates[0]
        elif len(candidates) > 1:
            same_dir = [c for c in candidates if c.parent == current_rel.parent]
            hit = same_dir[0] if same_dir else candidates[0]
            warnings.append(
                f"{current_rel}: ambiguous wikilink '[[{target}]]' matched "
                f"{len(candidates)} files, picked '{hit}'"
            )
    if hit is not None:
        start = current_rel.parent.as_posix()
        return os.path.relpath(hit.as_posix(), start).replace(os.sep, "/")

    # Not part of the published site, but does it exist in the repo at all
    # (e.g. 00-how-to-use.md, a pipeline-skills doc)? Link out to GitHub
    # instead of rendering dead, unclickable text.
    excluded_hit = repo_path_index.get(key)
    if excluded_hit is None and "/" not in target:
        candidates = repo_basename_index.get(key, [])
        excluded_hit = candidates[0] if candidates else None
    if excluded_hit is not None:
        warnings.append(
            f"{current_rel}: wikilink '[[{target}]]' points to a file excluded "
            f"from the site, linked out to GitHub instead"
        )
        return GITHUB_BLOB_BASE + excluded_hit.as_posix()

    warnings.append(f"{current_rel}: could not resolve wikilink '[[{target}]]'")
    return None


def convert_wikilinks(text, current_rel, path_index, basename_index, repo_path_index, repo_basename_index, warnings):
    def replace(match: re.Match) -> str:
        # Wikilinks inside Markdown tables often escape the alias pipe as
        # "\|" so it doesn't get parsed as a table cell separator. Unescape
        # it here so target/label splitting works the same either way.
        inner = match.group(1).replace("\\|", "|")
        target_part, _, label = inner.partition("|")
        target_part = target_part.strip()
        label = label.strip() or None

        if "#" in target_part:
            target, _, anchor = target_part.partition("#")
        else:
            target, anchor = target_part, None
        target = target.strip()
        anchor = anchor.strip() if anchor else None

        if not target and anchor:
            text_out = label or anchor
            return f"[{text_out}](#{slugify(anchor)})"

        href = resolve_target(
            target, current_rel, path_index, basename_index,
            repo_path_index, repo_basename_index, warnings,
        )
        text_out = label or target
        if href is None:
            return f"**{text_out}**"
        if anchor and not href.startswith("http"):
            href = f"{href}#{slugify(anchor)}"
        return f"[{text_out}]({href})"

    return WIKILINK_RE.sub(replace, text)


def main() -> None:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True)

    rel_paths = collect_markdown_files()
    path_index, basename_index = build_indexes(rel_paths)
    repo_path_index, repo_basename_index = build_repo_wide_indexes()
    warnings: list[str] = []

    for rel in rel_paths:
        effective = HOMEPAGE_DST if rel == HOMEPAGE_SRC else rel
        src = ROOT / rel
        dst = BUILD_DIR / effective
        dst.parent.mkdir(parents=True, exist_ok=True)
        content = src.read_text(encoding="utf-8")
        content = convert_wikilinks(
            content, effective, path_index, basename_index,
            repo_path_index, repo_basename_index, warnings,
        )
        dst.write_text(content, encoding="utf-8")

    nav_dir = ROOT / "docs-site"
    root_pages = nav_dir / "nav-root.pages"
    specs_pages = nav_dir / "nav-speckit-specs.pages"
    if root_pages.exists():
        shutil.copy(root_pages, BUILD_DIR / ".pages")
    specs_dir = BUILD_DIR / "04-speckit-specs"
    if specs_pages.exists() and specs_dir.exists():
        shutil.copy(specs_pages, specs_dir / ".pages")

    print(f"Staged {len(rel_paths)} markdown files into {BUILD_DIR.relative_to(ROOT)}/")
    if warnings:
        print(f"\n{len(warnings)} wikilink warning(s):")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("All wikilinks resolved cleanly.")


if __name__ == "__main__":
    main()
