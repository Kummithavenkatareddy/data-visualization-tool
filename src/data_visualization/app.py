"""
Streamlit Web Application for interactive dataset preview, metadata inspection,
and dynamic Plotly chart visualization.
"""

import streamlit as st
import pandas as pd

from data_visualization.data_loader import (
    load_csv,
    get_dataset_metadata,
    load_sample_dataset,
    DataLoaderError,
)
from data_visualization.validators import (
    validate_dataset_not_empty,
    ValidationError,
)
from data_visualization.charts import generate_chart
from data_visualization.utils import (
    get_all_columns,
    get_numeric_columns,
    get_categorical_columns,
    sanitize_column_options,
)


def _render_dataframe(df: pd.DataFrame) -> None:
    """Helper to render DataFrame across Streamlit versions without deprecation warnings."""
    try:
        st.dataframe(df, width="stretch")
    except (TypeError, ValueError):
        st.dataframe(df, use_container_width=True)


def _render_plotly_chart(fig) -> None:
    """Helper to render Plotly chart across Streamlit versions without deprecation warnings."""
    try:
        st.plotly_chart(fig, width="stretch")
    except (TypeError, ValueError):
        st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    """Main function initializing the Streamlit User Interface."""
    st.set_page_config(
        page_title="Data Visualization Tool",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("📊 Data Visualization Tool")
    st.markdown(
        "Upload any CSV dataset or explore the built-in sample data. "
        "Inspect metadata and interactively create customizable Plotly charts."
    )

    st.sidebar.header("📁 Data Source Selection")
    data_source = st.sidebar.radio(
        "Choose Data Input Method:",
        options=["Use Built-in Sample Dataset", "Upload Custom CSV File"],
        index=0,
    )

    df: pd.DataFrame = None

    try:
        if data_source == "Use Built-in Sample Dataset":
            df = load_sample_dataset()
            st.sidebar.success("Loaded sample dataset successfully!")
        else:
            uploaded_file = st.sidebar.file_uploader(
                "Upload a CSV file",
                type=["csv"],
                help="Upload any valid CSV file to begin analysis.",
            )
            if uploaded_file is not None:
                df = load_csv(uploaded_file)
                st.sidebar.success("CSV file loaded successfully!")
            else:
                st.info("👈 Please upload a CSV file in the sidebar or switch to the sample dataset to proceed.")
                st.stop()

    except (DataLoaderError, ValidationError) as err:
        st.error(f"⚠️ Data Loading Error: {str(err)}")
        st.stop()
    except Exception as err:
        st.error(f"⚠️ Unexpected Error loading dataset: {str(err)}")
        st.stop()

    if df is None or df.empty:
        st.warning("The dataset is empty. Please upload or select a valid dataset.")
        st.stop()

    # Dataset Metadata Extraction
    metadata = get_dataset_metadata(df)

    # Dataset Overview & Metadata Section
    with st.expander("🔍 Dataset Overview & Metadata", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Rows", f"{metadata['row_count']:,}")
        col2.metric("Total Columns", f"{metadata['column_count']:,}")
        col3.metric("Numeric Columns", len(get_numeric_columns(df)))
        col4.metric("Total Missing Values", f"{metadata['missing_total']:,}")

        tab1, tab2 = st.tabs(["📋 Data Preview", "ℹ️ Metadata & Column Details"])

        with tab1:
            st.markdown("**First 10 rows of the dataset:**")
            _render_dataframe(df.head(10))

        with tab2:
            st.markdown("**Column Schema & Missing Values:**")
            meta_df = pd.DataFrame({
                "Column Name": metadata["column_names"],
                "Data Type": [metadata["data_types"][c] for c in metadata["column_names"]],
                "Missing Values": [metadata["missing_values"][c] for c in metadata["column_names"]],
                "Missing (%)": [
                    f"{(metadata['missing_values'][c] / metadata['row_count']) * 100:.1f}%"
                    if metadata["row_count"] > 0 else "0%"
                    for c in metadata["column_names"]
                ]
            })
            _render_dataframe(meta_df)

    st.markdown("---")
    st.header("📈 Interactive Visualization Studio")

    st.sidebar.header("🎨 Visualization Controls")
    chart_type = st.sidebar.selectbox(
        "Select Chart Type:",
        options=["Scatter Plot", "Line Chart", "Bar Chart", "Histogram", "Box Plot", "Pie Chart"],
        index=0,
    )

    all_cols = get_all_columns(df)
    num_cols = get_numeric_columns(df)
    cat_cols = get_categorical_columns(df)

    chart_kwargs = {}

    st.sidebar.subheader(f"⚙️ Config for {chart_type}")

    none_label = "-- None --"

    try:
        if chart_type == "Scatter Plot":
            x_col = st.sidebar.selectbox("X-Axis (Required)", options=all_cols, index=0 if all_cols else 0)
            default_y_idx = 1 if len(num_cols) > 1 else 0
            y_col = st.sidebar.selectbox("Y-Axis (Required, Numeric)", options=num_cols if num_cols else all_cols, index=default_y_idx if num_cols else 0)
            
            color_opts = sanitize_column_options(all_cols, include_none=True, none_label=none_label)
            color_selection = st.sidebar.selectbox("Color Grouping (Optional)", options=color_opts, index=0)
            
            chart_kwargs["x_col"] = x_col
            chart_kwargs["y_col"] = y_col
            chart_kwargs["color_col"] = None if color_selection == none_label else color_selection

        elif chart_type == "Line Chart":
            x_col = st.sidebar.selectbox("X-Axis (Required)", options=all_cols, index=0 if all_cols else 0)
            default_y_idx = 1 if len(num_cols) > 1 else 0
            y_col = st.sidebar.selectbox("Y-Axis (Required, Numeric)", options=num_cols if num_cols else all_cols, index=default_y_idx if num_cols else 0)
            
            color_opts = sanitize_column_options(all_cols, include_none=True, none_label=none_label)
            color_selection = st.sidebar.selectbox("Color Grouping (Optional)", options=color_opts, index=0)

            chart_kwargs["x_col"] = x_col
            chart_kwargs["y_col"] = y_col
            chart_kwargs["color_col"] = None if color_selection == none_label else color_selection

        elif chart_type == "Bar Chart":
            x_col = st.sidebar.selectbox("Category / X-Axis (Required)", options=all_cols, index=0 if all_cols else 0)
            y_col = st.sidebar.selectbox("Value / Y-Axis (Required, Numeric)", options=num_cols if num_cols else all_cols, index=0)
            
            color_opts = sanitize_column_options(all_cols, include_none=True, none_label=none_label)
            color_selection = st.sidebar.selectbox("Color Grouping (Optional)", options=color_opts, index=0)

            chart_kwargs["x_col"] = x_col
            chart_kwargs["y_col"] = y_col
            chart_kwargs["color_col"] = None if color_selection == none_label else color_selection

        elif chart_type == "Histogram":
            numeric_col = st.sidebar.selectbox("Numeric Column (Required)", options=num_cols if num_cols else all_cols, index=0)
            color_opts = sanitize_column_options(all_cols, include_none=True, none_label=none_label)
            color_selection = st.sidebar.selectbox("Color Grouping (Optional)", options=color_opts, index=0)
            nbins = st.sidebar.slider("Number of Bins (Optional)", min_value=5, max_value=100, value=20, step=5)

            chart_kwargs["numeric_col"] = numeric_col
            chart_kwargs["color_col"] = None if color_selection == none_label else color_selection
            chart_kwargs["nbins"] = nbins

        elif chart_type == "Box Plot":
            numeric_col = st.sidebar.selectbox("Numeric Column (Required)", options=num_cols if num_cols else all_cols, index=0)
            cat_opts = sanitize_column_options(all_cols, include_none=True, none_label=none_label)
            cat_selection = st.sidebar.selectbox("Category Grouping (Optional)", options=cat_opts, index=0)
            color_selection = st.sidebar.selectbox("Color Grouping (Optional)", options=cat_opts, index=0)

            chart_kwargs["numeric_col"] = numeric_col
            chart_kwargs["category_col"] = None if cat_selection == none_label else cat_selection
            chart_kwargs["color_col"] = None if color_selection == none_label else color_selection

        elif chart_type == "Pie Chart":
            names_col = st.sidebar.selectbox("Category Column (Required)", options=all_cols, index=0 if all_cols else 0)
            values_col = st.sidebar.selectbox("Numeric Values Column (Required)", options=num_cols if num_cols else all_cols, index=0)

            chart_kwargs["names_col"] = names_col
            chart_kwargs["values_col"] = values_col

        # Map display name to chart type string identifier
        chart_type_map = {
            "Scatter Plot": "scatter",
            "Line Chart": "line",
            "Bar Chart": "bar",
            "Histogram": "histogram",
            "Box Plot": "box",
            "Pie Chart": "pie",
        }
        normalized_chart_type = chart_type_map[chart_type]

        # Generate and render Plotly chart
        fig = generate_chart(normalized_chart_type, df, **chart_kwargs)
        _render_plotly_chart(fig)

    except ValidationError as err:
        st.error(f"❌ Configuration Error: {str(err)}")
    except Exception as err:
        st.error(f"❌ Error generating visualization: {str(err)}")


if __name__ == "__main__":
    main()
