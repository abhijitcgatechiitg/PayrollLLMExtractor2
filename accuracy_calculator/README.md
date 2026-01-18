# Accuracy Calculator

Simple tool to measure field-level accuracy of payroll extraction by comparing against manually verified ground truth data.

## 📁 Folder Structure

```
accuracy_calculator/
├── README.md                    # This file
├── calculate_accuracy.py        # Main accuracy calculation script
└── prepare_ground_truth.py      # Helper to create ground truth templates

golden_dataset/
└── PR-Register/
    ├── README.md                # Annotation guidelines
    ├── metadata.json            # Document information
    ├── ground_truth_page_1.json # Manually verified data (you create this)
    └── ground_truth_page_2.json # Manually verified data (you create this)
```

## 🚀 Quick Start

### Step 1: Prepare Ground Truth Template

Copy extraction output to golden dataset folder:

```bash
python accuracy_calculator/prepare_ground_truth.py PR-Register 1
```

This creates `golden_dataset/PR-Register/ground_truth_page_1.json`

### Step 2: Manually Verify Data

1. Open `golden_dataset/PR-Register/ground_truth_page_1.json`
2. Open `sample_pdfs/PR-Register.pdf` (page 1)
3. Go through each field and verify/correct the values
4. Save the corrected file

### Step 3: Calculate Accuracy

Compare extraction output against your verified ground truth:

```bash
python accuracy_calculator/calculate_accuracy.py outputs/PR-Register/page_1/mapped.json golden_dataset/PR-Register/ground_truth_page_1.json
```

## 📊 What You Get

### Console Output (Client-Friendly):
```
======================================================================
ACCURACY REPORT
======================================================================

📊 Overall Accuracy: 94.50%

📈 Field Statistics:
   Total Fields Checked: 200
   ✅ Correct: 189
   ❌ Incorrect: 8
   ⚠️  Missing: 3

❌ Issues Found (11 total):
   ❌ employee_info[2].earnings[1].ytd
      Expected: 1,234.56
      Got: 1,234.50
   ⚠️ employee_info[5].deductions[0].description
      Expected: Health Insurance
      Got: null
...

======================================================================
```

### Detailed Report File:
Saved as `accuracy_report.json` in the same folder as the extraction:
```json
{
  "timestamp": "2026-01-18T...",
  "summary": {
    "total_fields": 200,
    "correct_fields": 189,
    "incorrect_fields": 8,
    "missing_fields": 3,
    "accuracy_percentage": 94.5
  },
  "field_details": [...]
}
```

## 🎯 Accuracy Metrics Explained

- **Total Fields**: All fields in the schema that have ground truth values
- **Correct**: Extracted value exactly matches ground truth
- **Incorrect**: Extracted value doesn't match ground truth
- **Missing**: Field was not extracted (null/empty when it shouldn't be)
- **Accuracy %**: (Correct / Total) × 100

## 📋 Complete Workflow Example

```bash
# 1. Run extraction pipeline (if not already done)
python main.py sample_pdfs/PR-Register.pdf

# 2. Prepare ground truth for page 1
python accuracy_calculator/prepare_ground_truth.py PR-Register 1

# 3. Manually verify and correct the ground truth file
# (Open golden_dataset/PR-Register/ground_truth_page_1.json and edit)

# 4. Calculate accuracy
python accuracy_calculator/calculate_accuracy.py \
  outputs/PR-Register/page_1/mapped.json \
  golden_dataset/PR-Register/ground_truth_page_1.json

# 5. Repeat for page 2
python accuracy_calculator/prepare_ground_truth.py PR-Register 2
# (edit ground_truth_page_2.json)
python accuracy_calculator/calculate_accuracy.py \
  outputs/PR-Register/page_2/mapped.json \
  golden_dataset/PR-Register/ground_truth_page_2.json
```

## 💡 Tips for Creating Ground Truth

1. **Be Precise**: Match exact formatting from PDF (commas, decimals, spaces)
2. **Check QTD vs YTD**: These are easy to mix up
3. **Verify All Employees**: Don't skip any
4. **Use Null for Missing**: If data truly isn't in PDF, use `null` with confidence `0.0`
5. **Double Check Numbers**: Most common errors are in amounts

## 🔍 What Gets Compared

The accuracy calculator compares all fields with `{value, confidence}` structure:
- Employee names, IDs, status
- All earnings (regular, overtime, bonuses, etc.)
- All deductions (insurance, retirement, etc.)
- All taxes (federal, state, local, etc.)
- Balance totals (QTD and YTD)
- Company metadata (dates, payroll number, etc.)

**Not compared**: Metadata like `extraction_timestamp`, `source_file`

## 📝 Client Presentation

When showing results to clients, focus on:
1. **Overall Accuracy %** - The headline number
2. **Total Fields Checked** - Shows thoroughness
3. **Correct vs Incorrect breakdown** - Shows reliability
4. **Example Issues** - Shows transparency about errors

The client-friendly console output is designed for easy screenshots/presentations.
