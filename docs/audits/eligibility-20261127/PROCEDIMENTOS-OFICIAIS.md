# Procedimentos oficiais de instalação — 28/11/2026

Procedimentos oficiais dos dez projetos antes mantidos como manuais. Separar procedimento documentado, ferramenta compilada, contrato GetAll e execução com mídia original.

Os resultados abaixo descrevem o ponto verificado, sem transformar um build ou teste sintético em prova de mídia original, boot ou gameplay. O estado do contrato GetAll é calculado separadamente a partir do índice registrado em revision-summary.json.

## sm64ex

MSYS2 MINGW64 com pacotes oficiais da wiki; ROM própria baserom.us.z64; make EXTERNAL_DATA=1.

**Saída prevista:** build/us_pc/sm64.us.<microcode>.exe e recursos externos correspondentes.

**Resultado e limite:** O build depende da ROM para gerar assets. Não foi repetido com mídia original; a receita antiga que alterava fontes não foi reativada. A documentação oficial existe e isto não é uma alegação de impossibilidade de automação.

Fontes: [README.md](https://raw.githubusercontent.com/sm64pc/sm64ex/d7ca2c04364a6dd0dac58b47151e04e26887e6f0/README.md), [Makefile](https://raw.githubusercontent.com/sm64pc/sm64ex/d7ca2c04364a6dd0dac58b47151e04e26887e6f0/Makefile).

## render96ex

Compilar fonte oficial com a ROM própria e procedimento da wiki Windows; opções EXTERNAL_DATA=1/DynOS previstas no upstream. ModelPack/texture pack somente das fontes indicadas pelo autor.

**Saída prevista:** build/us_pc, pacote oficial Render96_DynOs_v3.0.7z em dynos/packs; texturas opcionais em res/gfx.

**Resultado e limite:** Não se deve retirar renderers, mudar código de runtime nem substituir packs para contornar erro de compilação. Build intacto com mídia original ainda não testado nesta retomada.

Fontes: [README.md](https://raw.githubusercontent.com/Render96/Render96ex/48da5c491c8abfb2f5192b59278c1c269411e533/README.md), [Makefile](https://raw.githubusercontent.com/Render96/Render96ex/48da5c491c8abfb2f5192b59278c1c269411e533/Makefile).

## sm64rt

Procedimento sm64ex/MSYS2, com RENDER_API=RT64 EXTERNAL_DATA=1 e RT64 oficial incluído na versão.

**Saída prevista:** Executável em build/us_pc com dependências RT64 correspondentes; Windows 10 2004+, GPU DXR e runtime VC++ documentados.

**Resultado e limite:** Desativar RT64 descaracterizaria o projeto. Build oficial dependente de ROM ainda não executado; não há prova de ausência de procedimento oficial.

Fontes: [README.md](https://raw.githubusercontent.com/DarioSamo/sm64rt/20e618b75ae4a6810bd92ac6a937cb167517aac5/README.md), [Makefile](https://raw.githubusercontent.com/DarioSamo/sm64rt/20e618b75ae4a6810bd92ac6a937cb167517aac5/Makefile).

## sm

MSBuild sm.sln /restore /p:RestorePackagesConfig=true /p:Configuration=Release /p:Platform=x64. Solução upstream v143 e SDL2 NuGet 2.26.3.

**Saída prevista:** build/bin-x64-Release/sm.exe e SDL2.dll; sm.ini oficial e ROM própria sm.smc ao lado da instalação conforme upstream.

**Resultado e limite:** Build real sem ROM passou em 17 s com 124 fontes intactas. Fonte compilada não é evidência de boot. Novo contrato de instalação está em implementação; não reativar perfil antigo com patches.

Fontes: [BUILDING.md](https://raw.githubusercontent.com/snesrev/sm/578f90b3cc49557bb70060ad033bb90b8cf8ac50/BUILDING.md), [README.md](https://raw.githubusercontent.com/snesrev/sm/578f90b3cc49557bb70060ad033bb90b8cf8ac50/README.md), [sm.vcxproj](https://raw.githubusercontent.com/snesrev/sm/578f90b3cc49557bb70060ad033bb90b8cf8ac50/src/sm.vcxproj).

## sm-rewrite

Visual Studio 2022/CMake/vcpkg: cmake --preset windows-relwithdebinfo; cmake --build build-windows-relwithdebinfo. Preset e CMake são do upstream.

**Saída prevista:** build-windows-relwithdebinfo/sm.exe, SDL2.dll e sm.ini oficial; ROM própria em runtime.

**Resultado e limite:** A alternativa oficial MSVC evita as adaptações MinGW anteriores. A prova isolada estava em andamento ao registrar este relatório; não equivale a build concluído nem autoriza reativar o perfil histórico.

Fontes: [BUILDING.md](https://raw.githubusercontent.com/testyourmine/sm_rewrite/523787384a7c912153883b21714f5edabf4e2406/BUILDING.md), [CMakePresets.json](https://raw.githubusercontent.com/testyourmine/sm_rewrite/523787384a7c912153883b21714f5edabf4e2406/CMakePresets.json), [README.md](https://raw.githubusercontent.com/testyourmine/sm_rewrite/523787384a7c912153883b21714f5edabf4e2406/README.md).

## ship-of-harkinian-soh

Torch standalone oficial no submódulo 2ab12fe9660aec04e02ee89fe81baed304a1a1d6, com opções de formato do Shipwright 9.3.1. torch.exe o2r ROM.z64 -s assets -d output -u 9.3.1.

**Saída prevista:** oot.o2r ou oot-mq.o2r conforme config; verificar version e portVersion antes de concluir.

**Resultado e limite:** Wrapper soh-torch 9.3.1 falha em C2664; alternativa standalone compilou intacta e 7 checks sintéticos passaram. Hash não reconhecido retorna exit0 sem archive: a instalação deve validar saída. Nenhuma ROM original, boot ou gameplay testados.

Fontes: [fonte oficial](https://github.com/HarbourMasters/Shipwright/blob/f0599f96f8d442f26d0fa1c5cedafddacd56633f/CMakeLists.txt), [fonte oficial](https://github.com/HarbourMasters/Torch/blob/2ab12fe9660aec04e02ee89fe81baed304a1a1d6/src/main.cpp).

## strikersrecomp

bootstrap.sh; python3 tools/generate.py --iso <ISO G4QE01 própria>; tools/package_module.sh para RecompCore recomendado. Standalone GXRuntime é rota distinta.

**Saída prevista:** Módulo gG4QE01_recomp; RecompCore com CPUCore=6. Fontes geradas da mídia permanecem locais.

**Resultado e limite:** O README cita DLL por plataforma, mas package_module.sh só distingue Darwin .dylib e demais .so, usando Ninja/ThinLTO e exemplo Metal. macOS é a plataforma testada declarada. Não foi comprovado pacote Windows fiel; não aplicar novos patches de SEH/renderer.

Fontes: [README.md](https://raw.githubusercontent.com/aharonahdoot/StrikersRecomp/cd88f71f5a836c103484c038454b4143000d883c/README.md), [bootstrap.sh](https://raw.githubusercontent.com/aharonahdoot/StrikersRecomp/cd88f71f5a836c103484c038454b4143000d883c/bootstrap.sh), [README.md](https://raw.githubusercontent.com/aharonahdoot/StrikersRecomp/cd88f71f5a836c103484c038454b4143000d883c/patches/README.md).

## mkdd-recomp

ciso_extract.py; Ghidra 12.1.4 + GameCubeLoader 1.3.0 + ghidra-cli 0.2.2; ExportSheets/ExportPcode; build_sheets/import_symbols/build_sheets/gen_rust; play.bat.

**Saída prevista:** Crates Rust gerados localmente, mkdd-bevy e ROM/disco via MKDD_DISC ou rust/disc.txt. Rust 1.98 e Bevy 0.19.1 documentados.

**Resultado e limite:** Repositório omite código/dados derivados da mídia. Pipeline Ghidra exige projeto/programa/configuração reais. Não foi reproduzido integralmente com disco; inserir IL customizada ou corrigir gerador no AllFix não é alternativa fiel.

Fontes: [README.md](https://raw.githubusercontent.com/LeftInWalmart/MKDD-Recomp/e173ce40a70eab4830f98ccd9dfdf1ac0d683657/README.md), [play.bat](https://raw.githubusercontent.com/LeftInWalmart/MKDD-Recomp/e173ce40a70eab4830f98ccd9dfdf1ac0d683657/play.bat).

## gt5-recomp

GT5-Installer.bat oficial seleciona pasta PS3_GAME ou ISO própria, provisiona ferramentas locais, extrai/desbloqueia EBOOT e chama setup oficial. Preferir a interface oficial de instalação e GT5Launcher.exe.

**Saída prevista:** GT5/input/EBOOT.elf, GT5/vfs, executáveis e launcher construídos pelo upstream; jogo base 01.00 BCES00569/BCUS98114.

**Resultado e limite:** O instalador tem modos engine/console e variáveis documentadas GT5_INSTALL_GAME/DEST/NOGUI/NOBUILD. As escolhas e aceitação dos componentes são da interface oficial; não impor aceite nem renderers. Não foi executado com disco nesta revisão.

Fontes: [GT5-Installer.bat](https://raw.githubusercontent.com/MormonFTP-hub/gt5-recomp/950f7ce48006b45e0c1391e80ea0071c04cef2cf/GT5-Installer.bat), [play.bat](https://raw.githubusercontent.com/MormonFTP-hub/gt5-recomp/950f7ce48006b45e0c1391e80ea0071c04cef2cf/GT5/play.bat), [rebuild.ps1](https://raw.githubusercontent.com/MormonFTP-hub/gt5-recomp/950f7ce48006b45e0c1391e80ea0071c04cef2cf/GT5/scripts/rebuild.ps1).

## god-of-war-recomp

python tools/iso_extract.py <ISO SCUS-97399 própria> game --layout; scripts/1_instalar_herramientas.cmd; scripts/2_compilar.cmd. GOW_WORK, GOW_ELF e GOW_LLVM são opções oficiais.

**Saída prevista:** GOW_WORK/out/build ou build-clang/ps2EntryRunner.exe, game com SCUS_973.99, IRX, PART1/PART2.PAK e .disc_layout; scripts/3_ejecutar_manual.cmd inicia o runtime.

**Resultado e limite:** O próprio script fixa PS2Recomp c5a9d02 e aplica patches versionados pelo autor. Isso difere de patches particulares do AllFix. Build completo com mídia ainda não reproduzido; não remover subsistemas/runtime.

Fontes: [README.es.md](https://raw.githubusercontent.com/KIexster/god-of-war-recomp/d1d11ec545c3baf2f3fc17e2df4247ac4b732d5c/README.es.md), [README.md](https://raw.githubusercontent.com/KIexster/god-of-war-recomp/d1d11ec545c3baf2f3fc17e2df4247ac4b732d5c/README.md), [README.pt-BR.md](https://raw.githubusercontent.com/KIexster/god-of-war-recomp/d1d11ec545c3baf2f3fc17e2df4247ac4b732d5c/README.pt-BR.md).

## Launcher SM64Plus

LauncherMirror permanece preparação parcial oficial; inspeção de 51 arquivos GML/sh/bat não identificou uma CLI de instalação. Receipt no GetAll docs/validations/official-scope/sm64plus-launcher-source-review.json.

Os relatórios JSON associados preservam commits, hashes e evidência de build. A receita reproduzível do extrator SoH está em Tools/NativeExtractors/SoH no repositório Desktop.
