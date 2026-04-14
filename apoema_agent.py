import os
import json
from crewai import Agent, Task, Crew, Process, LLM
from crewai_files import PDFFile
from prompt_loader import load_agent_prompt_yaml, load_task_prompt_yaml


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
    data_reader_config = load_agent_prompt_yaml("data_reader")
    data_reader = Agent(
        role=data_reader_config["Role"],
        goal=data_reader_config["Goal"],
        backstory=data_reader_config["Backstory"],
        llm=llm,
        verbose=True,
    )

    summarizer_config = load_agent_prompt_yaml("summarizer")
    summarizer = Agent(
        role=summarizer_config["Role"],
        goal=summarizer_config["Goal"],
        backstory=summarizer_config["Backstory"],
        llm=llm,
        verbose=True,
    )

    report_analyzer_config = load_agent_prompt_yaml("report_analyzer")
    report_analyzer = Agent(
        role=report_analyzer_config["Role"],
        goal=report_analyzer_config["Goal"],
        backstory=report_analyzer_config["Backstory"],
        llm=llm,
        verbose=True,
    )

    utility_assessor_config = load_agent_prompt_yaml("utility_assessor")
    utility_assessor = Agent(
        role=utility_assessor_config["Role"],
        goal=utility_assessor_config["Goal"],
        backstory=utility_assessor_config["Backstory"],
        llm=llm,
        verbose=True,
    )

    return data_reader, summarizer, report_analyzer, utility_assessor


def create_tasks(assessment_data_str, pdf_path, output_prefix, agents):
    """Create and return all tasks."""
    data_reader, summarizer, report_analyzer, utility_assessor = agents

    # Task 1: Data Analysis
    task1_config = load_task_prompt_yaml("task1_analyze", assessment_data_str)
    task1 = Task(
        description=task1_config["description"],
        agent=data_reader,
        expected_output=task1_config["expected_output"],
    )

    # Task 2: Summarization
    task2_config = load_task_prompt_yaml("task2_summarize")
    task2 = Task(
        description=task2_config["description"],
        agent=summarizer,
        expected_output=task2_config["expected_output"],
        markdown=True,
        output_file=f"./output/{output_prefix}_output.md",
    )

    tasks = [task1, task2]

    # Optional Tasks 3-6: Report Analysis (requires PDF file)
    if pdf_path and os.path.exists(pdf_path):
        # Task 3: Extract plots from PDF
        task3_config = load_task_prompt_yaml("task3_extract_plots")
        task3 = Task(
            description=task3_config["description"],
            agent=report_analyzer,
            expected_output=task3_config["expected_output"],
            input_files={
                "pdf_report": PDFFile(source=pdf_path),
            },
        )

        # Task 4: Analyze extracted plots
        task4_config = load_task_prompt_yaml("task4_analyze_plots")
        task4 = Task(
            description=task4_config["description"],
            agent=report_analyzer,
            expected_output=task4_config["expected_output"],
        )

        # Task 5: Map visualizations to CAPES criteria
        task5_config = load_task_prompt_yaml("task5_criteria_mapping")
        task5 = Task(
            description=task5_config["description"],
            agent=report_analyzer,
            expected_output=task5_config["expected_output"],
            markdown=True,
            output_file=f"./output/{output_prefix}_conformance_report.md",
        )

        # Task 6: Assess utility and assertiveness of graphics
        task6_config = load_task_prompt_yaml("task6_utility_assessment")
        task6 = Task(
            description=task6_config["description"],
            agent=utility_assessor,
            expected_output=task6_config["expected_output"],
            markdown=True,
            output_file=f"./output/{output_prefix}_utility_assessment.md",
        )

        tasks.extend([task3, task4, task5, task6])

    return tasks


def run_apoema_pipeline(assessment_data_str, pdf_path, output_prefix):
    """
    Execute the APOEMA assessment analysis pipeline.
    
    Args:
        assessment_data_str: Assessment data as JSON string
        pdf_path: Path to optional PDF file
        output_prefix: Prefix for output files
        
    Returns:
        result: The result from crew.kickoff()
    """
    llm = get_llm()
    agents = create_agents(llm)
    
    # Determine which agents to use
    data_reader, summarizer, report_analyzer, utility_assessor = agents
    crew_agents = [data_reader, summarizer]
    
    if pdf_path and os.path.exists(pdf_path):
        crew_agents.append(report_analyzer)
        if utility_assessor not in crew_agents:
            crew_agents.append(utility_assessor)
    
    tasks = create_tasks(assessment_data_str, pdf_path, output_prefix, agents)
    
    crew = Crew(
        agents=crew_agents,
        tasks=tasks,
        process=Process.sequential,
    )
    
    result = crew.kickoff()
    return result
