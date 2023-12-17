import random
import copy

class Cliente:
    def __init__(self, nome, quantidade, x, y):
        self.nome = nome
        self.quantidade = quantidade
        self.coordenadas = Ponto(x, y)

    def __repr__(self):
        return f'Cliente({self.nome}, {self.quantidade}, {repr(self.coordenadas)})'

class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Ponto({self.x}, {self.y})'

listaClientes = [
    Cliente(1, 4, 14, 2),
    Cliente(2, 4, 5, 6),
    Cliente(3, 2, 7, 7),
    Cliente(4, 4, 9, 4),
    Cliente(5, 3, 1, 2),
    Cliente(6, 2, 7, 7),
]

def criaGeracao(listaClientes):
    listaGeracao = []
    for i in range(10):
        listaGeracao.append(gerarArrayAleatorio(listaClientes))
    return listaGeracao

def totalPedidos(listaClientes):
    soma_elementos = sum(cliente.quantidade for cliente in listaClientes)
    return soma_elementos

def gerarArrayAleatorio(listaClientes):
    voltasSede = len(listaClientes)
    quantiaVoltasSedeAleatorio = random.randint(voltasSede, voltasSede + 5)

    clientes_copy = listaClientes.copy()

    for i in range(quantiaVoltasSedeAleatorio):
        clientes_copy.append(Cliente(0, 0, 0, 0))

    clientes_embaralhados = random.sample(clientes_copy, len(clientes_copy))
    return [Cliente(0, 0, 0, 0)] + clientes_embaralhados

def getDistancia(posCliente1, posCliente2):
    distancia = ((posCliente1.x - posCliente2.x) ** 2 + (posCliente1.y - posCliente2.y) ** 2)
    return distancia

def getTempoTolerancia(posSede, posCliente):
    return getDistancia(posSede, posCliente) * 1.5

def getSatisfacao(posSede, posCliente, tempoEntrega, quantidade):
    tempoTolerancia = getTempoTolerancia(posSede, posCliente)

    # Add a check to avoid division by zero
    if tempoTolerancia == 0:
        return 0

    percentualAtraso = ((tempoEntrega - tempoTolerancia) / tempoTolerancia) * 100

    if percentualAtraso <= 10:
        return 5
    elif percentualAtraso <= 20:
        return 4
    elif percentualAtraso <= 40:
        return 3
    elif percentualAtraso <= 60:
        return 2
    elif percentualAtraso <= 80:
        return 1
    else:
        return 0

def calcSatisfacao(clientes):
    tempo_atual = 0
    carga_atual = 4
    satisfacao_total = 0

    for i in range(1, len(clientes)):
        cliente_atual = clientes[i]
        pos_sede = clientes[0].coordenadas
        pos_cliente = cliente_atual.coordenadas

        distancia = getDistancia(pos_sede, pos_cliente)
        tempo_entrega = distancia * 0.5
        tempo_tolerancia = getTempoTolerancia(pos_sede, pos_cliente)

        if carga_atual < cliente_atual.quantidade:
            satisfacao_total -= 5

        if tempo_atual + tempo_entrega > tempo_tolerancia:
            satisfacao_total -= 10

        if carga_atual >= cliente_atual.quantidade and tempo_atual + tempo_entrega <= tempo_tolerancia:
            satisfacao = getSatisfacao(pos_sede, pos_cliente, tempo_entrega, cliente_atual.quantidade)
            satisfacao_total += satisfacao
            tempo_atual += tempo_entrega
            carga_atual -= cliente_atual.quantidade

    return satisfacao_total

# Restante do código...

# Funções adicionais
def calcularSatisfacaoPopulacao(populacao):
    satisfacoes = [calcSatisfacao(individuo) for individuo in populacao]
    return satisfacoes

def ordenarPopulacaoPorSatisfacao(populacao, satisfacoes):
    satisfacoes_ordenada = sorted(satisfacoes, reverse=True)

    def comparador(cliente1, cliente2):
        satisfacao_cliente1 = satisfacoes_ordenada[populacao.index(cliente1)]
        satisfacao_cliente2 = satisfacoes_ordenada[populacao.index(cliente2)]
        return satisfacao_cliente1 - satisfacao_cliente2

    populacao_ordenada = sorted(populacao, key=comparador, reverse=True)
    return populacao_ordenada

def selecionarMelhores(populacao_ordenada, percentual_elitismo):
    quantidade_melhores = int(len(populacao_ordenada) * percentual_elitismo)
    melhores = populacao_ordenada[:quantidade_melhores]
    return melhores

def selecionarIndividuoRoleta(populacao, satisfacoes):
    soma_satisfacoes = sum(satisfacoes)
    probabilidade_acumulada = [sum(satisfacoes[:i+1]) / soma_satisfacoes for i in range(len(satisfacoes))]
    sorteio = random.random()
    for i, probabilidade in enumerate(probabilidade_acumulada):
        if sorteio <= probabilidade:
            return populacao[i]

# ...

# Parâmetros
percentual_elitismo = 0.2
taxa_mutacao = 0.1

# Criação da população inicial
populacao = criaGeracao(listaClientes)

# Número de gerações
num_geracoes = 100

# Loop principal
for geracao in range(num_geracoes):
    satisfacoes = calcularSatisfacaoPopulacao(populacao)
    populacao = ordenarPopulacaoPorSatisfacao(populacao, satisfacoes)
    melhores = selecionarMelhores(populacao, percentual_elitismo)
    nova_populacao = melhores
    while len(nova_populacao) < len(populacao):
        pai1 = selecionarIndividuoRoleta(populacao, satisfacoes)
        pai2 = selecionarIndividuoRoleta(populacao, satisfacoes)
        filho1, filho2 = crossover(pai1, pai2)
        filho1_mutado = mutacao(filho1, taxa_mutacao)
        filho2_mutado = mutacao(filho2, taxa_mutacao)
        nova_populacao.extend([filho1_mutado, filho2_mutado])
    populacao = nova_populacao
    melhor_satisfacao = calcularSatisfacaoPopulacao([populacao[0]])[0]
    print(f"Geração {geracao + 1} - Melhor Satisfação: {melhor_satisfacao}")

melhor_solucao = populacao[0]
melhor_satisfacao = calcularSatisfacaoPopulacao([melhor_solucao])[0]
print(f"\nMelhor Solução - Satisfação: {melhor_satisfacao}")
print("Caminho da melhor solução:", melhor_solucao)
