"""
Data and configuration validation module for visualization inputs.
"""

from typing import Any, List, Optional
import pandas as pd


class ValidationError(Exception):
    """Custom exception raised when dataset or chart validation fails."""
    pass


def validate_dataset_not_empty(df: Optional[pd.DataFrame]) -> None:
    """
    Validate that the DataFrame is not None and not empty.

    Args:
        df: Pandas DataFrame to validate.

    Raises:
        ValidationError: If df is None or has 0 rows or 0 columns.
    """
    if df is None:
        raise ValidationError("No dataset loaded. Please upload or select a dataset.")
    if df.empty or len(df.columns) == 0:
        raise ValidationError("The loaded dataset is empty. Please select a non-empty dataset.")


def validate_columns_exist(df: pd.DataFrame, columns: List[Optional[str]]) -> None:
    """
    Validate that all specified column names exist in the DataFrame.

    Args:
        df: Pandas DataFrame.
        columns: List of column names to check (None values are ignored).

    Raises:
        ValidationError: If any specified column is missing from df.
    """
    validate_dataset_not_empty(df)
    missing = [col for col in columns if col is not None and col not in df.columns]
    if missing:
        missing_str = ", ".join(f"'{col}'" for col in missing)
        raise ValidationError(f"Selected column(s) not found in dataset: {missing_str}")


def validate_numeric_column(df: pd.DataFrame, column_name: str) -> None:
    """
    Validate that a specific column exists and contains numeric data.

    Args:
        df: Pandas DataFrame.
        column_name: Name of column to check.

    Raises:
        ValidationError: If column does not exist or is not numeric.
    """
    validate_columns_exist(df, [column_name])
    if not pd.api.types.is_numeric_dtype(df[column_name]):
        raise ValidationError(
            f"Column '{column_name}' must be numeric for this visualization. "
            f"Current data type is '{df[column_name].dtype}'."
        )


def validate_chart_config(chart_type: str, df: pd.DataFrame, **kwargs: Any) -> None:
    """
    Validate configuration parameters for a specified chart type.

    Args:
        chart_type: Name of chart type ('scatter', 'line', 'bar', 'histogram', 'box', 'pie').
        df: Pandas DataFrame.
        **kwargs: Chart-specific arguments.

    Raises:
        ValidationError: If required selections are missing or invalid.
    """
    validate_dataset_not_empty(df)

    normalized_type = chart_type.lower().strip()
    supported_charts = ["scatter", "line", "bar", "histogram", "box", "pie"]

    if normalized_type not in supported_charts:
        raise ValidationError(
            f"Unsupported chart type '{chart_type}'. "
            f"Supported chart types are: {', '.join(supported_charts)}."
        )

    if normalized_type == "scatter":
        x_col = kwargs.get("x_col")
        y_col = kwargs.get("y_col")
        color_col = kwargs.get("color_col")
        if not x_col or not y_col:
            raise ValidationError("Scatter plot requires both an X-axis and a Y-axis selection.")
        validate_columns_exist(df, [x_col, y_col, color_col])
        validate_numeric_column(df, y_col)

    elif normalized_type == "line":
        x_col = kwargs.get("x_col")
        y_col = kwargs.get("y_col")
        color_col = kwargs.get("color_col")
        if not x_col or not y_col:
            raise ValidationError("Line chart requires both an X-axis and a Y-axis selection.")
        validate_columns_exist(df, [x_col, y_col, color_col])
        validate_numeric_column(df, y_col)

    elif normalized_type == "bar":
        x_col = kwargs.get("x_col")
        y_col = kwargs.get("y_col")
        color_col = kwargs.get("color_col")
        if not x_col or not y_col:
            raise ValidationError("Bar chart requires both an X-axis (category) and a Y-axis (value) selection.")
        validate_columns_exist(df, [x_col, y_col, color_col])
        validate_numeric_column(df, y_col)

    elif normalized_type == "histogram":
        numeric_col = kwargs.get("numeric_col")
        color_col = kwargs.get("color_col")
        if not numeric_col:
            raise ValidationError("Histogram requires a numeric column selection.")
        validate_columns_exist(df, [numeric_col, color_col])
        validate_numeric_column(df, numeric_col)

    elif normalized_type == "box":
        numeric_col = kwargs.get("numeric_col")
        category_col = kwargs.get("category_col")
        color_col = kwargs.get("color_col")
        if not numeric_col:
            raise ValidationError("Box plot requires a numeric column selection.")
        validate_columns_exist(df, [numeric_col, category_col, color_col])
        validate_numeric_column(df, numeric_col)

    elif normalized_type == "pie":
        names_col = kwargs.get("names_col")
        values_col = kwargs.get("values_col")
        if not names_col or not values_col:
            raise ValidationError("Pie chart requires both a Category column and a Numeric Values column selection.")
        validate_columns_exist(df, [names_col, values_col])
        validate_numeric_column(df, values_col)
