"""
Test script for extraction phase (Step 1 + Step 2)
Tests PDF extraction and raw data extraction with LLM
"""

import sys
import json
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.step1_pdf_extraction import extract_text_from_pdf
from src.step2_raw_extraction import RawDataExtractor


def test_extraction():
    """Test the extraction phase on PR-Register.pdf"""
    
    print("="*60)
    print("EXTRACTION PHASE TEST")
    print("="*60)
    
    # Test Step 1: PDF Text Extraction
    print("\n[STEP 1] Extracting text from PDF...")
    pdf_path = "sample_pdfs/PR-Register.pdf"
    pages = extract_text_from_pdf(pdf_path)
    
    if not pages:
        print("❌ Failed to extract pages from PDF")
        return
    
    print(f"✓ Extracted {len(pages)} pages from PDF")
    print(f"  Page 1 text length: {len(pages[0]['text'])} characters")
    print(f"  Page 1 preview: {pages[0]['text'][:150].replace(chr(10), ' ')}...")
    
    # Test Step 2: Raw Data Extraction (on pages 1 and 2)
    print("\n[STEP 2] Extracting raw data from Pages 1 and 2 using LLM...")
    print("  Model: claude-haiku-4-5-20251001")
    
    try:
        extractor = RawDataExtractor()
        
        # Process both pages
        for page_idx in [0, 1]:  # Page 1 and Page 2
            page_num = page_idx + 1
            print(f"\n--- Processing Page {page_num} ---")
            
            interim_data = extractor.extract_raw_data(pages[page_idx]['text'], page_number=page_num)
            
            # Validate structure
            if not extractor.validate_interim_format(interim_data):
                print(f"❌ Page {page_num}: Interim data format validation failed")
                continue
            
            print(f"✓ Page {page_num}: Raw extraction successful")
            
            # Print summary
            print(f"\n  Summary:")
            print(f"  - Page metadata: {bool(interim_data.get('page_metadata'))}")
            print(f"  - Company name: {interim_data.get('page_metadata', {}).get('company_name')}")
            print(f"  - Payroll number: {interim_data.get('page_metadata', {}).get('payroll_number')}")
            print(f"  - Employees extracted: {len(interim_data.get('employees', []))}")
            print(f"  - Company totals present: {bool(interim_data.get('company_totals'))}")
            
            # Print first employee summary
            if interim_data.get('employees'):
                emp = interim_data['employees'][0]
                print(f"\n  First employee:")
                print(f"  - Name: {emp.get('employee_name')}")
                print(f"  - ID: {emp.get('employee_id')}")
                print(f"  - Earnings: {len(emp.get('earnings', []))} types")
                print(f"  - Deductions: {len(emp.get('deductions', []))} types")
                print(f"  - Taxes: {len(emp.get('taxes', []))} types")
            
            # Save to testing folder
            output_path = Path(__file__).parent / f"test_page{page_num}_interim.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(interim_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n✓ Saved interim data to: {output_path}")
        
        print("\n" + "="*60)
        print("TEST COMPLETED SUCCESSFULLY ✓")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_extraction()
