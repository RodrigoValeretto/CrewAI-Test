.PHONY: install run help clean

# Default target
help:
	@echo "APOEMA - Available commands:"
	@echo ""
	@echo "  make install                                   Install dependencies (uv sync)"
	@echo "  make run assessment-file=<path>               Run APOEMA (assessment analysis only)"
	@echo "  make run assessment-file=<path> pdf-file=<path>"
	@echo "                                                 Run with PDF plot analysis"
	@echo "  make run assessment-file=<path> png-file=<path> csv-file=<path>"
	@echo "                                                 Run with PNG+CSV plot analysis"
	@echo "  make run prefix=<string>                       Specify custom prefix for output files"
	@echo "  make help                                      Show this help message"
	@echo "  make clean                                     Clean generated output and cache"
	@echo ""
	@echo "Examples:"
	@echo "  make install"
	@echo "  make run assessment-file=cc_assessment_data.json"
	@echo "  make run assessment-file=cc_assessment_data.json pdf-file=cc_report.pdf"
	@echo "  make run assessment-file=cc_assessment_data.json png-file=plot.png csv-file=data.csv"
	@echo "  make run assessment-file=cc_assessment_data.json pdf-file=cc_report.pdf prefix=cc_analysis"
	@echo "  make run assessment-file=cc_assessment_data.json png-file=plot.png csv-file=data.csv prefix=plot_analysis"

# Install dependencies using uv
install:
	@echo "Installing dependencies with uv..."
	uv sync
	@echo "✓ Dependencies installed!"

# Run the main script with optional arguments
run:
	@uv run python main.py \
		$(if $(assessment-file),--assessment-file $(assessment-file)) \
		$(if $(pdf-file),--pdf-file $(pdf-file)) \
		$(if $(png-file),--png-file $(png-file)) \
		$(if $(csv-file),--csv-file $(csv-file)) \
		$(if $(prefix),--prefix $(prefix))

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	rm -rf output/*.md
	rm -rf __pycache__
	rm -rf .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned!"


