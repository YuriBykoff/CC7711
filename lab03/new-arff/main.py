import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
import seaborn as sns
from sklearn.metrics import roc_curve, auc

# Função para carregar o arquivo ARFF
def carregar_arff(caminho_arquivo):
    dados = []
    atributos = []
    lendo_dados = False
    
    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or linha.startswith('%'):
                continue
                
            if '@ATTRIBUTE' in linha.upper():
                nome_atributo = linha.split()[1]
                atributos.append(nome_atributo)
            elif '@DATA' in linha.upper():
                lendo_dados = True
            elif lendo_dados:
                dados.append(linha.split(','))
    
    return pd.DataFrame(dados, columns=atributos)

# Carregar o dataset
df = carregar_arff('estudantes.arff')

# Converter atributos categóricos para numéricos
codificador = LabelEncoder()
for coluna in df.select_dtypes(include=['object']).columns:
    df[coluna] = codificador.fit_transform(df[coluna])

# Converter colunas numéricas para o tipo float
colunas_numericas = ['idade', 'horas_estudo_semana', 'tempo_sono_diario', 'atividade_fisica_semana']
for coluna in colunas_numericas:
    df[coluna] = df[coluna].astype(float)

# Separar features e target
X = df.drop('aprovado', axis=1)
y = df['aprovado']

# Dividir em conjuntos de treino e teste
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, random_state=42)

# Criar e treinar o modelo de árvore de decisão
classificador = DecisionTreeClassifier(criterion='entropy', max_depth=5)
classificador.fit(X_treino, y_treino)

# Fazer predições
y_predicao = classificador.predict(X_teste)

# Avaliar o modelo
print("Relatório de Classificação:")
print(classification_report(y_teste, y_predicao))

# Matriz de Confusão com visualização melhorada
matriz_confusao = confusion_matrix(y_teste, y_predicao)
plt.figure(figsize=(10, 8))
sns.heatmap(matriz_confusao, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Reprovado', 'Aprovado'], 
            yticklabels=['Reprovado', 'Aprovado'])
plt.xlabel('Predito')
plt.ylabel('Real')
plt.title('Matriz de Confusão')
plt.savefig('matriz_confusao_estudantes.png', dpi=300)
plt.show()

# Visualizar a árvore de decisão com mais detalhes
plt.figure(figsize=(25, 15))
nomes_features = X.columns
nomes_classes = ['Reprovado', 'Aprovado']
tree.plot_tree(classificador, feature_names=nomes_features, class_names=nomes_classes, 
               filled=True, rounded=True, fontsize=12)
plt.title('Árvore de Decisão - Desempenho de Estudantes', fontsize=20)
plt.savefig('arvore_decisao_estudantes.png', dpi=300, bbox_inches='tight')
plt.show()

# Importância das features com visualização
importancia_features = pd.DataFrame({
    'Feature': X.columns,
    'Importancia': classificador.feature_importances_
}).sort_values('Importancia', ascending=False)

print("\nImportância das Features:")
print(importancia_features)

# Visualizar importância das features
plt.figure(figsize=(12, 8))
sns.barplot(x='Importancia', y='Feature', data=importancia_features)
plt.title('Importância das Features - Desempenho de Estudantes', fontsize=16)
plt.tight_layout()
plt.savefig('importancia_features_estudantes.png', dpi=300)
plt.show()

# Análise adicional: curva ROC
# Obter probabilidades para a classe positiva (aprovado)
pontuacoes_y = classificador.predict_proba(X_teste)[:, 1]

# Calcular a curva ROC
taxa_falsos_positivos, taxa_verdadeiros_positivos, limiares = roc_curve(y_teste, pontuacoes_y, pos_label=1)
area_roc = auc(taxa_falsos_positivos, taxa_verdadeiros_positivos)

# Plotar a curva ROC
plt.figure(figsize=(10, 8))
plt.plot(taxa_falsos_positivos, taxa_verdadeiros_positivos, color='darkorange', lw=2, label=f'Curva ROC (área = {area_roc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos')
plt.title('Curva ROC - Desempenho de Estudantes')
plt.legend(loc="lower right")
plt.savefig('curva_roc_estudantes.png', dpi=300)
plt.show()

# Análise adicional: Distribuição das variáveis mais importantes
top_features = importancia_features.head(3)['Feature'].values

plt.figure(figsize=(15, 10))
for i, feature in enumerate(top_features):
    plt.subplot(1, 3, i+1)
    if feature in colunas_numericas:
        sns.histplot(data=df, x=feature, hue='aprovado', bins=10, kde=True)
    else:
        sns.countplot(data=df, x=feature, hue='aprovado')
    plt.title(f'Distribuição de {feature}')
    plt.tight_layout()
plt.savefig('distribuicao_top_features.png', dpi=300)
plt.show()

# Análise de correlação entre as variáveis
plt.figure(figsize=(12, 10))
matriz_correlacao = df.corr()
sns.heatmap(matriz_correlacao, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Matriz de Correlação entre Variáveis')
plt.tight_layout()
plt.savefig('matriz_correlacao.png', dpi=300)
plt.show()

print("\nAnálise concluída! Os resultados foram salvos em arquivos PNG.") 