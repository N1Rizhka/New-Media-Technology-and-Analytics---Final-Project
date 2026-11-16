# NMTA Team 5 — Q15 Final Project

**Question:** What should the “you may also like” shelf show, and to whom?  
**Method:** Association rules (Week 3) on Lumen Beauty Sep–Nov 2026 orders  
**Team 5:** Nini Rizhamadze, Giulia Scarpa, Milena Moschetti, Thi Thuy Khuc, Lina-Sophie Reinsch, Hai Yen Bui  
**Visual style:** Tongji University blue (同济蓝), not a cosmetic brand palette

## Open first (submission)

See **[`deliverables/PROJECT_README.md`](deliverables/PROJECT_README.md)** for the ZIP packing list, how to run the notebook (`mlxtend>=0.23.4`), and what each table holds.

| File | Role |
|---|---|
| [`deliverables/NMTA_T05_slides.pdf`](deliverables/NMTA_T05_slides.pdf) | Pitch slides (required name) · also `.pptx` |
| [`deliverables/NMTA_T05_report.pdf`](deliverables/NMTA_T05_report.pdf) | One PDF: main report then appendix |
| [`deliverables/NMTA_T05_report.docx`](deliverables/NMTA_T05_report.docx) | Main report (Word) |
| [`deliverables/NMTA_T05_report_appendix.docx`](deliverables/NMTA_T05_report_appendix.docx) | Appendix A1–A3 (Word) |
| [`deliverables/Team5_Q15_shelf_association_rules.ipynb`](deliverables/Team5_Q15_shelf_association_rules.ipynb) | Reproducible notebook |

## Data

Official course CSVs in [`data/`](data/). Key live metrics also in `deliverables/metrics_from_data.json`.

## Rebuild locally

```bash
pip install reportlab python-pptx python-docx pypdf pandas matplotlib "mlxtend>=0.23.4"
python scripts/build_report_docx.py
python scripts/build_pitch_pptx.py
```

## Professor feedback addressed

- Both units of analysis (orders + histories); 1.45 = distinct products / order  
- Support/confidence as frequency filters, not significance; counts + denominators  
- Shelf decision cards; expected results + drop / kill conditions  
- Serves new/occasional buyers (light + first orders)  
- Theory: STP + skincare complementarity; bias in ethics (A1)  
- Pilot honesty: 6 weeks = safety check; ~40 weeks to separate 5% from 2%  
- Ethics + AI in appendix (A1 / A2); supporting figures A3  
- Slides include Theory, Limitations, and Ethics appendix after the close  
