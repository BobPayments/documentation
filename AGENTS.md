> For Mintlify product knowledge (components, configuration, writing standards),
> install the Mintlify skill: `npx skills add https://mintlify.com/docs`

# Documentation project instructions

## About this project

- This is a documentation site built on [Mintlify](https://mintlify.com)
- Pages are MDX files with YAML frontmatter
- Configuration lives in `docs.json`
- Run `mint dev` to preview locally
- Run `mint broken-links` to check links

## Navigation structure

- The **Documentação** tab holds guides and concepts only — no endpoint pages, so no HTTP method badges appear in its sidebar.
- The **Referência da API** tab is curated by resource in `docs.json`, not generated from `openapi.yaml`. Each endpoint is an MDX page under `pages/` whose frontmatter points at the operation (`openapi: "POST /api/v1/transactions/"`), which keeps URLs stable and human-readable.
- Because that tab is curated, **a new operation in `openapi.yaml` will not show up on its own**: add the matching MDX page and list it in the resource group. Mintlify still serves an auto-generated `/api-reference/<summary>` page for it, but that page is outside the navigation and `seo.indexing: "navigable"` keeps it out of search.

## Terminology

 - Use **pagamento** when talking about the product capability and **transação** when referring to the API resource.
 - Write **PIX** in uppercase.
 - Use **projeto** for the account scope associated with an API key; reserve **loja** for the merchant's business.
 - Call the test environment **sandbox** — never "Dev Mode" or "Bob Sandbox". `devMode` stays as-is only when naming the API field.

## Style preferences

{/* Add any project-specific style rules below */}

- Use active voice and second person ("you")
- Keep sentences concise — one idea per sentence
- Use sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for file names, commands, paths, and code references

## Content boundaries

 - Document the public PIX API, server SDKs, sandbox, webhooks and integration workflows.
 - Do not document payment links, checkout, frontend checkout SDKs or crypto as public capabilities.
 - Do not document internal admin features, gateway credentials, secret keys or unreleased payment methods as if they were available.
