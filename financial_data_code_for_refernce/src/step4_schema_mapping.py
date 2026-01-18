"""
Step 4: Schema Mapping (PASS 2)
Maps raw interim data to global schema with confidence scores.
Output: mapped.json with structured financial data
"""

import json
import os
import copy
from typing import Dict, List
from dotenv import load_dotenv
from anthropic import Anthropic
from src.prompts.mapper_prompt import get_mapper_prompt
from schema.global_schema import GLOBAL_SFP_SCHEMA

# Load environment variables
load_dotenv()


class SchemaMatcher:
    """Maps raw financial data to global schema."""
    
    def __init__(self, model: str = "claude-3-haiku-20240307"):
        """
        Initialize the matcher with Anthropic client.
        
        Args:
            model: Claude model to use
        """
        self.client = Anthropic()
        self.model = model
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def map_interim_to_schema(self, interim_data: Dict, metadata: Dict = None) -> Dict:
        """
        Map interim JSON to global schema with confidence scores.
        
        Args:
            interim_data: Dictionary with 'items' list from Step 3
            metadata: Currency, years, etc.
            
        Returns:
            Dictionary following global schema structure with mapped values
        """
        items = interim_data.get('items', [])
        
        if not items:
            print("Warning: No items to map")
            return self._create_empty_mapped_schema(metadata or {})
        
        print(f"Mapping {len(items)} items to global schema...")
        
        # Send items to Claude for mapping
        prompt = get_mapper_prompt(items, GLOBAL_SFP_SCHEMA)
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text
            
            # Parse Claude's mapping response
            try:
                mappings = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to extract JSON from response
                import re
                json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                if json_match:
                    mappings = json.loads(json_match.group())
                else:
                    raise ValueError("No valid JSON found in response")
            
            # Build schema with mapped values
            mapped_schema = self._build_mapped_schema(
                mappings, 
                interim_data, 
                metadata or {}
            )
            
            return mapped_schema
            
        except Exception as e:
            print(f"Error during mapping: {e}")
            return self._create_empty_mapped_schema(metadata or {})
    
    def _build_mapped_schema(self, mappings: List[Dict], interim_data: Dict, metadata: Dict) -> Dict:
        """
        Build the mapped schema by filling in values from interim data.
        
        Args:
            mappings: List of mapping results from Claude
            interim_data: Original interim data with values
            metadata: Currency, years, etc.
            
        Returns:
            Populated schema dictionary
        """
        # Start with template
        mapped = copy.deepcopy(GLOBAL_SFP_SCHEMA)
        
        # Set metadata
        mapped['metadata']['currency'] = metadata.get('currency', interim_data.get('currency', 'Unknown'))
        mapped['metadata']['years'] = metadata.get('years', interim_data.get('years', []))
        mapped['metadata']['extraction_timestamp'] = metadata.get('extraction_timestamp', '')
        
        unmapped = []
        
        # Process each mapping
        for mapping in mappings:
            schema_field = mapping.get('schema_field')
            section = mapping.get('section')
            confidence = mapping.get('confidence', 0.0)
            label_raw = mapping.get('label_raw', '')
            values = mapping.get('values', {})
            is_total = mapping.get('is_total', False)
            
            if schema_field and section:
                # Valid mapping - populate schema
                try:
                    field_obj = mapped[section][schema_field]
                    
                    # Fill in values
                    if values:
                        field_obj['value'] = list(values.values())[0] if values else None  # Primary value
                        field_obj['years'] = values
                    
                    field_obj['confidence'] = confidence
                    field_obj['currency'] = metadata.get('currency', interim_data.get('currency'))
                    field_obj['notes'] = mapping.get('reason', '')
                    field_obj['is_total'] = is_total
                    
                except (KeyError, TypeError) as e:
                    print(f"Warning: Could not map to {section}.{schema_field}: {e}")
                    unmapped.append({
                        'label_raw': label_raw,
                        'values': values,
                        'reason': f'Failed to map to schema: {str(e)}'
                    })
            else:
                # Unmapped item
                unmapped.append({
                    'label_raw': label_raw,
                    'values': values,
                    'reason': mapping.get('reason', 'No matching schema field')
                })
        
        # Add unmapped items
        mapped['unmapped_items']['items'] = unmapped
        
        return mapped
    
    def _create_empty_mapped_schema(self, metadata: Dict) -> Dict:
        """Create an empty schema with metadata only."""
        schema = copy.deepcopy(GLOBAL_SFP_SCHEMA)
        schema['metadata'].update(metadata)
        return schema


if __name__ == "__main__":
    print("This module should be run via main.py")
    print("Usage: python main.py <pdf_filename>")
