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


    def test_ig_farben_studies_have_source_bound_graph_coverage(self):
        root = coverage.ROOT
        entries = coverage.read_registry(root)
        studies = [
            "hermann-schmitz-ig-farben-finanz-ruestungsnetzwerk-1881-1960.md",
            "ig-farben-august-von-knieriem-1929-1957.md",
        ]
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        table = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        actors = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        sources = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        rels = yaml.safe_load((root / "data/relations.yml").read_text(encoding="utf-8"))["relations"]
        known = {relation["id"]: relation for relation in rels}
        distinct = set()
        for study in studies:
            decision = entries[study]
            self.assertEqual(decision["status"], "network")
            self.assertEqual(
                decision["sha256"],
                hashlib.sha256((root / "research" / study).read_bytes()).hexdigest(),
            )
            for relation_id in decision["relation_ids"]:
                distinct.add(relation_id)
                relation = known[relation_id]
                self.assertIn(f'id="{relation_id.lower()}"', table)
                self.assertIn(relation["label"], graph)
                for source_id in relation["sources"]:
                    self.assertIn(f'id="{source_id.lower()}"', sources)
        self.assertEqual(len(distinct), 14)
        self.assertIn("PER-DE-HERMANN-SCHMITZ", actors)
        self.assertIn("PER-DE-AUGUST-VON-KNIERIEM", actors)
        self.assertIn("ORG-INT-BIS", actors)


    def test_source_criticism_and_existing_network_coverage(self):
        root = coverage.ROOT
        registry = coverage.read_registry(root)
        mapping = {
            "cia-opc-kmmanly-qksnitch-gfw-1951-2024.md":
                ["REL-DE-KMM-001", "REL-DE-KMM-003", "REL-DE-KMM-011"],
            "organisation-gehlen-gruendung-ns-inlandsspionage-1945-1968.md":
                ["REL-DE-GEHLEN-001", "REL-DE-GEHLEN-006", "REL-DE-GEHLEN-008"],
            "bilderberg-washington-post-finanzierung-medienoffenlegung-2005-2012.md":
                ["REL-US-BBF-001", "REL-US-BBF-002", "REL-US-BBF-004"],
            "monica-crowley-ukraine-wuhan-covid-ursprung-2023-2026.md":
                ["REL-US-UA-BIOSEC-2022-001"],
            "cromwell-karl-i-geldgeber-quellenpruefung-1290-1656.md":
                ["REL-GB-CROM-1649-001", "REL-GB-CROM-1653-001",
                 "REL-GB-CROM-1655-001"],
        }
        relations = {
            row["id"]: row
            for row in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        table = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        people = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        sources = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        for study, required in mapping.items():
            with self.subTest(study=study):
                decision = registry[study]
                self.assertEqual(decision["status"], "network")
                self.assertEqual(
                    decision["sha256"],
                    hashlib.sha256((root / "research" / study).read_bytes()).hexdigest(),
                )
                self.assertTrue(set(required) <= set(decision["relation_ids"]))
                for relation_id in required:
                    relation = relations[relation_id]
                    self.assertIn(f'id="{relation_id.lower()}"', table)
                    self.assertIn(relation["label"], graph)
                    for source_id in relation["sources"]:
                        self.assertIn(f'id="{source_id.lower()}"', sources)
        for actor_id in (
            "ORG-US-DOD", "PRG-UA-BIOSAFETY-COOP",
            "PER-GB-ANTONIO-FERNANDES-CARVAJAL",
            "PER-GB-OLIVER-CROMWELL", "ORG-GB-PROTECTORATE-1653",
        ):
            self.assertIn(actor_id, people)

        no_relation = [
            "rockefeller-38-briefe-gier-zuschreibung-1918-2026.md",
            "lobbykontakte-exekutiver-fussabdruck-transparenz-2026.md",
            "atlantik-bruecke-demokratische-rechenschaft-2026.md",
        ]
        for study in no_relation:
            with self.subTest(no_relation_study=study):
                decision = registry[study]
                self.assertEqual(decision["status"], "no_network_relation")
                self.assertGreater(len(decision["reason"].strip()), 30)
                self.assertEqual(
                    decision["sha256"],
                    hashlib.sha256((root / "research" / study).read_bytes()).hexdigest(),
                )


    def test_p2_bank_studies_link_existing_evidenced_network(self):
        root = coverage.ROOT
        registry = coverage.read_registry(root)
        selected = {
            "p2-bafisud-bankrang-nmb-bcu-1980-1985.md": [
                "REL-UY-BAFISUD-NMB-1983-001",
                "REL-UY-BAFISUD-BCU-1984-001",
            ],
            "p2-bafisud-cisalpine-credito-varesino-1978-1983.md": [
                "REL-BS-UY-BAFISUD-1978-001",
                "REL-IT-PA-VARESINO-1978-001",
                "REL-PA-CH-VARESINO-1981-001",
                "REL-IT-UY-INTERBANK-DEPOSITS-1980-001",
            ],
            "p2-interalpha-ambrosiano-nmb-bafisud-bcu-1972-1984.md": [
                "REL-INT-INTERALPHA-1979-001",
                "REL-INT-INTERALPHA-1979-002",
                "REL-INT-INTERALPHA-1979-003",
                "REL-UY-BAFISUD-BCU-1984-001",
            ],
        }
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        table = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        source_index = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        relations = {
            relation["id"]: relation
            for relation in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        for name, expected_ids in selected.items():
            with self.subTest(study=name):
                decision = registry[name]
                self.assertEqual(decision["status"], "network")
                self.assertEqual(
                    decision["sha256"],
                    hashlib.sha256((root / "research" / name).read_bytes()).hexdigest(),
                )
                self.assertTrue(set(expected_ids) <= set(decision["relation_ids"]))
                for relation_id in expected_ids:
                    relation = relations[relation_id]
                    self.assertIn(relation["label"], graph)
                    self.assertIn(f'id="{relation_id.lower()}"', table)
                    for source_id in relation["sources"]:
                        self.assertIn(f'id="{source_id.lower()}"', source_index)
        # These direct, bounded relations are not a proof of majority control
        # or of a transfer from BAFISUD to political or violent beneficiaries.
        self.assertIn(
            "5,5 Prozent",
            relations["REL-BS-UY-BAFISUD-1978-001"]["label"],
        )
        self.assertIn(
            "Beträge nicht als identisch bewiesen",
            relations["REL-UY-BAFISUD-BCU-1984-001"]["label"],
        )


    def test_media_financing_and_warburg_legacy_coverage(self):
        root = coverage.ROOT
        registry = coverage.read_registry(root)
        mapped = {
            "bilderberg-american-friends-irs-medien-2004-2025.md":
                ["REL-US-BBF-001", "REL-US-BBF-002",
                 "REL-US-BBF-003", "REL-US-BBF-010"],
            "bilderberg-uk-minister-transparenz-polizeikosten-1993-2013.md":
                ["REL-GB-BB-UK-001", "REL-GB-BB-UK-002"],
            "atlantik-bruecke-halle-foerderbetraege-friends-2020-2026.md":
                ["REL-US-HALLE-AB-GRANT-2022",
                 "REL-US-HALLE-AB-GRANT-2023", "REL-US-ABFRIENDS-MERZ-2021"],
            "atlantik-bruecke-agenda-finanzierer-2021-2026.md":
                ["REL-DE-AB-NEW-BRIDGE-001", "REL-DE-JHS-AB-NEWBRIDGE-2026"],
            "ewk-bpa-apuz-presse-und-finanzierung-1951-1967.md":
                ["REL-DE-KMM-005", "REL-DE-KMM-009"],
            "warburg-bank-einfluss-1798-2026.md":
                ["REL-DE-CUMEX-001", "REL-DE-CUMEX-002"],
            "warburg-hamburg-steuerverwaltung-belegmatrix-2014-2026.md":
                ["REL-DE-CUMEX-001", "REL-DE-CUMEX-002"],
        }
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        table = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        actors = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        sources = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        relations = {
            relation["id"]: relation
            for relation in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        for name, ids in mapped.items():
            with self.subTest(study=name):
                entry = registry[name]
                self.assertEqual(entry["status"], "network")
                self.assertEqual(entry["sha256"], hashlib.sha256(
                    (root / "research" / name).read_bytes()
                ).hexdigest())
                self.assertTrue(set(ids) <= set(entry["relation_ids"]))
                for relation_id in ids:
                    relation = relations[relation_id]
                    self.assertIn(relation["label"], graph)
                    self.assertIn(f'id="{relation_id.lower()}"', table)
                    for source_id in relation["sources"]:
                        self.assertIn(f'id="{source_id.lower()}"', sources)
        self.assertIn("ORG-US-ATLANTIK-BRUECKE-FRIENDS-EIN202174611", actors)
        self.assertIn("PER-DE-FRIEDRICH-MERZ", actors)
        # Do not turn a historical, not image-confirmed role into present
        # ownership, corrupt influence or a verified donation transfer.
        historical = relations["REL-US-ABFRIENDS-MERZ-2021"]
        self.assertEqual(historical["evidence_level"], "plausible")
        self.assertIn("keine heutige Funktion", historical["label"])
        self.assertEqual(historical["period"], {"start": "2021"})


    def test_bis_reichsbank_and_ss_finance_are_source_bound(self):
        root = coverage.ROOT
        registry = coverage.read_registry(root)
        names = [
            "biz-bank-of-england-standardoil-rockefeller-mccloy-1930-1953.md",
            "schroeder-funk-puhl-himmler-biz-raubgold-1933-1949.md",
        ]
        relations = {
            relation["id"]: relation
            for relation in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        table = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        people = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        source_index = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        seen = set()
        for name in names:
            with self.subTest(study=name):
                entry = registry[name]
                self.assertEqual(entry["status"], "network")
                self.assertEqual(
                    entry["sha256"],
                    hashlib.sha256((root / "research" / name).read_bytes()).hexdigest(),
                )
                for relation_id in entry["relation_ids"]:
                    relation = relations[relation_id]
                    seen.add(relation_id)
                    self.assertIn(relation["label"], graph)
                    self.assertIn(f'id="{relation_id.lower()}"', table)
                    for source_id in relation["sources"]:
                        self.assertIn(f'id="{source_id.lower()}"', source_index)
        new_bis_ids = {
            relation_id for relation_id in seen
            if relation_id.startswith(
                ("REL-INT-BIS-1939-", "REL-DE-RB-", "REL-GB-BIS-GOLD-",
                 "REL-INT-BIS-GOLD-", "REL-DE-BIS-GOLD-",
                 "REL-DE-CH-SNB-GOLD-", "REL-DE-SS-")
            )
        }
        self.assertEqual(len(new_bis_ids), 16)
        for node in (
            "PER-DE-KURT-VON-SCHROEDER",
            "PER-DE-WALTHER-FUNK",
            "PER-DE-EMIL-PUHL",
            "PER-DE-OSWALD-POHL",
            "ORG-DE-REICHSBANK-HISTORIC",
            "ORG-GB-BANK-OF-ENGLAND-HISTORIC",
            "PRG-DE-HIMMLER-SONDERKONTO-S-1943",
        ):
            self.assertIn(node, people)
        # Court-examined victim property is not the same traceable gold
        # as the 3.7 tonnes of central-bank gold returned by BIS in 1948.
        self.assertIn("nicht mit Melmer-Opfergold gleichgesetzt",
                      relations["REL-DE-BIS-GOLD-1945-001"]["label"])
        # Puhl's subordinate BIS membership must not be promoted to director.
        self.assertIn("nur unter Stellvertreter",
                      relations["REL-INT-BIS-1939-003"]["label"])


    def test_eni_tradinvest_and_sudam_loan_claim_source_limits(self):
        root = coverage.ROOT
        name = "p2-sudam-bafisud-psi-parteien-medienfinanzierung-1979-1993.md"
        registry = coverage.read_registry(root)
        decision = registry[name]
        self.assertEqual(decision["status"], "network")
        self.assertEqual(
            decision["sha256"],
            hashlib.sha256((root / "research" / name).read_bytes()).hexdigest()
        )
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        network = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        actors = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        source_index = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        relations = {
            row["id"]: row
            for row in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        new_ids = [
            "REL-IT-ENI-TRAD-1979-001",
            "REL-BS-NI-TRAD-1979-001",
            "REL-BS-PE-TRAD-1979-001",
            "REL-BS-BS-TRAD-1979-001",
            "REL-BS-BS-TRAD-1979-002",
            "REL-BS-PE-TRAD-1980-001",
            "REL-INT-TRAD-SIEG-1979-001",
            "REL-BS-SIEG-1978-001",
            "REL-NI-SIEG-1978-001",
            "REL-IT-SIEG-CONSUL-1982-001",
            "REL-BS-PA-SUDAM-1980-001",
        ]
        self.assertTrue(set(new_ids) <= set(decision["relation_ids"]))
        for relation_id in new_ids:
            with self.subTest(relation=relation_id):
                relation = relations[relation_id]
                self.assertIn(relation["label"], graph)
                self.assertIn(f'id="{relation_id.lower()}"', network)
                for source_id in relation["sources"]:
                    self.assertIn(f'id="{source_id.lower()}"', source_index)
        for id_ in ("ORG-BS-TRADINVEST-ENI", "ORG-NI-AMBROSIANO-MANAGUA",
                    "ORG-PE-AMBROSIANO-ANDINO", "PER-INT-PIERRE-W-SIEGENTHALER"):
            self.assertIn(id_, actors)
        # The 1979 12.5m original and its 6.5m/6m reallocation
        # are the same credit exposure, NOT three disbursements.
        self.assertIn("keine drei addierbaren",
                      relations["REL-BS-NI-TRAD-1979-001"]["label"])
        # The 1980 50m ENI–Andino loan is distinct from the
        # alleged Sudam loan of 21m and does not document PSI receipts.
        self.assertIn("kein Beleg für spätere PSI-Zahlung",
                      relations["REL-BS-PE-TRAD-1980-001"]["label"])
        claimed = relations["REL-BS-PA-SUDAM-1980-001"]
        self.assertEqual(claimed["evidence_level"], "plausible")
        self.assertIn("PSI-Endzahlung nicht durch Bankkonto belegt",
                      claimed["label"])
        consular = relations["REL-IT-SIEG-CONSUL-1982-001"]
        self.assertEqual(consular["period"]["start"], "1982-06-30")


    def test_bdj_nsu_british_media_legacy_studies_are_graph_linked(self):
        root = coverage.ROOT
        mapping = {
            "bdj-lcprowl-eca-mccloy-1950-1953.md":
                ["REL-DE-BDJ-001", "REL-DE-BDJ-002"],
            "nsu-komplex-skandale-belegmatrix-1994-2026.md":
                ["REL-DE-THS-001", "REL-DE-THS-002", "REL-DE-UKC18-001"],
            "britische-neonazinetzwerke-combat18-blood-honour-nsu-1991-2026.md":
                ["REL-DE-UKC18-001", "REL-DE-UKC18-002", "REL-DE-UKC18-003"],
            "piatto-verfassungsschutz-justiz-npd-nsu-1994-2000.md":
                ["REL-DE-UKC18-001"],
            "bilderberg-medien-diskretion-originalakten-1954-2026.md":
                ["REL-GB-BB-UK-006", "REL-GB-BB-UK-007",
                 "REL-US-BBF-008", "REL-US-BBF-009"],
            "atlantik-bruecke-medieninteressenkonflikte-1952-2026.md":
                ["REL-GB-BB-UK-006", "REL-GB-BB-UK-007",
                 "REL-US-BBF-008", "REL-US-BBF-009"],
            "atlantik-bruecke-bilderberg-vergleich-2026.md":
                ["REL-GB-BB-UK-006", "REL-GB-BB-UK-007",
                 "REL-US-BBF-008", "REL-US-BBF-009"],
        }
        registry = coverage.read_registry(root)
        links = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        sources = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        relations = {
            relation["id"]: relation
            for relation in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        for study, ids in mapping.items():
            with self.subTest(study=study):
                decision = registry[study]
                self.assertEqual(decision["status"], "network")
                self.assertEqual(
                    decision["sha256"],
                    hashlib.sha256((root / "research" / study).read_bytes()).hexdigest(),
                )
                self.assertEqual(set(decision["relation_ids"]), set(ids))
                for relation_id in ids:
                    relation = relations[relation_id]
                    self.assertIn(f'id="{relation_id.lower()}"', links)
                    self.assertIn(relation["label"], graph)
                    for source_id in relation["sources"]:
                        self.assertIn(f'id="{source_id.lower()}"', sources)
        # Documented state financing and informant handling do not
        # prove state orders for unrelated murders or UK intelligence control.
        self.assertIn(
            "keine MI5-Kante",
            relations["REL-DE-UKC18-002"]["label"],
        )
        self.assertIn(
            "keine britische Dienstanweisung",
            relations["REL-DE-UKC18-003"]["label"],
        )


if __name__ == "__main__":
    unittest.main()