# NMTA Team 5 — Q15 Final Project

**Question:** What should the “you may also like” shelf show, and to whom?  
**Method:** Association rules (Week 3) on Lumen Beauty Sep–Nov 2026 orders  
**Team 5:** Nini Rizhamadze, Giulia Scarpa, Milena Moschetti, Thi Thuy Khuc, Lina-Sophie Reinsch, Hai Yen Bui

## Deliverables (submit these)

| File | Role |
|---|---|
| [`deliverables/Team5_Q15_shelf_association_rules.ipynb`](deliverables/Team5_Q15_shelf_association_rules.ipynb) | Reproducible Python notebook |
| [`deliverables/Team5_Q15_report.pdf`](deliverables/Team5_Q15_report.pdf) | Main report (≤12 pages) |
| [`deliverables/Team5_Q15_appendix.pdf`](deliverables/Team5_Q15_appendix.pdf) | Ethics (§6) + AI use (§7) appendix |
| [`deliverables/Team5_Q15_pitch.pptx`](deliverables/Team5_Q15_pitch.pptx) | 8-minute pitch slides |

## Data (required to re-run the notebook)

Copy from the course project kit into `data/`:

- `lb_order_lines.csv`
- `lb_users.csv`

See [`data/README.md`](data/README.md). Numbers in the report/slides match the verified run on the official course export.

## Rebuild PDF / PPT locally

```bash
pip install reportlab python-pptx pypdf mlxtend pandas matplotlib
python scripts/build_report_pdf.py
python scripts/build_pitch_pptx.py
```

## Professor feedback addressed

- Both units of analysis (orders + histories); 1.45 = distinct products / order  
- Support/confidence as frequency filters, not significance; counts + denominators on rules  
- Shelf decision cards (trigger, customers, position, no-history view, reject evidence)  
- Serves new/occasional buyers checked via light buyers + first orders  
- Expected results + explicit drop / kill conditions  
- Ethics + AI moved to appendix; AI tools named (Claude, Cursor)  
- Goes beyond the menu (channel split, first-order check, light-vs-heavy stretch)

## Source materials (reference)

Project brief, rubric, question menu, data dictionary/guidebook, team plan, professor comment screenshots, and earlier drafts live in the repo root.
