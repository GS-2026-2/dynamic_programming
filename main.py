'''
Escola no Prazo - modulo de Dynamic Programming.

Este arquivo eh so a INTERFACE (menu, input e print). Os calculos estao
em cronograma.py, em funcoes puras.

Para rodar:  python main.py
'''

import time

from dados import TAREFAS_EVENTO, gera_cronograma_aleatorio
from cronograma import analisa_cronograma, dias_de_atraso


def mostra_tarefas(tarefas):
    print('\nTAREFAS DO EVENTO')
    for nome, tarefa in tarefas.items():
        dependencias = ', '.join(tarefa['depende_de']) or '(nenhuma)'
        print(f"- {nome}: {tarefa['descricao']}")
        print(f"    {tarefa['duracao']} dia(s) | {tarefa['responsavel']} | depende de: {dependencias}")


def mostra_ordem(tarefas, resultado):
    print('\nORDEM DE EXECUCAO')
    for nome in resultado['ordem']:
        print(f"  dia {resultado['inicio'][nome] + 1:>2} a {resultado['termino'][nome]:>2}"
              f"  {nome} ({tarefas[nome]['responsavel']})")


def mostra_caminho_critico(tarefas, resultado):
    print(f"\nPRAZO MINIMO: {resultado['prazo']} dias uteis")
    print('CAMINHO CRITICO (atrasar qualquer uma destas atrasa o evento):')
    for nome in resultado['caminho']:
        print(f"  -> {nome}: {tarefas[nome]['descricao']} ({tarefas[nome]['responsavel']})")


def pergunta_prazo(resultado):
    dias = int(input('\nQuantos dias uteis faltam ate o evento? '))   # ValueError se nao for numero
    atraso = dias_de_atraso(resultado['prazo'], dias)
    if atraso == 0:
        print('Da tempo.')
    else:
        print(f'NAO da tempo: faltam {atraso} dia(s).')
        print('Priorize o caminho critico:', ', '.join(resultado['caminho']))


def mostra_desempenho():
    print('\nTEMPO DO CALCULO (cronogramas simulados)')
    print(f"{'tarefas':>8} {'segundos':>10}")
    for quantidade in [1000, 2000, 4000, 8000, 16000]:
        tarefas = gera_cronograma_aleatorio(quantidade)
        comeco = time.perf_counter()
        analisa_cronograma(tarefas)
        fim = time.perf_counter()
        print(f'{quantidade:>8} {fim - comeco:>10.4f}')
    print('Dobrar as tarefas ~dobra o tempo: O(V + E).')


def menu():
    tarefas = TAREFAS_EVENTO
    resultado = analisa_cronograma(tarefas)
    while True:
        print('\n=== ESCOLA NO PRAZO - apresentacao de boas praticas ===')
        print('1 - Ver tarefas e dependencias')
        print('2 - Ordem de execucao')
        print('3 - Caminho critico e prazo minimo')
        print('4 - Da tempo ate o evento?')
        print('5 - Tempo do calculo')
        print('0 - Sair')
        escolha = input('Opcao: ').strip()
        try:
            if escolha == '1':
                mostra_tarefas(tarefas)
            elif escolha == '2':
                mostra_ordem(tarefas, resultado)
            elif escolha == '3':
                mostra_caminho_critico(tarefas, resultado)
            elif escolha == '4':
                pergunta_prazo(resultado)
            elif escolha == '5':
                mostra_desempenho()
            elif escolha == '0':
                break
            else:
                print('Opcao invalida.')
        except ValueError as erro:
            print(f'Entrada invalida: {erro}')


if __name__ == '__main__':
    try:
        menu()
    except ValueError as erro:
        print(f'Erro nos dados do cronograma: {erro}')
    except (KeyboardInterrupt, EOFError):
        print('\nEncerrado.')
