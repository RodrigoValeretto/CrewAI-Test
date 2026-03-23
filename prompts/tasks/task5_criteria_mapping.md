# Task 5: Map Visualizations to CAPES Criteria and Generate Conformance Report

## Description

1. **Integração de Perspectivas:** Utilize os critérios extraídos da Ficha de Avaliação (Data Reader) e as análises das visualizações (Report Analyzer) para realizar o cruzamento final de conformidade.
2. **Mapeamento de Critérios:** Para cada gráfico do APOEMA, identifique qual Quesito e Indicador específico da CAPES ele endereça. Determine se o alinhamento é total, parcial ou se há um desalinhamento (ex: o gráfico mostra dados que a ficha não considera mais relevantes).
3. **Auditoria de Cobertura e Suficiência:** Avalie se as visualizações presentes são suficientes para que um avaliador atribua uma nota ao programa. Identifique "zonas de sombra" (critérios de alto peso na ficha que não possuem representação visual no APOEMA).
4. **Cálculo de Risco:** Baseado na tendência dos dados (Task 4), determine o risco de uma avaliação negativa (Baixo, Médio, Alto) para cada quesito da ficha.
5. **Síntese de Conformidade:** Gere um diagnóstico que aponte a taxa de cobertura do dashboard em relação às exigências da Grande Área (ex: Computação, Sociologia).
6. **Redação do Relatório Final:** Traduza toda a inteligência técnica processada em um relatório executivo formatado em Markdown, focado na tomada de decisão do Coordenador do PPG.

## Expected Output

Um relatório detalhado em Markdown (`criterios_conformance_report.md`), estruturado profissionalmente, contendo:

### 📊 Diagnóstico de Conformidade CAPES

- **Resumo Executivo:** Análise da maturidade dos dados do programa frente à ficha de avaliação da área.
- **Score Geral de Aderência:** Um percentual (0-100%) que represente o quanto as visualizações atuais cobrem as necessidades da ficha.

### 🔍 Análise por Quesito de Avaliação

- **[Nome do Quesito - Peso X%]**:
  - **Visualizações Associadas:** IDs dos gráficos que sustentam este quesito.
  - **Status de Evidência:** (Suficiente / Insuficiente / Ausente).
  - **Análise de Risco:** Diagnóstico se os dados atuais sugerem conformidade ou risco de nota baixa.

### ⚠️ Lacunas de Evidência (Gap Analysis)

- Lista de critérios da ficha de avaliação que **não** possuem representação visual no APOEMA, com recomendação do que deveria ser plotado.

### 📈 Matriz de Relevância vs. Utilidade

- Uma tabela cruzando os critérios da ficha com os gráficos existentes, avaliando a utilidade de cada um para a área específica (ex: justificando por que um gráfico de 'Produção Técnica' é mais útil para as Engenharias que para as Humanidades).

### 🚀 Recomendações Estratégicas

- Lista de ações prioritárias para melhorar a defesa do programa perante a CAPES.

**Instrução de Formato:** Retorne APENAS o relatório em Markdown detalhado. Não inclua blocos de código JSON ou explicações fora do documento de auditoria.
