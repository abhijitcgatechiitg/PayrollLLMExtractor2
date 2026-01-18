"""
Global Schema for Payroll Register Data Extraction

Design Principles:
1. Employee-centric: Each employee is a separate record
2. Flexible deductions/earnings/taxes: Support multiple codes per employee
3. QTD/YTD tracking: Both current period and year-to-date values
4. Page metadata: Track source page, pay period, company info
5. Confidence tracking: Each mapped field includes confidence score (simplified to value + confidence only)
6. Unmapped items: Capture items that don't fit the schema

Structure Philosophy:
- This schema captures ONLY the essential payroll fields
- Not all interim data will be mapped (by design)
- Focus on: employee details, earnings, deductions, taxes, net pay
- Company totals are optional (can be calculated if needed)

SIMPLIFIED STRUCTURE (removed mapped_from and notes to reduce token usage):
- Each field now has only: {value, confidence}
- This reduces output size by ~30-40% while keeping essential information
"""

GLOBAL_PAYROLL_SCHEMA = {
    "document_type": "PayrollRegister",
    
    # Page-level metadata
    "metadata": {
        "company_name": None,
        "company_number": None,
        "payroll_number": None,
        "pay_period_start": None,
        "pay_period_end": None,
        "check_date": None,
        "page_number": None,
        "extraction_timestamp": None,
        "source_file": None
    },
    
    # Parent Field 1: Page-level employee tax totals (aggregated across all employees)
    "balance_employee_tax": [
        {
            "tax_code": {
                "value": None,
                "confidence": 0.0
            },
            "tax_amount": {
                "value": None,
                "confidence": 0.0
            }
        }
    ],
    
    # Parent Field 2: Page-level employer tax totals (aggregated across all employees)
    "balance_employer_tax": [
        {
            "tax_code": {
                "value": None,
                "confidence": 0.0
            },
            "tax_amount": {
                "value": None,
                "confidence": 0.0
            }
        }
    ],
    
    # Parent Field 3: Company-level totals (aggregated summaries)
    "company_totals": {
        "com_period_start_date": {
            "value": None,
            "confidence": 0.0
        },
        "com_period_end_date": {
            "value": None,
            "confidence": 0.0
        },
        "com_balance_earnings": [
            {
                "com_earning_code": {
                    "value": None,
                    "confidence": 0.0
                },
                "com_earning_qtd_hours": {
                    "value": None,
                    "confidence": 0.0
                },
                "com_earning_qtd_amount": {
                    "value": None,
                    "confidence": 0.0
                },
                "com_earning_ytd_hours": {
                    "value": None,
                    "confidence": 0.0
                },
                "com_earning_ytd_amount": {
                    "value": None,
                    "confidence": 0.0
                }
            }
        ],
        "com_balance_deductions": [
            {
                "com_deduction_code": {
                    "value": None,
                    "confidence": 0.0
                },
                "com_deduction_qtd_hours": {
                    "value": None,
                    "confidence": 0.0
                },
                "com_deduction_qtd_amount": {
                    "value": None,
                    "confidence": 0.0
                },
                "com_deduction_ytd_hours": {
                    "value": None,
                    "confidence": 0.0
                },
                "com_deduction_ytd_amount": {
                    "value": None,
                    "confidence": 0.0
                }
            }
        ],
        "com_balance_employee_tax": [
            {
                "com_tax_code": {
                    "value": None,
                    "confidence": 0.0
                },
                "com_tax_amount": {
                    "value": None,
                    "confidence": 0.0
                }
            }
        ],
        "com_balance_employer_tax": [
            {
                "com_tax_code": {
                    "value": None,
                    "confidence": 0.0
                },
                "com_tax_amount": {
                    "value": None,
                    "confidence": 0.0
                }
            }
        ]
    },
    
    # Parent Field 4: Employee-level information (array of all employees on this page)
    "employee_info": [
        # Each employee follows this structure:
        {
            "employee_details": {
                "employee_number": {
                    "value": None,
                    "confidence": 0.0
                },
                "fullname": {
                    "value": None,
                    "confidence": 0.0
                },
                "ssn": {
                    "value": None,
                    "confidence": 0.0
                },
                "department_number": {
                    "value": None,
                    "confidence": 0.0
                },
                "pay_frequency": {
                    "value": None,
                    "confidence": 0.0
                },
                "payment_type": {
                    "value": None,
                    "confidence": 0.0
                },
                "tax_status_federal": {
                    "value": None,
                    "confidence": 0.0
                },
                "tax_exemptions_federal": {
                    "value": None,
                    "confidence": 0.0
                },
                "tax_status_state": {
                    "value": None,
                    "confidence": 0.0
                },
                "tax_exemptions_state": {
                    "value": None,
                    "confidence": 0.0
                },
                "state": {
                    "value": None,
                    "confidence": 0.0
                },
                "pay_period_start_date": {
                    "value": None,
                    "confidence": 0.0
                },
                "pay_period_end_date": {
                    "value": None,
                    "confidence": 0.0
                }
            },
            
            # Earnings section (can have multiple earning types)
            "balance_earnings": [
                {
                    "earning_code": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "earning_description": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "rate": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "earning_qtd_hours": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "earning_qtd_amount": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "earning_ytd_hours": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "earning_ytd_amount": {
                        "value": None,
                        "confidence": 0.0
                    }
                }
            ],
            
            # Deductions section (can have multiple deduction types)
            "balance_deductions": [
                {
                    "deduction_code": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "deduction_description": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "deduction_qtd_amount": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "deduction_ytd_amount": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "deduction_qtd_hours": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "deduction_ytd_hours": {
                        "value": None,
                        "confidence": 0.0
                    }
                }
            ],
            
            # Taxes section (employee taxes)
            "balance_employee_tax": [
                {
                    "tax_code": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "tax_description": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "tax_qtd_amount": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "tax_ytd_amount": {
                        "value": None,
                        "confidence": 0.0
                    },
                    "tax_jurisdiction": {
                        "value": None,
                        "confidence": 0.0
                    }
                }
            ],
            
            # Unmapped items specific to this employee
            "unmapped_items": {
                "items": [],
                "reason": "Items that couldn't be mapped to schema"
            }
        }
    ],
    
    # Page-level unmapped items (not employee-specific)
    "unmapped_items": {
        "items": [],
        "reason": "Items that couldn't be mapped to any employee or metadata"
    }
}


