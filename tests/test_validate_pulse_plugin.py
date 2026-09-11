import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_pulse_plugin import validate


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIRECTORY = REPOSITORY_ROOT / "plugins" / "LEAPWare-Pulse"


class ValidateStatusPluginTests(unittest.TestCase):
    def assertMutationIsRejected(self, mutate, expected_error):
        with tempfile.TemporaryDirectory() as temporary_directory:
            plugin_directory = Path(temporary_directory) / "LEAPWare-Pulse"
            shutil.copytree(PLUGIN_DIRECTORY, plugin_directory)
            mutate(plugin_directory)
            try:
                errors = validate(plugin_directory)
            except Exception as error:
                self.fail(f"validator raised {error!r}")
            self.assertTrue(
                any(expected_error in error for error in errors),
                expected_error,
            )

    def test_accepts_the_real_plugin_package(self):
        self.assertEqual([], validate(PLUGIN_DIRECTORY))

    def test_rejects_a_wrong_manifest_name(self):
        def mutate(plugin_directory):
            manifest_path = plugin_directory / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["name"] = "wrong-name"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        self.assertMutationIsRejected(mutate, "manifest name")

    def test_rejects_an_empty_manifest_object(self):
        def mutate(plugin_directory):
            manifest_path = plugin_directory / ".codex-plugin" / "plugin.json"
            manifest_path.write_text("{}", encoding="utf-8")

        self.assertMutationIsRejected(mutate, "manifest name")

    def test_rejects_a_zero_byte_manifest(self):
        def mutate(plugin_directory):
            manifest_path = plugin_directory / ".codex-plugin" / "plugin.json"
            manifest_path.write_text("", encoding="utf-8")

        self.assertMutationIsRejected(mutate, "valid JSON")

    def test_rejects_a_manifest_without_a_version(self):
        def mutate(plugin_directory):
            manifest_path = plugin_directory / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            del manifest["version"]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        self.assertMutationIsRejected(mutate, "manifest version")

    def test_rejects_a_non_object_manifest(self):
        def mutate(plugin_directory):
            manifest_path = plugin_directory / ".codex-plugin" / "plugin.json"
            manifest_path.write_text("[]", encoding="utf-8")

        self.assertMutationIsRejected(mutate, "JSON object")

    def test_rejects_an_undeclared_top_level_capability(self):
        def mutate(plugin_directory):
            (plugin_directory / "hooks").mkdir()

        self.assertMutationIsRejected(mutate, "package inventory")

    def test_rejects_inline_mcp_servers(self):
        def mutate(plugin_directory):
            manifest_path = plugin_directory / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["mcpServers"] = {"server": {"command": "python"}}
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        self.assertMutationIsRejected(mutate, "mcpServers")

    def test_rejects_inline_apps(self):
        def mutate(plugin_directory):
            manifest_path = plugin_directory / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["apps"] = {"app": {"id": "example"}}
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        self.assertMutationIsRejected(mutate, "apps")

    def test_rejects_a_missing_full_plan_rule(self):
        def mutate(plugin_directory):
            skill_path = plugin_directory / "skills" / "LEAPWare-Pulse" / "SKILL.md"
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8").replace(
                    "Keep all agreed milestones visible; preserve stable names and criteria across updates.",
                    "Keep milestones concise.",
                ),
                encoding="utf-8",
            )

        self.assertMutationIsRejected(mutate, "full-plan")

    def test_rejects_a_missing_unknown_denominator_rule(self):
        def mutate(plugin_directory):
            skill_path = plugin_directory / "skills" / "LEAPWare-Pulse" / "SKILL.md"
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8").replace(
                    "If the checklist or denominator is incomplete, label the task **Not yet measurable** and omit its numerical bar; still show known subtasks and what is missing.",
                    "Use the available criteria.",
                ),
                encoding="utf-8",
            )

        self.assertMutationIsRejected(mutate, "unknown denominator")

    def test_rejects_an_incorrect_percentage_floor_rule(self):
        def mutate(plugin_directory):
            skill_path = plugin_directory / "skills" / "LEAPWare-Pulse" / "SKILL.md"
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8").replace(
                    "calculate `floor(100 * verified / total)`",
                    "calculate `round(100 * verified / total)`",
                ),
                encoding="utf-8",
            )

        self.assertMutationIsRejected(mutate, "percentage floor")

    def test_rejects_a_missing_unchecked_criteria_rule(self):
        def mutate(plugin_directory):
            skill_path = plugin_directory / "skills" / "LEAPWare-Pulse" / "SKILL.md"
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8").replace(
                    "A failed attempt leaves its outcome unchecked. Partial completion stays unchecked; state the completed portion briefly if useful.",
                    "A failed attempt should be recorded.",
                ),
                encoding="utf-8",
            )

        self.assertMutationIsRejected(mutate, "unchecked criteria")

    def test_rejects_a_missing_optional_work_total_rule(self):
        def mutate(plugin_directory):
            skill_path = plugin_directory / "skills" / "LEAPWare-Pulse" / "SKILL.md"
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8").replace(
                    "Keep optional, unapproved work outside committed totals.",
                    "Keep optional work visible.",
                ),
                encoding="utf-8",
            )

        self.assertMutationIsRejected(mutate, "optional work totals")

    def test_rejects_a_missing_authority_boundary(self):
        def mutate(plugin_directory):
            skill_path = plugin_directory / "skills" / "LEAPWare-Pulse" / "SKILL.md"
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8").replace(
                    "A status request does not authorize external messages, deployments, new scope or background monitoring.",
                    "A status request reports current work.",
                ),
                encoding="utf-8",
            )

        self.assertMutationIsRejected(mutate, "authority boundary")

    def test_rejects_a_missing_default_skill_prompt(self):
        def mutate(plugin_directory):
            metadata_path = plugin_directory / "skills" / "LEAPWare-Pulse" / "agents" / "openai.yaml"
            metadata_path.write_text(
                metadata_path.read_text(encoding="utf-8").replace(
                    "$LEAPWare-Pulse",
                    "LEAPWare-Pulse",
                ),
                encoding="utf-8",
            )

        self.assertMutationIsRejected(mutate, "$LEAPWare-Pulse")
