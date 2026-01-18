major fields in old global schema
I was given an image of schema along with the description. THERE can be few more nested fields inside some parent fields.
parent fields: 4
1. balance_employee_tax : container for employee tax with
2. balance_employer_tax : 
3. company_totals
4. employee_info

child fields info: 
balance_employee_tax
1. tax_amount
2. tax_code

balance_employer_tax
1. tax_amount
2. tax_code

company_totals: 6 child fields
1. com_balance_deductions : 5 child fields
    a. com_deduction_code
    b. com_deduction_qtd_hours
    c. com_deduction_qtd_amount
    d. com_deduction_ytd_hours
    e.com_deduction_ytd_hours
2. com_balance_earnings: 5 child fields
    a. com_earning_code
    b. com_earining_qtd_hours
    c. com_earning_qtd_amount
    d. com_earning_ytd_hours
    e. com_earining_ytd_amount
3. com_balance_employee_tax: 2 child
    com_tax_amount
    com_tax_code
4. com_balance_employer_tax: 2 child
    com_tax_amount
    com_tax_code
5. com_period_end_date
6. com_period_start_date

employee_info
1. balance_deductions: This field will have each deduction code and it's values( can be multiple codes so needs to added for all of them)
    a. deduction_code
    b. deduction_qtd_amount
    c. deduction_qtd_hours
    d. deduction_ytd_hours
    e. deduction_ytd_amount
2. balance_deductions ( in case of second deduction code(just added for your example))
    a. deduction_code
    b. deduction_qtd_amount
    c. deduction_qtd_hours
    d. deduction_ytd_hours
    e. deduction_ytd_amount
3. balance_earnings
    a. earning_code
    b. earning_qtd_amount
    c. earning_qtd_hours
    d. earning_ytd_hours
    e. earning_ytd_amount
4. employee_details:
    fullname
    pay_period_start_date
    pay_period_end_date
    ssn:
    