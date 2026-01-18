# Ground Truth for PR-Register.pdf

This folder contains manually verified ground truth data for accuracy testing.

## Files Structure

- `ground_truth_page_1.json` - Manually verified correct extraction for page 1
- `ground_truth_page_2.json` - Manually verified correct extraction for page 2
- `metadata.json` - Document information

## How to Create Ground Truth

1. **Copy the current extraction output** from `outputs/PR-Register/page_N/mapped.json`
2. **Manually verify each field** by looking at the original PDF
3. **Correct any errors** - Fix incorrect values
4. **Update confidence** - Set to 1.0 for fields that are correctly extractable, 0.0 for truly missing
5. **Save as** `ground_truth_page_N.json`

## Ground Truth Standards

- **For exact matches**: Value must exactly match what's in the PDF
- **For missing data**: Set value to null and confidence to 0.0
- **For amounts**: Include exact formatting (e.g., "1,234.56" not "1234.56")
- **For dates**: Use exact format from PDF (e.g., "03/23/14")
- **For names**: Use exact capitalization and spacing

## Fields to Verify Carefully

1. **Employee names** - Exact spelling and capitalization
2. **Amounts** - Correct values and decimal places
3. **Dates** - Correct format
4. **QTD/YTD values** - Often similar, easy to mix up
5. **Tax codes** - Multiple similar codes exist
6. **Employee IDs** - Check all digits

## Annotation Process

When creating ground truth:
1. Open the PDF side-by-side with the JSON
2. Go through each employee one by one
3. Verify every single field value
4. Mark any extraction errors
5. Document any ambiguous cases in comments
