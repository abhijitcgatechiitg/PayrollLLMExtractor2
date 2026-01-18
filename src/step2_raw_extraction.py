"""
Step 2: Raw Data Extraction (PASS 1)
Extracts payroll data from page text AS-IS, without forcing schema.
Output: interim.json with all employees and their data in raw format.
"""

import json
import os
from typing import Dict
from dotenv import load_dotenv
from anthropic import Anthropic
from src.prompts.extractor_prompt import get_extractor_prompt

# Load environment variables
load_dotenv()


class RawDataExtractor:
    """Extracts raw payroll data from page text using Claude."""
    
    def __init__(self, model: str = "claude-haiku-4-5-20251001"):
        """
        Initialize the extractor with Anthropic client.
        
        Args:
            model: Claude model to use (default: claude-haiku-4-5-20251001)
        """
        self.client = Anthropic()
        self.model = model
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def extract_raw_data(self, page_text: str, page_number: int) -> Dict:
        """
        Extract raw payroll data from page text using Claude.
        
        Args:
            page_text: Text content from a single PDF page
            page_number: Page number for reference
            
        Returns:
            Dictionary with structure:
            {
                "page_metadata": {...},
                "employees": [...]
            }
        """
        prompt = get_extractor_prompt(page_text)
        
        try:
            print(f"  Extracting data from page {page_number}...")
            message = self.client.messages.create(
                model=self.model,
                max_tokens=8000,  # Large token limit for multiple employees
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text
            
            # Parse JSON response
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to find JSON in response if Claude added extra text
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    raise ValueError("No valid JSON found in response")
            
            # Add page number to metadata
            if "page_metadata" not in result:
                result["page_metadata"] = {}
            result["page_metadata"]["page_number"] = page_number
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"  Error: Could not parse JSON response: {e}")
            print(f"  Response preview: {response_text[:200]}...")
            return {
                "page_metadata": {"page_number": page_number, "error": "JSON parse error"},
                "employees": []
            }
        except Exception as e:
            print(f"  Error extracting raw data: {e}")
            return {
                "page_metadata": {"page_number": page_number, "error": str(e)},
                "employees": []
            }
    
    def validate_interim_format(self, data: Dict) -> bool:
        """
        Validate that extracted data has expected format.
        
        Args:
            data: The extracted data
            
        Returns:
            True if valid, False otherwise
        """
        if "page_metadata" not in data:
            print("  Warning: Missing 'page_metadata'")
            return False
        
        if "employees" not in data:
            print("  Warning: Missing 'employees'")
            return False
        
        if not isinstance(data["employees"], list):
            print("  Warning: 'employees' is not a list")
            return False
        
        return True


if __name__ == "__main__":
    print("This module should be run via main.py")
    print("Usage: python main.py <pdf_filename>")
