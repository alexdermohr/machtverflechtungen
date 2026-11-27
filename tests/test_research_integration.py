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
                ["REL-DE-THS-001", "REL-DE-THS-002", "REL-DE-UKC18-001",
                 "REL-DE-NSU-HH-GBA-2026-001",
                 "REL-DE-NSU-LINGEN-STA-2018-001",
                 "REL-DE-NSU-LINGEN-BFV-2013-001",
                 "REL-DE-NSU-BVERWG-BFV-2020-001",
                 "REL-DE-NSU-LINGEN-TLFV-2002-001",
                 "REL-DE-NSU-BFV-PARL-DATE-2012-001",
                 "REL-DE-NSU-MAD-BFV-1999-001",
                 "REL-DE-NSU-MAD-TLFV-1999-001",
                 "REL-DE-NSU-GBA-PRUEFUNG-1999-001",
                 "REL-DE-NSU-FRITSCHE-BMI-2003-001",
                 "REL-DE-NSU-LKA-VP562-001",
                 "REL-DE-NSU-GBA-BERLIN-2012-001",
                 "REL-DE-NSU-GBA-WERNER-ASSERVATE-2014-001",
                 "REL-DE-NSU-STA-GBA-2016-001",
                 "REL-DE-NSU-ST-LKA-DATENTRAEGER-2014-001",
                 "REL-DE-NSU-ST-LFV-DATENTRAEGER-2014-001",
                 "REL-DE-NSU-GBA-STARKE-VERTRAULICHKEIT-001",
                 "REL-DE-NSU-BERLIN-LFV-AKTEN-2012-001",
                 "REL-DE-NSU-GERA-TLFV-FRAGEN-001",
                 "REL-DE-NSU-TLFV-GERA-AKTEN-001",
                 "REL-DE-NSU-BFV-G10-VERNICHTUNG-001",
                 "REL-DE-NSU-BMI-BFV-G10-2011-001",
                 "REL-DE-NSU-BMI-BFV-MORATORIUM-2012-001",
                 "REL-DE-NSU-MAD-AKTEN-2012-001",
                 "REL-DE-NSU-BMVG-MAD-KENNTNIS-2012-001"],
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

    def test_brandenburg_nabe_warning_and_constitutional_court_diverge(self):
        root = coverage.ROOT
        study = "brandenburg-nabe-razziawarnung-aktenzugang-2001-2004.md"
        decision = coverage.read_registry(root)[study]
        self.assertEqual(decision["status"], "network")
        self.assertEqual(
            decision["sha256"],
            hashlib.sha256((root / "research" / study).read_bytes()).hexdigest(),
        )
        rows = {
            row["id"]: row
            for row in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        network = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        actors = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        sources = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        court = [
            "REL-DE-BB-VERFG-2004-001",
            "REL-DE-BB-VERFG-2004-002",
            "REL-DE-BB-VERFG-2004-003",
        ]
        warnings = ["REL-DE-BB-NABE-2001-001", "REL-DE-BB-NABE-2001-002"]
        self.assertEqual(set(decision["relation_ids"]), set(court + warnings))
        for relation_id in court + warnings:
            relation = rows[relation_id]
            self.assertIn(relation["label"], graph)
            self.assertIn(f'id="{relation_id.lower()}"', network)
            for source_id in relation["sources"]:
                self.assertIn(f'id="{source_id.lower()}"', sources)
        for node in ("ORG-DE-VERFG-BRANDENBURG",
                     "PER-DE-KERSTIN-KAISER-NICHT",
                     "PER-DE-HEINZ-VIETZE",
                     "PER-DE-CHRISTIAN-K-2001",
                     "PER-DE-SVEN-SCH-2001"):
            self.assertIn(node, actors)
        self.assertEqual(
            rows[court[0]]["evidence_level"], "established"
        )
        self.assertEqual(rows[warnings[1]]["evidence_level"], "strong")
        self.assertIn("keine automatische Herausgabe", rows[court[0]]["label"])
        self.assertIn("als verfassungsgemäß", rows[court[1]]["label"])
        self.assertIn("Originalmitschnitt", rows[warnings[1]]["label"])
        self.assertNotIn("SRC-DE-BB-NSU-GRUENE-SONDERVOTUM-2019",
                         rows[court[0]]["sources"])
        self.assertNotIn("SRC-DE-VERFG-BRANDENBURG-604-20041209",
                         rows[warnings[1]]["sources"])

    def test_kiep_schreiber_and_sponsorship_are_source_bound(self):
        root = coverage.ROOT
        name = "atlantik-bruecke-kiep-schreiber-ruestung-sponsoren-1991-2010.md"
        decision = coverage.read_registry(root)[name]
        self.assertEqual(decision["status"], "network")
        self.assertEqual(
            decision["sha256"],
            hashlib.sha256((root / "research" / name).read_bytes()).hexdigest(),
        )
        relations = {
            relation["id"]: relation
            for relation in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        sources = {
            source["id"]: source
            for source in yaml.safe_load(
                (root / "data/sources.yml").read_text(encoding="utf-8")
            )["sources"]
        }
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        table = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        chronology = (root / "docs/generated/relation-timeline.md").read_text(encoding="utf-8")
        focus = (root / "docs/generated/network-focus-atlantik-bruecke.md").read_text(encoding="utf-8")
        actors = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        source_index = (root / "docs/quellen/index.md").read_text(encoding="utf-8")

        self.assertEqual(len(decision["relation_ids"]), 18)
        for id_ in decision["relation_ids"]:
            with self.subTest(relation=id_):
                relation = relations[id_]
                self.assertIn(relation["label"], graph)
                self.assertIn(f'id="{id_.lower()}"', table)
                self.assertIn(f"[{id_}](network.md#{id_.lower()})", chronology)
                for source_id in relation["sources"]:
                    self.assertIn(f'id="{source_id.lower()}"', source_index)
                    self.assertIn(source_id, sources)
        for node in (
            "PER-DE-WALTHER-LEISLER-KIEP", "PER-DE-KARLHEINZ-SCHREIBER",
            "ORG-DE-CDU-1991", "ORG-PA-ATG-1991",
            "ORG-DE-DEUTSCHE-BANK-2008", "ORG-DE-BUNDESBANK-2008",
        ):
            self.assertIn(node, actors)

        named_sponsors = [
            id_ for id_ in decision["relation_ids"]
            if id_.endswith("-SPONSOR-2009-001")
        ]
        self.assertEqual(len(named_sponsors), 8)
        for id_ in named_sponsors:
            self.assertRegex(relations[id_]["label"], r"[Bb]etrag|Geldtransfer|Geldfluss")
            self.assertEqual(relations[id_]["evidence_level"], "strong")
            self.assertIn(
                "SRC-DE-AB-JB-2008-2009", relations[id_]["sources"]
            )
            self.assertIn(f"[{id_}](network.md#{id_.lower()})", focus)
        self.assertIn("keine vereinsseitige Autorisierung",
                      relations["REL-DE-AB-KIEP-KOHL-1993-001"]["label"])
        self.assertIn("keine unabhängige Atlantik-Brücke-Spende",
                      relations["REL-DE-AB-SCHREIBER-KIEP-CASH-1991-001"]["label"])
        self.assertIn("nicht erneut zu addieren",
                      relations["REL-DE-AB-KIEP-CDU-DONATION-1991-001"]["label"])
        self.assertEqual(
            sources["SRC-DE-BT-PARTEISPENDEN-KIEP-SCHREIBER-2002"]["tier"], "A"
        )
        self.assertEqual(
            sources["SRC-DE-AB-JB-2008-2009"]["tier"], "B"
        )


    def test_journalism_grants_2012_do_not_imply_media_control(self):
        root = coverage.ROOT
        name = "atlantik-bruecke-journalistenreisen-zeit-gmf-1983-2012.md"
        decision = coverage.read_registry(root)[name]
        self.assertEqual(decision["status"], "network")
        self.assertEqual(
            decision["sha256"],
            hashlib.sha256((root / "research" / name).read_bytes()).hexdigest(),
        )
        relations = {
            x["id"]: x for x in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        sources = {
            x["id"]: x for x in yaml.safe_load(
                (root / "data/sources.yml").read_text(encoding="utf-8")
            )["sources"]
        }
        network = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        chrono = (root / "docs/generated/relation-timeline.md").read_text(encoding="utf-8")
        actors = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        source_index = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        focus = (root / "docs/generated/network-focus-atlantik-bruecke.md").read_text(encoding="utf-8")
        self.assertEqual(len(decision["relation_ids"]), 9)
        for relation_id in decision["relation_ids"]:
            with self.subTest(relation=relation_id):
                relation = relations[relation_id]
                self.assertIn(relation["label"], graph)
                self.assertIn(f'id="{relation_id.lower()}"', network)
                self.assertIn(
                    f"[{relation_id}](network.md#{relation_id.lower()})", chrono
                )
                for source_id in relation["sources"]:
                    self.assertIn(source_id, sources)
                    self.assertIn(f'id="{source_id.lower()}"', source_index)
        self.assertIn(
            "[REL-DE-AB-JOUR-ORGANIZED-1983-001](network.md#rel-de-ab-jour-organized-1983-001)",
            focus,
        )
        for node in (
            "ORG-DE-ZEIT-STIFTUNG-1991", "ORG-DE-ROBERT-BOSCH-STIFTUNG",
            "ORG-US-GMF-2012", "ORG-US-ACG-2012", "ORG-US-AICGS-2012",
            "ORG-US-FORMER-CONGRESS-MEMBERS-2012",
            "PRG-US-ARTHUR-BURNS-FELLOWSHIP-2012",
        ):
            self.assertIn(node, actors)

        distinct_grants = {
            "REL-US-GMF-ACG-2012-001": 50000,
            "REL-US-GMF-AICGS-2012-001": 50000,
            "REL-US-GMF-FORMER-CONGRESS-2012-001": 90000,
            "REL-US-GMF-ARTHUR-BURNS-2012-001": 20000,
        }
        self.assertEqual(sum(distinct_grants.values()), 210000)
        for relation_id, amount in distinct_grants.items():
            relation = relations[relation_id]
            self.assertIn(f"{amount:,}".replace(",", "."), relation["label"])
            self.assertEqual(relation["sources"], ["SRC-US-GMF-IRS-990-SCHEDULE-I-2012"])
            self.assertEqual(relation["evidence_level"], "established")
        self.assertEqual(sources["SRC-US-GMF-IRS-990-SCHEDULE-I-2012"]["tier"], "A")
        self.assertEqual(sources["SRC-DE-ZEITST-PECHEL-BUCERIUS-1992"]["tier"], "B")
        for relation_id in ("REL-DE-AB-JOUR-BOSCH-1992-001",
                            "REL-DE-AB-JOUR-GMF-1992-001"):
            self.assertNotIn("period", relations[relation_id])
        self.assertIn("nicht mit IRS-Grants von 2012 gleichzusetzen",
                      relations["REL-DE-AB-JOUR-GMF-1992-001"]["label"])
        self.assertIn("kein Beleg einer inhaltlich beauftragten",
                      relations["REL-US-GMF-ARTHUR-BURNS-2012-001"]["label"])


    def test_p2_rizzoli_archival_financing_and_press_contracts(self):
        root = coverage.ROOT
        name = "p2-rizzoli-corriere-ambrosiano-mediensteuerung-1975-1984.md"
        decision = coverage.read_registry(root)[name]
        self.assertEqual(decision["status"], "network")
        self.assertEqual(
            decision["sha256"],
            hashlib.sha256((root / "research" / name).read_bytes()).hexdigest(),
        )
        self.assertEqual(len(decision["relation_ids"]), 21)
        relations = {
            x["id"]: x
            for x in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        sources = {
            x["id"]: x
            for x in yaml.safe_load(
                (root / "data/sources.yml").read_text(encoding="utf-8")
            )["sources"]
        }
        network = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        chrono = (root / "docs/generated/relation-timeline.md").read_text(encoding="utf-8")
        source_index = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        for id_ in decision["relation_ids"]:
            with self.subTest(relation=id_):
                row = relations[id_]
                self.assertIn(row["label"], graph)
                self.assertIn(f'id="{id_.lower()}"', network)
                self.assertIn(f"[{id_}](network.md#{id_.lower()})", chrono)
                for source in row["sources"]:
                    self.assertIn(f'id="{source.lower()}"', source_index)
                    self.assertEqual(sources[source]["tier"], "A")
        signed_1980 = [
            x for x in decision["relation_ids"]
            if x.startswith("REL-IT-P2-AGREEMENT-")
            and x != "REL-IT-P2-AGREEMENT-RIZZOLI-CORP-1980-001"
        ]
        signed_1979 = [
            x for x in decision["relation_ids"]
            if x.startswith("REL-IT-P2-PRESSPACT-")
            and x != "REL-IT-P2-PRESSPACT-PUBLISHER-1979-001"
        ]
        self.assertEqual(len(signed_1980), 5)
        self.assertEqual(len(signed_1979), 4)
        self.assertTrue(all(relations[x]["period"]["start"] == "1980-09-18" for x in signed_1980))
        self.assertTrue(all(relations[x]["period"]["start"] == "1979-07-05" for x in signed_1979))
        self.assertIn(
            "22,5 Milliarden Lire",
            relations["REL-IT-AMBROSIANO-RIZZOLI-1980-001"]["label"],
        )
        self.assertEqual(relations["REL-IT-P2-RIZZOLI-1975-1981-001"]["evidence_level"], "strong")
        self.assertIn(
            "keine nachgewiesene Steuerung jedes Corriere-Beitrags",
            relations["REL-IT-P2-RIZZOLI-EDITORIAL-1980-001"]["label"],
        )
        self.assertIn(
            "bestritt", relations["REL-IT-P2-PRESSPACT-SCALFARI-1979-001"]["label"]
        )
        self.assertIn(
            "18/1/1980", sources["SRC-IT-P2-RIZZOLI-PERRELLA-PARAPHS-1980"]["locator"]
        )
        entities = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        self.assertIn("Historische Vertragsurkunden", entities)
        p2focus = (root / "docs/generated/network-focus-p2.md").read_text(encoding="utf-8")
        rizzolifocus = (root / "docs/generated/network-focus-rizzoli.md").read_text(encoding="utf-8")
        self.assertIn("REL-IT-P2-RIZZOLI-1975-1981-001", p2focus)
        self.assertIn("REL-IT-AMBROSIANO-RIZZOLI-1980-001", rizzolifocus)


    def test_acg_erp_program_grants_and_meetings_stay_distinct(self):
        root = coverage.ROOT
        study = "acg-erp-projektfoerderung-2018-2019.md"
        entry = coverage.read_registry(root)[study]
        self.assertEqual(entry["status"], "network")
        self.assertEqual(entry["sha256"], hashlib.sha256(
            (root / "research" / study).read_bytes()
        ).hexdigest())
        self.assertEqual(len(entry["relation_ids"]), 9)
        relations = {
            r["id"]: r for r in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        sources = {
            s["id"]: s for s in yaml.safe_load(
                (root / "data/sources.yml").read_text(encoding="utf-8")
            )["sources"]
        }
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        network = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        chronology = (root / "docs/generated/relation-timeline.md").read_text(encoding="utf-8")
        sources_index = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        actors = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        for relation_id in entry["relation_ids"]:
            with self.subTest(relation=relation_id):
                row = relations[relation_id]
                self.assertIn(row["label"], graph)
                self.assertIn(f'id="{relation_id.lower()}"', network)
                self.assertIn(
                    f"[{relation_id}](network.md#{relation_id.lower()})",
                    chronology,
                )
                for source in row["sources"]:
                    self.assertIn(f'id="{source.lower()}"', sources_index)
                    self.assertIn(source, sources)
        for node in (
            "PRG-DE-ERP-TRANSATLANTIK-2019", "ORG-DE-BMWI-2019",
            "PRG-US-ACG-CITIES-2019", "PRG-US-ACG-WARBURG-2018",
            "ORG-DE-BDI-2019", "PER-DE-MARJA-LIISA-VOELLERS-2019",
        ):
            self.assertIn(node, actors)

        budget = relations["REL-DE-ERP-BMWI-2019-001"]
        self.assertEqual(budget["evidence_level"], "established")
        self.assertIn("3,6 Mio. EUR", budget["label"])
        self.assertIn("weder ACG-Bewilligung", budget["label"])
        self.assertIn(
            "SRC-DE-BGBL-ERP-2019-TITLE-68103", budget["sources"]
        )
        self.assertEqual(
            sources["SRC-DE-BGBL-ERP-2019-TITLE-68103"]["tier"], "A"
        )
        bracket = relations["REL-US-ERP-ACG-GRANTBRACKET-2018-001"]
        self.assertEqual(bracket["evidence_level"], "strong")
        self.assertIn("kein geprüfter Kontotransfer", bracket["label"])
        tours = relations["REL-US-ERP-ACG-WARBURG-2018-001"]
        self.assertIn("zehn Rednertouren", tours["label"])
        self.assertIn("keine 70 ERP-finanzierten Reisen", tours["label"])
        cities = relations["REL-US-ERP-ACG-CITIES-2019-001"]
        self.assertIn("nicht zu zwei nachgewiesenen Bundesüberweisungen", cities["label"])
        for id_ in ("REL-US-ACG-CITIES-BMWI-2019-001",
                    "REL-US-ACG-CITIES-BDI-2019-001",
                    "REL-US-ACG-CITIES-VOELLERS-2019-001"):
            self.assertEqual(relations[id_]["evidence_level"], "strong")
        self.assertNotEqual(
            budget["to"], cities["to"],
            "The whole ERP budget must never be attributed to the ACG trip",
        )


    def test_bologna_bank_files_post_bomb_timing_and_prosecutorial_claims(self):
        root = coverage.ROOT
        study = "bologna-p2-ambrosiano-geldfluesse-1979-2026.md"
        decision = coverage.read_registry(root)[study]
        self.assertEqual(decision["status"], "network")
        self.assertEqual(
            decision["sha256"], hashlib.sha256(
                (root / "research" / study).read_bytes()
            ).hexdigest()
        )
        self.assertEqual(len(decision["relation_ids"]), 8)
        relations = {
            x["id"]: x for x in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        sources = {
            x["id"]: x for x in yaml.safe_load(
                (root / "data/sources.yml").read_text(encoding="utf-8")
            )["sources"]
        }
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        table = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        timeline = (root / "docs/generated/relation-timeline.md").read_text(encoding="utf-8")
        source_index = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        actors = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        focus = (root / "docs/generated/network-focus-ubs-genf-1980.md").read_text(encoding="utf-8")
        for id_ in decision["relation_ids"]:
            with self.subTest(id=id_):
                record = relations[id_]
                self.assertIn(record["label"], graph)
                self.assertIn(f'id="{id_.lower()}"', table)
                self.assertIn(
                    f"[{id_}](network.md#{id_.lower()})", timeline
                )
                for source in record["sources"]:
                    self.assertIn(f'id="{source.lower()}"', source_index)
                    self.assertIn(source, sources)
        for node in (
            "ORG-CH-UBS-GENEVA-1980", "PER-IT-MARCO-CERUTI-1980",
            "PER-IT-FEDERICO-UMBERTO-DAMATO",
            "DOC-IT-DOCUMENTO-BOLOGNA-1982",
            "ORG-IT-PROCURA-GENERALE-BOLOGNA-2024",
        ):
            self.assertIn(node, actors)
        for id_ in ("REL-CH-UBS-GELLI-1981-001",
                    "REL-CH-UBS-CERUTI-1981-001",
                    "REL-PE-CH-BOLOGNA-ANDINO-UBS-1980-001"):
            self.assertIn(id_, focus)
        post = relations["REL-PE-CH-BOLOGNA-ANDINO-UBS-1980-001"]
        self.assertEqual(post["period"]["start"], "1980-08-22")
        self.assertIn("NACH dem Anschlag 02.08.1980", post["label"])
        self.assertIn("Teilmenge, nicht zusätzliche Zahlung", post["label"])
        for id_ in ("REL-IT-BOLOGNA-PG-GELLI-2024-001",
                    "REL-IT-BOLOGNA-PG-DAMATO-2024-001"):
            self.assertEqual(relations[id_]["evidence_level"], "plausible")
            self.assertEqual(
                relations[id_]["sources"],
                ["SRC-IT-BOLOGNA-PG-REPORT-2024"]
            )
        self.assertIn(
            "keine persönliche neue Verurteilung",
            relations["REL-IT-BOLOGNA-PG-DAMATO-2024-001"]["label"]
        )
        self.assertEqual(
            relations["REL-IT-BOLOGNA-GELLI-DOCUMENT-1982-001"]["period"],
            {"start": "1982-09-13"}
        )
        self.assertEqual(sources["SRC-IT-P2-UBS-GELLI-CERUTI-19810511"]["tier"], "A")
        self.assertEqual(
            sources["SRC-IT-BOLOGNA-DOMANI-COURT-EXCERPT-2024"]["tier"], "B"
        )


    def test_mccloy_1975_federal_fund_is_not_1973_ford_grant(self):
        root = coverage.ROOT
        study = "acg-mccloy-fund-ford-archiv-1973-1975.md"
        decision = coverage.read_registry(root)[study]
        self.assertEqual(decision["status"], "network")
        self.assertEqual(
            decision["sha256"],
            hashlib.sha256((root / "research" / study).read_bytes()).hexdigest(),
        )
        self.assertEqual(len(decision["relation_ids"]), 8)
        relations = {
            r["id"]: r for r in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        sources = {
            s["id"]: s for s in yaml.safe_load(
                (root / "data/sources.yml").read_text(encoding="utf-8")
            )["sources"]
        }
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        network = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        chrono = (root / "docs/generated/relation-timeline.md").read_text(encoding="utf-8")
        actors = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        source_index = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        for id_ in decision["relation_ids"]:
            with self.subTest(relation=id_):
                row = relations[id_]
                self.assertIn(row["label"], graph)
                self.assertIn(f'id="{id_.lower()}"', network)
                self.assertIn(f"[{id_}](network.md#{id_.lower()})", chrono)
                for source_id in row["sources"]:
                    self.assertIn(f'id="{source_id.lower()}"', source_index)
                    self.assertIn(source_id, sources)
        for name in (
            "PRG-US-MCCLOY-FUND-1975", "ORG-DE-BUNDESREGIERUNG-1975",
            "PER-US-JOHN-J-MCCLOY", "PER-DE-WALTER-SCHEEL",
            "PER-US-GERALD-FORD", "ORG-US-FORD-FOUNDATION-1973",
            "PRG-US-ACG-MCCLOY-FELLOWSHIPS-1976",
        ):
            self.assertIn(name, actors)
        federal = relations["REL-US-ACG-MCCLOY-FUND-GOV-1975-001"]
        self.assertEqual(federal["period"]["start"], "1975-06-16")
        self.assertEqual(federal["evidence_level"], "established")
        self.assertIn("1.000.000 USD", federal["label"])
        self.assertIn("kein selbst eingesehener", federal["label"].lower())
        self.assertIn("SRC-US-FORD-PRESIDENTIAL-DIARY-19750616",
                      federal["sources"])
        self.assertEqual(
            sources["SRC-US-FORD-PRESIDENTIAL-DIARY-19750616"]["tier"], "A"
        )
        ford = relations["REL-US-FORDFOUNDATION-YOUNGLEADERS-1973-001"]
        self.assertEqual(ford["period"]["start"], "1973-06-27")
        self.assertEqual(ford["evidence_level"], "strong")
        self.assertEqual(
            ford["sources"], ["SRC-GB-ZETSCHE-PHD-ACG-YOUNG-FORD-1973"]
        )
        self.assertEqual(
            sources["SRC-GB-ZETSCHE-PHD-ACG-YOUNG-FORD-1973"]["tier"], "B"
        )
        fellowships = relations["REL-US-ACG-MCCLOY-FELLOWSHIPS-1976-001"]
        self.assertEqual(fellowships["period"]["start"], "1976")
        self.assertIn("nicht vorgelegt", fellowships["label"])



    def test_warburg_eug_capital_votes_2023_and_2025_decision(self):
        root = coverage.ROOT
        registry = coverage.read_registry(root)
        main_study = "warburg-ezb-stimmrechtskontrolle-2013-2026.md"
        ownership_study = "warburg-gruppe-eigentum-kontrolle-registervergleich-2016-2026.md"
        for study in (main_study, ownership_study):
            self.assertEqual(registry[study]["status"], "network")
            self.assertEqual(
                registry[study]["sha256"],
                hashlib.sha256((root / "research" / study).read_bytes()).hexdigest(),
            )
        self.assertEqual(len(registry[main_study]["relation_ids"]), 10)
        self.assertEqual(len(registry[ownership_study]["relation_ids"]), 6)
        relations = {
            row["id"]: row for row in yaml.safe_load(
                (root / "data/relations.yml").read_text(encoding="utf-8")
            )["relations"]
        }
        sources = {
            row["id"]: row for row in yaml.safe_load(
                (root / "data/sources.yml").read_text(encoding="utf-8")
            )["sources"]
        }
        src = "SRC-EU-GENERAL-COURT-WARBURG-T36623-2025"
        self.assertEqual(sources[src]["tier"], "A")
        self.assertEqual(sources["SRC-EU-CJ-WARBURG-APPEAL-C39P-2026"]["tier"], "A")
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        network = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        chrono = (root / "docs/generated/relation-timeline.md").read_text(encoding="utf-8")
        focus = (root / "docs/generated/network-focus-warburg-kontrolle.md").read_text(encoding="utf-8")
        source_index = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        entities = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        self.assertIn(f'id="{src.lower()}"', source_index)
        for relid in registry[main_study]["relation_ids"]:
            row = relations[relid]
            if relid == "REL-EU-WARBURG-EUG-DECISION-2025-001":
                self.assertEqual(row["sources"], [src, "SRC-EU-CJ-WARBURG-APPEAL-C39P-2026"])
            else:
                self.assertEqual(row["sources"], [src])
            self.assertIn(row["label"], graph)
            self.assertIn(f'id="{relid.lower()}"', network)
            self.assertIn(f"[{relid}](network.md#{relid.lower()})", chrono)
        for relid in (
            "REL-DE-WARBURG-GRUPPE-BANK-2023-001",
            "REL-DE-WARBURG-BANK-MARCARD-2023-001",
            "REL-DE-WARBURG-BANK-HYPO-2023-001",
        ):
            self.assertIn(relid, focus)
        for entity in ("ORG-DE-WARBURG-MWB1-2023", "ORG-DE-WARBURG-GRUPPE-2023",
                       "ORG-DE-WARBURG-FMWV-2013", "ORG-EU-ECB-2023"):
            self.assertIn(entity, entities)
        fmvw = relations["REL-DE-WARBURG-FMWV-MWB1-2013-001"]
        self.assertEqual(fmvw["period"]["start"], "2013")
        self.assertIn("87,5 %", fmvw["label"])
        self.assertIn("51 % Stimmen", fmvw["label"])
        self.assertIn("keine ungeprüfte aktualisierung auf 2026",
                      relations["REL-DE-WARBURG-MWB1-GRUPPE-2023-001"]["label"].lower())
        hypo = relations["REL-DE-WARBURG-BANK-HYPO-2023-001"]
        self.assertEqual(hypo["period"]["end"], "2023-06-01")
        self.assertIn("nur beabsichtigt",
                      relations["REL-EU-WARBURG-ECB-OPPOSITION-2023-001"]["label"])
        self.assertEqual(
            relations["REL-EU-WARBURG-EUG-DECISION-2025-001"]["period"]["start"],
            "2025-11-19",
        )



    def test_springer_warburg_2006_contract_is_separate_from_2012_voting_pool(self):
        root = coverage.ROOT
        study = "warburg-axel-springer-doepfner-finanzierung-2006-2025.md"
        entry = coverage.read_registry(root)[study]
        self.assertEqual(entry["status"], "network")
        self.assertEqual(
            entry["sha256"],
            hashlib.sha256((root / "research" / study).read_bytes()).hexdigest(),
        )
        self.assertEqual(len(entry["relation_ids"]), 11)
        relations = {r["id"]: r for r in yaml.safe_load(
            (root / "data/relations.yml").read_text(encoding="utf-8")
        )["relations"]}
        sources = {r["id"]: r for r in yaml.safe_load(
            (root / "data/sources.yml").read_text(encoding="utf-8")
        )["sources"]}
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        table = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        chrono = (root / "docs/generated/relation-timeline.md").read_text(encoding="utf-8")
        focus = (root / "docs/generated/network-focus-springer-doepfner.md").read_text(encoding="utf-8")
        source_index = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        actors = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        for relid in entry["relation_ids"]:
            row = relations[relid]
            self.assertIn(row["label"], graph)
            self.assertIn(f'id="{relid.lower()}"', table)
            self.assertIn(f"[{relid}](network.md#{relid.lower()})", chrono)
            for sid in row["sources"]:
                self.assertIn(sid, sources)
                self.assertIn(f'id="{sid.lower()}"', source_index)
                self.assertEqual(sources[sid]["tier"], "A")
        for doc in ("DOC-DE-SPRINGER-VINKULIERUNG-2006",
                    "DOC-DE-SPRINGER-VOTING-POOL-2012",
                    "ORG-DE-BRILLIANT-310-2006"):
            self.assertIn(doc, actors)
        for rel in ("REL-DE-DOEPFNER-BRILLIANT-MANAGEMENT-2006-001",
                    "REL-DE-DOEPFNER-SPRINGER-VINK-2006-001",
                    "REL-DE-DOEPFNER-SPRINGER-POOL-2012-001",
                    "REL-DE-SPRINGER-DOEPFNER-EQUITY-2006-001",
                    "REL-DE-FRIEDE-DOEPFNER-GIFT-2012-001"):
            self.assertIn(rel, focus)
        bank_contract = relations["REL-DE-WARBURG-SPRINGER-VINK-2006-001"]
        self.assertEqual(bank_contract["period"], {"start":"2006-07-31","end":"2006-08-04"})
        self.assertIn("NICHT individuelle Kredithöhe",bank_contract["label"])
        shares = relations["REL-DE-SPRINGER-DOEPFNER-EQUITY-2006-001"]
        self.assertIn("52,36 Mio.", shares["label"])
        self.assertIn("keine Darlehenssumme", shares["label"])
        self.assertEqual(relations["REL-DE-FRIEDE-DOEPFNER-GIFT-2012-001"]["period"]["start"], "2012-08-14")
        pool = relations["REL-DE-SPRINGER-VOTING-POOL-2012-001"]
        self.assertIn("52.826.967",pool["label"])
        self.assertNotIn("Warburg",pool["from"])
        self.assertNotIn("Bankkredit 60 Mio.",pool["label"])
        brilliant = relations["REL-DE-BRILLIANT-SPRINGER-ACQ-2006-001"]
        self.assertEqual(brilliant["period"]["start"], "2006-07-13")
        self.assertIn("104,10 EUR", brilliant["label"])
        self.assertIn("77 EUR", brilliant["label"])
        self.assertIn("nicht ohne Transaktionsakten gleichsetzen", brilliant["label"])




    def test_warburg_pincus_1978_self_report_separated_from_dol_rule_and_fed_market_data(self):
        root = coverage.ROOT
        name = "warburg-pincus-erisa-pensionskapital-1977-1980.md"
        entry = coverage.read_registry(root)[name]
        self.assertEqual(entry["status"], "network")
        self.assertEqual(
            entry["sha256"],
            hashlib.sha256((root / "research" / name).read_bytes()).hexdigest(),
        )
        self.assertEqual(len(entry["relation_ids"]), 7)
        rels = {r["id"]: r for r in yaml.safe_load(
            (root / "data/relations.yml").read_text(encoding="utf-8")
        )["relations"]}
        sources = {r["id"]: r for r in yaml.safe_load(
            (root / "data/sources.yml").read_text(encoding="utf-8")
        )["sources"]}
        graph = (root / "docs/generated/network-graph.md").read_text(encoding="utf-8")
        table = (root / "docs/generated/network.md").read_text(encoding="utf-8")
        chrono = (root / "docs/generated/relation-timeline.md").read_text(encoding="utf-8")
        focus = (root / "docs/generated/network-focus-warburg-pincus-erisa.md").read_text(encoding="utf-8")
        source_index = (root / "docs/quellen/index.md").read_text(encoding="utf-8")
        actors = (root / "docs/generated/entities.md").read_text(encoding="utf-8")
        for relid in entry["relation_ids"]:
            row = rels[relid]
            self.assertIn(row["label"], graph)
            self.assertIn(f'id="{relid.lower()}"', table)
            self.assertIn(f"[{relid}](network.md#{relid.lower()})", chrono)
            for sid in row["sources"]:
                self.assertIn(sid, sources)
                self.assertIn(f'id="{sid.lower()}"', source_index)
        self.assertEqual(sources["SRC-US-WARBURG-PINCUS-FIRM-HISTORY-1978"]["tier"], "B")
        self.assertEqual(sources["SRC-US-DOL-ERISA-PRUDENCE-FR-19790626"]["tier"], "A")
        self.assertEqual(sources["SRC-US-FED-PRIVATE-EQUITY-STAFF-1995"]["tier"], "B")
        for entity in ("ORG-US-WARBURG-PINCUS-1978", "ORG-US-DOL-ERISA-1979",
                       "DOC-US-DOL-ERISA-RULE-1979", "PRG-US-ERISA-PENSION-PLANS-1979"):
            self.assertIn(entity, actors)
        for relid in ("REL-US-WP-NVCA-1973-001", "REL-US-WP-DOL-CONSULTATIONS-1978-001"):
            self.assertIn(relid, focus)
        self.assertNotIn("REL-US-DOL-ERISA-FINAL-1979-001", focus)
        wp = rels["REL-US-WP-DOL-CONSULTATIONS-1978-001"]
        self.assertEqual(wp["evidence_level"], "plausible")
        self.assertEqual(wp["period"]["start"], "1978")
        self.assertIn("Firmen-Selbstaussage", wp["label"])
        self.assertNotIn("ORG-DE-MM-WARBURG", (wp["from"],wp["to"]))
        final = rels["REL-US-DOL-ERISA-FINAL-1979-001"]
        self.assertEqual(final["period"]["start"], "1979-06-26")
        self.assertEqual(final["evidence_level"], "established")
        self.assertIn("nicht als alleinigen Urheber", final["label"])
        portfolio = rels["REL-US-ERISA-RULE-PORTFOLIO-1979-001"]
        self.assertEqual(portfolio["period"]["start"], "1979-07-23")
        self.assertIn("KEINE generelle Erlaubnis", portfolio["label"])
        market = rels["REL-US-ERISA-VC-AGGREGATES-1976-1979-001"]
        self.assertEqual(market["period"], {"start": "1976", "end": "1979"})
        self.assertIn("ERSTEN HALBJAHR 1979", market["label"])
        self.assertIn("KEIN nachgewiesener individueller Geldfluss", market["label"])


    def test_nsu_judicial_oversight_preserves_attribution_and_outcome_limits(self):
        root = coverage.ROOT
        matrix = (root / "research/nsu-komplex-skandale-belegmatrix-1994-2026.md").read_text(encoding="utf-8")
        los = (root / "research/bfv-los-nsu-2011-2014.md").read_text(encoding="utf-8")
        row = next(line for line in matrix.splitlines() if line.startswith("| NSU-28 |"))
        self.assertIn("Referatsgruppenleiter D. seine Mitarbeiter", row)
        self.assertIn("Hauptbericht leitet das Zitat fehlerhaft", row)
        self.assertIn("S. 1277, Fn. 3694", row)
        self.assertIn("Eine eigene Stopp-Anweisung Lingens für den 07./08.11. ist daraus nicht ableitbar", los)
        self.assertNotIn("\n\n| NSU-46 |", matrix)
        rels = {r["id"]: r for r in yaml.safe_load(
            (root / "data/relations.yml").read_text(encoding="utf-8")
        )["relations"]}
        self.assertIn("vorläufigen Rückumsetzung", rels["REL-DE-NSU-OVG-BFV-RUECKUMSETZUNG-2013-001"]["label"])
        self.assertIn("keine Entscheidung zur materiellen Berechtigung", rels["REL-DE-NSU-VGD-BFV-DISZIPLINAR-2015-001"]["label"])
        self.assertIn("tatsächliche Vorlage offen", rels["REL-DE-NSU-BT-NRW-GERICHTSAKTEN-2016-001"]["label"])

    def test_nsu_and_amri_use_shared_modern_authority_identities(self):
        root = coverage.ROOT
        entities = {e["id"]: e for e in yaml.safe_load(
            (root / "data/entities.yml").read_text(encoding="utf-8")
        )["entities"]}
        relations = {r["id"]: r for r in yaml.safe_load(
            (root / "data/relations.yml").read_text(encoding="utf-8")
        )["relations"]}
        self.assertNotIn("period", relations["REL-DE-NSU-HH-GBA-2026-001"])
        self.assertEqual(relations["REL-DE-TH-TLFV-TLKA-PFLICHT-2012-001"]["period"],
                         {"start": "2012-08-18", "end": "2014-12-31"})
        self.assertIn("SRC-DE-TH-GVBL-THURVERFSCHG-20140808",
                      relations["REL-DE-TH-TLFV-TLKA-PFLICHT-2012-001"]["sources"])
        self.assertEqual(relations["REL-DE-TH-AFV-TLKA-PFLICHT-2014-001"]["period"]["start"],
                         "2015-01-01")
        for lka in ("ORG-DE-ST-LKA", "ORG-DE-TLKA", "ORG-DE-LKA-BERLIN", "ORG-DE-LKA-NRW"):
            self.assertEqual(entities[lka]["type"], "police_authority", lka)
        obsolete = ('ORG-DE-BERLIN-LKA', 'ORG-DE-BERLIN-LFV-2012', 'ORG-DE-GBA-NSU-2026', 'ORG-DE-GBA-NSU-1998-2012', 'ORG-DE-GBA-NSU-2014', 'ORG-DE-BMI-2003', 'ORG-DE-BMI-2011-2012')
        self.assertTrue(set(obsolete).isdisjoint(entities))
        self.assertTrue(set(obsolete).isdisjoint(
            endpoint for r in relations.values() for endpoint in (r["from"], r["to"])))
        for entity in ("ORG-DE-LKA-BERLIN", "ORG-DE-GBA", "ORG-DE-LFV-BERLIN", "ORG-DE-BMI-AMRI-2017"):
            self.assertIn(entity, entities)
            for dossier in ("REL-DE-NSU-", "REL-DE-AMRI-"):
                self.assertTrue(any(rid.startswith(dossier) and
                    entity in (r["from"], r["to"]) for rid, r in relations.items()),
                    (entity, dossier))


if __name__ == "__main__":
    unittest.main()