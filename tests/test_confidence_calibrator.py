from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    REPO_ROOT
    / "skills"
    / "truth-first-counterargument"
    / "scripts"
    / "confidence_calibrator.py"
)
SPEC = importlib.util.spec_from_file_location("confidence_calibrator", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def item(
    evidence_id: str,
    stance: str,
    group: str,
    *,
    quality: int = 4,
    directness: int = 4,
    relevance: int = 3,
    transparency: int = 3,
    materiality: int = 3,
) -> dict:
    return {
        "id": evidence_id,
        "claim_ids": ["C1"],
        "stance": stance,
        "independence_group": group,
        "source_quality": quality,
        "directness": directness,
        "relevance": relevance,
        "transparency": transparency,
        "materiality": materiality,
        "url": f"https://example.test/{evidence_id}",
    }


class ConfidenceCalibratorTests(unittest.TestCase):
    def test_three_independent_strong_sources_allow_high_estimate(self) -> None:
        payload = {
            "evidence": [
                item("E1", "supports", "origin-a"),
                item("E2", "supports", "origin-b"),
                item("E3", "supports", "origin-c"),
                item(
                    "E4",
                    "contradicts",
                    "origin-d",
                    quality=1,
                    directness=1,
                    relevance=2,
                    transparency=1,
                    materiality=2,
                ),
            ]
        }
        result = MODULE.score_case(payload, "C1")
        self.assertGreaterEqual(result["truth_estimate_percent"], 85)
        self.assertEqual(result["research_confidence"], "high")

    def test_repeated_same_origin_cannot_create_fake_consensus(self) -> None:
        payload = {
            "evidence": [
                item("E1", "supports", "shared-wire"),
                item("E2", "supports", "shared-wire"),
                item("E3", "supports", "shared-wire"),
            ]
        }
        result = MODULE.score_case(payload, "C1")
        self.assertLessEqual(result["truth_estimate_percent"], 65)
        self.assertEqual(result["independent_directional_origins"], 1)

    def test_balanced_independent_evidence_is_unresolved(self) -> None:
        payload = {
            "evidence": [
                item("E1", "supports", "origin-a"),
                item("E2", "contradicts", "origin-b"),
            ]
        }
        result = MODULE.score_case(payload, "C1")
        self.assertEqual(result["truth_estimate_percent"], 50)
        self.assertIn("unresolved", result["evidence_band"])

    def test_same_canonical_url_is_merged_across_claimed_groups(self) -> None:
        first = item("E1", "supports", "origin-a")
        second = item("E2", "supports", "origin-b")
        first["url"] = "https://example.test/report?utm_source=social"
        second["url"] = "https://example.test/report"
        result = MODULE.score_case({"evidence": [first, second]}, "C1")
        self.assertEqual(result["independent_directional_origins"], 1)
        self.assertLessEqual(result["truth_estimate_percent"], 65)
        self.assertTrue(any("canonical URL" in warning for warning in result["warnings"]))

    def test_missing_origin_for_directional_evidence_fails_closed(self) -> None:
        missing = item("E1", "supports", "")
        with self.assertRaisesRegex(ValueError, "independence_group is required"):
            MODULE.score_case({"evidence": [missing]}, "C1")

    def test_same_origin_copies_do_not_inflate_research_confidence(self) -> None:
        copied = [item(f"E{i}", "supports", "shared-origin") for i in range(1, 6)]
        copied.extend(
            [
                item(
                    "E6",
                    "supports",
                    "weak-origin-a",
                    quality=1,
                    directness=1,
                    relevance=2,
                ),
                item(
                    "E7",
                    "contradicts",
                    "weak-origin-b",
                    quality=1,
                    directness=1,
                    relevance=2,
                ),
            ]
        )
        result = MODULE.score_case({"evidence": copied}, "C1")
        self.assertEqual(result["independent_directional_origins"], 3)
        self.assertEqual(result["high_quality_direct_origins"], 1)
        self.assertNotEqual(result["research_confidence"], "high")

    def test_no_evidence_is_not_reported_as_proof(self) -> None:
        result = MODULE.score_case({"evidence": []}, "C1")
        self.assertEqual(result["truth_estimate_percent"], 50)
        self.assertEqual(result["research_confidence"], "low")
        self.assertTrue(result["warnings"])

    def test_invalid_range_fails_closed(self) -> None:
        bad = item("E1", "supports", "origin-a")
        bad["directness"] = 9
        with self.assertRaises(ValueError):
            MODULE.score_case({"evidence": [bad]}, "C1")


if __name__ == "__main__":
    unittest.main()
