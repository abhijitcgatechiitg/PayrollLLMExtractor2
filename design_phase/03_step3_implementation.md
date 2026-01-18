# Step 3 Schema Mapping - Implementation Details

## Overview
Step 3 takes the interim JSON from Step 2 and maps it to the global payroll schema using an LLM.

## File: src/step3_schema_mapping.py

### SchemaMapper Class

#### `__init__(model="claude-haiku-4-5-20251001")`
**Purpose**: Initialize the mapper with Anthropic client
- Loads environment variables from `.env` file
- Gets `ANTHROPIC_API_KEY` from environment
- Creates Anthropic client instance
- Sets the Claude model to use

**Error Handling**: Raises `ValueError` if API key is missing

---

#### `map_to_global_schema(interim_data, page_number)`
**Purpose**: Main function that performs the mapping from interim JSON to global schema

**Input**:
- `interim_data`: Dictionary containing raw extracted data from Step 2
- `page_number`: Integer indicating which page is being processed

**Process**:
1. Converts interim data dictionary to JSON string
2. Gets schema structure example using `_get_schema_example()`
3. Builds complete mapping prompt using `get_mapper_prompt()` from prompts/mapper_prompt.py
4. Calls Claude API with:
   - Model: claude-haiku-4-5-20251001
   - Max tokens: 16000 (larger than extraction due to verbose schema output)
   - Temperature: 0 (deterministic mapping)
5. Extracts response text from Claude
6. Parses JSON from response using `_extract_json_from_response()`
7. Validates structure using `validate_mapped_format()`
8. Returns mapped data dictionary

**Output**: Dictionary following global schema structure

**Error Handling**: Raises exception if API call fails or validation fails

---

#### `_get_schema_example()`
**Purpose**: Generate a simplified text description of the global schema structure

**Why Needed**: 
- The full global schema with all nested field definitions is very verbose
- Sending the entire structure would waste tokens
- A simplified description is sufficient for the LLM to understand the target format

**Output**: Multi-line string describing the schema sections:
1. metadata section
2. balance_employee_tax (page-level aggregates)
3. balance_employer_tax (page-level aggregates)
4. company_totals section
5. employee_info array
6. unmapped_items section

Also describes the field wrapper structure: `{value, confidence, mapped_from, notes}`

---

#### `_extract_json_from_response(response_text)`
**Purpose**: Parse JSON from LLM response, handling markdown formatting

**Why Needed**: Claude sometimes wraps JSON in markdown code blocks like:
```
```json
{ ... }
```
```

**Process**:
1. Strips whitespace from response text
2. Removes opening markdown markers (````json` or `````)
3. Removes closing markdown markers (`````)
4. Attempts to parse as JSON
5. If parsing fails, prints error and first 500 characters for debugging

**Output**: Dictionary parsed from JSON

**Error Handling**: Raises `json.JSONDecodeError` if parsing fails

---

#### `validate_mapped_format(data)`
**Purpose**: Validate that mapped data follows the global schema structure

**Validation Checks**:
1. **Top-level keys**: Ensures all required keys are present:
   - metadata
   - balance_employee_tax
   - balance_employer_tax
   - company_totals
   - employee_info
   - unmapped_items

2. **Type checking**: Verifies `employee_info` is a list/array

3. **Employee structure**: For each employee, checks for required sections:
   - employee_details
   - balance_earnings
   - balance_deductions
   - balance_employee_tax

**Output**: Boolean (True if valid, False if validation fails)

**Side Effects**: Prints validation failure messages for debugging

---

### Standalone Functions

#### `map_interim_to_global(interim_json_path, output_json_path, page_number)`
**Purpose**: Convenience function for file-based mapping

**Process**:
1. Loads interim JSON from file
2. Creates SchemaMapper instance
3. Calls `map_to_global_schema()`
4. Creates output directory if needed
5. Saves mapped data to output file
6. Returns mapped data

**Use Case**: Simplifies external calls by handling all file I/O

---

### Main Section (`if __name__ == "__main__"`)
**Purpose**: Allow command-line execution of the mapper

**Usage**: 
```bash
python step3_schema_mapping.py <interim_json_path> <output_json_path> <page_number>
```

**Example**:
```bash
python step3_schema_mapping.py outputs/PR-Register/page_1/interim.json outputs/PR-Register/page_1/mapped.json 1
```

---

## Key Design Decisions

### 1. LLM-Based Mapping
**Why**: Payroll formats vary significantly. LLM can handle:
- Different field names and aliases
- Missing or optional fields
- Intelligent inference (e.g., tax jurisdiction classification)
- Flexible mapping logic without hardcoded rules

### 2. Confidence Scoring
**Why**: Track mapping certainty for downstream validation
- 1.0 = Direct mapping
- 0.9-0.95 = Simple transformation
- 0.8-0.85 = Inference required
- Lower = Uncertain mapping

### 3. mapped_from Field
**Why**: Traceability - know exactly where each value came from in the interim JSON
- Enables debugging
- Allows verification
- Supports auditing

### 4. Large Token Budget (16000)
**Why**: Global schema output is verbose with all the field wrappers
- Each field has 4 properties (value, confidence, mapped_from, notes)
- Multiple employees with arrays of earnings/deductions/taxes
- Company totals section
- Need room for complete, well-formed JSON

### 5. Temperature 0
**Why**: Mapping should be deterministic
- Same input should produce same output
- No creative interpretation needed
- Consistency across multiple runs

---

## Integration with Other Components

### Inputs From:
- **Step 2 (step2_raw_extraction.py)**: Interim JSON with raw extracted data
- **prompts/mapper_prompt.py**: Detailed mapping instructions and rules
- **schema/global_schema.py**: Target schema structure (used for validation)

### Outputs To:
- **Step 4 (step4_validation.py)**: Mapped JSON for validation (future)
- **main.py**: Orchestrator that runs the full pipeline

---

## Testing
Test file: `testing/test_mapping.py`
- Loads `test_page1_interim.json`
- Runs mapping
- Saves to `test_page1_mapped.json`
- Prints summary of mapped data
