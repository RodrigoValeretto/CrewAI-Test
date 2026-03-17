import os
import json
import sys
from crewai import Agent, Task, Crew, Process, LLM
from crewai_files import PDFFile
from datetime import datetime
from prompt_loader import load_agent_prompt, load_task_prompt

# 1. Configuration: Get your free API key from Google AI Studio
gemini_api_key = os.getenv("GEMINI_API_KEY")

agent_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=gemini_api_key,
    temperature=0.7,
)


# 2. Load assessment data from JSON file
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
    assessment_file = "assessment_data.json"
    pdf_path = None
    
    if len(sys.argv) > 1:
        assessment_file = sys.argv[1]
    
    if len(sys.argv) > 2:
        pdf_path = sys.argv[2]
    
    return assessment_file, pdf_path


assessment_file, pdf_path = parse_arguments()
assessment_data = load_assessment_data(assessment_file)

if assessment_data is None:
    print(f"Erro: Não foi possível carregar o arquivo {assessment_file}")
    exit(1)

# Convert assessment data to string for agent processing
assessment_data_str = json.dumps(assessment_data, ensure_ascii=False, indent=2)

# 3. Define your Agents
data_reader_config = load_agent_prompt("data_reader")
data_reader = Agent(
    role=data_reader_config["Role"],
    goal=data_reader_config["Goal"],
    backstory=data_reader_config["Backstory"],
    llm=agent_llm,
    verbose=True,
)

summarizer_config = load_agent_prompt("summarizer")
summarizer = Agent(
    role=summarizer_config["Role"],
    goal=summarizer_config["Goal"],
    backstory=summarizer_config["Backstory"],
    llm=agent_llm,
    verbose=True,
)

report_analyzer_config = load_agent_prompt("report_analyzer")
report_analyzer = Agent(
    role=report_analyzer_config["Role"],
    goal=report_analyzer_config["Goal"],
    backstory=report_analyzer_config["Backstory"],
    llm=agent_llm,
    verbose=True,
)

# 4. Define Tasks
task1_config = load_task_prompt("task1_analyze", assessment_data_str)
task1 = Task(
    description=task1_config["description"],
    agent=data_reader,
    expected_output=task1_config["expected_output"],
)

task2_config = load_task_prompt("task2_summarize")
task2 = Task(
    description=task2_config["description"],
    agent=summarizer,
    expected_output=task2_config["expected_output"],
    markdown=True,
    output_file=f"./output/output_{datetime.now().strftime('%Y%m%d%H%M%S')}.md",
)

# 5. Optional Tasks 3-5: Report Analysis (requires PDF file)
pdf_path = parse_arguments()
tasks = [task1, task2]
agents = [data_reader, summarizer]

if pdf_path and os.path.exists(pdf_path):
    print(f"\n✓ Arquivo PDF carregado: {os.path.basename(pdf_path)}")

    # Task 3: Extract plots from PDF
    task3_config = load_task_prompt("task3_extract_plots")
    task3 = Task(
        description=task3_config["description"],
        agent=report_analyzer,
        expected_output=task3_config["expected_output"],
        input_files={
            "pdf_report": PDFFile(source=pdf_path),
        },
    )

    # Task 4: Analyze extracted plots
    task4_config = load_task_prompt("task4_analyze_plots")
    task4 = Task(
        description=task4_config["description"],
        agent=report_analyzer,
        expected_output=task4_config["expected_output"],
    )

    # Task 5: Map visualizations to CAPES criteria
    task5_config = load_task_prompt("task5_criteria_mapping")
    task5 = Task(
        description=task5_config["description"],
        agent=report_analyzer,
        expected_output=task5_config["expected_output"],
        markdown=True,
        output_file=f"./output/conformance_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.md",
    )

    tasks.extend([task3, task4, task5])
    agents.append(report_analyzer)
    print("✓ Tarefas de análise de relatório adicionadas ao pipeline\n")
else:
    if pdf_path:
        print(f"⚠ Arquivo PDF não encontrado: {pdf_path}")
    print("\n💡 Dica: Execute com um arquivo PDF para análise de relatórios")
    print("   Uso: python main.py <arquivo_assessment.json> <caminho_do_pdf>")
    print("   Uso (apenas assessment): python main.py <arquivo_assessment.json>")
    print("\nExecutando apenas tarefas 1 e 2...\n")

# 6. Kickoff the Crew
crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.sequential,
)

result = crew.kickoff()
print("\n" + "=" * 80)
print("EXECUÇÃO CONCLUÍDA")
print("=" * 80)
