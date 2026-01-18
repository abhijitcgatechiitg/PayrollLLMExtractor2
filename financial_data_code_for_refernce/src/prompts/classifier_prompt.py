"""
Step 2: SFP (Statement of Financial Position) Classifier Prompt
This prompt is used to ask Claude whether a given page contains SFP data.
"""

CLASSIFIER_PROMPT_TEMPLATE = """You are a financial document classifier. Your task is to identify whether a given page contains a Statement of Financial Position (SFP), also known as a Balance Sheet.

A Statement of Financial Position typically contains:
- Assets (Current and Non-Current)
- Liabilities (Current and Non-Current)
- Equity/Shareholders' Funds
- Financial years/periods (usually 1-3 years for comparison)
- Numerical values representing amounts

The page may also be called:
- Balance Sheet
- Statement of Financial Position
- SFP
- Assets & Liabilities Statement

Your response should be ONLY a JSON object with this structure (replace the values):
{{"contains_sfp": true or false, "confidence": 0.0 to 1.0, "reason": "Brief explanation"}}

Examples of pages that CONTAIN SFP:
- A page showing "Assets = Liabilities + Equity" in tabular format
- Pages titled "Balance Sheet" with financial figures
- Pages with row labels like "Current Assets", "Fixed Assets", "Current Liabilities", etc.

Examples of pages that DO NOT contain SFP:
- Management discussion & analysis pages
- Audit opinion pages
- Footnotes or accounting policies
- Cash flow statements
- Income statements (Profit & Loss)

Now, analyze this page:

--- PAGE CONTENT START ---
{}
--- PAGE CONTENT END ---

Respond ONLY with the JSON object, no additional text."""


def get_classifier_prompt(page_text: str) -> str:
    """
    Format the classifier prompt with actual page content.
    
    Args:
        page_text: The text content of the page to classify
        
    Returns:
        Formatted prompt ready to send to LLM
    """
    return CLASSIFIER_PROMPT_TEMPLATE.format(page_text)
