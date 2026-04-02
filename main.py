import os
import json
import argparse
from datetime import datetime
from pipeline import run_apoema_pipeline


def load_assessment_data(filepath="assessment_data.json"):
    """Load assessment data from JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run APOEMA assessment analysis")
    parser.add_argument(
        "--assessment-file",
        type=str,
        default="assessment_data.json",
        help="Path to the assessment data JSON file (default: assessment_data.json)",
    )
    parser.add_argument(
        "--pdf-file",
        type=str,
        default=None,
        help="Path to the PDF report file (optional)",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default=datetime.now().strftime("%Y%m%d%H%M%S"),
        help="Prefix for output files (default: timestamp of execution)",
    )

    args = parser.parse_args()
    return args.assessment_file, args.pdf_file, args.prefix


def main():
    """Main entry point."""
    assessment_file, pdf_path, output_prefix = parse_arguments()
    assessment_data = load_assessment_data(assessment_file)

    if assessment_data is None:
        print(f"Erro: Não foi possível carregar o arquivo {assessment_file}")
        exit(1)

    # Convert assessment data to string for agent processing
    assessment_data_str = json.dumps(assessment_data, ensure_ascii=False, indent=2)

    # Display PDF information
    if pdf_path and os.path.exists(pdf_path):
        print(f"\n✓ Arquivo PDF carregado: {os.path.basename(pdf_path)}")
        print("✓ Tarefas de análise de relatório adicionadas ao pipeline\n")
    else:
        if pdf_path:
            print(f"⚠ Arquivo PDF não encontrado: {pdf_path}")
        print("\n💡 Dica: Execute com um arquivo PDF para análise de relatórios")
        print(
            "   Uso: python main.py --assessment-file <arquivo.json> --pdf-file <arquivo.pdf>"
        )
        print("   Uso (apenas assessment): python main.py --assessment-file <arquivo.json>")
        print(
            "   Uso (com prefixo customizado): python main.py --assessment-file <arquivo.json> --prefix my_run"
        )
        print("\nExecutando apenas tarefas 1 e 2...\n")

    # Run the APOEMA pipeline
    result = run_apoema_pipeline(assessment_data_str, pdf_path, output_prefix)

    print("\n" + "=" * 80)
    print("EXECUÇÃO CONCLUÍDA")
    print("=" * 80)


if __name__ == "__main__":
    main()
