# Global Schema Enhancement - Design Decisions

## What Changed

### 1. **Year-Agnostic Design** ✅
- Each field has a `"years"` dictionary that dynamically stores values
- Example: `"years": {"2019": "70910990", "2018": "70910990"}`
- Works with ANY year combination (2020-2021, 2018-2019-2020, etc.)

### 2. **Description-Aided Mapping** ✅
- Every field now has:
  - `"description"`: What the field represents
  - `"aliases"`: Common alternate names from PDFs
- Example: `ShareCapital` has aliases like "Share Capital", "Share Stock", "Common Stock"
- **Helps Claude LLM** match raw PDF labels to schema fields with higher accuracy

### 3. **Confidence Tracking** ✅
- Each field has `"confidence": 0.0-1.0`
- Tracks how certain the mapping is
  - 1.0 = Perfect match (e.g., "Share Capital" → ShareCapital)
  - 0.7 = Good match with some ambiguity
  - 0.3 = Weak match (needs review)
- Helps identify data quality issues

### 4. **Removed Redundancies** ✅
- Removed `"BankBalances"` (covered by CashAndCashEquivalents)
- Removed `"Loans"` (covered by OtherCurrentAssets or FinancialAssets context)
- Consolidated to avoid confusion

### 5. **Enhanced Metadata** ✅
- Top-level `metadata` section tracks:
  - Currency (detected from PDF)
  - Years (detected from PDF)
  - Extraction timestamp

### 6. **Unmapped Items Capture** ✅
- `"unmapped_items"` section for items from PDF that don't fit schema
- Prevents data loss
- Helps identify schema gaps

### 7. **Validation Section** ✅
- `"validation"` tracks:
  - `accounting_equation_valid`: Assets = Liabilities + Equity?
  - `errors`: Critical issues blocking use
  - `warnings`: Items needing attention

---

## How Step 4 Will Use This

**Step 4 (Schema Mapping) will:**

1. **Take interim.json** from Step 3 (raw extracted items)
2. **For each raw item**, send to Claude with:
   - The raw label
   - The global schema (with descriptions + aliases)
   - Instructions: "Find best matching schema field or put in unmapped"
3. **Claude returns mapping** with confidence score
4. **Build mapped.json** filling in the schema with:
   - Mapped values
   - Confidence scores
   - Year data
   - Unmapped items

---

## Example Output (Step 4 will produce)

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
      "value": "70910990",
      "confidence": 1.0,
      "years": {"2019": "70910990", "2018": "70910990"},
      "notes": "Perfect match"
    },
    "ReservesAndSurplus": {
      "value": "1488693",
      "confidence": 0.95,
      "years": {"2019": "1488693", "2018": "40298434"},
      "notes": "Mapped from 'Reserves and Surplus' in PDF"
    }
  },
  "unmapped_items": [
    {
      "label_raw": "Some unusual field",
      "values": {"2019": "...", "2018": "..."},
      "reason": "No matching schema field found"
    }
  ],
  "validation": {
    "accounting_equation_valid": true,
    "errors": [],
    "warnings": []
  }
}
```

---

## Benefits of This Design

✅ **Company-Agnostic**: Same schema works for KIDS MEDICAL, ACME Corp, etc.
✅ **Year-Flexible**: Works with any time period combination
✅ **Traceable**: Can see mapping confidence and original labels in notes
✅ **Safe**: Unmapped items prevent forced/incorrect mappings
✅ **Validatable**: Built-in accounting equation check
✅ **Debuggable**: Description + aliases help identify mapping issues
