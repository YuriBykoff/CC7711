import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ----- PARTE 1: SISTEMA BÁSICO COM FUNÇÃO TRIANGULAR -----
print("=== CONSTRUINDO SISTEMA BÁSICO DE AVALIAÇÃO DE OBESIDADE ===")

# Definindo as variáveis de entrada (Antecedentes)
imc = ctrl.Antecedent(np.arange(15, 41, 1), 'imc')
cintura = ctrl.Antecedent(np.arange(60, 131, 1), 'cintura')

# Definindo a variável de saída (Consequente)
obesidade = ctrl.Consequent(np.arange(0, 101, 1), 'obesidade')

# Definindo os conjuntos fuzzy para IMC usando função triangular
imc['abaixo_do_peso'] = fuzz.trimf(imc.universe, [15, 15, 18.5])
imc['normal'] = fuzz.trimf(imc.universe, [17, 21.75, 25])
imc['sobrepeso'] = fuzz.trimf(imc.universe, [24, 27.5, 30])
imc['obesidade'] = fuzz.trimf(imc.universe, [29, 35, 40])

# Definindo os conjuntos fuzzy para Circunferência da Cintura
cintura['baixo_risco'] = fuzz.trimf(cintura.universe, [60, 60, 80])
cintura['risco_moderado'] = fuzz.trimf(cintura.universe, [75, 90, 100])
cintura['alto_risco'] = fuzz.trimf(cintura.universe, [95, 110, 130])

# Definindo os conjuntos fuzzy para Obesidade
obesidade['saudável'] = fuzz.trimf(obesidade.universe, [0, 0, 30])
obesidade['moderada'] = fuzz.trimf(obesidade.universe, [20, 50, 70])
obesidade['severa'] = fuzz.trimf(obesidade.universe, [60, 80, 90])
obesidade['mórbida'] = fuzz.trimf(obesidade.universe, [85, 100, 100])

# Visualizando os conjuntos fuzzy
imc.view()
plt.title('Conjuntos Fuzzy para IMC (Triangular)')
plt.savefig('imc_triangular.png')

cintura.view()
plt.title('Conjuntos Fuzzy para Circunferência da Cintura (Triangular)')
plt.savefig('cintura_triangular.png')

obesidade.view()
plt.title('Conjuntos Fuzzy para Nível de Obesidade (Triangular)')
plt.savefig('obesidade_triangular.png')

# Definindo as regras
regra1 = ctrl.Rule(imc['abaixo_do_peso'] & cintura['baixo_risco'], obesidade['saudável'])
regra2 = ctrl.Rule(imc['normal'] & cintura['baixo_risco'], obesidade['saudável'])
regra3 = ctrl.Rule(imc['normal'] & cintura['risco_moderado'], obesidade['moderada'])
regra4 = ctrl.Rule(imc['sobrepeso'] & cintura['baixo_risco'], obesidade['moderada'])
regra5 = ctrl.Rule(imc['sobrepeso'] & cintura['risco_moderado'], obesidade['moderada'])
regra6 = ctrl.Rule(imc['sobrepeso'] & cintura['alto_risco'], obesidade['severa'])
regra7 = ctrl.Rule(imc['obesidade'] & cintura['risco_moderado'], obesidade['severa'])
regra8 = ctrl.Rule(imc['obesidade'] & cintura['alto_risco'], obesidade['mórbida'])

print("Regras definidas para o sistema básico:")
print("1. Se IMC é abaixo do peso E cintura é baixo risco, então obesidade é saudável")
print("2. Se IMC é normal E cintura é baixo risco, então obesidade é saudável")
print("3. Se IMC é normal E cintura é risco moderado, então obesidade é moderada")
print("4. Se IMC é sobrepeso E cintura é baixo risco, então obesidade é moderada")
print("5. Se IMC é sobrepeso E cintura é risco moderado, então obesidade é moderada")
print("6. Se IMC é sobrepeso E cintura é alto risco, então obesidade é severa")
print("7. Se IMC é obesidade E cintura é risco moderado, então obesidade é severa")
print("8. Se IMC é obesidade E cintura é alto risco, então obesidade é mórbida")

