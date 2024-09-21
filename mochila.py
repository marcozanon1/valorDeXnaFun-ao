import random


# Definir função de aptidão (fitness)
def fitness(cromossomo, pesos_e_valores, peso_maximo):
    valor_total = 0
    peso_total = 0
    for i, gene in enumerate(cromossomo):
        if gene == 1:
            peso_total += pesos_e_valores[i][0]
            valor_total += pesos_e_valores[i][1]
    if peso_total > peso_maximo:
        return 0  # Penalidade por exceder o peso
    return valor_total


# Gerar cromossomos (população inicial)
def gerar_cromossomo(tamanho):
    return [random.randint(0, 1) for _ in range(tamanho)]


def gerar_populacao(tamanho_populacao, tamanho_cromossomo):
    return [gerar_cromossomo(tamanho_cromossomo) for _ in range(tamanho_populacao)]


# Seleção por torneio
def selecao_torneio(populacao, fitnesses, k=3):
    selecionados = random.sample(list(zip(populacao, fitnesses)), k)
    return max(selecionados, key=lambda x: x[1])[0]


# Crossover (ponto único)
def crossover(pai1, pai2):
    ponto = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2


# Mutação
def mutacao(cromossomo, taxa_mutacao=0.01):
    for i in range(len(cromossomo)):
        if random.random() < taxa_mutacao:
            cromossomo[i] = 1 - cromossomo[i]  # Alternar entre 0 e 1


# Algoritmo genético
def algoritmo_genetico(pesos_e_valores, peso_maximo, numero_de_cromossomos, geracoes):
    tamanho_cromossomo = len(pesos_e_valores)
    populacao = gerar_populacao(numero_de_cromossomos, tamanho_cromossomo)

    melhor_de_cada_geracao = []

    for geracao in range(geracoes):
        # Calcular fitness de cada cromossomo
        fitnesses = [fitness(cromossomo, pesos_e_valores, peso_maximo) for cromossomo in populacao]

        # Armazenar o melhor cromossomo da geração
        melhor_fitness = max(fitnesses)
        melhor_cromossomo = populacao[fitnesses.index(melhor_fitness)]
        melhor_de_cada_geracao.append((melhor_fitness, melhor_cromossomo))

        # Nova geração
        nova_populacao = []

        while len(nova_populacao) < numero_de_cromossomos:
            pai1 = selecao_torneio(populacao, fitnesses)
            pai2 = selecao_torneio(populacao, fitnesses)
            filho1, filho2 = crossover(pai1, pai2)

            # Aplicar mutação
            mutacao(filho1)
            mutacao(filho2)

            nova_populacao.append(filho1)
            nova_populacao.append(filho2)

        populacao = nova_populacao[:numero_de_cromossomos]

    # Calcular a média dos pesos dos itens no melhor cromossomo de cada geração
    medias_pesos = []
    for _, melhor_cromossomo in melhor_de_cada_geracao:
        peso_total = sum(pesos_e_valores[i][0] for i, gene in enumerate(melhor_cromossomo) if gene == 1)
        medias_pesos.append(peso_total)

    return medias_pesos, melhor_de_cada_geracao


# Exemplo de uso:
pesos_e_valores = [[2, 10], [4, 30], [6, 300], [8, 10], [8, 30], [8, 300], [12, 50], [25, 75], [50, 100], [100, 400]]
peso_maximo = 100
numero_de_cromossomos = 150
geracoes = 50

melhor_de_cada_geracao = algoritmo_genetico(pesos_e_valores, peso_maximo, numero_de_cromossomos, geracoes)


print(melhor_de_cada_geracao)