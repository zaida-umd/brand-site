# Claude Code — Brand Site Design

This is the **Brand Site design project**. It builds on the design-system
page builder, vendored as a submodule at `page-builder/`.

`page-builder/CLAUDE.md` defines the canonical rules — **read it first**. This
file layers brand-site-specific guidance on top and does not repeat it.

## Where to find things

| What | Location |
|---|---|
| Slash commands | `page-builder/.claude/commands/*.md` |
| Layout/spacing/component rules | `page-builder/RULES.md` |
| Component slots & attributes | `page-builder/registry/` |
| Critical CSS (canonical) | `page-builder/styles/critical.css` |
| Skeleton + inlined CSS | `page-builder/TEMPLATE.html` |
| Layout HTML patterns | `page-builder/LAYOUT-PATTERNS.md` |
| Generic page-builder overrides | `page-builder/OVERRIDES.md` |
| **Brand Site-specific overrides** | `OVERRIDES.md` (this repo) |

**Registry first**: before hand-rolling any element, search
`page-builder/registry/` for an existing `umd-element-*` component.

## Class namespace

House classes are `umd-brand-site-<component>[-<part>]`, written in full
words (`page-builder/RULES.md` §40). If the live site already uses its own
`umd-<name>-` prefix, use that name instead and change it here. Check a page with:

```bash
python3 page-builder/tools/check-class-names.py --namespace brand-site pages/**/*.html
```

## Scope: one page on a live site

brand.umd.edu is complete and already on the design system. This project
builds only new pages for it — currently `pages/trademarks-licensing/vendor-search.html`.
So in `shared/header.html` every nav link points to the **live** brand.umd.edu
URL, except pages this project builds, which use `{{ROOT}}`. Drawer refs still
use the live section slugs (`trademarks-licensing`, …) as directory names, so a
page added under any of them gets its drawer state automatically.

The chrome mirrors the live site: the full-color logo, no CTA, no utility row,
`search-url="https://search.umd.edu"`, and a simple footer for the Office of
Marketing and Communications. Visual tone is **restrained**: interior pages on
the live site are hero-minimal with accordions, tabs and cards.

`pages/index.html` is a scaffold placeholder. The real home page is the live site.

## Output paths

Pages are organised by site section, one directory per section, with the
section's landing page as `index.html` so `/pages/<section>/` serves it:

```
pages/
├── index.html                  site home (stays at the top)
└── <section>/
    ├── index.html              section landing
    └── <page-name>.html
```

- New pages → `pages/<section>/<page-name>.html`; a new section starts with its own `index.html`
- New images → `images/<section>/`, or `images/<page>/` for one page's assets
- Briefs / source notes → `briefs/<page-name>.md`

Do **not** write to `test/`, `qa/`, or `examples/`. Test and QA fixtures live in
the page-builder repo; demo and example pages live in the separate
`page-builder-examples` repo. Neither belongs here.

### Depth: never hard-code `../`

Pages sit at two different depths (`pages/index.html` vs
`pages/<section>/<page>.html`), so a fixed `../` prefix is wrong on half of
them. Anything shared across pages — `shared/header.html`, `shared/footer.html`,
and the image paths in any `briefs/*-data.json` — writes its paths
**repo-root-relative behind a `{{ROOT}}` token**:

```html
<img src="{{ROOT}}images/logos/brand-site-logo.svg" />
<a href="{{ROOT}}pages/<section>/">Section</a>
```

`page-builder/tools/chrome.py` expands `{{ROOT}}` to the right number of `../`
for the page being written. A page that moves between directories is then a
path change and nothing else.

Inside a single page's own body, ordinary relative paths are fine — they just
have to match that page's depth.

## Shared chrome — never copy it between pages

Every page in this project must use the **same** header, navigation, logo, and
footer. Pages should read as one coherent site, not invent their own chrome.

