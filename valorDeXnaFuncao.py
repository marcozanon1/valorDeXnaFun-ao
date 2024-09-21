import random


def funcao_objetivo(x):
    return x ** 3 - 6 * x + 14


def decodificar_binario(cromossomo, min_val=-10, max_val=10):
    valor_binario = int("".join(map(str, cromossomo)), 2)
    max_bin = 2 ** len(cromossomo) - 1
    return min_val + (max_val - min_val) * (valor_binario / max_bin)


def gerar_cromossomo(tamanho):
    return [random.randint(0, 1) for _ in range(tamanho)]


def calcular_fitness(cromossomo):
    x = decodificar_binario(cromossomo)
    return -funcao_objetivo(x)


def selecao_torneio(populacao, fitness_populacao, tamanho_torneio=3):
    torneio = random.sample(range(len(populacao)), tamanho_torneio)
    melhor = max(torneio, key=lambda idx: fitness_populacao[idx])
    return populacao[melhor]


def selecao_roleta_viciada(populacao, fitness_populacao):
    soma_fitness = sum(fitness_populacao)
    pick = random.uniform(0, soma_fitness)
    atual = 0
    for i, fitness in enumerate(fitness_populacao):
        atual += fitness
        if atual > pick:
            return populacao[i]


def crossover(pai1, pai2, num_pontos=1):
    if num_pontos == 1:
        ponto = random.randint(1, len(pai1) - 1)
        filho1 = pai1[:ponto] + pai2[ponto:]
        filho2 = pai2[:ponto] + pai1[ponto:]
    else:
        ponto1 = random.randint(1, len(pai1) - 2)
        ponto2 = random.randint(ponto1 + 1, len(pai1) - 1)
        filho1 = pai1[:ponto1] + pai2[ponto1:ponto2] + pai1[ponto2:]
        filho2 = pai2[:ponto1] + pai1[ponto1:ponto2] + pai2[ponto2:]

    return filho1, filho2


def mutacao(cromossomo, taxa_mutacao):
    for i in range(len(cromossomo)):
        if random.random() < taxa_mutacao:
            cromossomo[i] = 1 - cromossomo[i]
    return cromossomo


# Algoritmo Genético
def algoritmo_genetico(
        tamanho_populacao, tamanho_cromossomo, geracoes, taxa_mutacao=0.01,
        num_pontos_crossover=1, metodo_selecao="torneio", elitismo=False, perc_elite=0.1):
    populacao = [gerar_cromossomo(tamanho_cromossomo) for _ in range(tamanho_populacao)]
    melhor_individuo_geral = None
    melhor_fitness_geral = float('-inf')

    for geracao in range(geracoes):
        fitness_populacao = [calcular_fitness(cromossomo) for cromossomo in populacao]

        num_elite = int(tamanho_populacao * perc_elite) if elitismo else 0
        elite = sorted(populacao, key=lambda ind: calcular_fitness(ind), reverse=True)[:num_elite]

        nova_populacao = elite[:]

        while len(nova_populacao) < tamanho_populacao:
            if metodo_selecao == "torneio":
                pai1 = selecao_torneio(populacao, fitness_populacao)
                pai2 = selecao_torneio(populacao, fitness_populacao)
            else:
                pai1 = selecao_roleta_viciada(populacao, fitness_populacao)
                pai2 = selecao_roleta_viciada(populacao, fitness_populacao)

            # Crossover
            filho1, filho2 = crossover(pai1, pai2, num_pontos=num_pontos_crossover)

            # Mutação
            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)

            nova_populacao.append(filho1)
            if len(nova_populacao) < tamanho_populacao:
                nova_populacao.append(filho2)

        populacao = nova_populacao

        # Encontrar o melhor da geração
        fitness_geracao = [calcular_fitness(cromossomo) for cromossomo in populacao]
        melhor_fitness_geracao = max(fitness_geracao)
        melhor_individuo_geracao = populacao[fitness_geracao.index(melhor_fitness_geracao)]

        if melhor_fitness_geracao > melhor_fitness_geral:
            melhor_fitness_geral = melhor_fitness_geracao
            melhor_individuo_geral = melhor_individuo_geracao

        x_melhor = decodificar_binario(melhor_individuo_geral)
        print(f"Geracao {geracao + 1}: Melhor x = {x_melhor}, Fitness = {-melhor_fitness_geral}")

    return decodificar_binario(melhor_individuo_geral), -melhor_fitness_geral


tamanho_populacao = 10
tamanho_cromossomo = 16
geracoes = 100
taxa_mutacao = 0.01
num_pontos_crossover = 1
metodo_selecao = "torneio"
elitismo = True
perc_elite = 0.2

# Executar o algoritmo genético
melhor_x, melhor_fitness = algoritmo_genetico(
    tamanho_populacao, tamanho_cromossomo, geracoes, taxa_mutacao,
    num_pontos_crossover, metodo_selecao, elitismo, perc_elite)

print(f"\nMelhor x encontrado: {melhor_x}")
print(f"Valor minimo da funcao: {melhor_fitness}")