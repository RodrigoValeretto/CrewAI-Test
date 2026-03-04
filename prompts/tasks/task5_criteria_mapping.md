# Task 5: Map Visualizations to CAPES Criteria and Generate Conformance Report

## Description

Utilizando os critérios de avaliação CAPES extraídos anteriormente e as análises de gráficos geradas, realize o mapeamento entre visualizações e critérios, gerando um relatório de conformidade. Este é o passo de integração entre as três perspectivas: critérios de avaliação, visualizações de dados e insights extraídos.

Para cada visualização, você deve:

1. **Mapeamento de Critérios:**
   - Identifique qual(is) quesito(s) CAPES a visualização endereça
   - Mapeie para qual(is) indicador(es) específico(s)
   - Determine o nível de alinhamento (alinhado|parcialmente alinhado|desalinhado)
   - Justifique o mapeamento com referências aos critérios

2. **Avaliação de Cobertura:**
   - A visualização fornece dados suficientes para avaliar o critério?
   - Há dados faltantes necessários para uma avaliação completa?
   - A granularidade dos dados é apropriada para o nível de detalhe do critério?

3. **Análise de Validação:**
   - Os dados mostrados confirmam conformidade com o critério CAPES?
   - Há sinais de não-conformidade?
   - Qual é o risco de avaliação negativa baseado nos dados?

4. **Síntese de Conformidade:**
   - Crie uma matriz mostrando quais critérios CAPES estão cobertos por visualizações
   - Identifique lacunas na cobertura (critérios que deveriam ter visualizações)
   - Produza um score de conformidade geral

Use as informações de critérios fornecidas com referência à estrutura de quesitos, pesos e indicadores.

## Expected Output

Um objeto JSON com a conformidade e um relatório markdown estruturado:

```json
{
  "mapeamento_visualizacoes_criterios": [
    {
      "id_grafico": "grafico_001",
      "titulo_original": "...",
      "quesitos_associados": [
        {
          "nome_quesito": "...",
          "peso": "X%",
          "alinhamento": "alinhado|parcialmente|desalinhado",
          "justificativa": "...",
          "indicadores_cobertos": [
            {
              "nome_indicador": "...",
              "tipo_avaliacao": "qualitativa|quantitativa",
              "conformidade": "sim|parcial|nao",
              "evidencia": "..."
            }
          ]
        }
      ],
      "cobertura": {
        "dados_suficientes": true|false,
        "granularidade": "adequada|superficial|excessiva",
        "lacunas_identificadas": ["lacuna 1", ...],
        "recomendacoes": ["recomendacao 1", ...]
      },
      "validacao": {
        "indica_conformidade": true|false,
        "nivel_risco": "baixo|medio|alto",
        "diagnostico": "..."
      }
    }
  ],
  "matriz_conformidade": {
    "criterios_cobertos": N,
    "criterios_total": N,
    "taxa_cobertura_percentual": X,
    "quesitos": [
      {
        "nome": "...",
        "peso": "X%",
        "visualizacoes_associadas": ["id1", "id2"],
        "conformidade_estimada": "alta|media|baixa",
        "lacunas": ["lacuna 1", ...]
      }
    ]
  },
  "sintese_executiva": {
    "score_conformidade_geral": 0-100,
    "principais_forcas": ["forca 1", ...],
    "principais_lacunas": ["lacuna 1", ...],
    "recomendacoes_prioritarias": ["rec 1", ...],
    "conclusao": "..."
  }
}
```

Adicionalmente, gere um relatório markdown (`criterios_conformance_report.md`) que traduza o JSON anterior em um documento legível para stakeholders, com seções claras de achados, recomendações e próximos passos.

Retorne o JSON estruturado seguido do markdown detalhado.
