#!/usr/bin/env python3
"""Validação de integridade do catálogo remoto AllFix (schemas v4/v1/v1)."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]

# Uma plataforma de origem por jogo: categorias compostas ou grupos editoriais
# não são admitidos. Para introduzir outro console, atualize esta lista e os
# registros correspondentes no catálogo no mesmo PR.
ALLOWED_PLATFORM_GROUPS = frozenset({
    "Android", "Arcade", "Game Boy Advance", "GameCube", "Nintendo 64",
    "Nintendo Switch", "Nintendo Switch 2", "PlayStation 1",
    "PlayStation 2", "PlayStation 3", "PlayStation 4", "PlayStation 5",
    "SEGA Dreamcast", "SEGA Mega Drive", "SNES", "Wii", "Wii U",
    "Xbox 360", "Xbox Original",
})


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise ValueError(detail)


def load(filename: str) -> dict:
    path = ROOT / filename
    with path.open("r", encoding="utf-8") as stream:
        data = json.load(stream)
    require(isinstance(data, dict), f"{filename}: objeto JSON esperado")
    return data


def valid_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate_date(record: dict, key: str, identity: str, required: bool) -> None:
    if required:
        require(key in record, f"{identity}: {key} ausente")
    value = record.get(key)
    if value is None:
        return
    require(isinstance(value, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value),
            f"{identity}: {key} deve ser YYYY-MM-DD ou null")
    try:
        date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{identity}: {key} contém uma data inválida") from None


def validate_addition_history(catalog: dict, base: dict) -> None:
    def entries(document: dict) -> dict:
        games = document["games"]
        return {
            "jogo": {g["id"]: g.get("added_at") for g in games},
            "projeto": {p["id"]: p.get("added_at") for g in games for p in g.get("projects", [])},
        }

    previous = entries(base)
    for kind, records in entries(catalog).items():
        for identity, value in records.items():
            if identity not in previous[kind]:
                require(value is not None, f"{kind} novo {identity}: informe a data de inclusão")
            elif previous[kind][identity] is not None:
                require(value == previous[kind][identity],
                        f"{kind} {identity}: preserve a data de inclusão existente")


def validate(require_dates: bool = False, compare_with: str | None = None) -> None:
    catalog = load("catalog.json")
    requirements = load("requirements.json")
    about = load("about.json")

    require(catalog.get("schema_version") == 4, "catalog.json: schema v4 esperado")
    require(requirements.get("schema_version") == 1, "requirements.json: schema v1 esperado")
    require(about.get("schema_version") == 1, "about.json: schema v1 esperado")
    require(catalog.get("requirements_file") == "requirements.json", "requirements_file inválido")
    require(catalog.get("about_file") == "about.json", "about_file inválido")

    games = catalog.get("games")
    require(isinstance(games, list) and bool(games), "Lista de jogos vazia ou inválida")
    require(isinstance(requirements.get("projects"), dict), "requirements.projects inválido")
    require(isinstance(about.get("games"), dict), "about.games inválido")
    require(isinstance(about.get("projects"), dict), "about.projects inválido")

    game_ids: set[str] = set()
    project_to_game: dict[str, str] = {}
    repositories: set[str] = set()

    for game in games:
        require(isinstance(game, dict), "Jogo deve ser objeto")
        gid = game.get("id")
        require(isinstance(gid, str) and bool(gid.strip()), "ID de jogo ausente")
        require(gid not in game_ids, f"ID de jogo duplicado: {gid}")
        game_ids.add(gid)
        validate_date(game, "release_date", gid, require_dates)
        validate_date(game, "added_at", gid, require_dates)

        require(isinstance(game.get("title"), str) and bool(game["title"].strip()),
                f"Título ausente: {gid}")
        group = game.get("platform_group")
        require(group in ALLOWED_PLATFORM_GROUPS,
                f"{gid}: categoria não é console/plataforma individual: {group!r}")
        projects = game.get("projects")
        require(isinstance(projects, list) and bool(projects), f"Jogo sem projetos: {gid}")

        for project in projects:
            require(isinstance(project, dict), f"Projeto inválido em {gid}")
            pid = project.get("id")
            require(isinstance(pid, str) and bool(pid.strip()), f"ID de projeto ausente em {gid}")
            require(pid not in project_to_game, f"ID de projeto duplicado: {pid}")
            project_to_game[pid] = gid
            validate_date(project, "added_at", pid, require_dates)

            source = project.get("source")
            require(isinstance(source, dict), f"{pid}: source ausente")
            require(valid_url(source.get("url")), f"{pid}: source.url inválida")
            require(isinstance(source.get("provider"), str), f"{pid}: source.provider inválido")
            if source.get("provider") == "github":
                repo_name = source.get("github_repository")
                require(isinstance(repo_name, str) and "/" in repo_name,
                        f"{pid}: github_repository inválido")
                require(repo_name.casefold() not in repositories,
                        f"Repositório GitHub repetido: {repo_name}")
                repositories.add(repo_name.casefold())
                releases_url = source.get("releases_url")
                require(releases_url is None or valid_url(releases_url),
                        f"{pid}: releases_url inválida")

            require(isinstance(project.get("fallback_name"), str)
                    and bool(project["fallback_name"].strip()), f"{pid}: fallback_name ausente")
            windows = project.get("windows")
            require(isinstance(windows, dict), f"{pid}: objeto windows ausente")
            require(isinstance(windows.get("installation_enabled"), bool),
                    f"{pid}: installation_enabled deve ser booleano")

    expected_projects = set(project_to_game)
    require(set(requirements["projects"]) == expected_projects,
            "IDs de requirements.projects diferem dos IDs do catálogo")
    require(set(about["projects"]) == expected_projects,
            "IDs de about.projects diferem dos IDs do catálogo")
    require(set(about["games"]) == game_ids,
            "IDs de about.games diferem dos IDs do catálogo")

    for gid in game_ids:
        entry = about["games"][gid]
        require(isinstance(entry, dict) and isinstance(entry.get("description"), str),
                f"{gid}: descrição do jogo ausente")

    for pid, gid in project_to_game.items():
        record = requirements["projects"][pid]
        description = about["projects"][pid]
        require(isinstance(record, dict) and record.get("game_id") == gid,
                f"{pid}: game_id inválido em requirements")
        require(isinstance(description, dict) and description.get("game_id") == gid,
                f"{pid}: game_id inválido em about")
        require(isinstance(record.get("source_text"), dict),
                f"{pid}: source_text ausente")
        require(isinstance(record.get("evidence"), list),
                f"{pid}: evidence deve ser lista")
        for key in ("system", "installation", "build", "general"):
            require(key in record["source_text"], f"{pid}: source_text.{key} ausente")
            require(record.get(key) is None or isinstance(record[key], str),
                    f"{pid}: {key} localizado deve ser texto ou null")
        require(isinstance(description.get("description_pt"), str),
                f"{pid}: description_pt ausente")

    if compare_with:
        base = json.loads(subprocess.check_output(
            ["git", "show", f"{compare_with}:catalog.json"], cwd=ROOT))
        validate_addition_history(catalog, base)

    print(f"PASSOU: {len(game_ids)} jogos, {len(project_to_game)} projetos, "
          "IDs únicos, referências 1:1, schemas e campos obrigatórios.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-dates", action="store_true", help="exige os campos de data, mesmo quando nulos")
    parser.add_argument("--compare-with", metavar="REV", help="compara datas de inclusão com uma revisão do Git")
    args = parser.parse_args()
    try:
        validate(args.require_dates, args.compare_with)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        sys.exit(1)
