'''
Funcoes PURAS sobre o grafo de dependencias (nenhuma delas faz print ou
input). O grafo eh representado por dicionarios, como no metro da aula.
'''


def valida_tarefas(tarefas):
    '''Confere se o dicionario de tarefas esta bem formado.

    Levanta ValueError com uma mensagem clara quando:
    - a duracao nao eh um inteiro positivo;
    - uma tarefa depende de si mesma;
    - uma tarefa depende de outra que nao existe.
    O(V + E): olha cada tarefa e cada dependencia uma vez.
    '''
    for nome, tarefa in tarefas.items():
        duracao = tarefa['duracao']
        if not isinstance(duracao, int) or duracao <= 0:
            raise ValueError(f"tarefa '{nome}': duracao deve ser inteiro positivo")
        for dependencia in tarefa['depende_de']:
            if dependencia == nome:
                raise ValueError(f"tarefa '{nome}' depende de si mesma")
            if dependencia not in tarefas:
                raise ValueError(f"tarefa '{nome}' depende de '{dependencia}', que nao existe")


def monta_sucessores(tarefas):
    '''Lista de adjacencia: tarefa -> tarefas que dependem dela.

    Os dados guardam "quem vem ANTES" (depende_de); a ordenacao
    topologica precisa do contrario, "quem vem DEPOIS".
    >>> monta_sucessores({'a': {'depende_de': []}, 'b': {'depende_de': ['a']}})
    {'a': ['b'], 'b': []}
    '''
    sucessores = {}
    for nome in tarefas:
        sucessores[nome] = []
    for nome, tarefa in tarefas.items():
        for dependencia in tarefa['depende_de']:
            sucessores[dependencia].append(nome)
    return sucessores


def ordem_topologica(tarefas):
    '''Uma ordem de execucao em que toda tarefa vem depois das que ela depende.

    Algoritmo de Kahn. A fila eh uma lista mais um indice `proximo` que
    anda (a fila da aula de grafos): nada sai da lista, entao retirar da
    fila custa O(1), e nao O(n) como o fila.pop(0).

    Se sobrar tarefa fora da ordem, eh porque ha dependencia circular
    (A espera B, que espera A): levanta ValueError com as tarefas presas.
    O(V + E).
    >>> ordem_topologica({'a': {'depende_de': []}, 'b': {'depende_de': ['a']}})
    ['a', 'b']
    '''
    sucessores = monta_sucessores(tarefas)
    faltam = {}          # tarefa -> quantas dependencias ainda nao terminaram
    for nome, tarefa in tarefas.items():
        faltam[nome] = len(tarefa['depende_de'])

    fila = []
    for nome in tarefas:
        if faltam[nome] == 0:
            fila.append(nome)
    proximo = 0
    while proximo < len(fila):
        atual = fila[proximo]
        proximo = proximo + 1
        for seguinte in sucessores[atual]:
            faltam[seguinte] = faltam[seguinte] - 1
            if faltam[seguinte] == 0:
                fila.append(seguinte)

    if len(fila) < len(tarefas):
        presas = []
        for nome in tarefas:
            if faltam[nome] > 0:
                presas.append(nome)
        raise ValueError(f"dependencia circular entre as tarefas: {presas}")
    return fila
