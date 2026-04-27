import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_files import PDFFile, TextFile, ImageFile
from prompt_loader import load_agent_prompt, load_task_prompt


# Initialize LLM configuration
def get_llm():
    """Create and return the LLM instance."""
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    return LLM(
        model="gemini/gemini-2.5-flash",
        api_key=gemini_api_key,
        temperature=0.7,
    )


def create_agents(llm):
    """Create and return all agents."""
    data_reader_config = load_agent_prompt("data_reader")
    data_reader = Agent(
        role=data_reader_config["Role"],
        goal=data_reader_config["Goal"],
        backstory=data_reader_config["Backstory"],
        llm=llm,
        verbose=True,
    )

    summarizer_config = load_agent_prompt("summarizer")
    summarizer = Agent(
        role=summarizer_config["Role"],
        goal=summarizer_config["Goal"],
        backstory=summarizer_config["Backstory"],
        llm=llm,
        verbose=True,
    )

    report_analyzer_config = load_agent_prompt("report_analyzer")
    report_analyzer = Agent(
        role=report_analyzer_config["Role"],
        goal=report_analyzer_config["Goal"],
        backstory=report_analyzer_config["Backstory"],
        llm=llm,
        verbose=True,
    )

    utility_assessor_config = load_agent_prompt("utility_assessor")
    utility_assessor = Agent(
        role=utility_assessor_config["Role"],
        goal=utility_assessor_config["Goal"],
        backstory=utility_assessor_config["Backstory"],
        llm=llm,
        verbose=True,
    )

    plot_data_analyst_config = load_agent_prompt("plot_data_analyst")
    plot_data_analyst = Agent(
        role=plot_data_analyst_config["Role"],
        goal=plot_data_analyst_config["Goal"],
        backstory=plot_data_analyst_config["Backstory"],
        llm=llm,
        verbose=True,
    )

    plot_insights_generator_config = load_agent_prompt("plot_insights_generator")
    plot_insights_generator = Agent(
        role=plot_insights_generator_config["Role"],
        goal=plot_insights_generator_config["Goal"],
        backstory=plot_insights_generator_config["Backstory"],
        llm=llm,
        verbose=True,
    )

    return (
        data_reader,
        summarizer,
        report_analyzer,
        utility_assessor,
        plot_data_analyst,
        plot_insights_generator,
    )


def create_tasks(pdf_path, output_prefix, agents, png_path=None, csv_path=None):
    """Create and return all tasks."""
    (
        data_reader,
        summarizer,
        report_analyzer,
        utility_assessor,
        plot_data_analyst,
        plot_insights_generator,
    ) = agents

    # Task 1: Data Analysis
    task1_config = load_task_prompt("task1_analyze")
    task1 = Task(
        description=task1_config["description"],
        agent=data_reader,
        expected_output=task1_config["expected_output"],
    )

    # Task 2: Summarization
    task2_config = load_task_prompt("task2_summarize")
    task2 = Task(
        description=task2_config["description"],
        agent=summarizer,
        expected_output=task2_config["expected_output"],
        markdown=True,
        output_file=f"./output/{output_prefix}_output.md",
        context=[task1],
    )

    tasks = [task1, task2]

    # Optional Tasks 3-6: Report Analysis (requires PDF file)
    if pdf_path and os.path.exists(pdf_path):
        # Task 3: Extract plots from PDF
        task3_config = load_task_prompt("task3_extract_plots")
        task3 = Task(
            description=task3_config["description"],
            agent=report_analyzer,
            expected_output=task3_config["expected_output"],
        )

        # Task 4: Analyze extracted plots
        task4_config = load_task_prompt("task4_analyze_plots")
        task4 = Task(
            description=task4_config["description"],
            agent=report_analyzer,
            expected_output=task4_config["expected_output"],
            context=[task3],
        )

        # Task 5: Map visualizations to CAPES criteria
        task5_config = load_task_prompt("task5_criteria_mapping")
        task5 = Task(
            description=task5_config["description"],
            agent=report_analyzer,
            expected_output=task5_config["expected_output"],
            markdown=True,
            output_file=f"./output/{output_prefix}_conformance_report.md",
            context=[task1, task3, task4],
        )

        # Task 6: Assess utility and assertiveness of graphics
        task6_config = load_task_prompt("task6_utility_assessment")
        task6 = Task(
            description=task6_config["description"],
            agent=utility_assessor,
            expected_output=task6_config["expected_output"],
            markdown=True,
            output_file=f"./output/{output_prefix}_utility_assessment.md",
            context=[task4, task5],
        )

        tasks.extend([task3, task4, task5, task6])

    # Optional Tasks 7-9: PNG + CSV Plot Analysis (alternative to PDF)
    elif png_path and os.path.exists(png_path) and csv_path and os.path.exists(csv_path):
        # Task 7: Analyze PNG image and CSV data
        task7_config = load_task_prompt("task7_plot_data_analysis")
        task7 = Task(
            description=task7_config["description"],
            agent=plot_data_analyst,
            expected_output=task7_config["expected_output"],
        )

        # Task 8: Generate insights and narrative from analysis
        task8_config = load_task_prompt("task8_plot_insights")
        task8 = Task(
            description=task8_config["description"],
            agent=plot_insights_generator,
            expected_output=task8_config["expected_output"],
            markdown=True,
            output_file=f"./output/{output_prefix}_plot_insights.md",
            context=[task1, task2, task7],
        )

        # Task 9: Assess utility and importance of the plot
        task9_config = load_task_prompt("task9_plot_utility_importance")
        task9 = Task(
            description=task9_config["description"],
            agent=utility_assessor,
            expected_output=task9_config["expected_output"],
            markdown=True,
            output_file=f"./output/{output_prefix}_plot_importance.md",
            context=[task1, task2, task7, task8],
        )

        tasks.extend([task7, task8, task9])

    return tasks


def run_apoema_pipeline(assessment_file, pdf_path, output_prefix, png_path=None, csv_path=None):
    """
    Execute the APOEMA assessment analysis pipeline.

    Args:
        assessment_file: Path to the assessment data JSON file
        pdf_path: Path to optional PDF file
        output_prefix: Prefix for output files
        png_path: Path to optional PNG plot image file
        csv_path: Path to optional CSV data file

    Returns:
        result: The result from crew.kickoff()
    """
    llm = get_llm()
    agents = create_agents(llm)
    input_files = {"assessment_data": TextFile(source=assessment_file)}

    # Determine which agents to use
    (
        data_reader,
        summarizer,
        report_analyzer,
        utility_assessor,
        plot_data_analyst,
        plot_insights_generator,
    ) = agents
    crew_agents = [data_reader, summarizer]

    if pdf_path and os.path.exists(pdf_path):
        crew_agents.extend([report_analyzer, utility_assessor])
        input_files["report_pdf"] = PDFFile(source=pdf_path)
    elif png_path and os.path.exists(png_path) and csv_path and os.path.exists(csv_path):
        crew_agents.extend([plot_data_analyst, plot_insights_generator, utility_assessor])
        input_files["plot_image"] = ImageFile(source=png_path)
        input_files["plot_data"] = TextFile(source=csv_path)

    tasks = create_tasks(pdf_path, output_prefix, agents, png_path, csv_path)

    crew = Crew(
        agents=crew_agents,
        tasks=tasks,
        process=Process.sequential,
    )

    result = crew.kickoff(input_files=input_files)
    return result
