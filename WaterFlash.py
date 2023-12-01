import random


class Ponto: #Classe que representa a localizaçao do cliente, lembrando que o primeiro índice do array é a posição da Sede
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Pedido: #Classe que representa o pedido do cliente, contendo o identificador do mesmo e a quantidade de águas
    def __init__(self, cliente, quantidade):
        self.cliente = cliente
        self.quantidade = quantidade

listaPontos = [#Array composta pela lista de pontos dos clientes, lembrando que o primeiro índice do array é a posição da Sede
    Ponto(0, 0),
    Ponto(5, 6),
    Ponto(7, 7),
    Ponto(2, 8),
    Ponto(9, 1),
    Ponto(3, 4),
]

listaPedidos = [#Array composta pela lista de Pedidos dos clientes
    Pedido(1, 2),
    Pedido(3, 4),
    Pedido(5, 6),
]

def repr_ponto(ponto):
    return (ponto.x, ponto.y)

def gerarArrayAleatorio(ListaPontos):
    tamanho = len(ListaPontos)
    ordem = []
    for i in range(tamanho):
        ordem.append(i)

    for i in range(tamanho):
        j = random.randrange(tamanho)
        ordem[i], ordem[j] = ordem[j], ordem[i]

    return [repr_ponto(ListaPontos[i]) for i in ordem]

def calcSatisfacao(arrayOrdem):
    satisfacao = 0
    tempoEntrega = 0
    for i in range(len(arrayOrdem) - 1):
        atual = arrayOrdem[i]
        proximo = arrayOrdem[i + 1]

        tempoEntrega += getDistancia(atual, proximo) * 0.5
        print(tempoEntrega)
        print("tempo:", tempoEntrega)
        satisfacao += getSatisfacao(atual, proximo, tempoEntrega)
        print("satisfação:",satisfacao)

    return satisfacao
      
def getDistancia(posSede, posCliente): #Função que pega a distância entre o cliente e a sede
    distancia = ((posSede[0] - posCliente[0])**2 + (posSede[1]- posCliente[1])**2)**(1/2)
    return(distancia)

def getTempoTolerancia(posSede, posCliente): #Função que calcula o tempo de tolerância da entrega
    return getDistancia(posSede, posCliente)*1.5*0.5

def getSatisfacao(posSede, posCliente, tempoEntrega): #Função que calcula a satisfação do cliente mediante o tempo de entrega
    tempoTolerancia = getTempoTolerancia(posSede,posCliente) #Chama a função que calcula o tempo de tolerância da entrega, tomando por parâmetro a posição da sede e a posição do cliente

    if tempoEntrega == tempoTolerancia:
        return 6

    if tempoEntrega < tempoTolerancia / 2:
        return 10

    if tempoEntrega >= tempoTolerancia / 2:
        return 8
    
    percentualAtraso = ((tempoEntrega - tempoTolerancia)/ tempoTolerancia)*100 #Cálculo feito para saber o percentual de atraso da entrega, tomando por base a distância 
    
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

# print(getTempoTolerancia(listaPontos[0], listaPontos[1]))
# print(repr(listaPontos))
listaPontos = gerarArrayAleatorio(listaPontos)
print(listaPontos)
print(calcSatisfacao(listaPontos))