# Sistema de controle
sistema_ctrl = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8])
sistema = ctrl.ControlSystemSimulation(sistema_ctrl)

# Função para testar o sistema
def testar_sistema(imc_valor, cintura_valor):
    sistema.input['imc'] = imc_valor
    sistema.input['cintura'] = cintura_valor
    try:
        sistema.compute()
        return sistema.output['obesidade']
    except KeyError:
        # Tratando casos extremos
        if imc_valor >= 35 and cintura_valor >= 110:
            return 100.0  # Obesidade mórbida para valores extremos altos
        elif imc_valor <= 16 and cintura_valor <= 65:
            return 0.0    # Saudável para valores extremos baixos
        else:
            return 50.0   # Valor intermediário para outros casos indefinidos

# ----- PARTE 2: TESTES COM DIFERENTES FUNÇÕES DE PERTINÊNCIA -----
print("\n=== TESTANDO DIFERENTES FUNÇÕES DE PERTINÊNCIA ===")

# Salvando a configuração triangular original
imc_trimf = imc.terms.copy()
cintura_trimf = cintura.terms.copy()
obesidade_trimf = obesidade.terms.copy()

# FUNÇÃO GAUSSIANA
# Redefina os conjuntos fuzzy usando gaussmf
imc.terms.clear()
cintura.terms.clear()
obesidade.terms.clear()

imc['abaixo_do_peso'] = fuzz.gaussmf(imc.universe, 15, 2)
imc['normal'] = fuzz.gaussmf(imc.universe, 22, 2)
imc['sobrepeso'] = fuzz.gaussmf(imc.universe, 27, 2)
imc['obesidade'] = fuzz.gaussmf(imc.universe, 35, 3)

cintura['baixo_risco'] = fuzz.gaussmf(cintura.universe, 70, 5)
cintura['risco_moderado'] = fuzz.gaussmf(cintura.universe, 90, 5)
cintura['alto_risco'] = fuzz.gaussmf(cintura.universe, 110, 10)

obesidade['saudável'] = fuzz.gaussmf(obesidade.universe, 10, 10)
obesidade['moderada'] = fuzz.gaussmf(obesidade.universe, 40, 10)
obesidade['severa'] = fuzz.gaussmf(obesidade.universe, 70, 10)
obesidade['mórbida'] = fuzz.gaussmf(obesidade.universe, 95, 5)

# Visualizando os conjuntos fuzzy gaussianos
imc.view()
plt.title('Conjuntos Fuzzy para IMC (Gaussiano)')
plt.savefig('imc_gaussiano.png')

cintura.view()
plt.title('Conjuntos Fuzzy para Circunferência da Cintura (Gaussiano)')
plt.savefig('cintura_gaussiano.png')

obesidade.view()
plt.title('Conjuntos Fuzzy para Nível de Obesidade (Gaussiano)')
plt.savefig('obesidade_gaussiano.png')

# Salvando a configuração gaussiana
imc_gaussmf = imc.terms.copy()
cintura_gaussmf = cintura.terms.copy()
obesidade_gaussmf = obesidade.terms.copy()

# FUNÇÃO TRAPEZOIDAL
# Redefina os conjuntos fuzzy usando trapmf
imc.terms.clear()
cintura.terms.clear()
obesidade.terms.clear()

imc['abaixo_do_peso'] = fuzz.trapmf(imc.universe, [15, 15, 17, 18.5])
imc['normal'] = fuzz.trapmf(imc.universe, [17, 19, 23, 25])
imc['sobrepeso'] = fuzz.trapmf(imc.universe, [24, 26, 28, 30])
imc['obesidade'] = fuzz.trapmf(imc.universe, [29, 32, 40, 40])

cintura['baixo_risco'] = fuzz.trapmf(cintura.universe, [60, 60, 70, 80])
cintura['risco_moderado'] = fuzz.trapmf(cintura.universe, [75, 85, 95, 100])
cintura['alto_risco'] = fuzz.trapmf(cintura.universe, [95, 105, 130, 130])

