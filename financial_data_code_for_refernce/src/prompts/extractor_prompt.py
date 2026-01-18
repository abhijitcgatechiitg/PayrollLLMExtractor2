"""
Step 3: Raw Data Extractor Prompt
This prompt tells Claude to extract SFP table data AS-IS without forcing any schema.
The key is to preserve raw labels, values, and structure exactly as they appear.
"""

EXTRACTOR_PROMPT_TEMPLATE = """You are a financial data extraction specialist. Your task is to extract table data from a Statement of Financial Position (Balance Sheet) EXACTLY as it appears in the document.

CRITICAL RULES:
1. Extract data AS-IS - do NOT normalize or force business field names
2. Preserve exact row labels from the PDF
3. Detect financial years/periods from column headers
4. Detect currency if mentioned
5. Extract ALL numerical values for each year
6. Mark rows that appear to be subtotals or totals
7. Include ANY extra information in notes (e.g., references, conditions)
8. Do NOT invent or assume field names

Output ONLY a valid JSON object with this exact structure (no markdown, no extra text):
{{
  "section": "SFP",
  "years": ["year1", "year2"],
  "currency": "detected currency or USD if not found",
  "items": [
    {{
      "label_raw": "exact label from PDF",
      "category_raw": "Assets/Liabilities/Equity if detectable, else null",
      "is_total": true/false,
      "values": {{"year1": "value1", "year2": "value2"}},
      "extra": {{"reference": "note number", "notes": "any extra info"}}
    }}
  ]
}}

EXAMPLES OF CORRECT EXTRACTION:

Input PDF rows:
```
Share Capital         70,910,990    70,910,990
Reserves and Surplus  1,488,693     40,298,434
```

Correct Output:
```json
[
  {{"label_raw": "Share Capital", "category_raw": "Equity", "is_total": false, "values": {{"2019": "70,910,990", "2018": "70,910,990"}}, "extra": {{}}}},
  {{"label_raw": "Reserves and Surplus", "category_raw": "Equity", "is_total": false, "values": {{"2019": "1,488,693", "2018": "40,298,434"}}, "extra": {{}}}}
]
```

IMPORTANT:
- Preserve spacing and formatting in labels
- If a row is a subtotal (contains "total" or "Total" or similar), mark is_total: true
- If a value is missing or dash (-), use null or empty string ""
- Years should be detected from headers (e.g., "As at 31st March 2019" -> "2019")

Now extract data from this SFP text:

--- SFP TEXT START ---
{}
--- SFP TEXT END ---

Output ONLY the JSON object."""


def get_extractor_prompt(sfp_text: str) -> str:
    """
    Format the extractor prompt with actual SFP text.
    
    Args:
        sfp_text: The combined text from all SFP pages
        
    Returns:
        Formatted prompt ready to send to LLM
    """
    return EXTRACTOR_PROMPT_TEMPLATE.format(sfp_text)
