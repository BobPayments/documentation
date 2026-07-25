# CAC-teto e budget de aquisição

**Área:** Finanças · **Apurado em:** 2026-07-24 · **Status:** vigente

## O número

**CAC-teto de trabalho: R$100 – R$150 por cliente pagante.**

Teto absoluto de ~R$360 — só liberável se a retenção real confirmar uma vida média maior
que a atual. **Não use R$360 como meta de trabalho.**

## Como se chegou nele

| Entrada | Valor | Origem |
|---|---|---|
| ARPU SMB | R$ 349 | média dos planos pagos SMB (R$79–R$499), **excluindo o Exclusive** |
| Margem bruta | 85% | modelo SaaS, custo de infra/processamento |
| Churn mensal | ~27% | Stripe livemode, base histórica |
| Vida média | ~3,6 meses | 1 / 0,27 |

**LTV ≈ 349 × 0,85 × 3,6 ≈ R$1.068.**

Um teto de R$360 é ~1/3 do LTV — a régua clássica LTV:CAC de 3:1. Mas a vida média de
3,6 meses vem de um churn de 27% medido sobre **uma base minúscula**, e uma base pequena
faz o churn oscilar muito. Trabalhar em **R$100–150** dá margem para o número piorar sem
que a aquisição vire prejuízo. É um teto conservador de propósito.

## O erro que foi corrigido — não repita

Havia um CAC-teto anterior de **R$62**, e ele estava **errado**: o ARPU tinha sido
calculado sobre *todas* as assinaturas, incluindo **13 trials de R$0** que nunca pagaram.
Média com R$0 no denominador derruba o ARPU e derruba o teto junto.

**Regra:** CAC-teto se calcula sobre **pagantes reais**. Trial não pagante não entra em
ARPU — ele entra na taxa de conversão de trial, que é outra métrica.

E, pela outra ponta, o ARPU também **exclui o cliente Exclusive** — incluí-lo inflaria o
ARPU para algo que nenhum cliente adquirido por mídia paga. Ver
[risco-de-concentracao-de-receita.md](risco-de-concentracao-de-receita.md).

## Budget recomendado

| Cenário | Verba | Uso |
|---|---|---|
| **Conservador (recomendado)** | **R$25/dia** | teste de canal |
| Agressivo | R$60/dia | só após o canal provar CAC dentro do teto |

## Implicação para leitura de testes de canal

A R$25/dia, **uma semana de teste custa R$175 — aproximadamente 1 CAC-teto**.

Isso significa que o teste inteiro compra o equivalente a **um** cliente. Portanto
**"0 ou 1 cadastro em uma semana" é amostra pequena, não fracasso do canal** — é
exatamente o resultado que a matemática prevê mesmo num canal saudável.

Um teste de R$175 não tem poder estatístico para condenar um canal. Para que um número
de cadastros signifique alguma coisa, é preciso ou mais verba, ou mais tempo, ou olhar
métricas intermediárias (CPC, CTR, custo por clique qualificado, taxa de landing) em vez
do número de cadastros.

**Consequência operacional:** não matar canal no dia 7 com base em contagem de cadastros.
