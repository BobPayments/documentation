# Conta de teste interna em produção (o "trial de 2028")

**Área:** Finanças · **Apurado em:** 2026-07-25 · **Corrigido em:** 2026-07-25
**Fontes:** Stripe (livemode) + réplica

> **Correção.** A versão anterior deste documento tratava esta assinatura como receita sendo
> regalada por erro humano no Dashboard. **Está errado.** O Bruno confirmou que **é a conta de
> teste dele**. Não é receita perdida, não é erro, não é caso a resolver. O documento foi
> mantido — em vez de apagado — porque a conta continua existindo em livemode e continua
> contaminando métricas se ninguém souber que ela está lá.

## O que é

Uma assinatura Scale (R$499/mês) em `trialing` com `trial_end` em **2028-04-15**, criada em
2026-04-26. `livemode: true`, `cancel_at_period_end: false`.

**É conta de teste interna do Bruno.** O trial longo é proposital: mantém a conta utilizável
sem gerar cobrança. Os 720 dias exatos, que pareciam digitação equivocada, são só isso — um
prazo redondo escolhido de propósito.

As **12.751 transações em sandbox** registradas nessa conta, que pareciam um lead altamente
engajado, são tráfego de teste.

## Por que isso importa mesmo não sendo problema

**Uma conta interna em livemode entra em toda contagem que não a exclua explicitamente.**
Ela já havia distorcido três leituras antes da correção:

1. **Funil de ativação** — contava como 1 dos 11 usuários, e como "pagante preso no sandbox".
   Corrigido: o funil real tem **10 usuários**. Ver
   [funil-de-ativacao-medido.md](funil-de-ativacao-medido.md).
2. **Base de leads** — era apontada como "o melhor lead da base, disparado", com prioridade 1
   na fila de toque. **Esse lead não existe.**
3. **Preço médio contratado** — entrava na média das assinaturas pagas, puxando-a para cima.

**Não afeta o MRR**, porque `trialing` nunca foi contado como receita ativa. Ver
[risco-de-concentracao-de-receita.md](risco-de-concentracao-de-receita.md).

## ⚠️ Ressalva aberta: pode não ser a única

Esta conta só foi identificada como interna porque alguém perguntou. **Não existe marcação no
banco nem no Stripe que distinga conta interna de cliente real** — nenhuma flag, nenhum
metadata, nenhum padrão de e-mail verificável a partir dos dados agregados.

Consequência: **não é possível afirmar que as outras 24 assinaturas do Stripe são todas de
clientes reais.** Se houver outras contas de teste, elas estão hoje dentro do churn histórico
(os 19 cancelados), do funil e das médias — em todos os documentos desta pasta.

**Recomendação:** marcar contas internas de forma legível por consulta — `metadata` no customer
do Stripe, ou uma flag em `users`. Enquanto não existir, toda apuração desta pasta carrega essa
incerteza, e a única forma de resolver é o Bruno listar quais contas são dele.

## Tamanho, para referência

- Stripe: **25 assinaturas** no histórico, das quais 1 é esta conta de teste → **24** a
  investigar como reais.
- Assinaturas em `trialing`: **apenas esta**. Nenhum outro trial existe, e o código nunca cria
  trial (`stripe-billing-provider.ts:379` apenas lê o `trial_end` vindo do Stripe), então não
  nascem novos sozinhos.
- **Decisão do Bruno em 25/07: a Bob não terá trial.** Como não há trial em código nem outro
  trial ativo, não há nada a encerrar além do que se decidir sobre esta conta interna.

## Registro metodológico

O critério "`expires_at` NULL com plano pago" foi testado como sinal de anomalia e **não serve**:
dá 6 de 8 linhas porque `expires_at` NULL é o estado normal de assinatura recorrente em curso.
Fica registrado para ninguém refazer a consulta achando que encontrou um buraco.
