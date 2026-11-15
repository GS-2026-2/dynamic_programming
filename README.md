# Escola no Prazo — Dynamic Programming

## Ficha da CitizenTech

| Campo | Resposta |
| --- | --- |
| **Nome da CitizenTech** | Escola no Prazo |
| **Cidade e bairro** | São Paulo (SP), Bela Vista — escola pública estadual da região da Paulista |
| **Cidadão beneficiado** | Direção e coordenação de escolas públicas e, por consequência, professores e alunos que participam das atividades da escola |
| **Problema, em uma frase** | Avisos chegam tarde e as demandas da escola não têm prazo, responsável nem ordem clara, e por isso a escola atrasa ou perde atividades como a participação em eventos |
| **Como funciona** | A escola transforma cada solicitação em tarefas com prazo, responsável e dependências, acompanha o recebimento dos comunicados e a execução, e o sistema mostra quais tarefas determinam o prazo final |
| **O que cada parte faz** | **Agile:** personas de direção e coordenação, telas de demandas, cronograma e acompanhamento, backlog e pitch · **AR-VR:** simulação 3D da preparação de um evento escolar · **Data Science:** regressão linear (tempo para concluir uma demanda) e logística (probabilidade de atraso) · **Database:** demanda, tarefa, responsável, dependência, comunicado e confirmação de recebimento · **Java:** API de demandas e tarefas com status, prazos e validações · **Dynamic Programming:** grafo de dependências e caminho crítico · **Network:** rede da escola com setores administrativos, público e servidores |
| **Link do repositório** | https://github.com/GS-2026-2/dynamic_programming |
| **Indicador de impacto** | Percentual de tarefas concluídas dentro do prazo e dias de atraso em relação à data do evento, medidos no acompanhamento interno (registrar o aviso depois que ele chega não elimina o atraso no envio, então o benefício é medido dentro da escola) |
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

O MVP da Escola no Prazo é **organizar a participação da escola em uma apresentação de boas práticas**. Para isso é preciso cumprir 11 tarefas (registrar o convite, aprovar, escolher a prática, selecionar a equipe, coletar autorizações, preparar o material, pedir transporte, ensaiar, inscrever, confirmar a logística e apresentar), e várias dependem de outras.

A pergunta que a coordenação precisa responder é: **quais tarefas determinam o prazo final, e quanto cada uma pode atrasar sem atrasar o evento?** Quando o aviso chega tarde (o episódio que deu origem ao projeto), a mesma conta responde se ainda dá tempo e onde concentrar o esforço.

## Algoritmos abordados

Os três conceitos da lista do professor aparecem: **grafos**, **memoização** e **tabulação**.

1. **Grafo dirigido de dependências** (`grafo.py`). Cada tarefa é um vértice; existe uma aresta A → B quando B depende de A. O grafo é guardado em dicionários (lista de adjacência), como o metrô da aula.

2. **Ordenação topológica pelo algoritmo de Kahn** (`ordem_topologica`). Coloca na fila as tarefas que não dependem de ninguém; cada tarefa retirada "libera" as que dependiam dela. A fila é uma **lista com o índice `proximo`** (a fila vista em aula), então retirar custa O(1) e não O(n) como `fila.pop(0)`. Se sobrar tarefa fora da ordem, há **dependência circular**, e o programa avisa quais tarefas estão presas.

3. **Caminho crítico por programação dinâmica** (`caminho_critico.py`). A recorrência é:

   ```
   termino(t) = duracao(t) + max( termino(d) para cada d de que t depende )
   termino(t) = duracao(t)        se t não depende de ninguém
   ```

   O prazo mínimo do evento é o maior `termino`. Os subproblemas se repetem (várias tarefas dependem da mesma), por isso a recorrência é resolvida de dois jeitos:
   - **Memoização** (`termino_memo`): a recursão acima com um dicionário de cache. Cada tarefa é calculada uma vez só.
   - **Tabulação** (`calcula_tabela`): preenche a tabela de início e término na ordem topológica, de baixo para cima. Quando chega numa tarefa, as dependências dela já estão na tabela. A tabela também guarda `veio_de`, a dependência que termina por último, e por ela o **caminho crítico** é remontado de trás para frente (como o `veio_de` do metrô).

   Os testes conferem que memoização e tabulação dão **o mesmo resultado**.

4. **Folgas** (`calcula_folgas`). Uma segunda passada da tabulação, de trás para frente na ordem topológica, calcula o início mais tarde de cada tarefa. Folga = início mais tarde − início mais cedo. Folga 0 significa que a tarefa está no caminho crítico.

