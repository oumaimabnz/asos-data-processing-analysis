from pathlib import Path

import pandas as pd


def compute_brand_strategy(df: pd.DataFrame, min_products: int = 10) -> pd.DataFrame:
    """
    Aggregate product-level data into brand-level strategy metrics.
    """
    brand_strategy = (
        df.groupby("Brand")
        .agg(
            {
                "price": "mean",
                "Stockout_rate": "mean",
                "Lost_revenue": "sum",
                "name": "count",
            }
        )
        .reset_index()
    )

    brand_strategy = brand_strategy[brand_strategy["name"] > min_products]

    return brand_strategy


def identify_winners(
    brand_strategy: pd.DataFrame,
    min_price: float = 40,
    min_stockout_rate: float = 0.4,
) -> pd.DataFrame:
    """
    Select brands in the high-price, high-stockout quadrant.
    """
    return brand_strategy[
        (brand_strategy["price"] > min_price)
        & (brand_strategy["Stockout_rate"] > min_stockout_rate)
    ].copy()


def save_brand_strategy(df: pd.DataFrame, output_path: str) -> None:
    """
    Save brand strategy summary to CSV.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)