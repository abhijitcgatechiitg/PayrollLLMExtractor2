"""
Main Orchestrator
Runs the entire financial data extraction pipeline from a single entry point.
Usage: python main.py <pdf_filename>
Example: python main.py sofp_sample3.pdf
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Import pipeline steps
from src.step1_pdf_extraction import extract_text_from_pdf
from src.step2_sfp_classifier import SFPClassifier
from src.step3_raw_extraction import RawDataExtractor
from src.step4_schema_mapping import SchemaMatcher
from src.step5_validation import FinancialValidator


def log_step(step_num: int, step_name: str):
    """Print formatted step header."""
    print("\n" + "="*60)
    print(f"STEP {step_num}: {step_name}")
    print("="*60)


def log_success(message: str):
    """Print success message."""
    print(f"✓ {message}")


def log_error(message: str):
    """Print error message."""
    print(f"✗ {message}")


def ensure_output_dirs():
    """Ensure output directories exist."""
    Path("./outputs/intermediate").mkdir(parents=True, exist_ok=True)
    Path("./outputs/final").mkdir(parents=True, exist_ok=True)


def main():
    """Main orchestration function."""
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py <pdf_filename>")
        print("Example: python main.py sofp_sample3.pdf")
        print("\nAvailable PDFs in sample_pdfs/:")
        sample_pdfs = list(Path("./sample_pdfs").glob("*.pdf"))
        for pdf in sample_pdfs:
            print(f"  - {pdf.name}")
        sys.exit(1)
    
    pdf_filename = sys.argv[1]
    pdf_path = f"./sample_pdfs/{pdf_filename}"
    base_name = pdf_filename.replace(".pdf", "")
    
    # Verify PDF exists
    if not Path(pdf_path).exists():
        log_error(f"PDF file not found: {pdf_path}")
        sys.exit(1)
    
    # Ensure output directories exist
    ensure_output_dirs()
    
    print("\n" + "="*60)
    print("FINANCIAL DATA EXTRACTION PIPELINE")
    print("="*60)
    print(f"Processing: {pdf_filename}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # ==========================================
        # STEP 1: Extract text from PDF
        # ==========================================
        log_step(1, "PDF Text Extraction")
        
        pages = extract_text_from_pdf(pdf_path)
        
        if not pages:
            log_error("No pages extracted from PDF")
            sys.exit(1)
        
        log_success(f"Extracted {len(pages)} pages from PDF")
        
        # Save extracted pages
        extracted_json_path = f"./outputs/intermediate/{base_name}_extracted.json"
        with open(extracted_json_path, 'w', encoding='utf-8') as f:
            json.dump(pages, f, indent=2, ensure_ascii=False)
        log_success(f"Saved to: {extracted_json_path}")
        
        # Print page preview
        for page in pages[:3]:  # Show first 3 pages
            text_preview = page['text'][:80].replace('\n', ' ')
            print(f"  Page {page['page_number']}: {text_preview}...")
        
        if len(pages) > 3:
            print(f"  ... and {len(pages) - 3} more pages")
        
        # ==========================================
        # STEP 2: Classify pages (Find SFP)
        # ==========================================
        log_step(2, "SFP Page Classification")
        
        classifier = SFPClassifier()
        results = classifier.classify_pages(pages)
        
        log_success(f"Found {results['total_sfp_pages']} SFP page(s)")
        
        if results['total_non_sfp_pages'] > 0:
            print(f"  Non-SFP pages: {results['total_non_sfp_pages']}")
        
        # Save classification results
        classified_json_path = f"./outputs/intermediate/{base_name}_classified.json"
        with open(classified_json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        log_success(f"Saved to: {classified_json_path}")
        
        if results['sfp_pages']:
            print("\n  SFP Pages identified:")
            for sfp_page in results['sfp_pages']:
                print(f"    - Page {sfp_page['page_number']}: {sfp_page['reason']}")
        else:
            log_error("No SFP pages found in PDF")
            print("\n  This PDF may not contain a Statement of Financial Position.")
            sys.exit(1)
        
        # ==========================================
        # STEP 3: Extract raw table data
        # ==========================================
        log_step(3, "Raw Table Extraction (PASS 1)")
        
        extractor = RawDataExtractor()
        interim_data = extractor.extract_raw_data(results['sfp_text'])
        
        # Validate interim format
        if not extractor.validate_interim_format(interim_data):
            log_error("Extracted data does not match expected format")
            print("Continuing with extracted data anyway...")
        
        log_success(f"Extracted {len(interim_data.get('items', []))} financial line items")
        
        # Show extraction summary
        print(f"\n  Detected years: {interim_data.get('years', [])}")
        print(f"  Detected currency: {interim_data.get('currency', 'Unknown')}")
        print(f"  Financial items extracted: {len(interim_data.get('items', []))}")
        
        if interim_data.get('items'):
            print(f"\n  Sample items (first 3):")
            for item in interim_data.get('items', [])[:3]:
                label = item.get('label_raw', 'Unknown')
                values = item.get('values', {})
                print(f"    - {label}: {values}")
        
        # Save interim JSON
        interim_json_path = f"./outputs/intermediate/{base_name}_interim.json"
        with open(interim_json_path, 'w', encoding='utf-8') as f:
            json.dump(interim_data, f, indent=2, ensure_ascii=False)
        log_success(f"Saved to: {interim_json_path}")
        
        # ==========================================
        # STEP 4: Map to global schema
        # ==========================================
        log_step(4, "Schema Mapping (PASS 2)")
        
        matcher = SchemaMatcher()
        metadata = {
            'currency': results.get('sfp_text', '').upper().split('INR')[-1][:3] if 'INR' in results.get('sfp_text', '') else 'Unknown',
            'years': interim_data.get('years', []),
            'extraction_timestamp': datetime.now().isoformat()
        }
        
        mapped_data = matcher.map_interim_to_schema(interim_data, metadata)
        
        log_success(f"Mapped data to global schema")
        
        # Show mapping summary
        unmapped_count = len(mapped_data.get('unmapped_items', {}).get('items', []))
        print(f"\n  Items mapped: {len(interim_data.get('items', [])) - unmapped_count}")
        print(f"  Items unmapped: {unmapped_count}")
        
        if unmapped_count > 0:
            print(f"\n  Unmapped items (needs review):")
            for item in mapped_data.get('unmapped_items', {}).get('items', [])[:3]:
                print(f"    - {item.get('label_raw', 'Unknown')}: {item.get('reason', '')}")
            if unmapped_count > 3:
                print(f"    ... and {unmapped_count - 3} more")
        
        # Save mapped JSON
        mapped_json_path = f"./outputs/intermediate/{base_name}_mapped.json"
        with open(mapped_json_path, 'w', encoding='utf-8') as f:
            json.dump(mapped_data, f, indent=2, ensure_ascii=False)
        log_success(f"Saved to: {mapped_json_path}")
        
        # ==========================================
        # STEP 5: Validation
        # ==========================================
        log_step(5, "Validation")
        
        validator = FinancialValidator()
        validation_result = validator.validate_mapped_data(mapped_data)
        
        # Update mapped_data with validation results
        mapped_data['validation'] = validation_result
        
        print(f"✓ Validation complete: {validation_result['status']}")
        print(f"  Errors: {validation_result['total_errors']}")
        print(f"  Warnings: {validation_result['total_warnings']}")
        
        if validation_result['errors']:
            print("\n  Errors found:")
            for error in validation_result['errors'][:3]:
                print(f"    ✗ {error}")
            if len(validation_result['errors']) > 3:
                print(f"    ... and {len(validation_result['errors']) - 3} more")
        
        if validation_result['warnings']:
            print("\n  Warnings:")
            for warning in validation_result['warnings'][:3]:
                print(f"    ⚠ {warning}")
            if len(validation_result['warnings']) > 3:
                print(f"    ... and {len(validation_result['warnings']) - 3} more")
        
        # ==========================================
        # STEP 6: Save Final Output
        # ==========================================
        log_step(6, "Save Final Output")
        
        # Save final mapped JSON to outputs/final/
        final_json_path = f"./outputs/final/{base_name}_final.json"
        with open(final_json_path, 'w', encoding='utf-8') as f:
            json.dump(mapped_data, f, indent=2, ensure_ascii=False)
        log_success(f"Saved final output to: {final_json_path}")
        
        # ==========================================
        # Pipeline complete
        # ==========================================
        print("\n" + "="*60)
        print("PIPELINE EXECUTION COMPLETE")
        print("="*60)
        print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nOutput files created in: outputs/intermediate/")
        print(f"  - {base_name}_extracted.json")
        print(f"  - {base_name}_classified.json")
        
    except KeyboardInterrupt:
        print("\n\n✗ Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        log_error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
