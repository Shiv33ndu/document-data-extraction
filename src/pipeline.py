from pathlib import Path

from src.extract import extract_text_from_pdf, extract_fields_by_type
from src.classifier import classify_document


def process_document(path: str) -> str:
    
    # assumes the input file is a digital PDF 
    text = extract_text_from_pdf(path)
    
    # find the doc type using some set of predictable keyword from the document
    doc_type = classify_document(text)
    
    # use the correct extractor as per the doc type 
    fields = extract_fields_by_type(doc_type, text)

    return {
        "document_type": doc_type,
        "fields": fields
    }


def main():
    path = Path(__file__).parent.parent

    file_path = Path(path / "data" / "samples1" / "form_f1040s1.pdf")

    output = process_document(file_path)

    print(output)

if __name__ == "__main__":
    main()