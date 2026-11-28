# Revisão de elegibilidade — 27/11/2026

Foram revisados os148 IDs do catálogo no commit44bdb508842407d501e420457274eb4064f5d935. `reviewed-projects.json` preserva as observações concretas, URLs, limites e classificação inicial por projeto. A revisão não executou jogos comerciais nem equivale a homologação GetAll.

As fontes incluem relatos de partidas/progressão no tracker oficial, demonstrações/capturas inspecionadas, registros de playtests do autor e corridas publicadas. README, release existente, build e teste sintético não foram suficientes isoladamente. Onde a fonte estava indisponível, o resultado é uma pendência específica, sem concluir que o port nunca existiu.

`eligibility.json` na raiz contém somente os ativos. `excluded-projects.json` guarda metadados completos, motivos e condições de reavaliação. As classificações finais consideram também disponibilidade da automação após a retirada de intervenções indevidas. Essa disponibilidade não comprova mídia original, boot ou gameplay do GetAll.

## Reprodução

```bash
python scripts/apply_review_20261127.py --getall-index ../getall-scope/index.json
python scripts/validate_catalog.py --require-dates --compare-with 44bdb508842407d501e420457274eb4064f5d935
python -m unittest discover -s tests -v
```

A reprodução usa decisões documentadas de curadoria. Não decide jogabilidade por palavras-chave. Links e versões podem mudar; os hashes/IDs registrados identificam o material observado quando disponíveis. Dados pessoais irrelevantes de discussões não foram incorporados.

## Casos reavaliados na integração

- Hookshot: fonte corrigida para ItsNotRexed/Hookshot. O ZIP e os componentes oficiais foram identificados por manifesto/hashes. Não foi encontrado bypass de shaders no caminhoHookshot; essa hipótese foi descartada.
- Project2099: runtimeBeta5, instalador e avisos internos existem. O ZIP foi inspecionado por faixasHTTP, sem transferir o pacote inteiro. A pendência diz respeito à procedência documentada dos recursos, não à existência de launcher.
- P.T.: além das publicações de vídeo, foi recuperado relato primário de exploração/interação com lanterna e banheiro, com resposta do mantenedor naissue10.
- Burnout3: há execução interativa oficial. A decisão de mantê-lo em reavaliação decorre do estágio de corridas2–4FPS e ausência de persistência documentados, não de ausência de runtime.
