"""APOEMA Crew implementation using CrewBase and YAML configuration."""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from crewai_files import PDFFile
import yaml


@CrewBase
class APOEMACrewBase:
    """Base crew configuration for APOEMA system using YAML configs."""

    agents_config = "config/agents"
    tasks_config = "config/tasks"

    def __init__(self, assessment_data_str: str, pdf_path: str = None, output_prefix: str = None):
        """Initialize crew with assessment data and optional PDF."""
        self.assessment_data_str = assessment_data_str
        self.pdf_path = pdf_path
        self.output_prefix = output_prefix or "apoema"
        self.pdf_file = None
        
        if pdf_path and os.path.exists(pdf_path):
            self.pdf_file = PDFFile(source=pdf_path)

    def _get_llm(self) -> LLM:
        """Create and return LLM instance."""
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        return LLM(
            model="gemini/gemini-2.5-flash",
            api_key=gemini_api_key,
            temperature=0.7,
        )

    @agent
    def data_reader(self) -> Agent:
        """Data Reader Agent."""
        config_path = Path(__file__).parent / "config" / "agents" / "data_reader.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return Agent(config=config, llm=self._get_llm())

    @agent
    def summarizer(self) -> Agent:
        """Summarizer Agent."""
        config_path = Path(__file__).parent / "config" / "agents" / "summarizer.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return Agent(config=config, llm=self._get_llm())

    @agent
    def report_analyzer(self) -> Agent:
        """Report Analyzer Agent."""
        config_path = Path(__file__).parent / "config" / "agents" / "report_analyzer.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return Agent(config=config, llm=self._get_llm())

    @agent
    def utility_assessor(self) -> Agent:
        """Utility Assessor Agent."""
        config_path = Path(__file__).parent / "config" / "agents" / "utility_assessor.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return Agent(config=config, llm=self._get_llm())

    @task
    def analyze_assessment_data(self) -> Task:
        """Task 1: Analyze assessment data."""
        config_path = Path(__file__).parent / "config" / "tasks" / "task1_analyze.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return Task(config=config, agent=self.data_reader())

    @task
    def summarize_strategic_insights(self) -> Task:
        """Task 2: Summarize strategic insights."""
        config_path = Path(__file__).parent / "config" / "tasks" / "task2_summarize.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        config["output_file"] = f"./output/{self.output_prefix}_output.md"
        return Task(config=config, agent=self.summarizer())

    @task
    def extract_plots_from_pdf(self) -> Task:
        """Task 3: Extract plots from PDF."""
        config_path = Path(__file__).parent / "config" / "tasks" / "task3_extract_plots.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        task_kwargs = {"config": config, "agent": self.report_analyzer()}
        if self.pdf_file:
            task_kwargs["input_files"] = {"pdf_report": self.pdf_file}
        return Task(**task_kwargs)

    @task
    def analyze_plots(self) -> Task:
        """Task 4: Analyze plots."""
        config_path = Path(__file__).parent / "config" / "tasks" / "task4_analyze_plots.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        task_kwargs = {"config": config, "agent": self.report_analyzer()}
        if self.pdf_file:
            task_kwargs["input_files"] = {"pdf_report": self.pdf_file}
        return Task(**task_kwargs)

    @task
    def map_to_capes_criteria(self) -> Task:
        """Task 5: Map to CAPES criteria."""
        config_path = Path(__file__).parent / "config" / "tasks" / "task5_criteria_mapping.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        config["output_file"] = f"./output/{self.output_prefix}_conformance_report.md"
        return Task(config=config, agent=self.report_analyzer())

    @task
    def assess_utility(self) -> Task:
        """Task 6: Assess utility."""
        config_path = Path(__file__).parent / "config" / "tasks" / "task6_utility_assessment.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        config["output_file"] = f"./output/{self.output_prefix}_utility_assessment.md"
        return Task(config=config, agent=self.utility_assessor())

    @crew
    def crew_with_pdf(self) -> Crew:
        """Crew with all agents and tasks (with PDF)."""
        return Crew(
            agents=[
                self.data_reader(),
                self.summarizer(),
                self.report_analyzer(),
                self.utility_assessor(),
            ],
            tasks=[
                self.analyze_assessment_data(),
                self.summarize_strategic_insights(),
                self.extract_plots_from_pdf(),
                self.analyze_plots(),
                self.map_to_capes_criteria(),
                self.assess_utility(),
            ],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def crew_without_pdf(self) -> Crew:
        """Crew without PDF-dependent tasks."""
        return Crew(
            agents=[
                self.data_reader(),
                self.summarizer(),
            ],
            tasks=[
                self.analyze_assessment_data(),
                self.summarize_strategic_insights(),
            ],
            process=Process.sequential,
            verbose=True,
        )

    def run_pipeline(self) -> str:
        """Execute the appropriate pipeline."""
        if self.pdf_file:
            return self.crew_with_pdf().kickoff(inputs={"assessment_data": self.assessment_data_str})
        else:
            return self.crew_without_pdf().kickoff(inputs={"assessment_data": self.assessment_data_str})


def run_apoema_pipeline(assessment_data_str: str, pdf_path: str = None, output_prefix: str = None) -> str:
    """Execute the APOEMA assessment analysis pipeline."""
    crew = APOEMACrewBase(assessment_data_str, pdf_path, output_prefix)
    return crew.run_pipeline()
