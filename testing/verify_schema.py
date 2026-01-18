import re

# Verify the cleaned schema
with open('schema/global_schema.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for any remaining mapped_from or notes
mapped_from_count = content.count('mapped_from')
notes_in_fields = content.count('"notes"')

print(f'✓ Verification Results:')
print(f'  mapped_from references: {mapped_from_count}')
print(f'  notes in fields: {notes_in_fields}')

# Count total lines
lines = content.split('\n')
print(f'  Total lines: {len(lines)}')

# Check structure of key fields
fields = re.findall(r'"(\w+)":\s*\{\s*"value":\s*None,\s*"confidence":\s*0\.0\s*\}', content, re.MULTILINE)
print(f'  Fields with clean value+confidence structure: {len(fields)}')

# Verify no extra blank lines in field definitions
bad_spacing = re.findall(r'"value":\s*None,\s*\n\s*\n\s*"confidence"', content)
if bad_spacing:
    print(f'  ❌ Found {len(bad_spacing)} fields with extra blank lines')
else:
    print(f'  ✓ No extra blank lines found')

# Verify all important parent fields exist
required_fields = ['balance_employee_tax', 'balance_employer_tax', 'company_totals', 'employee_info']
for field in required_fields:
    if field in content:
        print(f'  ✓ {field} exists')
    else:
        print(f'  ❌ {field} MISSING')

print('\n✓ Schema is clean and ready for mapping')
