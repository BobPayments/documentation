# Trial de Scale válido até 2028 — real, e caso isolado

**Área:** Finanças · **Confirmado em:** 2026-07-25 · **Fontes:** Stripe (livemode) + réplica

## O fato

Existe **uma** assinatura Scale (R$499/mês) em `trialing` com **`trial_end` em 2028-04-15** —
**631 dias no futuro** a partir da confirmação. `livemode: true`,
`cancel_at_period_end: false`, `expires_at` e `cut_at` nulos.

Um trial de dois anos não é trial: é assinatura gratuita.

É o usuário chamado **REF 1** em
[funil-de-ativacao-medido.md](funil-de-ativacao-medido.md) — o que rodou 12.751 transações em
sandbox e parou.

## É real, não artefato do banco

A suspeita inicial era de dessincronização: a linha em `user_plans` não era atualizada desde
2026-04-26. A comparação status a status das 7 linhas que têm assinatura no Stripe deu
**zero divergência**:

| Plano | Banco | Stripe |
|---|---|---|
| exclusive | active | active |
| scale | past_due | past_due |
| scale | **trialing** | **trialing** |
| scale | active | active |
| growth | active | active |
| growth | active | active |
| starter | canceled | canceled |

O banco não estava desatualizado — nada aconteceu com essa assinatura desde abril, o que é
coerente com um trial de dois anos, que não gera evento.

## Tamanho: 1 em 25. Não é padrão

- No Stripe: **25 assinaturas** em todo o histórico. Com `trial_end` no futuro: **uma**.
- No banco: das 8 linhas de `user_plans`, só 1 tem `trial_ends_at` preenchido.

**Sobre o critério "`expires_at` NULL com plano pago":** são 6 de 8, **mas isso não aponta
nada**. `expires_at` NULL é o estado normal de assinatura recorrente em curso — ela não expira,
renova. Das 6, cinco são legítimas (4 `active` + 1 `past_due`) e a sexta é a própria trialing.
Reportar as 6 como suspeitas seria alarme falso. Fica registrado para que ninguém refaça a
consulta achando que encontrou um buraco.

## Causa provável: erro humano no Dashboard, não bug de código

Dois indícios convergentes:

1. **A data é exatamente 720 dias após o início** (2026-04-26 + 720 = 2028-04-15). Número
   redondo demais para ter sido escolhido como data — parece alguém digitando `720` num campo
   de dias.
2. **O código nunca cria trial.** Não existe `trial_period_days` em lugar nenhum do back; o
   único ponto que toca isso é `stripe-billing-provider.ts:379`, que apenas **lê** o
   `trial_end` vindo do Stripe.

Portanto o trial foi criado à mão no Dashboard, não pelo checkout do produto — e **não há risco
de se replicar sozinho** em novos clientes.

## Quanto custa

R$499/mês não faturados enquanto durar; até abril/2028, ~R$10.500. O número que importa é o de
curto prazo: **3 meses ≈ R$1.500**, da mesma ordem do MRR SMB inteiro (a base sem o Exclusive
gira R$1–2k/mês — ver
[risco-de-concentracao-de-receita.md](risco-de-concentracao-de-receita.md)).

**Ressalva honesta:** só vira receita se essa pessoa fosse converter, e hoje ela está travada
no sandbox com zero transações de produção. Não é dinheiro perdido — é o preço de não ter
percebido.

## O que NÃO foi feito, de propósito

**Nada foi alterado.** Encurtar o trial é escrita em produção afetando um cliente real, e no
Stripe não se desfaz. A ordem recomendada:

1. O Fecho conversa com a pessoa — o gancho é destravar produção, **nunca** prazo. O argumento
   "seu teste acaba em X dias" não existe; se usado, o cliente confere e a credibilidade cai.
2. Só se houver interesse, encurta-se o trial de comum acordo.

Mexer antes do toque queima o único bom lead da base.