| File | What it holds |
|---|---|
| `shared/head-meta.html` | Site-wide `<head>` meta — ships a `noindex, nofollow` pair; delete it when the site goes live |
| `shared/header.html` | Header stack with this project's nav items and logo |
| `shared/footer.html` | Footer |
| `shared/chrome.css` | CSS companions the chrome markup depends on — create only if needed |
| `shared/page-scripts.html` | End-of-body `<script src>` tags every page loads |
| `shared/chrome-scripts.html` | Chrome-driven shadow injections |
| `shared/gate.html` | Access gate — blanks every page until a reviewer signs in |

Shared scripts are **never** pasted inline and their paths are **never**
hand-written: `shared/page-scripts.html` references them as
`{{ROOT}}page-builder/scripts/<name>.js` so the depth resolves per page.
`TEMPLATE.html`'s own `../scripts/...` path is correct only inside the
page-builder repo and 404s from a project.

**Edit `shared/`, then run the inliner:**

```bash
python3 page-builder/tools/build-chrome.py          # splices shared/ into every page under pages/
python3 page-builder/tools/build-chrome.py --check  # exits non-zero if any page is stale
```

Never hand-edit the chrome inside a `pages/*.html` file — it sits between
`SHARED:<key>:START` / `:END` markers and the next build overwrites it.

The CSS and scripts travel **with** the markup for a reason: a page assembled
from a sibling's chrome markup plus `TEMPLATE.html`'s `<head>` silently loses
the CSS companions — no console error, no broken layout, just unstyled chrome.

### The access gate

`shared/gate.html` keeps this prototype blank for anyone without the shared
credentials. It is not what keeps the site out of search results — that is the
`noindex` pair in `shared/head-meta.html`, and the two travel together. The gate
ships **enabled with no accounts**, so the site is locked until someone adds
one:

```bash
python3 page-builder/tools/gate.py --write shared/gate.html   # prompts, no echo
python3 page-builder/tools/build-chrome.py
```

`gate.py --list` shows the usernames; `--remove <username>` drops one. Never
type a password into `shared/gate.html` by hand — the file stores a
PBKDF2-SHA256 hash and the plaintext should exist only in a password manager.
To make this project public instead, delete `shared/gate.html` and re-run the
inliner; the region is stripped from every page.

**It is not access control.** The check runs in the browser, so every page's
markup is retrievable with `curl` by anyone holding the URL. Keep this repo
**private**, and put nothing behind the gate that would matter if it leaked.
`page-builder/scripts/gate.js` explains the boundary in full.

### The drawer's refs are directory names

`data-child-ref` / `data-parent-ref` values in the mobile drawer are the section
**directory names** under `pages/`. The inliner stamps `data-active` and
`data-selected` per page by matching those against the page's own path — rename
a directory and its drawer ref has to follow.

## Image paths

- **Brand Site-owned** (logos, project photography): `{{ROOT}}images/...`
- **Shared fallback library** (campus, people, events, default):
  `{{ROOT}}page-builder/images/large/...`, `{{ROOT}}page-builder/images/small/...`

When `images-index.json` is needed, read `page-builder/images/images-index.json`.

Never add project photography to the page-builder submodule — it holds only the
shared fallback library. Project images belong in this repo's `images/`.

## Overrides

Project-specific shadow injections and CSS overrides go in this repo's
`OVERRIDES.md`, never into the `page-builder/` submodule. The submodule is
shared with every other project; a brand-site-specific tweak committed
there breaks that boundary.

Chrome-driven injections belong in `shared/chrome-scripts.html`. Injections
driven by **page content** stay in the page that needs them and are logged in
`OVERRIDES.md`.

## Updating the page-builder pin

```bash
cd page-builder && git pull origin main && cd ..
python3 page-builder/tools/build-chrome.py --check   # confirm nothing drifted
git add page-builder && git commit -m "Bump page-builder submodule"
```

A submodule bump can move `critical.css`, the registry, or the stylesheet pin —
re-run any pages' checks after bumping, and QA anything using
`umd-element-carousel-*` (see `page-builder/CLAUDE.md`).
