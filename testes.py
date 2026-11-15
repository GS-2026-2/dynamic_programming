'''
Testes com assert, no estilo da apostila.
Para rodar:  python testes.py
'''

from dados import TAREFAS_EVENTO, gera_cronograma_aleatorio
from cronograma import ordem_topologica, analisa_cronograma, dias_de_atraso


def tarefa(duracao, depende_de):
    return {'descricao': '', 'duracao': duracao, 'responsavel': '', 'depende_de': depende_de}


def da_erro(funcao, *argumentos):
    try:
        funcao(*argumentos)
    except ValueError:
        return True
    return False


# grafo pequeno: a (0-2), b (2-5), c (2-3), d (5-9)
pequeno = {'a': tarefa(2, []), 'b': tarefa(3, ['a']), 'c': tarefa(1, ['a']), 'd': tarefa(4, ['b', 'c'])}
assert ordem_topologica(pequeno) == ['a', 'b', 'c', 'd']
r = analisa_cronograma(pequeno)
assert r['prazo'] == 9
assert r['inicio']['d'] == 5
assert r['caminho'] == ['a', 'b', 'd']

# dados invalidos
assert da_erro(analisa_cronograma, {'a': tarefa(1, ['b']), 'b': tarefa(1, ['a'])})   # ciclo
assert da_erro(analisa_cronograma, {'a': tarefa(1, ['x'])})                          # nao existe
assert da_erro(analisa_cronograma, {'a': tarefa(0, [])})                             # duracao 0
assert analisa_cronograma({})['prazo'] == 0

# MVP: apresentacao de boas praticas
r = analisa_cronograma(TAREFAS_EVENTO)
assert r['prazo'] == 13
assert r['caminho'] == ['receber_convite', 'definir_pratica', 'selecionar_equipe',
                        'preparar_material', 'ensaio_geral', 'confirmar_logistica', 'apresentacao']
assert dias_de_atraso(13, 15) == 0
assert dias_de_atraso(13, 10) == 3
assert da_erro(dias_de_atraso, 13, -1)

# cronograma grande: toda tarefa comeca depois de todas as suas dependencias
grande = gera_cronograma_aleatorio(3000)
r = analisa_cronograma(grande)
for nome, t in grande.items():
    for dependencia in t['depende_de']:
        assert r['inicio'][nome] >= r['termino'][dependencia]
assert r['prazo'] == r['termino'][r['caminho'][-1]]

print('todos os testes passaram')
