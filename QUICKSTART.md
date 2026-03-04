# ⚡ APOEMA - Quick Start Guide

Get started with APOEMA in 5 minutes!

## 🚀 Quick Setup

### 1. Clone & Enter Project
```bash
cd crewai-test
```

### 2. Setup Python Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
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
python main.py
```

**Output:** `output/output_YYYYMMDDHHMMSS.md`

### Option B: Full Analysis with PDF Report
```bash
python main.py /path/to/report.pdf
```

**Outputs:**
- `output/output_YYYYMMDDHHMMSS.md` - Criteria analysis
- `output/conformance_report_YYYYMMDDHHMMSS.md` - Conformance report

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
pip install crewai crewai_files google-generativeai
```

**PDF not found?**
```bash
# Use absolute path or relative from project root
python main.py ./reports/my-report.pdf
```

## 📊 Example Workflow

```bash
# 1. Test basic functionality
python main.py

# 2. Once working, analyze with a PDF
python main.py ./my_report.pdf

# 3. Check results
cat output/output_*.md
cat output/conformance_report_*.md
```

## 💡 Tips

- **First run:** Use without PDF to ensure setup is correct
- **Use absolute paths:** For PDF files outside the project directory
- **Check output/:** All results are timestamped in this directory
- **Keep assessment_data.json:** This file contains CAPES criteria

---

**Need help?** See [README.md](./README.md) for full documentation.
