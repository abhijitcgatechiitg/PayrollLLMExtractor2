"""
Step 2: Raw Data Extractor Prompt
This prompt tells Claude to extract payroll data AS-IS from the PDF page.
The goal is to preserve all data exactly as it appears, with clear employee boundaries.
"""

EXTRACTOR_PROMPT_TEMPLATE = """You are a payroll data extraction specialist. Your task is to extract ALL payroll data from a Payroll Register page EXACTLY as it appears in the document.

CRITICAL RULES:
1. Extract data AS-IS - do NOT normalize, calculate, or infer anything
2. Preserve exact labels, codes, and values from the PDF
3. Identify and maintain EMPLOYEE BOUNDARIES - each employee is a separate record
4. Extract ALL fields for each employee: personal info, earnings, deductions, taxes
5. Preserve QTD (current period) and YTD (year-to-date) values separately
6. Include page-level metadata (company name, pay period, check date, etc.)
7. Do NOT skip any employees or data fields
8. If a value is missing, dash (-), or unclear, use null

OUTPUT STRUCTURE:
Return ONLY a valid JSON object (no markdown, no extra text) with this structure:

{{
  "page_metadata": {{
    "company_name": "extracted company name or null",
    "company_number": "Co. No. or null",
    "payroll_number": "Payroll # or null",
    "pay_period_start": "start date or null",
    "pay_period_end": "end date or null",
    "check_date": "check date or null",
    "page_number": "page number or null"
  }},
  "employees": [
    {{
      "employee_id": "unique identifier for this employee (Emp. No.)",
      "employee_name": "full name",
      "ssn": "SSN (may be masked)",
      "department": "Dept. number or null",
      "check_number": "Ck. No. or null",
      "payment_type": "DD/Check or null",
      "pay_frequency": "Weekly/Biweekly/etc or null",
      "tax_status_federal": "Single/Married or null",
      "tax_exemptions_federal": "number or null",
      "tax_status_state": "Single/Married or null", 
      "tax_exemptions_state": "number or null",
      "state": "state abbreviation or null",
      "earnings": [
        {{
          "code": "earning code with description (e.g., '0-Regular Pay')",
          "description": "human readable description",
          "rate": "rate value or null",
          "current_hours": "current period hours or null",
          "current_amount": "current period amount or null",
          "ytd_hours": "year-to-date hours or null",
          "ytd_amount": "year-to-date amount or null"
        }}
      ],
      "deductions": [
        {{
          "code": "deduction code with description (e.g., '4-401K Plan')",
          "description": "human readable description",
          "current_amount": "current period amount or null",
          "ytd_amount": "year-to-date amount or null",
          "current_hours": "current period hours if applicable or null",
          "ytd_hours": "year-to-date hours if applicable or null"
        }}
      ],
      "taxes": [
        {{
          "code": "tax code (e.g., 'Federal WH', 'OASDI', 'Medicare')",
          "description": "tax description",
          "current_amount": "current period amount or null",
          "ytd_amount": "year-to-date amount or null",
          "jurisdiction": "Federal/State/Local or null"
        }}
      ],
      "totals": {{
        "total_current_earnings": "if shown or null",
        "total_ytd_earnings": "if shown or null",
        "net_pay": "if shown or null"
      }}
    }}
  ],
  "company_totals": {{
    "total_earnings": [
      {{
        "earning_code": "code or description",
        "total_qtd_hours": "current period total hours or null",
        "total_qtd_amount": "current period total amount or null",
        "total_ytd_hours": "year-to-date total hours or null",
        "total_ytd_amount": "year-to-date total amount or null"
      }}
    ],
    "total_deductions": [
      {{
        "deduction_code": "code or description",
        "total_qtd_amount": "current period total amount or null",
        "total_ytd_amount": "year-to-date total amount or null"
      }}
    ],
    "total_employee_taxes": [
      {{
        "tax_code": "tax code or description",
        "total_qtd_amount": "current period total amount or null",
        "total_ytd_amount": "year-to-date total amount or null"
      }}
    ],
    "total_employer_taxes": [
      {{
        "tax_code": "tax code or description",
        "total_qtd_amount": "current period total amount or null",
        "total_ytd_amount": "year-to-date total amount or null"
      }}
    ],
    "department_totals": [
      {{
        "department": "department number or name",
        "total_amount": "total for this department or null"
      }}
    ]
  }}
}}
```

**Note:** The example above shows empty company_totals arrays. Company totals are OPTIONAL - many payroll registers may not have them. Only populate company_totals if you see clear summary/total rows at the bottom of the page that aggregate data across all employees (e.g., "TOTAL REGULAR PAY: 10,000" or "TOTAL 401K DEDUCTIONS: 500"). If no company totals are present, use empty arrays for each category.


IMPORTANT EXTRACTION GUIDELINES:


**Employee Boundaries:**
- Each row in the payroll register = one employee
- Keep all data grouped by employee
- Look for employee name, SSN, Emp No to identify boundaries

**Earnings Extraction:**
- Multiple earning types per employee are common (Regular Pay, Sick Pay, Vacation, Bonus, etc.)
- Each earning type gets its own entry in the "earnings" array
- Preserve the code (e.g., "0-Regular Pay", "1-Vacation Pay")
- Extract Rate, Hours, and Amount (both current and YTD)

**Deductions Extraction:**
- Multiple deduction types per employee (401K, Medical, Dental, Child Support, etc.)
- Each deduction gets its own entry in "deductions" array  
- Preserve the code (e.g., "4-401K Plan", "2-CAF Medical")
- Extract both current and YTD amounts

**Taxes Extraction:**
- Multiple tax types per employee (Federal WH, OASDI, Medicare, State WH, etc.)
- Each tax gets its own entry in "taxes" array
- Identify jurisdiction: Federal (Federal WH), State (MA: State WH), FICA (OASDI, Medicare)
- Extract both current and YTD amounts

**Column Mapping:**
Typical payroll register columns:
- Employee info: Name, SSN, Emp No, Dept
- Earnings: Description, Rate, Hours (Current), Pay (Current), Hours (YTD), Amount (YTD)
- Deductions: Description, Current, YTD
- Taxes: Description, Current, YTD
- Payment: Type (DD/Check), Net Pay, Ck. No.


**Company-Level Totals:**
- Look for summary rows AFTER all employees (often at page bottom)
- Extract any "Total" or "Subtotal" rows that aggregate across all employees
- Capture department subtotals if shown
- Include any company-wide earnings, deductions, or tax totals
- These are typically separate from individual employee data
- If no company totals are present, use empty arrays for each category
yourself - only extract what's explicitly shown
- Do NOT convert data types or formats
- Do NOT infer missing values
- Do NOT combine fields or create new fields
- Do NOT skip employees even if data seems incomplete
- Do NOT invent company totals - only capture if clearly shown in the documentd Support", "M2-401(k) ER M")
- Tax status: Look for "Fed:" and state labels with Single/Married and exemption numbers

**What NOT to do:**
- Do NOT calculate totals or aggregates
- Do NOT convert data types or formats
- Do NOT infer missing values
- Do NOT combine fields or create new fields
- Do NOT skip employees even if data seems incomplete

EXAMPLE (for reference):
If you see:
```
Employee Name: Golikowski, Roger D.    Emp. No.: 2001015    SSN: *******6132    Dept: 1
Pay: Weekly    Status: Married (0 Fed, 0 MA)    Type: DD    Ck. No.: 342.86
Earnings:
  0-Regular Pay    Rate: 19.75    Hours: 40.00    Amount: 790.00    YTD Hours: 280.00    YTD: 5,530.00
Deductions:
  4-401K Plan    Current: 23.70    YTD: 165.90
Taxes:
  Federal WH    Current: 48.98    YTD: 342.86
  OASDI         Current: 46.54    YTD: 325.80
  Medicare      Current: 10.88    YTD: 76.20
  MA: State WH  Current: 36.71    YTD: 256.93
```

Extract as:
```json
{{page_metadata": {{
    "company_name": "The Sample Company",
    "payroll_number": "198",
    "pay_period_start": "03/23/14",
    "pay_period_end": "03/29/14",
    "check_date": "04/04/14",
    "page_number": "1"
  }},
  "page_totals": {{
    "total_earnings": [],
    "total_deductions": [],
    "total_employee_taxes": [],
    "total_employer_taxes": [],
    "department_totals": []
  }},
  "employees": [
    {{
      "
  "employee_id": "2001015",
  "employee_name": "Golikowski, Roger D.",
  "ssn": "*******6132",
  "department": "1",
  "check_number": "342.86",
  "payment_type": "DD",
  "pay_frequency": "Weekly",
  "tax_status_federal": "Married",
  "tax_exemptions_federal": "0",
  "tax_status_state": "Married",
  "tax_exemptions_state": "0",
  "state": "MA",
  "earnings": [
    {{
      "code": "0-Regular Pay",
      "description": "Regular Pay",
      "rate": "19.75",
      "current_hours": "40.00",
      "current_amount": "790.00",
      "ytd_hours": "280.00",
      "ytd_amount": "5,530.00"
    }}
  ],
  "deductions": [
    {{
      "code": "4-401K Plan",
      "description": "401K Plan",
      "current_amount": "23.70",
      "ytd_amount": "165.90",
      "current_hours": null,
      "ytd_hours": null
    }}
  ],
  "taxes": [
    {{
      "code": "Federal WH",
      "description": "Federal Withholding",
      "current_amount": "48.98",
      "ytd_amount": "342.86",
      "jurisdiction": "Federal"
    }},
    {{
      "code": "OASDI",
      "description": "Social Security",
      "current_amount": "46.54",
      "ytd_amount": "325.80",
      "jurisdiction": "Federal"
    }},
    {{
      "code": "Medicare",
    }}
  ]
}}
```

**Note:** The example above shows empty page_totals arrays because individual employee example doesn't show page-level totals. If your page has summary rows like "TOTAL REGULAR PAY: 10,000" or "TOTAL 401K DEDUCTIONS: 500", capture those in the page_totals section.   "current_amount": "10.88",
      "ytd_amount": "76.20",
      "jurisdiction": "Federal"
    }},
    {{
      "code": "MA: State WH",
      "description": "Massachusetts State Withholding",
      "current_amount": "36.71",
      "ytd_amount": "256.93",
      "jurisdiction": "State"
    }}
  ],
  "totals": {{
    "total_current_earnings": "790.00",
    "total_ytd_earnings": "5,530.00",
    "net_pay": null
  }}

Now extract ALL payroll data from this page:

--- PAYROLL PAGE TEXT START ---
{}
--- PAYROLL PAGE TEXT END ---

Return ONLY the JSON object. No explanations, no markdown formatting.
"""


def get_extractor_prompt(page_text: str) -> str:
    """
    Format the extractor prompt with actual page text.
    
    Args:
        page_text: The text extracted from a single PDF page
        
    Returns:
        Formatted prompt ready to send to LLM
    """
    return EXTRACTOR_PROMPT_TEMPLATE.format(page_text)
