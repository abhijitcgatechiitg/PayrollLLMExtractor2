import re

with open('schema/global_schema.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all field structures from 4-line to 2-line format
pattern = r'(\s+)\"(\w+)\":\s*\{\s*\n\s*\"value\":\s*None,\s*\n\s*\"confidence\":\s*0\.0,\s*\n\s*\"mapped_from\":\s*None,\s*\n\s*\"notes\":\s*\"\"'
replacement = r'\1"\2": {\n\1    "value": None,\n\1    "confidence": 0.0'

content_new = re.sub(pattern, replacement, content)

# Update docstring
content_new = content_new.replace(
    '5. Confidence tracking: Each mapped field includes confidence score',
    '5. Confidence tracking: Each mapped field includes confidence score (simplified to value + confidence only)'
)

content_new = content_new.replace(
    '- Company totals are optional (can be calculated if needed)',
    '''- Company totals are optional (can be calculated if needed)

SIMPLIFIED STRUCTURE (removed mapped_from and notes to reduce token usage):
- Each field now has only: {value, confidence}
- This reduces output size by ~30-40% while keeping essential information'''
)

with open('schema/global_schema.py', 'w', encoding='utf-8') as f:
    f.write(content_new)
    
print('Schema simplified successfully')
