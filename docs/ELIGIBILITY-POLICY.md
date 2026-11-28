# Critérios de inclusão e descoberta

O catálogo ativo contém apenas ports/recompilações com funcionamento comprovado
por evidência específica de execução. A revisão da evidência pública do upstream
é distinta da homologação local de instalação ou gameplay pelo GetAll.

## Classificações

| Código | Significado | Loja ativa |
|---|---|---|
| functional_eligible | Funcional e elegível | Sim |
| functional_with_limitations | Funcional com limitações documentadas | Sim |
| functional_manual_install | Funcional, mas sem automação fiel disponível nesta revisão | Sim, com procedimento oficial |
| unproven | Funcionalidade ou procedência não comprovada após investigação | Não |
| ineligible | Não funcional, decompilação base sem port ou outra inelegibilidade comprovada | Não |

## Evidência e proveniência

Cada admissão precisa de fonte oficial/distribuição verificável, procedimento de
instalação e evidência específica de gameplay. Exemplos: demonstração de gameplay,
relato detalhado de execução/jornada no tracker oficial, playthrough ou teste com
mídia original. Registrar URL, tipo, observação concreta e limites. Screenshots só
contam com contexto que estabeleça gameplay, e não somente a tela inicial.

README, porcentagem de decompilação, presença de release, build que gera EXE,
renderização isolada e testes sintéticos não bastam. Não transformar um link de
vídeo não examinado em relato de teste. Divergências e procedência incerta exigem
investigação adicional; persistindo a lacuna, arquivar para reavaliação.

As limitações de um projeto funcional devem acompanhar sua entrada. Ausência de
boot GetAll não é prova de que o upstream não funciona. Não implementar funções
faltantes, aplicar patches próprios a fontes, trocar renderers/runtimes ou cortar
recursos para satisfazer o catálogo.

## Descoberta e reavaliação

1. Pesquisar projetos novos e rever `excluded-projects.json` quando houver novas
   releases, demonstrações ou fontes. Registrar candidatos antes de admiti-los.
2. Conferir o repositório canônico, a procedência dos componentes e a mídia original
   exigida. Mirrors precisam de vínculo verificável com o autor original.
3. Reunir evidência de gameplay e o método oficial de instalação. Para um projeto
   sem EXE pronto, uma compilação oficial reproduzível de jogo funcional é válida.
4. Atualizar `eligibility.json` e só então colocar projetos elegíveis no catálogo.
   Os validadores rejeitam entradas ativas sem evidência específica.
5. Manter fora da loja os excluídos, preservando ID, fonte, snapshots, motivo,
   evidência, última verificação e condições de reinclusão. A presença de uma
   release nova somente abre uma revisão; nunca reativa automaticamente.
6. Preservar `added_at` e `release_date` dos mantidos. A data de lançamento da edição
   do jogo não é a data de criação/lançamento do port. Usar campo separado e fonte
   explícita quando registrar a data de release do projeto; desconhecida é null.
7. Preservar o carrossel por `games[].added_at` e as opções de ordenação.
8. Executar validação estrutural, evidência, histórico de datas e testes antes do
   commit/PR. Nunca fazer merge ou publicar release automaticamente.

## Instalação

O GetAll pode importar mídia, verificar hashes, provisionar dependências, chamar
geradores/build oficiais e reproduzir o launcher. Se isso ainda exigir modificação
indevida, informar instalação automatizada indisponível e apontar o procedimento
oficial. Não retirar automaticamente um port funcional por essa limitação do GetAll.
