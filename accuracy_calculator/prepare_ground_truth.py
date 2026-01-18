"""
Helper script to copy extraction output to golden dataset for manual verification.
Use this to quickly create ground truth templates.
"""

import json
import shutil
from pathlib import Path


def copy_for_annotation(pdf_name: str, page_number: int):
    """
    Copy extracted output to golden dataset folder for manual annotation.
    
    Args:
        pdf_name: Name of PDF (e.g., "PR-Register")
        page_number: Page number to copy
    """
    # Source file
    source_file = Path(f"outputs/{pdf_name}/page_{page_number}/mapped.json")
    
    # Destination
    golden_dir = Path(f"golden_dataset/{pdf_name}")
    golden_dir.mkdir(parents=True, exist_ok=True)
    dest_file = golden_dir / f"ground_truth_page_{page_number}.json"
    
    if not source_file.exists():
        print(f"❌ Source file not found: {source_file}")
        print(f"   Make sure you've run the extraction pipeline first.")
        return
    
    # Copy file
    shutil.copy(source_file, dest_file)
    print(f"✅ Copied to: {dest_file}")
    print(f"\n📝 Next steps:")
    print(f"   1. Open {dest_file}")
    print(f"   2. Open sample_pdfs/{pdf_name}.pdf")
    print(f"   3. Manually verify and correct each field value")
    print(f"   4. Save the corrected file")
    print(f"   5. Run accuracy calculation with:")
    print(f"      python calculate_accuracy.py \\")
    print(f"        outputs/{pdf_name}/page_{page_number}/mapped.json \\")
    print(f"        {dest_file}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python prepare_ground_truth.py <pdf_name> <page_number>")
        print("\nExample:")
        print("  python prepare_ground_truth.py PR-Register 1")
        print("  python prepare_ground_truth.py PR-Register 2")
    else:
        pdf_name = sys.argv[1]
        page_number = int(sys.argv[2])
        copy_for_annotation(pdf_name, page_number)
