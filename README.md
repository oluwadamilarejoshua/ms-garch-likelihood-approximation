# MS-GARCH Likelihood Approximation Study

**Impact of Likelihood Approximation Choices on the Performance of Markov-Switching GARCH Models: Evidence from Thirty Global Financial Assets**

**Authors:**
- Joshua Ogundairo (MTech Candidate, Statistics — Federal University of Technology, Akure, FUTA)  
  Email: ogundairosta154470@futa.edu.ng
- Oluwadare O. Ojo (Associate Professor of Statistics, FUTA)  
  Email: ojooo@futa.edu.ng

---

## About This Repository

This repository contains all research artifacts from the above study, organized as follows:

### Repository Structure

```
ms_garch_article/
├── article/                    ← Research article (journal-format)
│   ├── ms_garch_article.tex    ← LaTeX source
│   ├── ms_garch_article.pdf    ← Compiled PDF (18 pages)
│   └── references.bib          ← Bibliography
│
├── full_models/                ← Complete model parameter reference
│   ├── ms_garch_full_models.tex ← LaTeX source (generated from CSV)
│   ├── ms_garch_full_models.pdf ← Compiled PDF (112 pages, all 220 models)
│   ├── generate_full_models.py  ← Python script used to generate the LaTeX
│   └── references.bib
│
├── results/                    ← All CSV data files
│   ├── comprehensive_results_220.csv       ← Master results (all 220 cases)
│   ├── Bonds_Baseline_Parameters.csv
│   ├── Bonds_Baseline_Diagnostics.csv
│   ├── Bonds_Exogenous_Parameters.csv
│   ├── Bonds_Exogenous_Diagnostics.csv
│   ├── Crypto_Baseline_Parameters.csv
│   ├── Crypto_Baseline_Diagnostics.csv
│   ├── Crypto_Exogenous_Parameters.csv
│   ├── Crypto_Exogenous_Diagnostics.csv
│   ├── Derivatives_Baseline_Parameters.csv
│   ├── Derivatives_Baseline_Diagnostics.csv
│   ├── Derivatives_Exogenous_Parameters.csv
│   ├── Derivatives_Exogenous_Diagnostics.csv
│   ├── Equities_Baseline_Parameters.csv
│   ├── Equities_Baseline_Diagnostics.csv
│   ├── Equities_Exogenous_Parameters.csv
│   ├── Equities_Exogenous_Diagnostics.csv
│   ├── Forex_Baseline_Parameters.csv
│   ├── Forex_Baseline_Diagnostics.csv
│   ├── Forex_Exogenous_Parameters.csv
│   ├── Forex_Exogenous_Diagnostics.csv
│   └── plots/
│       ├── Full_Portfolio_Market_Visualization_5_Panes.png
│       └── MSGARCH_Comparative_Analysis.png
│
└── code/
    └── Likelihood_Approximation_for_MS_GARCH.ipynb  ← Full estimation notebook
```

---

## Study Overview

This research evaluates four likelihood approximation methods for **MS-GARCH(1,1)** models — a framework that combines Markov-regime switching with GARCH volatility dynamics — applied to **30 financial assets** from five market archetypes over a ten-year period (September 2015 – August 2025).

### Approximation Methods
| Method | Description |
|---|---|
| **Gray's Collapsing** | Moment-matching procedure that collapses variance paths at each step |
| **Plug-in** | Deterministic approximation using filtered regime probabilities |
| **Gaussian Quadrature** | Five-point Gauss-Hermite numerical integration |
| **Particle Filter** | Sequential Monte Carlo with 1,000 SIR particles |

### Assets and Markets
| Market | Target Assets | Pivot (Exogenous Variable) |
|---|---|---|
| Equities | FTSE, N225, IXIC, EEM, VTV | GSPC |
| Bonds | IEI, TLT, BNDX, LQD, HYG | TNX |
| Cryptocurrencies | ETH-USD, LTC-USD, XRP-USD, DOGE-USD, NMC-USD | BTC-USD |
| Derivatives | ES=F, NQ=F, VIX, GC=F, CL=F | BTC=F |
| Forex | GBPUSD=X, JPY=X, AUDUSD=X, CHF=X, EURGBP=X | EURUSD=X |

