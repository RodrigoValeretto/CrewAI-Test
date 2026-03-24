# Task 3: Extract and Catalog Visualizations from PDF Report

## Description

1. **Processamento de Visão e Texto:** Analise o arquivo PDF `{REPORT_PDF}` gerado pelo sistema APOEMA. Sua missão é realizar uma engenharia reversa das visualizações de dados presentes (gráficos, tabelas e plots).
2. **Catalogação Técnica:** Para cada elemento visual detectado, identifique obrigatoriamente:
   - **ID e Localização:** Sequência numérica e página do documento.
   - **Tipologia e Títulos:** Classificação (barras, linhas, dispersão, pizza, tabela) e transcrição fiel de títulos/subtítulos.
   - **Semântica dos Eixos e Legendas:** Extração de rótulos do Eixo X (categorias/tempo) e Eixo Y (métricas/escalas), além de cores e séries de dados.
   - **Métricas e Valores:** Identificação dos valores brutos ou aproximados representados nas séries e o período cronológico de referência.
3. **Auditoria de Qualidade Visual:** Avalie a legibilidade, a presença de eixos nomeados e se há inconsistências (ex: legenda faltando ou escala distorcida).
4. **Formatação Estrita:** Consolide todos os achados em um objeto JSON seguindo o esquema fornecido, garantindo que os dados estejam prontos para processamento programático por outros agentes.

## Expected Output

Um objeto JSON puro, sem blocos de texto explicativo antes ou depois, contendo um array de visualizações com a seguinte estrutura:

```json
{
  "visualizacoes": [
    {
      "id": "string",
      "pagina": "number",
      "titulo": "string",
      "subtitulo": "string",
      "tipo": "bar_chart|line_chart|scatter|table|heatmap|map|other",
      "eixo_x": {
        "rotulo": "string",
        "unidade": "string",
        "categorias": ["string"]
      },
      "eixo_y": {
        "rotulo": "string",
        "unidade": "string",
        "range": ["number", "number"]
      },
      "series_dados": [
        {
          "nome": "string",
          "valores": ["number/string"],
          "cor_aproximada": "hex_code"
        }
      ],
      "periodo_referencia": "string",
      "legendas": ["string"],
      "anotacoes": "string",
      "observacoes_qualidade": "string",
      "dados_extraiveis": "boolean",
      "completude_visual": "alta|media|baixa"
    }
  ],
  "resumo_extracao": {
    "total_visualizacoes": "number",
    "tipos_presentes": ["string"],
    "status_processamento": "sucesso|parcial"
  }
}
