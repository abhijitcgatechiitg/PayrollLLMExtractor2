"""
Step 3: Raw Table Extraction (PASS 1)
Extracts data from SFP text AS-IS, without forcing any business logic or schema.
Output: interim.json with flexible, universal table format
"""

import json
import os
from typing import Dict, List
from dotenv import load_dotenv
from anthropic import Anthropic
from src.prompts.extractor_prompt import get_extractor_prompt

# Load environment variables
load_dotenv()


class RawDataExtractor:
    """Extracts raw financial table data from SFP text."""
    
    def __init__(self, model: str = "claude-3-haiku-20240307"):
        """
        Initialize the extractor with Anthropic client.
        
        Args:
            model: Claude model to use
        """
        self.client = Anthropic()
        self.model = model
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def extract_raw_data(self, sfp_text: str) -> Dict:
        """
        Extract raw table data from SFP text using Claude.
        
        Args:
            sfp_text: Combined text from all SFP pages
            
        Returns:
            Dictionary with structure:
            {
                "section": "SFP",
                "years": [...],
                "currency": "...",
                "items": [...]
            }
        """
        prompt = get_extractor_prompt(sfp_text)
        
        try:
            print("Sending SFP text to Claude for raw extraction...")
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,  # Larger token limit for detailed extraction
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse the response
            response_text = message.content[0].text
            
            # Try to extract JSON from response
            # Sometimes Claude might add extra text, so let's be flexible
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to find JSON in the response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    raise ValueError("No valid JSON found in response")
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"Error: Could not parse JSON response: {e}")
            print(f"Response was: {response_text[:500]}")
            return {
                "section": "SFP",
                "years": [],
                "currency": "Unknown",
                "items": [],
                "error": "Failed to extract data"
            }
        except Exception as e:
            print(f"Error extracting raw data: {e}")
            return {
                "section": "SFP",
                "years": [],
                "currency": "Unknown",
                "items": [],
                "error": str(e)
            }
    
    def validate_interim_format(self, data: Dict) -> bool:
        """
        Validate that the extracted data has the expected interim format.
        
        Args:
            data: The extracted data
            
        Returns:
            True if valid, False otherwise
        """
        required_keys = ["section", "years", "currency", "items"]
        
        for key in required_keys:
            if key not in data:
                print(f"Warning: Missing key '{key}' in extracted data")
                return False
        
        if not isinstance(data["items"], list):
            print("Warning: 'items' is not a list")
            return False
        
        # Validate item structure
        for item in data["items"]:
            required_item_keys = ["label_raw", "values"]
            for key in required_item_keys:
                if key not in item:
                    print(f"Warning: Item missing key '{key}'")
                    return False
        
        return True


if __name__ == "__main__":
    # This module is meant to be imported by main.py
    print("This module should be run via main.py")
    print("Usage: python main.py <pdf_filename>")
