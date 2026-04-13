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

## ✅ Run APOEMA

### Option A: Analyze CAPES Criteria Only
```bash
make run
```

**Output:** `output/output_YYYYMMDDHHMMSS.md`

### Option B: Full Analysis with PDF Report
```bash
make run pdf-file=./path/to/report.pdf
```

**Outputs:**
- `output/output_YYYYMMDDHHMMSS.md` - Criteria analysis
- `output/conformance_report_YYYYMMDDHHMMSS.md` - Conformance report

### Other Makefile Options

```bash
# Custom assessment file
make run assessment-file=custom_assessment.json

# Custom output prefix
make run prefix=my_analysis

# All options together
make run assessment-file=custom.json pdf-file=report.pdf prefix=analysis_v2

# View all available commands
make help
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

# 2. Test basic functionality
make run

# 3. Once working, analyze with a PDF
make run pdf-file=./my_report.pdf

# 4. Check results
cat output/output_*.md
cat output/conformance_report_*.md

# 5. Clean up generated files
make clean
```

## 💡 Tips

- **First run:** Use without PDF to ensure setup is correct
- **Use absolute paths:** For PDF files outside the project directory
- **Check output/:** All results are timestamped in this directory
- **Keep assessment_data.json:** This file contains CAPES criteria
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
