# Revisão de elegibilidade — 27/11/2026

Foram revisados os 148 IDs do catálogo no commit `44bdb508842407d501e420457274eb4064f5d935`. `reviewed-projects.json` preserva as observações, URLs, limites e classificação inicial por projeto. A revisão documental não executou jogos comerciais e não equivale à homologação de instalação pelo GetAll.

As fontes incluem relatos de partidas e progressão no tracker oficial, demonstrações e capturas inspecionadas, playtests do autor e corridas publicadas. README, existência de release, build e teste sintético não foram suficientes isoladamente. Quando uma fonte estava indisponível, a pendência foi registrada sem concluir que o port nunca funcionou.

`eligibility.json` na raiz contém somente os ativos. `excluded-projects.json` guarda metadados completos, motivos e condições de reavaliação. As classificações finais também consideram a disponibilidade de automação após a retirada de intervenções indevidas. Essa disponibilidade não comprova mídia original, boot ou gameplay pelo GetAll.

## Reprodução

```bash
python scripts/apply_review_20261127.py --getall-index ../getall-scope-20261127/index.json
python scripts/validate_catalog.py --require-dates --compare-with 44bdb508842407d501e420457274eb4064f5d935
python -m unittest discover -s tests -v
```

A reprodução usa decisões documentadas de curadoria. Não decide jogabilidade por palavras-chave. Os IDs, datas e snapshots são conferidos contra o baseline. Links e versões podem mudar; os hashes identificam o material observado quando disponíveis.

## Escopo das evidências preservadas

Os registros JSON guardam as fontes, as observações e seus limites. Hashes de snapshots brutos herdados da pesquisa anterior foram mantidos, mas as cópias correspondentes não foram localizadas no workspace retomado. Esses hashes não devem ser apresentados como prova de que o arquivo bruto continua disponível.

A reconferência adicional está em `source-followup-20261127.json`, com URLs fixadas por commit quando possível, hashes efetivamente calculados, tamanhos e conclusões limitadas. Nenhum asset do jogo ou runtime foi obtido para produzir esse registro.

## Casos reavaliados na integração

- **Hookshot:** fonte corrigida para ItsNotRexed/Hookshot. O ZIP e os componentes oficiais foram identificados por manifesto e hashes. Não foi encontrado bypass de shaders no caminho Hookshot inspecionado.
- **Project 2099:** runtime Beta5, instalador e avisos internos existem. O diretório do ZIP e registros EOTP foram inspecionados por faixas HTTP. A pendência é a procedência dos recursos completos de substituição, não a existência de launcher.
- **P.T.:** foi recuperado um relato primário de exploração e interação com a lanterna e o banheiro, com resposta do mantenedor na issue 10.
- **Burnout 3:** há execução interativa oficial. A retirada temporária decorre das corridas a 2–4 FPS e da ausência de persistência documentadas, não de ausência de runtime.
- **GT5:** além dos relatos com Master Mod, foi conferido o relatório upstream de uma sessão com disco europeu 01.00 e configuração padrão. O escopo, o hardware e a contagem real de frames estão identificados; o teste não foi reproduzido pelo GetAll.
- **Vandal Hearts:** o NOTICE distingue a licença do código próprio dos dados derivados incorporados nos binários. A fonte oferece geração local com arquivos próprios. A receita binária não demonstra esse caminho, portanto deve permanecer suspensa até sua substituição por um procedimento oficial verificado.
- **REDRIVER2:** a issue 234 pergunta a procedência dos dados extras em `data/DRIVER2` e ainda não possui resposta. Há prova de jogabilidade e fonte disponível; a receita do pacote completo precisa resolver essa pendência antes da reativação.

## Continuidade do registro

A revisão mantém 108 jogos e 137 projetos ativos; os 11 excluídos continuam registrados para reavaliação. Os validadores também verificam que exclusões anteriores não desapareçam e que a reinclusão não altere artificialmente as datas de entrada.

O estado available_contract registra um contrato ativo; testes sintéticos e builds de ferramentas não demonstram instalação com mídia original. A matriz GetAll registra separadamente as etapas e as evidências de cada projeto.

## Procedimentos oficiais conferidos na continuação

[PROCEDIMENTOS-OFICIAIS.md](PROCEDIMENTOS-OFICIAIS.md) descreve os procedimentos investigados, comandos, saídas e limites. Os JSON associados preservam commits, hashes, logs e provas. SoH, SM e sm_rewrite compilaram ferramentas ou executáveis sem alterar fontes; Double Dash compilou o alvo runtime_check; o modo lib e o launcher GT5 passaram. Esses resultados não comprovam mídia original, primeiro boot ou gameplay.

O snapshot final de 28/11/2026 tem 130 projetos funcionais com limitações, 3 com instalação manual e 4 elegíveis sem ressalva específica. Permanecem 108 jogos, 137 projetos ativos e 11 arquivados. O índice GetAll usado contém 146 receitas, das quais 134 estão ativas e 12 desativadas; seu SHA-256 está em revision-summary.json.

Os três projetos sem contrato ativo são StrikersRecomp, Vandal Hearts e REDRIVER2. Os bloqueios concretos e as condições para restaurar a automação estão preservados no relatório, sem excluir a funcionalidade upstream desses projetos.

O vídeo de Dr. Mario 64 de Video Game Esoterica foi atribuído ao fork theboy181/drmario64_recomp_plus, mantido no catálogo. A referência cruzada no registro excluído AngheloAlf/drmario64_recomp impede transferir indevidamente essa evidência ao projeto base.
