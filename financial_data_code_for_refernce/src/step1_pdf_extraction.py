"""
Step 1: PDF Text Extraction
Extracts raw text from each page of a PDF using PyMuPDF.
This module is imported and called by main.py
"""

import fitz  # PyMuPDF
from typing import List, Dict


def extract_text_from_pdf(pdf_path: str) -> List[Dict]:
    """
    Extract text from all pages of a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of dictionaries with page_number and text content
        Example: [
            {"page_number": 0, "text": "Balance Sheet..."},
            {"page_number": 1, "text": "..."}
        ]
    """
    pages = []
    
    try:
        # Open the PDF document
        pdf_document = fitz.open(pdf_path)
        
        # Extract text from each page
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text = page.get_text()
            
            pages.append({
                "page_number": page_num,
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
