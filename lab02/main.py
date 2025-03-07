from aima3.logic import expr, FolKB, fol_fc_ask

clauses = []

# --- Fatos sobre a genealogia ---

# Relações de progenitor:
clauses.append(expr("Progenitor(Maria,Joao)"))   
clauses.append(expr("Progenitor(Ana,Maria)"))       
clauses.append(expr("Progenitor(Maria,Pedro)"))    
clauses.append(expr("Progenitor(Carlos,Joao)"))    

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

# Definição de Mãe: 
clauses.append(expr("Progenitor(x,y) & Sexo(x,Feminino) ==> Mae(x,y)"))

# Definição de Pai: 
clauses.append(expr("Progenitor(x,y) & Sexo(x,Masculino) ==> Pai(x,y)"))

# Definição de Irmão e Irmã:
clauses.append(expr("Progenitor(z,x) & Progenitor(z,y) & Sexo(x,Masculino) ==> Irmao(x,y)"))
clauses.append(expr("Progenitor(z,x) & Progenitor(z,y) & Sexo(x,Feminino) ==> Irma(x,y)"))

# Definição de Descendente:
clauses.append(expr("Progenitor(x,y) ==> Descendente(y,x)"))
clauses.append(expr("Progenitor(x,y) & Descendente(z,y) ==> Descendente(z,x)"))


Genealogia = FolKB(clauses)

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

for i in perguntas:
    resposta = fol_fc_ask(Genealogia, expr(i))
    print("%s -> %s" % (i, list(resposta)))
