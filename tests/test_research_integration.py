"""Regression tests for research-to-network coverage and deliberate non-relations."""
from __future__ import annotations

import hashlib
from pathlib import Path
import tempfile
import unittest

import yaml

from scripts import research_integration as coverage


class ResearchIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "research").mkdir()
        (self.root / "data").mkdir()
        self.relations = [
            {"id": "REL-TEST-001", "from": "ORG-A", "to": "ORG-B", "sources": ["SRC-A"]}
        ]
        self.entries = {}
        self.study = "test-research.md"
        self.path = self.root / "research" / self.study
        self.path.write_text("# Test\n\nEvidence of a documented relation.\n", encoding="utf-8")
        self._save()

    def _save(self):
        (self.root / "data" / "research-integrations.yml").write_text(
            yaml.safe_dump({"studies": self.entries}, allow_unicode=True), encoding="utf-8"
        )
        (self.root / "data" / "relations.yml").write_text(
            yaml.safe_dump({"relations": self.relations}, allow_unicode=True), encoding="utf-8"
        )

    def _entry(self, status="network", **kwargs):
        return {
            "sha256": hashlib.sha256(self.path.read_bytes()).hexdigest(),
            "status": status,
            **kwargs,
        }

    def test_unchanged_baseline_study_is_visible_as_legacy_backlog(self):
        blob = coverage.git_blob_id(self.path.read_bytes())
        report = coverage.audit(self.root, {self.study: blob})
        self.assertEqual(report.errors, [])
        self.assertEqual(report.legacy, [self.study])

    def test_changed_baseline_requires_new_decision(self):
        blob = coverage.git_blob_id(self.path.read_bytes())
        self.path.write_text("# Test\n\nNew finding!\n", encoding="utf-8")
        report = coverage.audit(self.root, {self.study: blob})
        self.assertIn("lacks a network-integration decision", " ".join(report.errors))

    def test_new_study_without_review_is_rejected(self):
        report = coverage.audit(self.root, {})
        self.assertTrue(report.errors)
        self.assertEqual(report.legacy, [])

    def test_source_bound_relation_links_are_accepted(self):
        self.entries[self.study] = self._entry(relation_ids=["REL-TEST-001"])
        self._save()
        report = coverage.audit(self.root, {})
        self.assertEqual(report.errors, [])
        self.assertEqual(report.network, [self.study])

    def test_unknown_relation_is_rejected(self):
        self.entries[self.study] = self._entry(relation_ids=["REL-NOT-THERE"])
        self._save()
        report = coverage.audit(self.root, {})
        self.assertIn("unknown relation", " ".join(report.errors))

    def test_no_network_relation_requires_specific_reason(self):
        self.entries[self.study] = self._entry(
            "no_network_relation", reason="This paper checks the provenance of one quotation, without any new actor relationship."
        )
        self._save()
        self.assertEqual(coverage.audit(self.root, {}).errors, [])
        self.entries[self.study]["reason"] = "No"
        self._save()
        self.assertIn("substantive reason", " ".join(coverage.audit(self.root, {}).errors))

    def test_stale_review_hash_detects_updated_research(self):
        self.entries[self.study] = self._entry(relation_ids=["REL-TEST-001"])
        self._save()
        self.path.write_text("# Test\n\nRelation plus an additional important finding.\n")
        self.assertIn("stale", " ".join(coverage.audit(self.root, {}).errors))

    def test_missing_graph_relation_and_orphan_registry_entry_fail(self):
        self.entries[self.study] = self._entry(relation_ids=[])
        self.entries["removed.md"] = self._entry(relation_ids=["REL-TEST-001"])
        self._save()
        report = coverage.audit(self.root, {})
        self.assertIn("requires relation_ids", " ".join(report.errors))
        self.assertIn("missing study removed.md", " ".join(report.errors))

    def test_legacy_baseline_matches_current_repository(self):
        # The pinned commit is intentionally a one-time compatibility boundary.
        # A later edit of an old study is not grandfathered automatically.
        actual = coverage.baseline_blobs(coverage.ROOT)
        self.assertIn("bcci-cia-treasury-first-american-1972-1998.md", actual)
        self.assertGreater(len(actual), 100)


    def test_bcci_evidence_is_reachable_in_all_relevant_overviews(self):
        # One real, published end-to-end example: study -> relation IDs ->
        # rendered graph, source-bound relation table and actor index.
        root = coverage.ROOT
        entries = coverage.read_registry(root)
        file = "bcci-cia-treasury-first-american-1972-1998.md"
        ids = entries[file]["relation_ids"]
        self.assertEqual(len(ids), 6)
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        network = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        people = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        source_index = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        relations = yaml.safe_load((root / "data/relations.yml").read_text(encoding="utf-8"))["relations"]
        by_id = {relation["id"]: relation for relation in relations}
        for relation_id in ids:
            relation = by_id[relation_id]
            self.assertIn(f'id="{relation_id.lower()}"', network)
            self.assertIn(relation["label"], graph)
            for source_id in relation["sources"]:
                self.assertIn(f'id="{source_id.lower()}"', source_index)
        self.assertIn("ORG-INT-BCCI", people)
        self.assertIn("ORG-AN-CCAH", people)


if __name__ == "__main__":
    unittest.main()
