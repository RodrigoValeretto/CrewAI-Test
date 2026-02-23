import os
import json
from crewai import Agent, Task, Crew, Process, LLM
from datetime import datetime

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


def write_output(value):
    """Load assessment data from JSON file."""
    now_str = datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        with open(f"output_{now_str}.md", "w") as f:
            return f.write(value)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None
    except Exception as e:
        print("Error writing value to output file:", e)
        print("\n\nValue:\n", value)


assessment_data = load_assessment_data()

if assessment_data is None:
    print("Erro: Não foi possível carregar o arquivo assessment_data.json")
    exit(1)

# Convert assessment data to string for agent processing
assessment_data_str = json.dumps(assessment_data, ensure_ascii=False, indent=2)

# 3. Define your Agents
data_reader = Agent(
    role="Leitor de Dados de Avaliação",
    goal="Ler e interpretar dados de avaliação pós-graduação em formato JSON, extraindo informações relevantes do documento.",
    backstory="Você é um assistente especializado em análise de dados de avaliação acadêmica de pós-graduação. "
    "Trabalha com dados em português-brasileiro e compreende profundamente os critérios de avaliação. "
    "Sua tarefa é extrair e interpretar informações de arquivos de avaliação com precisão.",
    llm=agent_llm,
    verbose=True,
)

summarizer = Agent(
    role="Resumidor de Pontos Críticos",
    goal="Resumir os pontos-chave de atenção na avaliação de forma clara e estruturada em português-brasileiro e em markdown na estrutura correta.",
    backstory="Você é um especialista em síntese de informações acadêmicas. "
    "Consegue identificar e comunicar os pontos mais importantes que necessitam atenção durante a avaliação. "
    "Seus resumos são claros, bem estruturados e úteis para tomadas de decisão.",
    llm=agent_llm,
    verbose=True,
)

# 4. Define Tasks
task1 = Task(
    description=f"""Analise o seguinte arquivo JSON de avaliação de pós-graduação e extraia as informações principais:

{assessment_data_str}

Por favor, identifique e descreva:
1. Estrutura geral do documento
2. Principais categorias ou critérios de avaliação
3. Períodos de avaliação mencionados
4. Qualquer outra informação relevante encontrada no documento

Responda em português-brasileiro.""",
    agent=data_reader,
    expected_output="Uma análise detalhada das informações contidas no arquivo de avaliação.",
)

task2 = Task(
    description="Com base na análise anterior do arquivo de avaliação, resuma os pontos-chave que devem receber atenção especial durante a avaliação. "
    "Forneça um parágrafo resumido seguido de uma lista em tópicos dos pontos críticos. Responda em português-brasileiro e em markdown.",
    agent=summarizer,
    expected_output="Um resumo em parágrafo e uma lista de tópicos com os pontos críticos da avaliação em uma estrutura de markdown.",
)

# 5. Kickoff the Crew
crew = Crew(
    agents=[data_reader, summarizer], tasks=[task1, task2], process=Process.sequential
)

result = crew.kickoff()
write_output(str(result))
