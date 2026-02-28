<p align="center">
  <img alt="Bob Payments Logo" src="https://resend-attachments.s3.amazonaws.com/bbjVzq13Vc2xBio" width="200" />
</p>

# Bob Payments Documentation

[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/BobPayments/documentation/issues)

Bob Payments é um orquestrador de pagamentos PIX para desenvolvedores. Em vez de integrar e manter cada gateway individualmente, você conecta uma única API e nós cuidamos do roteamento, fallback e disponibilidade. Built by developers for developers, it offers:

- Múltiplos gateways PIX por trás de uma única API
- QR Code e código copia-e-cola gerados em uma chamada
- Notificações em tempo real via webhooks com verificação HMAC-SHA256
- Sandbox completo para simular pagamentos sem mover dinheiro real
- Respostas JSON consistentes em todos os endpoints
- Autenticação simples via Bearer Token

## 🚀 Quick Start

Esta documentação é construída com [Mintlify](https://mintlify.com).

1. **Visualizar localmente**
```bash
# Instalar o CLI do Mintlify
npm i -g mintlify

# Iniciar o servidor de desenvolvimento
mintlify dev
```

2. **Acesse `http://localhost:3000` para ver a documentação**

## 📚 Estrutura

```
.
├── pages/
│   ├── introduction.mdx        # Visão geral da API
│   ├── devmode.mdx             # Ambiente sandbox
│   ├── authentication.mdx      # Autenticação Bearer Token
│   ├── webhooks.mdx            # Webhooks e verificação de assinatura
│   ├── production.mdx          # Guia para ir a produção
│   ├── pix/                    # Cobranças PIX
│   ├── customers/              # Gestão de clientes
│   └── store/                  # Dados da loja
├── docs.json                   # Configuração do Mintlify
└── openapi.yaml                # Especificação OpenAPI (gerada automaticamente)
```

## 🔧 Desenvolvimento local

```bash
mintlify dev
```

Se o servidor não iniciar, execute `mintlify install` para reinstalar as dependências.

## 🚀 Deploy

As alterações são publicadas automaticamente quando mescladas na branch `main`, via integração do Mintlify com o GitHub.

## 💪 Suporte

- Abra uma issue no [GitHub](https://github.com/BobPayments/documentation/issues)
- Entre em contato via [suporte@payments.bob.company](mailto:suporte@payments.bob.company)
