"""
Mapper Prompt - Maps interim JSON to global schema
"""

def get_mapper_prompt(interim_json: str, global_schema_example: str) -> str:
    """
    Generate the prompt for mapping interim JSON to global schema.
    
    Args:
        interim_json: The raw extracted data from step 2
        global_schema_example: Example of the target global schema structure
    
    Returns:
        Complete prompt for the mapper LLM
    """
    
    prompt = f"""You are a payroll data mapping specialist. Your task is to map raw payroll data from an interim JSON format into a structured global schema.

# YOUR TASK
Map the provided interim JSON data to the global payroll schema. Follow the mapping rules carefully to ensure data integrity and proper field population.

# INTERIM JSON DATA (Raw Extraction)
```json
{interim_json}
```

# TARGET GLOBAL SCHEMA STRUCTURE
{global_schema_example}

# MAPPING RULES

## 1. METADATA MAPPING
- Map `page_metadata` from interim JSON to `metadata` in global schema
- Fields to map:
  * company_name → company_name
  * company_number → company_number  
  * payroll_number → payroll_number
  * pay_period_start → pay_period_start
  * pay_period_end → pay_period_end
  * check_date → check_date
  * page_number → page_number
- Set confidence to 1.0 for direct mappings

## 2. EMPLOYEE_INFO MAPPING
- Each employee in `interim.employees[]` becomes one entry in `global.employee_info[]`
- Preserve the order of employees from the interim JSON

### 2.1 Employee Details Section
Map these fields for each employee:
- employee_id → employee_number (confidence: 1.0)
- employee_name → fullname (confidence: 1.0)
- ssn → ssn (confidence: 1.0)
- department → department_number (confidence: 1.0)
- pay_frequency → pay_frequency (confidence: 1.0)
- payment_type → payment_type (confidence: 1.0)
- tax_status_federal → tax_status_federal (confidence: 1.0)
- tax_exemptions_federal → tax_exemptions_federal (confidence: 1.0)
- tax_status_state → tax_status_state (confidence: 1.0)
- tax_exemptions_state → tax_exemptions_state (confidence: 1.0)
- state → state (confidence: 1.0)
- Use pay_period_start and pay_period_end from page_metadata for employee-level dates

### 2.2 Balance Earnings Section
For each earning in `interim.employees[].earnings[]`:
- earning_code: Map from "code" field (e.g., "0-Regular Pay")
- earning_description: Map from "description" field
- rate: Map from "rate" field
- earning_qtd_hours: Map from "current_hours"
- earning_qtd_amount: Map from "current_amount"
- earning_ytd_hours: Map from "ytd_hours"
- earning_ytd_amount: Map from "ytd_amount"
- Set confidence to 1.0 for all direct mappings

### 2.3 Balance Deductions Section
For each deduction in `interim.employees[].deductions[]`:
- deduction_code: Map from "code" field (e.g., "4-401K Plan")
- deduction_description: Map from "description" field
- deduction_qtd_amount: Map from "current_amount"
- deduction_ytd_amount: Map from "ytd_amount"
- deduction_qtd_hours: Map from "current_hours" (may be null)
- deduction_ytd_hours: Map from "ytd_hours" (may be null)
- Set confidence to 1.0 for direct mappings

### 2.4 Balance Employee Tax Section
For each tax in `interim.employees[].taxes[]`:
- tax_code: Map from "code" field (e.g., "Federal WH")
- tax_description: Map from "description" field
- tax_qtd_amount: Map from "current_amount"
- tax_ytd_amount: Map from "ytd_amount"
- tax_jurisdiction: Infer from tax code:
  * "Federal WH", "OASDI", "Medicare" → "Federal"
  * "State WH", "MA State WH", "CA State WH" → "State"
  * Others → analyze and classify (confidence: 0.8-0.9 if inferred)
- Set confidence to 1.0 for direct mappings, 0.8-0.9 for inferred fields (like tax_jurisdiction)

## 3. COMPANY_TOTALS MAPPING
Only populate this section if `interim.company_totals` exists and has data.

### 3.1 Company Period Dates
- com_period_start_date: Map from company_totals.period_start (if present)
- com_period_end_date: Map from company_totals.period_end (if present)

### 3.2 Company Earnings
For each earning in `interim.company_totals.earnings[]`:
- com_earning_code: Map from "code"
- com_earning_qtd_hours: Map from "current_hours"
- com_earning_qtd_amount: Map from "current_amount"
- com_earning_ytd_hours: Map from "ytd_hours"
- com_earning_ytd_amount: Map from "ytd_amount"

### 3.3 Company Deductions
For each deduction in `interim.company_totals.deductions[]`:
- com_deduction_code: Map from "code"
- com_deduction_qtd_hours: Map from "current_hours"
- com_deduction_qtd_amount: Map from "current_amount"
- com_deduction_ytd_hours: Map from "ytd_hours"
- com_deduction_ytd_amount: Map from "ytd_amount"

### 3.4 Company Employee Taxes
For each employee tax in `interim.company_totals.employee_taxes[]`:
- com_tax_code: Map from "code"
- com_tax_amount: Use "ytd_amount" or "current_amount" based on what's available

### 3.5 Company Employer Taxes
For each employer tax in `interim.company_totals.employer_taxes[]`:
- com_tax_code: Map from "code"
- com_tax_amount: Use "ytd_amount" or "current_amount" based on what's available

## 4. PAGE-LEVEL TAX AGGREGATES
**IMPORTANT**: These are currently NOT populated in this implementation.
- balance_employee_tax (page-level) → Leave as empty array []
- balance_employer_tax (page-level) → Leave as empty array []
- Rationale: Company totals already capture aggregate taxes; page-level aggregates would be redundant

## 5. CONFIDENCE SCORING GUIDELINES
- **1.0**: Direct field-to-field mapping with no transformation
- **0.95**: Direct mapping with minor formatting (e.g., removing commas from numbers)
- **0.9**: Mapping with simple inference (e.g., extracting code from "0-Regular Pay")
- **0.8-0.85**: Mapping with moderate inference (e.g., classifying tax jurisdiction)
- **0.7-0.75**: Mapping with significant inference or uncertainty
- **0.5 or below**: Low confidence; data might be ambiguous

## 6. UNMAPPED ITEMS
- If any field in interim JSON cannot be mapped to the global schema, add it to the appropriate `unmapped_items` section
- Employee-specific unmapped data goes to `employee_info[].unmapped_items`
- Page-level unmapped data goes to the root `unmapped_items`

## 7. NULL HANDLING
- If a field is null or missing in interim JSON, leave it as null in global schema
- Set confidence to 0.0 for null/missing fields

## 8. SPECIAL CASES

### Check Numbers
- Check numbers are in interim JSON but NOT in the global schema
- Add to employee-level unmapped_items if needed

### Numeric Values with Formatting
- Remove commas from numbers: "5,530.00" → "5530.00"
- Keep as strings if decimal precision matters

### Masked/Redacted Data
- Preserve masked SSNs as-is: "*******6132" → "*******6132"

### Empty Arrays
- If employee has no deductions, balance_deductions should be an empty array []
- Same applies to earnings, taxes, etc.

# OUTPUT FORMAT
Return ONLY the mapped global schema JSON. Do NOT include any explanations, markdown formatting, or additional text.

The output must be valid JSON following the exact structure of the global schema.

# EXAMPLE OUTPUT STRUCTURE (abbreviated)
```json
{{
  "document_type": "PayrollRegister",
  "metadata": {{
    "company_name": {{
      "value": "The Sample Company",
      "confidence": 1.0
    }},
    ...
  }},
  "balance_employee_tax": [],
  "balance_employer_tax": [],
  "company_totals": {{
    "com_balance_earnings": [...],
    ...
  }},
  "employee_info": [
    {{
      "employee_details": {{
        "fullname": {{
          "value": "Doe, John",
          "confidence": 1.0
        }},
        ...
      }},
      "balance_earnings": [...],
      "balance_deductions": [...],
      "balance_employee_tax": [...],
      "unmapped_items": {{
        "items": [],
        "reason": ""
      }}
    }}
  ],
  "unmapped_items": {{
    "items": [],
    "reason": ""
  }}
}}
```

Now, perform the mapping and return the complete mapped global schema JSON.
"""
    
    return prompt
