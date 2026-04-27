# ⚡ APOEMA - Quick Start Guide

Get started with APOEMA in 5 minutes!

## 🚀 Quick Setup

### 1. Clone & Enter Project
```bash
cd crewai-test
```

### 2. Install uv (Fast Dependency Manager)
```bash
# One-liner installer
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv
```

### 3. Install Dependencies & Create Virtual Environment
```bash
# Install with Makefile (recommended - simplest)
make install

# Or manually with uv
uv sync
```

### 4. Configure API Key
Get your free Google Gemini API key from [ai.google.dev](https://ai.google.dev):

```bash
# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"

# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"

# Windows CMD
set GEMINI_API_KEY=your-api-key-here
```

## ⚡ How APOEMA-CrewAI Works

APOEMA-CrewAI analyzes post-graduation programs against CAPES evaluation criteria by analyzing assessment documents and validating program reports in 2 or 3 stages:

### Stage 1: Assessment Analysis (Required)
```bash
make run assessment-file=cc_assessment_data.json
```
- Loads the assessment criteria for your area of study in CAPES classification
- Uses LLM to analyze and extract insights from the assessment
- Generates structured report of evaluation criteria and expectations
- **Output:** `output/output_YYYYMMDDHHMMSS.md`

### Stage 2A: PDF Validation (Optional - Alternative 1)
```bash
make run assessment-file=cc_assessment_data.json pdf-file=cc_report.pdf
```
- Takes the assessment criteria from Stage 1
- Analyzes plots/visualizations from APOEMA-generated PDF report
- Checks if program data meets assessment standards
- Validates that plots are appropriate for the area of study
- **Outputs:** 
  - `output/output_YYYYMMDDHHMMSS.md` (assessment analysis)
  - `output/conformance_report_YYYYMMDDHHMMSS.md` (validation results)
  - `output/utility_assessment_YYYYMMDDHHMMSS.md` (plot utility analysis)

### Stage 2B: PNG+CSV Analysis (Optional - Alternative 2)
```bash
make run assessment-file=cc_assessment_data.json png-file=plot.png csv-file=data.csv
```
- Takes the assessment criteria from Stage 1
- Analyzes a PNG plot image with corresponding CSV data
- Extracts technical metrics and statistical insights
- Validates relevance to the evaluation area and CAPES criteria
- **Outputs:**
  - `output/output_YYYYMMDDHHMMSS.md` (assessment analysis)
  - `output/plot_insights_YYYYMMDDHHMMSS.md` (plot analysis and insights)
  - `output/plot_importance_YYYYMMDDHHMMSS.md` (relevance assessment)

### Custom Output Prefix (Optional)
```bash
make run assessment-file=cc_assessment_data.json prefix=cc_analysis
```
- Changes output file prefix from timestamp to custom name
- Useful for organizing multiple analyses

### Examples
```bash
# Assessment analysis only
make run assessment-file=cc_assessment_data.json

# With PDF report validation
make run assessment-file=cc_assessment_data.json pdf-file=cc_report.pdf prefix=cc_analysis

# With PNG plot and CSV data analysis
make run assessment-file=cc_assessment_data.json png-file=plot.png csv-file=data.csv prefix=plot_analysis

# Full example with all parameters
make run assessment-file=cc_assessment_data.json png-file=plot.png csv-file=data.csv prefix=my_analysis
```

## 📖 Next Steps

- Read [README.md](./README.md) for detailed documentation
- Check [REPORT_ANALYZER_GUIDE.md](./REPORT_ANALYZER_GUIDE.md) for advanced usage
- View generated reports in `output/` directory

## 🆘 Troubleshooting

**API Key not working?**
```bash
echo $GEMINI_API_KEY  # Verify it's set
```

**Module not found?**
```bash
uv sync  # Reinstall dependencies
```

**PDF not found?**
```bash
# Use absolute path or relative from project root
uv run python main.py ./reports/my-report.pdf
```

## 📊 Example Workflow

```bash
# 1. Install dependencies
make install

# 2. Analyze assessment data for your area of study
make run assessment-file=cc_assessment_data.json

# 3. Check results
cat output/output_*.md

# 4A. If you have a program report, validate it against assessment
make run assessment-file=cc_assessment_data.json pdf-file=cc_report.pdf

# 4B. OR if you have a PNG plot with CSV data
make run assessment-file=cc_assessment_data.json png-file=plot.png csv-file=data.csv

# 5. Review analysis results
cat output/conformance_report_*.md  # For PDF analysis
cat output/plot_insights_*.md       # For PNG+CSV analysis

# 6. Clean up generated files
make clean
```

## 💡 Tips

- **assessment_data.json is required:** This defines your area of study in CAPES classification and the evaluation criteria
- **pdf-file is optional:** Use it to validate a program's PDF report against the assessment standards
- **png-file and csv-file are optional:** Use them together to analyze a specific plot with its underlying data (alternative to PDF)
- **prefix is optional:** Defaults to timestamp, use it to organize multiple analyses
- **PDF and PNG+CSV are alternatives:** Provide either PDF OR (PNG + CSV), not both
- **Check output/:** All results are timestamped or prefixed in this directory
- **uv is fast:** Dependency resolution and installation in seconds!

## 🛠️ Advanced uv Usage

### Activate the Virtual Environment Directly
```bash
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate      # Windows
```
Then run commands normally: `python main.py --pdf-file report.pdf`

### Add a New Dependency
```bash
uv add package-name          # Production dependency
uv add --dev package-name    # Development dependency
```

### Update Dependencies
```bash
uv sync --upgrade  # Update all packages
```

## 💻 Using Commands Without Makefile

If you prefer to skip the Makefile, you can use uv directly:

```bash
# Install
uv sync

# Run with arguments
uv run python main.py --pdf-file ./reports/report.pdf
uv run python main.py --assessment-file custom.json --prefix my_analysis
```

---

**Need help?** See [README.md](./README.md) for full documentation.
