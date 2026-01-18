"""
Test script for schema mapping phase (Step 3)
Tests mapping of interim JSON to global schema
"""

import sys
import json
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.step3_schema_mapping import SchemaMapper


def test_mapping():
    """Test the mapping phase on test_page1_interim.json"""
    
    print("="*60)
    print("SCHEMA MAPPING TEST")
    print("="*60)
    
    # Test Step 3: Schema Mapping
    print("\n[STEP 3] Mapping interim JSON to global schema...")
    print("  Model: claude-haiku-4-5-20251001")
    print("  Input: testing/test_page1_interim.json")
    
    # Load interim data
    interim_path = Path(__file__).parent / "test_page1_interim.json"
    
    if not interim_path.exists():
        print(f"❌ Interim JSON file not found: {interim_path}")
        print("   Run test_extraction.py first to generate interim data")
        return
    
    with open(interim_path, 'r', encoding='utf-8') as f:
        interim_data = json.load(f)
    
    print(f"  Loaded interim data: {len(interim_data.get('employees', []))} employees")
    
    try:
        # Create mapper and perform mapping
        mapper = SchemaMapper()
        mapped_data = mapper.map_to_global_schema(interim_data, page_number=1)
        
        # Print summary
        print(f"\n  Summary:")
        print(f"  - Document type: {mapped_data.get('document_type')}")
        print(f"  - Company name: {mapped_data.get('metadata', {}).get('company_name', {}).get('value')}")
        print(f"  - Employees mapped: {len(mapped_data.get('employee_info', []))}")
        
        # Check first employee details
        if mapped_data.get('employee_info'):
            emp = mapped_data['employee_info'][0]
            emp_details = emp.get('employee_details', {})
            print(f"\n  First employee details:")
            print(f"  - Name: {emp_details.get('fullname', {}).get('value')}")
            print(f"  - Employee #: {emp_details.get('employee_number', {}).get('value')}")
            print(f"  - Earnings: {len(emp.get('balance_earnings', []))} types")
            print(f"  - Deductions: {len(emp.get('balance_deductions', []))} types")
            print(f"  - Taxes: {len(emp.get('balance_employee_tax', []))} types")
            
            # Show first earning detail
            if emp.get('balance_earnings'):
                earning = emp['balance_earnings'][0]
                print(f"\n  First earning:")
                print(f"  - Code: {earning.get('earning_code', {}).get('value')}")
                print(f"  - Amount (QTD): {earning.get('earning_qtd_amount', {}).get('value')}")
                print(f"  - Confidence: {earning.get('earning_code', {}).get('confidence')}")
                print(f"  - Mapped from: {earning.get('earning_code', {}).get('mapped_from')}")
        
        # Check company totals
        company_totals = mapped_data.get('company_totals', {})
        if company_totals.get('com_balance_earnings'):
            print(f"\n  Company totals:")
            print(f"  - Earnings: {len(company_totals.get('com_balance_earnings', []))} types")
            print(f"  - Deductions: {len(company_totals.get('com_balance_deductions', []))} types")
            print(f"  - Employee taxes: {len(company_totals.get('com_balance_employee_tax', []))} types")
            print(f"  - Employer taxes: {len(company_totals.get('com_balance_employer_tax', []))} types")
        
        # Save to testing folder
        output_path = Path(__file__).parent / "test_page1_mapped.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(mapped_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved mapped data to: {output_path}")
        print("\n" + "="*60)
        print("TEST COMPLETED SUCCESSFULLY ✓")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error during mapping: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_mapping()
