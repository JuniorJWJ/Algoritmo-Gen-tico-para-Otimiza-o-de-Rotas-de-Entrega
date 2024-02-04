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


def repr_ponto(ponto):
    return (ponto.x, ponto.y)

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

    if tempoEntrega == tempoTolerancia:
        return 6

    if tempoEntrega < tempoTolerancia / 2:
        return 10

    if tempoEntrega >= tempoTolerancia / 2:
        return 8

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

        if cliente_atual.nome == 0:
            carga_atual = 4

    return satisfacao_total

def mutacao(individuo):
    ponto_corte1 = random.randint(0, len(individuo) - 2)
    ponto_corte2 = random.randint(ponto_corte1 + 1, len(individuo) - 1)
    parte_embaralhada = individuo[ponto_corte1:ponto_corte2]
    random.shuffle(parte_embaralhada)
    individuo[ponto_corte1:ponto_corte2] = parte_embaralhada
    return individuo




def crossover(pai1, pai2):
    ponto_corte1 = random.randint(1, len(pai1) - 2)
    ponto_corte2 = random.randint(ponto_corte1 + 1, len(pai2) - 1)
    filho1 = pai1[:ponto_corte1] + pai2[ponto_corte1:ponto_corte2] + pai1[ponto_corte2:]
    filho2 = pai2[:ponto_corte1] + pai1[ponto_corte1:ponto_corte2] + pai2[ponto_corte2:]
    return filho1, filho2



def elitismo(populacao_ordenada, elitismo_size):
    melhores_individuos = [individuo for individuo, _ in populacao_ordenada[:elitismo_size]]
    return melhores_individuos


def evolucao(populacao, taxa_mutacao, elitismo_size):
    satisfacao_por_individuo = [(individuo, calcSatisfacao(individuo)) for individuo in populacao]
    populacao_ordenada = sorted(satisfacao_por_individuo, key=lambda x: x[1], reverse=True)

    melhores_individuos = elitismo(populacao_ordenada, elitismo_size)
    nova_geracao = copy.deepcopy(melhores_individuos)

    while len(nova_geracao) < len(populacao):
        pai1, pai2 = random.sample(melhores_individuos, 2)
        filho1, filho2 = crossover(pai1, pai2)
        nova_geracao.append(filho1)
        nova_geracao.append(filho2)

    nova_geracao = [mutacao(individuo) for individuo in nova_geracao]

    return nova_geracao


# Exemplo de uso
# Exemplo de uso
populacao = criaGeracao(listaClientes)

melhor_individuo = None
melhor_satisfacao = float('-inf')

for geracao in range(100000):  # Ajuste o número de gerações conforme necessário
    populacao = evolucao(populacao, taxa_mutacao=0.1, elitismo_size=2)
    satisfacao_total = calcSatisfacao(populacao[0])
    print(f"Geração {geracao + 1}: Satisfação Total = {satisfacao_total}")

    # Atualiza o melhor indivíduo se necessário
    if satisfacao_total > melhor_satisfacao:
        melhor_satisfacao = satisfacao_total
        melhor_individuo = copy.deepcopy(populacao[0])

print("\nMelhor Caminho:")
print(melhor_individuo)
print(f"Satisfação Total: {melhor_satisfacao}")
#teste
