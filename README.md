# Data Visualization Tool

An interactive, production-quality Python web application built with Streamlit, Pandas, Plotly, and pytest for dataset exploration and dynamic chart generation.

---

## Overview

The **Data Visualization Tool** allows users to load CSV datasets or explore built-in sample data, view comprehensive dataset metadata (row counts, column schemas, data types, missing value percentages), and dynamically generate interactive Plotly visualizations.

The tool provides full interactive control over chart configurations—dynamically enabling options relevant to the selected chart type—and offers hover tooltips, zoom, pan, legend toggling, and reset controls.

---

## Features

- **Flexible Data Input**: Upload custom CSV datasets or demonstrate features instantly using the built-in sample dataset.
- **Dataset Preview & Schema**: Preview the first 10 rows and inspect detailed column schemas, data types, and missing value counts.
- **Interactive Plotly Visualizations**:
  - Scatter Plot
  - Line Chart
  - Bar Chart
  - Histogram
  - Box Plot
  - Pie Chart
- **Dynamic Configuration Panel**: UI controls automatically adapt based on the selected visualization type.
- **Robust Error Handling**: Friendly error messages prevent raw Python tracebacks upon invalid file uploads or incompatible column selections.
- **Modular & Tested Architecture**: Clean separation between data loading, validation, chart generation, helper utilities, and the Streamlit frontend.

---

## Technology Stack

- **Python**: 3.11+
- **Data Manipulation**: Pandas
- **Interactive Plotting**: Plotly Express & Plotly Graph Objects
- **Web Application Framework**: Streamlit
- **Automated Testing**: pytest

---

## Project Structure

```
data-visualization-tool/
├── src/
│   └── data_visualization/
│       ├── __init__.py
│       ├── app.py            # Streamlit user interface entry point
│       ├── data_loader.py    # CSV reading and metadata extraction logic
│       ├── validators.py    # Input validation and schema rules
│       ├── charts.py        # Plotly chart generation functions
│       └── utils.py         # Helper utilities and data classifiers
├── tests/
│   ├── test_data_loader.py  # Tests for CSV loading & metadata
│   ├── test_validators.py   # Tests for input validation logic
│   └── test_charts.py       # Tests for chart generation & Plotly figures
├── data/
│   └── sample.csv           # Built-in sample CSV dataset
├── examples/
│   └── README.md            # Detailed sample dataset usage and workflows
├── README.md                # Main project documentation
├── ARCHITECTURE.md          # Architectural design & data flow specification
├── DEVELOPMENT.md          # Developer setup, testing, and contribution guide
├── pyproject.toml           # Package configuration & build metadata
├── .gitignore               # Ignored build and temporary files
└── LICENSE                  # MIT License
```

---

## Installation Instructions

1. **Clone or download the repository**:
   ```bash
   git clone <repository-url>
   cd data-visualization-tool
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   
   # On Windows (PowerShell):
   .venv\Scripts\Activate.ps1

   # On Linux / macOS:
   source .venv/bin/activate
   ```

3. **Install the package in editable mode with development dependencies**:
   ```bash
   python -m pip install -e ".[dev]"
   ```

---

## Usage Instructions & Launching Streamlit

Run the Streamlit application directly from the project root directory:

```bash
python -m streamlit run src/data_visualization/app.py
```

The application will start automatically and open in your default browser at `http://localhost:8501`.

---

## Supported Visualizations

| Chart Type | Required Inputs | Optional Inputs | Best Used For |
| :--- | :--- | :--- | :--- |
| **Scatter Plot** | X-Axis, Y-Axis (Numeric) | Color Grouping | Exploring correlations between two continuous variables |
| **Line Chart** | X-Axis, Y-Axis (Numeric) | Color Grouping | Tracking trends over time or ordered sequences |
| **Bar Chart** | Category (X-Axis), Value (Y-Axis Numeric) | Color Grouping | Comparing discrete categories |
| **Histogram** | Numeric Column | Color Grouping, Bin Count | Analyzing value distribution and skewness |
| **Box Plot** | Numeric Column | Category Grouping, Color Grouping | Outlier detection and quartile distribution comparison |
| **Pie Chart** | Category Column, Value Column (Numeric) | - | Visualizing relative proportions of a whole |

---

## Dataset Requirements

For custom CSV uploads, datasets should meet the following basic guidelines:
- Must be a valid CSV file with UTF-8 encoding.
- First row must contain unique column headers.
- Datasets must contain at least one row and one column.
- Numerical charts require at least one column formatted with valid numerical values (integers or floats).

---

## Example Workflow

1. Launch the application with `python -m streamlit run src/data_visualization/app.py`.
2. Keep **Use Built-in Sample Dataset** selected in the sidebar (or upload your own CSV file).
3. Expand **Dataset Overview & Metadata** to verify row counts, column data types, and missing value counts.
4. Under **Visualization Controls**, select **Scatter Plot**.
5. Set **X-Axis** to `Sales`, **Y-Axis** to `Profit`, and **Color Grouping** to `Category`.
6. Interact with the rendered Plotly chart by hovering over data points, zooming in on dense regions, toggling categories in the legend, or clicking the reset button.

---

## Testing Instructions

Execute the full automated pytest suite from the project root:

```bash
python -m pytest
```

To view verbose test execution details:

```bash
python -m pytest -v
```

---

## Example Output & Visual Interface Description

- **Sidebar Control Panel**: Features data input selection, file uploader widget, visualization selector dropdown, and dynamic parameters.
- **Metric Cards Display**: Highlights dataset dimensions (`Total Rows`, `Total Columns`, `Numeric Columns`, `Total Missing Values`) in cards at the top.
- **Interactive Plotly Canvas**: Renders high-resolution interactive charts with hover cards, pan/zoom tools, and legend controls.

---

## Limitations

- **Memory Constraints**: Large CSV files (>100MB) may take longer to parse or render depending on system RAM.
- **Automatic Type Conversion**: String columns containing numerical data are treated as categorical unless cleaned prior to upload.
- **Static File Inputs**: Supports CSV files only; Excel or JSON files require prior conversion to CSV format.

---

## Future Improvements

- Support for Excel (`.xlsx`), JSON, and Parquet file formats.
- Data transformation utilities (e.g., missing value imputation, log scaling, filtering).
- Advanced visualizations such as Heatmaps, Violin Plots, 3D Scatter plots, and Correlation Matrices.
- Export options for rendered visualizations (e.g., SVG, PNG, standalone HTML).
