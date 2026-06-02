"""
Generates ms_garch_full_models.tex from comprehensive_results_220.csv
Run from the full_models/ directory or adjust paths as needed.
"""
import pandas as pd
import os

BASE = r"c:\Users\joshua.ogundairo\Documents\My MTech Research Work-20260406T114909Z-1-001\My MTech Research Work\Report Writing"
CSV_PATH = os.path.join(BASE, "Results", "comprehensive_results_220.csv")
OUT_TEX  = os.path.join(BASE, "ms_garch_article", "full_models", "ms_garch_full_models.tex")

df = pd.read_csv(CSV_PATH)

METHOD_LABELS = {
    'gray':       "Gray's",
    'plugin':     'Plug-in',
    'quadrature': 'Quadrature',
    'particle':   'Particle Filter',
}
MARKET_ORDER = ['Equity', 'Bond', 'Crypto', 'Derivative', 'Forex']
MARKET_LABELS = {
    'Equity':     'Equity Market',
    'Bond':       'Bond Market',
    'Crypto':     'Cryptocurrency Market',
    'Derivative': 'Derivatives Market',
    'Forex':      'Foreign Exchange Market',
}
PIVOTS = {
    'Equity':     'GSPC',
    'Bond':       'TNX',
    'Crypto':     'BTC-USD',
    'Derivative': 'BTC=F',
    'Forex':      'EURUSD=X',
}
ASSET_DISPLAY = {
    'ETH-USD':  'ETH-USD',   'LTC-USD':  'LTC-USD',   'XRP-USD':  'XRP-USD',
    'DOGE-USD': 'DOGE-USD',  'NMC-USD':  'NMC-USD',   'BTC-USD':  'BTC-USD',
    'ES=F':   'ES=F',   'NQ=F':  'NQ=F',    'GC=F':  'GC=F',
    'CL=F':   'CL=F',   'BTC=F': 'BTC=F',
    'GBPUSD=X': 'GBPUSD=X', 'JPY=X':    'JPY=X',    'AUDUSD=X': 'AUDUSD=X',
    'CHF=X':    'CHF=X',    'EURGBP=X': 'EURGBP=X', 'EURUSD=X': 'EURUSD=X',
    '^FTSE': 'FTSE', '^GSPC': 'GSPC', '^IXIC': 'IXIC', '^N225': 'N225',
    '^TNX':  'TNX',  '^VIX':  'VIX',
    'BNDX': 'BNDX', 'HYG': 'HYG', 'IEI': 'IEI', 'LQD': 'LQD', 'TLT': 'TLT',
    'EEM': 'EEM', 'VTV': 'VTV',
}


def fmt(v, digits=4):
    if pd.isna(v):
        return '--'
    try:
        return f"{float(v):.{digits}f}"
    except Exception:
        return str(v)


def conv_str(v):
    if pd.isna(v):
        return '--'
    return 'Yes' if str(v).strip().upper() == 'TRUE' else 'No'


def tex_safe(s):
    """Make a string safe for LaTeX (used in labels)."""
    return str(s).replace('-','').replace('=','').replace('^','').replace('.','').lower()


def make_asset_table(asset_df, asset, spec_label, is_exo):
    """Return LaTeX source for one asset x spec parameter table."""
    methods = ['gray', 'plugin', 'quadrature', 'particle']
    lbl = tex_safe(asset) + '_' + spec_label.lower()
    disp = ASSET_DISPLAY.get(asset, asset)

    # Escape special LaTeX chars in display name
    disp_tex = disp.replace('_', '\\_').replace('^', '\\^{}').replace('=', '$=$').replace('&', '\\&')

    pivot_val = ''
    if is_exo:
        col = asset_df['Pivot'].dropna()
        pivot_val = col.iloc[0] if not col.empty else 'N/A'

    hdr_note = (r"Baseline spec: $\gamma_1 = \gamma_2 = 0$." if not is_exo
                else r"Exogenous spec; pivot = \texttt{" + pivot_val + r"}.")
    hdr_note += r" Conv.\,=\,convergence status."

    cols = (r"\textbf{Method} & $c_1$ & $c_2$ & $\gamma_1$ & $\gamma_2$ & "
            r"$\omega_1$ & $\alpha_1$ & $\beta_1$ & "
            r"$\omega_2$ & $\alpha_2$ & $\beta_2$ & "
            r"$p_{11}$ & $p_{22}$ & Conv. & LogLik \\")

    rows = []
    for method in methods:
        mdf = asset_df[asset_df['Method'] == method]
        if mdf.empty:
            rows.append(
                METHOD_LABELS[method] + r" & \multicolumn{14}{c}{No estimate} \\"
            )
            continue
        row = mdf.iloc[0]
        g1 = fmt(row['g1']) if is_exo else '--'
        g2 = fmt(row['g2']) if is_exo else '--'
        rows.append(
            f"{METHOD_LABELS[method]} & {fmt(row['c1'])} & {fmt(row['c2'])} & "
            f"{g1} & {g2} & "
            f"{fmt(row['w1'])} & {fmt(row['a1'])} & {fmt(row['b1'])} & "
            f"{fmt(row['w2'])} & {fmt(row['a2'])} & {fmt(row['b2'])} & "
            f"{fmt(row['p11'])} & {fmt(row['p22'])} & "
            f"{conv_str(row['Converged'])} & {fmt(row['LogLik'],2)} \\\\"
        )

    lines = [
        r"\begin{table}[H]",
        r"\centering\scriptsize",
        r"\caption{" + f"{disp_tex} --- {spec_label} Specification" + r"}",
        r"\label{tab:" + lbl + r"}",
        r"\begin{tabular}{lrrrrrrrrrrrrcr}",
        r"\toprule",
        cols,
        r"\midrule",
    ] + rows + [
        r"\bottomrule",
        r"\end{tabular}",
        r"\smallskip",
        r"\begin{flushleft}\scriptsize " + hdr_note + r"\end{flushleft}",
        r"\end{table}",
        "",
    ]
    return '\n'.join(lines)


