# Developer Guide

This document provides setup instructions, workflow guidelines, testing protocols, and contribution standards for developers working on the **Data Visualization Tool**.

---

## 1. Development Environment Setup

### Prerequisites
- **Python**: Version 3.11 or higher
- **Git**: Installed and configured
- **Virtual Environment Tool**: `venv` (standard library)

### Step-by-Step Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd data-visualization-tool
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate Virtual Environment**:
   - **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Editable Package with Development Dependencies**:
   ```bash
   python -m pip install -e ".[dev]"
   ```

---

## 2. Running the Application

To launch the Streamlit app during development:

```bash
python -m streamlit run src/data_visualization/app.py
```

Streamlit's auto-reload functionality automatically refreshes the browser when modifications to `app.py` or imported package modules are saved.

---

## 3. Running Automated Tests

Run the complete pytest test suite:

```bash
python -m pytest
```

### Useful Pytest Flags

- **Verbose Mode**:
  ```bash
  python -m pytest -v
  ```
- **Stop on First Failure**:
  ```bash
  python -m pytest -x
  ```
- **Run Specific Test File**:
  ```bash
  python -m pytest tests/test_charts.py
  ```
- **Run Specific Test Function**:
  ```bash
  python -m pytest tests/test_charts.py -k "test_scatter_plot_generation"
  ```

---

## 4. Code Quality & Style Guidelines

- **PEP 8 Compliance**: Follow standard Python code layout and naming conventions.
- **Type Hints**: Annotate function parameters and return values.
- **Docstrings**: Provide clear Google-style docstrings for all public modules, functions, and classes.
- **Clean Architecture**: Do not import Streamlit in backend modules (`data_loader.py`, `validators.py`, `charts.py`). Keep UI code isolated to `app.py`.

---

## 5. Adding a New Visualization

Follow these steps to add a new chart type (e.g., `Heatmap`):

1. **Add Validation Rule (`src/data_visualization/validators.py`)**:
   Add support in `validate_chart_config()` to check required parameters (e.g., numeric X and Y axes for correlation/heatmap).

2. **Implement Builder Function (`src/data_visualization/charts.py`)**:
   ```python
   def create_heatmap(df: pd.DataFrame, title: Optional[str] = None) -> go.Figure:
       numeric_df = df.select_dtypes(include=["number"])
       corr = numeric_df.corr()
       fig = px.imshow(corr, text_auto=True, title=title or "Correlation Heatmap")
       return _apply_common_layout(fig, title or "Correlation Heatmap")
   ```

3. **Update Dispatcher (`src/data_visualization/charts.py`)**:
   Add `"heatmap"` handling in `generate_chart()`.

4. **Update Streamlit UI (`src/data_visualization/app.py`)**:
   Add `"Heatmap"` option to the sidebar chart selectbox and specify its controls.

5. **Write Tests (`tests/test_charts.py`)**:
   Add unit tests verifying that the new builder returns a valid `plotly.graph_objects.Figure`.

---

## 6. Troubleshooting

### Issue: Package Imports Not Recognized
- **Symptom**: `ModuleNotFoundError: No module named 'data_visualization'`
- **Fix**: Re-run editable installation:
  ```bash
  python -m pip install -e ".[dev]"
  ```

### Issue: Streamlit Fails to Start
- **Symptom**: `streamlit: command not found`
- **Fix**: Ensure your virtual environment is activated (`.venv\Scripts\Activate.ps1` or `source .venv/bin/activate`).

### Issue: Pytest Does Not Discover Tests
- **Fix**: Ensure pytest is run from the project root directory where `pyproject.toml` is located.
