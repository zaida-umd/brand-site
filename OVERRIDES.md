# Brand Site — Overrides

Project-specific deviations from the design system: shadow-DOM injections, CSS
overrides, and page-built classes that exist only in this repo.

**Append-only log, not a rule source.** The canonical rules are
`page-builder/RULES.md` and `page-builder/CLAUDE.md`. Generic page-builder
deviations belong in `page-builder/OVERRIDES.md`; anything here is
brand-site-specific by definition.

Never commit a brand-site-specific override into the `page-builder/`
submodule — it is shared with every other project.

## Where an override lives

| Driven by | Lives in |
|---|---|
| The header/footer chrome | `shared/chrome.css` or `shared/chrome-scripts.html` |
| One page's own content | That page, logged below |

## Shadow injections

<!-- ### <component> — <what and why>
     Page(s): pages/...
     Reason the DS cannot do this natively:
     Injected CSS: -->

_None yet._

## Page-built classes

Classes defined in this repo rather than by the design system. Inline links must
use the DS gradient underline (`page-builder/RULES.md` §33), never
`text-decoration: underline`.

_None yet._
