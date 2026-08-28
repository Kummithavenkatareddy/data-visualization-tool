"""
Utility helper functions for data classification and formatting.
"""

from typing import List, Optional
import pandas as pd


def get_all_columns(df: pd.DataFrame) -> List[str]:
    """
    Get list of all column names from a DataFrame.

    Args:
        df: Pandas DataFrame.

    Returns:
        List[str]: List of column names.
    """
    if df is None or df.empty and len(df.columns) == 0:
        return []
    return list(df.columns)


def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """
    Get list of numeric column names from a DataFrame.

    Args:
        df: Pandas DataFrame.

    Returns:
        List[str]: List of numeric column names.
    """
    if df is None or df.empty and len(df.columns) == 0:
        return []
    return list(df.select_dtypes(include=["number"]).columns)


def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """
    Get list of non-numeric / categorical / object column names from a DataFrame.

    Args:
        df: Pandas DataFrame.

    Returns:
        List[str]: List of categorical column names.
    """
    if df is None or df.empty and len(df.columns) == 0:
        return []
    return list(df.select_dtypes(exclude=["number"]).columns)


def sanitize_column_options(columns: List[str], include_none: bool = True, none_label: str = "-- None --") -> List[Optional[str]]:
    """
    Prepare a dropdown option list with optional '-- None --' sentinel value.

    Args:
        columns: Original list of column names.
        include_none: Whether to prefix options with '-- None --'.
        none_label: String representation of the None option.

    Returns:
        List[Optional[str]]: Sanitized list of options.
    """
    opts = list(columns)
    if include_none:
        return [none_label] + opts
    return opts
