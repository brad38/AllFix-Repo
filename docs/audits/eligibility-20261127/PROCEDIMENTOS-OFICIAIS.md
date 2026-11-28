# Procedimentos oficiais de instalação — 28/11/2026

Procedimentos oficiais conferidos na continuação: rotas restauradas, ferramentas compiladas e bloqueios concretos. Instalação com mídia original, boot e gameplay são evidências separadas.

Os resultados descrevem o ponto efetivamente verificado. Um build de ferramenta ou teste sintético não demonstra mídia original, boot ou gameplay. O contrato GetAll é registrado separadamente no índice fixado em revision-summary.json.

## sm64ex

MSYS2 MINGW64 com pacotes oficiais da wiki; ROM própria baserom.us.z64; make EXTERNAL_DATA=1.

**Saída prevista:** build/us_pc/sm64.us.<microcode>.exe e recursos externos correspondentes.

**Resultado e limite:** MSYS2 oficial privado e o alvo make -C tools -j2 all passaram com fontes rastreadas intactas; ROM ausente foi rejeitada. Novo contrato executa o procedimento oficial com mídia própria, sem reativar o perfil histórico com patches. Build final dependente de ROM, boot e gameplay não foram testados.

Fontes: [README.md](https://raw.githubusercontent.com/sm64pc/sm64ex/d7ca2c04364a6dd0dac58b47151e04e26887e6f0/README.md), [Makefile](https://raw.githubusercontent.com/sm64pc/sm64ex/d7ca2c04364a6dd0dac58b47151e04e26887e6f0/Makefile).

## render96ex

Compilar fonte oficial com a ROM própria e procedimento da wiki Windows; opções EXTERNAL_DATA=1/DynOS previstas no upstream. ModelPack/texture pack somente das fontes indicadas pelo autor.

**Saída prevista:** build/us_pc, pacote oficial Render96_DynOs_v3.0.7z em dynos/packs; texturas opcionais em res/gfx.

**Resultado e limite:** MSYS2 oficial privado e o alvo make -C tools -j2 all passaram com fontes rastreadas intactas; ROM ausente foi rejeitada. Novo contrato executa o procedimento oficial com mídia própria, sem reativar o perfil histórico com patches. Build final dependente de ROM, boot e gameplay não foram testados.

Fontes: [README.md](https://raw.githubusercontent.com/Render96/Render96ex/48da5c491c8abfb2f5192b59278c1c269411e533/README.md), [Makefile](https://raw.githubusercontent.com/Render96/Render96ex/48da5c491c8abfb2f5192b59278c1c269411e533/Makefile).

## sm64rt

Procedimento sm64ex/MSYS2, com RENDER_API=RT64 EXTERNAL_DATA=1 e RT64 oficial incluído na versão.

**Saída prevista:** Executável em build/us_pc com dependências RT64 correspondentes; Windows 10 2004+, GPU DXR e runtime VC++ documentados.

**Resultado e limite:** MSYS2 oficial privado e o alvo make -C tools -j2 all passaram com fontes rastreadas intactas; ROM ausente foi rejeitada. Novo contrato executa o procedimento oficial com mídia própria, sem reativar o perfil histórico com patches. Build final dependente de ROM, boot e gameplay não foram testados.

Fontes: [README.md](https://raw.githubusercontent.com/DarioSamo/sm64rt/20e618b75ae4a6810bd92ac6a937cb167517aac5/README.md), [Makefile](https://raw.githubusercontent.com/DarioSamo/sm64rt/20e618b75ae4a6810bd92ac6a937cb167517aac5/Makefile).

## sm

MSBuild sm.sln /restore /p:RestorePackagesConfig=true /p:Configuration=Release /p:Platform=x64. Solução upstream v143 e SDL2 NuGet 2.26.3.

**Saída prevista:** build/bin-x64-Release/sm.exe e SDL2.dll; sm.ini oficial e ROM própria sm.smc ao lado da instalação conforme upstream.

**Resultado e limite:** Build MSVC real sem ROM passou, com 124 fontes intactas. Novo perfil sm-official-msvc-source-578f90b exige ROM válida antes da compilação e usa a solução oficial. Prova negativa sem ROM abre a mensagem modal upstream e foi encerrada por timeout; isso não conta como boot aprovado.

Fontes: [BUILDING.md](https://raw.githubusercontent.com/snesrev/sm/578f90b3cc49557bb70060ad033bb90b8cf8ac50/BUILDING.md), [README.md](https://raw.githubusercontent.com/snesrev/sm/578f90b3cc49557bb70060ad033bb90b8cf8ac50/README.md), [src/sm.vcxproj](https://raw.githubusercontent.com/snesrev/sm/578f90b3cc49557bb70060ad033bb90b8cf8ac50/src/sm.vcxproj), [src/sm.vcxproj.filters](https://raw.githubusercontent.com/snesrev/sm/578f90b3cc49557bb70060ad033bb90b8cf8ac50/src/sm.vcxproj.filters).

## sm-rewrite

Visual Studio 2022/CMake/vcpkg: cmake --preset windows-relwithdebinfo; cmake --build build-windows-relwithdebinfo. Preset e CMake são do upstream.

**Saída prevista:** build-windows-relwithdebinfo/sm.exe, SDL2.dll e sm.ini oficial; ROM própria em runtime.

**Resultado e limite:** Build MSVC real passou com 193 fontes intactas, baseline vcpkg oficial 7f9f0e44db287e8e67c0e888141bfa200ab45121 e SDL2 2.30.0. Sem ROM o executável retorna erro/exit1. Novo perfil sm-rewrite-official-msvc-source-5237873 preserva fontes/configuração. Nenhuma mídia original, boot ou gameplay testados.

Fontes: [BUILDING.md](https://raw.githubusercontent.com/testyourmine/sm_rewrite/523787384a7c912153883b21714f5edabf4e2406/BUILDING.md), [CMakePresets.json](https://raw.githubusercontent.com/testyourmine/sm_rewrite/523787384a7c912153883b21714f5edabf4e2406/CMakePresets.json), [README.md](https://raw.githubusercontent.com/testyourmine/sm_rewrite/523787384a7c912153883b21714f5edabf4e2406/README.md).

## ship-of-harkinian-soh

Torch standalone oficial no submódulo 2ab12fe9660aec04e02ee89fe81baed304a1a1d6, com opções de formato do Shipwright 9.3.1. torch.exe o2r ROM.z64 -s assets -d output -u 9.3.1.

**Saída prevista:** oot.o2r ou oot-mq.o2r conforme config; verificar version e portVersion antes de concluir.

**Resultado e limite:** Wrapper soh-torch 9.3.1 falha em C2664; alternativa standalone compilou intacta e 7 checks sintéticos passaram. Hash não reconhecido retorna exit0 sem archive: a instalação deve validar saída. Nenhuma ROM original, boot ou gameplay testados.

Fontes: [fonte oficial](https://github.com/HarbourMasters/Shipwright/blob/f0599f96f8d442f26d0fa1c5cedafddacd56633f/CMakeLists.txt), [fonte oficial](https://github.com/HarbourMasters/Torch/blob/2ab12fe9660aec04e02ee89fe81baed304a1a1d6/src/main.cpp).

## strikersrecomp

Procedimento upstream: bootstrap.sh, tools/generate.py com ISO própria; módulo RecompCore ou build standalone nos hosts oficialmente documentados. Não foi afirmado que o projeto seja impossível de compilar no Windows.

**Saída prevista:** Módulo gG4QE01_recomp; RecompCore com CPUCore=6. Fontes geradas da mídia permanecem locais.

**Resultado e limite:** O bootstrap oficial fixa GXRuntime v0.1.0, mas essa versão exporta DolRuntime enquanto o Strikers exige GXRuntime. A embalagem RecompCore oficial não contempla .dll no Windows e o GXRuntime lista suporte Windows no roadmap. A integração anterior recorria a alterações próprias; não há contrato Windows íntegro validado nesta revisão. Condição para restaurar: Validar uma combinação oficial compatível de dependências e embalagem Windows, ou integrar um ambiente oficialmente suportado sem modificar código/runtime do jogo.

Fontes: [README.md](https://raw.githubusercontent.com/aharonahdoot/StrikersRecomp/cd88f71f5a836c103484c038454b4143000d883c/README.md), [bootstrap.sh](https://raw.githubusercontent.com/aharonahdoot/StrikersRecomp/cd88f71f5a836c103484c038454b4143000d883c/bootstrap.sh), [patches/README.md](https://raw.githubusercontent.com/aharonahdoot/StrikersRecomp/cd88f71f5a836c103484c038454b4143000d883c/patches/README.md), [tools/generate.py](https://raw.githubusercontent.com/aharonahdoot/StrikersRecomp/cd88f71f5a836c103484c038454b4143000d883c/tools/generate.py), [tools/package_module.sh](https://raw.githubusercontent.com/aharonahdoot/StrikersRecomp/cd88f71f5a836c103484c038454b4143000d883c/tools/package_module.sh).

## mkdd-recomp

ciso_extract.py; Ghidra 12.1.4 + GameCubeLoader 1.3.0 + ghidra-cli 0.2.2; ExportSheets/ExportPcode; build_sheets/import_symbols/build_sheets/gen_rust; play.bat.

**Saída prevista:** Crates Rust gerados localmente, mkdd-bevy e ROM/disco via MKDD_DISC ou rust/disc.txt. Rust 1.98 e Bevy 0.19.1 documentados.

**Resultado e limite:** Repositório omite código/dados derivados da mídia. Pipeline Ghidra exige projeto/programa/configuração reais. Não foi reproduzido integralmente com disco; inserir IL customizada ou corrigir gerador no AllFix não é alternativa fiel.

Fontes: [README.md](https://raw.githubusercontent.com/LeftInWalmart/MKDD-Recomp/e173ce40a70eab4830f98ccd9dfdf1ac0d683657/README.md), [play.bat](https://raw.githubusercontent.com/LeftInWalmart/MKDD-Recomp/e173ce40a70eab4830f98ccd9dfdf1ac0d683657/play.bat).

## gt5-recomp

Carregar GT5-Installer.bat oficial em modo lib, consultar componentes/licenças e executar Invoke-Engine intacto após os aceites necessários e seleção da mídia própria. O launcher oficial GT5Launcher.exe fornece o lançamento --play.

**Saída prevista:** GT5/input/EBOOT.elf, GT5/vfs, executáveis e launcher construídos pelo upstream; jogo base 01.00 BCES00569/BCUS98114.

**Resultado e limite:** Modo lib e build-launcher.ps1 passaram num caminho com espaços e acentos; 254 fontes permaneceram iguais. A consulta retornou os componentes Microsoft/NVIDIA conforme os pré-requisitos, sem instalar nada nem executar o engine. Não houve mídia original, extração completa, runtime, boot ou gameplay.

Fontes: [GT5-Installer.bat](https://raw.githubusercontent.com/MormonFTP-hub/gt5-recomp/64ca1697c5f9bb513bfe0414d9a36c10dafd0a37/GT5-Installer.bat), [launcher/build-launcher.ps1](https://raw.githubusercontent.com/MormonFTP-hub/gt5-recomp/64ca1697c5f9bb513bfe0414d9a36c10dafd0a37/launcher/build-launcher.ps1), [GT5/play.bat](https://raw.githubusercontent.com/MormonFTP-hub/gt5-recomp/64ca1697c5f9bb513bfe0414d9a36c10dafd0a37/GT5/play.bat), [README.md](https://raw.githubusercontent.com/MormonFTP-hub/gt5-recomp/64ca1697c5f9bb513bfe0414d9a36c10dafd0a37/README.md).

## god-of-war-recomp

tools/iso_extract.py da ISO SCUS-97399 própria, preservando o layout calculado pelo autor; scripts/compilar.ps1 oficial em ambiente vcvars64 MSVC/CMake/Ninja; scripts/ejecutar.ps1 no lançamento. PS2Recomp c5a9d02 e patches versionados pelo autor permanecem intactos.

**Saída prevista:** GOW_WORK/out/build ou build-clang/ps2EntryRunner.exe, game com SCUS_973.99, IRX, PART1/PART2.PAK e .disc_layout; scripts/3_ejecutar_manual.cmd inicia o runtime.

**Resultado e limite:** Contrato novo implementa a sequência oficial e verifica os arquivos extraídos contra a ISO, os metadados .disc_layout/.disc_meta, os fontes originais e o executável selecionado. A validação estrutural sintética não comprova mídia comercial, build final, boot ou gameplay. Instalar ferramentas Microsoft ausentes depende de aceite explícito.

Fontes: [README.es.md](https://raw.githubusercontent.com/KIexster/god-of-war-recomp/d1d11ec545c3baf2f3fc17e2df4247ac4b732d5c/README.es.md), [README.md](https://raw.githubusercontent.com/KIexster/god-of-war-recomp/d1d11ec545c3baf2f3fc17e2df4247ac4b732d5c/README.md), [README.pt-BR.md](https://raw.githubusercontent.com/KIexster/god-of-war-recomp/d1d11ec545c3baf2f3fc17e2df4247ac4b732d5c/README.pt-BR.md), [game/README.md](https://raw.githubusercontent.com/KIexster/god-of-war-recomp/d1d11ec545c3baf2f3fc17e2df4247ac4b732d5c/game/README.md).

## mariokartdd-recomp

Clang/MSVC/SDK, CMake/Ninja e Python oficiais; submódulo gcn-recomp b2193d7; ISO própria GM4E01 em rom/game.iso; build.ps1 intacto. Nenhum renderer/frontend removido, GCN_OPENXR=ON e GCN_BENCH_ONLY=OFF.

**Saída prevista:** build/mkdd.exe, build/main.dol SHA-1 e389e50357d4a5076ab3d38672204658f411123d e ROM própria preservada. Lançar build/mkdd.exe rom/game.iso a partir da raiz para não depender do caminho antigo de staging.

**Resultado e limite:** runtime_check oficial passou com 42 objetos e 165 fontes intactas, usando LLVM 23.1.3/MSVC 14.44. Clang 18 incompatível foi registrado sem bypass. extract_dol.py rejeita ISO sintética de SHA-1 errado. Nenhum link final do jogo, build OpenXR, mídia original, boot ou gameplay. Não confundir este projeto ethannicholas com o ID mkdd-recomp/LeftInWalmart.

Fontes: [.gitmodules](https://raw.githubusercontent.com/ethannicholas/mariokartdd-recomp/bd36eb982ea58c6651584cc48264876d1aba9546/.gitmodules), [CMakeLists.txt](https://raw.githubusercontent.com/ethannicholas/mariokartdd-recomp/bd36eb982ea58c6651584cc48264876d1aba9546/CMakeLists.txt), [LICENSE](https://raw.githubusercontent.com/ethannicholas/mariokartdd-recomp/bd36eb982ea58c6651584cc48264876d1aba9546/LICENSE), [README.md](https://raw.githubusercontent.com/ethannicholas/mariokartdd-recomp/bd36eb982ea58c6651584cc48264876d1aba9546/README.md), [build.ps1](https://raw.githubusercontent.com/ethannicholas/mariokartdd-recomp/bd36eb982ea58c6651584cc48264876d1aba9546/build.ps1), [build.sh](https://raw.githubusercontent.com/ethannicholas/mariokartdd-recomp/bd36eb982ea58c6651584cc48264876d1aba9546/build.sh).

## vandalhearts-pcport

CMake VH_PSX_EXE + VH_KROM_SOURCE, mantendo VH_WEBP/VH_HDVIDEO ligados. A fonte atual pode ler diretamente PS-X EXE sem ELF/PsyQ; o gerador aceita BIOS próprio e valida o hash da região de fonte. A embalagem unificada oficial compila os dois cores regionais US/JP e usa libav estático.

**Saída prevista:** Executável e dados gerados de PS-X EXE/BIOS próprios, preservando WebP, HD video e cores regionais previstos pelo upstream.

**Resultado e limite:** O NOTICE declara dados do jogo/BIOS incorporados nos binários. A alternativa fonte foi verificada e usa executável PS-X e BIOS próprios; o teste nativo CMake intacto falhou na criação obrigatória de symlinks por falta de privilégio. O procedimento Windows documentado usa cross-compilação Linux/macOS e dependências próprias, ainda sem integração validada no Desktop. Condição para restaurar: Integrar e verificar ambiente oficial de compilação que suporte o staging de symlinks, gerando todos os dados necessários exclusivamente das mídias/BIOS fornecidos pelo usuário. Não substituir por binário que já incorpora esses dados.

Fontes: [LICENSE](https://raw.githubusercontent.com/HalmyLyseas/VandalHearts-PcPort/14552fffa0e0b47e02b57592e274fc6e7a649923/LICENSE), [NOTICE](https://raw.githubusercontent.com/HalmyLyseas/VandalHearts-PcPort/14552fffa0e0b47e02b57592e274fc6e7a649923/NOTICE), [README.md](https://raw.githubusercontent.com/HalmyLyseas/VandalHearts-PcPort/14552fffa0e0b47e02b57592e274fc6e7a649923/README.md), [docs/building.md](https://raw.githubusercontent.com/HalmyLyseas/VandalHearts-PcPort/14552fffa0e0b47e02b57592e274fc6e7a649923/docs/building.md), [docs/cross-platform.md](https://raw.githubusercontent.com/HalmyLyseas/VandalHearts-PcPort/14552fffa0e0b47e02b57592e274fc6e7a649923/docs/cross-platform.md), [platform/pc/Makefile](https://raw.githubusercontent.com/HalmyLyseas/VandalHearts-PcPort/14552fffa0e0b47e02b57592e274fc6e7a649923/platform/pc/Makefile).

## redriver2

Método Windows oficial com ambos CDs próprios, launcher Java ou _convert_cd_fmv_xa.bat. A via de fonte VS2019/premake permanece documentada, porém sua embalagem usa o mesmo diretório de dados; não foi verificada uma rota que derive todos os extras dos discos.

**Saída prevista:** Executável oficial, mídia de ambos CDs e extras de data/DRIVER2 com procedência ou reconstrução documentada.

**Resultado e limite:** A compilação oficial copia os mesmos 76 arquivos rastreados data/DRIVER2 ao pacote. Os conversores oficiais geram apenas vídeo e áudio da mídia própria; não fornecem reconstrução dos extras LANG/GFX/GAL/REPLAYS questionados na issue234. Compilar somente o executável não resolve a lacuna de procedência desses dados. Condição para restaurar: Documentar a procedência dos extras ou validar uma reconstrução oficial desses dados a partir das mídias próprias, preservando as funcionalidades do upstream.

Fontes: [.appveyor/AfterBuild.bat](https://raw.githubusercontent.com/OpenDriver2/REDRIVER2/acca6b139302dd72c1fbff52556f3493aafda2dd/.appveyor/AfterBuild.bat), [.appveyor/AfterBuild.sh](https://raw.githubusercontent.com/OpenDriver2/REDRIVER2/acca6b139302dd72c1fbff52556f3493aafda2dd/.appveyor/AfterBuild.sh), [.appveyor/Build.bat](https://raw.githubusercontent.com/OpenDriver2/REDRIVER2/acca6b139302dd72c1fbff52556f3493aafda2dd/.appveyor/Build.bat), [.appveyor/Build.sh](https://raw.githubusercontent.com/OpenDriver2/REDRIVER2/acca6b139302dd72c1fbff52556f3493aafda2dd/.appveyor/Build.sh), [.gitmodules](https://raw.githubusercontent.com/OpenDriver2/REDRIVER2/acca6b139302dd72c1fbff52556f3493aafda2dd/.gitmodules), [LICENSE](https://raw.githubusercontent.com/OpenDriver2/REDRIVER2/acca6b139302dd72c1fbff52556f3493aafda2dd/LICENSE).

## SM64Plus

LauncherMirror contém a interface e build.sh oficial. A GUI não tem CLI de importação, mas o script oficial e seu checkout foram verificados; a integração nova fornece MSYS2 privado, pacotes assinados e mídia própria, preservando fontes. O script rejeitou ROM ausente e as ferramentas compilaram. O contrato é disponível; boot continua não comprovado.

O índice final contém 146 receitas: 134 ativas e 12 desativadas, cobrindo 134 projetos. Os três projetos mantidos sem automação são StrikersRecomp, Vandal Hearts e REDRIVER2. O catálogo mantém 137 projetos elegíveis e registra as limitações de cada um.

Os JSON associados preservam commits, hashes, comandos e limites. A receita reproduzível do extrator SoH está em Tools/NativeExtractors/SoH no repositório Desktop. Os contratos novos mantêm os perfis históricos com intervenções suspensos.
