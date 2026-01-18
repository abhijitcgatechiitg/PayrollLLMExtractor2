"""
Step 2: SFP Page Classification
Uses Claude LLM to identify which pages contain Statement of Financial Position data.
This module is imported and called by main.py
"""

import json
import os
from typing import List, Dict
from dotenv import load_dotenv
from anthropic import Anthropic
from src.prompts.classifier_prompt import get_classifier_prompt

# Load environment variables
load_dotenv()


class SFPClassifier:
    """Classifies pages to identify which contain Statement of Financial Position data."""
    
    def __init__(self, model: str = "claude-3-haiku-20240307"):
        """
        Initialize the classifier with Anthropic client.
        
        Args:
            model: Claude model to use (default: haiku for cost efficiency)
        """
        self.client = Anthropic()
        self.model = model
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def classify_page(self, page_text: str) -> Dict:
        """
        Classify a single page using Claude.
        
        Args:
            page_text: The text content of the page
            
        Returns:
            Dictionary with classification result
            Example: {
                "contains_sfp": true,
                "confidence": 0.95,
                "reason": "Contains balance sheet structure..."
            }
        """
        prompt = get_classifier_prompt(page_text)
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse the response
            response_text = message.content[0].text
            result = json.loads(response_text)
            return result
            
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON response: {response_text}")
            return {
                "contains_sfp": False,
                "confidence": 0.0,
                "reason": "Failed to parse LLM response"
            }
        except Exception as e:
            print(f"Error classifying page: {e}")
            return {
                "contains_sfp": False,
                "confidence": 0.0,
                "reason": f"Classification error: {str(e)}"
            }
    
    def classify_pages(self, pages: List[Dict]) -> Dict:
        """
        Classify all pages in a list.
        
        Args:
            pages: List of page dictionaries from step1_pdf_extraction
            
        Returns:
            Dictionary with classification results:
            {
                "sfp_pages": [...],
                "non_sfp_pages": [...],
                "sfp_text": "Combined text of all SFP pages"
            }
        """
        sfp_pages = []
        non_sfp_pages = []
        sfp_texts = []
        
        print(f"Classifying {len(pages)} pages...")
        
        for page in pages:
            page_num = page["page_number"]
            page_text = page["text"]
            
            # Skip very short pages (likely blank)
            if len(page_text.strip()) < 100:
                print(f"  Page {page_num}: SKIPPED (too short)")
                continue
            
            # Classify the page
            result = self.classify_page(page_text)
            
            if result["contains_sfp"]:
                sfp_pages.append({
                    "page_number": page_num,
                    "confidence": result.get("confidence", 0),
                    "reason": result.get("reason", ""),
                    "text": page_text
                })
                sfp_texts.append(page_text)
                print(f"  Page {page_num}: ✓ SFP FOUND (confidence: {result.get('confidence', 0)})")
            else:
                non_sfp_pages.append({
                    "page_number": page_num,
                    "reason": result.get("reason", "")
                })
                print(f"  Page {page_num}: ✗ Not SFP")
        
        return {
            "sfp_pages": sfp_pages,
            "non_sfp_pages": non_sfp_pages,
            "sfp_text": "\n\n".join(sfp_texts),
            "total_sfp_pages": len(sfp_pages),
            "total_non_sfp_pages": len(non_sfp_pages)
        }




if __name__ == "__main__":
    # This module is meant to be imported by main.py
    print("This module should be run via main.py")
    print("Usage: python main.py <pdf_filename>")
