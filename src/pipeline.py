from src.analysis import compute_brand_strategy, save_brand_strategy
from src.data_loader import load_data
from src.preprocessing import (
    add_brand_features,
    add_stockout_features,
    clean_data,
    filter_valid_brands,
    save_processed_data,
)
from src.visualization import plot_brand_strategy_dashboard

# Orchestrates full data workflow:
# ingestion → preprocessing → feature engineering → analysis → visualization

def run_pipeline() -> None:
    # 1. Load data
    df = load_data("data/products_asos.csv")

    # 2. Clean and preprocess
    df = clean_data(df)
    df = add_brand_features(df)
    df = filter_valid_brands(df, min_count=5)
    df = add_stockout_features(df)

    # 3. Save processed outputs
    save_processed_data(
        df,
        "outputs/processed/asos_cleaned_data.csv",
        "outputs/processed/asos_cleaned_data.json",
    )

    # 4. Brand strategy analysis
    brand_strategy = compute_brand_strategy(df, min_products=10)

    save_brand_strategy(
        brand_strategy,
        "outputs/processed/brand_strategy.csv",
    )

    # 5. Dashboard visualization
    plot_brand_strategy_dashboard(
        brand_strategy,
        "outputs/plots/brand_strategy_dashboard.png",
    )

    print("Pipeline executed successfully.")
    print(f"Processed dataset rows: {len(df)}")
    print(f"Brand strategy rows: {len(brand_strategy)}")