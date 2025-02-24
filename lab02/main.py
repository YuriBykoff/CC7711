from aima3.logic import expr, FolKB, fol_fc_ask

# Lista de cláusulas (fatos e regras)
clauses = []

# --- Fatos sobre a genealogia ---

# Relações de progenitor:
clauses.append(expr("Progenitor(Maria,Joao)"))    # Maria é progenitora de Joao.
clauses.append(expr("Progenitor(Ana,Maria)"))       # Ana é progenitora de Maria.
clauses.append(expr("Progenitor(Maria,Pedro)"))     # Maria é progenitora de Pedro.
clauses.append(expr("Progenitor(Carlos,Joao)"))     # Carlos é progenitor de Joao.

# Fatos de sexo:
clauses.append(expr("Sexo(Ana,Feminino)"))
clauses.append(expr("Sexo(Maria,Feminino)"))
clauses.append(expr("Sexo(Joao,Masculino)"))
clauses.append(expr("Sexo(Carlos,Masculino)"))
clauses.append(expr("Sexo(Pedro,Masculino)"))

# --- Regras para inferência de novas relações ---

# Se alguém é progenitor de outra pessoa, ambos são pessoas.
clauses.append(expr("Progenitor(x,y) ==> Pessoa(x)"))
clauses.append(expr("Progenitor(x,y) ==> Pessoa(y)"))

# Definição de Mãe: se x é progenitora de y e x é do sexo Feminino, então x é mãe de y.
clauses.append(expr("Progenitor(x,y) & Sexo(x,Feminino) ==> Mae(x,y)"))

# Definição de Pai: se x é progenitor de y e x é do sexo Masculino, então x é pai de y.
clauses.append(expr("Progenitor(x,y) & Sexo(x,Masculino) ==> Pai(x,y)"))

# Definição de Irmão e Irmã:
# Se dois indivíduos compartilham pelo menos um mesmo progenitor e o primeiro é do sexo Masculino, então ele é irmão do outro.
clauses.append(expr("Progenitor(z,x) & Progenitor(z,y) & Sexo(x,Masculino) ==> Irmao(x,y)"))
# Se dois indivíduos compartilham pelo menos um mesmo progenitor e o primeiro é do sexo Feminino, então ela é irmã da outra.
clauses.append(expr("Progenitor(z,x) & Progenitor(z,y) & Sexo(x,Feminino) ==> Irma(x,y)"))

# Definição de Descendente:
# Regra base: Se x é progenitor de y, então y é descendente de x.
clauses.append(expr("Progenitor(x,y) ==> Descendente(y,x)"))
# Regra transitiva: Se x é progenitor de y e z é descendente de y, então z é descendente de x.
clauses.append(expr("Progenitor(x,y) & Descendente(z,y) ==> Descendente(z,x)"))

# --- Criação da Base de Conhecimento ---

Genealogia = FolKB(clauses)

# --- Lista de Consultas ---
perguntas = [
    "Sexo(x,Masculino)",
    "Sexo(Maria,x)",
    "Irmao(x,Ana)",
    "Irma(x,Joao)",
    "Descendente(x,Maria)",
    "Descendente(Joao,x)",
    "Pessoa(x)",
    "Mae(x,y)",
    "Pai(x,y)"
]

# Execução das consultas e impressão dos resultados
for i in perguntas:
    resposta = fol_fc_ask(Genealogia, expr(i))
    print("%s -> %s" % (i, list(resposta)))
