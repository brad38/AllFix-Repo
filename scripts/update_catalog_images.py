#!/usr/bin/env python3
"""Preenche apenas capas e banners ausentes no catalogo do AllFix.

Sem chave embutida, sem sobrescrever imagens existentes e sem depender do app.
"""
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
API = "https://www.steamgriddb.com/api/v2"
KEY = os.environ.get("STEAMGRIDDB_API_KEY", "").strip()
if not KEY:
    sys.exit("STEAMGRIDDB_API_KEY ausente: configure o secret do repositorio.")

SESSION = requests.Session()
SESSION.headers.update({"Authorization": "Bearer " + KEY, "User-Agent": "AllFix-Catalog-Image-Updater/1.0"})

# Edicoes com nomes iguais: IDs correspondem aos jogos originais, nao remakes.
KNOWN_IDS = {
    "the-legend-of-zelda-ocarina-of-time": 21202,
    "perfect-dark": 37787,
    "bomberman-64": 1680,
    "mystical-ninja-starring-goemon": 33703,
    "god-of-war-2005": 36454,
    "crash-team-racing": 36474,
    "wipeout": 5296247,
    "bloody-roar-ii": 34481,
    "king-s-field-jp-1994": 5270235,
    "sonic-the-hedgehog-2006": 5249681,
    "sonic-3-knuckles": 33827,
    "outrun": 35252,
    "the-darkness": 5272254,
    "peter-jackson-s-king-kong": 5249080,
    "jak-and-daxter-1-2-e-3": 5285926,
}
# Agrupamentos nao devem receber arte de um unico jogo arbitrario.
GROUPED_IDS = {"tomb-raider-i-v", "sonic-the-hedgehog-1-2-2013"}


def normalize(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", value.lower())


def get(endpoint):
    for attempt in range(4):
        try:
            response = SESSION.get(API + "/" + endpoint, timeout=20)
            if response.status_code == 429 or response.status_code >= 500:
                time.sleep(2 ** attempt)
                continue
            response.raise_for_status()
            body = response.json()
            if not body.get("success"):
                raise RuntimeError("Resposta da API sem sucesso")
            return body.get("data") or []
        except (requests.RequestException, ValueError, RuntimeError) as exc:
            if attempt == 3:
                raise RuntimeError(f"Falha na API em {endpoint.split('/')[0]}") from exc
            time.sleep(2 ** attempt)
    return []


def game_id(game):
    gid = game["id"]
    if gid in GROUPED_IDS:
        return None
    if gid in KNOWN_IDS:
        return KNOWN_IDS[gid]
    title = game["title"]
    for sep in (" / ", " & ", " (20"):
        title = title.split(sep)[0]
    matches = [
        item for item in get("search/autocomplete/" + quote(title, safe=""))
        if normalize(item.get("name", "")) == normalize(title)
    ]
    if len(matches) == 1:
        return matches[0]["id"]
    # Se houver varias edicoes, nao escolher uma sem verificacao.
    return None


def artwork(items, kind):
    good = []
    for item in items:
        url = item.get("url")
        width, height = item.get("width", 0), item.get("height", 0)
        if not isinstance(url, str) or not url.startswith("https://cdn2.steamgriddb.com/"):
            continue
        if item.get("nsfw") or item.get("humor") or item.get("lock") or not height or not width:
            continue
        ratio = width / height
        if kind == "cover" and not (height >= 500 and 0.55 <= ratio <= 0.8):
            continue
        if kind == "banner" and not (width >= 900 and 1.8 <= ratio <= 3.5):
            continue
        good.append(item)
    good.sort(key=lambda item: (
        item.get("style") in ("alternate", "material", "blurred"),
        item.get("language") not in (None, "en", "pt", "pt-BR"),
        -(item.get("upvotes", 0) - item.get("downvotes", 0)),
        -item.get("width", 0) * item.get("height", 0),
    ))
    return good[0]["url"] if good else None


def main():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8-sig"))
    games = catalog["games"]
    assert catalog["schema_version"] == 4
    assert len(games) == 87
    assert sum(len(game["projects"]) for game in games) == 119
    updated = 0
    failures = 0
    for game in games:
        missing = [kind for kind in ("cover", "banner") if not game.get(kind)]
        if not missing:
            continue
        try:
            identifier = game_id(game)
            if identifier is None:
                print(f"Ignorado (identificacao ambigua): {game['id']}")
                continue
            for kind in missing:
                endpoint = "grids" if kind == "cover" else "heroes"
                url = artwork(get(f"{endpoint}/game/{identifier}?limit=100"), kind)
                if url:
                    # Nao sobrescreve valores existentes.
                    game[kind] = url
                    updated += 1
                    print(f"Imagem {kind} encontrada: {game['id']}")
        except Exception:
            failures += 1
            print(f"Falha ao consultar imagens: {game['id']}", file=sys.stderr)
    if updated:
        CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Concluido: {updated} novas imagens; {failures} jogos com erro.")
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
