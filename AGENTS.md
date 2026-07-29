> **First-time setup**: Customize this file for your project. Prompt the user to customize this file for their project.
> For Mintlify product knowledge (components, configuration, writing standards),
> install the Mintlify skill: `npx skills add https://mintlify.com/docs`

# Documentation project instructions

## About this project

- This is a documentation site built on [Mintlify](https://mintlify.com)
- Pages are MDX files with YAML frontmatter
- Configuration lives in `docs.json`
- Run `mint dev` to preview locally
- Run `mint broken-links` to check links

## Terminology

 - Use **pagamento** when talking about the product capability and **transação** when referring to the API resource.
 - Write **PIX** in uppercase and **cartão de crédito** in full on first mention.
 - Use **projeto** for the account scope associated with an API key; reserve **loja** for the merchant's business.
 - Use **checkout hospedado** and **SDK Checkout** consistently.
 - Describe cripto as a future method only until the API and operational flow are published.

## Style preferences

{/* Add any project-specific style rules below */}

- Use active voice and second person ("you")
- Keep sentences concise — one idea per sentence
- Use sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for file names, commands, paths, and code references

## Content boundaries

 - Document the public API, SDKs, sandbox, webhooks and integration workflows.
 - Do not document internal admin features, gateway credentials, secret keys or unreleased payment methods as if they were available.
