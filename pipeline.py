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

    def _load_agent_config(self, agent_name: str) -> dict:
        """Load agent config from YAML."""
        config_path = Path(__file__).parent / "config" / "agents" / f"{agent_name}.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    def _load_task_config(self, task_name: str) -> dict:
        """Load task config from YAML."""
        config_path = Path(__file__).parent / "config" / "tasks" / f"{task_name}.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    @agent
    def data_reader(self) -> Agent:
        """Data Reader Agent."""
        return Agent(config=self._load_agent_config("data_reader"), llm=self._get_llm())

    @agent
    def summarizer(self) -> Agent:
        """Summarizer Agent."""
        return Agent(config=self._load_agent_config("summarizer"), llm=self._get_llm())

    @agent
    def report_analyzer(self) -> Agent:
        """Report Analyzer Agent."""
        return Agent(config=self._load_agent_config("report_analyzer"), llm=self._get_llm())

    @agent
    def utility_assessor(self) -> Agent:
        """Utility Assessor Agent."""
        return Agent(config=self._load_agent_config("utility_assessor"), llm=self._get_llm())

    @task
    def analyze_assessment_data(self) -> Task:
        """Task 1: Analyze assessment data."""
        return Task(config=self._load_task_config("task1_analyze"), agent=self.data_reader())

    @task
    def summarize_strategic_insights(self) -> Task:
        """Task 2: Summarize strategic insights."""
        return Task(config=self._load_task_config("task2_summarize"), agent=self.summarizer())

    @task
    def extract_plots_from_pdf(self) -> Task:
        """Task 3: Extract plots from PDF."""
        config = self._load_task_config("task3_extract_plots")
        task_kwargs = {"config": config, "agent": self.report_analyzer()}
        if self.pdf_file:
            task_kwargs["input_files"] = {"pdf_report": self.pdf_file}
        return Task(**task_kwargs)

    @task
    def analyze_plots(self) -> Task:
        """Task 4: Analyze plots."""
        config = self._load_task_config("task4_analyze_plots")
        task_kwargs = {"config": config, "agent": self.report_analyzer()}
        if self.pdf_file:
            task_kwargs["input_files"] = {"pdf_report": self.pdf_file}
        return Task(**task_kwargs)

    @task
    def map_to_capes_criteria(self) -> Task:
        """Task 5: Map to CAPES criteria."""
        return Task(config=self._load_task_config("task5_criteria_mapping"), agent=self.report_analyzer())

    @task
    def assess_utility(self) -> Task:
        """Task 6: Assess utility."""
        return Task(config=self._load_task_config("task6_utility_assessment"), agent=self.utility_assessor())

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
        inputs = {
            "assessment_data": self.assessment_data_str,
            "prefix": self.output_prefix,
        }
        
        if self.pdf_file:
            return self.crew_with_pdf().kickoff(inputs=inputs)
        else:
            return self.crew_without_pdf().kickoff(inputs=inputs)


def run_apoema_pipeline(assessment_data_str: str, pdf_path: str = None, output_prefix: str = None) -> str:
    """Execute the APOEMA assessment analysis pipeline."""
    crew = APOEMACrewBase(assessment_data_str, pdf_path, output_prefix)
    return crew.run_pipeline()
