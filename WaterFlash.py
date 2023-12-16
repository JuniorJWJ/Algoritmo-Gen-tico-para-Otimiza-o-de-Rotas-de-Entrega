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



def calcSatisfacao(arrayOrdem):
    print(arrayOrdem)
    satisfacao = 0
    tempoEntrega = 0
    cargaAtual = 4

    for i in range(len(arrayOrdem) - 1):
        atual = arrayOrdem[i]
        # print("atual:", atual)
        proximo = arrayOrdem[i + 1]
        # print("proximo:", proximo)
                
        # if proximo.quantidade > cargaAtual:
        #     proximo = (Cliente(0, 0, 0, 0))
        #     # arrayOrdem.insert(i + 1, Cliente(0, 0, 0, 0))
        #     arrayOrdem.insert(arrayOrdem[i + 1], arrayOrdem[i + 1])
        #     print("arrayordem:", arrayOrdem)
        #     i += 1  
        #     cargaAtual = 4  

        tempoEntrega += getDistancia(atual.coordenadas, proximo.coordenadas) * 0.5
        # print(tempoEntrega)
        
        
        cargaAtual -= atual.quantidade

        satisfacao += getSatisfacao(atual.coordenadas, proximo.coordenadas, tempoEntrega, atual.quantidade)

    
    if arrayOrdem[-1].nome != 0 and cargaAtual < 4:
        arrayOrdem.append(Cliente(0, 4, 0, 0))

    # print(arrayOrdem)
    return satisfacao


def getDistancia(posSede, posCliente):
    distancia = ((posSede.x - posCliente.x) ** 2 + (posSede.y - posCliente.y) ** 2) ** (1 / 2)
    return distancia

def getTempoTolerancia(posSede, posCliente):
    return getDistancia(posSede, posCliente) * 0.75

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

def criaGeracao(listaClientes):
    listaGeracao = []
    for i in range(10):
        listaGeracao.append(gerarArrayAleatorio(listaClientes))

    return listaGeracao


listaClientes = [
    Cliente(1, 4, 14, 2),
    Cliente(2, 4, 5, 6),
    Cliente(3, 2, 7, 7),
    Cliente(4, 4, 9, 4),
    Cliente(5, 3, 1, 2),
    Cliente(6, 2, 7, 7),
]
print("*********************************************************************************************************************************************************************************************************")
populacao = criaGeracao(listaClientes)
for i in populacao:
    print(i,"\n")
# print(populacao)
# (calcSatisfacao(populacao[0]))

# print(totalPedidos(populacao[0]))