obesidade['saudável'] = fuzz.trapmf(obesidade.universe, [0, 0, 20, 30])
obesidade['moderada'] = fuzz.trapmf(obesidade.universe, [20, 40, 55, 70])
obesidade['severa'] = fuzz.trapmf(obesidade.universe, [60, 70, 85, 95])
obesidade['mórbida'] = fuzz.trapmf(obesidade.universe, [90, 95, 100, 100])

# Visualizando os conjuntos fuzzy trapezoidais
imc.view()
plt.title('Conjuntos Fuzzy para IMC (Trapezoidal)')
plt.savefig('imc_trapezoidal.png')

cintura.view()
plt.title('Conjuntos Fuzzy para Circunferência da Cintura (Trapezoidal)')
plt.savefig('cintura_trapezoidal.png')

obesidade.view()
plt.title('Conjuntos Fuzzy para Nível de Obesidade (Trapezoidal)')
plt.savefig('obesidade_trapezoidal.png')

# Salvando a configuração trapezoidal
imc_trapmf = imc.terms.copy()
cintura_trapmf = cintura.terms.copy()
obesidade_trapmf = obesidade.terms.copy()

# ----- PARTE 3: ANÁLISE DE SENSIBILIDADE -----
print("\n=== ANÁLISE DE SENSIBILIDADE ===")

# Restaurando a configuração triangular para fazer os testes
imc.terms = imc_trimf
cintura.terms = cintura_trimf
obesidade.terms = obesidade_trimf

# Casos de teste
casos_teste = [
    # IMC, Cintura
    (17, 70),    # Abaixo do peso, cintura baixa
    (22, 75),    # Normal, cintura baixa
    (22, 90),    # Normal, cintura moderada
    (27, 75),    # Sobrepeso, cintura baixa
    (27, 90),    # Sobrepeso, cintura moderada
    (27, 105),   # Sobrepeso, cintura alta
    (32, 90),    # Obesidade, cintura moderada
    (32, 105),   # Obesidade, cintura alta
    # Valores limites
    (15, 60),    # IMC mínimo, cintura mínima
    (40, 130)    # IMC máximo, cintura máxima
]

print("Testando o sistema com função triangular:")
for imc_v, cintura_v in casos_teste:
    resultado = testar_sistema(imc_v, cintura_v)
    print(f"IMC: {imc_v}, Cintura: {cintura_v} → Obesidade: {resultado:.2f}%")

# Função para comparar os três modelos em um caso específico
def comparar_modelos(imc_valor, cintura_valor):
    # Configurar para modelo triangular
    imc.terms = imc_trimf
    cintura.terms = cintura_trimf
    obesidade.terms = obesidade_trimf
    resultado_trimf = testar_sistema(imc_valor, cintura_valor)
    
    # Configurar para modelo gaussiano
    imc.terms = imc_gaussmf
    cintura.terms = cintura_gaussmf
    obesidade.terms = obesidade_gaussmf
    resultado_gaussmf = testar_sistema(imc_valor, cintura_valor)
    
    # Configurar para modelo trapezoidal
    imc.terms = imc_trapmf
    cintura.terms = cintura_trapmf
    obesidade.terms = obesidade_trapmf
    resultado_trapmf = testar_sistema(imc_valor, cintura_valor)
    
    return resultado_trimf, resultado_gaussmf, resultado_trapmf

# Casos para comparação
casos_comparacao = [
    (22, 75),  # Normal, cintura baixa
    (27, 90),  # Sobrepeso, cintura moderada
    (32, 105)  # Obesidade, cintura alta
]

print("\nComparando diferentes funções de pertinência:")
for imc_v, cintura_v in casos_comparacao:
    tri, gauss, trap = comparar_modelos(imc_v, cintura_v)
    print(f"IMC: {imc_v}, Cintura: {cintura_v}")
    print(f"  Triangular: {tri:.2f}%")
    print(f"  Gaussiana: {gauss:.2f}%")
    print(f"  Trapezoidal: {trap:.2f}%")

