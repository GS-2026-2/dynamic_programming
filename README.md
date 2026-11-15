# Escola no Prazo — Dynamic Programming

## Ficha da CitizenTech

| Campo | Resposta |
| --- | --- |
| **Nome da CitizenTech** | Escola no Prazo |
| **Cidade e bairro** | São Paulo (SP), Bela Vista — escola pública estadual da região da Paulista |
| **Cidadão beneficiado** | Direção e coordenação de escolas públicas e, por consequência, professores e alunos que participam das atividades da escola |
| **Problema, em uma frase** | Avisos chegam tarde e as demandas da escola não têm prazo, responsável nem ordem clara, e por isso a escola atrasa ou perde atividades como a participação em eventos |
| **Como funciona** | A escola transforma cada solicitação em tarefas com prazo, responsável e dependências, acompanha o recebimento dos comunicados e a execução, e o sistema mostra quais tarefas determinam o prazo final |
| **O que cada parte faz** | **Agile:** personas, telas de demandas e cronograma, backlog e pitch · **AR-VR:** simulação 3D da preparação de um evento escolar · **Data Science:** regressão linear (tempo para concluir uma demanda) e logística (probabilidade de atraso) · **Database:** demanda, tarefa, responsável, dependência, comunicado e confirmação de recebimento · **Java:** API de demandas e tarefas · **Dynamic Programming:** grafo de dependências e caminho crítico · **Network:** rede da escola com setores administrativos, público e servidores |
| **Link do repositório** | https://github.com/GS-2026-2/dynamic_programming |
| **Indicador de impacto** | Percentual de tarefas concluídas dentro do prazo e dias de atraso em relação à data do evento, medidos no acompanhamento interno da escola |
| **ODS conectados** | **ODS 4 – Educação de qualidade:** a escola deixa de perder eventos e atividades por falta de organização · **ODS 9 – Indústria, inovação e infraestrutura:** digitaliza a gestão de demandas da escola pública |

## Integrantes

| RM | Nome |
| --- | --- |
| 561805 | Vítor Silva Borsato |
| 561602 | João Pedro Godinho Passiani |
| 562082 | Gabriel Molinari Droppa |
| 565988 | Isabela de Deus |
| 564805 | Thomaz Vasconcelos Mendes |

## O que esta parte resolve

O MVP da Escola no Prazo é **organizar a participação da escola em uma apresentação de boas práticas**. São 11 tarefas (registrar o convite, aprovar, escolher a prática, selecionar a equipe, coletar autorizações, preparar o material, pedir transporte, ensaiar, inscrever, confirmar a logística e apresentar), e várias dependem de outras.

O programa responde: **em que ordem fazer as tarefas, qual o prazo mínimo e quais tarefas determinam esse prazo** (o caminho crítico). Quando o aviso chega tarde, ele também diz se ainda dá tempo.

## Algoritmos abordados

Técnicas da lista do professor usadas: **grafos** e **tabulação**.

1. **Grafo dirigido de dependências.** Cada tarefa é um vértice; existe uma aresta A → B quando B depende de A. O grafo fica em dicionários (`dados.py`).

2. **Ordenação topológica (algoritmo de Kahn)** — `ordem_topologica` em `cronograma.py`. Começa pelas tarefas que não dependem de ninguém; cada tarefa retirada da fila "libera" as que dependiam dela. A fila é uma **lista com o índice `proximo`** (a fila vista em aula), então retirar custa O(1), e não O(n) como `fila.pop(0)`. Se sobrar tarefa fora da ordem, há **dependência circular** e o programa avisa.

3. **Caminho crítico por tabulação** — `calcula_tabela` e `caminho_critico`. A recorrência é:

   ```
   inicio(t)  = maior termino entre as dependências de t   (0 se não tem dependência)
   termino(t) = inicio(t) + duracao(t)
   ```

   A tabela é preenchida na ordem topológica, então quando o programa chega numa tarefa as dependências dela já estão calculadas e cada valor é calculado uma vez só. O prazo mínimo é o maior `termino`. A tabela guarda também `veio_de`, a dependência que termina por último e segura o início de cada tarefa; voltando por ela a partir da última tarefa, o programa remonta o caminho crítico.

## Funcionalidades implementadas (menu do `main.py`)

1. **Ver tarefas e dependências:** descrição, duração, setor responsável e de quem cada tarefa depende.
2. **Ordem de execução:** em que dia cada tarefa começa e termina.
3. **Caminho crítico e prazo mínimo:** as tarefas que, se atrasarem, atrasam o evento. No MVP, o prazo mínimo é de 13 dias úteis.
4. **Dá tempo até o evento?:** recebe quantos dias faltam e responde se cabe; se não couber, diz quantos dias faltam e quais tarefas priorizar.
5. **Tempo do cálculo:** mede o tempo do algoritmo em cronogramas cada vez maiores.

O programa recusa dados inválidos: dependência circular, dependência de tarefa inexistente e duração inválida.

## Eficiência

**Análise teórica** (V = tarefas, E = dependências):

| Função | Complexidade | Por quê |
| --- | --- | --- |
| `valida_tarefas` | O(V + E) | olha cada tarefa e cada dependência uma vez |
| `ordem_topologica` | O(V + E) | cada tarefa entra e sai da fila uma vez, cada dependência é vista uma vez, e a fila com `proximo` retira em O(1) |
| `calcula_tabela` | O(V + E) | uma passada na ordem topológica; o acesso ao dicionário é O(1) |
| `caminho_critico` | O(V) | volta pelo `veio_de` |

O total é **O(V + E)**. Testar todos os caminhos possíveis entre as tarefas, sem a tabela, pode ser exponencial; com a tabela, cada tarefa é calculada uma vez.

**Análise prática** (opção 5 do menu, medida com `time.perf_counter`). Resultado de uma execução:

| tarefas | segundos |
| ---: | ---: |
| 1000 | 0.0009 |
| 2000 | 0.0018 |
| 4000 | 0.0037 |
| 8000 | 0.0080 |
| 16000 | 0.0200 |

Dobrar o número de tarefas praticamente dobra o tempo: o crescimento é linear, como a análise teórica previu.

## Estrutura do código

| Arquivo | Conteúdo |
| --- | --- |
| `main.py` | interface: menu, `input` e `print`, com `try/except` para entradas inválidas |
| `cronograma.py` | funções puras: validação, ordenação topológica, tabulação e caminho crítico |
| `dados.py` | cronograma simulado do MVP e gerador de cronogramas grandes para medir tempo |
| `testes.py` | testes automatizados com `assert` |

As funções de cálculo não fazem `print` nem `input`: recebem dados por parâmetro e devolvem o resultado. Erros de dados são sinalizados com `ValueError` e tratados na interface.

## Como executar

Requer Python 3 (testado no 3.12), sem bibliotecas externas.

```
python main.py      # menu interativo
python testes.py    # testes automatizados
```

## Origem dos dados

Todos os dados são **simulados** pela equipe. As tarefas do MVP representam as etapas típicas de uma escola para participar de um evento externo, e os responsáveis são **setores** da escola, não pessoas. Os cronogramas grandes da medição de tempo são gerados aleatoriamente com semente fixa. Nenhum dado pessoal real é usado.
