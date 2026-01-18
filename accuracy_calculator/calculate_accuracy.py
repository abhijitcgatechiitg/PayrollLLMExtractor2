"""
Accuracy Calculator for Payroll Extraction System

Compares extracted data against ground truth to calculate field-level accuracy.
Provides simple metrics: total fields, correct fields, incorrect fields, missing fields.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime


class AccuracyCalculator:
    """Calculate field-level accuracy by comparing extracted vs ground truth data."""
    
    def __init__(self):
        self.results = {
            'total_fields': 0,
            'correct_fields': 0,
            'incorrect_fields': 0,
            'missing_fields': 0,
            'accuracy_percentage': 0.0,
            'field_details': []
        }
    
    def compare_values(self, extracted: Any, ground_truth: Any, field_path: str) -> Dict:
        """
        Compare extracted value with ground truth.
        
        Returns dict with: field_path, extracted_value, ground_truth_value, status
        """
        result = {
            'field_path': field_path,
            'extracted_value': extracted,
            'ground_truth_value': ground_truth,
            'status': 'unknown'
        }
        
        # Handle null/None cases
        if ground_truth is None or ground_truth == "":
            if extracted is None or extracted == "":
                result['status'] = 'correct_null'
            else:
                result['status'] = 'false_positive'  # Extracted something that shouldn't exist
            return result
        
        if extracted is None or extracted == "":
            result['status'] = 'missing'
            return result
        
        # Compare values
        if self._values_match(extracted, ground_truth):
            result['status'] = 'correct'
        else:
            result['status'] = 'incorrect'
        
        return result
    
    def _values_match(self, val1: Any, val2: Any) -> bool:
        """Check if two values match (with tolerance for floats)."""
        # Exact match
        if val1 == val2:
            return True
        
        # Try numeric comparison with tolerance
        try:
            # Convert to float if possible
            if isinstance(val1, str) and isinstance(val2, str):
                # Remove commas for numeric strings
                num1 = float(val1.replace(',', ''))
                num2 = float(val2.replace(',', ''))
                # Allow 0.01 tolerance for rounding
                return abs(num1 - num2) < 0.01
        except (ValueError, AttributeError):
            pass
        
        # Case-insensitive string match
        try:
            return str(val1).strip().lower() == str(val2).strip().lower()
        except:
            pass
        
        return False
    
    def compare_field_structure(self, extracted_field: Dict, ground_truth_field: Dict, 
                               field_path: str) -> Dict:
        """
        Compare a field with {value, confidence} structure.
        Only compares the 'value' part.
        """
        extracted_value = extracted_field.get('value') if isinstance(extracted_field, dict) else extracted_field
        ground_truth_value = ground_truth_field.get('value') if isinstance(ground_truth_field, dict) else ground_truth_field
        
        return self.compare_values(extracted_value, ground_truth_value, field_path)
    
    def traverse_and_compare(self, extracted: Any, ground_truth: Any, path: str = "root"):
        """
        Recursively traverse JSON structures and compare all fields.
        """
        # Skip metadata and non-data fields
        skip_fields = ['extraction_timestamp', 'source_file', 'document_type']
        
        if isinstance(ground_truth, dict) and isinstance(extracted, dict):
            for key in ground_truth.keys():
                if key in skip_fields:
                    continue
                
                current_path = f"{path}.{key}" if path != "root" else key
                
                # If this looks like a field with {value, confidence} structure
                if isinstance(ground_truth.get(key), dict) and 'value' in ground_truth.get(key, {}):
                    extracted_field = extracted.get(key, {'value': None, 'confidence': 0.0})
                    comparison = self.compare_field_structure(extracted_field, ground_truth[key], current_path)
                    self._record_comparison(comparison)
                
                # If it's a nested structure, recurse
                elif isinstance(ground_truth.get(key), (dict, list)):
                    self.traverse_and_compare(
                        extracted.get(key, {} if isinstance(ground_truth[key], dict) else []),
                        ground_truth[key],
                        current_path
                    )
        
        elif isinstance(ground_truth, list) and isinstance(extracted, list):
            # Compare lists (like employee arrays)
            for idx, gt_item in enumerate(ground_truth):
                current_path = f"{path}[{idx}]"
                extracted_item = extracted[idx] if idx < len(extracted) else {}
                self.traverse_and_compare(extracted_item, gt_item, current_path)
    
    def _record_comparison(self, comparison: Dict):
        """Record a single field comparison."""
        self.results['total_fields'] += 1
        self.results['field_details'].append(comparison)
        
        status = comparison['status']
        if status == 'correct' or status == 'correct_null':
            self.results['correct_fields'] += 1
        elif status == 'incorrect' or status == 'false_positive':
            self.results['incorrect_fields'] += 1
        elif status == 'missing':
            self.results['missing_fields'] += 1
    
    def calculate_accuracy(self, extracted_file: Path, ground_truth_file: Path) -> Dict:
        """
        Calculate accuracy by comparing extracted output with ground truth.
        
        Args:
            extracted_file: Path to extracted/mapped.json
            ground_truth_file: Path to ground_truth.json
        
        Returns:
            Dictionary with accuracy metrics
        """
        # Reset results
        self.results = {
            'total_fields': 0,
            'correct_fields': 0,
            'incorrect_fields': 0,
            'missing_fields': 0,
            'accuracy_percentage': 0.0,
            'field_details': []
        }
        
        # Load files
        with open(extracted_file, 'r') as f:
            extracted_data = json.load(f)
        
        with open(ground_truth_file, 'r') as f:
            ground_truth_data = json.load(f)
        
        # Compare all fields
        self.traverse_and_compare(extracted_data, ground_truth_data)
        
        # Calculate accuracy percentage
        if self.results['total_fields'] > 0:
            self.results['accuracy_percentage'] = (
                self.results['correct_fields'] / self.results['total_fields']
            ) * 100
        
        return self.results
    
    def print_summary(self, results: Dict = None):
        """Print a client-friendly summary of accuracy results."""
        if results is None:
            results = self.results
        
        print("\n" + "="*70)
        print("ACCURACY REPORT")
        print("="*70)
        print(f"\n📊 Overall Accuracy: {results['accuracy_percentage']:.2f}%")
        print(f"\n📈 Field Statistics:")
        print(f"   Total Fields Checked: {results['total_fields']}")
        print(f"   ✅ Correct: {results['correct_fields']}")
        print(f"   ❌ Incorrect: {results['incorrect_fields']}")
        print(f"   ⚠️  Missing: {results['missing_fields']}")
        
        # Show some incorrect fields as examples
        incorrect_fields = [f for f in results['field_details'] if f['status'] in ['incorrect', 'missing']]
        if incorrect_fields:
            print(f"\n❌ Issues Found ({len(incorrect_fields)} total):")
            for field in incorrect_fields[:10]:  # Show first 10
                status_icon = "❌" if field['status'] == 'incorrect' else "⚠️"
                print(f"   {status_icon} {field['field_path']}")
                print(f"      Expected: {field['ground_truth_value']}")
                print(f"      Got: {field['extracted_value']}")
        
        print("\n" + "="*70)
    
    def save_detailed_report(self, output_file: Path, results: Dict = None):
        """Save detailed accuracy report to JSON file."""
        if results is None:
            results = self.results
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_fields': results['total_fields'],
                'correct_fields': results['correct_fields'],
                'incorrect_fields': results['incorrect_fields'],
                'missing_fields': results['missing_fields'],
                'accuracy_percentage': results['accuracy_percentage']
            },
            'field_details': results['field_details']
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: {output_file}")


def main():
    """Example usage: Calculate accuracy for a specific page."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python calculate_accuracy.py <extracted_file> <ground_truth_file>")
        print("\nExample:")
        print("  python calculate_accuracy.py \\")
        print("    outputs/PR-Register/page_1/mapped.json \\")
        print("    golden_dataset/PR-Register/ground_truth_page_1.json")
        return
    
    extracted_file = Path(sys.argv[1])
    ground_truth_file = Path(sys.argv[2])
    
    if not extracted_file.exists():
        print(f"Error: Extracted file not found: {extracted_file}")
        return
    
    if not ground_truth_file.exists():
        print(f"Error: Ground truth file not found: {ground_truth_file}")
        return
    
    # Calculate accuracy
    calculator = AccuracyCalculator()
    results = calculator.calculate_accuracy(extracted_file, ground_truth_file)
    
    # Print summary
    calculator.print_summary(results)
    
    # Save detailed report
    report_file = extracted_file.parent / "accuracy_report.json"
    calculator.save_detailed_report(report_file, results)


if __name__ == "__main__":
    main()
