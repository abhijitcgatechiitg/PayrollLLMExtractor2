"""
Global Schema for Statement of Financial Position (Balance Sheet)

Design principles:
1. Year-agnostic: Values stored with dynamic year keys (e.g., "2019", "2020")
2. Description-aided mapping: Each field has a description to help LLM mapping
3. Confidence tracking: Maps include confidence score and data quality metrics
4. Unmapped items capture: Fields for items that don't fit standard schema
5. Company-agnostic: Works across different companies and reporting standards

Structure for each field:
{
    "value": None,           # Mapped numeric value or null if not found
    "confidence": 0.0,       # 0.0-1.0 confidence score of mapping
    "years": {},             # e.g., {"2019": "70910990", "2018": "70910990"}
    "currency": None,        # e.g., "INR", "USD"
    "mapped_from": None,     # Original raw label from PDF (for debugging)
    "notes": ""              # Any additional notes or flags
}
"""

GLOBAL_SFP_SCHEMA = {
    "section": "StatementOfFinancialPosition",
    "metadata": {
        "description": "Balance Sheet - Statement of Financial Position",
        "currency": None,
        "years": [],
        "extraction_timestamp": None
    },
    
    # ============ EQUITY SECTION ============
    "Equity": {
        "description": "Owner's equity and retained earnings",
        "ShareCapital": {
            "description": "Share capital / Common stock / Issued capital",
            "aliases": ["Share Capital", "Shares held", "Share Stock", "Common Stock"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "ReservesAndSurplus": {
            "description": "Retained earnings, reserves, accumulated profits",
            "aliases": ["Reserves and Surplus", "Retained Earnings", "Accumulated Profit", "Reserves"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "OtherEquity": {
            "description": "Other equity components, treasury stock, other reserves",
            "aliases": ["Other Equity", "Other Reserves", "Treasury Stock"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "TotalEquity": {
            "description": "Total equity (sum of all equity components)",
            "aliases": ["Total Equity", "Total Shareholders' Funds", "Total Capital"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "is_total": True,
            "notes": ""
        }
    },
    
    # ============ LIABILITIES SECTION ============
    "NonCurrentLiabilities": {
        "description": "Long-term obligations (due beyond 12 months)",
        "LongTermBorrowings": {
            "description": "Long-term loans, bonds, debentures",
            "aliases": ["Long-term Borrowings", "Long Term Debt", "Bonds Payable"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "DeferredTaxLiabilities": {
            "description": "Deferred tax liabilities from temporary differences",
            "aliases": ["Deferred Tax Liabilities", "Deferred Tax", "Tax Payable (Deferred)"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "LongTermProvisions": {
            "description": "Provisions for long-term obligations (pensions, warranties, etc.)",
            "aliases": ["Long term Provision", "Long-term Provisions", "Pension Obligations"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "OtherNonCurrentLiabilities": {
            "description": "Other long-term liabilities not classified elsewhere",
            "aliases": ["Other Non-current Liabilities", "Other Long-term Liabilities"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "TotalNonCurrentLiabilities": {
            "description": "Total non-current liabilities",
            "aliases": ["Total Non-current Liabilities", "Total Long-term Liabilities"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "is_total": True,
            "notes": ""
        }
    },
    
    "CurrentLiabilities": {
        "description": "Short-term obligations (due within 12 months)",
        "ShortTermBorrowings": {
            "description": "Short-term loans, overdrafts, current portion of long-term debt",
            "aliases": ["Short-term Borrowings", "Short Term Debt", "Bank Overdraft", "Current Portion of Long-term Debt"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "TradePayables": {
            "description": "Accounts payable to suppliers",
            "aliases": ["Trade Payables", "Accounts Payable", "Creditors"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "OtherCurrentLiabilities": {
            "description": "Other short-term liabilities (accruals, deferred revenue, etc.)",
            "aliases": ["Other Current Liabilities", "Accrued Expenses", "Short-term Accruals"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "ShortTermProvisions": {
            "description": "Provisions for short-term obligations",
            "aliases": ["Short-term Provisions", "Current Provisions"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "TotalCurrentLiabilities": {
            "description": "Total current liabilities",
            "aliases": ["Total Current Liabilities", "Total Short-term Liabilities"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "is_total": True,
            "notes": ""
        }
    },
    
    "LiabilitiesTotal": {
        "description": "Total liabilities (current + non-current)",
        "aliases": ["Total Liabilities"],
        "value": None,
        "confidence": 0.0,
        "years": {},
        "is_total": True,
        "notes": ""
    },
    
    # ============ ASSETS SECTION ============
    "NonCurrentAssets": {
        "description": "Long-term assets (expected to be used beyond 12 months)",
        "PropertyPlantEquipmentNet": {
            "description": "PP&E net of accumulated depreciation",
            "aliases": ["Property Plant and Equipment", "Fixed Assets", "PPE", "Tangible Assets (Net)"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "CapitalWorkInProgress": {
            "description": "Assets under construction or development",
            "aliases": ["Capital Work in Progress", "CWIP", "Construction in Progress"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "RightOfUseAssets": {
            "description": "Right-of-use assets under lease agreements (IFRS 16/ASC 842)",
            "aliases": ["Right of Use Assets", "Lease Assets", "ROU Assets"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "IntangibleAssets": {
            "description": "Goodwill, patents, trademarks, software, etc.",
            "aliases": ["Intangible Assets", "Goodwill", "Patents", "Intellectual Property"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "IntangibleAssetsUnderDevelopment": {
            "description": "Intangible assets still in development phase",
            "aliases": ["Intangible Assets under Development", "Intangibles Under Development"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "FinancialAssets": {
            "description": "Long-term investments, securities, loans given",
            "aliases": ["Financial Assets", "Long-term Investments", "Investment Securities"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "DeferredTaxAsset": {
            "description": "Deferred tax asset from temporary differences and tax losses",
            "aliases": ["Deferred Tax Asset", "Tax Asset (Deferred)"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "OtherNonCurrentAssets": {
            "description": "Other long-term assets not classified elsewhere",
            "aliases": ["Other Non-current Assets", "Other Long-term Assets", "Long-term Loans and Advances"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "TotalNonCurrentAssets": {
            "description": "Total non-current assets",
            "aliases": ["Total Non-current Assets", "Total Fixed Assets"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "is_total": True,
            "notes": ""
        }
    },
    
    "CurrentAssets": {
        "description": "Short-term assets (expected to be converted to cash within 12 months)",
        "Inventories": {
            "description": "Stock of goods, raw materials, work in progress",
            "aliases": ["Inventories", "Stock", "Inventory", "Raw Materials", "Finished Goods"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "TradeReceivables": {
            "description": "Accounts receivable from customers",
            "aliases": ["Trade Receivables", "Accounts Receivable", "Debtors"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "CashAndCashEquivalents": {
            "description": "Cash on hand, bank accounts, short-term deposits",
            "aliases": ["Cash and Cash Equivalents", "Cash", "Bank Balance", "Short-term Deposits"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "OtherCurrentAssets": {
            "description": "Other short-term assets (prepaid expenses, short-term advances, etc.)",
            "aliases": ["Other Current Assets", "Prepaid Expenses", "Short-term Advances"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "notes": ""
        },
        "TotalCurrentAssets": {
            "description": "Total current assets",
            "aliases": ["Total Current Assets"],
            "value": None,
            "confidence": 0.0,
            "years": {},
            "is_total": True,
            "notes": ""
        }
    },
    
    "AssetsTotal": {
        "description": "Total assets (current + non-current)",
        "aliases": ["Total Assets"],
        "value": None,
        "confidence": 0.0,
        "years": {},
        "is_total": True,
        "notes": ""
    },
    
    # ============ UNMAPPED & VALIDATION ============
    "unmapped_items": {
        "description": "Items from PDF that could not be mapped to schema",
        "items": []
    },
    
    "validation": {
        "description": "Financial statement validation checks",
        "accounting_equation_valid": False,  # Assets = Liabilities + Equity
        "errors": [],
        "warnings": []
    }
}
