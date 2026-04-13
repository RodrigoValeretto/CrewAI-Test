.PHONY: install run help clean

# Default target
help:
	@echo "APOEMA - Available commands:"
	@echo ""
	@echo "  make install                          Install dependencies (uv sync)"
	@echo "  make run                              Run APOEMA with default settings"
	@echo "  make run assessment-file=<path>       Specify custom assessment JSON file"
	@echo "  make run pdf-file=<path>              Specify PDF report file"
	@echo "  make run prefix=<string>              Specify custom prefix for output files"
	@echo "  make run assessment-file=<path> pdf-file=<path> prefix=<string>"
	@echo "                                        Use multiple custom options"
	@echo "  make help                             Show this help message"
	@echo "  make clean                            Clean generated output and cache"
	@echo ""
	@echo "Examples:"
	@echo "  make install"
	@echo "  make run"
	@echo "  make run assessment-file=custom_assessment.json"
	@echo "  make run pdf-file=./reports/report.pdf"
	@echo "  make run prefix=my_analysis"
	@echo "  make run assessment-file=custom.json pdf-file=report.pdf prefix=analysis_v2"

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
		$(if $(prefix),--prefix $(prefix))

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	rm -rf output/*.md
	rm -rf __pycache__
	rm -rf .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned!"


