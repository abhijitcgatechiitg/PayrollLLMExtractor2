# Enhanced Schema - Visual Guide

## Schema Hierarchy

```
GLOBAL_SFP_SCHEMA
├── metadata
│   ├── currency: "INR"
│   ├── years: ["2019", "2018"]
│   └── extraction_timestamp
│
├── Equity (Section)
│   ├── ShareCapital (Field)
│   │   ├── description
│   │   ├── aliases: [...]
│   │   ├── value
│   │   ├── confidence: 0.0-1.0
│   │   ├── years: {"2019": "...", "2018": "..."}
│   │   ├── currency
│   │   ├── mapped_from
│   │   └── notes
│   │
│   ├── ReservesAndSurplus
│   │   └── (same structure)
│   │
│   └── TotalEquity
│       ├── is_total: true
│       └── (same structure)
│
├── NonCurrentLiabilities (Section)
│   ├── LongTermBorrowings
│   ├── DeferredTaxLiabilities
│   ├── LongTermProvisions
│   ├── OtherNonCurrentLiabilities
│   └── TotalNonCurrentLiabilities
│
├── CurrentLiabilities (Section)
│   ├── ShortTermBorrowings
│   ├── TradePayables
│   ├── OtherCurrentLiabilities
│   ├── ShortTermProvisions
│   └── TotalCurrentLiabilities
│
├── LiabilitiesTotal (Cross-section)
│
├── NonCurrentAssets (Section)
│   ├── PropertyPlantEquipmentNet
│   ├── CapitalWorkInProgress
│   ├── RightOfUseAssets
│   ├── IntangibleAssets
│   ├── FinancialAssets
│   ├── DeferredTaxAsset
│   ├── OtherNonCurrentAssets
│   └── TotalNonCurrentAssets
│
├── CurrentAssets (Section)
│   ├── Inventories
│   ├── TradeReceivables
│   ├── CashAndCashEquivalents
│   ├── OtherCurrentAssets
│   └── TotalCurrentAssets
│
├── AssetsTotal (Cross-section)
│
├── unmapped_items (Tracking)
│   └── items: [{label_raw, values, reason}, ...]
│
└── validation (Checks)
    ├── accounting_equation_valid: true/false
    ├── errors: [...]
    └── warnings: [...]
```

---

## Field Structure Anatomy

Each field looks like:
```python
"ShareCapital": {
    "description": "What is this field?",
    "aliases": ["Alt name 1", "Alt name 2", "..."],
    "value": "Latest/Primary value",
    "confidence": 0.95,  # 0.0 = No match, 1.0 = Perfect match
    "years": {
        "2019": "value1",
        "2018": "value2"
    },
    "currency": "INR",
    "mapped_from": "Share Capital",  # Original PDF label
    "notes": "Any additional info"
}
```

---

## Key Improvements Over Original Schema

| Feature | Original | Enhanced | Benefit |
|---------|----------|----------|---------|
| Multi-year storage | ❌ | ✅ `years: {2019: "...", 2018: "..."}` | Works with any years |
| Descriptions | ❌ | ✅ Per-field descriptions | LLM can understand fields |
| Aliases | ❌ | ✅ List of alternate names | Better PDF matching |
| Confidence tracking | ❌ | ✅ 0.0-1.0 score | Quality visibility |
| Metadata | ❌ | ✅ Currency, years, timestamp | Better context |
| Unmapped handling | ❌ | ✅ Dedicated section | No data loss |
| Validation | ❌ | ✅ Accounting equation check | Data integrity |

---

## Step 3 → Step 4 Data Flow

```
Step 3 Output (interim.json)
├── Raw item: "Share Capital", 2019: 70910990, 2018: 70910990
│
├─→ Step 4 Processing (Mapping)
│   ├─ Read global_schema.py
│   ├─ Find matching field using:
│   │  ├─ descriptions
│   │  ├─ aliases
│   │  └─ fuzzy matching
│   ├─ Calculate confidence
│   └─ Fill schema field
│
└─→ Step 4 Output (mapped.json)
    └─ ShareCapital field filled with:
       ├─ value: "70910990"
       ├─ confidence: 1.0
       ├─ years: {2019: "...", 2018: "..."}
       ├─ mapped_from: "Share Capital"
       └─ notes: "Perfect match"
```

---

## Design Principles (Your Requirements)

✅ **Year-Agnostic**
- `years: {"2019": "X", "2018": "Y"}` works for any years
- No hardcoded assumptions

✅ **Description-Aided**
- Each field has `description` and `aliases`
- Claude LLM uses these to match PDF labels

✅ **Confidence Tracked**
- `confidence: 0.95` shows mapping quality
- Helps identify uncertain mappings

✅ **Company-Universal**
- Works for KIDS MEDICAL, ACME, any company
- Same schema, different data

✅ **No Original Label Required**
- `mapped_from` optional (for debugging only)
- Schema is the single source of truth

---

## Next: Building Step 4

Step 4 will:
1. Load interim.json (25 raw items from KIDS MEDICAL)
2. Load global_schema.py (enhanced with descriptions)
3. For each raw item, ask Claude to map it
4. Fill mapped.json with confidence scores
5. Output clean, validated financial data

Ready? 🚀
