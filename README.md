# Green Transition Alpha Fund

Research prototype for a benchmark-aware ESG equity strategy focused on climate-transition leaders. The project combines sustainability screening, portfolio construction logic, proxy backtesting, and product-design analysis to evaluate whether lower-carbon equity exposure can be delivered without overstating investment or impact claims.

## Project Overview

The Green Transition Alpha Fund is designed as an active, long-only global equity strategy benchmarked against MSCI ACWI. The fund concept targets companies with credible climate-transition exposure, including firms with lower carbon intensity, green revenue contribution, forward-looking decarbonisation plans, and transition-aligned capital expenditure.

The project was built for DSS5203 ESG Data for Sustainable Finance and Investments at the National University of Singapore. It should be read as an academic research and product-design prototype, not as an investable fund, investment recommendation, or live performance record.

## What This Project Demonstrates

- ESG fund product design with a clear investment universe, benchmark, client segment, and reporting logic.
- Climate-transition screening using negative exclusions, ESG quality filters, carbon-intensity constraints, and forward-looking transition indicators.
- Benchmark-aware portfolio construction and lifecycle governance, including monitoring, engagement, proxy voting, and reporting.
- Proxy backtesting against broad-market and clean-energy references to assess returns, volatility, drawdown, Sharpe ratio, and carbon-intensity trade-offs.
- Professional communication through a presentation deck, written investment note, and reproducible Python analysis script.

## Methodology

1. Define a global equity universe and apply exclusion screens for high-risk or misaligned sectors.
2. Use ESG and climate data concepts to identify firms with credible transition exposure.
3. Compare the proposed strategy with MSCI ACWI-style broad-market exposure and clean-energy proxy behaviour.
4. Evaluate performance using annualized return, annualized volatility, Sharpe ratio, maximum drawdown, and cumulative NAV.
5. Interpret the results conservatively, separating lower carbon intensity from risk-adjusted investment performance.

## Key Takeaway

The project does not claim that ESG exposure automatically generates superior alpha. Its main conclusion is more disciplined: climate-transition investing can be a credible thematic equity strategy, but its quality depends on valuation discipline, diversification, benchmark awareness, and transparent disclosure of carbon and performance trade-offs.

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

## Reproducing the Python Analysis

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the proxy backtest:

```bash
python src/green_transition_backtest.py
```

The script downloads historical proxy data through `yfinance`, calculates standard portfolio metrics, and writes charts to `figures/`.

## Important Caveat

Backtesting results are for academic illustration only. They depend on proxy instruments, data availability, period selection, and simplifying assumptions. They are not proof of future performance and should not be interpreted as investment advice.
