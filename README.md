# AllFix — catálogo de projetos funcionais

Fonte: https://github.com/brad38/AllFix-Repo

A revisão de27/11/2026 contém **108 jogos e137 projetos ativos**, a partir de110 jogos e148 projetos. Os11 projetos retirados estão em registro separado e podem ser reavaliados. Não existe meta artificial de quantidade.

O catálogo oferece ports/recompilações que permitem jogar e possuem fonte ou distribuição oficial verificável. A funcionalidade upstream é independente da disponibilidade ou homologação do GetAll. Um projeto funcional pode permanecer com instalação automática temporariamente indisponível.

## Arquivos

- `catalog.json` — schema4, jogos, projetos, IDs, mídia, plataformas, datas e marcadores de elegibilidade.
- `requirements.json` — schema1, requisitos e procedimento oficial; `scope_review` contém a revisão atual em português. Trechos históricos de README ficam preservados.
- `about.json` — schema1, descrições dos jogos/projetos e revisão atual, sem apresentar descrição editorial como teste.
- `eligibility.json` — schema1, somente projetos ativos, com evidências concretas, limites e procedência.
- `excluded-projects.json` — schema1, projetos fora da loja, motivo, condições de retorno e cópia completa dos metadados anteriores.

A interface é em português brasileiro. Requisitos de compilação são distintos dos de execução. Tags e downloads continuam consultados sob demanda na origem oficial; a revisão de evidências registra versões observadas sem convertê-las em versão dinâmica do catálogo.

## Critérios e revisão

Consulte [a política de elegibilidade](docs/ELIGIBILITY-POLICY.md), [o relatório dos excluídos](docs/audits/eligibility-20261127/EXCLUSOES.md) e [o método/evidências dos148 IDs](docs/audits/eligibility-20261127/README.md).

A inclusão exige evidência específica de jogo em execução: partidas/progressão relatadas no tracker oficial, demos/capturas examinadas, playtests documentados ou outros registros verificáveis. README, percentual de decompilação, release existente, build e fixture sintética não bastam isoladamente. Bugs e limitações documentadas não excluem automaticamente um port jogável.

O GetAll automatiza procedimentos oficiais, com mídia própria quando necessária. Não deve completar motores, gameplay, compiladores de shaders ou runtimes, nem aplicar patches próprios ao código upstream. Os detalhes dessa política estão na instrução do usuário preservada em `docs/INSTALLATION-SCOPE-REQUEST-20261127.md`.

## Descoberta e reavaliação

A rotina de descoberta pesquisa novos projetos e revisita `excluded-projects.json` quando surgem releases, demos ou mudanças de distribuição. Um achado entra primeiro em revisão. Só é admitido após registrar procedência, procedimento oficial e evidência específica de gameplay. A rotina não ativa candidatos ou receitas automaticamente apenas por uma release nova.

O status `available_contract` informa a existência de contrato ativo GetAll. Não comprova instalação com mídia original, boot ou jogabilidade. `temporarily_unavailable` encaminha ao procedimento oficial sem retirar o projeto funcional da loja.

## Datas e ordenação

`games[].release_date` é a data de lançamento da edição original do jogo. `games[].added_at` e `games[].projects[].added_at` são as datas de inclusão no AllFix. Nenhum desses campos é substituído pela data da pesquisa, build ou release do port. Os registros retidos preservam IDs, datas e metadados; a única correção de origem desta revisão é o repositório canônico do Hookshot, documentada no relatório.

O carrossel Adicionados recentemente usa `added_at` do jogo, com desempate por título e ID. As categorias continuam representando uma plataforma de origem por jogo. A fonte das datas históricas está em [RELEASE-DATES.md](RELEASE-DATES.md).

## Validação

```bash
python scripts/validate_catalog.py --require-dates --compare-with 44bdb508842407d501e420457274eb4064f5d935
python -m unittest discover -s tests -v
```

O validador exige correspondência1:1 entre os IDs ativos e os documentos de requisitos, descrições e elegibilidade. Ele impede vazamento do registro de excluídos para a loja, evidência insuficiente e alteração das datas existentes. Os schemas de elegibilidade/exclusão estão em `schemas/`. CI executa os contratos e regressões, sem instalar jogos.

Não houve merge emmain ou publicação de release nesta revisão. A branch é para revisão e teste com catálogo fixado por commit no complemento de desenvolvimento.
