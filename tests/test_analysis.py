import pandas as pd

from src.analysis import compute_brand_strategy, identify_winners


def test_compute_brand_strategy_returns_dataframe():
    df = pd.DataFrame(
        {
            "Brand": ["A"] * 11 + ["B"] * 11,
            "price": [50] * 11 + [30] * 11,
            "Stockout_rate": [0.5] * 11 + [0.2] * 11,
            "Lost_revenue": [100] * 11 + [40] * 11,
            "name": ["item"] * 22,
        }
    )

    result = compute_brand_strategy(df, min_products=10)
    assert not result.empty
    assert "Brand" in result.columns


def test_identify_winners_filters_correctly():
    df = pd.DataFrame(
        {
            "Brand": ["A", "B"],
            "price": [45, 20],
            "Stockout_rate": [0.5, 0.1],
            "Lost_revenue": [1000, 100],
            "name": [12, 15],
        }
    )

    winners = identify_winners(df)
    assert len(winners) == 1
    assert winners.iloc[0]["Brand"] == "A"