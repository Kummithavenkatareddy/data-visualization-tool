"""
Unit tests for validators module.
"""

import pytest
import pandas as pd

from data_visualization.validators import (
    validate_dataset_not_empty,
    validate_columns_exist,
    validate_numeric_column,
    validate_chart_config,
    ValidationError,
)


@pytest.fixture
def sample_df():
    """Fixture providing a standard test DataFrame."""
    return pd.DataFrame({
        "Category": ["A", "B", "C", "D"],
        "Sales": [100.0, 200.5, 150.0, 300.0],
        "Units": [10, 20, 15, 30],
        "TextCol": ["X", "Y", "Z", "W"],
    })


def test_validate_dataset_not_empty_success(sample_df):
    """Test valid non-empty dataset validation."""
    validate_dataset_not_empty(sample_df)


def test_validate_dataset_not_empty_raises():
    """Test empty dataset validation raises ValidationError."""
    with pytest.raises(ValidationError, match="empty"):
        validate_dataset_not_empty(pd.DataFrame())

    with pytest.raises(ValidationError, match="No dataset loaded"):
        validate_dataset_not_empty(None)


def test_column_validation_success(sample_df):
    """Test column existence validation passes when columns exist."""
    validate_columns_exist(sample_df, ["Category", "Sales"])
    validate_columns_exist(sample_df, ["Sales", None])


def test_column_validation_missing(sample_df):
    """Test column validation raises error when column is missing."""
    with pytest.raises(ValidationError, match=r"Selected column\(s\) not found"):
        validate_columns_exist(sample_df, ["Sales", "NonExistentCol"])


def test_numeric_column_validation_success(sample_df):
    """Test numeric column validation passes for int/float columns."""
    validate_numeric_column(sample_df, "Sales")
    validate_numeric_column(sample_df, "Units")


def test_numeric_column_validation_failure(sample_df):
    """Test numeric column validation fails for string columns."""
    with pytest.raises(ValidationError, match="must be numeric"):
        validate_numeric_column(sample_df, "Category")


def test_validate_chart_config_scatter(sample_df):
    """Test scatter chart config validation."""
    # Valid
    validate_chart_config("scatter", sample_df, x_col="Category", y_col="Sales", color_col="TextCol")
    
    # Missing required Y-axis
    with pytest.raises(ValidationError, match="requires both an X-axis and a Y-axis"):
        validate_chart_config("scatter", sample_df, x_col="Category", y_col=None)

    # Non-numeric Y-axis
    with pytest.raises(ValidationError, match="must be numeric"):
        validate_chart_config("scatter", sample_df, x_col="Sales", y_col="Category")


def test_validate_chart_config_line(sample_df):
    """Test line chart config validation."""
    validate_chart_config("line", sample_df, x_col="Category", y_col="Sales")
    
    with pytest.raises(ValidationError, match="requires both an X-axis and a Y-axis"):
        validate_chart_config("line", sample_df, x_col=None, y_col="Sales")


def test_validate_chart_config_bar(sample_df):
    """Test bar chart config validation."""
    validate_chart_config("bar", sample_df, x_col="Category", y_col="Sales")

    with pytest.raises(ValidationError, match="must be numeric"):
        validate_chart_config("bar", sample_df, x_col="Sales", y_col="TextCol")


def test_validate_chart_config_histogram(sample_df):
    """Test histogram config validation."""
    validate_chart_config("histogram", sample_df, numeric_col="Sales")

    with pytest.raises(ValidationError, match="Histogram requires a numeric column"):
        validate_chart_config("histogram", sample_df, numeric_col=None)

    with pytest.raises(ValidationError, match="must be numeric"):
        validate_chart_config("histogram", sample_df, numeric_col="Category")


def test_validate_chart_config_box(sample_df):
    """Test box plot config validation."""
    validate_chart_config("box", sample_df, numeric_col="Sales", category_col="Category")

    with pytest.raises(ValidationError, match="Box plot requires a numeric column"):
        validate_chart_config("box", sample_df, numeric_col=None)


def test_validate_chart_config_pie(sample_df):
    """Test pie chart config validation."""
    validate_chart_config("pie", sample_df, names_col="Category", values_col="Sales")

    with pytest.raises(ValidationError, match="Pie chart requires both a Category column"):
        validate_chart_config("pie", sample_df, names_col="Category", values_col=None)


def test_invalid_chart_type(sample_df):
    """Test invalid chart type name raises ValidationError."""
    with pytest.raises(ValidationError, match="Unsupported chart type"):
        validate_chart_config("invalid_chart_type", sample_df, x_col="Category", y_col="Sales")
