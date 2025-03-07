## Descrição do Dataset

O arquivo `estudantes.arff` contém dados fictícios sobre estudantes e seus hábitos de estudo. Os atributos incluem:

- **idade**: Idade do estudante (numérico)
- **horas_estudo_semana**: Quantidade de horas dedicadas ao estudo por semana (numérico)
- **frequencia_aulas**: Frequência de participação nas aulas (baixa, média, alta)
- **uso_biblioteca**: Se o estudante utiliza a biblioteca (sim, não)
- **participacao_grupos_estudo**: Se o estudante participa de grupos de estudo (sim, não)
- **tempo_sono_diario**: Média de horas de sono por dia (numérico)
- **uso_internet_estudo**: Nível de uso da internet para estudos (baixo, médio, alto)
- **trabalha**: Se o estudante trabalha além de estudar (sim, não)
- **atividade_fisica_semana**: Horas de atividade física por semana (numérico)
- **aprovado**: Se o estudante foi aprovado ou não (sim, não) - variável alvo

1. **Carregamento e Pré-processamento dos Dados**:
- Carrega o arquivo ARFF
- Converte atributos categóricos para numéricos
- Converte colunas numéricas para o tipo float

2. **Modelagem com Árvore de Decisão**:
- Divide os dados em conjuntos de treino e teste
- Cria e treina um modelo de árvore de decisão
- Realiza predições

3. **Avaliação do Modelo**:
- Gera relatório de classificação
- Cria matriz de confusão
- Visualiza a árvore de decisão
- Analisa a importância das features
- Gera curva ROC

4. **Análises Adicionais**:
- Distribuição das variáveis mais importantes
- Matriz de correlação entre as variáveis

## Resultados

Os resultados são salvos em arquivos PNG:
- `matriz_confusao_estudantes.png`: Matriz de confusão do modelo
- `arvore_decisao_estudantes.png`: Visualização da árvore de decisão
- `importancia_features_estudantes.png`: Gráfico de importância das features
- `curva_roc_estudantes.png`: Curva ROC do modelo
- `distribuicao_top_features.png`: Distribuição das variáveis mais importantes
- `matriz_correlacao.png`: Matriz de correlação entre as variáveis

