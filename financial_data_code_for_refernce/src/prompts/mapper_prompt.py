"""
Step 4: Schema Mapper Prompt
Maps raw extracted data from interim.json to the global schema.
Uses descriptions and aliases to intelligently match fields.
"""

MAPPER_PROMPT_TEMPLATE = """You are a financial data mapping expert. Your task is to map raw financial line items to a predefined global schema.

CRITICAL RULES:
1. DO NOT invent fields - only use what's in the schema
2. Match using: exact names, aliases, descriptions, semantic meaning
3. Output a confidence score (0.0-1.0) for each mapping
4. If unsure or no good match → put in "unmapped" (don't force it)
5. Preserve ALL numeric values and years as-is
6. Return ONLY valid JSON, no extra text

SCHEMA DEFINITIONS (use descriptions + aliases to match):
{{
  "Equity": {{
    "ShareCapital": {{"description": "Share capital / Common stock", "aliases": ["Share Capital", "Shares held", "Share Stock"]}},
    "ReservesAndSurplus": {{"description": "Retained earnings, reserves, accumulated profits", "aliases": ["Reserves and Surplus", "Retained Earnings", "Accumulated Profit"]}},
    "OtherEquity": {{"description": "Other equity components", "aliases": ["Other Equity", "Other Reserves"]}},
    "TotalEquity": {{"description": "Total equity", "aliases": ["Total Equity", "Total Shareholders' Funds"]}}
  }},
  "NonCurrentLiabilities": {{
    "LongTermBorrowings": {{"description": "Long-term loans, bonds", "aliases": ["Long-term Borrowings", "Long Term Debt"]}},
    "DeferredTaxLiabilities": {{"description": "Deferred tax liability", "aliases": ["Deferred Tax Liabilities", "Deferred Tax"]}},
    "LongTermProvisions": {{"description": "Long-term provisions", "aliases": ["Long term Provision", "Pension Obligations"]}},
    "OtherNonCurrentLiabilities": {{"description": "Other long-term liabilities", "aliases": ["Other Non-current Liabilities"]}},
    "TotalNonCurrentLiabilities": {{"description": "Total non-current liabilities", "aliases": ["Total Non-current Liabilities"]}}
  }},
  "CurrentLiabilities": {{
    "ShortTermBorrowings": {{"description": "Short-term loans, overdrafts", "aliases": ["Short-term Borrowings", "Bank Overdraft"]}},
    "TradePayables": {{"description": "Accounts payable to suppliers", "aliases": ["Trade Payables", "Accounts Payable", "Creditors"]}},
    "OtherCurrentLiabilities": {{"description": "Other short-term liabilities", "aliases": ["Other Current Liabilities", "Accrued Expenses"]}},
    "ShortTermProvisions": {{"description": "Short-term provisions", "aliases": ["Short-term Provisions", "Current Provisions"]}},
    "TotalCurrentLiabilities": {{"description": "Total current liabilities", "aliases": ["Total Current Liabilities"]}}
  }},
  "NonCurrentAssets": {{
    "PropertyPlantEquipmentNet": {{"description": "PPE net of depreciation", "aliases": ["Property Plant and Equipment", "Fixed Assets", "Tangible Assets (Net)"]}},
    "CapitalWorkInProgress": {{"description": "Assets under construction", "aliases": ["Capital Work in Progress", "CWIP", "Construction in Progress"]}},
    "RightOfUseAssets": {{"description": "Lease assets", "aliases": ["Right of Use Assets", "ROU Assets"]}},
    "IntangibleAssets": {{"description": "Goodwill, patents, trademarks", "aliases": ["Intangible Assets", "Goodwill", "Patents"]}},
    "IntangibleAssetsUnderDevelopment": {{"description": "Intangible assets in development", "aliases": ["Intangible Assets under Development"]}},
    "FinancialAssets": {{"description": "Long-term investments", "aliases": ["Financial Assets", "Long-term Investments"]}},
    "DeferredTaxAsset": {{"description": "Deferred tax asset", "aliases": ["Deferred Tax Asset", "Tax Asset (Deferred)"]}},
    "OtherNonCurrentAssets": {{"description": "Other long-term assets", "aliases": ["Other Non-current Assets", "Long-term Loans and Advances"]}},
    "TotalNonCurrentAssets": {{"description": "Total non-current assets", "aliases": ["Total Non-current Assets"]}}
  }},
  "CurrentAssets": {{
    "Inventories": {{"description": "Stock, raw materials, WIP", "aliases": ["Inventories", "Stock", "Raw Materials", "Finished Goods"]}},
    "TradeReceivables": {{"description": "Accounts receivable", "aliases": ["Trade Receivables", "Accounts Receivable", "Debtors"]}},
    "CashAndCashEquivalents": {{"description": "Cash, bank deposits", "aliases": ["Cash and Cash Equivalents", "Cash", "Bank Balance"]}},
    "OtherCurrentAssets": {{"description": "Other short-term assets", "aliases": ["Other Current Assets", "Prepaid Expenses", "Short-term Advances"]}},
    "TotalCurrentAssets": {{"description": "Total current assets", "aliases": ["Total Current Assets"]}}
  }}
}}

MAPPING TASK:
For EACH raw item below, respond with:
{{
  "label_raw": "exact label from PDF",
  "schema_field": "FieldName or null if unmapped",
  "section": "SectionName or null if unmapped",
  "confidence": 0.0-1.0,
  "reason": "why this match or why unmapped",
  "values": {{"2019": "X", "2018": "Y"}},
  "is_total": true/false
}}

RAW ITEMS TO MAP:
{}

IMPORTANT:
- Respond with ONLY a JSON array of mapping results
- Each item gets one result object
- confidence: 1.0 = certain match, 0.5 = uncertain, 0.0 = no match
- No explanations outside JSON"""


def get_mapper_prompt(interim_items: list, schema_definitions: dict) -> str:
    """
    Format the mapper prompt with interim items and schema.
    
    Args:
        interim_items: List of raw items from interim.json
        schema_definitions: Schema with descriptions and aliases
        
    Returns:
        Formatted prompt ready to send to LLM
    """
    # Format items for prompt as JSON
    import json
    items_for_prompt = []
    for item in interim_items:
        items_for_prompt.append({
            "label_raw": item.get("label_raw", ""),
            "values": item.get("values", {}),
            "is_total": item.get("is_total", False)
        })
    
    items_text = json.dumps(items_for_prompt, indent=2)
    
    return MAPPER_PROMPT_TEMPLATE.format(items_text)
