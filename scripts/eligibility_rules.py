"""Admission rules for reviewed project evidence; never infer gameplay from builds."""
from __future__ import annotations

from datetime import date
from urllib.parse import urlparse

FUNCTIONAL = frozenset({
    "functional_eligible", "functional_with_limitations", "functional_manual_install",
})
INACTIVE = frozenset({"unproven", "ineligible"})
CLASSIFICATIONS = FUNCTIONAL | INACTIVE
GAMEPLAY_EVIDENCE = frozenset({
    "gameplay_demo", "maintainer_gameplay_report", "user_gameplay_report",
    "original_media_play_test", "gameplay_video", "gameplay_issue",
    "gameplay_screenshot_with_context", "documented_playthrough",
})
INSUFFICIENT_ALONE = frozenset({
    "readme", "release_exists", "build_success", "decompilation_percentage",
    "title_screen", "rendering_demo", "synthetic_test",
})


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def https(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and not parsed.username


def validate_assessment(project_id: str, record: dict, *, active: bool) -> None:
    require(isinstance(record, dict), f"{project_id}: assessment must be an object")
    require(record.get("project_id") == project_id, f"{project_id}: assessment identity mismatch")
    status = record.get("classification")
    require(isinstance(record.get("reason"), str) and len(record["reason"].strip()) >= 20,
            f"{project_id}: explain the eligibility decision")
    require(status in CLASSIFICATIONS, f"{project_id}: unknown eligibility classification")
    require(record.get("eligible") is (status in FUNCTIONAL), f"{project_id}: eligibility/status mismatch")
    require(active == (status in FUNCTIONAL), f"{project_id}: eligibility does not match active catalog")
    try:
        date.fromisoformat(record["last_verified_local"])
    except (ValueError, KeyError, TypeError):
        raise ValueError(f"{project_id}: review date required") from None
    evidence = record.get("gameplay_evidence")
    require(isinstance(evidence, list), f"{project_id}: evidence list required")
    for item in evidence:
        require(isinstance(item, dict) and https(item.get("url")), f"{project_id}: evidence URL must be HTTPS")
        require(isinstance(item.get("kind"), str) and bool(item["kind"].strip()),
                f"{project_id}: evidence kind required")
        require(isinstance(item.get("observed"), str) and len(item["observed"].strip()) >= 20,
                f"{project_id}: explain what the source actually establishes")
    if active:
        require(https(record.get("official_repository")),
                f"{project_id}: official repository must be HTTPS")
        require(any(item.get("kind") in GAMEPLAY_EVIDENCE for item in evidence),
                f"{project_id}: README/release/build/fixture alone cannot prove gameplay")
        require(isinstance(record.get("official_install_method"), str)
                and len(record["official_install_method"].strip()) >= 20,
                f"{project_id}: official installation procedure required")
        require(record.get("provenance_review") in {"official_source", "official_distribution", "official_source_and_distribution"},
                f"{project_id}: official provenance must be reviewed")
    else:
        conditions = record.get("reinclusion_conditions")
        require(isinstance(conditions, list) and bool(conditions)
                and all(isinstance(value, str) and value.strip() for value in conditions),
                f"{project_id}: reinclusion conditions must be a nonempty list of text")
    require(isinstance(record.get("limitations"), list)
            and all(isinstance(value, str) and value.strip() for value in record["limitations"]),
            f"{project_id}: limitations must be a list of text")
    # No automated source completion, feature stripping or unconditional success
    # may be treated as a legitimate installation method.
    require(record.get("requires_allfix_game_changes", False) is False or not active,
            f"{project_id}: active installation depends on AllFix game changes")


def validate_registers(catalog: dict, assessments: dict, excluded: dict) -> None:
    require(assessments.get("schema_version") == 1, "eligibility.json: schema v1 required")
    require(excluded.get("schema_version") == 1, "excluded-projects.json: schema v1 required")
    active = {p["id"]: p for g in catalog["games"] for p in g["projects"]}
    records = assessments.get("projects")
    archived = excluded.get("projects")
    require(isinstance(records, dict) and isinstance(archived, dict), "eligibility/excluded projects must be maps")
    require(set(records) == set(active), "eligibility IDs differ from active catalog")
    require(not set(active) & set(archived), "excluded project still appears in active catalog")
    for pid, record in records.items():
        validate_assessment(pid, record, active=True)
        marker = active[pid].get("eligibility")
        require(isinstance(marker, dict) and marker.get("classification") == record["classification"]
                and marker.get("reviewed_at") == record["last_verified_local"],
                f"{pid}: catalog eligibility marker does not match review")
    for pid, record in archived.items():
        validate_assessment(pid, record["assessment"], active=False)
        require(record.get("project", {}).get("id") == pid, f"{pid}: preserve excluded project snapshot")
        require(record.get("game", {}).get("id") == record.get("game_id"), f"{pid}: preserve game identity")
        require(isinstance(record.get("requirements"), dict) and isinstance(record.get("about"), dict),
                f"{pid}: preserve supporting metadata for later reconsideration")
