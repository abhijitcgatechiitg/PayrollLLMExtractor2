"""
Main Orchestrator - Runs the complete payroll extraction pipeline
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.step1_pdf_extraction import extract_text_from_pdf
from src.step2_raw_extraction import RawDataExtractor
from src.step3_schema_mapping import SchemaMapper
from src.step4_validation import DataValidator


class PayrollExtractionPipeline:
    """Main pipeline orchestrator for payroll data extraction."""
    
    def __init__(self, output_base_dir: str = "outputs"):
        """
        Initialize the pipeline.
        
        Args:
            output_base_dir: Base directory for all outputs
        """
        load_dotenv()
        self.output_base_dir = output_base_dir
        self.raw_extractor = RawDataExtractor()
        self.schema_mapper = SchemaMapper()
        # self.validator = DataValidator()  # Validation placeholder - not used yet
    
    def process_pdf(self, pdf_path: str) -> dict:
        """
        Process a single PDF through the complete pipeline.
        
        Args:
            pdf_path: Path to the PDF file
        
        Returns:
            Summary of processing results
        """
        print("="*70)
        print("PAYROLL EXTRACTION PIPELINE")
        print("="*70)
        print(f"Processing: {pdf_path}")
        start_time = datetime.now()
        print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Initialize statistics
        total_input_tokens = 0
        total_output_tokens = 0
        total_extraction_time = 0
        total_mapping_time = 0
        
        # Setup output directory
        pdf_name = Path(pdf_path).stem
        output_dir = Path(self.output_base_dir) / pdf_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Step 1: Extract text from PDF
        print("[STEP 1] Extracting text from PDF...")
        pages = extract_text_from_pdf(pdf_path)
        print(f"  ✓ Extracted {len(pages)} pages")
        print()
        
        # Process each page
        results = []
        
        for page_data in pages:
            page_num = page_data['page_number']
            page_text = page_data['text']
            
            print(f"--- Processing Page {page_num} ---")
            
            # Create page output directory
            page_dir = output_dir / f"page_{page_num}"
            page_dir.mkdir(exist_ok=True)
            
            # Step 2: Raw extraction
            print(f"[STEP 2] Extracting raw data from page {page_num}...")
            try:
                import time
                extraction_start = time.time()
                interim_data = self.raw_extractor.extract_raw_data(page_text, page_num)
                extraction_time = time.time() - extraction_start
                total_extraction_time += extraction_time
                
                # Note: Token stats are printed in step2, but not returned. We'll track from step3.
                
                # Save interim JSON
                interim_path = page_dir / "interim.json"
                with open(interim_path, 'w', encoding='utf-8') as f:
                    json.dump(interim_data, f, indent=2, ensure_ascii=False)
                
                num_employees = len(interim_data.get('employees', []))
                print(f"  ✓ Extracted {num_employees} employees")
                print(f"  ✓ Saved to: {interim_path}")
                
            except Exception as e:
                print(f"  ❌ Error in raw extraction: {e}")
                results.append({
                    "page": page_num,
                    "status": "failed",
                    "step": "raw_extraction",
                    "error": str(e)
                })
                print()
                continue
            
            # Step 3: Schema mapping
            print(f"[STEP 3] Mapping to global schema...")
            try:
                import time
                mapping_start = time.time()
                mapped_data = self.schema_mapper.map_to_global_schema(interim_data, page_num)
                mapping_time = time.time() - mapping_start
                total_mapping_time += mapping_time
                
                # Track tokens from the last API call (stored in mapper)
                # Note: step2 tokens are already printed, we'll aggregate from summary
                
                # Add metadata
                mapped_data['metadata']['extraction_timestamp'] = datetime.now().isoformat()
                mapped_data['metadata']['source_file'] = pdf_name
                
                # Save mapped JSON
                mapped_path = page_dir / "mapped.json"
                with open(mapped_path, 'w', encoding='utf-8') as f:
                    json.dump(mapped_data, f, indent=2, ensure_ascii=False)
                
                print(f"  ✓ Mapped {len(mapped_data.get('employee_info', []))} employees")
                print(f"  ✓ Saved to: {mapped_path}")
                
            except Exception as e:
                print(f"  ❌ Error in schema mapping: {e}")
                results.append({
                    "page": page_num,
                    "status": "failed",
                    "step": "schema_mapping",
                    "error": str(e)
                })
                print()
                continue
            
            # Step 4: Validation (placeholder) - COMMENTED OUT
            # print(f"[STEP 4] Validating data...")
            # try:
            #     validation_report = self.validator.validate(mapped_data)
            #     
            #     # Save validation report
            #     validation_path = page_dir / "validation_report.json"
            #     with open(validation_path, 'w', encoding='utf-8') as f:
            #         json.dump(validation_report, f, indent=2)
            #     
            #     print(f"  ✓ Validation status: {validation_report['status']}")
            #     if validation_report.get('warnings'):
            #         print(f"  ⚠ Warnings: {len(validation_report['warnings'])}")
            #     
            # except Exception as e:
            #     print(f"  ⚠ Warning: Validation failed: {e}")
            
            # Record success
            results.append({
                "page": page_num,
                "status": "success",
                "employees": num_employees,
                "interim_path": str(interim_path),
                "mapped_path": str(mapped_path)
            })
            
            print()
        
        # Summary
        print("="*70)
        print("PIPELINE SUMMARY")
        print("="*70)
        
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] == 'failed']
        
        print(f"Total pages: {len(pages)}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(failed)}")
        
        if successful:
            total_employees = sum(r.get('employees', 0) for r in successful)
            print(f"Total employees extracted: {total_employees}")
        
        # Calculate total time
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()
        
        # Performance statistics
        print("\n📊 PERFORMANCE STATISTICS:")
        print(f"   Total processing time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
        print(f"   Average time per page: {total_time/len(pages):.2f} seconds")
        if total_extraction_time > 0:
            print(f"   Total extraction time (Step 2): {total_extraction_time:.2f} seconds")
        if total_mapping_time > 0:
            print(f"   Total mapping time (Step 3): {total_mapping_time:.2f} seconds")
        
        print(f"\nOutput directory: {output_dir.absolute()}")
        print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        # Save pipeline summary
        summary = {
            "pdf_file": pdf_path,
            "pdf_name": pdf_name,
            "timestamp": datetime.now().isoformat(),
            "total_pages": len(pages),
            "successful_pages": len(successful),
            "failed_pages": len(failed),
            "results": results
        }
        
        summary_path = output_dir / "pipeline_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        return summary


def main():
    """Main entry point for the pipeline."""
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <pdf_path>")
        print("\nExample:")
        print("  python main.py sample_pdfs/PR-Register.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    # Run pipeline
    pipeline = PayrollExtractionPipeline()
    summary = pipeline.process_pdf(pdf_path)
    
    # Exit with appropriate code
    if summary['failed_pages'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
