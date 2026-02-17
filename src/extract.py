import pdfplumber
import re
from typing import Dict

from src.preprocess import normalize_text

def extract_text_from_pdf(path: str) -> str:
    text = []

    with pdfplumber.open(path) as file:
        for page in file.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

    return "\n".join(text)




def extract_invoice_fields(text: str) -> Dict:
    fields = {}  #dict placeholder

    text = normalize_text(text)

    # regex to target the fields 
    invoice_no = re.search(
        r"(Invoice\s*(?:No|#)?\s*[:\-]?\s*)([A-Z0-9-]+)",
        text,
        re.IGNORECASE
    )

    date = re.search(
        r"(Invoice\s*Date|Date)\s*[:\-]?\s*([0-9A-Za-z,./-]+)",
        text,
        re.IGNORECASE
    )

    total = re.search(
        r"(Total\s*|Total\s*(?:Due)?|Amount\s*Due)\s*[:\-]?\s*\$?\s*([0-9,]+\.\d{2})",
        text,
        re.IGNORECASE
    )

    fields["invoice_number"] = invoice_no.group(2) if invoice_no else None
    fields["date"] = date.group(2) if date else None
    fields["total_amount"] = total.group(2) if total else None

    return fields


def extract_contract_fields(text: str) -> Dict:
    fields = {}
    text = normalize_text(text)

    effective_date = re.search(r"Effective\s*Date\s*[:\-]?\s*([0-9A-Za-z,.\s/-]+)", text, re.IGNORECASE)
    
    # improved parties regex to handle "Inc." or "Ltd."
    # Looks for 'between' followed by the text until the end of that specific clause/line
    parties = re.search(r"between\s+(.+?)\s+and\s+(.+?)(?=\n|\.|\s{2,})", text, re.IGNORECASE)

    fields["effective_date"] = effective_date.group(1).strip() if effective_date else None
    if parties:
        fields["parties"] = f"{parties.group(1).strip()} & {parties.group(2).strip()}"
    else:
        fields["parties"] = None
    return fields



def extract_form_fields(text: str) -> Dict:
    fields = {}
    # Key improvement: Ensure we don't grab the whole next paragraph as a 'value'
    # This looks for 'Key: Value' appearing on its own line or followed by space
    pairs = re.findall(r"^([A-Za-z ]+):\s*(.+)$", text, re.MULTILINE)
    for key, value in pairs:
        fields[key.strip().lower().replace(" ", "_")] = value.strip()
    return fields


def extract_financial_fields(text: str) -> Dict:
    fields = {}
    # Note: Use [\d,.]+ to capture full currency amounts with commas and decimals
    assets = re.search(r"Total\s*Assets\s*[:\-]?\s*\$?\s*([\d,.]+)", text, re.IGNORECASE)
    liabilities = re.search(r"Total\s*Liabilities\s*[:\-]?\s*\$?\s*([\d,.]+)", text, re.IGNORECASE)

    fields["total_assets"] = assets.group(1) if assets else None
    fields["total_liabilities"] = liabilities.group(1) if liabilities else None
    return fields


def extract_email_fields(text: str) -> Dict:
    fields = {}

    text = normalize_text(text)

    sender = re.search(r"From:\s*(.+)", text)
    recipient = re.search(r"To:\s*(.+)", text)
    subject = re.search(r"Subject:\s*(.+)", text)

    fields["from"] = sender.group(1) if sender else None
    fields["to"] = recipient.group(1) if recipient else None
    fields["subject"] = subject.group(1) if subject else None

    return fields



def extract_report_fields(text: str) -> Dict:
    fields = {}

    text = normalize_text(text)

    # Title (first non-empty line heuristic)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    fields["title"] = lines[0] if lines else None

    # Executive summary presence
    summary = re.search(
        r"(Executive\s+Summary)(.*?)(\n[A-Z][^\n]{3,}|$)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    fields["executive_summary"] = summary.group(2).strip() if summary else None

    # Date
    date = re.search(
        r"(Date|Published)\s*[:\-]?\s*([0-9A-Za-z,./-]+)",
        text,
        re.IGNORECASE
    )

    fields["date"] = date.group(2) if date else None

    # Author / Organization
    author = re.search(
        r"(Author|Prepared by)\s*[:\-]?\s*(.+)",
        text,
        re.IGNORECASE
    )

    fields["author"] = author.group(2) if author else None

    return fields


def extract_compliance_fields(text: str) -> Dict:
    fields = {}

    text = normalize_text(text)

    # Policy / document name (first line heuristic)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    fields["document_name"] = lines[0] if lines else None

    # Effective date
    effective_date = re.search(
        r"(Effective\s*Date)\s*[:\-]?\s*([0-9A-Za-z,./-]+)",
        text,
        re.IGNORECASE
    )

    fields["effective_date"] = (
        effective_date.group(2) if effective_date else None
    )

    # Version
    version = re.search(
        r"(Version)\s*[:\-]?\s*([0-9.]+)",
        text,
        re.IGNORECASE
    )

    fields["version"] = version.group(2) if version else None

    # Regulatory references
    regulation = re.search(
        r"(Regulation|Standard)\s*[:\-]?\s*(.+)",
        text,
        re.IGNORECASE
    )

    fields["regulatory_reference"] = (
        regulation.group(2) if regulation else None
    )

    # Issuing authority
    authority = re.search(
        r"(Issued by|Authority)\s*[:\-]?\s*(.+)",
        text,
        re.IGNORECASE
    )

    fields["issuing_authority"] = (
        authority.group(2) if authority else None
    )

    return fields



def extract_fields_by_type(doc_type: str, text: str) -> Dict:
    """
    Route to the correct extractor based on document type.
    """

    if doc_type == "invoice":
        return extract_invoice_fields(text)

    if doc_type == "contract":
        return extract_contract_fields(text)

    if doc_type == "form":
        return extract_form_fields(text)

    if doc_type == "report":
        return extract_report_fields(text)  

    if doc_type == "financial_statement":
        return extract_financial_fields(text)

    if doc_type == "compliance":
        return extract_compliance_fields(text)

    if doc_type == "email":
        return extract_email_fields(text)

    return {}
