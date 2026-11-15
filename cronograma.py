'''
Funcoes PURAS do cronograma (nao fazem print nem input).

As tarefas formam um grafo dirigido: existe uma aresta A -> B quando a
tarefa B depende da tarefa A. Com esse grafo calculamos:
1. a ordem de execucao (ordenacao topologica, algoritmo de Kahn);
2. o dia em que cada tarefa termina, por TABULACAO (programacao dinamica);
3. o caminho critico: as tarefas que determinam o prazo final.
'''


def valida_tarefas(tarefas):
    '''Levanta ValueError se alguma tarefa tiver duracao invalida ou
    depender de uma tarefa que nao existe. O(V + E).'''
    for nome, tarefa in tarefas.items():
        if not isinstance(tarefa['duracao'], int) or tarefa['duracao'] <= 0:
            raise ValueError(f"tarefa '{nome}': duracao deve ser inteiro positivo")
        for dependencia in tarefa['depende_de']:
            if dependencia not in tarefas:
                raise ValueError(f"tarefa '{nome}' depende de '{dependencia}', que nao existe")


def ordem_topologica(tarefas):
    '''Ordem em que toda tarefa vem depois das que ela depende (Kahn).

    A fila eh uma lista com o indice `proximo` (a fila da aula): nada sai
    da lista, entao retirar custa O(1), e nao O(n) como o fila.pop(0).
    Se sobrar tarefa fora da ordem, ha dependencia circular. O(V + E).
    >>> ordem_topologica({'a': {'depende_de': []}, 'b': {'depende_de': ['a']}})
    ['a', 'b']
    '''
    sucessores = {}      # tarefa -> tarefas que dependem dela
    faltam = {}          # tarefa -> quantas dependencias ainda nao terminaram
    for nome in tarefas:
        sucessores[nome] = []
    for nome, tarefa in tarefas.items():
        faltam[nome] = len(tarefa['depende_de'])
        for dependencia in tarefa['depende_de']:
            sucessores[dependencia].append(nome)

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
        raise ValueError('dependencia circular entre as tarefas')
    return fila


def calcula_tabela(tarefas, ordem):
    '''Tabulacao: inicio e termino mais cedo de cada tarefa.

    Recorrencia:
        inicio(t)  = maior termino entre as dependencias de t (0 se nao tem)
        termino(t) = inicio(t) + duracao(t)
    Seguindo a ordem topologica, as dependencias de uma tarefa ja estao na
    tabela quando chegamos nela, entao cada valor eh calculado uma vez so.
    `veio_de` guarda a dependencia que segura o inicio da tarefa: eh por
    ela que o caminho critico eh remontado. O(V + E).
    '''
    inicio = {}
    termino = {}
    veio_de = {}
    for nome in ordem:
        inicio[nome] = 0
        veio_de[nome] = None
        for dependencia in tarefas[nome]['depende_de']:
            if termino[dependencia] > inicio[nome]:
                inicio[nome] = termino[dependencia]
                veio_de[nome] = dependencia
        termino[nome] = inicio[nome] + tarefas[nome]['duracao']
    return inicio, termino, veio_de


def caminho_critico(termino, veio_de):
    '''Da tarefa que termina por ultimo, volta pelo `veio_de` ate o
    comeco e inverte. O(V).'''
    if termino == {}:
        return []
    atual = max(termino, key=termino.get)
    caminho = []
    while atual is not None:
        caminho.append(atual)
        atual = veio_de[atual]
    caminho.reverse()
    return caminho


def analisa_cronograma(tarefas):
    '''Junta tudo. Devolve ordem, inicio, termino, prazo e caminho critico.'''
    valida_tarefas(tarefas)
    ordem = ordem_topologica(tarefas)
    inicio, termino, veio_de = calcula_tabela(tarefas, ordem)
    prazo = max(termino.values(), default=0)
    return {'ordem': ordem, 'inicio': inicio, 'termino': termino,
            'prazo': prazo, 'caminho': caminho_critico(termino, veio_de)}


def dias_de_atraso(prazo, dias_disponiveis):
    '''Quantos dias faltam para caber no tempo disponivel (0 = da tempo).'''
    if dias_disponiveis < 0:
        raise ValueError('dias disponiveis nao pode ser negativo')
    return max(0, prazo - dias_disponiveis)