def make_equation_block(asset_df, asset, spec_label, is_exo, method):
    """Return LaTeX equation block for one asset x spec x method."""
    mdf = asset_df[asset_df['Method'] == method]
    if mdf.empty:
        return ""
    row = mdf.iloc[0]
    disp = ASSET_DISPLAY.get(asset, asset)
    safe = tex_safe(asset + method)

    lines = [
        r"\paragraph{" + METHOD_LABELS[method] + " Method}",
    ]

    # Mean equations
    if is_exo:
        lines.append(r"\begin{align}")
        lines.append(
            r"\mu_{1} &= " + fmt(row['c1']) + r" " +
            (("+ " if float(row['g1'] if not pd.isna(row['g1']) else 0) >= 0 else "") +
             fmt(row['g1'])) + r"\, x_t \\"
        )
        lines.append(
            r"\mu_{2} &= " + fmt(row['c2']) + r" " +
            (("+ " if float(row['g2'] if not pd.isna(row['g2']) else 0) >= 0 else "") +
             fmt(row['g2'])) + r"\, x_t"
        )
        lines.append(r"\end{align}")
    else:
        lines.append(r"\begin{align}")
        lines.append(r"\mu_{1} &= " + fmt(row['c1']) + r" \\")
        lines.append(r"\mu_{2} &= " + fmt(row['c2']))
        lines.append(r"\end{align}")

    # Variance equations
    lines.append(r"\begin{align}")
    lines.append(
        r"\sigma^2_{t}(1) &= " + fmt(row['w1']) +
        r" + " + fmt(row['a1']) + r"\, y_{t-1}^2 + " + fmt(row['b1']) + r"\, \sigma^2_{t-1} \\"
    )
    lines.append(
        r"\sigma^2_{t}(2) &= " + fmt(row['w2']) +
        r" + " + fmt(row['a2']) + r"\, y_{t-1}^2 + " + fmt(row['b2']) + r"\, \sigma^2_{t-1}"
    )
    lines.append(r"\end{align}")

    # Transition matrix
    lines.append(r"\begin{equation}")
    lines.append(
        r"P = \begin{pmatrix} " +
        fmt(row['p11']) + r" & " + fmt(1 - float(row['p11'])) + r" \\ " +
        fmt(1 - float(row['p22'])) + r" & " + fmt(row['p22']) +
        r" \end{pmatrix}"
    )
    lines.append(r"\end{equation}")
    lines.append(
        r"LogLik $= " + fmt(row['LogLik'], 2) + r"$; Converged: " + conv_str(row['Converged']) + "."
    )
    lines.append("")
    return '\n'.join(lines)


# ============================================================
# Build the full LaTeX document
# ============================================================

