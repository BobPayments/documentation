# Base de winback e segmentação do churn

**Área:** Finanças · **Apurado em:** 2026-07-24 · **Fonte:** Stripe livemode

> **Nota sobre dados:** este documento é público no repositório, então **não contém
> identificadores de cliente** (nome, e-mail, `customer id` ou `subscription id`). As
> assinaturas aparecem por descrição e por rótulo anônimo estável (A, B, W1…). Os IDs
> reais ficam no Stripe e na nota operacional de winback no canvas — que é onde a
> recuperação é executada. Aqui está a análise, não a lista de contatos.

## O ponto central

Os "19 cancelados" **não são um bloco**. Tratá-los como uma lista única leva a mandar a
abordagem errada para a maioria deles. A segmentação por histórico de faturas pagas:

| Segmento | Qtd | MRR perdido | Ação correta |
|---|---|---|---|
| 🔴 **Involuntário** (falha de cartão) | 2 | R$ 698 | **dunning / atualização de cartão** — prioridade |
| 🟡 **Voluntário ex-pagante** | 4 | R$ 158 | winback com oferta (ticket baixo) |
| ⚪ **Nunca pagou** (trial expirado) | 13 | R$ 0 | **conversão de trial** — não é churn nem dunning |

**Só 6 dos 19 chegaram a pagar alguma vez.** Os outros 13 são um problema de funil de
ativação, não de retenção.

Note também a assimetria de valor: **2 assinaturas concentram 82% do MRR perdido.** O
esforço de recuperação deveria seguir essa proporção.

## 🔴 Involuntário — dunning (prioridade)

| Ref. | Plano | Faturas pagas | Cancelada |
|---|---|---|---|
| **A** | Scale R$ 499 | **21** | 2026-04-20 |
| **B** | Growth R$ 199 | 3 | 2026-04-27 |

**A é o maior valor recuperável da base**: 21 faturas pagas, ou seja, quase dois anos de
cliente satisfeito perdido por um cartão que falhou. Não é um cliente que quis sair — é um
cliente que o sistema deixou cair. Ver
[dunning-stripe-config-e-reconfiguracao.md](dunning-stripe-config-e-reconfiguracao.md).

Ambos os cancelamentos são de abril/2026, sob a régua de dunning **antiga** (corte curto,
~1 dia). A régua atual — 8 tentativas ao longo de 1 semana, com e-mails — provavelmente
teria recuperado pelo menos um deles.

## 🟡 Voluntário ex-pagante — winback

| Ref. | Plano | Faturas pagas | Cancelada |
|---|---|---|---|
| W1 | — | 1 | 2026-07-01 |
| W2 | R$ 79 | 1 | 2026-02-21 |
| W3 | R$ 79 | 1 | 2026-02-18 |
| W4 | — | 2 | 2026-02-18 |

Padrão: quase todos pagaram **1 fatura e saíram**, em planos antigos de R$79. Isso é
sinal de que o produto não entregou valor no primeiro ciclo — winback aqui tem taxa de
sucesso baixa se nada mudou no produto desde então.

**W3 e W4 são do mesmo cliente** (duas assinaturas canceladas na mesma data). Ou seja, os
4 cancelamentos voluntários vêm de apenas **3 clientes distintos**.

## ⚪ Nunca pagou — 13 trials (frente de conversão)

Nenhum chegou a ser cobrado. Características do lote:

- **6 das 13 expiraram no mesmo dia, 2026-07-01** — expiração em massa, vários em plano
  Scale R$499 que nunca gerou uma cobrança. Um lote assim concentrado sugere trials
  criados juntos que nunca ativaram, e não 6 decisões independentes de não comprar.
- As 7 restantes se espalham entre fevereiro e julho/2026, sem concentração.

Essa é uma frente de **ativação/onboarding**, separada de dunning e de winback. Misturá-la
com churn inflaria a taxa de cancelamento com gente que nunca foi cliente.

## Lacuna de dados a corrigir

**O motivo de cancelamento é `None` em todos os 19.** Nem o Stripe nem o produto capturam
por que o cliente saiu. Isso torna impossível separar "saiu porque faltou feature" de
"saiu porque achou caro" de "saiu porque não entendeu o produto" — e portanto impossível
priorizar correção.

**Recomendação:** capturar motivo de cancelamento no fluxo de cancelamento do produto
(campo obrigatório com opções + texto livre). Baixo esforço, e sem isso toda análise de
churn daqui para frente continua cega.

## Como executar a recuperação

Os IDs de assinatura e cliente e os e-mails saem do Stripe (Dashboard ou API, filtrando
por `status=canceled` e cruzando com o histórico de faturas pagas, que é o que separa os
três segmentos acima). A lista nominal operacional está na nota de winback no canvas.
**Não traga esses identificadores para o repositório.**
