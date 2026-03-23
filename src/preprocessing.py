import json
import re
from pathlib import Path

import pandas as pd


BRAND_MAP = {
    "New": "New Look",
    "River": "River Island",
    "Miss": "Miss Selfridge",
    "Under": "Under Armour",
    "Vero": "Vero Moda",
    "In": "In The Style",
}


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning:
    - convert price to numeric
    - drop rows with missing price
    - ensure description is string
    """
    df = df.copy()

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])
    df["description"] = df["description"].astype(str)

    return df


def get_brand(text: str) -> str:
    """
    Extract raw brand after 'by '.
    """
    if "by" in text:
        try:
            return text.split("by ")[1].split(" ")[0]
        except Exception:
            return "Unknown"
    return "Unknown"


def split_camel_case(brand: str) -> str:
    """
    Fix glued brand strings like 'StradivariusThrow' -> 'Stradivarius'.
    """
    if not isinstance(brand, str):
        return brand

    match = re.match(r"([A-Z][a-z]+)", brand)
    if match:
        return match.group(1)

    return brand


def add_brand_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add brand extraction and cleaning columns.
    """
    df = df.copy()

    df["brand_raw"] = df["description"].apply(get_brand)
    df["brand_raw"] = df["brand_raw"].apply(split_camel_case)
    df["Brand"] = df["brand_raw"].map(BRAND_MAP).fillna(df["brand_raw"])

    return df


def filter_valid_brands(df: pd.DataFrame, min_count: int = 5) -> pd.DataFrame:
    """
    Keep only brands with enough occurrences.
    """
    brand_counts = df["Brand"].value_counts()
    valid_brands = brand_counts[brand_counts > min_count].index
    return df[df["Brand"].isin(valid_brands)].copy()


def calculate_stockout_metrics(size_str):
    """
    Calculate stockout count and stockout rate from size availability string.
    """
    if not isinstance(size_str, str):
        return 0, 0.0

    sizes = size_str.split(",")
    total_sizes = len(sizes)
    out_of_stock_count = size_str.count("Out of stock")
    rate = out_of_stock_count / total_sizes if total_sizes > 0 else 0.0

    return out_of_stock_count, rate


def add_stockout_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add stockout_count, stockout_rate, and lost_revenue columns.
    """
    df = df.copy()

    metrics = df["size"].apply(calculate_stockout_metrics)
    df["Stockout_count"] = [x[0] for x in metrics]
    df["Stockout_rate"] = [x[1] for x in metrics]
    df["Lost_revenue"] = df["price"] * df["Stockout_count"]

    return df


def save_processed_data(df: pd.DataFrame, csv_path: str, json_path: str) -> None:
    """
    Save processed dataset to CSV and JSON.
    """
    csv_file = Path(csv_path)
    json_file = Path(json_path)

    csv_file.parent.mkdir(parents=True, exist_ok=True)
    json_file.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(csv_file, index=False)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2)