'''
Caminho critico do cronograma: quais tarefas determinam o prazo final.

Recorrencia (a "terceirizacao", como no rouba(casa) do House Robber):

    termino(t) = duracao(t) + max( termino(d) para d em depende_de(t) )
    termino(t) = duracao(t)                       se t nao depende de ninguem

O prazo minimo do evento eh o maior termino. Os subproblemas se repetem
(varias tarefas dependem da mesma), entao calculamos de dois jeitos:
- memoizacao: a recursao acima com um dicionario de cache;
- tabulacao: preenchendo a tabela na ordem topologica, de baixo pra cima.
Os dois precisam dar o mesmo resultado (ver testes.py).

Todas as funcoes aqui sao PURAS: recebem dados, devolvem dados.
'''

from grafo import valida_tarefas, ordem_topologica, monta_sucessores


def termino_memo(tarefas, nome, memo):
    '''Dia em que a tarefa `nome` termina, no mais cedo. Versao top-down.

    `memo` eh o cache: cada tarefa eh calculada uma vez so. Sem ele, uma
    tarefa com muitos caminhos ate ela seria recalculada em cada caminho
    (crescimento exponencial, como o fibonacci sem memo).
    So pode ser chamada em grafo SEM ciclo - quem garante eh a
    `calcula_terminos_memo`.
    '''
    if nome in memo:
        return memo[nome]
    tarefa = tarefas[nome]
    inicio = 0
    for dependencia in tarefa['depende_de']:
        termino_dep = termino_memo(tarefas, dependencia, memo)
        if termino_dep > inicio:
            inicio = termino_dep
    memo[nome] = inicio + tarefa['duracao']
    return memo[nome]


def calcula_terminos_memo(tarefas):
    '''Termino mais cedo de TODAS as tarefas, por memoizacao. O(V + E).

    O cache eh criado aqui dentro, a cada chamada: nao sobra cache de um
    cronograma para outro. A ordem topologica eh calculada antes so para
    rejeitar ciclos (que fariam a recursao nunca acabar).
    '''
    valida_tarefas(tarefas)
    ordem_topologica(tarefas)
    memo = {}
    for nome in tarefas:
        termino_memo(tarefas, nome, memo)
    return memo


def calcula_tabela(tarefas, ordem):
    '''Tabulacao (bottom-up): inicio e termino mais cedo de cada tarefa.

    Percorre a ordem topologica: quando chega numa tarefa, as dependencias
    dela ja estao na tabela. Guarda tambem `veio_de`, a dependencia que
    terminou por ultimo - eh ela que segura o inicio da tarefa, e eh por
    ela que o caminho critico eh remontado (como o veio_de do metro).
    O(V + E).
    '''
    inicio = {}
    termino = {}
    veio_de = {}
    for nome in ordem:
        tarefa = tarefas[nome]
        inicio[nome] = 0
        veio_de[nome] = None
        for dependencia in tarefa['depende_de']:
            if termino[dependencia] > inicio[nome]:
                inicio[nome] = termino[dependencia]
                veio_de[nome] = dependencia
        termino[nome] = inicio[nome] + tarefa['duracao']
    return {'inicio': inicio, 'termino': termino, 'veio_de': veio_de}


def prazo_minimo(termino):
    '''Menor numero de dias para concluir tudo: o maior termino. O(V).'''
    maior = 0
    for dia in termino.values():
        if dia > maior:
            maior = dia
    return maior


def caminho_critico(tabela):
    '''As tarefas, em ordem, da cadeia que determina o prazo final.

    Comeca pela tarefa que termina por ultimo e volta pelo `veio_de`
    ate uma tarefa sem dependencias; depois inverte. O(V).
    '''
    termino = tabela['termino']
    if termino == {}:
        return []
    ultima = None
    for nome, dia in termino.items():
        if ultima is None or dia > termino[ultima]:
            ultima = nome
    ao_contrario = []
    atual = ultima
    while atual is not None:
        ao_contrario.append(atual)
        atual = tabela['veio_de'][atual]
    ao_contrario.reverse()
    return ao_contrario


def calcula_folgas(tarefas, ordem, tabela, prazo):
    '''Quantos dias cada tarefa pode atrasar sem atrasar o evento.

    Passada de tras pra frente na ordem topologica (tabulacao de novo):
    o termino mais TARDE de uma tarefa eh o menor inicio mais tarde entre
    as tarefas que dependem dela. Folga = inicio mais tarde - inicio mais
    cedo. Tarefa com folga 0 esta no caminho critico. O(V + E).
    '''
    sucessores = monta_sucessores(tarefas)
    inicio_tarde = {}
    for posicao in range(len(ordem) - 1, -1, -1):
        nome = ordem[posicao]
        termino_tarde = prazo
        for seguinte in sucessores[nome]:
            if inicio_tarde[seguinte] < termino_tarde:
                termino_tarde = inicio_tarde[seguinte]
        inicio_tarde[nome] = termino_tarde - tarefas[nome]['duracao']

    folgas = {}
    for nome in ordem:
        folgas[nome] = inicio_tarde[nome] - tabela['inicio'][nome]
    return folgas


def analisa_cronograma(tarefas):
    '''Junta tudo: ordem, tabela, prazo, caminho critico e folgas.

    Levanta ValueError se os dados forem invalidos ou tiverem ciclo.
    '''
    valida_tarefas(tarefas)
    ordem = ordem_topologica(tarefas)
    tabela = calcula_tabela(tarefas, ordem)
    prazo = prazo_minimo(tabela['termino'])
    return {
        'ordem': ordem,
        'inicio': tabela['inicio'],
        'termino': tabela['termino'],
        'prazo': prazo,
        'caminho': caminho_critico(tabela),
        'folgas': calcula_folgas(tarefas, ordem, tabela, prazo),
    }


def verifica_prazo(resultado, dias_disponiveis):
    '''O cronograma cabe nos dias que faltam ate o evento?

    Responde o caso do aviso que chega atrasado: com os dias que sobraram,
    da tempo? Se nao der, quantos dias faltam. O(1).
    '''
    if dias_disponiveis < 0:
        raise ValueError('dias disponiveis nao pode ser negativo')
    atraso = resultado['prazo'] - dias_disponiveis
    if atraso < 0:
        atraso = 0
    return {'cabe': atraso == 0, 'dias_de_atraso': atraso,
            'dias_de_sobra': max(0, dias_disponiveis - resultado['prazo'])}
