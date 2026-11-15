'''
Dados SIMULADOS do MVP da Escola no Prazo: organizar a participacao da
escola em uma apresentacao de boas praticas da Diretoria de Ensino.

Nenhum dado pessoal real: os responsaveis sao SETORES da escola, nao
pessoas. As tarefas e duracoes foram montadas pela equipe a partir das
etapas que uma escola costuma cumprir para levar um projeto a um evento
externo (convite, autorizacoes, transporte, ensaio, inscricao).

Cada tarefa eh um dicionario:
    'descricao'   -> o que precisa ser feito
    'duracao'     -> dias uteis necessarios
    'responsavel' -> setor da escola
    'depende_de'  -> lista das tarefas que precisam terminar ANTES dela

As dependencias formam um grafo dirigido: existe uma aresta A -> B
quando B depende de A.
'''

import random


def gera_cronograma_aleatorio(quantidade, semente=42):
    '''Cronograma grande, sem ciclos, so para medir tempo.

    A tarefa i depende de ate 3 tarefas sorteadas entre as 50 anteriores,
    entao nunca ha ciclo. Semente fixa: o resultado eh sempre o mesmo.
    '''
    sorteio = random.Random(semente)
    tarefas = {}
    for i in range(quantidade):
        candidatas = list(range(max(0, i - 50), i))
        escolhidas = sorteio.sample(candidatas, min(len(candidatas), sorteio.randint(0, 3)))
        tarefas[f'T{i}'] = {'descricao': f'tarefa {i}', 'duracao': sorteio.randint(1, 5),
                            'responsavel': 'simulado',
                            'depende_de': [f'T{j}' for j in escolhidas]}
    return tarefas


TAREFAS_EVENTO = {
    'receber_convite': {
        'descricao': 'Registrar o convite da Diretoria de Ensino',
        'duracao': 1,
        'responsavel': 'Secretaria',
        'depende_de': [],
    },
    'definir_pratica': {
        'descricao': 'Escolher a boa pratica que sera apresentada',
        'duracao': 2,
        'responsavel': 'Coordenacao',
        'depende_de': ['receber_convite'],
    },
    'aprovar_participacao': {
        'descricao': 'Direcao aprova a participacao da escola',
        'duracao': 1,
        'responsavel': 'Direcao',
        'depende_de': ['receber_convite'],
    },
    'selecionar_equipe': {
        'descricao': 'Selecionar professores e alunos participantes',
        'duracao': 2,
        'responsavel': 'Coordenacao',
        'depende_de': ['definir_pratica', 'aprovar_participacao'],
    },
    'enviar_inscricao': {
        'descricao': 'Enviar a inscricao para a Diretoria de Ensino',
        'duracao': 1,
        'responsavel': 'Secretaria',
        'depende_de': ['definir_pratica', 'aprovar_participacao'],
    },
    'solicitar_transporte': {
        'descricao': 'Solicitar o transporte para o dia do evento',
        'duracao': 3,
        'responsavel': 'Administrativo',
        'depende_de': ['aprovar_participacao'],
    },
    'coletar_autorizacoes': {
        'descricao': 'Coletar autorizacoes dos responsaveis pelos alunos',
        'duracao': 4,
        'responsavel': 'Secretaria',
        'depende_de': ['selecionar_equipe'],
    },
    'preparar_material': {
        'descricao': 'Preparar slides e material da apresentacao',
        'duracao': 5,
        'responsavel': 'Professores',
        'depende_de': ['selecionar_equipe'],
    },
    'ensaio_geral': {
        'descricao': 'Ensaio geral com a equipe',
        'duracao': 1,
        'responsavel': 'Professores',
        'depende_de': ['preparar_material'],
    },
    'confirmar_logistica': {
        'descricao': 'Confirmar transporte, autorizacoes e inscricao',
        'duracao': 1,
        'responsavel': 'Coordenacao',
        'depende_de': ['coletar_autorizacoes', 'solicitar_transporte',
                       'ensaio_geral', 'enviar_inscricao'],
    },
    'apresentacao': {
        'descricao': 'Dia da apresentacao de boas praticas',
        'duracao': 1,
        'responsavel': 'Direcao',
        'depende_de': ['confirmar_logistica'],
    },
}
