# AllFix ? catalogo remoto

Fonte publica de dados: https://raw.githubusercontent.com/brad38/AllFix-Repo/main/catalog.json

## Schema v3
- Um unico `catalog.json`, com 87 jogos e 119 projetos.
- `games[]`: dados editoriais estaticos por jogo; `cover`, `banner`, `screenshots` usam fontes externas, atualmente nao preenchidas.
- `games[].projects[].source`: URL oficial, provedor e identificador GitHub (quando existe). **115 projetos GitHub e 4 fontes externas/sem repositorio GitHub individual identificado.**
- `fallback_name`: rotulo apenas para falha da API ou fonte externa. Para projetos GitHub, buscar nome/descricao atuais via GitHub REST API GET /repos/{owner}/{repo}.
- `documentation.requirements`: texto, URL-fonte, estado de verificacao e data. Estao pendentes de revisao; nao alegar que foram confirmados no README.
- `legacy_unverified`: anotacoes e observacoes de pesquisa anterior, preservadas para revisao. **Nao exibir como dados atuais/confirmados**.
- `windows.installation_enabled` = false ate verificacao de instalacao.
- Releases e assets Windows: consultar GitHub Releases API sob demanda; nao armazenar tag atual no catalogo.
- Nenhuma avaliacao disponivel: ocultar estrelas/rating em vez de atribuir nota baixa.

**Incompatibilidade:** clientes que exigem `schema_version=2` devem ser migrados antes de usar esta versao v3.

## Inclusao de novos projetos
Deduplicar por URL canonica do repositorio e por ID; associar a jogo existente ou cadastrar novo jogo; ler README/documentacao para requisitos de execucao no Windows; preencher `documentation.requirements` apenas quando houver fonte explicita, com URL e estado verificado; caso contrario manter pendente. Nao confundir instrucoes de build com requisitos para executar. Preservar os dados existentes e validar contagens/JSON antes de publicar.
