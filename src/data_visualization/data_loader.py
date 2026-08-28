"""
Data loading module for reading CSV files and extracting dataset metadata.
"""

from pathlib import Path
from typing import Any, Dict, Union, IO
import pandas as pd


class DataLoaderError(Exception):
    """Custom exception raised when data loading or parsing fails."""
    pass


def load_csv(file_or_path: Union[str, Path, IO[Any]]) -> pd.DataFrame:
    """
    Safely load a CSV dataset into a Pandas DataFrame.

    Args:
        file_or_path: File path (str/Path) or file-like object (e.g. Streamlit UploadedFile).

    Returns:
        pd.DataFrame: Parsed Pandas DataFrame.

    Raises:
        DataLoaderError: If the CSV file cannot be parsed, is empty, or does not exist.
    """
    if file_or_path is None:
        raise DataLoaderError("No file or file path provided.")

    try:
        if isinstance(file_or_path, (str, Path)):
            path = Path(file_or_path)
            if not path.exists():
                raise DataLoaderError(f"File not found: '{path}'")
            if path.stat().st_size == 0:
                raise DataLoaderError("The provided CSV file is empty (0 bytes).")
            df = pd.read_csv(path)
        else:
            # File-like object
            file_or_path.seek(0)
            df = pd.read_csv(file_or_path)

        if df is None or df.empty and len(df.columns) == 0:
            raise DataLoaderError("The dataset contains no data or columns.")

        return df

    except pd.errors.EmptyDataError:
        raise DataLoaderError("The CSV file is empty or contains no readable data.")
    except pd.errors.ParserError as e:
        raise DataLoaderError(f"Failed to parse CSV file: {str(e)}")
    except UnicodeDecodeError:
        raise DataLoaderError("Encoding error: File is not a valid UTF-8 text/CSV file.")
    except DataLoaderError:
        raise
    except Exception as e:
        raise DataLoaderError(f"An error occurred while loading the dataset: {str(e)}")


def get_dataset_metadata(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Extract comprehensive metadata from a DataFrame.

    Args:
        df: Pandas DataFrame to analyze.

    Returns:
        Dict[str, Any]: Dictionary containing row count, column count, column names,
                        data types, missing value counts per column, and total missing cells.
    """
    if df is None:
        raise DataLoaderError("Cannot extract metadata from a None object.")

    row_count, col_count = df.shape
    column_names = list(df.columns)
    data_types = {col: str(df[col].dtype) for col in column_names}
    missing_values = {col: int(df[col].isna().sum()) for col in column_names}
    total_missing = sum(missing_values.values())

    return {
        "row_count": row_count,
        "column_count": col_count,
        "column_names": column_names,
        "data_types": data_types,
        "missing_values": missing_values,
        "missing_total": total_missing,
    }


def load_sample_dataset() -> pd.DataFrame:
    """
    Load the built-in sample CSV dataset included with the project.

    Returns:
        pd.DataFrame: Sample dataset.

    Raises:
        DataLoaderError: If sample.csv cannot be located or loaded.
    """
    base_dir = Path(__file__).resolve().parent.parent.parent
    sample_path = base_dir / "data" / "sample.csv"

    if not sample_path.exists():
        raise DataLoaderError(f"Sample dataset not found at expected path: '{sample_path}'")

    return load_csv(sample_path)
