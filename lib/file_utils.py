"""File upload/download utilities for Streamlit apps."""

import io
import tempfile
import zipfile
from pathlib import Path

import streamlit as st


def create_zip(files: dict[str, bytes]) -> bytes:
    """Create a ZIP file from a dictionary of filename -> content pairs.

    Args:
        files: Dict mapping filenames to file content bytes.

    Returns:
        ZIP file as bytes.
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename, content in files.items():
            zf.writestr(filename, content)
    return buffer.getvalue()


def get_temp_dir() -> Path:
    """Get or create a temporary directory for the current session.

    Returns:
        Path to temporary directory.
    """
    if "temp_dir" not in st.session_state:
        st.session_state["temp_dir"] = tempfile.mkdtemp()
    return Path(st.session_state["temp_dir"])


def download_button_zip(
    files: dict[str, bytes],
    filename: str = "output.zip",
    label: str = "ダウンロード (ZIP)",
):
    """Show a download button for a ZIP file containing multiple files.

    Args:
        files: Dict mapping filenames to file content bytes.
        filename: Name of the ZIP file.
        label: Button label text.
    """
    zip_bytes = create_zip(files)
    st.download_button(
        label=label,
        data=zip_bytes,
        file_name=filename,
        mime="application/zip",
        type="primary",
    )
