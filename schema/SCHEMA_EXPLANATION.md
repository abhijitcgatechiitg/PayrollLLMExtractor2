# Payroll Global Schema Explanation

## Overview
This schema is designed to extract payroll data from PDF documents (like PR-Register.pdf). The structure follows a 4-parent-field approach with employee-level and company-level data.

## Main Structure

### 1. metadata
Basic document info like company name, payroll number, pay period dates, page number, etc.

### 2. balance_employee_tax (page-level)
Array of employee tax totals aggregated for all employees on the page.
- tax_code: e.g., "Federal WH", "OASDI", "Medicare"
- tax_amount: total amount

### 3. balance_employer_tax (page-level)
Array of employer tax totals aggregated for all employees on the page.
- tax_code
- tax_amount

### 4. company_totals
Company-wide aggregated data:
- com_period_start_date, com_period_end_date
- com_balance_earnings: array of earning totals with qtd/ytd hours and amounts
- com_balance_deductions: array of deduction totals with qtd/ytd hours and amounts
- com_balance_employee_tax: array of employee tax totals
- com_balance_employer_tax: array of employer tax totals

### 5. employee_info (main data)
Array of employees, each containing:

**employee_details:**
- Basic info: fullname, ssn, employee_number, department_number
- Tax info: tax_status_federal, tax_exemptions_federal, state, etc.
- Pay info: pay_frequency, payment_type
- Dates: pay_period_start_date, pay_period_end_date

**balance_earnings:** (array)
Each earning entry has:
- earning_code, earning_description, rate
- earning_qtd_hours, earning_qtd_amount (current period)
- earning_ytd_hours, earning_ytd_amount (year-to-date)

**balance_deductions:** (array)
Each deduction entry has:
- deduction_code, deduction_description
- deduction_qtd_amount, deduction_qtd_hours (current)
- deduction_ytd_amount, deduction_ytd_hours (year-to-date)

**balance_employee_tax:** (array)
Each tax entry has:
- tax_code, tax_description, tax_jurisdiction
- tax_qtd_amount (current)
- tax_ytd_amount (year-to-date)

**unmapped_items:**
For any data that doesn't fit the schema

## Important Notes

- QTD = Quarter-to-Date (or Period-to-Date) = Current period values
- YTD = Year-to-Date = Cumulative values
- Each field has: value, confidence (0.0-1.0), mapped_from, notes
- Arrays support multiple entries (multiple earnings, deductions, taxes per employee)
- Not all interim data will map to this schema - that's by design

## Example Flow
1. Page 1 of PR-Register.pdf has 9 employees
2. Each employee gets their own entry in employee_info array
3. Each employee can have multiple earnings (Regular Pay, Sick Pay, etc.)
4. Each employee can have multiple deductions (401K, Medical, etc.)
5. Each employee can have multiple taxes (Federal WH, OASDI, Medicare, State WH)
6. Company totals aggregate all employees' data
7. Anything that doesn't fit goes to unmapped_items
