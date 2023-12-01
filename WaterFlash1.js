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

function repr_ponto(ponto) {
    return `({ponto.x}, {ponto.y})`;
}

function gerarArrayAleatorio(listaPontos) {
    const tamanho = listaPontos.length;
    const ordem = Array.from({ length: tamanho }, (_, i) => i);
    const random = Math.random();

    for (let i = 0; i < tamanho; i++) {
        const j = Math.floor(random * tamanho);
        [ordem[i], ordem[j]] = [ordem[j], ordem[i]];
    }

    return ordem;
}

function calcSatisfacao(arrayOrdem) {
    let satisfacao = 0;
    for (let i = 0; i < arrayOrdem.length - 1; i++) {
        const atual = arrayOrdem[i];
        const proximo = arrayOrdem[i + 1];

        const tempoEntrega = getDistancia(listaPontos[atual], listaPontos[proximo]) * 0.5;
        satisfacao += getSatisfacao(atual, proximo, tempoEntrega);
    }

    return satisfacao;
}

function getDistancia(posSede, posCliente) {
    return Math.sqrt(
        Math.pow(posSede.x - posCliente.x, 2) + Math.pow(posCliente.y - posCliente.y, 2)
    );
}

function getTempoTolerancia(posSede, posCliente) {
    return getDistancia(posSede, posCliente) * 1.5 * 0.5;
}

function getSatisfacao(atual, proximo, tempoEntrega) {
    const tempoTolerancia = getTempoTolerancia(atual, proximo);

    if (tempoEntrega <= tempoTolerancia) {
        return 6;
    }

    const percentualAtraso = ((tempoEntrega - tempoTolerancia) / tempoTolerancia) * 100;

    if (percentualAtraso <= 10) {
        return 5;
    } else if (percentualAtraso <= 20) {
        return 4;
    } else if (percentualAtraso <= 40) {
        return 3;
    } else if (percentualAtraso <= 60) {
        return 2;
    } else if (percentualAtraso <= 80) {
        return 1;
    } else {
        return 0;
    }
}

// console.log(getTempoTolerancia(listaPontos[0], listaPontos[1]));
listaPontos = gerarArrayAleatorio(listaPontos);
console.log(listaPontos.map(repr_ponto));
console.log(calcSatisfacao(listaPontos));
