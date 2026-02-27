# Bob Payments — Documentação

Documentação pública da API Bob Payments, construída com [Mintlify](https://mintlify.com).

## Pré-visualizar localmente

```bash
npx mintlify dev
```

## Atualizar a referência da API

Com o backend rodando localmente:

```bash
./update-openapi.sh
```

Isso busca o spec em `http://localhost:3000/docs/json` e atualiza o `openapi.yaml`.

## Estrutura

```
pages/          # Páginas de documentação (MDX)
openapi.yaml    # Spec OpenAPI gerado do backend
docs.json       # Configuração do Mintlify
```

## Deploy

O deploy é automático via Mintlify ao fazer push na branch `main`.
