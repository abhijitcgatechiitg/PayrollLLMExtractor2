# Payroll LLM Extractor

A two-pass AI-powered system for extracting structured payroll data from PDF documents. Built with Claude AI and designed to handle various payroll formats with high accuracy.

## 🎯 What It Does

This tool automatically extracts employee payroll information from PDF reports and converts it into a standardized JSON format. It handles:

- Multiple employees per page
- Various earnings, deductions, and tax types
- Quarter-to-date (QTD) and Year-to-date (YTD) values
- Company-level totals and aggregates
- Employee and employer tax information

## ✨ Key Features

- **Two-Pass Extraction**: First extracts raw data, then maps to standardized schema
- **No Inference**: Only extracts explicitly present data - never calculates or assumes values
- **Confidence Scoring**: Each extracted field includes a confidence level (0.0 - 1.0)
- **Page-by-Page Processing**: Handles multi-page documents with independent page processing
- **Performance Tracking**: Built-in statistics for processing time and token usage

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Anthropic API key ([Get one here](https://www.anthropic.com/))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/abhijitcgatechiitg/PayrollLLMExtractor2.git
cd PayrollLLMExtractor2
```

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in root directory:
```
ANTHROPIC_API_KEY=your_api_key_here
```

### Usage

Run the extraction pipeline on a PDF:
```bash
python main.py sample_pdfs/PR-Register.pdf
```

The tool will process each page and save outputs to the `outputs/` directory.

## 📊 Output Structure

For each processed PDF, the system creates:

```
outputs/
└── your_pdf_name/
    ├── page_1/
    │   ├── interim.json    # Raw extracted data
    │   └── mapped.json     # Standardized schema output
    ├── page_2/
    │   ├── interim.json
    │   └── mapped.json
    └── pipeline_summary.json  # Overall statistics
```

### Sample Output

Each employee record includes:
- Full name and identification
- Earnings breakdown (regular, overtime, bonuses, etc.)
- Deductions (insurance, retirement, etc.)
- Tax withholdings (federal, state, local, etc.)
- Balance totals with QTD/YTD values
- Confidence scores for each field

## 📁 Project Structure

```
├── schema/              # Global schema definition
├── src/                 # Core extraction pipeline
│   ├── prompts/        # AI prompts for extraction and mapping
│   └── step*.py        # Pipeline stages
├── design_phase/       # Design documentation
├── sample_pdfs/        # Sample payroll documents
├── testing/            # Test scripts
└── main.py            # Pipeline orchestrator
```

## 📈 Performance

Tested on sample 2-page payroll document (13 employees):
- **Processing Time**: ~2.5 minutes total
- **Token Usage**: ~21K tokens per page average
- **Success Rate**: 100% extraction accuracy

## 🛠️ Requirements

- `pymupdf==1.26.7` - PDF text extraction
- `anthropic==0.76.0` - Claude AI API
- `python-dotenv==1.2.1` - Environment configuration

See [requirements.txt](requirements.txt) for complete list.

## 📖 Documentation

Detailed documentation available in `design_phase/`:
- Complete project summary
- Schema design rationale
- Code structure decisions
- Implementation details

## 🤝 Contributing

This is a specialized extraction system. For questions or suggestions, please open an issue.

## 📄 License

This project is available for educational and research purposes.

## 👤 Author

**Akshit**  
GitHub: [@abhijitcgatechiitg](https://github.com/abhijitcgatechiitg)

---

Built with ❤️ using Claude AI
