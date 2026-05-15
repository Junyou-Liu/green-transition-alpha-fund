# Green Transition Alpha Fund

This repository contains an academic ESG equity strategy prototype for climate-transition investing. It combines fund design, benchmark-aware screening logic, proxy backtesting, and written investment communication. The project is framed as research and product design, not as an investable fund or investment recommendation.

## What This Project Shows

- ESG fund design with a defined universe, benchmark, client segment, and reporting logic.
- Climate-transition screening concepts, including exclusions, ESG quality filters, carbon-intensity constraints, and forward-looking transition indicators.
- Benchmark-aware comparison against a broad-market MSCI ACWI proxy and a clean-energy proxy.
- Standard portfolio metrics: annualized return, annualized volatility, Sharpe ratio, maximum drawdown, cumulative NAV, and carbon-intensity proxy comparison.
- Professional deliverables: Python backtest script, written note, individual write-up, and presentation deck.

## Method

The Python script uses `yfinance` to download proxy price data. By default, the clean-energy fund proxy is `ICLN` and the broad-market benchmark proxy is `ACWI`. The analysis then:

1. Aligns overlapping price history between the fund proxy and benchmark proxy.
2. Calculates annualized return, annualized volatility, Sharpe ratio, and maximum drawdown.
3. Adds illustrative carbon-intensity assumptions to compare performance and sustainability trade-offs.
4. Exports charts and tables for interpretation.
5. Keeps the conclusion conservative: lower-carbon exposure is not treated as automatic alpha.

## Key Takeaway

The project argues that climate-transition equity exposure can be presented as a credible thematic strategy only when performance, diversification, valuation discipline, benchmark risk, and carbon disclosure are shown together. The backtest is a proxy exercise, so it should be read as a product-design and ESG analytics workflow rather than proof of future performance.

## Repository Structure

```text
.
|-- README.md
|-- requirements.txt
|-- src/
|   `-- green_transition_backtest.py
|-- docs/
|   |-- backtesting_note.docx
|   `-- individual_writeup.pdf
`-- presentation/
    `-- green_transition_alpha_fund.pptx
```

## Reproduce

```bash
pip install -r requirements.txt
python src/green_transition_backtest.py
```

The script downloads proxy data, calculates the metrics, and writes charts to `figures/`.

## Scope and Limits

This project was built for DSS5203 ESG Data for Sustainable Finance and Investments at the National University of Singapore. It uses proxy instruments and simplified assumptions, so the outputs should not be interpreted as investment advice, live performance, or impact verification.

## Stack

Python, pandas, NumPy, matplotlib, seaborn, yfinance, PowerPoint, and Word/PDF reporting.
