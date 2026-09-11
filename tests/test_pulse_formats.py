"""Release-contract mutations for the three approved checklist views."""
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_pulse_plugin import validate


PLUGIN = Path(__file__).resolve().parents[1] / "plugins" / "LEAPWare-Pulse"
SKILL = Path("skills/LEAPWare-Pulse/SKILL.md")
FORMATS = Path("skills/LEAPWare-Pulse/references/formats.md")


class PulseFormatContractTests(unittest.TestCase):
    def test_packages_the_three_branded_views(self):
        self.assertTrue((PLUGIN / FORMATS).is_file(), "missing checklist view reference")
        reference = (PLUGIN / FORMATS).read_text(encoding="utf-8")
        for brand in ("LEAPWare Pulse Panorama", "LEAPWare Pulse Brief", "LEAPWare Pulse Focus"):
            self.assertIn(brand, reference)

    def assert_removed_rule_rejected(self, path, rule, expected):
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "LEAPWare-Pulse"
            shutil.copytree(PLUGIN, copy)
            target = copy / path
            text = target.read_text(encoding="utf-8") if target.exists() else ""
            self.assertIn(rule, text, "mutation fixture must contain the rule it removes")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text.replace(rule, ""), encoding="utf-8")
            errors = validate(copy)
            self.assertTrue(any(expected in error for error in errors), errors)

    def test_rejects_missing_default_routing(self):
        self.assert_removed_rule_rejected(SKILL,
            "Without an explicit view or a recorded owner preference, use Panorama.",
            "default view rule")

    def test_rejects_missing_explicit_routing(self):
        for mode in ("panorama", "brief", "focus"):
            with self.subTest(mode=mode):
                self.assert_removed_rule_rejected(SKILL, f"`lw-pulse {mode}`", "view routing")

    def test_rejects_missing_panorama_contract(self):
        self.assert_removed_rule_rejected(FORMATS,
            "Show all milestones in execution order, with every required criterion as a nested checkbox.",
            "Panorama layout")

    def test_rejects_missing_brief_contract(self):
        self.assert_removed_rule_rejected(FORMATS,
            "Show one flat checkbox per required criterion in execution order, labelled with its milestone and stable criterion identity.",
            "Brief layout")

    def test_rejects_missing_focus_contract(self):
        self.assert_removed_rule_rejected(FORMATS,
            "Group criteria under Active, Next, Blocked, Unverified, Remaining, Complete, Deferred and Cancelled, in that order; omit empty groups.",
            "Focus layout")

    def test_rejects_missing_evidence_gate(self):
        self.assert_removed_rule_rejected(SKILL,
            "A checked task row, a teammate claim or a passing unrelated test is not completion evidence.",
            "completion evidence rule")

    def test_rejects_missing_main_clean_rule(self):
        self.assert_removed_rule_rejected(SKILL,
            "Claim main is clean only after checking main's worktree for staged, unstaged and untracked changes; a clean feature worktree does not prove this.",
            "main cleanliness rule")

    def test_rejects_missing_counting_boundary(self):
        self.assert_removed_rule_rejected(FORMATS,
            "Compute the plan-wide count from unique required criteria, never from milestone rows or state-group totals.",
            "view counting rule")


if __name__ == "__main__":
    unittest.main()
