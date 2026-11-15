'''
Escola no Prazo - modulo de Dynamic Programming.

Este arquivo eh so a INTERFACE (menu, input e print). Os calculos estao
em grafo.py e caminho_critico.py, em funcoes puras.

Para rodar:  python main.py
'''

from dados import TAREFAS_EVENTO
from caminho_critico import analisa_cronograma, verifica_prazo
from desempenho import mede_escalabilidade, compara_com_e_sem_memo


def mostra_tarefas(tarefas):
    print('\nTAREFAS DO EVENTO')
    for nome, tarefa in tarefas.items():
        dependencias = ', '.join(tarefa['depende_de']) or '(nenhuma)'
        print(f"- {nome}: {tarefa['descricao']}")
        print(f"    {tarefa['duracao']} dia(s) | {tarefa['responsavel']} | depende de: {dependencias}")


def mostra_ordem(tarefas, resultado):
    print('\nORDEM DE EXECUCAO (cada tarefa so comeca depois das que ela depende)')
    for nome in resultado['ordem']:
        print(f"  dia {resultado['inicio'][nome] + 1:>2} a {resultado['termino'][nome]:>2}"
              f"  {nome} ({tarefas[nome]['responsavel']})")


def mostra_caminho_critico(tarefas, resultado):
    print(f"\nPRAZO MINIMO: {resultado['prazo']} dias uteis")
    print('CAMINHO CRITICO (atrasar qualquer uma destas atrasa o evento):')
    for nome in resultado['caminho']:
        print(f"  -> {nome}: {tarefas[nome]['descricao']} ({tarefas[nome]['responsavel']})")


def mostra_folgas(resultado):
    print('\nFOLGA DE CADA TAREFA (quantos dias pode atrasar sem atrasar o evento)')
    for nome in resultado['ordem']:
        folga = resultado['folgas'][nome]
        marca = '  <- critica' if folga == 0 else ''
        print(f"  {nome:<22} {folga} dia(s){marca}")


def pergunta_prazo(resultado):
    texto = input('\nQuantos dias uteis faltam ate o evento? ')
    dias = int(texto)                       # ValueError se nao for numero
    situacao = verifica_prazo(resultado, dias)
    if situacao['cabe']:
        print(f"Da tempo. Sobram {situacao['dias_de_sobra']} dia(s) de margem.")
    else:
        print(f"NAO da tempo: faltam {situacao['dias_de_atraso']} dia(s).")
        print('Priorize as tarefas do caminho critico:', ', '.join(resultado['caminho']))


def mostra_desempenho():
    print('\nESCALABILIDADE (tempo em segundos)')
    print(f"{'tarefas':>8} {'arestas':>8} {'tabulacao':>10} {'memoizacao':>11} {'iguais':>7}")
    for linha in mede_escalabilidade([1000, 2000, 4000, 8000, 16000]):
        print(f"{linha['tarefas']:>8} {linha['arestas']:>8} {linha['tempo_tabulacao']:>10.4f}"
              f" {linha['tempo_memoizacao']:>11.4f} {str(linha['mesmo_prazo']):>7}")
    print('Dobrar as tarefas ~dobra o tempo: O(V + E).')

    print('\nRECURSAO SEM CACHE x COM CACHE (cronograma em escada)')
    print(f"{'tarefas':>8} {'chamadas sem memo':>18} {'sem memo (s)':>13} {'com memo (s)':>13}")
    for linha in compara_com_e_sem_memo([16, 18, 20, 22, 24]):
        print(f"{linha['tarefas']:>8} {linha['chamadas_sem_memo']:>18} "
              f"{linha['tempo_sem_memo']:>13.4f} {linha['tempo_com_memo']:>13.6f}")
    print('Sem cache as chamadas crescem como o fibonacci; com cache, cada tarefa eh calculada uma vez.')


def menu():
    tarefas = TAREFAS_EVENTO
    resultado = analisa_cronograma(tarefas)
    opcoes = {
        '1': ('Ver tarefas e dependencias', lambda: mostra_tarefas(tarefas)),
        '2': ('Ordem de execucao', lambda: mostra_ordem(tarefas, resultado)),
        '3': ('Caminho critico e prazo minimo', lambda: mostra_caminho_critico(tarefas, resultado)),
        '4': ('Folga de cada tarefa', lambda: mostra_folgas(resultado)),
        '5': ('Da tempo ate o evento?', lambda: pergunta_prazo(resultado)),
        '6': ('Analise de desempenho', mostra_desempenho),
    }
    while True:
        print('\n=== ESCOLA NO PRAZO - apresentacao de boas praticas ===')
        for chave, (texto, _) in opcoes.items():
            print(f'{chave} - {texto}')
        print('0 - Sair')
        escolha = input('Opcao: ').strip()
        if escolha == '0':
            break
        if escolha not in opcoes:
            print('Opcao invalida.')
            continue
        try:
            opcoes[escolha][1]()
        except ValueError as erro:
            print(f'Entrada invalida: {erro}')


if __name__ == '__main__':
    try:
        menu()
    except ValueError as erro:
        print(f'Erro nos dados do cronograma: {erro}')
    except (KeyboardInterrupt, EOFError):
        print('\nEncerrado.')
