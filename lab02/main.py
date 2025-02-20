from aima3.logic import expr, FolKB, fol_fc_ask

# Lista de cláusulas (fatos e regras)
clauses = []

# --- Fatos sobre a família Carvalho ---

# O casal Pietro e Antonita criaram cinco filhos: João, Clara, Francisco, Valéria e Ana.
clauses.append(expr("parent(pietro, joao)"))
clauses.append(expr("parent(antonita, joao)"))

clauses.append(expr("parent(pietro, clara)"))
clauses.append(expr("parent(antonita, clara)"))

clauses.append(expr("parent(pietro, francisco)"))
clauses.append(expr("parent(antonita, francisco)"))

clauses.append(expr("parent(pietro, valeria)"))
clauses.append(expr("parent(antonita, valeria)"))

clauses.append(expr("parent(pietro, ana)"))
clauses.append(expr("parent(antonita, ana)"))

# Informações de sexo
clauses.append(expr("masculino(pietro)"))
clauses.append(expr("feminino(antonita)"))

clauses.append(expr("masculino(joao)"))
clauses.append(expr("feminino(clara)"))
clauses.append(expr("masculino(francisco)"))
clauses.append(expr("feminino(valeria)"))
clauses.append(expr("feminino(ana)"))

# Ana teve duas filhas: Helena e Joana.
clauses.append(expr("parent(ana, helena)"))
clauses.append(expr("parent(ana, joana)"))

clauses.append(expr("feminino(helena)"))
clauses.append(expr("feminino(joana)"))

# Mário é filho de João.
clauses.append(expr("parent(joao, mario)"))
clauses.append(expr("masculino(mario)"))

# Carlos nasceu da relação entre Helena e Mário.
clauses.append(expr("parent(helena, carlos)"))
clauses.append(expr("parent(mario, carlos)"))
clauses.append(expr("masculino(carlos)"))

# Francisco não teve filhos, mas casou-se com Fabiana.
clauses.append(expr("casado(francisco, fabiana)"))
clauses.append(expr("feminino(fabiana)"))

# Clara era mãe de Pietro2 e Enzo.
clauses.append(expr("parent(clara, pietro2)"))
clauses.append(expr("parent(clara, enzo)"))

clauses.append(expr("masculino(pietro2)"))
clauses.append(expr("masculino(enzo)"))

# Pietro2 e Enzo casaram com as irmãs Francisca e Antonia.
clauses.append(expr("casado(pietro2, francisca)"))
clauses.append(expr("casado(enzo, antonia)"))

clauses.append(expr("feminino(francisca)"))
clauses.append(expr("feminino(antonia)"))

# Francisca e Antonia são filhas de Jacynto e Claudia.
clauses.append(expr("parent(jacynto, francisca)"))
clauses.append(expr("parent(claudia, francisca)"))

clauses.append(expr("parent(jacynto, antonia)"))
clauses.append(expr("parent(claudia, antonia)"))

clauses.append(expr("masculino(jacynto)"))
clauses.append(expr("feminino(claudia)"))

# Jacynto é filho de Luzia e Pablo.
clauses.append(expr("parent(luzia, jacynto)"))
clauses.append(expr("parent(pablo, jacynto)"))

clauses.append(expr("feminino(luzia)"))
clauses.append(expr("masculino(pablo)"))

# --- Regras para inferência de novas relações ---

# Definição de pai e mãe:
clauses.append(expr("parent(x,y) & masculino(x) ==> pai(x,y)"))
clauses.append(expr("parent(x,y) & feminino(x) ==> mae(x,y)"))

# Definição de irmãos/irmãs usando o predicado 'diferente'
clauses.append(expr("parent(p, x) & parent(p, y) & diferente(x, y) ==> irmaos(x,y)"))

# Definição de tio e tia:
clauses.append(expr("parent(p, n) & irmaos(t, p) & masculino(t) ==> tio(t,n)"))
clauses.append(expr("parent(p, n) & irmaos(t, p) & feminino(t) ==> tia(t,n)"))

# Definição de avô e avó:
clauses.append(expr("pai(x, p) & parent(p, n) ==> avô(x,n)"))
clauses.append(expr("mae(x, p) & parent(p, n) ==> avó(x,n)"))

# Definição de primo e prima:
clauses.append(expr("masculino(x) & parent(p, x) & parent(q, y) & irmaos(p, q) ==> primo(x,y)"))
clauses.append(expr("feminino(x) & parent(p, x) & parent(q, y) & irmaos(p, q) ==> prima(x,y)"))

# Definição de descendente e ascendente:
clauses.append(expr("parent(y, x) ==> descendente(x,y)"))
clauses.append(expr("parent(y, z) & descendente(x,z) ==> descendente(x,y)"))
clauses.append(expr("descendente(y,x) ==> ascendente(x,y)"))

# Acrescentando fatos para o predicado 'diferente'
# Lista dos individuos conhecidos:
individuos = [
    "pietro", "antonita", "joao", "clara", "francisco", "valeria", "ana",
    "helena", "joana", "mario", "carlos", "pietro2", "enzo",
    "jacynto", "claudia", "luzia", "pablo", "fabiana", "francisca", "antonia"
]

for ind1 in individuos:
    for ind2 in individuos:
        if ind1 != ind2:
            clauses.append(expr(f"diferente({ind1}, {ind2})"))

# --- Criação da Base de Conhecimento ---

Genealogia = FolKB(clauses)

# --- Lista de Consultas ---
perguntas = [
    "avó(x, carlos)",        # avós de Carlos
    "avô(x, carlos)",        # avôs de Carlos
    "tio(x, enzo)",          # tios de Enzo
    "tia(x, enzo)",          # tias de Enzo
    "primo(x, antonia)",     # primos de Antonia
    "prima(x, antonia)",     # primas de Antonia
    "descendente(carlos, x)", # ascendentes de Carlos (x tais que Carlos é seu descendente)
    "ascendente(x, mario)"    # ascendentes de Mário
]

# Execução das consultas e impressão dos resultados
for i in perguntas:
    resposta = fol_fc_ask(Genealogia, expr(i))
    print("%s -> %s" % (i, list(resposta)))