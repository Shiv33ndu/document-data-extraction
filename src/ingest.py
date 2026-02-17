from pathlib import Path
from typing import List


SUPPORTED_EXTENSIONS = {".pdf", ".txt"}


def discover_documents(input_dir: str) -> List[Path]:
    """
    Discover supported documents inside a directory (recursive).

    Parameters
    ----------
    input_dir : str
        Path to the directory containing documents.

    Returns
    -------
    List[Path]
        List of file paths to supported documents.
    """

    base_path = Path(input_dir)

    if not base_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    if not base_path.is_dir():
        raise ValueError(f"Provided path is not a directory: {input_dir}")

    documents = []

    for file in base_path.rglob("*"):
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS:
            documents.append(file)

    return sorted(documents)


def validate_document(path: Path) -> bool:
    """
    Validate a single document path.

    Returns True if valid and supported.
    """

    if not path.exists():
        return False

    if not path.is_file():
        return False

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False

    return True
