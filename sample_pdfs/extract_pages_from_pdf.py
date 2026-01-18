"""
Extract individual pages from a PDF and save each as separate PDF files.
Usage: python extract_pages_from_pdf.py <pdf_file>
Output: Creates pdf_name_page_1.pdf, pdf_name_page_2.pdf, etc.
"""

import sys
import os
from pathlib import Path
import pymupdf  # fitz


def extract_pages(pdf_path):
    """
    Extract each page from a PDF and save as separate PDF files.
    
    Args:
        pdf_path: Path to the PDF file
    """
    # Validate file exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found: {pdf_path}")
        return
    
    if not pdf_path.lower().endswith('.pdf'):
        print(f"❌ Error: Not a PDF file: {pdf_path}")
        return
    
    # Get file info
    pdf_name = Path(pdf_path).stem  # filename without extension
    output_dir = Path(pdf_path).parent
    
    print(f"Processing: {pdf_path}")
    print(f"Output directory: {output_dir}")
    
    try:
        # Open PDF
        pdf_document = pymupdf.open(pdf_path)
        total_pages = len(pdf_document)
        
        print(f"Total pages: {total_pages}\n")
        
        # Extract each page
        for page_num in range(total_pages):
            # Create new PDF with single page
            new_pdf = pymupdf.open()
            page = pdf_document[page_num]
            new_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
            
            # Save with naming convention
            output_filename = f"{pdf_name}_page_{page_num + 1}.pdf"
            output_path = output_dir / output_filename
            
            new_pdf.save(str(output_path))
            new_pdf.close()
            
            print(f"✓ Saved: {output_filename}")
        
        pdf_document.close()
        
        print(f"\n✅ Successfully extracted {total_pages} pages!")
        print(f"Files saved in: {output_dir}")
        
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pages_from_pdf.py <pdf_file>")
        print("Example: python extract_pages_from_pdf.py PR-Register.pdf")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    extract_pages(pdf_file)
