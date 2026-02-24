import os
import json
from crewai import Agent, Task, Crew, Process, LLM
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


assessment_data = load_assessment_data()

if assessment_data is None:
    print("Erro: Não foi possível carregar o arquivo assessment_data.json")
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

# 5. Kickoff the Crew
crew = Crew(
    agents=[data_reader, summarizer],
    tasks=[task1, task2],
    process=Process.sequential,
)

result = crew.kickoff()
