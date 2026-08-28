"""
Chart generation module using Plotly Express and Plotly Graph Objects.
"""

from typing import Any, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data_visualization.validators import validate_chart_config


def _apply_common_layout(fig: go.Figure, title: str) -> go.Figure:
    """
    Apply a consistent, modern visual theme and responsive layout to a Plotly figure.

    Args:
        fig: Plotly Figure instance.
        title: Chart title.

    Returns:
        go.Figure: Styled figure.
    """
    fig.update_layout(
        title={
            "text": title,
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 18, "family": "Arial, sans-serif"}
        },
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Arial, sans-serif"
        )
    )
    return fig


def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: Optional[str] = None,
    title: Optional[str] = None
) -> go.Figure:
    """
    Generate an interactive Scatter Plot.

    Args:
        df: Pandas DataFrame.
        x_col: Column name for X-axis.
        y_col: Column name for Y-axis.
        color_col: Optional column name for color grouping.
        title: Optional custom plot title.

    Returns:
        go.Figure: Interactive Plotly scatter plot figure.
    """
    chart_title = title or f"Scatter Plot: {y_col} vs {x_col}"
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        hover_data=df.columns,
        title=chart_title,
    )
    fig.update_traces(marker=dict(size=8, opacity=0.8))
    return _apply_common_layout(fig, chart_title)


def create_line_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: Optional[str] = None,
    title: Optional[str] = None
) -> go.Figure:
    """
    Generate an interactive Line Chart.

    Args:
        df: Pandas DataFrame.
        x_col: Column name for X-axis.
        y_col: Column name for Y-axis.
        color_col: Optional column name for color grouping.
        title: Optional custom plot title.

    Returns:
        go.Figure: Interactive Plotly line chart figure.
    """
    chart_title = title or f"Line Chart: {y_col} over {x_col}"
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        markers=True,
        title=chart_title,
    )
    return _apply_common_layout(fig, chart_title)


def create_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: Optional[str] = None,
    title: Optional[str] = None
) -> go.Figure:
    """
    Generate an interactive Bar Chart.

    Args:
        df: Pandas DataFrame.
        x_col: Column name for X-axis (categories).
        y_col: Column name for Y-axis (values).
        color_col: Optional column name for color grouping.
        title: Optional custom plot title.

    Returns:
        go.Figure: Interactive Plotly bar chart figure.
    """
    chart_title = title or f"Bar Chart: {y_col} by {x_col}"
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        barmode="group",
        title=chart_title,
    )
    return _apply_common_layout(fig, chart_title)


def create_histogram(
    df: pd.DataFrame,
    numeric_col: str,
    color_col: Optional[str] = None,
    nbins: Optional[int] = None,
    title: Optional[str] = None
) -> go.Figure:
    """
    Generate an interactive Histogram.

    Args:
        df: Pandas DataFrame.
        numeric_col: Column name for histogram distribution.
        color_col: Optional column name for color grouping.
        nbins: Optional number of bins.
        title: Optional custom plot title.

    Returns:
        go.Figure: Interactive Plotly histogram figure.
    """
    chart_title = title or f"Histogram Distribution: {numeric_col}"
    fig = px.histogram(
        df,
        x=numeric_col,
        color=color_col,
        nbins=nbins,
        marginal="box",
        title=chart_title,
    )
    return _apply_common_layout(fig, chart_title)


def create_box_plot(
    df: pd.DataFrame,
    numeric_col: str,
    category_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: Optional[str] = None
) -> go.Figure:
    """
    Generate an interactive Box Plot.

    Args:
        df: Pandas DataFrame.
        numeric_col: Column name for numeric values.
        category_col: Optional category column for grouping on X-axis.
        color_col: Optional column name for color grouping.
        title: Optional custom plot title.

    Returns:
        go.Figure: Interactive Plotly box plot figure.
    """
    chart_title = title or f"Box Plot: {numeric_col}"
    if category_col:
        chart_title += f" grouped by {category_col}"

    fig = px.box(
        df,
        x=category_col,
        y=numeric_col,
        color=color_col or category_col,
        points="all",
        title=chart_title,
    )
    return _apply_common_layout(fig, chart_title)


def create_pie_chart(
    df: pd.DataFrame,
    names_col: str,
    values_col: str,
    title: Optional[str] = None
) -> go.Figure:
    """
    Generate an interactive Pie Chart.

    Args:
        df: Pandas DataFrame.
        names_col: Column name for pie slices (category).
        values_col: Column name for slice proportions (numeric values).
        title: Optional custom plot title.

    Returns:
        go.Figure: Interactive Plotly pie chart figure.
    """
    chart_title = title or f"Pie Chart: {values_col} distribution by {names_col}"
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        hole=0.3,
        title=chart_title,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return _apply_common_layout(fig, chart_title)


def generate_chart(chart_type: str, df: pd.DataFrame, **kwargs: Any) -> go.Figure:
    """
    Validate inputs and generate the corresponding Plotly chart figure.

    Args:
        chart_type: Name of chart ('scatter', 'line', 'bar', 'histogram', 'box', 'pie').
        df: Pandas DataFrame.
        **kwargs: Chart-specific configuration options.

    Returns:
        go.Figure: Plotly Figure instance.

    Raises:
        ValidationError: If input selections are invalid or incompatible.
    """
    validate_chart_config(chart_type, df, **kwargs)

    normalized = chart_type.lower().strip()

    if normalized == "scatter":
        return create_scatter_plot(
            df,
            x_col=kwargs["x_col"],
            y_col=kwargs["y_col"],
            color_col=kwargs.get("color_col"),
            title=kwargs.get("title"),
        )
    elif normalized == "line":
        return create_line_chart(
            df,
            x_col=kwargs["x_col"],
            y_col=kwargs["y_col"],
            color_col=kwargs.get("color_col"),
            title=kwargs.get("title"),
        )
    elif normalized == "bar":
        return create_bar_chart(
            df,
            x_col=kwargs["x_col"],
            y_col=kwargs["y_col"],
            color_col=kwargs.get("color_col"),
            title=kwargs.get("title"),
        )
    elif normalized == "histogram":
        return create_histogram(
            df,
            numeric_col=kwargs["numeric_col"],
            color_col=kwargs.get("color_col"),
            nbins=kwargs.get("nbins"),
            title=kwargs.get("title"),
        )
    elif normalized == "box":
        return create_box_plot(
            df,
            numeric_col=kwargs["numeric_col"],
            category_col=kwargs.get("category_col"),
            color_col=kwargs.get("color_col"),
            title=kwargs.get("title"),
        )
    elif normalized == "pie":
        return create_pie_chart(
            df,
            names_col=kwargs["names_col"],
            values_col=kwargs["values_col"],
            title=kwargs.get("title"),
        )
    else:
        # Fallback unreachable due to validate_chart_config
        raise ValueError(f"Unknown chart type: '{chart_type}'")
