# AllFix — dados remotos da Loja (schema v4)

Fonte: https://github.com/brad38/AllFix-Repo

Arquivos na raiz:
- **catalog.json**: estrutura principal (108 jogos, 143 projetos, identificadores, plataformas, links dos repositórios, imagens externas, addons); referencias `requirements_file` e `about_file`.
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

## Novos ports promissores (23/11/2026)

Foram adicionados **19 projetos**, incluindo **17 jogos novos** e dois projetos alternativos para **God of War (2005)**, que permanece uma única entrada com múltiplos ports. Entre eles: LAS Recomp, Super Odyssey PC Recomp, God Hand Rearmed, GTA Stories Recompiled, SpartanPort, The Last Guardian PC, inFAMOUS Second Son PC, P.T. for PC, Gears of War 2 PC Port, Ninja Gaiden II Recompiled, PGR4 Recomp, Burnout 3 Recomp, OpenCE, Lost Odyssey Recomp, SSX Recomp, DKB Recomp e mkw-recomp e Forza Horizon 1: ReImagined (segundo projeto de Forza Horizon, ao lado do Pinyon Shift).

**Escopo:** somente catalogação; `windows.installation_enabled=false` em todos os novos projetos. A disponibilidade de releases e a jogabilidade não foram verificadas localmente. Descrições editoriais dos novos jogos e mídias (`cover` e `banner`) ainda precisam de curadoria; os campos de mídia ficam `null` em vez de apontar para imagens não verificadas. As seções de requisitos incluem trechos dos READMEs originais e resumos provisórios em português, pendentes de revisão técnica. Nenhum jogo ou ROM é distribuído.
