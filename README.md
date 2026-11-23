# AllFix — dados remotos da Loja (schema v4)

Fonte: https://github.com/brad38/AllFix-Repo

Arquivos na raiz:
- **catalog.json**: estrutura principal (94 jogos, 127 projetos, identificadores, plataformas, links dos repositórios, imagens externas, addons); referencias `requirements_file` e `about_file`.
- **requirements.json**: requisitos por ID do projeto; categorias `system` (sistema), `installation` (instalação/execução), `build` (compilação), `general` (geral). O objeto `source_text` contém as seções ORIGINAIS dos READMEs, na maioria em inglês. Os campos localizados podem permanecer `null` nos registros ainda não traduzidos; não tratar `legacy_reported_pt` como documentação confirmada.
- **about.json**: informações para a aba Sobre, indexadas por ID de jogo e de projeto. As descrições dos projetos em português estão em `description_pt` e são acompanhadas de informações sobre sua verificação; descrições e resumos editoriais não são prova de funcionamento. As descrições dos jogos devem permanecer separadas dos detalhes dos projetos de port e recompilação.

A interface deve ser em português brasileiro. Não apresentar texto inglês cru ao usuário; enquanto faltar tradução de requisitos, exibir aviso em português e um link para a documentação oficial. Não apresentar requisitos desatualizados da pesquisa antiga como verificados. Seções de compilação não são requisitos de execução.

Os dados dinâmicos de repositórios GitHub (nome, descrição, disponibilidade) e as versões/downloads são consultados pela API do GitHub sob demanda, com cache. **Não** incluir tags/releases atuais no catálogo. Projetos de provedores externos requerem integração apropriada.

**Compatibilidade:** o aplicativo que aceita apenas schema v3 precisa ser adaptado antes de usar a versão v4. A divisão em três arquivos é uma mudança intencional do formato de distribuição de dados.

**Importante:** a auditoria original localizou seções relevantes em 99 projetos, mas não revisou manualmente todas as instruções de README/BUILDING. `verification_status=documented_in_readme` significa apenas que o trecho consta no README, não que a instalação tenha sido testada. A tradução de texto técnico completo ainda está pendente, conforme `translation_status`.

## Validação do catálogo

A validação local não instala jogos nem executa código dos projetos catalogados:

```bash
python -m json.tool catalog.json > /dev/null
python -m json.tool requirements.json > /dev/null
python -m json.tool about.json > /dev/null
python scripts/validate_catalog.py
```

O validador confere versões de schema, IDs únicos, URLs de fonte, campos estruturais e correspondência entre jogos, projetos, requisitos e descrições. O workflow `.github/workflows/validate-catalog.yml` executa esses testes em PRs que modificam o catálogo, e verifica também espaços em branco no diff.

A verificação estrutural não substitui a conferência de imagens externas, o teste de execução do jogo nem a homologação do instalador GetAll.

## Ports de Gran Turismo catalogados em 23/11/2026

- **Gran Turismo 4 — GT4Recomp** (Windows; jogo de PS2; requisitos de ISO SCUS-97328 v2.00 ou Spec II 1.10).
- **Gran Turismo 5 — GT5 Recomp** (Windows; recompilação estática de PS3, requer cópia própria e preparação local; Linux experimental).
- **Gran Turismo 7 — RyGT** (Windows; port da versão PS4 CUSA24769; o antigo ryGT7 foi integrado ao RyGT).

Os três projetos iniciam com `windows.installation_enabled=false`, sem receitas GetAll ou homologação no All-Fix. A disponibilidade de ferramentas não significa que o jogo original seja distribuído nem que a instalação tenha sido testada.
