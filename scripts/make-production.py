#!/usr/bin/env python3
"""Turn the staging site into the production site.

Used by the "Publish to production" GitHub Actions workflow in the
taniarae-site repo. You can also run it locally to preview the result:

    python3 scripts/make-production.py <staging-folder> <production-folder>

What it does:
  1. Deletes the previously published site files from the production folder
     (it keeps .git, .github, CNAME and README.md).
  2. Copies the site files from staging (see SITE_FILES).
  3. Removes every <!-- STAGING-ONLY --> ... <!-- /STAGING-ONLY --> block
     (noindex tag, staging ribbon).
  4. Swaps the staging values from site.config.json for the production ones
     (site URL, Formspree form ID, email subject).
  5. Uses robots.production.txt as robots.txt and makes sure CNAME is right.
  6. Fails if anything staging-like is left over.

Python standard library only. No installs needed.
"""
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

# Files and folders that make up the public website.
# Docs (AGENTS.md, EDITING-GUIDE.md), scripts and config stay in staging.
SITE_FILES = [
    "index.html",
    "privacy.html",
    "404.html",
    "assets",
    "sitemap.xml",
    "llms.txt",
    "site.webmanifest",
    ".nojekyll",
]
KEEP_IN_PRODUCTION = {".git", ".github", "CNAME", "README.md"}
TEXT_SUFFIXES = {".html", ".xml", ".txt", ".webmanifest", ".json", ".css", ".js", ".md"}

STAGING_BLOCK = re.compile(r"[ \t]*<!-- STAGING-ONLY -->.*?<!-- /STAGING-ONLY -->[ \t]*\n?", re.S)

# Must never reach production. Publishing fails if any is found.
FORBIDDEN = ["[STAGING]", "noindex", "github.io", "STAGING-ONLY"]
FORBIDDEN_IN_HTML = ['class="staging-ribbon"']
# Setup placeholders: publishing fails until they are filled in everywhere.
# (Built from parts so a find-and-replace of the placeholders never edits this list.)
SETUP_PLACEHOLDERS = ["[" + name + "]" for name in (
    "GITHUB_USERNAME", "DOMAIN", "STAGING_FORM_ID",
    "PRODUCTION_FORM_ID", "INSTAGRAM_HANDLE", "CONTACT_EMAIL")]
# Content placeholders Tania still has to fill in: a warning only.
CONTENT_PLACEHOLDER = re.compile(r"\[[A-Z][A-Z0-9 ,.'’-]{2,}\]")


def fail(message):
    print(f"::error::{message}")
    sys.exit(1)


def text_files(root):
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.parts and path.suffix in TEXT_SUFFIXES:
            yield path


def main(src, dest):
    config = json.loads((src / "site.config.json").read_text(encoding="utf-8"))
    stg, prod = config["staging"], config["production"]

    # 1. Clean previously published files
    for item in dest.iterdir():
        if item.name in KEEP_IN_PRODUCTION:
            continue
        shutil.rmtree(item) if item.is_dir() else item.unlink()

    # 2. Copy the site
    for name in SITE_FILES:
        source = src / name
        if not source.exists():
            fail(f"Missing in staging: {name}")
        if source.is_dir():
            shutil.copytree(source, dest / name)
        else:
            shutil.copy2(source, dest / name)
    shutil.copy2(src / "robots.production.txt", dest / "robots.txt")

    # 3 + 4. Strip staging-only blocks and swap values
    swaps = [
        (stg["siteUrl"], prod["siteUrl"]),
        (f"formspree.io/f/{stg['formId']}", f"formspree.io/f/{prod['formId']}"),
        (stg["formSubject"], prod["formSubject"]),
    ]
    for path in text_files(dest):
        text = path.read_text(encoding="utf-8")
        new = STAGING_BLOCK.sub("", text)
        for old, value in swaps:
            new = new.replace(old, value)
        if new != text:
            path.write_text(new, encoding="utf-8")

    # 5. CNAME must hold the production domain
    domain = urlparse(prod["siteUrl"]).hostname or ""
    cname = dest / "CNAME"
    if not cname.exists() or cname.read_text().strip() != domain:
        cname.write_text(domain + "\n")
        print(f"CNAME set to {domain}")

    # 6. Checks
    problems, warnings = [], set()
    for path in list(text_files(dest)) + [cname]:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(dest)
        checks = FORBIDDEN + SETUP_PLACEHOLDERS + (FORBIDDEN_IN_HTML if path.suffix == ".html" else [])
        for bad in checks:
            if bad in text:
                problems.append(f"{rel}: contains {bad}")
        for match in CONTENT_PLACEHOLDER.findall(text):
            if match not in SETUP_PLACEHOLDERS:
                warnings.add(f"{rel}: {match}")
    for w in sorted(warnings):
        print(f"::warning::Placeholder still to fill in: {w}")
    if problems:
        for p in problems:
            print(f"::error::{p}")
        fail("Staging leftovers found. Nothing was published.")
    print("Production site ready.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