### Experimental Design
- **220 cases** = 25 target assets × 4 methods × 2 specs + 5 pivots × 4 methods × 1 spec
- **Baseline spec**: captures internal volatility dynamics (γ₁ = γ₂ = 0)
- **Exogenous spec**: incorporates cross-market pivot variable (γ₁, γ₂ estimated)

---

## Key Findings

1. **Plug-in dominates** log-likelihood maximisation across all five market archetypes and all four kurtosis classes — often by margins exceeding 2,000 log-likelihood units for equity-index futures.
2. **Particle Filter is the weakest estimator** in every context, underperforming analytical methods by 2,000–4,000 units while exhibiting parameter degeneracy near initialisation values. Use only as a last-resort convergence fallback.
3. **Quadrature's niche**: preferred method for exogenous cryptocurrency models in the medium-kurtosis range, where it outperforms Plug-in in convergence-adjusted likelihood.
4. **VIX is intractable**: all analytical methods failed to converge for the CBOE Volatility Index in every specification — the sole instrument for which the Particle Filter is the only convergent solution.
5. **Exogenous conditioning is selective**: bond and equity markets benefit from pivot conditioning; Forex shows negligible improvement, confirming idiosyncratic internal dynamics in major currency pairs.

### Kurtosis-Based Method Selection Guide
| Kurtosis Class | Primary Method | Fallback |
|---|---|---|
| Low (K < 10) | Plug-in | Gray's (convergence guarantee) |
| Medium (10 ≤ K < 20) | Plug-in (baseline); Quadrature (exog. crypto) | Gray's |
| High (20 ≤ K < 50) | Plug-in (verify convergence) | Gray's or Quadrature |
| Extreme (K ≥ 50) | Plug-in (attempt first) | Particle Filter (last resort only) |

---

## Reproducing the Results

### Data Collection
All data retrieved via `yfinance` Python library (free, open access):
```python
import yfinance as yf
data = yf.download("BTC-USD", start="2015-09-01", end="2025-08-31")
```

### Running the Estimation Notebook
```bash
jupyter notebook code/Likelihood_Approximation_for_MS_GARCH.ipynb
```
The notebook contains the full estimation pipeline: data collection, preprocessing, all four approximation implementations (via C++/Cython backend), and result aggregation.

### Compiling the LaTeX Documents
```bash
# Research article (from article/ directory)
pdflatex ms_garch_article.tex
bibtex ms_garch_article
pdflatex ms_garch_article.tex
pdflatex ms_garch_article.tex

# Full models reference (from full_models/ directory)
# First regenerate LaTeX from CSV if needed:
python generate_full_models.py
pdflatex ms_garch_full_models.tex
pdflatex ms_garch_full_models.tex
```

### Requirements
- Python 3.8+: `numpy`, `pandas`, `scipy`, `yfinance`, `jupyter`
- LaTeX: MiKTeX or TeX Live with standard packages (`amsmath`, `booktabs`, `natbib`, `fancyhdr`, `mdframed`)

---

## CSV Data Dictionary

### `comprehensive_results_220.csv`
| Column | Description |
|---|---|
| Asset | Asset ticker symbol |
| Method | Approximation method (gray / plugin / quadrature / particle) |
| c1, c2 | Regime-dependent conditional mean intercepts |
| g1, g2 | Regime-dependent exogenous (γ) sensitivity coefficients |
| w1, a1, b1 | GARCH parameters for Regime 1 (ω, α, β) |
| w2, a2, b2 | GARCH parameters for Regime 2 (ω, α, β) |
| p11, p22 | Regime persistence probabilities |
| LogLik | Log-likelihood at optimum |
| Converged | Boolean convergence flag (L-BFGS-B criterion) |
| AIC, BIC | Information criteria |
| T_obs | Number of observations |
| Market | Market archetype |
| Has_Exo | Whether this is an exogenous specification |
| Pivot | Exogenous conditioning asset (NaN for baseline) |
| Persist_S1, Persist_S2 | Regime persistence (= p11 and p22 respectively) |

---

## Citation

If you use this data, code, or findings, please cite:

> Ogundairo, J., & Ojo, O.O. (2026). *Impact of Likelihood Approximation Choices on the Performance of Markov-Switching GARCH Models: Evidence from Thirty Global Financial Assets*. Federal University of Technology, Akure.

---

## License

This research repository is made available for academic and non-commercial use. The estimation code and LaTeX templates are released under the MIT License. The data was obtained from Yahoo Finance and is subject to Yahoo's terms of use.
