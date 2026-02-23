import os
from crewai import Agent, Task, Crew, Process, LLM

# 1. Configuration: Get your free API key from Google AI Studio
# Set it in your environment or directly here for the prototype
gemini_api_key = "AIzaSyDGfBXUsHtPJ4YAKxHe_h5j3HiKRATVOUc"


# Define the model (Gemini 2.0 Flash is fast and free-tier friendly)
# agent_llm = LLM(
#     model="ollama/llama3.2",
#     temperature=0.7,
# )

agent_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=gemini_api_key,
    temperature=0.7,
)

# 2. Define your Agents
researcher = Agent(
    role="Academic Researcher",
    goal="Extract key methodology details from provided text",
    backstory="You are a meticulous post-grad assistant specialized in technical analysis.",
    llm=agent_llm,
    verbose=True,
)

writer = Agent(
    role="Technical Writer",
    goal="Summarize findings into a LaTeX-ready format",
    backstory="You turn complex research into clear, concise academic prose.",
    llm=agent_llm,
    verbose=True,
)

# 3. Define Tasks
task1 = Task(
    description="Analyze the attached abstract for core variables.",
    agent=researcher,
    expected_output="A list of 5 variables.",
)
task2 = Task(
    description="Write a summary based on the researcher's findings.",
    agent=writer,
    expected_output="A 200-word summary.",
)

# 4. Kickoff the Crew
crew = Crew(
    agents=[researcher, writer], tasks=[task1, task2], process=Process.sequential
)

result = crew.kickoff()
print(result)
