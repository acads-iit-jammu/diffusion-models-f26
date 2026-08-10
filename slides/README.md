# Slide decks

Quarto **revealjs** sources. This is a separate Quarto project from the course
book, because a book chapter cannot render as revealjs — Quarto silently ignores
`format: revealjs` on a chapter and emits an ordinary page. Decks are therefore
built here into `../materials/`, and surfaced on the site by a thin wrapper page
in `../decks/`.

## Writing a new deck

```sh
cp _template.qmd w03-deck-01-my-topic.qmd
quarto preview w03-deck-01-my-topic.qmd    # live reload in the browser
./build-decks.sh w03-deck-01-my-topic      # -> ../materials/w03-deck-01-my-topic.html
```

`_template.qmd` demonstrates every construct the house theme supports. Naming
convention is `wNN-deck-NN-slug.qmd`; the output keeps the same basename, so the
name is also the public URL.

`##` starts a slide. Do **not** put a `format:` block in the document — the
shared settings live in `_quarto.yml` and a local block would override them.

## Putting it on the site

Three steps, none automatic:

1. **Wrapper page** — copy an existing `../decks/*.qmd`. It carries the title,
   slide count, which lecture note the deck supports, the launch link and the
   inline preview.
2. **Sidebar** — add the wrapper to the `Decks` part in `../_quarto.yml`.
3. **Resources** — add `materials/<name>.html` to `project: resources:` in
   `../_quarto.yml`, or it will not be copied into `_site`.

Then link it from the relevant week card in `../curriculum.qmd`.

## House theme

`iitjammu-reveal.scss` matches the site palette. Classes available:
`.note` (callout), `.big` (emphasis line), `.quote` + `.accent` (closing slide),
`.cols`/`.col` (two columns), `.kicker`, and `table.grid` with `td.hi`, `td.hi2`,
`td.tot`, `td.net` for highlighted count tables.

## Two settings worth not breaking

- `embed-resources: true` — each deck is one self-contained file.
- `html-math-method: mathml` — LaTeX becomes MathML at build time. The default
  (MathJax) fetches from a CDN *at runtime*, via a URL built in JavaScript that
  `embed-resources` cannot inline, so equations silently vanish in a room with no
  network. Do not switch this back.

## Size

`type: website` (not `default`) so all decks share one `../materials/site_libs/`.
The three options measured:

| Setup | Total for 7 decks |
|---|---|
| `embed-resources: true` | 24 MB (3.5 MB per deck) |
| `type: default` | 40 MB (each deck its own `_files/`) |
| **`type: website`, shared libs** | **~6 MB** (364 KB of HTML + 5.7 MB shared) |

All three are equally offline. The shared-library build is the cheapest by far,
so decks are no longer self-contained single files — a deck needs
`materials/site_libs/` beside it.

## PDFs

Not generated automatically. Headless-Chrome printing of `?print-pdf` is
unreliable here: reveal lays out page breaks in JavaScript, and Chrome usually
prints before that finishes, yielding a 1-page PDF. It succeeds occasionally,
which makes it worse than useless in a build script.

To export one by hand: open the deck, press **E** for print view, then Cmd-P and
"Save as PDF". For an automated route, `decktape` is the tool that does this
properly (it drives the browser and waits) — not currently installed.

## Gotchas

- `quarto render` in this folder emits a stray `../materials/index.html` — a
  redirect to whichever deck rendered last, and a `../materials/search.json`.
  `build-decks.sh` deletes both; if you run `quarto render` or `quarto preview`
  directly, delete them yourself.
- `quarto render a.qmd b.qmd` renders only the **first** file. Always loop, or
  use `build-decks.sh`.
- Not all LaTeX survives the MathML conversion, and failure is **silent**:
  Pandoc emits the raw `$$...$$` into the slide instead of an equation. The one
  that bit us was `\small` inside `\text{}`. Put step annotations outside the
  math as `[caption]{.step}` rather than inside it. `build-decks.sh` now warns
  when any unconverted math survives a build.
- The output filename matches the source and *is* the public URL. Renaming a
  deck breaks live links.
