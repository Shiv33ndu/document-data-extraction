import json
from pathlib import Path
from typing import List, Dict


def save_json(results: List[Dict], output_path: str) -> None:
    """
    Save results to a JSON file.
    """

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
