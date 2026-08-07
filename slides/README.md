# Presentation — NovaBank Cloud Foundation

`novabank-cloud-foundation.odp` is the interview/customer presentation for this PoC, in **OpenDocument Presentation** format (opens natively in LibreOffice Impress / Apache OpenOffice Impress; imports cleanly into PowerPoint and Google Slides too).

It is **generated from Python**, not hand-edited in an office app, so the deck stays version-controlled, diffable, and reproducible from the same source-of-truth docs (`docs/architecture-summary.md`, `docs/assumptions.md`) as the rest of the repo.

## Contents (12 slides)

1. Title
2. Agenda
3. The situation at NovaBank (6D: Discover)
4. Why Azure, why PaaS-first (6D: Define & Design)
5. Proposed architecture (diagram)
6. Core building blocks
7. Two environments, one Terraform module (dev vs prod)
8. Repeatable delivery — CI/CD, OIDC, `terraform` commands
9. Live demo (section break)
10. Using AI as part of the workflow
11. Trade-offs, risks & next steps
12. Questions & discussion

## Regenerating the deck

```powershell
# from the repo root, using the project's Python environment
pip install odfpy matplotlib Pillow

python slides/generate_diagram.py       # regenerates slides/assets/architecture-diagram.png
python slides/generate_presentation.py  # regenerates slides/novabank-cloud-foundation.odp
```

Edit `generate_presentation.py` (slide content/layout) or `generate_diagram.py` (architecture diagram) and re-run — the `.odp` is fully rebuilt from scratch each time.

## Files

| File                              | Purpose                                                            |
| --------------------------------- | ------------------------------------------------------------------ |
| `generate_presentation.py`        | Builds all 12 slides (text, tables, cards, image) via `odfpy`      |
| `generate_diagram.py`             | Renders `assets/architecture-diagram.png` via `matplotlib`         |
| `assets/architecture-diagram.png` | Architecture diagram embedded on the "Proposed architecture" slide |
| `novabank-cloud-foundation.odp`   | The generated presentation — open this one to present              |

## Presenting

Open `novabank-cloud-foundation.odp` in LibreOffice Impress (free, cross-platform) and use **Slide Show → Start from First Slide** (F5). Speaker notes are not included by default; add them per-slide in Impress' Notes view if needed before presenting.
