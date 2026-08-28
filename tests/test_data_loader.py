"""
Unit tests for data_loader module.
"""

from io import StringIO
import tempfile
from pathlib import Path
import pytest
import pandas as pd

from data_visualization.data_loader import (
    load_csv,
    get_dataset_metadata,
    load_sample_dataset,
    DataLoaderError,
)


def test_successful_csv_loading_from_stringio():
    """Test loading valid CSV content from a StringIO stream."""
    csv_content = "Name,Age,Score\nAlice,30,95.5\nBob,25,88.0"
    file_obj = StringIO(csv_content)
    df = load_csv(file_obj)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["Name", "Age", "Score"]


def test_successful_csv_loading_from_file_path(tmp_path):
    """Test loading valid CSV from a temporary file path."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("Category,Values\nA,10\nB,20\n", encoding="utf-8")
    df = load_csv(csv_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert df.iloc[0]["Category"] == "A"


def test_load_sample_dataset():
    """Test loading built-in sample dataset."""
    df = load_sample_dataset()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "Category" in df.columns
    assert "Sales" in df.columns


def test_invalid_csv_handling_non_existent_file():
    """Test loading from a non-existent file path raises DataLoaderError."""
    with pytest.raises(DataLoaderError, match="File not found"):
        load_csv("non_existent_file_xyz_12345.csv")


def test_invalid_csv_handling_none_input():
    """Test passing None to load_csv raises DataLoaderError."""
    with pytest.raises(DataLoaderError, match="No file or file path provided"):
        load_csv(None)


def test_empty_dataset_handling_zero_bytes(tmp_path):
    """Test loading 0-byte CSV file raises DataLoaderError."""
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("", encoding="utf-8")
    with pytest.raises(DataLoaderError, match="empty"):
        load_csv(empty_file)


def test_empty_dataset_handling_header_only():
    """Test metadata extraction on header-only or empty DataFrame."""
    empty_df = pd.DataFrame(columns=["A", "B"])
    meta = get_dataset_metadata(empty_df)
    assert meta["row_count"] == 0
    assert meta["column_count"] == 2
    assert meta["column_names"] == ["A", "B"]


def test_get_dataset_metadata():
    """Test dataset metadata calculation."""
    data = {
        "Col1": [1, 2, None],
        "Col2": ["A", "B", "C"],
        "Col3": [1.1, None, 3.3]
    }
    df = pd.DataFrame(data)
    meta = get_dataset_metadata(df)
    
    assert meta["row_count"] == 3
    assert meta["column_count"] == 3
    assert meta["column_names"] == ["Col1", "Col2", "Col3"]
    assert meta["missing_values"]["Col1"] == 1
    assert meta["missing_values"]["Col2"] == 0
    assert meta["missing_values"]["Col3"] == 1
    assert meta["missing_total"] == 2
