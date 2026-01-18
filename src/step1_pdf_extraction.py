"""
Step 1: PDF Text Extraction
Extracts raw text from each page of a PDF using PyMuPDF.
Each page is extracted independently for separate processing.
"""

import pymupdf  # fitz
from typing import List, Dict


def extract_text_from_pdf(pdf_path: str) -> List[Dict]:
    """
    Extract text from all pages of a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of dictionaries with page_number and text content
        Example: [
            {"page_number": 1, "text": "Payroll Register..."},
            {"page_number": 2, "text": "..."}
        ]
    """
    pages = []
    
    try:
        pdf_document = pymupdf.open(pdf_path)
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text = page.get_text()
            
            pages.append({
                "page_number": page_num + 1,  # 1-indexed for human readability
                "text": text
            })
        
        pdf_document.close()
        return pages
    
    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
        return []
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return []


if __name__ == "__main__":
    print("This module should be run via main.py")
    print("Usage: python main.py <pdf_filename>")
