import random
import copy
random.seed(11)

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
        listaGeracao.append( [ gerarArrayAleatorio(listaClientes), 0 ])

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
    distancia = ((posCliente1.x - posCliente2.x) * 2 + (posCliente1.y - posCliente2.y) * 2)
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

def isSede(cliente):
    if cliente.coordenadas.x == 0 and (cliente.coordenadas.y == 0):
        return True
    return False
def calcSatisfacao(clientes):
   
    tempo_atual = 0
    carga_atual = 4
    satisfacao_total = 0

    
    #print(clientes[0], "\n")
    cliente_teste = clientes[0]
    for clin in cliente_teste:
        #print("carga atual", carga_atual)
       # print("cliente atual", clin)
        pos_sede = Cliente(0, 0, 0, 0).coordenadas
        pos_cliente = clin.coordenadas

        distancia = getDistancia(pos_sede, pos_cliente)
        #print("distancia", distancia)
        tempo_entrega = distancia * 0.5
        tempo_tolerancia = getTempoTolerancia(pos_sede, pos_cliente)
        #print("carga_atual < clin.quantidade", carga_atual , clin.quantidade)
        if(isSede(clin)):
            carga_atual = 4
            
        if carga_atual < clin.quantidade:
            satisfacao_total -= 5
        
            
        if tempo_atual + tempo_entrega > tempo_tolerancia:
            satisfacao_total -= 10

        if carga_atual >= clin.quantidade:
            satisfacao = getSatisfacao(pos_sede, pos_cliente, tempo_entrega, clin.quantidade)
            satisfacao_total += satisfacao
            tempo_atual += tempo_entrega
            carga_atual -= clin.quantidade

        #if cliente_teste.nome == 0:
           # carga_atual = 4
    #print("satisfacao_total", satisfacao_total)
    return satisfacao_total

def mutacao(individuo):
    ponto_corte1 = random.randint(0, len(individuo) - 2)
    ponto_corte2 = random.randint(ponto_corte1 + 1, len(individuo) - 1)
    parte_embaralhada = individuo[ponto_corte1:ponto_corte2]
    random.shuffle(parte_embaralhada)
    individuo[ponto_corte1:ponto_corte2] = parte_embaralhada
    return individuo




def crossover(pai1, pai2):
    ponto_corte1 = random.randint(1, len(pai1))
    filho1 = pai1[:ponto_corte1] + pai2[ponto_corte1:] 
    filho2 = pai2[:ponto_corte1] + pai1[ponto_corte1:] 
    return filho1, filho2



def elitismo(populacao_ordenada, elitismo_size):
    melhores_individuos = [individuo for individuo, _ in populacao_ordenada[:elitismo_size]]
    return melhores_individuos


# Exemplo de uso
# Exemplo de uso
populacao = criaGeracao(listaClientes)

melhor_individuo = None
melhor_satisfacao = -10000

for geracao in range(1000):  # Ajuste o número de gerações conforme necessário
    print("Geracao", geracao)
    
    satisfacao_por_individuo = []
    for i in populacao:
        satisfacao_por_individuo.append([ i, calcSatisfacao(i) ] )
    
    populacao_ordenada = sorted(satisfacao_por_individuo, key=lambda x: x[1], reverse=True)
    
    fitness_melhor = populacao_ordenada[0][-1]
    print(fitness_melhor)
   
    # Atualiza o melhor indivíduo se necessário
    if fitness_melhor > melhor_satisfacao:
        melhor_satisfacao = fitness_melhor
        melhor_individuo = copy.deepcopy(populacao_ordenada[0])
    
    #melhores_individuos = elitismo(populacao_ordenada, elitismo_size)
    nova_geracao = []
    pai1 = populacao_ordenada[0][0]
    pai2 = populacao_ordenada[1][0]
    nova_geracao.append(pai1)
    nova_geracao.append(pai2)
    
    filho1, filho2 = crossover(pai1, pai2)
    nova_geracao.append(filho1)
    nova_geracao.append(filho2)
    
    for _ in range(0,6):
        nova_geracao.append( [ gerarArrayAleatorio(listaClientes), 0] )
 
    populacao = nova_geracao

    

print("\nMelhor Caminho:")
print(melhor_individuo)
print(f"Satisfação Total: {melhor_satisfacao}")