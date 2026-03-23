import pandas as pd

from src.preprocessing import calculate_stockout_metrics, clean_data, get_brand, split_camel_case


def test_clean_data_removes_missing_price():
    df = pd.DataFrame(
        {
            "price": ["10.5", None, "20"],
            "description": ["Dress by New Look", "Skirt by River Island", "Top by Miss Selfridge"],
        }
    )
    cleaned = clean_data(df)
    assert cleaned["price"].isnull().sum() == 0


def test_get_brand_extracts_first_token_after_by():
    text = "Dress by New Look in floral print"
    brand = get_brand(text)
    assert brand == "New"


def test_split_camel_case():
    assert split_camel_case("StradivariusThrow") == "Stradivarius"


def test_calculate_stockout_metrics():
    size_str = "UK 6, UK 8 - Out of stock, UK 10 - Out of stock"
    count, rate = calculate_stockout_metrics(size_str)
    assert count == 2
    assert rate > 0