# Finanças — Bob Payments

Apurações da área de Finanças. Tudo aqui foi verificado contra dados reais do Stripe
livemode e do banco de produção em **2026-07-24**, salvo indicação em contrário.

## Documentos

- **[Risco de concentração de receita](risco-de-concentracao-de-receita.md)** —
  1 cliente = ~85% do MRR. **Leia este primeiro.** É o fato que condiciona todas as
  outras decisões.
- **[CAC-teto e budget de aquisição](cac-teto-e-budget-de-aquisicao.md)** —
  CAC-teto R$100–150, budget R$25/dia, e por que um teste de 1 semana custa ~1 CAC-teto.
- **[Reconciliação Stripe × banco](reconciliacao-stripe-x-banco.md)** —
  por que o Stripe mostra 19 cancelados e o banco mostra 1. Stripe é a fonte de verdade
  para churn histórico.
- **[Dunning no Stripe: config e reconfiguração](dunning-stripe-config-e-reconfiguracao.md)** —
  estado antes/depois, o desfecho `unpaid` → `past_due`, e o fato de que essas settings
  só existem no Dashboard (sem API de escrita).
- **[Base de winback e segmentação do churn](base-winback-e-segmentacao-do-churn.md)** —
  os 19 cancelados abertos em 2 involuntários / 4 winback / 13 trials.
- **[Funil de ativação medido](funil-de-ativacao-medido.md)** —
  3 de 10 usuários sem plano nenhum, 2 já com projeto e presos no sandbox. O degrau invisível
  existe. Inclui a armadilha da não-monotonicidade e o custo real do conserto.
- **[Conta de teste interna em produção](trial-de-2028-caso-isolado.md)** —
  A assinatura Scale em trial até 2028 é CONTA DE TESTE INTERNA do Bruno, não cliente. O que
  ela distorceu, e a ressalva de que pode não ser a única conta interna na base.
- **[Como consultar a réplica de leitura](consultar-a-replica-de-leitura.md)** —
  receita operacional: Prisma do container Fly, `pgbouncer=true` obrigatório, e o que não tentar.

## Números de referência (2026-07-24)

| Métrica | Valor |
|---|---|
| MRR total (25/jul) | R$ 5.902,77 |
| MRR ex-Exclusive (25/jul) | **R$ 897,77** |
| MRR — concentração | 84,8% em 1 cliente (Exclusive) |
| Faturamento Jun/2026 (fechado) | R$ 6.895,10 (13 faturas) |
| Faturamento Jul/2026 (parcial até 24) | R$ 7.107,22 (11 faturas) |
| ARPU SMB (ex-Exclusive, só pagantes) | R$ 349 |
| Churn mensal | ~27% → vida média ~3,6 meses |
| CAC-teto de trabalho | R$ 100–150 |
| Budget de aquisição recomendado | R$ 25/dia |
| Alvo real de dunning | 2 assinaturas (MRR R$698) |
| Usuários sem plano nenhum | 3 de 10 (30%), sendo 2 já com projeto criado |
| Preço médio contratado (ex-Exclusive, ex-teste) | R$ 295 |
| Ritmo de signup (últimos 3 meses) | ~0,7/mês, em queda |

## Armadilhas conhecidas

1. **Não calcule ARPU incluindo trials de R$0** — foi o que produziu o CAC-teto errado
   de R$62.
2. **Não calcule ARPU incluindo o cliente Exclusive** — infla o número para algo que
   nenhum cliente adquirido por mídia paga.
3. **Não puxe churn histórico do banco** — ele só tem a assinatura corrente.
4. **Não infira configuração do Stripe a partir de eventos antigos** — a régua de dunning
   inferida via API refletia abril, não o estado atual.
5. **Não sonde API com verbo destrutivo em produção** — no Stripe o estrago não se desfaz.
6. **Exclua a conta de teste interna** de qualquer contagem de usuários, assinaturas ou
   médias de preço. Ela é livemode e não tem marcação — e pode não ser a única. Ver
   [trial-de-2028-caso-isolado.md](trial-de-2028-caso-isolado.md).
