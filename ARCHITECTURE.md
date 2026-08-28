# Architecture Specification

This document details the architectural design, component responsibilities, data flow, error handling strategy, and extension points of the **Data Visualization Tool**.

---

## 1. Overall Architecture

The application adopts a **layered modular design** with strict separation of concerns between data loading, domain validation, chart rendering, and the user interface.

```
+-----------------------------------------------------------------------+
|                           Streamlit UI Layer                          |
|                     (src/data_visualization/app.py)                   |
+-----------------------------------+-----------------------------------+
                                    |
          +-------------------------+-------------------------+
          |                                                   |
          v                                                   v
+-------------------------------+           +-------------------------------+
|       Data Loader Layer       |           |      Validation Engine        |
| (data_loader.py / utils.py)   |           |        (validators.py)        |
+---------------+---------------+           +---------------+---------------+
                |                                           |
                +-------------------+-----------------------+
                                    |
                                    v
                        +-----------------------+
                        |   Chart Engine        |
                        |      (charts.py)      |
                        +-----------+-----------+
                                    |
                                    v
                        +-----------------------+
                        |  Plotly Figure Object |
                        +-----------------------+
```

---

## 2. Component Responsibilities

### `src/data_visualization/app.py` (UI Layer)
- Serves as the Streamlit user interface entry point.
- Renders layout components: header, sidebar controls, metric cards, dataset preview, and chart canvas.
- Manages user selections and passes inputs down to data loader and chart generation layers.
- Intercepts domain errors (`DataLoaderError`, `ValidationError`) and renders friendly UI alerts without exposing raw tracebacks.

### `src/data_visualization/data_loader.py` (Data Layer)
- Encapsulates file I/O operations for CSV parsing.
- Handles string paths, Path objects, and Streamlit `UploadedFile` streams.
- Computes dataset metadata metrics (row count, column count, schema, missing values).
- Provides safe access to the built-in sample dataset.

### `src/data_visualization/validators.py` (Validation Layer)
- Enforces data integrity and visualization prerequisites.
- Validates dataset non-emptiness, column existence, and numeric data type requirements.
- Raises descriptive `ValidationError` exceptions for incompatible user selections.

### `src/data_visualization/charts.py` (Visualization Layer)
- Contains pure chart builder functions returning `plotly.graph_objects.Figure` instances.
- Applies consistent aesthetic styling and interactive layout properties.
- Free of any UI framework (Streamlit) dependencies, ensuring clean testability.

### `src/data_visualization/utils.py` (Utility Layer)
- Offers helper routines for classifying dataframe columns (numeric vs categorical).
- Prepares sanitized dropdown options for Streamlit controls.

---

## 3. Data Flow

```
1. User Selects Data Input (Sample CSV or Uploaded File)
   ↓
2. data_loader.load_csv() parses raw CSV into Pandas DataFrame
   ↓
3. data_loader.get_dataset_metadata() extracts row/col metrics & schemas
   ↓
4. UI displays preview table & metadata cards
   ↓
5. User selects chart type & config options in sidebar
   ↓
6. validators.validate_chart_config() validates choices & dtypes
   ↓ (If invalid: raises ValidationError → UI displays st.error)
7. charts.generate_chart() constructs Plotly Figure
   ↓
8. app.py renders Plotly Figure interactively via st.plotly_chart()
```

---

## 4. Relationship Between Key Technologies

- **Pandas**: Functions as the core data representation layer (`pd.DataFrame`). All data parsing, metadata calculations, and type checks rely on Pandas.
- **Validators**: Acts as a bridge between user selections and plotting logic, verifying that the Pandas DataFrame satisfies the mathematical requirements of the chosen chart.
- **Plotly**: Transforms Pandas DataFrames into interactive SVG/WebGL `Figure` objects.
- **Streamlit**: Acts strictly as the user interface presentation layer. It collects user input, invokes backend modules, and displays resulting figures and metrics.

---

## 5. Error Handling Strategy

1. **No Raw Tracebacks**: All application boundaries catch operational exceptions and display clear user guidance (`st.error`).
2. **Custom Exceptions**:
   - `DataLoaderError`: Raised for missing files, empty CSVs, or encoding/parse errors.
   - `ValidationError`: Raised for missing columns, non-numeric column selections where numeric data is required, or empty datasets.
3. **Graceful Degradation**: Invalid chart configurations display warning banners encouraging the user to adjust sidebar inputs rather than crashing the session.

---

## 6. Testing Architecture

The test suite is built using `pytest` and structured parallel to the source code:

- **`tests/test_data_loader.py`**: Verifies CSV loading under valid, invalid, empty, and file-stream conditions.
- **`tests/test_validators.py`**: Verifies non-empty dataframe validation, missing column validation, numeric type enforcement, and chart configuration rules.
- **`tests/test_charts.py`**: Verifies that every chart creation function returns valid `plotly.graph_objects.Figure` objects with expected data traces.

---

## 7. Extension Points: Adding New Chart Types

To add a new visualization (e.g., `Violin Plot`):

1. **Add validation rules** in `src/data_visualization/validators.py`:
   - Extend `validate_chart_config` to recognize `"violin"` and validate its required columns (e.g., numeric column, optional category).

2. **Add builder function** in `src/data_visualization/charts.py`:
   - Define `create_violin_plot(df, numeric_col, category_col=None, title=None) -> go.Figure`.
   - Update `generate_chart()` dispatch logic.

3. **Add UI controls** in `src/data_visualization/app.py`:
   - Add `"Violin Plot"` to the chart selector dropdown and specify its input widgets.

4. **Add unit tests** in `tests/test_charts.py` and `tests/test_validators.py`.