# Field descriptions for LLM mapping assistance
FIELD_DESCRIPTIONS = {
    "metadata": {
        "company_name": "Name of the company/organization",
        "company_number": "Company number or identifier",
        "payroll_number": "Payroll run or batch number",
        "pay_period_start": "Start date of the pay period",
        "pay_period_end": "End date of the pay period",
        "check_date": "Date checks are issued or payment is made",
        "page_number": "Page number from source document",
        "source_file": "Name of the source PDF file"
    },
    "balance_employee_tax": {
        "tax_code": "Code identifying the type of employee tax (page-level aggregate)",
        "tax_amount": "Total employee tax amount for all employees on this page"
    },
    "balance_employer_tax": {
        "tax_code": "Code identifying the type of employer tax (page-level aggregate)",
        "tax_amount": "Total employer tax amount for all employees on this page"
    },
    "company_totals": {
        "com_period_start_date": "Company-wide pay period start date",
        "com_period_end_date": "Company-wide pay period end date",
        "com_earning_code": "Earning code for company-level totals",
        "com_earning_qtd_hours": "Total hours for this earning type (current period, company-wide)",
        "com_earning_qtd_amount": "Total amount for this earning type (current period, company-wide)",
        "com_earning_ytd_hours": "Total hours for this earning type (year-to-date, company-wide)",
        "com_earning_ytd_amount": "Total amount for this earning type (year-to-date, company-wide)",
        "com_deduction_code": "Deduction code for company-level totals",
        "com_deduction_qtd_hours": "Total hours for this deduction type (current period, company-wide)",
        "com_deduction_qtd_amount": "Total amount for this deduction type (current period, company-wide)",
        "com_deduction_ytd_hours": "Total hours for this deduction type (year-to-date, company-wide)",
        "com_deduction_ytd_amount": "Total amount for this deduction type (year-to-date, company-wide)",
        "com_tax_code": "Tax code for company-level totals",
        "com_tax_amount": "Total tax amount (company-wide)"
    },
    "employee_info": {
        "employee_details": {
            "employee_number": "Unique identifier for the employee (Emp. No.)",
            "fullname": "Employee's full name",
            "ssn": "Social Security Number (may be partially masked)",
            "department_number": "Department or division number",
            "pay_frequency": "How often the employee is paid (Weekly, Biweekly, etc.)",
            "payment_type": "Method of payment (DD for Direct Deposit, Check, etc.)",
            "tax_status_federal": "Federal tax filing status (Single, Married, etc.)",
            "tax_exemptions_federal": "Number of federal tax exemptions claimed",
            "tax_status_state": "State tax filing status",
            "tax_exemptions_state": "Number of state tax exemptions claimed",
            "state": "State abbreviation for tax purposes",
            "pay_period_start_date": "Start date of the pay period for this employee",
            "pay_period_end_date": "End date of the pay period for this employee"
        },
        "balance_earnings": {
            "earning_code": "Code identifying the type of earning",
            "earning_description": "Description of the earning type (Regular Pay, Overtime, Bonus, etc.)",
            "rate": "Hourly or salary rate for this earning",
            "earning_qtd_hours": "Hours worked in current period",
            "earning_qtd_amount": "Earnings amount for current period",
            "earning_ytd_hours": "Total hours worked year-to-date",
            "earning_ytd_amount": "Total earnings year-to-date"
        },
        "balance_deductions": {
            "deduction_code": "Code identifying the type of deduction",
            "deduction_description": "Description of the deduction (401K, Insurance, etc.)",
            "deduction_qtd_amount": "Deduction amount for current period",
            "deduction_ytd_amount": "Total deductions year-to-date",
            "deduction_qtd_hours": "Hours associated with deduction (if applicable)",
            "deduction_ytd_hours": "YTD hours associated with deduction (if applicable)"
        },
        "balance_employee_tax": {
            "tax_code": "Code identifying the type of tax for this employee",
            "tax_description": "Description of the tax (Federal Withholding, FICA, etc.)",
            "tax_qtd_amount": "Tax amount for current period",
            "tax_ytd_amount": "Total tax withheld year-to-date",
            "tax_jurisdiction": "Level of government collecting the tax (Federal, State, Local)"
        }
    }
}


