"""
CLI entry point for launching the Streamlit application via python -m data_visualization.
"""

import sys
from pathlib import Path
from streamlit.web.cli import main as streamlit_cli


def cli_entry() -> None:
    """Launch the Streamlit web interface."""
    app_path = Path(__file__).resolve().parent / "app.py"
    sys.argv = ["streamlit", "run", str(app_path)] + sys.argv[1:]
    streamlit_cli()


if __name__ == "__main__":
    cli_entry()
