#!/usr/bin/env python3
"""Reproduce the reviewed catalog, preserving every retained ID/date and archived record.

Uses the reviewed documentary evidence, not a classifier based on README keywords.
Run from this repository with --getall-index ../getall-scope/index.json.
"""
import argparse
import collections
import copy
import hashlib
import json
from pathlib import Path
import subprocess

from eligibility_rules import validate_registers
from validate_catalog import validate_addition_history

ROOT = Path(__file__).resolve().parents[1]
BASE = "44bdb508842407d501e420457274eb4064f5d935"
DATE = "2026-11-27"
EVIDENCE = ROOT / "docs/audits/eligibility-20261127"


def read_base(name):
    return json.loads(subprocess.check_output(["git", "show", BASE + ":" + name], cwd=ROOT))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--getall-index", type=Path, required=True)
    args = parser.parse_args()
    records = json.loads((EVIDENCE / "reviewed-projects.json").read_text(encoding="utf-8"))
    catalog, requirements, about = [read_base(name) for name in ("catalog.json", "requirements.json", "about.json")]
    original = copy.deepcopy(catalog)
    previous_ids = {p["id"] for g in catalog["games"] for p in g["projects"]}
    assert len(records) == len(previous_ids) == 148
    assert {r["project_id"] for r in records} == previous_ids
    assessed = {r["project_id"]: copy.deepcopy(r) for r in records}
    index_data = args.getall_index.read_bytes()
    recipes = json.loads(index_data)["recipes"]
    available = collections.defaultdict(list)
    for recipe in recipes:
        if recipe["status"] in {"validated", "experimental"}:
            available[recipe["project_id"]].append(recipe["tag"])

    eligible = {"schema_version": 1, "reviewed_at": DATE,
        "scope": "Evidência pública de gameplay upstream. Não é homologação local do GetAll.",
        "projects": {}}
    excluded = {"schema_version": 1, "reviewed_at": DATE,
        "policy": "Registro para reavaliação; estes IDs não aparecem na loja ativa.", "projects": {}}
    games = []
    changed_sources = []
    for game in catalog["games"]:
        retained = []
        for project in game["projects"]:
            pid = project["id"]
            review = assessed[pid]
            if not review["eligible"]:
                excluded["projects"][pid] = {
                    "game_id": game["id"],
                    "game": {key: copy.deepcopy(value) for key, value in game.items() if key != "projects"},
                    "project": copy.deepcopy(project), "assessment": review,
                    "requirements": requirements["projects"].pop(pid),
                    "about": {"project": about["projects"].pop(pid), "game": copy.deepcopy(about["games"][game["id"]])}}
                continue
            # An available contract is not proof of original-media installation or gameplay.
            automation = "available_contract" if available[pid] else "temporarily_unavailable"
            if not available[pid]:
                review["classification"] = "functional_manual_install"
            elif pid in {"hookshot-zelda-oot-port", "strikers-wiicompiled", "mkdd-recomp", "wipeout-rewrite", "crash-team-racing-turbocharged", "mkw-recomp"}:
                review["classification"] = "functional_with_limitations"
            review["automation_catalog_state"] = automation
            review["automation_contract_tags"] = available[pid]
            if pid == "hookshot-zelda-oot-port":
                old = copy.deepcopy(project["source"])
                project["source"] = {"url": "https://github.com/ItsNotRexed/Hookshot", "provider": "github",
                    "github_repository": "ItsNotRexed/Hookshot", "releases_url": "https://github.com/ItsNotRexed/Hookshot/releases"}
                changed_sources.append({"project_id": pid, "before": old, "after": copy.deepcopy(project["source"]),
                    "reason": "Use the canonical maintainer distribution; mirror executable digests differed."})
            project["eligibility"] = {"classification": review["classification"], "reviewed_at": DATE,
                "automation_availability": automation,
                "notice_pt": "Projeto oficial funcional. A instalação automática está temporariamente indisponível; siga o procedimento do autor."
                    if automation == "temporarily_unavailable" else
                    "Há evidência de jogabilidade no projeto oficial. A validação da instalação pelo GetAll é registrada separadamente."}
            retained.append(project)
            eligible["projects"][pid] = review
            supplement = {"reviewed_at": DATE, "classification": review["classification"],
                "official_installation_pt": review["official_install_method"],
                "limitations_pt": review["limitations"], "evidence": review["gameplay_evidence"],
                "notice_pt": project["eligibility"]["notice_pt"], "official_repository": review["official_repository"]}
            requirements["projects"][pid]["scope_review"] = copy.deepcopy(supplement)
            about["projects"][pid]["scope_review"] = copy.deepcopy(supplement)
        if retained:
            game["projects"] = retained
            games.append(game)
        else:
            about["games"].pop(game["id"])
    catalog["games"] = games
    catalog["catalog_version"] = "2026-11-27-functional-eligibility-review"
    catalog["eligibility_file"] = "eligibility.json"
    validate_addition_history(catalog, original)
    validate_registers(catalog, eligible, excluded)
    for name, doc in (("catalog.json", catalog), ("requirements.json", requirements), ("about.json", about),
                      ("eligibility.json", eligible), ("excluded-projects.json", excluded)):
        save(ROOT / name, doc)
    retained_ids = set(eligible["projects"])
    old_projects = {p["id"]: p for g in original["games"] for p in g["projects"]}
    # Assert that source correction + new review markers are the only retained-project edits.
    for game in games:
        old_game = next(g for g in original["games"] if g["id"] == game["id"])
        assert {k:v for k,v in game.items() if k != "projects"} == {k:v for k,v in old_game.items() if k != "projects"}
        for project in game["projects"]:
            keys = set(old_projects[project["id"]])
            if project["id"] == "hookshot-zelda-oot-port": keys.remove("source")
            assert all(project[k] == old_projects[project["id"]][k] for k in keys)
    summary = {"base_catalog_commit": BASE, "reviewed_at": DATE,
        "before": {"games": len(original["games"]), "projects": len(previous_ids)},
        "after": {"games": len(games), "projects": len(retained_ids)},
        "excluded_project_ids": list(excluded["projects"]),
        "removed_game_ids": sorted({g["id"] for g in original["games"]} - {g["id"] for g in games}),
        "classification_counts": dict(collections.Counter(r["classification"] for r in eligible["projects"].values())),
        "retained_ids_dates_and_metadata_preserved": True, "source_corrections": changed_sources,
        "getall_index_sha256": hashlib.sha256(index_data).hexdigest(),
        "note": "available_contract does not mean original-media validation, boot or gameplay by GetAll."}
    save(EVIDENCE / "revision-summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
