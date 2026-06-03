# MS-GARCH Likelihood Approximation Study

Research artifacts from the study: *Impact of Likelihood Approximation Choices on the Performance of Markov-Switching GARCH Models*.

## Repository Structure

```
ms_garch_article/
├── article/                             ← Research article (journal-format)
│   ├── ms_garch_article.tex             ← LaTeX source
│   ├── ms_garch_article.pdf             ← Compiled PDF
│   └── references.bib                   ← Bibliography
│
├── full_models/                         ← Complete model parameter reference
│   ├── ms_garch_full_models.tex         ← LaTeX source
│   ├── ms_garch_full_models.pdf         ← Compiled PDF (all 220 models)
│   └── references.bib                   ← Bibliography
│
├── results/                             ← CSV data files
│   ├── comprehensive_results_220.csv    ← Master results (all 220 cases)
│   ├── <Market>_<Spec>_Parameters.csv  ← Per-market parameter tables
│   ├── <Market>_<Spec>_Diagnostics.csv ← Per-market diagnostic tables
│   └── plots/                          ← Result visualisations
│
└── code/
    └── Likelihood_Approximation_for_MS_GARCH.ipynb  ← Full estimation notebook
```
