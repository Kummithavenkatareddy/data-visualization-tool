"""
Unit tests for charts module.
"""

import pytest
import pandas as pd
import plotly.graph_objects as go

from data_visualization.charts import (
    create_scatter_plot,
    create_line_chart,
    create_bar_chart,
    create_histogram,
    create_box_plot,
    create_pie_chart,
    generate_chart,
)
from data_visualization.validators import ValidationError


@pytest.fixture
def sample_df():
    """Fixture providing a standard test DataFrame."""
    return pd.DataFrame({
        "Category": ["Electronics", "Furniture", "Office Supplies", "Electronics"],
        "Sales": [1200.5, 250.0, 45.0, 650.0],
        "Units": [5, 10, 25, 4],
        "Region": ["North", "South", "East", "West"]
    })


def test_scatter_plot_generation(sample_df):
    """Test scatter plot generation returns Plotly Figure with scatter trace."""
    fig = create_scatter_plot(sample_df, x_col="Units", y_col="Sales", color_col="Region")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
    assert fig.data[0].type == "scatter"
    assert fig.data[0].mode == "markers"


def test_line_chart_generation(sample_df):
    """Test line chart generation returns Plotly Figure with line trace."""
    fig = create_line_chart(sample_df, x_col="Category", y_col="Sales", color_col="Region")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
    assert fig.data[0].type == "scatter"
    assert "lines" in fig.data[0].mode


def test_bar_chart_generation(sample_df):
    """Test bar chart generation returns Plotly Figure with bar trace."""
    fig = create_bar_chart(sample_df, x_col="Category", y_col="Sales", color_col="Region")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
    assert fig.data[0].type == "bar"


def test_histogram_generation(sample_df):
    """Test histogram generation returns Plotly Figure with histogram trace."""
    fig = create_histogram(sample_df, numeric_col="Sales", color_col="Region", nbins=10)
    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
    # First trace is histogram (with optional marginal box trace)
    trace_types = [trace.type for trace in fig.data]
    assert "histogram" in trace_types


def test_box_plot_generation(sample_df):
    """Test box plot generation returns Plotly Figure with box trace."""
    fig = create_box_plot(sample_df, numeric_col="Sales", category_col="Category")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
    assert fig.data[0].type == "box"


def test_pie_chart_generation(sample_df):
    """Test pie chart generation returns Plotly Figure with pie trace."""
    fig = create_pie_chart(sample_df, names_col="Category", values_col="Sales")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].type == "pie"


def test_generate_chart_universal_launcher(sample_df):
    """Test generate_chart universal interface for all chart types."""
    fig_scatter = generate_chart("scatter", sample_df, x_col="Units", y_col="Sales")
    assert isinstance(fig_scatter, go.Figure)

    fig_line = generate_chart("line", sample_df, x_col="Category", y_col="Sales")
    assert isinstance(fig_line, go.Figure)

    fig_bar = generate_chart("bar", sample_df, x_col="Category", y_col="Sales")
    assert isinstance(fig_bar, go.Figure)

    fig_hist = generate_chart("histogram", sample_df, numeric_col="Sales")
    assert isinstance(fig_hist, go.Figure)

    fig_box = generate_chart("box", sample_df, numeric_col="Sales")
    assert isinstance(fig_box, go.Figure)

    fig_pie = generate_chart("pie", sample_df, names_col="Category", values_col="Sales")
    assert isinstance(fig_pie, go.Figure)


def test_invalid_visualization_configuration_handling(sample_df):
    """Test invalid visualization configuration raises ValidationError in generate_chart."""
    # Missing required X-axis for scatter
    with pytest.raises(ValidationError, match="requires both an X-axis and a Y-axis"):
        generate_chart("scatter", sample_df, x_col=None, y_col="Sales")

    # Non-numeric column for histogram
    with pytest.raises(ValidationError, match="must be numeric"):
        generate_chart("histogram", sample_df, numeric_col="Category")

    # Non-existent chart type
    with pytest.raises(ValidationError, match="Unsupported chart type"):
        generate_chart("radar_chart", sample_df, x_col="Category", y_col="Sales")
