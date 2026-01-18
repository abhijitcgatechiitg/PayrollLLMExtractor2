# Financial Data Extraction Pipeline

A multi-stage LLM-based tool to extract structured financial data from PDF documents.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Environment
Create a `.env` file with your Anthropic API key:
```
ANTHROPIC_API_KEY=your_key_here
```

---

## Pipeline Workflow

### Run the Complete Pipeline
Simply run the orchestrator with a PDF filename:

```bash
python main.py <pdf_filename>
```

**Example:**
```bash
python main.py sofp_sample3.pdf
```

This will automatically run:
1. **Step 1** - Extract text from PDF
2. **Step 2** - Classify pages to find SFP
3. **Step 3** - [Coming] Extract raw table data
4. **Step 4** - [Coming] Map to global schema
5. **Step 5** - [Coming] Validate financial data
6. **Step 6** - [Coming] Save final output

---

## Output Files

After running `python main.py sofp_sample3.pdf`, you'll find:

```
outputs/intermediate/
├── sofp_sample3_extracted.json      # Raw extracted pages
└── sofp_sample3_classified.json     # SFP classification results

outputs/final/
└── sofp_sample3_final.json          # [Coming] Final mapped schema
```
