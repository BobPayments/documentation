# Dunning no Stripe — configuração, reconfiguração e limites da API

**Área:** Finanças · **Apurado e aplicado em:** 2026-07-24 · **Status:** concluído

## Resumo

A régua de recuperação de pagamento (Revenue Recovery) do Stripe foi auditada no
Dashboard live e **uma única alteração foi aplicada**: o desfecho da assinatura ao
esgotar as tentativas passou de `unpaid` para `past_due`.

## ⚠️ Limitação que custou tempo — registre isso

**As configurações de Revenue Recovery do Stripe (retry schedule, e-mails de dunning,
ação ao esgotar as tentativas) existem SOMENTE no Dashboard. Não há API REST de escrita
para elas.** A chave `sk_live` lê o efeito dessas settings (por exemplo,
`next_payment_attempt` numa fatura), mas não consegue alterá-las.

Consequência: qualquer mudança nessa régua é **manual, no Dashboard**, e precisa ser
verificada com reload da página. Não dá para versionar em código nem automatizar.

## O que a API fazia parecer (inferência) vs. o que era real

A primeira leitura foi feita só via API, inspecionando faturas e assinaturas — e levou a
uma conclusão **errada**, porque os dados observados eram de abril/2026:

| | Inferido via API (dados de abril) | Real no Dashboard (jul/2026) |
|---|---|---|
| Tentativas | ~2 (D0 + ~24h) | **Smart Retries, até 8 tentativas em 1 semana** |
| Janela | ~1 a 1,5 dia | ~7 dias |
| E-mails de falha | ilegível via API | **já ligados** (cartão, débito, expiração) |
| Desfecho da assinatura | cancelada na seca (`payment_failed`) | `unpaid` ("marcar como não paga") |
| Desfecho da fatura | VOID | "deixar vencida" |

**Lição:** a premissa "o Stripe corta na seca em 1 dia" era verdadeira em abril e já
havia sido corrigida antes desta auditoria. Inferir configuração a partir de eventos
antigos produz um retrato desatualizado — sempre confirmar no Dashboard.

## ANTES (verificado no Dashboard live, 2026-07-24)

- **Retry:** Smart Retries ativado — até 8 tentativas ao longo de 1 semana.
- **E-mails:** falha de pagamento de cartão **ON**; débito bancário **ON**;
  expiração de cartão **ON**.
- **Ao esgotar as tentativas — assinatura:** "marcar como não paga" (`unpaid`).
- **Ao esgotar as tentativas — fatura:** "deixar vencida".

## DEPOIS (aplicado e verificado após reload, 2026-07-24)

- **Retry:** MANTIDO — Smart Retries, 8×/1 semana. Já opera dentro da janela de 7 dias
  (a fatura `past_due` corrente tinha retry agendado para D+1), então não foi preciso
  trocar por uma régua fixa D0/D+2/D+4/D+6 — que recuperaria menos.
- **E-mails:** MANTIDOS ON.
- **Assinatura ao esgotar:** **MUDADO de `unpaid` → `past_due`** ("deixar a assinatura
  vencida"), alinhado à decisão da Direção.
- **Fatura ao esgotar:** inalterada ("deixar vencida").

**Escopo da alteração:** exatamente um toggle. Retry, e-mails, preços, clientes e demais
seções não foram tocados.

### Por que `past_due` e não `unpaid`

São estados distintos no Stripe. `unpaid` é um estado terminal de cobrança — o Stripe
para de tentar e a assinatura fica num limbo que exige intervenção. `past_due` mantém a
assinatura no fluxo normal de recuperação e permite que ela **volte sozinha para `active`
se o cliente pagar**, sem ação manual. Para uma base pequena, onde cada recuperação
importa, `past_due` é o estado certo.

## Pendência: corte em D+7 não é nativo do Stripe

Não existe configuração "cancelar a assinatura no 7º dia". O Stripe oferece apenas o
desfecho ao esgotar as tentativas, sem controle fino do prazo.

**Spec da automação (trabalho do back, não de Finanças):**

1. Webhook em `invoice.payment_failed` / `customer.subscription.updated` grava
   `past_due_started_at` quando a assinatura entra em `past_due`.
2. Cron diário cancela via API as assinaturas em `past_due`/`unpaid` há **≥ 7 dias**
   sem recuperação.
3. O job deve ser **idempotente**. Se o cliente pagar antes, o Stripe reativa a
   assinatura sozinho e o job simplesmente não a encontra mais no filtro.

**Nenhum cancelamento manual.** Enquanto a automação não existir, assinaturas em
`past_due` permanecem nesse estado — o que é preferível a cortar cedo demais.

## Alvo real do dunning

**2 assinaturas** (churn involuntário, MRR R$698) — não 19, não 1. Ver
[reconciliacao-stripe-x-banco.md](reconciliacao-stripe-x-banco.md) e
[base-winback-e-segmentacao-do-churn.md](base-winback-e-segmentacao-do-churn.md).

## Regra da casa aprendida aqui

Nunca descobrir comportamento de endpoint com verbo destrutivo (`DELETE`/`PUT`) em
produção. No Stripe o estrago não se desfaz.
