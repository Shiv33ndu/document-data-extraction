def classify_document(text: str) -> str:
    """
    Classify the document based on the keywords. This expects a predictive layout for the documents like 
    - Emails  
    - Invoice / Receipt
    - Contract
    - Forms
    - Reports
    - Financial Statements
    - Compliance
    
    :param text: textual data from digital pdf file 
    :type text: str
    :return: the type of document
    :rtype: str
    """
    t = text.lower()
    
    # Define weights: 3 for unique anchors, 1 for general context
    categories = {
        "invoice": {
            "anchors": ["invoice no:", "bill to:", "total amount due:", "payment terms:"],
            "context": ["description", "tax", "subtotal", "qty"]
        },
        "contract": {
            "anchors": ["service agreement", "this agreement is made", "term:", "termination:"],
            "context": ["agreement", "party", "signed", "effective date"]
        },
        "report": {
            "anchors": ["executive summary:", "key findings:", "performance report"],
            "context": ["prepared by:", "conclusion", "analysis"]
        },
        "financial_statement": {
            "anchors": ["balance sheet", "income statement", "cash flow", "as of"],
            "context": ["assets:", "liabilities:", "equity", "receivable", "payable"]
        },
        "compliance": {
            "anchors": ["compliance policy", "regulation:", "gdpr", "review cycle:"],
            "context": ["regulatory", "audit", "policy", "requirements"]
        },
        "email": {
            "anchors": ["from:", "to:", "subject:", "sent:", "cc:"],
            "context": ["best regards", "hi ", "attached documents"]
        },
        "form": {
            "anchors": ["please fill", "application form", "signature of applicant"],
            "context": ["checkbox", "[ ]", "male", "female", "dob:"]
        }
    }

    scores = {cat: 0 for cat in categories}

    for cat, keywords in categories.items():
        # Anchors are very strong indicators (Weight: 3)
        scores[cat] += sum(3 for k in keywords["anchors"] if k in t)
        # Contextual words provide support (Weight: 1)
        scores[cat] += sum(1 for k in keywords["context"] if k in t)

    # Find the category with the highest score
    best_match = max(scores, key=scores.get)

    # Return 'unknown' if no significant keywords are found
    if scores[best_match] == 0:
        return "unknown"
        
    return best_match   