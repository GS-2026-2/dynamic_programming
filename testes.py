'''
Testes automatizados com assert, no estilo da apostila.
Para rodar:  python testes.py
'''

from dados import TAREFAS_EVENTO
from grafo import valida_tarefas, monta_sucessores, ordem_topologica
from caminho_critico import (analisa_cronograma, calcula_terminos_memo,
                             verifica_prazo)
from desempenho import (gera_cronograma_aleatorio, gera_escada,
                        termino_sem_memo)


def tarefa(duracao, depende_de):
    return {'descricao': '', 'duracao': duracao, 'responsavel': '', 'depende_de': depende_de}


def ocorre_erro(funcao, *argumentos):
    '''True se a funcao levanta ValueError com esses argumentos.'''
    try:
        funcao(*argumentos)
    except ValueError:
        return True
    return False


# --- grafo ---
pequeno = {'a': tarefa(2, []), 'b': tarefa(3, ['a']), 'c': tarefa(1, ['a']),
           'd': tarefa(4, ['b', 'c'])}
assert monta_sucessores(pequeno) == {'a': ['b', 'c'], 'b': ['d'], 'c': ['d'], 'd': []}
assert ordem_topologica(pequeno) == ['a', 'b', 'c', 'd']
assert ordem_topologica({}) == []

ciclo = {'a': tarefa(1, ['c']), 'b': tarefa(1, ['a']), 'c': tarefa(1, ['b']), 'd': tarefa(1, [])}
assert ocorre_erro(ordem_topologica, ciclo)
assert ocorre_erro(valida_tarefas, {'a': tarefa(1, ['x'])})      # dependencia inexistente
assert ocorre_erro(valida_tarefas, {'a': tarefa(0, [])})         # duracao invalida
assert ocorre_erro(valida_tarefas, {'a': tarefa(1, ['a'])})      # depende de si mesma

# --- caminho critico no grafo pequeno ---
# a: 0-2, b: 2-5, c: 2-3, d: 5-9  -> prazo 9, critico a-b-d, c tem 2 de folga
r = analisa_cronograma(pequeno)
assert r['prazo'] == 9
assert r['caminho'] == ['a', 'b', 'd']
assert r['folgas'] == {'a': 0, 'b': 0, 'c': 2, 'd': 0}
assert r['inicio']['d'] == 5

# --- MVP: apresentacao de boas praticas ---
r = analisa_cronograma(TAREFAS_EVENTO)
assert r['prazo'] == 13
assert r['caminho'] == ['receber_convite', 'definir_pratica', 'selecionar_equipe',
                        'preparar_material', 'ensaio_geral', 'confirmar_logistica',
                        'apresentacao']
for nome in r['caminho']:
    assert r['folgas'][nome] == 0
assert r['folgas']['solicitar_transporte'] == 6
assert r['folgas']['coletar_autorizacoes'] == 2
assert verifica_prazo(r, 15) == {'cabe': True, 'dias_de_atraso': 0, 'dias_de_sobra': 2}
assert verifica_prazo(r, 10) == {'cabe': False, 'dias_de_atraso': 3, 'dias_de_sobra': 0}
assert ocorre_erro(verifica_prazo, r, -1)

# --- memoizacao e tabulacao dao o mesmo resultado ---
for exemplo in [pequeno, TAREFAS_EVENTO, gera_cronograma_aleatorio(500, semente=7),
                gera_cronograma_aleatorio(2000, semente=3)]:
    assert calcula_terminos_memo(exemplo) == analisa_cronograma(exemplo)['termino']
assert ocorre_erro(calcula_terminos_memo, ciclo)

# --- sem memo: mesmo resultado, muito mais chamadas ---
escada = gera_escada(15)
contador = {'chamadas': 0}
assert termino_sem_memo(escada, 'T14', contador) == calcula_terminos_memo(escada)['T14'] == 15
assert contador['chamadas'] > 1000           # com memo seriam 15 calculos

print('todos os testes passaram')
