# Design Log - Code Structure

**Date:** January 18, 2026  
**Phase:** Code Structure Design - FINALIZED ✅

## Decision: Project Structure

```
Payroll_extraction_part2/
├── main.py                          # Simple orchestrator
├── .env                             # API keys (ANTHROPIC_API_KEY)
├── requirements.txt                 # pymupdf, anthropic, python-dotenv
├── .gitignore                       
│
├── src/
│   ├── step1_pdf_extraction.py      # Extract text page-by-page
│   ├── step2_raw_extraction.py      # PASS 1: Extract interim JSON
│   ├── step3_schema_mapping.py      # PASS 2: Map to global schema
│   ├── step4_validation.py          # Placeholder (dummy for future)
│   │
│   └── prompts/
│       ├── extractor_prompt.py      # Raw extraction prompt
│       └── mapper_prompt.py         # Schema mapping prompt
│
├── schema/
│   ├── global_schema.py             # ✅ DONE
│   └── SCHEMA_EXPLANATION.md        # ✅ DONE
│
├── outputs/
│   └── <pdf_name>/                  # One folder per PDF
│       ├── page_1/
│       │   ├── interim.json         # Raw extraction
│       │   └── mapped.json          # Final mapped output
│       ├── page_2/
│       │   ├── interim.json
│       │   └── mapped.json
│       └── ...
│
├── sample_pdfs/
│   └── PR-Register.pdf              # Test file
│
└── design_phase/                    # Design documentation
    ├── 01_schema_design.md
    └── 02_code_structure.md
```

## Pipeline Flow

### Usage:
```bash
python main.py PR-Register.pdf
```

### Steps:
1. **Step 1**: Extract all pages → List[{page_number, text}]
2. **For each page**:
   - Step 2: Raw extraction → interim.json
   - Step 3: Map to schema → mapped.json
   - Save to `outputs/<pdf_name>/page_<N>/`
3. Done

### Key Differences from Financial Code:

❌ **NO Classifier** - No step2_sfp_classifier.py (all pages are payroll)  
✅ **Page-by-Page** - Each page processed independently  
✅ **Per-Page Folders** - outputs/<pdf_name>/page_N/ structure

## Important Rules

### DO:
- Keep code simple and clean
- Process each page independently
- Save interim and mapped JSON per page
- Only populate fields that exist in interim JSON

### DON'T:
- No inference or calculations
- No summary reports
- No complex logging
- Never guess or fill missing values
- Keep fields empty/null if not found

## Two-Pass LLM Approach

**Pass 1 (Raw Extraction):**
- Extract ALL data as-is from page
- Handle multiple employees per page
- Output: interim.json (flat structure, not yet grouped)

**Pass 2 (Schema Mapping):**
- Group data by employee
- Populate all 4 parent fields (only if data exists)
- Map to global schema structure
- Output: mapped.json

## Next Steps:
1. Create main.py
2. Create step1_pdf_extraction.py
3. Create step2_raw_extraction.py + extractor_prompt.py
4. Create step3_schema_mapping.py + mapper_prompt.py
5. Create step4_validation.py (placeholder)
6. Test with PR-Register.pdf