doc_lines = [
    r"% ============================================================",
    r"%  MS-GARCH Full Model Parameter Reference",
    r"%  All 220 estimated models: parameter tables and equations",
    r"% ============================================================",
    r"\documentclass[11pt, a4paper]{article}",
    r"\usepackage[utf8]{inputenc}",
    r"\usepackage[T1]{fontenc}",
    r"\usepackage{mathptmx}",
    r"\usepackage[top=2cm, bottom=2.5cm, left=2.5cm, right=2.5cm]{geometry}",
    r"\usepackage{amsmath, amssymb}",
    r"\usepackage{array, booktabs, longtable}",
    r"\usepackage{float}",
    r"\usepackage{caption}",
    r"\captionsetup{font=small, labelfont=bf}",
    r"\usepackage{setspace}",
    r"\onehalfspacing",
    r"\usepackage{titlesec}",
    r"\titleformat{\section}{\large\bfseries}{\thesection.}{0.8em}{}",
    r"\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection.}{0.6em}{}",
    r"\usepackage[authoryear,round]{natbib}",
    r"\bibliographystyle{apalike}",
    r"\usepackage[hidelinks]{hyperref}",
    r"\usepackage{fancyhdr}",
    r"\pagestyle{fancy}",
    r"\fancyhf{}",
    r"\fancyhead[L]{\small\textit{Ogundairo \& Ojo}}",
    r"\fancyhead[R]{\small\textit{MS-GARCH Full Model Reference}}",
    r"\fancyfoot[C]{\thepage}",
    r"\renewcommand{\headrulewidth}{0.4pt}",
    r"\setlength{\parindent}{0pt}",
    r"\setlength{\parskip}{4pt}",
    r"",
    r"\begin{document}",
    r"",
    r"\begin{center}",
    r"{\LARGE \bfseries MS-GARCH Likelihood Approximation Study}\\[0.6em]",
    r"{\large \bfseries Complete Model Parameter Reference}\\[1em]",
    r"{\large Joshua Ogundairo\textsuperscript{a} \quad and \quad Oluwadare O. Ojo\textsuperscript{a}}\\[0.4em]",
    r"{\small \textsuperscript{a}Department of Statistics, Federal University of Technology, Akure (FUTA), Nigeria}\\[0.2em]",
    r"{\small \href{mailto:ogundairosta154470@futa.edu.ng}{ogundairosta154470@futa.edu.ng} \quad \href{mailto:ojooo@futa.edu.ng}{ojooo@futa.edu.ng}}\\[0.6em]",
    r"{\small Companion document to: \textit{Impact of Likelihood Approximation Choices on the Performance of MS-GARCH Models}}\\[0.4em]",
    r"{\small June 2026}",
    r"\end{center}",
    r"",
    r"\vspace{0.5em}\hrule\vspace{1em}",
    r"",
    r"\noindent\textbf{About this document.}",
    r"This file contains the complete estimated parameter sets for all 220 MS-GARCH(1,1) model runs",
    r"reported in the companion article. Models are organized by market archetype (Section~1--5),",
    r"then by asset, and within each asset by specification (Baseline and Exogenous) and approximation",
    r"method (Gray's collapsing, Plug-in, Gaussian Quadrature, Particle Filter).",
    r"Parameter tables present the twelve-element vector",
    r"$\Psi = \{c_1, c_2, \gamma_1, \gamma_2, \omega_1, \alpha_1, \beta_1, \omega_2, \alpha_2, \beta_2, p_{11}, p_{22}\}$",
    r"alongside the log-likelihood (LogLik) and convergence status (Conv.).",
    r"Equation blocks then render the fitted model explicitly for each method.",
    r"Dashes (--) in the $\gamma$ columns indicate the baseline (internal-dynamics-only) specification",
    r"where $\gamma_1 = \gamma_2 = 0$ by construction.",
    r"",
    r"\tableofcontents",
    r"\newpage",
    r"",
]

for market in MARKET_ORDER:
    mdf = df[df['Market'] == market]
    pivot = PIVOTS[market]
    assets = mdf['Asset'].unique()

    # Sort: pivot last
    assets_sorted = [a for a in assets if a != pivot and not str(a).replace('^','') == pivot]
    # Also handle ^-prefixed pivots
    pivot_variants = [pivot, '^' + pivot]
    assets_sorted = [a for a in assets if a not in pivot_variants]
    pivot_assets   = [a for a in assets if a in pivot_variants]
    assets_sorted  = assets_sorted + pivot_assets

    doc_lines.append(r"\section{" + MARKET_LABELS[market] + "}")
    doc_lines.append(
        r"\noindent Pivot (exogenous conditioning variable): \textbf{\texttt{" + pivot + r"}}."
    )
    doc_lines.append(r"")

    for asset in assets_sorted:
        adf = mdf[mdf['Asset'] == asset]
        disp = ASSET_DISPLAY.get(asset, asset)
        disp_tex = disp.replace('_', '\\_').replace('^', '\\^{}').replace('=', '$=$')

        doc_lines.append(r"\subsection{Asset: \texttt{" + disp_tex + "}}")

        # ----------- BASELINE -----------
        base_df = adf[adf['Has_Exo'] == False]
        if not base_df.empty:
            doc_lines.append(r"\subsubsection*{Baseline Specification}")
            doc_lines.append(make_asset_table(base_df, asset, 'Baseline', False))
            doc_lines.append(r"\medskip")
            doc_lines.append(r"\noindent\textbf{Fitted Equations (Baseline):}")
            for method in ['gray', 'plugin', 'quadrature', 'particle']:
                doc_lines.append(make_equation_block(base_df, asset, 'Baseline', False, method))

        # ----------- EXOGENOUS -----------
        exo_df = adf[adf['Has_Exo'] == True]
        if not exo_df.empty:
            doc_lines.append(r"\subsubsection*{Exogenous Specification}")
            doc_lines.append(make_asset_table(exo_df, asset, 'Exogenous', True))
            doc_lines.append(r"\medskip")
            doc_lines.append(r"\noindent\textbf{Fitted Equations (Exogenous):}")
            for method in ['gray', 'plugin', 'quadrature', 'particle']:
                doc_lines.append(make_equation_block(exo_df, asset, 'Exogenous', True, method))

        doc_lines.append(r"\clearpage")

doc_lines.append(r"\end{document}")

tex_content = '\n'.join(doc_lines)

with open(OUT_TEX, 'w', encoding='utf-8') as f:
    f.write(tex_content)

print(f"Written: {OUT_TEX}")
print(f"Total lines: {len(doc_lines)}")
