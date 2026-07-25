# Risco de concentração de receita

**Área:** Finanças · **Apurado em:** 2026-07-24 · **Fonte:** Stripe (livemode)

> Este é o achado mais relevante da apuração de Finanças de julho/2026. Nenhuma decisão
> de aquisição, precificação ou retenção deveria ser tomada sem ele na mesa.

## O fato

**1 cliente (plano Exclusive, ~R$5.000/mês) representa ~85% do MRR.**

Faturamento observado:

| Período | Faturado | Faturas pagas |
|---|---|---|
| Jun/2026 (fechado) | R$ 6.895,10 | 13 |
| Jul/2026 (parcial até 24/jul) | R$ 7.107,22 | 11 |

Ou seja: tirando o Exclusive, a operação inteira — todos os demais clientes somados —
gira em torno de **~R$1.000 a R$2.000/mês**.

## Por que isso importa

1. **A saída desse cliente não é churn, é evento de sobrevivência.** Um único cancelamento
   derruba ~85% da receita recorrente. Não existe volume na cauda para absorver.
2. **Todas as métricas agregadas estão distorcidas.** ARPU, MRR médio, LTV e "crescimento
   mês a mês" calculados sobre a base inteira descrevem majoritariamente um cliente só.
   Por isso o CAC-teto foi calculado sobre o **ARPU SMB (R$349)**, e não sobre o ARPU da
   base — ver [cac-teto-e-budget-de-aquisicao.md](cac-teto-e-budget-de-aquisicao.md).
3. **Aquisição deixa de ser opcional.** O caminho para reduzir o risco não é reter melhor
   o Exclusive (isso é gestão de conta, não estrutura) — é ter mais clientes SMB pagantes.
   A verba de aquisição existe por causa deste número.

## O que fazer com isso

- **Monitorar como item de risco, não como métrica.** Qualquer sinal de insatisfação,
  atraso de pagamento ou queda de uso desse cliente é prioridade máxima e imediata.
- **Reportar MRR sempre em duas linhas:** MRR total e MRR ex-Exclusive. A segunda linha é
  a que mede se o negócio está crescendo.
- **Meta implícita de diversificação:** o risco só cai de verdade quando nenhum cliente
  isolado passa de ~30% do MRR. Isso é uma questão de anos de aquisição SMB, não de trimestre.

## Como foi apurado

Faturas pagas no Stripe (livemode) agregadas por mês de pagamento, cruzadas com os planos
das assinaturas ativas. A concentração aparece diretamente ao ordenar as faturas por valor:
o Exclusive responde sozinho por praticamente toda a diferença entre o total e a soma dos
planos SMB (R$79–R$499).
