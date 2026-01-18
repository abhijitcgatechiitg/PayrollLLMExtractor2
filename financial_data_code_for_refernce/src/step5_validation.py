"""
Step 5: Validation Layer
Validates financial data integrity.
Checks: accounting equation, numeric values, subtotals, etc.
"""

import re
from typing import Dict, List, Tuple


class FinancialValidator:
    """Validates financial statement data."""
    
    def __init__(self):
        """Initialize validator."""
        self.errors = []
        self.warnings = []
    
    def validate_mapped_data(self, mapped_data: Dict) -> Dict:
        """
        Validate the mapped financial data.
        
        Args:
            mapped_data: Mapped schema from Step 4
            
        Returns:
            Validation result with errors and warnings
        """
        self.errors = []
        self.warnings = []
        
        # Run validation checks
        self._validate_accounting_equation(mapped_data)
        self._validate_numeric_values(mapped_data)
        self._validate_subtotals(mapped_data)
        self._validate_consistency(mapped_data)
        self._validate_unmapped_items(mapped_data)
        
        # Compile results
        validation_result = {
            'accounting_equation_valid': len([e for e in self.errors if 'accounting equation' in e]) == 0,
            'total_errors': len(self.errors),
            'total_warnings': len(self.warnings),
            'errors': self.errors,
            'warnings': self.warnings,
            'status': 'PASS' if len(self.errors) == 0 else 'FAIL'
        }
        
        return validation_result
    
    def _validate_accounting_equation(self, mapped_data: Dict):
        """Validate: Assets = Liabilities + Equity"""
        try:
            assets_total = self._extract_numeric_value(
                mapped_data.get('AssetsTotal', {}).get('years', {})
            )
            
            liab_total = self._extract_numeric_value(
                mapped_data.get('LiabilitiesTotal', {}).get('years', {})
            )
            
            equity_total = self._extract_numeric_value(
                mapped_data.get('Equity', {}).get('TotalEquity', {}).get('years', {})
            )
            
            if assets_total is not None and liab_total is not None and equity_total is not None:
                expected_assets = liab_total + equity_total
                
                if abs(assets_total - expected_assets) > 1:  # Allow 1 unit difference for rounding
                    self.errors.append(
                        f"Accounting equation failed: Assets ({assets_total}) ≠ "
                        f"Liabilities ({liab_total}) + Equity ({equity_total})"
                    )
                else:
                    # Equation is valid
                    pass
            else:
                self.warnings.append("Cannot validate accounting equation - missing total values")
                
        except Exception as e:
            self.warnings.append(f"Error validating accounting equation: {str(e)}")
    
    def _validate_numeric_values(self, mapped_data: Dict):
        """Check that all values are numeric."""
        for section in ['Equity', 'NonCurrentLiabilities', 'CurrentLiabilities', 
                        'NonCurrentAssets', 'CurrentAssets']:
            if section not in mapped_data:
                continue
            
            section_data = mapped_data[section]
            
            for field_name, field_obj in section_data.items():
                if not isinstance(field_obj, dict):
                    continue
                
                years = field_obj.get('years', {})
                for year, value in years.items():
                    if value is None or value == '':
                        continue
                    
                    if not self._is_numeric(value):
                        self.errors.append(
                            f"{section}.{field_name} has non-numeric value for {year}: '{value}'"
                        )
    
    def _validate_subtotals(self, mapped_data: Dict):
        """Check that subtotals roughly equal sum of components."""
        # Check Current Assets
        current_assets = mapped_data.get('CurrentAssets', {})
        if 'TotalCurrentAssets' in current_assets:
            total = self._extract_numeric_value(current_assets['TotalCurrentAssets'].get('years', {}))
            components_sum = sum([
                self._extract_numeric_value(v.get('years', {}))
                for k, v in current_assets.items() 
                if k != 'TotalCurrentAssets' and isinstance(v, dict)
            ])
            
            if total and components_sum and abs(total - components_sum) > components_sum * 0.01:  # 1% tolerance
                self.warnings.append(
                    f"CurrentAssets total ({total}) differs from sum of components ({components_sum})"
                )
        
        # Similar checks for other asset/liability sections could be added
    
    def _validate_consistency(self, mapped_data: Dict):
        """Check consistency across years."""
        years = mapped_data.get('metadata', {}).get('years', [])
        
        if len(years) < 2:
            return  # Need at least 2 years to compare
        
        # Check for consistent structure across years
        for section in ['Equity', 'NonCurrentAssets']:
            if section not in mapped_data:
                continue
            
            for field_name, field_obj in mapped_data[section].items():
                if not isinstance(field_obj, dict):
                    continue
                
                year_values = field_obj.get('years', {})
                if len(year_values) < len(years):
                    self.warnings.append(
                        f"{section}.{field_name} missing data for {len(years) - len(year_values)} year(s)"
                    )
    
    def _validate_unmapped_items(self, mapped_data: Dict):
        """Check for critical unmapped items."""
        unmapped = mapped_data.get('unmapped_items', {}).get('items', [])
        
        if len(unmapped) > 10:
            self.warnings.append(
                f"High number of unmapped items ({len(unmapped)}). Check schema coverage."
            )
        
        # Check for potentially important unmapped items
        critical_keywords = ['total', 'assets', 'liabilities', 'equity']
        for item in unmapped:
            label = item.get('label_raw', '').lower()
            if any(keyword in label for keyword in critical_keywords):
                self.warnings.append(
                    f"Potentially important item unmapped: '{item.get('label_raw')}'"
                )
    
    def _is_numeric(self, value) -> bool:
        """Check if value is numeric."""
        if isinstance(value, (int, float)):
            return True
        
        if isinstance(value, str):
            # Remove common formatting
            cleaned = value.replace(',', '').replace(' ', '').strip()
            try:
                float(cleaned)
                return True
            except ValueError:
                return False
        
        return False
    
    def _extract_numeric_value(self, years_dict: Dict) -> float:
        """Extract first numeric value from years dictionary."""
        for year, value in years_dict.items():
            if value is None or value == '':
                continue
            
            if isinstance(value, (int, float)):
                return float(value)
            
            if isinstance(value, str):
                cleaned = value.replace(',', '').replace(' ', '')
                try:
                    return float(cleaned)
                except ValueError:
                    continue
        
        return None


if __name__ == "__main__":
    print("This module should be run via main.py")
    print("Usage: python main.py <pdf_filename>")