## Funcionalidades implementadas (menu do `main.py`)

1. **Ver tarefas e dependências:** descrição, duração, setor responsável e de quem depende.
2. **Ordem de execução:** em que ordem fazer as tarefas e em que dia cada uma começa e termina.
3. **Caminho crítico e prazo mínimo:** as tarefas que, se atrasarem, atrasam o evento (no MVP: 13 dias úteis).
4. **Folga de cada tarefa:** quantos dias cada tarefa pode atrasar (ex.: o transporte tem 6 dias de folga, o material da apresentação tem 0).
5. **Dá tempo até o evento?:** recebe quantos dias faltam e responde se cabe; se não couber, diz quantos dias faltam e quais tarefas priorizar.
6. **Análise de desempenho:** mede o tempo do algoritmo em cronogramas grandes.

O programa também **detecta dependência circular**, dependência de tarefa inexistente e duração inválida.

## Eficiência

**Análise teórica.** Com V tarefas e E dependências:

| Função | Complexidade | Por quê |
| --- | --- | --- |
| `valida_tarefas` | O(V + E) | olha cada tarefa e cada dependência uma vez |
| `ordem_topologica` | O(V + E) | cada tarefa entra e sai da fila uma vez; cada aresta é vista uma vez; a fila com `proximo` retira em O(1) |
| `termino_memo` / `calcula_terminos_memo` | O(V + E) | com o cache, cada tarefa é calculada uma vez e cada dependência é consultada uma vez; o `in` do dicionário é O(1) |
| `calcula_tabela` | O(V + E) | uma passada na ordem topológica |
| `calcula_folgas` | O(V + E) | uma passada de trás para frente |
| `caminho_critico` | O(V) | volta pelo `veio_de` |
| `verifica_prazo` | O(1) | uma subtração |

O total é **O(V + E)**. Sem o cache, a mesma recursão recalcula cada tarefa uma vez para cada caminho que chega nela e cresce de forma exponencial, como o Fibonacci recursivo.

**Análise prática** (opção 6 do menu, `desempenho.py`, medida com `time.perf_counter`). Resultado de uma execução:

| tarefas | arestas | tabulação (s) | memoização (s) |
| ---: | ---: | ---: | ---: |
| 1000 | 1566 | 0.0013 | 0.0012 |
| 2000 | 3015 | 0.0027 | 0.0017 |
| 4000 | 6067 | 0.0059 | 0.0034 |
| 8000 | 12030 | 0.0122 | 0.0071 |
| 16000 | 24193 | 0.0295 | 0.0147 |

Dobrar o número de tarefas praticamente dobra o tempo: o comportamento é linear, como a análise previu. A comparação com a recursão **sem** cache, num cronograma em "escada" (cada tarefa depende das duas anteriores), mostra o motivo da memoização: com 24 tarefas são 121.392 chamadas sem cache, contra 24 cálculos com cache.

## Estrutura do código

| Arquivo | Conteúdo |
| --- | --- |
| `main.py` | interface: menu, `input` e `print`, com `try/except` para entradas inválidas |
| `grafo.py` | funções puras do grafo: validação, sucessores e ordenação topológica |
| `caminho_critico.py` | funções puras de programação dinâmica: memoização, tabulação, caminho crítico, folgas e verificação de prazo |
| `desempenho.py` | geração de cronogramas para teste e medição de tempo |
| `dados.py` | cronograma simulado do MVP |
| `testes.py` | testes automatizados com `assert` |
| `prompts.md` | prompts usados com IA |

As funções de cálculo não fazem `print` nem `input`: recebem dados por parâmetro e devolvem o resultado. Erros de dados são sinalizados com `ValueError` e tratados na interface.

## Como executar

Requer Python 3 (testado no 3.12), sem bibliotecas externas.

```
python main.py      # menu interativo
python testes.py    # testes automatizados
```

## Origem dos dados

Todos os dados são **simulados** pela equipe. As tarefas e durações do MVP representam as etapas típicas de uma escola para participar de um evento externo, e os responsáveis são **setores** da escola (Secretaria, Coordenação, Direção, Professores, Administrativo), não pessoas. Os cronogramas grandes da análise de desempenho são gerados aleatoriamente com semente fixa. Nenhum dado pessoal real é usado.

## Uso de IA

Usamos IA como apoio. Os prompts estão em [`prompts.md`](prompts.md).
