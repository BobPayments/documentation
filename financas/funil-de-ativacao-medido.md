# Funil de ativação — medido com dado (não hipótese)

**Área:** Finanças · **Medido em:** 2026-07-25 · **Corrigido em:** 2026-07-25
**Fonte:** réplica de leitura de produção

> **Correção.** A primeira medição contava **11 usuários**. Um deles é a **conta de teste
> interna do Bruno** — a mesma que aparecia como "pagante preso no sandbox" e depois como
> "melhor lead da base". Ela foi removida de todas as contagens abaixo. **O funil real tem
> 10 usuários.** Ver [trial-de-2028-caso-isolado.md](trial-de-2028-caso-isolado.md).

Complementa `back/docs/metrics/FUNIL_DE_ATIVACAO.md`, do Fecho, que mapeou o caminho lendo
código mas não conseguia dizer onde trava — `ActivityLog` é indexado por projeto e só existe
do degrau 4 em diante. Este documento troca a hipótese dele por medição.

## O achado principal: existe um degrau invisível, e tem gente nele

**3 de 10 usuários (30%) não têm nenhuma linha em `user_plans`** — sem plano nenhum.
**Dois deles já criaram projeto**: estão no painel, em sandbox, sem conseguir ativar produção,
porque o gate exige plano ativo e **o Free não é automático**.

Era exatamente o que o Fecho havia deduzido do código. Não era teoria. A correção da conta de
teste **não afeta este achado** — os 3 sem plano são todos usuários reais; a proporção subiu
de 27% para 30% justamente porque o denominador caiu.

## Resultado das duas queries (já sem a conta de teste)

| Q1 (`users`) | | Q2 (projeto / sandbox / plano) | |
|---|---|---|---|
| contas | 10 | contas | 10 |
| e-mail verificado | 9 | criou projeto | 9 |
| perfil completo | 8 | saiu do sandbox | 6 |
| | | tem plano | **7** |
| | | tem plano pago (slug ≠ free) | 6 |

### Onde cada um dos 10 parou

| Estado | Qtd |
|---|---|
| Funil completo | 6 |
| Perfil incompleto, sem projeto, sem plano | 1 |
| E-mail **não** verificado, mas perfil completo e projeto criado, **sem plano** | 1 |
| Perfil completo, projeto criado, **sem plano** | 1 |
| Perfil **incompleto**, projeto criado, plano Free ativo | 1 |

## ⚠️ Armadilha: os estados não são monotônicos

Contar "quantos pararam no degrau N" com filtros independentes **conta gente duas vezes** — na
medição original somava 13 para 11 usuários. Só o agrupamento por padrão de estado (a tabela
acima) fecha certo.

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

## As pessoas presas, por leitura técnica

Sem identificadores — rótulos anônimos estáveis. Os IDs ficam no painel/Stripe.

| | REF 2 | REF 3 |
|---|---|---|
| Plano | nenhum | nenhum |
| Signup | há 101 dias | **há 16 dias** |
| Projeto criado | 2026-04-15 | 2026-07-09 |
| `connection_account` | nenhuma | nenhuma |
| Transações sandbox | 0 | 0 |
| Transações produção | 0 | 0 |

**O REF 1 saiu desta lista — era a conta de teste.** Com ele saem também as 12.751 transações
em sandbox que o faziam parecer um lead altamente engajado, e a recomendação de tratá-lo como
prioridade 1 de toque. **Esse lead não existe.**

O que sobra é fraco: **REF 2 é frio** (criou o projeto há 101 dias, nunca voltou, zero esforço
de integração) e **REF 3 é recente** (16 dias, ainda na janela natural de ativação — não precisa
de winback, precisa do próximo passo, que a tela não oferece).

**A verificar no código:** se o gate de produção aceita plano em `trialing` ou só `active`
(`toggle-dev-mode.ts`). A pergunta continua válida para o produto, mesmo sem o REF 1: define o
que acontece com um futuro cliente em trial. Como a Bob decidiu não ter trial, a prioridade cai.

## Quanto custa o degrau invisível — e por que o número não decide

**Teto aritmético:** 3 × R$295 (preço médio contratado, excluindo o Exclusive **e a conta de
teste**) = **R$885/mês**.

**É teto, não estimativa.** Três motivos para não decidir por ele:

1. **O conserto proposto leva a Free, não a pago** — atribuir Free no signup gera R$0 de MRR
   imediato. Ele destrava o gate, não a receita.
2. **N=3 não sustenta taxa de conversão.** E a armadilha específica: aplicar a taxa da própria
   base aos 3 presos é circular — eles são justamente os que *não* converteram.
3. **O estoque é velho:** presos há 16, ~90 e 152 dias. Quem está parado há 5 meses não
   converte quando a fricção some.

**O ritmo de signup está caindo:** fev 4 · mar 3 · abr 1 · mai 0 · jun 1 · jul 1 (10 contas
reais em 141 dias). Nos últimos 3 meses, ~0,7/mês. A 30% de captura, **~0,2 usuário/mês** entra
no buraco — adiar o conserto um mês custa ~R$62/mês de MRR-teto.

**Conclusão: pela receita que trava, o conserto não é urgente. Pelo sequenciamento, é.** Ele é
pré-requisito do teste de Google Ads: pagar CAC para trazer gente a um funil onde 30% cai num
buraco silencioso significa (a) desperdiçar ~1 dos ~4 cadastros esperados, e pior, (b) **medir
o buraco em vez do canal** — e matar um canal possivelmente bom por defeito nosso. Ver
[cac-teto-e-budget-de-aquisicao.md](cac-teto-e-budget-de-aquisicao.md).

**Recomendação:** o conserto precisa estar no ar antes do primeiro real de tráfego pago. Não é
problema de copy nem de tela de onboarding — é atribuir Free no signup, ou levar o usuário
direto à tela de plano depois de criar o projeto.

## Ressalva que vale para toda esta pasta

A conta de teste só foi identificada porque alguém perguntou. **Não há marcação que distinga
conta interna de cliente real** — se houver outras, ainda estão dentro destes números.

## O que falta instrumentar

O Fecho já listou: evento de funil por usuário (`signup`, `email_verified`,
`profile_completed`, `project_created`, `connection_created`, `production_activated`,
`checkout_started`, `plan_activated`). Enquanto não existir, toda medição aqui é **foto do
estado atual, não série histórica**.

## Como reproduzir

Ver [consultar-a-replica-de-leitura.md](consultar-a-replica-de-leitura.md). **Exclua a conta de
teste** de qualquer contagem nova.
