# Reconciliação Stripe × banco (assinaturas e churn)

**Área:** Finanças · **Apurado em:** 2026-07-24 · **Status:** concluído

## Conclusão em uma linha

**O Stripe é a fonte de verdade para churn histórico. O banco (Supabase, tabela
`user_plans`) reflete o *estado corrente* da assinatura e por design subnotifica
cancelamentos.** Divergência entre os dois não é bug — é diferença de modelo.

## O problema que motivou a apuração

O Stripe mostrava **19 assinaturas canceladas**; o banco de produção mostrava **1**.
A pergunta era se havia perda de dados, ambiente de teste misturado, ou erro de sync.

## O que foi verificado

### 1. Não é contaminação de ambiente de teste

Consulta feita com chave `sk_live`, checando o campo `livemode` em cada uma das 25
assinaturas retornadas: **`livemode = TRUE` em todas**. Portanto os 19 cancelamentos
são **reais e de produção** — não são resíduo de sandbox.

### 2. Os estados vivos batem perfeitamente

Comparando Stripe × `user_plans`:

| Status | Stripe | Banco | Bate? |
|---|---|---|---|
| `active` | 4 | 4 | ✅ |
| `past_due` | 1 | 1 | ✅ |
| `trialing` | 1 | 1 | ✅ |
| `canceled` | 19 | 1 | ❌ (esperado) |

Os 7 `subscription_id` presentes no banco são um **subconjunto** dos 25 do Stripe.

### 3. A divergência é estrutural, não acidental

`user_plans` guarda a assinatura **corrente** do usuário. Quando uma assinatura é
cancelada e o usuário assina de novo (ou o registro é sobrescrito), o histórico anterior
não é versionado. O banco nunca teve a intenção de ser um ledger de churn — e não é.

## Consequências práticas

- **Qualquer métrica de churn, winback ou coorte histórica deve sair do Stripe.**
  Puxar do banco vai subestimar o churn em ~95%.
- **Métricas de estado atual** (quantos ativos, quantos em atraso hoje) podem sair do
  banco com segurança — esses batem.
- **Se algum dia o churn histórico precisar ser consultável no produto**, isso exige
  versionar o histórico de assinaturas no banco (tabela de eventos / append-only via
  webhooks do Stripe). Hoje não existe e não é necessário para a operação.

## Desdobramento importante: o alvo real do dunning

Dos 19 cancelamentos, a segmentação por histórico de faturas pagas mostrou que
**o alvo de dunning são 2 assinaturas, não 19 e não 1**:

- **2** cancelamentos involuntários (falha de pagamento) — MRR R$698. Estes são dunning.
- **4** cancelamentos voluntários de ex-pagantes — MRR R$158. Estes são winback.
- **13** que nunca pagaram (trial expirado, R$0). Estes são **conversão de trial**, não churn.

Detalhamento em [base-winback-e-segmentacao-do-churn.md](base-winback-e-segmentacao-do-churn.md).

## Registrado na memória

Ver também o registro de memória `churn-source-of-truth`: *Stripe é a fonte, banco só
tem a assinatura corrente.*
