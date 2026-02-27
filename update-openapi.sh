#!/bin/bash
# Gera o openapi.yaml a partir do servidor backend local
# Uso: ./update-openapi.sh [URL]
#
# URL padrão: http://localhost:3000/docs/json
# Exemplo com URL diferente: ./update-openapi.sh http://localhost:4000/docs/json

URL="${1:-http://localhost:3000/docs/json}"

echo "Buscando spec de: $URL"

if ! curl -sf "$URL" > /dev/null; then
  echo "Erro: servidor não acessível em $URL"
  echo "Certifique-se de que o backend está rodando (npm run dev)"
  exit 1
fi

curl -s "$URL" | npx --yes js-yaml /dev/stdin > openapi.yaml 2>/dev/null || \
  node -e "
    const fs = require('fs');
    const data = require('/dev/stdin');
    const yaml = require('js-yaml');
    fs.writeFileSync('openapi.yaml', yaml.dump(data));
  " < <(curl -s "$URL") 2>/dev/null || \
  curl -s "$URL" > openapi.json && npx openapi-to-yaml openapi.json > openapi.yaml 2>/dev/null

# Fallback simples: salva como JSON convertido para YAML via Python se disponível
if [ ! -s openapi.yaml ]; then
  curl -s "$URL" | python3 -c "
import sys, json, yaml
data = json.load(sys.stdin)
print(yaml.dump(data, allow_unicode=True, default_flow_style=False))
" > openapi.yaml 2>/dev/null
fi

if [ -s openapi.yaml ]; then
  echo "openapi.yaml atualizado com sucesso!"
else
  echo "Falha ao gerar openapi.yaml. Certifique-se de ter python3+pyyaml ou nodejs instalado."
  exit 1
fi
