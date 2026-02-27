from pathlib import Path
from typing import List, Dict

from src.ingest import discover_documents
from src.extract import extract_text_from_pdf, extract_fields_by_type
from src.classifier import classify_document
from src.utils import save_json

from src.ocr import ocr_pdf, need_ocr, ocr_image


def process_document1(path: Path) -> Dict:
    """
    Process a single document and return structured output.
    Supports PDFs, images, and text files.
    """
    suffix = path.suffix.lower()

    # 1. ------ Text extraction -------
    if suffix == ".pdf":
        text = extract_text_from_pdf(path)

        # fallback to OCR if extraction poor
        if need_ocr(text):
            text = ocr_pdf(path)

    elif suffix in {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp"}:
        # image document OCR only
        text = ocr_image(path)

    elif suffix == ".txt":
        text = path.read_text(encoding="utf-8")
    
    else:
        raise ValueError(f"Unsupported file type: {suffix}")
    
    print(f"\n\nBefore Classification: {text}\n\n")
    
    # 2. ------ Classification ------
    doc_type = classify_document(text)

    # 3. ------ Field Extraction ------
    fields = extract_fields_by_type(doc_type, text)

    return {
        "file_name": path.name,
        "document_type": doc_type,
        "fields": fields,
        "flat_content": text
    }


def process_document(path: Path) -> Dict:
    suffix = path.suffix.lower()
    
    # Supported by Docling
    if suffix in {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".docx"}:
        text = ocr_pdf(path) # Works for both images and PDFs now
    elif suffix == ".txt":
        text = path.read_text(encoding="utf-8")
    else:
        raise ValueError(f"Unsupported type: {suffix}")
    

    print(f"\n\nBefore Classification: {text}\n\n")

    doc_type = classify_document(text)
    fields = extract_fields_by_type(doc_type, text)

    return {
        "file_name": path.name,
        "document_type": doc_type,
        "fields": fields,
        "flat_content": text
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
    input_dir = Path("data/test")
    output_dir = Path("results/results.json")

    results = process_directory(input_dir)

    save_json(results, output_dir)

    print(f"Extraction complete! Results are saved at {output_dir}")


if __name__ == "__main__":
    main()