# ----- PARTE 4: ADICIONANDO NOVA VARIÁVEL - ATIVIDADE FÍSICA -----
print("\n=== SISTEMA EXPANDIDO COM ATIVIDADE FÍSICA ===")

# Restaurando a configuração triangular
imc.terms = imc_trimf
cintura.terms = cintura_trimf
obesidade.terms = obesidade_trimf

# Nova variável de entrada: Atividade Física
atividade_fisica = ctrl.Antecedent(np.arange(0, 301, 1), 'atividade_fisica')

# Definindo conjuntos fuzzy para Atividade Física (minutos por semana)
atividade_fisica['sedentario'] = fuzz.trimf(atividade_fisica.universe, [0, 0, 60])
atividade_fisica['moderado'] = fuzz.trimf(atividade_fisica.universe, [30, 120, 210])
atividade_fisica['ativo'] = fuzz.trimf(atividade_fisica.universe, [180, 300, 300])

# Visualizando os conjuntos fuzzy para atividade física
atividade_fisica.view()
plt.title('Conjuntos Fuzzy para Atividade Física (min/semana)')
plt.savefig('atividade_fisica.png')

# Novas regras incluindo atividade física
regra9 = ctrl.Rule(atividade_fisica['sedentario'] & imc['sobrepeso'], obesidade['moderada'])
regra10 = ctrl.Rule(atividade_fisica['ativo'] & imc['sobrepeso'], obesidade['saudável'])
regra11 = ctrl.Rule(atividade_fisica['ativo'] & imc['obesidade'] & cintura['risco_moderado'], obesidade['moderada'])
regra12 = ctrl.Rule(atividade_fisica['sedentario'] & imc['normal'] & cintura['risco_moderado'], obesidade['moderada'])
regra13 = ctrl.Rule(atividade_fisica['ativo'] & imc['normal'], obesidade['saudável'])

print("Regras adicionais para o sistema expandido:")
print("9. Se atividade física é sedentário E IMC é sobrepeso, então obesidade é moderada")
print("10. Se atividade física é ativo E IMC é sobrepeso, então obesidade é saudável")
print("11. Se atividade física é ativo E IMC é obesidade E cintura é risco moderado, então obesidade é moderada")
print("12. Se atividade física é sedentário E IMC é normal E cintura é risco moderado, então obesidade é moderada")
print("13. Se atividade física é ativo E IMC é normal, então obesidade é saudável")

# Sistema de controle expandido
sistema_expandido_ctrl = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8, 
                                           regra9, regra10, regra11, regra12, regra13])
sistema_expandido = ctrl.ControlSystemSimulation(sistema_expandido_ctrl)

# Função para testar o sistema expandido
def testar_sistema_expandido(imc_valor, cintura_valor, atividade_valor):
    sistema_expandido.input['imc'] = imc_valor
    sistema_expandido.input['cintura'] = cintura_valor
    sistema_expandido.input['atividade_fisica'] = atividade_valor
    sistema_expandido.compute()
    return sistema_expandido.output['obesidade']

# Casos de teste para o sistema expandido
casos_teste_expandido = [
    # IMC, Cintura, Atividade Física
    (27, 90, 30),    # Sobrepeso, cintura moderada, sedentário
    (27, 90, 150),   # Sobrepeso, cintura moderada, moderadamente ativo
    (27, 90, 250),   # Sobrepeso, cintura moderada, muito ativo
    (32, 105, 30),   # Obesidade, cintura alta, sedentário
    (32, 105, 250)   # Obesidade, cintura alta, muito ativo
]

print("\nTestando o sistema expandido com atividade física:")
for imc_v, cintura_v, ativ_v in casos_teste_expandido:
    resultado = testar_sistema_expandido(imc_v, cintura_v, ativ_v)
    print(f"IMC: {imc_v}, Cintura: {cintura_v}, Atividade: {ativ_v} min/semana → Obesidade: {resultado:.2f}%")

