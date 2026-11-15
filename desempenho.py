'''
Analise pratica de eficiencia: medicao de tempo com time.perf_counter,
como no "Tempo do fibonacci" da apostila.

Duas medicoes:
1. Escalabilidade: o caminho critico (tabulacao e memoizacao) em
   cronogramas cada vez maiores. Se o algoritmo eh O(V + E), dobrar o
   numero de tarefas deve, mais ou menos, dobrar o tempo.
2. Por que memoizar: a mesma recorrencia SEM cache, num cronograma em
   "escada" (cada tarefa depende das duas anteriores). Sem cache ela
   recalcula os mesmos subproblemas e cresce como o fibonacci recursivo.

Os cronogramas aqui sao gerados aleatoriamente (com semente fixa, para o
resultado ser reproduzivel): servem so para medir tempo.
'''

import random
import time

from caminho_critico import analisa_cronograma, calcula_terminos_memo


def gera_cronograma_aleatorio(quantidade, max_dependencias=3, janela=50, semente=42):
    '''Cronograma sem ciclos com `quantidade` tarefas.

    A tarefa i so depende de tarefas com numero menor que i (de uma janela
    das `janela` anteriores), o que garante que nao ha ciclo. Assim
    E <= 3V e o tamanho do grafo cresce junto com V.
    '''
    sorteio = random.Random(semente)
    tarefas = {}
    for i in range(quantidade):
        dependencias = []
        if i > 0:
            primeira_possivel = max(0, i - janela)
            candidatas = list(range(primeira_possivel, i))
            quantas = sorteio.randint(0, min(max_dependencias, len(candidatas)))
            for j in sorteio.sample(candidatas, quantas):
                dependencias.append(f'T{j}')
        tarefas[f'T{i}'] = {'descricao': f'tarefa {i}', 'duracao': sorteio.randint(1, 5),
                            'responsavel': 'simulado', 'depende_de': dependencias}
    return tarefas


def gera_escada(quantidade):
    '''Cada tarefa depende das duas anteriores (formato do fibonacci).'''
    tarefas = {}
    for i in range(quantidade):
        dependencias = []
        if i >= 1:
            dependencias.append(f'T{i - 1}')
        if i >= 2:
            dependencias.append(f'T{i - 2}')
        tarefas[f'T{i}'] = {'descricao': f'tarefa {i}', 'duracao': 1,
                            'responsavel': 'simulado', 'depende_de': dependencias}
    return tarefas


def termino_sem_memo(tarefas, nome, contador):
    '''A mesma recorrencia do termino_memo, mas SEM cache.

    `contador` conta quantas vezes a funcao foi chamada (como o medidor
    do conta_maneiras_medida da apostila). Existe so para comparacao.
    '''
    contador['chamadas'] = contador['chamadas'] + 1
    inicio = 0
    for dependencia in tarefas[nome]['depende_de']:
        termino_dep = termino_sem_memo(tarefas, dependencia, contador)
        if termino_dep > inicio:
            inicio = termino_dep
    return inicio + tarefas[nome]['duracao']


def mede_tempo(funcao, *argumentos):
    '''Executa a funcao e devolve (resultado, segundos gastos).'''
    comeco = time.perf_counter()
    resultado = funcao(*argumentos)
    fim = time.perf_counter()
    return resultado, fim - comeco


def mede_escalabilidade(tamanhos):
    '''Tempo da tabulacao e da memoizacao para cada tamanho de cronograma.

    Devolve uma lista de dicionarios, um por tamanho, sem imprimir nada.
    '''
    linhas = []
    for quantidade in tamanhos:
        tarefas = gera_cronograma_aleatorio(quantidade)
        arestas = 0
        for tarefa in tarefas.values():
            arestas = arestas + len(tarefa['depende_de'])
        resultado, tempo_tabela = mede_tempo(analisa_cronograma, tarefas)
        terminos, tempo_memo = mede_tempo(calcula_terminos_memo, tarefas)
        linhas.append({'tarefas': quantidade, 'arestas': arestas,
                       'tempo_tabulacao': tempo_tabela, 'tempo_memoizacao': tempo_memo,
                       'mesmo_prazo': max(terminos.values()) == resultado['prazo']})
    return linhas


def compara_com_e_sem_memo(tamanhos):
    '''Chamadas e tempo da recursao sem cache x com cache, na escada.'''
    linhas = []
    for quantidade in tamanhos:
        tarefas = gera_escada(quantidade)
        ultima = f'T{quantidade - 1}'
        contador = {'chamadas': 0}
        sem_memo, tempo_sem = mede_tempo(termino_sem_memo, tarefas, ultima, contador)
        com_memo, tempo_com = mede_tempo(calcula_terminos_memo, tarefas)
        linhas.append({'tarefas': quantidade, 'chamadas_sem_memo': contador['chamadas'],
                       'tempo_sem_memo': tempo_sem, 'tempo_com_memo': tempo_com,
                       'mesmo_resultado': sem_memo == com_memo[ultima]})
    return linhas
