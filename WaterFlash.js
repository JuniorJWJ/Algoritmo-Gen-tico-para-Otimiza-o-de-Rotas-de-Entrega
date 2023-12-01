class Ponto {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

class Pedido {
    constructor(cliente, quantidade) {
        this.cliente = cliente;
        this.quantidade = quantidade;
    }
}

const listaPontos = [
    new Ponto(0, 0),
    new Ponto(5, 6),
    new Ponto(7, 7),
];

const listaPedidos = [
    new Pedido(1, 2),
    new Pedido(3, 4),
    new Pedido(5, 6),
];

function gerarArrayAleatorio(listaPontos) {
    return listaPontos.map(ponto => `(${ponto.x}, ${ponto.y})`).sort(() => Math.random() - 0.5);
}


function calcSatisfacao(arrayOrdem) {
    return arrayOrdem.reduce((satisfacao, ponto, index, array) => {
        const atual = parseInt(ponto);
        console.log("atual:",atual);
        const proximo = parseInt(array[index + 1]);

        if (proximo !== undefined) {
            const tempoEntrega = getDistancia(listaPontos[atual], listaPontos[proximo]) * 0.5;
            satisfacao += getSatisfacao(listaPontos[atual], listaPontos[proximo], tempoEntrega);
        }

        return satisfacao;
    }, 0);
}

function getDistancia(posSede, posCliente) {
    console.log(posSede, posCliente);
    const { x: xSede, y: ySede } = posSede;
    const { x: xCliente, y: yCliente } = posCliente;
    return Math.hypot(xSede - xCliente, ySede - yCliente);
}

function getTempoTolerancia(posSede, posCliente) {
    return getDistancia(posSede, posCliente) * 1.5 * 0.5;
}

function getSatisfacao(posSede, posCliente, tempoEntrega) {
    const tempoTolerancia = getTempoTolerancia(posSede, posCliente);

    if (tempoEntrega === tempoTolerancia) return 6;
    if (tempoEntrega < tempoTolerancia / 2) return 10;
    if (tempoEntrega >= tempoTolerancia / 2) return 8;

    const percentualAtraso = ((tempoEntrega - tempoTolerancia) / tempoTolerancia) * 100;

    if (percentualAtraso <= 10) return 5;
    if (percentualAtraso <= 20) return 4;
    if (percentualAtraso <= 40) return 3;
    if (percentualAtraso <= 60) return 2;
    if (percentualAtraso <= 80) return 1;

    return 0;
}

// Example usage:
const pontosAleatorios = gerarArrayAleatorio(listaPontos);
console.log(pontosAleatorios);
console.log(calcSatisfacao(pontosAleatorios));
