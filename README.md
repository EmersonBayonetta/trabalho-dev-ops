[![CI](https://github.com/EmersonBayonetta/trabalho-dev-ops/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/EmersonBayonetta/trabalho-dev-ops/actions/workflows/ci.yml)

# Portfólio fictício — Emerson Teododo

Site estático em HTML e CSS, com imagens SVG locais. O workflow de CI valida Pull Requests para `main` em Node.js 18 e 20; o workflow de CD publica o site no GitHub Pages após cada push em `main`.

## Validações de CI

- Confirma que `index.html` está na raiz.
- Rejeita arquivos com mais de 500 KB.
- Procura marcadores TODO/FIXME e termos sensíveis nos arquivos do site.
- Executa o `html-validate` e verifica links, âncoras e caminhos de imagens.

Para executar localmente:

```sh
npm ci
npm run lint
npm run validate:site
```

O validador de referências requer Python 3.

## Configuração necessária no GitHub

1. Confirme se o badge aponta para o repositório correto.
2. Em **Settings → Pages**, selecione **GitHub Actions** como origem de publicação.
3. Em **Settings → Branches**, crie uma regra para `main` que exija Pull Request e os dois checks `CI / Lint and validate (Node 18)` e `CI / Lint and validate (Node 20)`. Isso bloqueia o merge quando um check falhar.
4. Em **Settings → Collaborators**, convide `09116428-collab`.
5. Para receber e-mail quando o deploy falhar, configure os Secrets `SMTP_HOST`, `SMTP_PORT` (opcional; padrão 587), `SMTP_USERNAME`, `SMTP_PASSWORD`, `NOTIFY_EMAIL_FROM` e `NOTIFY_EMAIL_TO`. O servidor SMTP precisa aceitar STARTTLS.
6. Após executar os workflows, salve as capturas solicitadas: uma execução de CI falhando por erro de propósito, uma execução de deploy bem-sucedida e a URL publicada no GitHub Pages. Remova o erro de teste antes de integrar à `main`.
