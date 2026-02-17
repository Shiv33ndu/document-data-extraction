## Observations — Rule-Based Extraction

### Tool Selection Matters

During experimentation with digital PDF invoices, I initially used **PyMuPDF** for text extraction. While it is fast and reliable, it is not layout-aware, which led to missing or fragmented information such as totals, subtotals, and structured sections.

After evaluating alternatives, I switched to **pdfplumber**, which preserves layout information and performs significantly better for business documents containing tables and aligned text.

---

### Limitations of Rule-Based Extraction

Using heuristics and regular expressions works well for documents with predictable layouts. However, real-world documents exhibit significant variability in:

- Field naming ("Total", "Amount Due", "Balance")
- Layout structure
- Table formats
- Positioning of key information
- Presence of headers/footers
- Multi-page content

As a result, there is **no single rule set** that reliably handles all invoices or document templates.

*A robust rule-based system would require extensive pattern coverage and constant maintenance.*

---

### Need for Intelligent Systems

This variability highlights the need for more adaptive approaches such as:

- Machine learning–based document classification
- Named entity recognition
- Layout-aware models
- LLM-based extraction
- Hybrid rule + ML pipelines

**Rule-based methods are best suited as a baseline or for highly standardized documents.**

---

## Prototype Implemented 
```vbnet
Pipeline:
Ingest -> Text Extraction -> Document Classification -> Field Extraction -> Structured Output
```

**Supports**:
This system assumes the input to be Digital PDFs 

- Emails
- Invoices / Receipts
- Contract Docs
- Forms
- Financial Statements
- Compliance Docs
- Reports

Outputs structured JSON.


---

## Key Trade-offs

Rule-based systems:

**Strengths**
- Fast to implement
- Transparent
- Deterministic
- No training data required
- Low computational cost

**Weakness**
- Fragile to layout changes
- Hard to scale
- Poor generalization
- Sensitive to OCR noise