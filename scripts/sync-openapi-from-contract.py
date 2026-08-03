#!/usr/bin/env python3
"""Regenera documentation/openapi.yaml a partir de back/contract/openapi.snapshot.json.

Inclui apenas paths públicos de merchant e remove campos de provedor (gateway/connection)
conforme a política de docs públicas.

Uso (a partir da raiz do monorepo bob-payments):
  python3 documentation/scripts/sync-openapi-from-contract.py

Ou a partir de documentation/:
  python3 scripts/sync-openapi-from-contract.py
"""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Instale PyYAML: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

HERE = Path(__file__).resolve().parent
DOC_ROOT = HERE.parent
MONOREPO = DOC_ROOT.parent
SNAPSHOT = MONOREPO / "back" / "contract" / "openapi.snapshot.json"
OUT = DOC_ROOT / "openapi.yaml"

INCLUDE = {
    "/api/v1/transactions/": ["get", "post"],
    "/api/v1/transactions/{id}": ["get"],
    "/api/v1/checkout-sessions/": ["post"],
    "/api/v1/checkout-sessions/{token}/status": ["get"],
    "/api/v1/customers/": ["get"],
    "/api/v1/customers/{id}": ["get"],
    "/api/v1/store/": ["get"],
    "/api/v1/sandbox/transactions/{transactionId}/pay": ["post"],
    "/api/v1/card-tokenization-sessions/": ["post"],
}

STRIP_RESPONSE_FIELDS = {"gateway", "connection"}
STRIP_QUERY_PARAMS = {"connectionId"}
DESC_REPLACEMENTS = [
    (
        re.compile(
            r"utilizando a estratégia de execução paralela de gateways\.?\s*",
            re.I,
        ),
        "",
    ),
    (
        re.compile(
            r"A rota publicada deste método é usada na orquestração\.\s*",
            re.I,
        ),
        "",
    ),
]


def clean_desc(text: object) -> object:
    if not isinstance(text, str):
        return text
    for pat, rep in DESC_REPLACEMENTS:
        text = pat.sub(rep, text)
    return text.strip()


def strip_provider_fields(node: object) -> None:
    if isinstance(node, dict):
        if "parameters" in node and isinstance(node["parameters"], list):
            node["parameters"] = [
                p
                for p in node["parameters"]
                if not (
                    isinstance(p, dict) and p.get("name") in STRIP_QUERY_PARAMS
                )
            ]
        props = node.get("properties")
        if isinstance(props, dict):
            for field in list(props):
                if field in STRIP_RESPONSE_FIELDS:
                    del props[field]
            if "required" in node and isinstance(node["required"], list):
                node["required"] = [
                    r
                    for r in node["required"]
                    if r not in STRIP_RESPONSE_FIELDS
                ]
        if "description" in node:
            node["description"] = clean_desc(node["description"])
        for value in list(node.values()):
            strip_provider_fields(value)
    elif isinstance(node, list):
        for item in node:
            strip_provider_fields(item)


def main() -> int:
    if not SNAPSHOT.exists():
        print(f"Snapshot não encontrado: {SNAPSHOT}", file=sys.stderr)
        print(
            "Rode a partir do monorepo com back/contract/openapi.snapshot.json.",
            file=sys.stderr,
        )
        return 1

    snap = json.loads(SNAPSHOT.read_text())
    paths: dict = {}
    for path, methods in INCLUDE.items():
        item = snap["paths"].get(path)
        if not item:
            alt = path.rstrip("/") if path.endswith("/") else path + "/"
            item = snap["paths"].get(alt)
            if item:
                path = alt
        if not item:
            print(f"MISSING path {path}", file=sys.stderr)
            return 1
        out_item = {}
        for method in methods:
            if method not in item:
                print(f"MISSING {method.upper()} {path}", file=sys.stderr)
                return 1
            op = copy.deepcopy(item[method])
            strip_provider_fields(op)
            out_item[method] = op
        paths[path] = out_item

    docs_spec = {
        "openapi": snap.get("openapi", "3.0.3"),
        "info": {
            "title": "Bob Payments API",
            "description": (
                "API de pagamentos Bob Payments — PIX, cartão de crédito e cripto. "
                "Crie cobranças, gerencie clientes e receba webhooks."
            ),
            "version": (snap.get("info") or {}).get("version", "1.0.0"),
        },
        "servers": [
            {
                "url": "https://api.payments.bob.company",
                "description": "Servidor de produção",
            },
        ],
        "components": {
            "securitySchemes": {
                "ApiKeyAuth": snap["components"]["securitySchemes"]["ApiKeyAuth"],
                "BearerAuth": snap["components"]["securitySchemes"]["BearerAuth"],
            },
            "schemas": {},
        },
        "paths": paths,
    }

    OUT.write_text(
        yaml.dump(
            docs_spec,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=100,
        )
    )
    print(f"Wrote {OUT} ({len(paths)} paths)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
