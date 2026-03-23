import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """
    Load the ASOS dataset.
    """
    return pd.read_csv(path, on_bad_lines="skip", engine="python")