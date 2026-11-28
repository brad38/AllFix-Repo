# AllFix — catálogo de projetos funcionais

Fonte: https://github.com/brad38/AllFix-Repo

A revisão de 27/11/2026 contém **108 jogos e 137 projetos ativos**, a partir de 110 jogos e 148 projetos. Os 11 projetos retirados ficam em um registro separado para reavaliação. Não existe meta artificial de quantidade.

O catálogo oferece ports e recompilações que permitem jogar e possuem fonte ou distribuição oficial verificável. A funcionalidade upstream é independente da disponibilidade ou homologação do GetAll. Um projeto funcional pode permanecer com instalação automática temporariamente indisponível.

## Arquivos

- `catalog.json` — schema 4: jogos, projetos, IDs, mídia, plataformas, datas e marcadores de elegibilidade.
- `requirements.json` — schema 1: requisitos e procedimento oficial; `scope_review` contém a revisão atual em português. Trechos históricos de README ficam preservados.
- `about.json` — schema 1: descrições dos jogos e projetos, com revisão atual. Texto editorial não representa um teste.
- `eligibility.json` — schema 1: somente projetos ativos, com evidências concretas, limites e procedência.
- `excluded-projects.json` — schema 1: projetos fora da loja, motivos, condições de retorno e cópia completa dos metadados anteriores.

A interface é em português brasileiro. Requisitos de compilação são distintos dos requisitos de execução. Tags e downloads continuam consultados sob demanda na origem oficial; a revisão de evidências registra versões observadas sem convertê-las em versão dinâmica do catálogo.

## Critérios e revisão

Consulte [a política de elegibilidade](docs/ELIGIBILITY-POLICY.md), [o relatório dos excluídos](docs/audits/eligibility-20261127/EXCLUSOES.md) e [o método e as evidências dos 148 IDs](docs/audits/eligibility-20261127/README.md).

A inclusão exige evidência específica de jogo em execução: partidas ou progressão relatadas no tracker oficial, demonstrações e capturas examinadas, playtests documentados ou outros registros verificáveis. README, percentual de decompilação, presença de release, build e teste sintético não bastam isoladamente. Bugs e limitações documentadas não excluem automaticamente um port jogável.

O GetAll automatiza procedimentos oficiais, com mídia própria quando necessária. Não deve completar motores, gameplay, compiladores de shaders ou runtimes, nem aplicar patches próprios ao código upstream. A política completa está na [instrução do usuário preservada](docs/INSTALLATION-SCOPE-REQUEST-20261127.md).

A origem oficial de um pacote não transfere automaticamente a licença do código aos dados do jogo. Quando a receita ainda não consegue demonstrar a procedência dos componentes que distribui, ela fica indisponível até existir um caminho oficial verificado. O projeto pode permanecer no catálogo quando sua fonte e funcionalidade são verificáveis.

## Descoberta e reavaliação

A rotina de descoberta pesquisa novos projetos e revisita `excluded-projects.json` quando surgem releases, demonstrações ou fontes. Um achado entra primeiro em revisão. A admissão exige procedência, procedimento oficial e evidência específica de gameplay. Uma release nova não ativa automaticamente candidatos ou receitas.

O estado `available_contract` informa a existência de contrato ativo GetAll. Não comprova instalação com mídia original, boot ou jogabilidade, e pode incluir uma etapa parcial de preparação. `temporarily_unavailable` aponta ao procedimento oficial enquanto a automação fica suspensa.

## Datas e ordenação

`games[].release_date` é a data de lançamento da edição original do jogo. `games[].added_at` e `games[].projects[].added_at` são as datas de inclusão no AllFix. Nenhum desses campos é substituído pela data da pesquisa, build ou release do port.

Os registros mantidos preservam IDs, datas e metadados. A correção de origem do Hookshot para o mantenedor canônico está documentada no relatório. Reincluir um projeto exige preservar as datas originais guardadas no arquivo histórico.

O carrossel Adicionados recentemente usa `added_at` do jogo, com desempate por título e ID. As categorias continuam representando uma plataforma de origem por jogo. A fonte das datas históricas está em [RELEASE-DATES.md](RELEASE-DATES.md).

## Validação

```bash
python scripts/validate_catalog.py --require-dates --compare-with 44bdb508842407d501e420457274eb4064f5d935
python -m unittest discover -s tests -v
```

O validador exige correspondência 1:1 entre os IDs ativos e os documentos de requisitos, descrições e elegibilidade. A comparação histórica impede remover projetos sem preservar seus metadados completos, apagar exclusões já registradas ou redefinir datas ao reincluir projetos. Também rejeita vazamento de excluídos para a loja e evidência insuficiente.

Os schemas de elegibilidade e exclusão estão em `schemas/`. CI executa os contratos e regressões, sem instalar jogos, e compara o histórico com a base do PR ou o commit anterior da branch.

Esta revisão permanece em uma branch de trabalho, com catálogo fixado por commit no complemento de desenvolvimento.
