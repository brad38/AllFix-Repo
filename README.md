# AllFix — dados remotos da Loja (schema v4)

Fonte: https://github.com/brad38/AllFix-Repo

Arquivos na raiz:
- **catalog.json**: estrutura principal (111 jogos, 146 projetos, identificadores, plataformas, links dos repositórios, imagens externas, addons); referencias `requirements_file` e `about_file`.
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

- **Gran Turismo 4 — GT4Recomp** (PS2, Windows; ISO SCUS-97328 v2.00 ou Spec II 1.10).
- **Gran Turismo 5 — GT5 Recomp** (PS3, Windows; requer cópia própria e preparação local; Linux experimental).
- **Gran Turismo 7 — RyGT** (PS4, Windows; projeto antigo ryGT7 incorporado ao RyGT).

Os três projetos permanecem com `windows.installation_enabled=false`, sem receitas GetAll. Instalação e jogabilidade não foram homologadas pelo All-Fix.

## Ports promissores incorporados em 23/11/2026

19 projetos adicionados para 17 jogos novos e dois jogos existentes com ports alternativos: God of War (2005) — God of War Recomp, e Forza Horizon (2012) — Forza Horizon 1: ReImagined. Mantidos os projetos originais `gow-pc-port` e `pinyon-shift` e preservadas as fontes oficiais corrigidas de Picori, Team Forever e Leonida.

Novos projetos: LAS Recomp, Super Odyssey PC Recomp, God Hand Rearmed, GTA Stories Recompiled, SpartanPort, The Last Guardian PC, inFAMOUS Second Son PC, P.T. for PC, Gears of War 2 PC Port, Ninja Gaiden II Recompiled, PGR4 Recomp, Burnout 3 Recomp, OpenCE, Lost Odyssey Recomp, SSX Recomp, DKB Recomp e mkw-recomp.

**Curadoria realizada:** descrições editoriais dos 17 jogos revisadas, requisitos e limitações dos 19 ports novos individualizados por projeto e 17/17 jogos com capa e banner preenchidos. Os links de mídias externas não são garantia de disponibilidade permanente, e os estados de jogabilidade são declarados pelos mantenedores, não homologados pelo All-Fix. `windows.installation_enabled=false` para os novos projetos; sem alterações no GetAll, SDK ou Desktop.

## Categorias por plataforma de origem (23/11/2026)

O campo `platform_group` representa **uma única plataforma de origem do port**, sem agrupamentos genéricos de consoles. O validador rejeita valores compostos. Quando um jogo possui diferentes edições, a plataforma é a do projeto portado (por exemplo, `Gran Turismo 7` usa a edição PS4).

Categorias presentes e quantidade de jogos: Android (1), Arcade (1), Game Boy Advance (2), GameCube (8), Nintendo 64 (35), Nintendo Switch (4), Nintendo Switch 2 (2), PlayStation 1 (14), PlayStation 2 (5), PlayStation 3 (1), PlayStation 4 (6), PlayStation 5 (1), SEGA Dreamcast (1), SEGA Mega Drive (1), SNES (4), Wii (1), Wii U (1), Xbox 360 (19) e Xbox Original (4). Android e Arcade são plataformas individuais de origem, não rótulos de múltiplos consoles.

Foram recategorizados 90 jogos, preservando seus IDs e associações de projetos. Correções especiais incluem `The Wind Waker HD` (Wii U), `Mario Strikers Charged` (Wii), `The Minish Cap` (GBA), `Sonic Adventure` (Dreamcast), `Shadow the Hedgehog` (Xbox original) e `Silent Hill: Downpour` (Xbox 360).

**Mídia:** 109 de 111 jogos têm capa e banner. As entradas agrupadas legadas `tomb-raider-i-v` e `sonic-the-hedgehog-1-2-2013` permanecem sem arte única, intencionalmente, para não associar arbitrariamente a capa de um jogo a uma coleção. URLs externas podem mudar; a presença de URLs não garante a disponibilidade futura do arquivo.

**Limites:** não foram executados jogos, compilados projetos externos, validados instaladores, nem criadas receitas GetAll. Os 22 projetos adicionados nos PRs #4 e #5 continuam com `windows.installation_enabled=false`. Os resumos e requisitos em PT-BR foram revisados a partir das fontes dos projetos; não são testes independentes de desempenho ou jogabilidade.
