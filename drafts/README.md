# Draft material — not rendered

Everything under `drafts/` is tracked in git but **excluded from `_quarto.yml`**, so
Quarto never builds it and it does not appear on the site.

## `lecture-log/` — the old week-by-week pages (W01–W17)

Seventeen pages, one per teaching week. They were the site's original spine, before
the course was reorganised **by concept**: the numbered Lecture Notes now read
linearly and do not shift when a lecture does, and [`curriculum.qmd`](../curriculum.qmd)
is the timetable laid over them.

That leaves the week pages redundant for anything except a running log of what was
actually said in each session — and a log is only worth publishing if it stays true.

`w04.qmd` through `w17.qmd` are the live example of why. Notes 06 and 07 moved
forward into W03, which unsettled everything after it, so the curriculum now shows
W04 onwards as bare placeholders — dates, deadlines, holidays, nothing more. The
teaching plan for those weeks is here, not on the site, so the site never claims a
lecture that has not been committed to.

## Promotion rule

**Draft → Live only if we follow the exact curriculum.** A week page goes back into
`_quarto.yml` when the week it describes has been taught as the curriculum card says
it would be. Until then it stays here, where being out of date costs nothing.

Restoring one is two steps: move the file back out of `drafts/`, and add it to
`_quarto.yml`. Note that inbound links were stripped when these pages were
un-rendered — `curriculum.qmd`, `course.qmd` and several tutorials mention weeks as
plain text (`W02`) rather than as links.
