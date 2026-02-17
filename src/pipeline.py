from pathlib import Path
from typing import List, Dict

from src.ingest import discover_documents
from src.extract import extract_text_from_pdf, extract_fields_by_type
from src.classifier import classify_document
from src.utils import save_json


def process_document(path: Path) -> Dict:
    """
    Process a single document and return structured output.
    """

    text = extract_text_from_pdf(path)

    doc_type = classify_document(text)

    fields = extract_fields_by_type(doc_type, text)

    return {
        "file_name": path.name,
        "document_type": doc_type,
        "fields": fields
    }


def process_directory(input_dir: str) -> List[Dict]:
    """
    Process all supported documents in a directory.
    """

    documents = discover_documents(input_dir)

    results = []

    for doc_path in documents:
        try:
            result = process_document(doc_path)
            results.append(result)

        except Exception as e:
            results.append({
                "file_name": doc_path.name,
                "error": str(e)
            })

    return results


def main():
    input_dir = Path("data/samples2")
    output_dir = Path("results/results.json")

    results = process_directory(input_dir)

    save_json(results, output_dir)

    print(f"Extraction complete! Results are saved at {output_dir}")


if __name__ == "__main__":
    main()
