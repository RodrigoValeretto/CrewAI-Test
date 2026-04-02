"""APOEMA Crew implementation using CrewBase and YAML configuration."""

import os
import json
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from crewai_files import PDFFile
from prompt_loader import load_agent_prompt, load_task_prompt
import yaml


@CrewBase
class APOEMACrewBase:
    """Base crew configuration for APOEMA system."""

    agents_config = "config/agents"
    tasks_config = "config/tasks"

    def __init__(
        self, assessment_data_str: str, pdf_path: str = None, output_prefix: str = None
    ):
        """Initialize crew with assessment data and optional PDF.

        Args:
            assessment_data_str: Assessment data as JSON string
            pdf_path: Path to optional PDF file
            output_prefix: Prefix for output files
        """
        self.assessment_data_str = assessment_data_str
        self.pdf_path = pdf_path
        self.output_prefix = output_prefix or "apoema"
        self.pdf_file = None

        if pdf_path and os.path.exists(pdf_path):
            self.pdf_file = PDFFile(source=pdf_path)

    def _load_yaml_agent_config(self, agent_name: str) -> dict:
        """Load agent configuration from YAML file."""
        config_path = Path(__file__).parent / "config" / "agents" / f"{agent_name}.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _load_yaml_task_config(self, task_name: str) -> dict:
        """Load task configuration from YAML file."""
        config_path = Path(__file__).parent / "config" / "tasks" / f"{task_name}.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

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
        """Data Reader Agent - Extracts metadata from CAPES evaluation sheets."""
        config = self._load_yaml_agent_config("data_reader")
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm=self._get_llm(),
            verbose=config.get("verbose", False),
            allow_delegation=config.get("allow_delegation", False),
        )

    @agent
    def summarizer(self) -> Agent:
        """Summarizer Agent - Synthesizes strategic insights from evaluation criteria."""
        config = self._load_yaml_agent_config("summarizer")
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm=self._get_llm(),
            verbose=config.get("verbose", False),
            allow_delegation=config.get("allow_delegation", False),
        )

    @agent
    def report_analyzer(self) -> Agent:
        """Report Analyzer Agent - Analyzes visualizations and CAPES compliance."""
        config = self._load_yaml_agent_config("report_analyzer")
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm=self._get_llm(),
            verbose=config.get("verbose", False),
            allow_delegation=config.get("allow_delegation", False),
        )

    @agent
    def utility_assessor(self) -> Agent:
        """Utility Assessor Agent - Evaluates visualization utility and assertiveness."""
        config = self._load_yaml_agent_config("utility_assessor")
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm=self._get_llm(),
            verbose=config.get("verbose", False),
            allow_delegation=config.get("allow_delegation", False),
        )

    @task
    def analyze_assessment_data(self) -> Task:
        """Task 1: Analyze assessment data from CAPES evaluation sheet."""
        config = self._load_yaml_task_config("task1_analyze")
        description = config["description"]
        if "{ASSESSMENT_DATA}" in description:
            description = description.replace(
                "{ASSESSMENT_DATA}", self.assessment_data_str
            )

        return Task(
            description=description,
            agent=self.data_reader(),
            expected_output=config["expected_output"],
        )

    @task
    def summarize_strategic_insights(self) -> Task:
        """Task 2: Summarize strategic insights from evaluation criteria."""
        config = self._load_yaml_task_config("task2_summarize")

        return Task(
            description=config["description"],
            agent=self.summarizer(),
            expected_output=config["expected_output"],
            markdown=config.get("markdown", False),
            output_file=(
                f"./output/{self.output_prefix}_output.md"
                if config.get("markdown")
                else None
            ),
        )

    @task
    def extract_plots_from_pdf(self) -> Task:
        """Task 3: Extract and catalog visualizations from PDF report."""
        config = self._load_yaml_task_config("task3_extract_plots")

        task_kwargs = {
            "description": config["description"],
            "agent": self.report_analyzer(),
            "expected_output": config["expected_output"],
        }

        if self.pdf_file:
            task_kwargs["input_files"] = {"pdf_report": self.pdf_file}

        return Task(**task_kwargs)

    @task
    def analyze_plots(self) -> Task:
        """Task 4: Analyze plots and extract insights."""
        config = self._load_yaml_task_config("task4_analyze_plots")

        task_kwargs = {
            "description": config["description"],
            "agent": self.report_analyzer(),
            "expected_output": config["expected_output"],
        }

        if self.pdf_file:
            task_kwargs["input_files"] = {"pdf_report": self.pdf_file}

        return Task(**task_kwargs)

    @task
    def map_to_capes_criteria(self) -> Task:
        """Task 5: Map visualizations to CAPES criteria."""
        config = self._load_yaml_task_config("task5_criteria_mapping")

        return Task(
            description=config["description"],
            agent=self.report_analyzer(),
            expected_output=config["expected_output"],
            markdown=config.get("markdown", False),
            output_file=(
                f"./output/{self.output_prefix}_conformance_report.md"
                if config.get("markdown")
                else None
            ),
        )

    @task
    def assess_utility(self) -> Task:
        """Task 6: Assess graphics utility and assertiveness."""
        config = self._load_yaml_task_config("task6_utility_assessment")

        return Task(
            description=config["description"],
            agent=self.utility_assessor(),
            expected_output=config["expected_output"],
            markdown=config.get("markdown", False),
            output_file=(
                f"./output/{self.output_prefix}_utility_assessment.md"
                if config.get("markdown")
                else None
            ),
        )

    @crew
    def crew_with_pdf(self) -> Crew:
        """Crew with all agents and tasks (including PDF analysis)."""
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
        """Crew without PDF-dependent agents and tasks."""
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
        """Execute the appropriate pipeline based on PDF availability."""
        if self.pdf_file:
            result = self.crew_with_pdf().kickoff()
        else:
            result = self.crew_without_pdf().kickoff()

        return result


def run_apoema_pipeline(
    assessment_data_str: str, pdf_path: str = None, output_prefix: str = None
) -> str:
    """Execute the APOEMA assessment analysis pipeline.

    Args:
        assessment_data_str: Assessment data as JSON string
        pdf_path: Path to optional PDF file
        output_prefix: Prefix for output files

    Returns:
        Result from pipeline execution
    """
    crew = APOEMACrewBase(assessment_data_str, pdf_path, output_prefix)
    return crew.run_pipeline()
