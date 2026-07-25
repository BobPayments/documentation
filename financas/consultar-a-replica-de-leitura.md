# Como consultar a réplica de leitura de produção

**Área:** Finanças · **Escrito em:** 2026-07-25

Receita para rodar `SELECT` no banco de produção sem tropeçar nas mesmas pedras duas vezes.

## Onde está a URL

`DATABASE_READ_URL`, secret do app Fly **`bob-payments-api`**. Os `.env` do repo apontam para
`localhost` — **não são produção**. Segredos de produção entram só via Fly secrets.

## O caminho que funciona

```bash
fly ssh console -a bob-payments-api -C 'node -e "<script>"'
```

Use o **Prisma do próprio container** (`/app/node_modules/@prisma/client`) — o driver `pg`
**não está instalado** lá.

## As três pedras

1. **`pgbouncer=true` é obrigatório.** A réplica passa por PgBouncer em modo transaction. Sem
   isso, a **segunda** query da mesma execução falha com
   `prepared statement "s0" already exists` (código `42P05`). Um script de uma query só passa e
   engana:
   ```js
   const raw = process.env.DATABASE_READ_URL;
   new PrismaClient({ datasourceUrl: raw + (raw.includes('?') ? '&' : '?') + 'pgbouncer=true' })
   ```
2. **`count()` volta como BigInt** — `JSON.stringify` quebra sem um replacer que converta.
3. **Quoting.** São quatro camadas (bash → fly → node → SQL). Escreva o comando num `.sh` em
   vez de montar no prompt. Dentro do JS use crases; para literais SQL que precisam de aspas
   simples, use a forma `'\''valor'\''`. O `fly` faz shell-split **sem** expansão, então crases
   passam literais.

## O que não tentar

`base64` + `eval` e `fly ssh sftp put` são barrados pelo classificador de permissão — com
razão: o primeiro parece ofuscação e o segundo é escrita em container de produção. Use o script
legível inline.

## Regras que continuam valendo

- **Só leitura.** Nunca descobrir comportamento de endpoint com verbo destrutivo em produção.
- **Nada identificável sai da consulta** para o repositório: sem nome, e-mail, `customer id`,
  `subscription id` — e sem `alias`/`merchant_name` de conexão, que carregam nome de
  comerciante.
- **Toda medição no banco é foto do estado atual, não série histórica.** Para pergunta
  histórica sobre assinatura, a fonte é o Stripe — ver
  [reconciliacao-stripe-x-banco.md](reconciliacao-stripe-x-banco.md).
