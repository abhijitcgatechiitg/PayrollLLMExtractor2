# Schema Usage Example

## Before & After Comparison

### BEFORE (Your Original Schema)
```python
"ShareCapital": {}
```
❌ Problems:
- Can't store multi-year data
- No mapping confidence
- No help for LLM to understand what it is
- Can't track data quality

---

### AFTER (Enhanced Schema)
```python
"ShareCapital": {
    "description": "Share capital / Common stock / Issued capital",
    "aliases": ["Share Capital", "Shares held", "Share Stock", "Common Stock"],
    "value": "70910990",  # Latest or primary value
    "confidence": 1.0,     # 100% confident in mapping
    "years": {
        "2019": "70910990",
        "2018": "70910990"
    },
    "currency": "INR",
    "mapped_from": "Share Capital",  # Original PDF label
    "notes": "Exact match from PDF",
    "is_total": false
}
```
✅ Benefits:
- Multi-year values stored
- Confidence tracked (0.0-1.0)
- LLM understands field meaning
- Data quality visible
- Traceable to source

---

## Real Example from sofp_sample3.pdf

### Raw Data (Step 3 Output)
```json
{
    "label_raw": "Share Capital",
    "category_raw": "Equity",
    "is_total": false,
    "values": {
        "2019": "70,910,990",
        "2018": "70,910,990"
    }
}
```

### Mapped Data (Step 4 Output - Will Produce)
```json
{
    "section": "StatementOfFinancialPosition",
    "metadata": {
        "currency": "INR",
        "years": ["2019", "2018"],
        "extraction_timestamp": "2025-12-05T21:05:00"
    },
    "Equity": {
        "ShareCapital": {
            "description": "Share capital / Common stock / Issued capital",
            "aliases": ["Share Capital", "Shares held", "Share Stock", "Common Stock"],
            "value": "70910990",
            "confidence": 1.0,
            "years": {
                "2019": "70910990",
                "2018": "70910990"
            },
            "currency": "INR",
            "mapped_from": "Share Capital",
            "notes": "Exact match with PDF label",
            "is_total": false
        },
        "ReservesAndSurplus": {
            "description": "Retained earnings, reserves, accumulated profits",
            "aliases": ["Reserves and Surplus", "Retained Earnings", "Accumulated Profit"],
            "value": "1488693",
            "confidence": 0.95,
            "years": {
                "2019": "1488693",
                "2018": "40298434"
            },
            "currency": "INR",
            "mapped_from": "Reserves and Surplus",
            "notes": "High confidence match",
            "is_total": false
        },
        # ... more Equity items
        "TotalEquity": {
            "description": "Total equity (sum of all equity components)",
            "value": "72399683",
            "confidence": 1.0,
            "years": {
                "2019": "72399683",
                "2018": "111209424"
            },
            "is_total": true,
            "notes": "Sum of equity components"
        }
    },
    "NonCurrentLiabilities": {
        "LongTermBorrowings": {
            "description": "Long-term loans, bonds, debentures",
            "value": null,
            "confidence": 0.0,
            "years": {},
            "notes": "No matching data found in PDF"
        },
        # ... more liabilities
    },
    "CurrentLiabilities": {
        "ShortTermBorrowings": {
            "value": "3701333",
            "confidence": 1.0,
            "years": {"2019": "3701333", "2018": "2999555"},
            "notes": "Exact match"
        },
        "TradePayables": {
            "value": "680396",
            "confidence": 1.0,
            "years": {"2019": "680396", "2018": "530432"},
            "notes": "Exact match"
        }
        # ... more current liabilities
    },
    "NonCurrentAssets": {
        "PropertyPlantEquipmentNet": {
            "value": "1853896",
            "confidence": 0.9,
            "years": {"2019": "1853896", "2018": "37263829"},
            "mapped_from": "Property, Plant and Equipment (Net Block)",
            "notes": "Mapped from PPE section with high confidence"
        }
        # ... more non-current assets
    },
    "CurrentAssets": {
        "TradeReceivables": {
            "value": "2233486",
            "confidence": 1.0,
            "years": {"2019": "2233486", "2018": "2233486"}
        },
        "CashAndCashEquivalents": {
            "value": "1904455",
            "confidence": 0.95,
            "years": {"2019": "1904455", "2018": "2564569"},
            "notes": "Mapped from 'Cash and Cash Equivelants' (typo in PDF)"
        }
        # ... more current assets
    },
    "unmapped_items": [
        {
            "label_raw": "Capital Work in Progress",
            "values": {"2019": null, "2018": "35409934"},
            "reason": "Low confidence mapping - moved to unmapped for review"
        }
    ],
    "validation": {
        "accounting_equation_valid": true,
        "total_assets": "78267057",
        "total_liabilities_equity": "78267057",
        "errors": [],
        "warnings": [
            "Cash and Cash Equivalents has typo in PDF: 'Equivelants'"
        ]
    }
}
```

---

## How to Use This Output

### For Data Analysis
```python
# Get Share Capital for 2019
share_capital = mapped_data["Equity"]["ShareCapital"]["years"]["2019"]
# Result: "70910990"

# Check confidence before using
confidence = mapped_data["Equity"]["ShareCapital"]["confidence"]
if confidence < 0.8:
    print("Warning: Low confidence mapping!")
```

### For Quality Assurance
```python
# Check if mapping is valid
if not mapped_data["validation"]["accounting_equation_valid"]:
    print("Financial statement does not balance!")
    
# Review unmapped items
for item in mapped_data["unmapped_items"]:
    print(f"Unmapped: {item['label_raw']}")
```

### For Company Comparison
```python
# Same schema works for KIDS MEDICAL, ACME Corp, any company
# Extract and compare across companies using same fields:
kids_revenue = kids_data["CurrentAssets"]["TradeReceivables"]["years"]["2019"]
acme_revenue = acme_data["CurrentAssets"]["TradeReceivables"]["years"]["2019"]

# Direct comparison possible because schema is consistent
```

---

## ✨ Why This Design Wins

1. **Universality**: Same schema for all companies
2. **Flexibility**: Any year combination works
3. **Quality**: Confidence scores visible
4. **Traceability**: Know source of each value
5. **Safety**: Unmapped items prevent silent data loss
6. **Validation**: Built-in accounting checks
