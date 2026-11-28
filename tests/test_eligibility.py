"""Regression checks for admission, archived candidates, and immutable dates."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from eligibility_rules import validate_assessment, validate_registers
from validate_catalog import validate_addition_history


def reviewed():
    return {"project_id": "port", "classification": "functional_with_limitations",
            "eligible": True, "last_verified_local": "2026-11-27",
            "gameplay_evidence": [{"url": "https://example.org/issues/12",
                "kind": "user_gameplay_report",
                "observed": "Relato de uma corrida concluída com controles e resultado final."}],
            "official_repository": "https://example.org/port",
            "official_install_method": "Executar o launcher oficial e selecionar a mídia original verificada.",
            "provenance_review": "official_source_and_distribution", "limitations": ["Sem teste local GetAll."]}


class AdmissionTests(unittest.TestCase):
    def test_build_readme_release_and_fixture_are_not_gameplay(self):
        for kind in ("readme", "release_exists", "build_success", "title_screen", "synthetic_test"):
            record = reviewed()
            record["gameplay_evidence"][0]["kind"] = kind
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, "alone cannot prove"):
                validate_assessment("port", record, active=True)

    def test_functional_upstream_can_remain_without_getall_boot(self):
        record = reviewed()
        record["classification"] = "functional_manual_install"
        record["getall_boot"] = "not_tested"
        validate_assessment("port", record, active=True)

    def test_upstream_completion_cannot_be_an_installation_requirement(self):
        record = reviewed()
        record["requires_allfix_game_changes"] = True
        with self.assertRaisesRegex(ValueError, "depends on AllFix game changes"):
            validate_assessment("port", record, active=True)

    def test_unproven_is_archived_with_reason_and_reentry_conditions(self):
        record = reviewed()
        record.update(classification="unproven", eligible=False,
                      reason="Somente a tela inicial pôde ser verificada.",
                      reinclusion_conditions=["Demonstração verificável de gameplay e instalação oficial."])
        validate_assessment("port", record, active=False)
        with self.assertRaisesRegex(ValueError, "active catalog"):
            validate_assessment("port", record, active=True)
        record.pop("reinclusion_conditions")
        with self.assertRaisesRegex(ValueError, "reinclusion"):
            validate_assessment("port", record, active=False)

    def test_official_provenance_required(self):
        record = reviewed()
        record["provenance_review"] = "unverified_mirror"
        with self.assertRaisesRegex(ValueError, "provenance"):
            validate_assessment("port", record, active=True)

    def test_official_repository_is_a_verifiable_https_source(self):
        for url in (None, "file:///tmp/port", "https://user@example.org/port"):
            record = reviewed()
            record["official_repository"] = url
            with self.subTest(url=url), self.assertRaisesRegex(ValueError, "official repository"):
                validate_assessment("port", record, active=True)

    def test_archive_cannot_leak_back_into_active_store(self):
        record = reviewed()
        catalog = {"games": [{"id": "game", "projects": [{"id": "port", "eligibility": {
            "classification": record["classification"], "reviewed_at": record["last_verified_local"]}}]}]}
        assessments = {"schema_version": 1, "projects": {"port": record}}
        archive = {"schema_version": 1, "projects": {}}
        validate_registers(catalog, assessments, archive)
        archive["projects"]["port"] = {"assessment": record}
        with self.assertRaisesRegex(ValueError, "still appears"):
            validate_registers(catalog, assessments, archive)

    def test_removal_preserves_dates_for_retained_games_and_projects(self):
        original = {"games": [{"id": "game", "added_at": "2026-11-22",
            "release_date": "1998-11-21", "projects": [
                {"id": "port", "added_at": "2026-11-22"},
                {"id": "prototype", "added_at": "2026-11-23"}]}]}
        revised = copy.deepcopy(original)
        revised["games"][0]["projects"].pop()
        validate_addition_history(revised, original)
        revised["games"][0]["added_at"] = "2026-11-27"
        with self.assertRaisesRegex(ValueError, "inclusão"):
            validate_addition_history(revised, original)
        revised = copy.deepcopy(original)
        revised["games"][0]["release_date"] = "2026-11-27"
        with self.assertRaisesRegex(ValueError, "lançamento"):
            validate_addition_history(revised, original)


if __name__ == "__main__":
    unittest.main()
