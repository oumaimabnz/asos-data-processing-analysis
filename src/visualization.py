from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns


def plot_brand_strategy_dashboard(brand_strategy, output_path: str) -> None:
    """
    Create a dashboard-style scatter plot.

    - X axis: average price
    - Y axis: stockout rate
    - Bubble size: lost revenue
    - Color: stockout rate intensity
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(14, 9))

    sns.scatterplot(
        data=brand_strategy,
        x="price",
        y="Stockout_rate",
        size="Lost_revenue",
        hue="Stockout_rate",
        palette="viridis",
        sizes=(60, 900),
        alpha=0.8,
        edgecolor="black",
        linewidth=0.5,
        ax=ax,
        legend="brief",
    )

    # Threshold lines
    ax.axvline(x=40, color="red", linestyle="--", linewidth=1.5, alpha=0.8)
    ax.axhline(y=0.4, color="red", linestyle="--", linewidth=1.5, alpha=0.8)

    # Highlight top brands by lost revenue
    top_brands = brand_strategy.nlargest(8, "Lost_revenue")

    for _, row in top_brands.iterrows():
        ax.annotate(
            row["Brand"],
            (row["price"], row["Stockout_rate"]),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=10,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.8),
        )

    # Titles and labels
    ax.set_title(
        "Brand Strategy Dashboard\nPrice vs Stockout Rate with Lost Revenue Impact",
        fontsize=16,
        fontweight="bold",
        pad=16,
    )
    ax.set_xlabel("Average Price", fontsize=12)
    ax.set_ylabel("Stockout Rate", fontsize=12)

    # Quadrant labels
    ax.text(115, 0.52, "High Price\nHigh Stockout", fontsize=11, fontweight="bold", alpha=0.7)
    ax.text(18, 0.52, "Low Price\nHigh Stockout", fontsize=11, fontweight="bold", alpha=0.7)
    ax.text(115, 0.05, "High Price\nLow Stockout", fontsize=11, fontweight="bold", alpha=0.7)
    ax.text(18, 0.05, "Low Price\nLow Stockout", fontsize=11, fontweight="bold", alpha=0.7)

    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()