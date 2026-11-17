# NMTA Team 5 — Q15 Final Project

**Question:** What should the “you may also like” shelf show, and to whom?  
**Method:** Association rules (Week 3) on Lumen Beauty Sep–Nov 2026 orders  
**Team 5:** Nini Rizhamadze, Giulia Scarpa, Milena Moschetti, Thi Thuy Khuc, Lina-Sophie Reinsch, Hai Yen Bui  
**Visual style:** Tongji University blue (同济蓝)

## Send to the professor (`deliverables/`)

| File | Role |
|---|---|
| [`deliverables/NMTA_T05_slides.pdf`](deliverables/NMTA_T05_slides.pdf) | Pitch slides (PDF) |
| [`deliverables/NMTA_T05_slides.pptx`](deliverables/NMTA_T05_slides.pptx) | Pitch slides (PowerPoint) |
| [`deliverables/NMTA_T05_report.pdf`](deliverables/NMTA_T05_report.pdf) | Report + appendices (PDF) |
| [`deliverables/NMTA_T05_report.docx`](deliverables/NMTA_T05_report.docx) | Report + appendices (Word) |
| [`deliverables/Team5_Q15_shelf_association_rules.ipynb`](deliverables/Team5_Q15_shelf_association_rules.ipynb) | Reproducible notebook |

Team-only speaker notes (not for submission): [`pitch/Team5_Q15_pitch_script.md`](pitch/Team5_Q15_pitch_script.md)

## Data

Official course CSVs in [`data/`](data/). Figures regenerate into [`figures/`](figures/) on notebook **Restart & Run All**.

```bash
pip install pandas matplotlib "mlxtend>=0.23.4" numpy
jupyter notebook deliverables/Team5_Q15_shelf_association_rules.ipynb
```

## Rebuild slides / report locally

```bash
pip install reportlab python-pptx python-docx pypdf
python scripts/build_final_report.py
python scripts/build_pitch_pptx.py
```