# Common aliases for field matching (helps LLM map variations)
FIELD_ALIASES = {
    # Metadata fields
    "company_name": ["Company Name", "Company", "Organization", "Employer"],
    "company_number": ["Co. No.", "Co No", "Company No", "Company Number"],
    "payroll_number": ["Payroll #", "Payroll No", "Payroll Number", "Batch Number"],
    "pay_period_start": ["Pay Period Start", "Period Start", "Start Date"],
    "pay_period_end": ["Pay Period End", "Period End", "End Date"],
    "check_date": ["Check Date", "Payment Date", "Issue Date"],
    
    # Employee details
    "employee_number": ["Emp. No.", "Emp No", "Employee No", "Employee #", "EmpID", "Employee Number"],
    "fullname": ["Employee Name", "Name", "Full Name", "Employee"],
    "ssn": ["SSN No.", "SSN", "Social Security", "SS#", "SSN No"],
    "department_number": ["Dept.", "Dept", "Department", "Dept. No.", "Department No"],
    "pay_frequency": ["Pay Freq.", "Pay Frequency", "Frequency"],
    "payment_type": ["Type", "Payment Type", "Pay Type"],
    "tax_status_federal": ["Fed:", "Federal Status", "Tax Status"],
    "tax_status_state": ["State Status", "State Tax Status"],
    "state": ["State", "(State for)"],
    
    # Summary fields
    "net_pay": ["Net Pay", "Net Amount", "Take Home", "Net"],
    "check_number": ["Ck. No.", "Check No", "Check Number", "Ck #", "Ck No"],
    
    # Earnings
    "earning_code": ["Earning Code", "Pay Code", "Earnings Code"],
    "earning_description": ["Description", "Earning Description", "Pay Description"],
    "rate": ["Rate", "Hourly Rate", "Pay Rate"],
    "regular_pay": ["Regular Pay", "Regular", "Base Pay", "Straight Time", "0-Regular Pay"],
    "overtime_pay": ["Overtime", "OT", "Overtime Pay"],
    "earning_qtd_amount": ["Amount", "Current Amount", "Period Amount", "Current", "Pay"],
    "earning_ytd_hours": ["YTD Hours", "Year-to-Date Hours"],
    "earning_ytd_amount": ["YTD", "Year-to-Date", "YTD Amount"],
    
    # Deductions
    "deduction_code": ["Deduction Code", "Ded Code"],
    "deduction_description": ["Description", "Deduction Description", "Deduction"],
    "deduction_qtd_amount": ["Current", "Amount", "Current Amount", "QTD"],
    "deduction_ytd_amount": ["YTD", "Year-to-Date", "YTD Amount"],
    "401k": ["401K", "401(k)", "401K Plan", "4-401K Plan", "Retirement"],
    "medical_insurance": ["Medical", "CAF Medical", "2-CAF Medical", "Health Insurance"],
    "dental_insurance": ["Dental", "CAF Dental", "3-CAF Dental", "Dental Insurance"],
    "child_support": ["Child Support", "1-Child Support", "31-Child Support"],
    "garnishment": ["Garnishment", "Wage Garnishment", "Tax Levy", "32-Mass Tax Lev"],
    
    # Taxes
    "tax_code": ["Tax", "Tax Code", "Tax Description"],
    "tax_description": ["Description", "Tax Description"],
    "tax_qtd_amount": ["Current", "Amount", "Current Amount"],
    "tax_ytd_amount": ["YTD", "Year-to-Date", "YTD Amount"],
    "federal_withholding": ["Federal WH", "Fed WH", "Federal Withholding", "FWT"],
    "state_withholding": ["State WH", "MA: State WH", "State Withholding", "SWT", "MA State WH"],
    "fica_oasdi": ["OASDI", "Social Security", "SS Tax"],
    "fica_medicare": ["Medicare", "Medicare Tax"],
    
    # Company totals fields
    "com_earning_code": ["Earning Code", "Company Earning Code"],
    "com_earning_qtd_hours": ["Current Hours", "QTD Hours", "Period Hours"],
    "com_earning_qtd_amount": ["Current Amount", "QTD Amount", "Current"],
    "com_earning_ytd_hours": ["YTD Hours", "Year-to-Date Hours"],
    "com_earning_ytd_amount": ["YTD Amount", "Year-to-Date Amount", "YTD"],
    "com_deduction_code": ["Deduction Code", "Company Deduction Code"],
    "com_deduction_qtd_hours": ["Current Hours", "QTD Hours"],
    "com_deduction_qtd_amount": ["Current Amount", "QTD Amount", "Current"],
    "com_deduction_ytd_hours": ["YTD Hours"],
    "com_deduction_ytd_amount": ["YTD Amount", "YTD"],
    "com_tax_code": ["Tax Code", "Company Tax Code"],
    "com_tax_amount": ["Tax Amount", "Amount"],
    "com_period_start_date": ["Period Start", "Start Date", "Pay Period Start"],
    "com_period_end_date": ["Period End", "End Date", "Pay Period End"]
}
