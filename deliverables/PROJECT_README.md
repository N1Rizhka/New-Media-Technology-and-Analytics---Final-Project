# NMTA Team 5 · Q15 — submission pack

**Question:** What should the “you may also like” shelf show, and to whom?  
**Course:** New Media Technology and Analytics (20001920076) · Fall 2026 · Tongji SEM  
**Team 5:** Nini Rizhamadze, Giulia Scarpa, Milena Moschetti, Thi Thuy Khuc, Lina-Sophie Reinsch, Hai Yen Bui  
**Presentation slot:** 10:18

## Open these first

| Order | File | What it is |
|---|---|---|
| 1 | `NMTA_T05_slides.pdf` | Pitch slides (also `NMTA_T05_slides.pptx`) |
| 2 | `NMTA_T05_report.pdf` / `NMTA_T05_report.docx` | Report on `project_report_template` structure (§1–7, 8 pages) |
| 3 | `Team5_Q15_shelf_association_rules.ipynb` | Reproducible notebook — **Restart & Run All** |

Supporting: `Team5_Q15_pitch_script.md` (spoken script), `metrics_from_data.json` (key numbers).

## How to run the notebook

```bash
# from the repo root (needs data/ next to the notebook paths)
pip install pandas matplotlib mlxtend "mlxtend>=0.23.4" numpy
# This project was last run with mlxtend 0.25.0
jupyter notebook deliverables/Team5_Q15_shelf_association_rules.ipynb
# Kernel → Restart & Run All
```

Data files live in `data/`:

| File | Holds |
|---|---|
| `lb_order_lines.csv` | One row per SKU line in an order (baskets, rules) |
| `lb_users.csv` | Registered users (`n_orders`, first-order date, …) |
| `lb_streams.csv` | Livestream sessions (not used for Q15 baskets) |
| `lb_comments.csv` | Stream comments (not used) |
| `lb_follows.csv` | Follow/share edges (not used) |

Figures are written to `figures/` on Restart & Run All (Tongji-blue palette).

## Rebuild slides / report locally

```bash
pip install reportlab python-pptx python-docx pypdf
python scripts/build_report_docx.py
python scripts/build_pitch_pptx.py
```

## Chart / deck colours

Tongji blue (同济蓝 C100 M60 Y0 K0 ≈ `#0066B3`), with `#003D7A` / `#3F94E7` / `#EEF1F3` from the university site — not a brand-cosmetic palette.
