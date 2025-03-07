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
def load_arff(file_path):
    data = []
    attributes = []
    reading_data = False
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('%'):
                continue
                
            if '@ATTRIBUTE' in line.upper():
                attr_name = line.split()[1]
                attributes.append(attr_name)
            elif '@DATA' in line.upper():
                reading_data = True
            elif reading_data:
                data.append(line.split(','))
    
    return pd.DataFrame(data, columns=attributes)

# Carregar o dataset
df = load_arff('bank.arff')

# Converter atributos categóricos para numéricos
le = LabelEncoder()
for col in df.select_dtypes(include=['object']).columns:
    df[col] = le.fit_transform(df[col])

# Separar features e target
X = df.drop('subscribed', axis=1)
y = df['subscribed']

# Dividir em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Criar e treinar o modelo de árvore de decisão
clf = DecisionTreeClassifier(criterion='entropy', max_depth=5)
clf.fit(X_train, y_train)

# Fazer predições
y_pred = clf.predict(X_test)

# Avaliar o modelo
print("Relatório de Classificação:")
print(classification_report(y_test, y_pred))

# Matriz de Confusão com visualização melhorada
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['no', 'yes'], 
            yticklabels=['no', 'yes'])
plt.xlabel('Predito')
plt.ylabel('Real')
plt.title('Matriz de Confusão')
plt.savefig('confusion_matrix.png', dpi=300)
plt.show()

# Visualizar a árvore de decisão com mais detalhes
plt.figure(figsize=(25, 15))
tree.plot_tree(clf, feature_names=X.columns, class_names=['no', 'yes'], 
               filled=True, rounded=True, fontsize=12)
plt.title('Árvore de Decisão', fontsize=20)
plt.savefig('decision_tree.png', dpi=300, bbox_inches='tight')
plt.show()

# Importância das features com visualização
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': clf.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nImportância das Features:")
print(feature_importance)

# Visualizar importância das features
plt.figure(figsize=(12, 8))
sns.barplot(x='Importance', y='Feature', data=feature_importance.head(10))
plt.title('Top 10 Features Mais Importantes', fontsize=16)
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300)
plt.show()

# Análise adicional: curva ROC
# Obter probabilidades para a classe positiva (yes)
y_scores = clf.predict_proba(X_test)[:, 1]

# Calcular a curva ROC
fpr, tpr, thresholds = roc_curve(y_test, y_scores, pos_label=1)
roc_auc = auc(fpr, tpr)

# Plotar a curva ROC
plt.figure(figsize=(10, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'Curva ROC (área = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos')
plt.title('Curva ROC')
plt.legend(loc="lower right")
plt.savefig('roc_curve.png', dpi=300)
plt.show()
