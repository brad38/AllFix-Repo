# AllFix â€” catalogo remoto (schema v3)

Catalogo publico: https://raw.githubusercontent.com/brad38/AllFix-Repo/main/catalog.json

## Estrutura
- Um unico arquivo JSON: 87 jogos e 119 projetos.
- `games`: dados estaticos de curadoria por jogo.
- `projects[].source`: links oficiais e identificador GitHub, quando disponivel.
- `projects[].fallback_name`: rotulo de reserva; nome e descricao atuais de projetos GitHub sao consultados via GET /repos/{owner}/{repo}.
- `projects[].documentation.requirements`: `system`, `installation`, `build` e `general` com **trechos da documentacao oficial**. `source_url` e `evidence` indicam a fonte e os titulos das secoes de origem.
- `verification_status: documented_in_readme`: evidencia foi localizada no README (NAO significa que o projeto roda, que a instalacao foi testada ou que os requisitos estejam completos).
- `verification_status: pending_review`: o README nao foi acessivel ou nao havia secoes de requisitos explicitamente identificadas. Nao assumir que nao existem requisitos.
- `legacy_unverified`: material de pesquisa anterior preservado, nao tratar como confirmado.
- `windows.installation_enabled`: false ate validacao funcional.
- Versoes e assets consultados ao vivo via GitHub Releases, nao no catalogo.
- Capas/banners/screenshot de fontes externas. Sem ratings fabricados.

## Auditoria de README â€” 2026-11-22
Foram analisados automaticamente 119 registros; 114 READMEs oficiais encontrados por URL GitHub RAW (HEAD) e 5 sem README GitHub acessivel pela rota de catalogo (inclui URLs externas). O extrator identificou somente secoes rotuladas e preservou a evidencia textual. **Campos pendentes exigem revisao manual**, especialmente quando requisitos estao fora do README, em arquivos BUILDING/INSTALL ou outras paginas. Uma secao Building e apenas requisito de compilacao, nao de execucao.

## Descoberta futura
Ao adicionar novos projetos, ler README/docs oficiais, separar requisitos de sistema/instalacao/compilacao, registrar fonte, nao inferir hardware e nao confundir ferramentas de build com dependencias de execucao. Validar IDs e URLs sem remover dados preexistentes.
