# Design Log - Schema Design

**Date:** January 18, 2026  
**Phase:** Schema Design - COMPLETED ✅

## Decision: Global Schema Structure

### Four Parent Fields (Root Level):
1. **metadata** - Document-level info
2. **balance_employee_tax** - Page-level employee tax aggregates
3. **balance_employer_tax** - Page-level employer tax aggregates  
4. **company_totals** - Company-wide aggregates with date ranges
5. **employee_info** - Array of all employees (main data)

### Naming Conventions:
- `fullname` (not full_name)
- `balance_earnings`, `balance_deductions`, `balance_employee_tax`
- `qtd` for current period (quarter-to-date / period-to-date)
- `ytd` for year-to-date
- Company fields prefixed with `com_`

### Each Field Structure:
```
{
  "value": None,
  "confidence": 0.0,
  "mapped_from": None,
  "notes": ""
}
```

### Key Decisions:
- ✅ NO summary section (removed - no totals, no net_pay, no check_number at employee level)
- ✅ Arrays for earnings/deductions/taxes (multiple per employee)
- ✅ Confidence tracking for quality assessment
- ✅ Unmapped_items section for data that doesn't fit

### Files Created:
- `schema/global_schema.py` - Main schema with FIELD_DESCRIPTIONS and FIELD_ALIASES
- `schema/SCHEMA_EXPLANATION.md` - Simple explanation document

## Reference:
Based on old_global_schema.md structure adapted for payroll register documents.
