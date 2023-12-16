import random

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

    print(len(clientes_copy))
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

    for i in range(1, len(clientes)):  # Começa do índice 1 para evitar a sede no início
        cliente_atual = clientes[i]
        pos_sede = clientes[0].coordenadas
        pos_cliente = cliente_atual.coordenadas

        distancia = getDistancia(pos_sede, pos_cliente)
        tempo_entrega = distancia * 0.5
        tempo_tolerancia = getTempoTolerancia(pos_sede, pos_cliente)  # Adiciona esta linha

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
            print("voltou base")
            carga_atual = 4

    return satisfacao_total



print("*********************************************************************************************************************************************************************************************************")
populacao = criaGeracao(listaClientes)
for i in populacao:
    print(i,"\n")
# print(populacao)
# (calcSatisfacao(populacao[0]))

# print(totalPedidos(populacao[0]))
satisfacao_total = calcSatisfacao(populacao[0])
print("Satisfação Total:", satisfacao_total)
