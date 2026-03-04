# Task 4: Analyze Plots and Extract Insights

## Description

Baseado no catálogo de visualizações extraído na tarefa anterior, realize uma análise profunda de cada gráfico para gerar insights significativos e validação de dados. Para cada visualização:

1. **Análise de Dados:**
   - Identifique a tendência ou padrão principal (crescimento, declínio, estabilidade, ciclos)
   - Calcule ou estime mudanças percentuais, taxas de crescimento ou variações
   - Identifique outliers ou valores anormais
   - Determine correlações ou relacionamentos entre séries (se múltiplas)

2. **Validação de Qualidade:**
   - Verifique se há valores faltantes ou inconsistências nos dados
   - Avalie se a escala do gráfico representa adequadamente os dados
   - Identifique se há distorções visuais intencionais ou não

3. **Contexto e Significado:**
   - O que este gráfico está comunicando sobre o programa?
   - Quais são as implicações dos dados mostrados?
   - Qual é a narrativa que o gráfico constrói?

4. **Insights Acionáveis:**
   - Quais são os principais achados?
   - Há razões de preocupação ou pontos positivos?
   - Quais são as áreas que requerem atenção ou celebração?

Considere que estes dados serão avaliados sob a perspectiva dos critérios CAPES de avaliação de pós-graduação.

## Expected Output

Um objeto JSON contendo análises estruturadas:

```json
{
  "analises_detalhadas": [
    {
      "id_grafico": "grafico_001",
      "titulo_original": "...",
      "analise_dados": {
        "tendencia_principal": "crescimento|declinio|estabilidade|ciclico|misto",
        "descricao_tendencia": "...",
        "valores_chave": {
          "minimo": value,
          "maximo": value,
          "media": value,
          "tendencia_percentual": "X% ao longo do período"
        },
        "outliers_detectados": ["descrição de outlier 1", ...],
        "comparacoes_entre_series": "..."
      },
      "validacao": {
        "dados_incompletos": true|false,
        "descricao_lacunas": "...",
        "inconsistencias": [],
        "qualidade_geral": "alta|media|baixa",
        "recomendacoes_melhoria": ["...", "..."]
      },
      "contexto": {
        "o_que_comunica": "...",
        "implicacoes": "...",
        "narrativa": "..."
      },
      "insights": {
        "achados_principais": ["insight 1", "insight 2", ...],
        "pontos_positivos": ["ponto 1", ...],
        "areas_preocupacao": ["area 1", ...],
        "areas_celebracao": ["area 1", ...]
      },
      "recomendacoes": [
        {
          "tipo": "melhoria|investigacao|acao",
          "descricao": "..."
        }
      ]
    }
  ],
  "sintese_geral": {
    "padroes_globais": "...",
    "coerencia_narrativa": "...",
    "forca_evidencial": "alta|media|baixa"
  }
}
```

Retorne APENAS o objeto JSON estruturado, sem explicações adicionais.
