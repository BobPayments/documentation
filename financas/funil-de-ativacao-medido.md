# Funil de ativação — medido com dado (não hipótese)

**Área:** Finanças · **Medido em:** 2026-07-25 · **Fonte:** réplica de leitura de produção

Complementa `back/docs/metrics/FUNIL_DE_ATIVACAO.md`, do Fecho, que mapeou o caminho lendo
código mas não conseguia dizer onde trava — `ActivityLog` é indexado por projeto e só existe
do degrau 4 em diante. Este documento troca a hipótese dele por medição.

## O achado principal: existe um degrau invisível, e tem gente nele

**3 de 11 usuários (27%) não têm nenhuma linha em `user_plans`** — sem plano nenhum.
**Dois deles já criaram projeto**: estão no painel, em sandbox, sem conseguir ativar produção,
porque o gate exige plano ativo e **o Free não é automático**.

Era exatamente o que o Fecho havia deduzido do código. Não era teoria.

## Resultado das duas queries

| Q1 (`users`) | | Q2 (projeto / sandbox / plano) | |
|---|---|---|---|
| contas | 11 | contas | 11 |
| e-mail verificado | 10 | criou projeto | 10 |
| perfil completo | 9 | saiu do sandbox | 6 |
| | | tem plano | **8** |
| | | tem plano pago (slug ≠ free) | 7 |

### Onde cada um dos 11 parou

| Estado | Qtd |
|---|---|
| Funil completo | 6 |
| Perfil incompleto, sem projeto, sem plano | 1 |
| E-mail **não** verificado, mas perfil completo e projeto criado, **sem plano** | 1 |
| Perfil completo, projeto criado, **sem plano** | 1 |
| Perfil **incompleto**, projeto criado, plano Free ativo | 1 |
| Perfil completo, projeto, plano pago, **nunca saiu do sandbox** | 1 |

## ⚠️ Armadilha: os estados não são monotônicos

Contar "quantos pararam no degrau N" com filtros independentes **soma 13 para 11 usuários** —
conta gente duas vezes. Só o agrupamento por padrão de estado (a tabela acima) fecha em 11.

A causa é que o funil não é uma escada: há usuário com e-mail não verificado que completou
perfil e criou projeto, e usuário com perfil incompleto que ativou o Free. **Qualquer métrica
de funil aqui precisa ser calculada por padrão, não por degrau isolado.**

## O que isso muda na ordenação de prioridades

1. **O degrau 3 (documento antes de valor) não é a maior perda** — só 1 usuário parou ali. E
   nem é bloqueante de verdade: há gente com perfil incompleto que criou projeto e ativou Free.
2. **O vazio entre os degraus 5 e 8 é onde se perde**, como o Fecho suspeitava. É lá que estão
   os 2 sem plano com projeto criado.
3. **`email_verified` não é gate real.** Um usuário não verificado completou perfil e criou
   projeto — provavelmente o login social não seta a flag. O degrau 2 não trava ninguém e
   também não mede nada.

## As 3 pessoas presas, por leitura técnica

Sem identificadores — rótulos anônimos estáveis. Os IDs ficam no painel/Stripe.

| | REF 1 | REF 2 | REF 3 |
|---|---|---|---|
| Plano | scale, **trialing** (26/04) | nenhum | nenhum |
| Signup | há 90 dias | há 101 dias | **há 16 dias** |
| Projeto criado | 2026-04-26 | 2026-04-15 | 2026-07-09 |
| `connection_account` | **1, ativa** (gateway sandbox, 30/06) | nenhuma | nenhuma |
| Transações sandbox | **12.751** (última 30/06) | 0 | 0 |
| Transações produção | 0 | 0 | 0 |

**Correção registrada:** o REF 1 foi reportado primeiro como "pagante que nunca saiu do
sandbox". Ele está em **`trialing`**, não pago-ativo — a classificação inicial olhou o slug do
plano (`scale` ≠ `free`) e não o status. Não é cliente pagando sem usar; é trial travado.
Ver [trial-de-2028-caso-isolado.md](trial-de-2028-caso-isolado.md).

**REF 1 é o melhor lead da base.** Conectou o gateway, rodou 12.751 transações simuladas e
parou no dia seguinte. Não é usuário morto — é alguém que investiu esforço técnico real e
travou na saída do sandbox.

**A verificar no código:** se o gate de produção aceita plano em `trialing` ou só `active`
(`toggle-dev-mode.ts`). Se só aceita `active`, o REF 1 está bloqueado por regra, não por
escolha — e aí é bug, não objeção de venda.

## Quanto custa o degrau invisível — e por que o número não decide

**Teto aritmético:** 3 × R$329 (preço médio contratado, excluindo o Exclusive) = **R$987/mês**.

**É teto, não estimativa.** Três motivos para não decidir por ele:

1. **O conserto proposto leva a Free, não a pago** — atribuir Free no signup gera R$0 de MRR
   imediato. Ele destrava o gate, não a receita.
2. **N=3 não sustenta taxa de conversão.** E a armadilha específica: aplicar a taxa da própria
   base (7/11 = 64%) aos 3 presos é circular — eles são justamente os que *não* converteram.
3. **O estoque é velho:** presos há 16, ~90 e 152 dias. Quem está parado há 5 meses não
   converte quando a fricção some.

**O ritmo de signup está caindo:** fev 4 · mar 3 · abr 2 · mai 0 · jun 1 · jul 1 (11 contas em
141 dias). Nos últimos 3 meses, ~0,7/mês. A 27% de captura, **~0,2 usuário/mês** entra no
buraco — adiar o conserto um mês custa ~R$65/mês de MRR-teto.

**Conclusão: pela receita que trava, o conserto não é urgente. Pelo sequenciamento, é.** Ele é
pré-requisito do teste de Google Ads: pagar CAC para trazer gente a um funil onde 27% cai num
buraco silencioso significa (a) desperdiçar ~1 dos ~4 cadastros esperados, e pior, (b) **medir
o buraco em vez do canal** — e matar um canal possivelmente bom por defeito nosso. Ver
[cac-teto-e-budget-de-aquisicao.md](cac-teto-e-budget-de-aquisicao.md).

**Recomendação:** o conserto precisa estar no ar antes do primeiro real de tráfego pago. Não é
problema de copy nem de tela de onboarding — é atribuir Free no signup, ou levar o usuário
direto à tela de plano depois de criar o projeto.

## O que falta instrumentar

O Fecho já listou: evento de funil por usuário (`signup`, `email_verified`,
`profile_completed`, `project_created`, `connection_created`, `production_activated`,
`checkout_started`, `plan_activated`). Enquanto não existir, toda medição aqui é **foto do
estado atual, não série histórica** — quem passou por um degrau e voltou aparece só no estado
final.

## Como reproduzir

Ver [consultar-a-replica-de-leitura.md](consultar-a-replica-de-leitura.md).
