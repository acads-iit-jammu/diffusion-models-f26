# ID-5-02 (TO) · Mathematical Foundations of Diffusion Models · Monsoon 2026

Course website for ID-5-02 (TO), IIT Jammu — instructors Uma Satyaranjan and Soma S Dhavala.

Built with [Quarto](https://quarto.org/) (book project), themed for IIT Jammu.
Same layout as the CS-1-01 (MO) course site.

## Local preview

```sh
quarto preview
```

## Publish to GitHub Pages

```sh
quarto publish gh-pages
```

## Layout

- `_quarto.yml` — site configuration
- `iitjammu.scss` — theme (IIT Jammu blues, Roboto/Roboto Slab)
- `index.qmd`, `course.qmd`, `syllabus.qmd`, `resources.qmd` — pages
- `weeks/` — weekly notes (pre-read / in-class / after-class)
- `materials/` — student-facing files
- `private/` — instructor-only material (its own git repo, gitignored here, never published)
