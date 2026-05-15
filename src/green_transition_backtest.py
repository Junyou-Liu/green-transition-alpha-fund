"""Proxy backtest for the Green Transition Alpha Fund project.

The script compares a clean-energy proxy with a broad global equity proxy and
reports standard return and risk metrics. It is intended for academic
replication of the project logic, not for investment advice or live portfolio
management.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf


TRADING_DAYS = 252
DEFAULT_START = "2019-01-01"
DEFAULT_END = "2026-04-01"
RISK_FREE_RATE = 0.02


@dataclass(frozen=True)
class PerformanceMetrics:
    annualized_return: float
    annualized_volatility: float
    sharpe_ratio: float
    max_drawdown: float
    carbon_intensity: float


def download_price_series(ticker: str, start: str, end: str) -> pd.Series:
    """Download an adjusted close price series from Yahoo Finance."""
    data = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    if data.empty:
        raise ValueError(f"No price data returned for ticker: {ticker}")

    close = data["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    close = close.dropna()
    close.name = ticker
    if close.empty:
        raise ValueError(f"No usable close prices returned for ticker: {ticker}")
    return close


def calculate_metrics(
    prices: pd.Series,
    carbon_intensity: float,
    risk_free_rate: float = RISK_FREE_RATE,
) -> PerformanceMetrics:
    """Calculate annualized return, volatility, Sharpe ratio, and drawdown."""
    daily_returns = prices.pct_change().dropna()
    if daily_returns.empty:
        raise ValueError("At least two valid prices are required to calculate returns.")

    years = (prices.index[-1] - prices.index[0]).days / 365.25
    total_return = prices.iloc[-1] / prices.iloc[0] - 1
    annualized_return = (1 + total_return) ** (1 / years) - 1
    annualized_volatility = daily_returns.std() * np.sqrt(TRADING_DAYS)
    sharpe_ratio = (
        (annualized_return - risk_free_rate) / annualized_volatility
        if annualized_volatility > 0
        else np.nan
    )

    cumulative_nav = prices / prices.iloc[0]
    drawdown = cumulative_nav / cumulative_nav.cummax() - 1

    return PerformanceMetrics(
        annualized_return=annualized_return,
        annualized_volatility=annualized_volatility,
        sharpe_ratio=sharpe_ratio,
        max_drawdown=drawdown.min(),
        carbon_intensity=carbon_intensity,
    )


def build_metric_table(metrics: dict[str, PerformanceMetrics]) -> pd.DataFrame:
    """Create a presentation-ready metric table."""
    rows = []
    for name, metric in metrics.items():
        rows.append(
            {
                "portfolio": name,
                "annualized_return": metric.annualized_return,
                "annualized_volatility": metric.annualized_volatility,
                "sharpe_ratio": metric.sharpe_ratio,
                "max_drawdown": metric.max_drawdown,
                "carbon_intensity_tco2e_per_usd_m": metric.carbon_intensity,
            }
        )
    return pd.DataFrame(rows).set_index("portfolio")


def plot_cumulative_nav(prices: pd.DataFrame, output_dir: Path) -> None:
    """Plot cumulative NAV for all price series."""
    cumulative_nav = prices / prices.iloc[0]

    fig, ax = plt.subplots(figsize=(10, 5))
    for column in cumulative_nav.columns:
        ax.plot(cumulative_nav.index, cumulative_nav[column], linewidth=2, label=column)

    ax.set_title("Proxy Cumulative NAV")
    ax.set_ylabel("Cumulative NAV (Start = 1)")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "cumulative_nav.png", dpi=200)
    plt.close(fig)


def plot_metric_comparison(metric_table: pd.DataFrame, output_dir: Path) -> None:
    """Plot selected metrics for the proxy comparison."""
    display = metric_table.copy()
    display["annualized_return"] *= 100
    display["annualized_volatility"] *= 100
    display["max_drawdown"] *= 100

    selected = display[
        [
            "annualized_return",
            "annualized_volatility",
            "sharpe_ratio",
            "max_drawdown",
            "carbon_intensity_tco2e_per_usd_m",
        ]
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    selected[
        ["annualized_return", "annualized_volatility", "max_drawdown"]
    ].T.plot(kind="bar", ax=axes[0])
    axes[0].set_title("Return and Risk Metrics")
    axes[0].set_ylabel("Percent")
    axes[0].grid(axis="y", alpha=0.3)

    selected[["sharpe_ratio", "carbon_intensity_tco2e_per_usd_m"]].T.plot(
        kind="bar", ax=axes[1]
    )
    axes[1].set_title("Sharpe and Carbon Intensity")
    axes[1].grid(axis="y", alpha=0.3)

    for ax in axes:
        ax.tick_params(axis="x", rotation=30)
        ax.legend(loc="best")

    fig.tight_layout()
    fig.savefig(output_dir / "metric_comparison.png", dpi=200)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default=DEFAULT_START, help="Backtest start date.")
    parser.add_argument("--end", default=DEFAULT_END, help="Backtest end date.")
    parser.add_argument(
        "--fund-ticker",
        default="ICLN",
        help="Clean-energy proxy ticker for the transition fund.",
    )
    parser.add_argument(
        "--benchmark-ticker",
        default="ACWI",
        help="Broad-market benchmark proxy ticker.",
    )
    parser.add_argument(
        "--output-dir",
        default="figures",
        help="Directory for generated charts.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fund_prices = download_price_series(args.fund_ticker, args.start, args.end)
    benchmark_prices = download_price_series(args.benchmark_ticker, args.start, args.end)
    prices = pd.concat(
        {
            "Transition proxy": fund_prices,
            "MSCI ACWI proxy": benchmark_prices,
        },
        axis=1,
    ).dropna()

    if prices.empty:
        raise ValueError("No overlapping price history between fund and benchmark proxies.")

    metrics = {
        "Transition proxy": calculate_metrics(
            prices["Transition proxy"],
            carbon_intensity=65.0,
        ),
        "MSCI ACWI proxy": calculate_metrics(
            prices["MSCI ACWI proxy"],
            carbon_intensity=168.0,
        ),
    }
    metric_table = build_metric_table(metrics)

    plot_cumulative_nav(prices, output_dir)
    plot_metric_comparison(metric_table, output_dir)

    formatted = metric_table.copy()
    for column in ["annualized_return", "annualized_volatility", "max_drawdown"]:
        formatted[column] = formatted[column].map(lambda value: f"{value:.2%}")
    formatted["sharpe_ratio"] = formatted["sharpe_ratio"].map(lambda value: f"{value:.2f}")
    formatted["carbon_intensity_tco2e_per_usd_m"] = formatted[
        "carbon_intensity_tco2e_per_usd_m"
    ].map(lambda value: f"{value:.1f}")

    print("\nProxy backtest metrics")
    print(formatted.to_string())
    print(f"\nCharts saved to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
