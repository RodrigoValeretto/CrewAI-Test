"""APOEMA Crew implementation using CrewBase and YAML configuration."""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from crewai_files import PDFFile, TextFile
from datetime import datetime
import yaml


@CrewBase
class APOEMACrewBase:
    """Base crew configuration for APOEMA system using YAML configs."""

    def __init__(
        self, assessment_path: str, pdf_path: str = None, output_prefix: str = None
    ):
        """Initialize crew with assessment data and optional PDF."""
        self.assessment_file = TextFile(source=assessment_path)
        self.pdf_file = None
        self.output_prefix = output_prefix or datetime.now().strftime("%Y%m%d%H%M%S")

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
        """Load agent config from consolidated YAML."""
        return self.agents_config[agent_name]

    def _load_task_config(self, task_name: str) -> dict:
        """Load task config from consolidated YAML."""
        return self.tasks_config[task_name]

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
        return Agent(
            config=self._load_agent_config("report_analyzer"), llm=self._get_llm()
        )

    @agent
    def utility_assessor(self) -> Agent:
        """Utility Assessor Agent."""
        return Agent(
            config=self._load_agent_config("utility_assessor"), llm=self._get_llm()
        )

    @task
    def analyze_assessment_data(self) -> Task:
        """Task 1: Analyze assessment data."""
        return Task(config=self._load_task_config("task1_analyze"))

    @task
    def summarize_strategic_insights(self) -> Task:
        """Task 2: Summarize strategic insights."""
        return Task(config=self._load_task_config("task2_summarize"))

    @task
    def extract_plots_from_pdf(self) -> Task:
        """Task 3: Extract plots from PDF."""
        return Task(config=self._load_task_config("task3_extract_plots"))

    @task
    def analyze_plots(self) -> Task:
        """Task 4: Analyze plots."""
        return Task(config=self._load_task_config("task4_analyze_plots"))

    @task
    def map_to_capes_criteria(self) -> Task:
        """Task 5: Map to CAPES criteria."""
        return Task(config=self._load_task_config("task5_criteria_mapping"))

    @task
    def assess_utility(self) -> Task:
        """Task 6: Assess utility."""
        return Task(config=self._load_task_config("task6_utility_assessment"))

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
        input_files = {
            "pdf_report": self.pdf_file,
            "assessment_data": self.assessment_file,
        }

        inputs = {"prefix": self.output_prefix}

        crew = self.crew_with_pdf() if self.pdf_file else self.crew_without_pdf()
        return crew.kickoff(inputs=inputs, input_files=input_files)


def run_apoema_pipeline(
    assessment_path: str, pdf_path: str = None, output_prefix: str = None
) -> str:
    """Execute the APOEMA assessment analysis pipeline."""
    crew = APOEMACrewBase(assessment_path, pdf_path, output_prefix)
    return crew.run_pipeline()
