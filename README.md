# Brand Site Design

Design work for the UMD Brand Site site — multiple pages sharing a common
header, footer, and design-system chrome.

## Layout

```
brand-site-design/
├── pages/              Page HTML, one directory per site section
├── shared/             Header, footer, <head> meta, and their CSS/script companions
├── images/             Project-owned logos and photography
├── briefs/             Page briefs / source notes
├── page-builder/       Submodule → design-system-page-builder
│                       Source for critical.css, registry, RULES.md,
│                       slash commands (.claude/commands/), the shared
│                       image library, and tools/build-chrome.py
├── CLAUDE.md           Project rules for Claude Code
└── OVERRIDES.md        Project-specific shadow injections and CSS overrides
```

## Setup

```bash
git clone --recurse-submodules git@github.com:zaida-umd/brand-site-design.git
cd brand-site-design
python3 -m http.server 4177    # then open http://localhost:4177/pages/
```

Already cloned without submodules:

```bash
git submodule update --init --recursive
```

## Shared chrome

The header, footer, and site-wide `<head>` meta live once, in `shared/`, and are
inlined into every page. Edit `shared/`, never the chrome inside a page, then
run:

```bash
python3 page-builder/tools/build-chrome.py
```

`--check` exits non-zero if any page is stale, which makes it usable in CI.

## Image paths

- **Project-owned**: `{{ROOT}}images/logos/`, `{{ROOT}}images/<section>/`
- **Shared library** (campus, people, events): `{{ROOT}}page-builder/images/large/...`

`{{ROOT}}` is expanded to the correct number of `../` per page by the inliner —
see `CLAUDE.md` for why paths are never hard-coded.

## Working with this repo

Run Claude Code from the root of this repo; it reads `CLAUDE.md` here and the
canonical rules in `page-builder/CLAUDE.md`.

To update the page-builder pin:

```bash
cd page-builder && git pull origin main && cd ..
python3 page-builder/tools/build-chrome.py --check
git add page-builder && git commit -m "Bump page-builder submodule"
```

## Pages

<!-- List pages here as they are built. -->
