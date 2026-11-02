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
use the DS gradient underline (`page-builder/RULES.md` §34), never
`text-decoration: underline`.

### `umd-brand-site-filter-*` — left filter rail with keyword search
Pages: `pages/trademarks-licensing/licensed-vendors-database.html`,
`pages/trademarks-licensing/licensed-vendors-database-tshirt.html`

DS counterpart: none. The DS has the Filter Band (a horizontal select + search
panel, critical.css §23) but no faceted left rail. This rail is the
admissions-design programs explorer (`umd-admissions-filter-*`), renamespaced,
with the keyword search moved into the rail and nested bucket → category
checkboxes (`-bucket`, `-bucket-row`, `-bucket-toggle`, `-bucket-children`). It reuses the DS
`umd-field-checkbox-wrapper`, `umd-field-input`, `umd-text-cluster-pill` and
`umd-text-line-trailing`; the
results are unaltered tabular person cards, which draw their own rules. Behavior is in
`scripts/licensed-vendors-database.js`.

Two projects now hand-roll the same rail under different namespaces. If a third
project needs it, promote it to `page-builder` (LAYOUT-PATTERNS.md + a shared
script) rather than copying it again.

### `umd-element-person data-display="tabular"` — fundraiser status in the italic `slot="pronouns"`
Same pages. Cards are the DS tabular person card, unaltered, led by the contact
person with the vendor in `slot="association"` and the vendor website as a
secondary call-to-action in `slot="actions"`. "Approved for internal fundraisers" uses
the italic `slot="pronouns"` line. (As of components 2.0.0 the contact lockup
accepts `slot="additional-contact"` but never renders it, in any display.)

### `umd-field-input-search-wrapper` — 24px search icon
Same pages, scoped to `.umd-brand-site-filter-search`. The DS icon sits in a 32px
box; this page sets the icon to 24px (`--umd-space-md`) with a 32px hover square
(`--umd-space-lg`), both centered in the field. The icon artwork and hover colors
are the DS's, unchanged.
