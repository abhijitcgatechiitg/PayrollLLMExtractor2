"""
Step 3: Schema Mapping
Maps interim JSON to the global payroll schema using LLM
"""

import json
import os
import sys
from typing import Dict, Any
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.prompts.mapper_prompt import get_mapper_prompt
from schema.global_schema import GLOBAL_PAYROLL_SCHEMA


class SchemaMapper:
    """Maps interim payroll data to global schema using Claude."""
    
    def __init__(self, model: str = "claude-haiku-4-5-20251001"):
        """
        Initialize the mapper with Anthropic client.
        
        Args:
            model: Claude model to use (default: claude-haiku-4-5-20251001)
        """
        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = Anthropic(api_key=api_key)
        self.model = model
    
    def map_to_global_schema(
        self, 
        interim_data: Dict[str, Any],
        page_number: int
    ) -> Dict[str, Any]:
        """
        Map interim JSON data to global schema using LLM.
        
        Args:
            interim_data: The raw extracted data from step 2
            page_number: Page number being processed
        
        Returns:
            Mapped data following global schema structure
        """
        import time
        
        print(f"  Mapping data to global schema for page {page_number}...")
        
        # Start timing
        start_time = time.time()
        
        # Convert interim data to JSON string for prompt
        interim_json_str = json.dumps(interim_data, indent=2)
        
        # Create a simplified schema example (just the structure)
        schema_example = self._get_schema_example()
        
        # Get the mapping prompt
        prompt = get_mapper_prompt(interim_json_str, schema_example)
        
        # Call Claude API
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=24000,  # Need extra buffer for 9 employees with simplified schema
                temperature=0,  # Deterministic mapping
                timeout=600.0,  # 10 minutes timeout
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # End timing
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # Extract token usage
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = input_tokens + output_tokens
            
            # Print statistics
            print(f"\n  📊 Statistics:")
            print(f"     Time taken: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
            print(f"     Input tokens: {input_tokens:,}")
            print(f"     Output tokens: {output_tokens:,}")
            print(f"     Total tokens: {total_tokens:,}")
            print(f"     Model: {self.model}")
            
            # Extract the response text
            response_text = response.content[0].text
            
            # Parse JSON from response
            mapped_data = self._extract_json_from_response(response_text)
            
            # Validate the mapped data has required structure
            if not self.validate_mapped_format(mapped_data):
                raise ValueError("Mapped data does not follow global schema structure")
            
            return mapped_data
            
        except Exception as e:
            print(f"  Error during schema mapping: {e}")
            raise
    
    def _get_schema_example(self) -> str:
        """
        Generate a simplified example of the global schema structure.
        Shows the structure without all the nested details.
        """
        example = """
The global schema has these main sections:

1. **metadata**: Company info, payroll number, pay period dates, etc.
   - Each field has: {value, confidence}

2. **balance_employee_tax**: Page-level employee tax aggregates (array)
   - Leave empty [] for now

3. **balance_employer_tax**: Page-level employer tax aggregates (array)
   - Leave empty [] for now

4. **company_totals**: Company-wide totals (if available in interim data)
   - com_period_start_date, com_period_end_date
   - com_balance_earnings[] - array of earnings with code, qtd/ytd hours/amounts
   - com_balance_deductions[] - array of deductions with code, qtd/ytd hours/amounts
   - com_balance_employee_tax[] - array of employee taxes
   - com_balance_employer_tax[] - array of employer taxes

5. **employee_info**: Array of all employees on the page
   - employee_details: employee_number, fullname, ssn, department, pay_frequency, 
                       payment_type, tax statuses, state, pay period dates, etc.
   - balance_earnings[]: Array of earnings (code, description, rate, qtd/ytd hours/amounts)
   - balance_deductions[]: Array of deductions (code, description, qtd/ytd amounts/hours)
   - balance_employee_tax[]: Array of employee taxes (code, description, qtd/ytd amounts, jurisdiction)
   - unmapped_items: Items that couldn't be mapped

6. **unmapped_items**: Page-level unmapped items

**IMPORTANT - SIMPLIFIED FIELD STRUCTURE:**
Each field follows this structure (ONLY 2 properties):
{
  "value": <actual value or null>,
  "confidence": <0.0 to 1.0>
}

DO NOT include "mapped_from" or "notes" properties. Only "value" and "confidence".
"""
        return example
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract JSON from the LLM response.
        Handles cases where the response might include markdown code blocks.
        """
        # Remove markdown code blocks if present
        text = response_text.strip()
        
        if text.startswith("```json"):
            text = text[7:]  # Remove ```json
        elif text.startswith("```"):
            text = text[3:]  # Remove ```
        
        if text.endswith("```"):
            text = text[:-3]  # Remove trailing ```
        
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            print(f"  Failed to parse JSON response: {e}")
            print(f"  Response length: {len(text)} characters")
            print(f"  Response text (first 500 chars): {text[:500]}")
            print(f"  Response text (last 500 chars): {text[-500:]}")
            # Try to save the malformed response for debugging
            debug_path = Path(__file__).parent.parent / "testing" / "debug_malformed_response.txt"
            with open(debug_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"  Saved full response to: {debug_path}")
            raise
    
    def validate_mapped_format(self, data: Dict[str, Any]) -> bool:
        """
        Validate that the mapped data follows the global schema structure.
        
        Args:
            data: The mapped data to validate
        
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check top-level keys
            required_keys = ["metadata", "balance_employee_tax", "balance_employer_tax", 
                           "company_totals", "employee_info", "unmapped_items"]
            
            for key in required_keys:
                if key not in data:
                    print(f"  Validation failed: Missing key '{key}'")
                    return False
            
            # Check that employee_info is an array
            if not isinstance(data["employee_info"], list):
                print(f"  Validation failed: 'employee_info' must be an array")
                return False
            
            # Check that each employee has required sections
            for idx, employee in enumerate(data["employee_info"]):
                required_emp_keys = ["employee_details", "balance_earnings", 
                                    "balance_deductions", "balance_employee_tax"]
                for key in required_emp_keys:
                    if key not in employee:
                        print(f"  Validation failed: Employee {idx} missing '{key}'")
                        return False
            
            print(f"  ✓ Mapped data structure is valid")
            return True
            
        except Exception as e:
            print(f"  Validation error: {e}")
            return False


def map_interim_to_global(
    interim_json_path: str,
    output_json_path: str,
    page_number: int
) -> Dict[str, Any]:
    """
    Convenience function to map an interim JSON file to global schema.
    
    Args:
        interim_json_path: Path to interim JSON file
        output_json_path: Path where mapped JSON should be saved
        page_number: Page number being processed
    
    Returns:
        Mapped data dictionary
    """
    # Load interim data
    with open(interim_json_path, 'r', encoding='utf-8') as f:
        interim_data = json.load(f)
    
    # Map to global schema
    mapper = SchemaMapper()
    mapped_data = mapper.map_to_global_schema(interim_data, page_number)
    
    # Save mapped data
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(mapped_data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ Saved mapped data to: {output_json_path}")
    
    return mapped_data


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) != 4:
        print("Usage: python step3_schema_mapping.py <interim_json_path> <output_json_path> <page_number>")
        sys.exit(1)
    
    interim_path = sys.argv[1]
    output_path = sys.argv[2]
    page_num = int(sys.argv[3])
    
    map_interim_to_global(interim_path, output_path, page_num)
