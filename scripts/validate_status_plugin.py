"""Validate the source-only LEAPWare-status plugin package."""

import argparse
import json
from pathlib import Path


EXPECTED_PATHS = {
    ".codex-plugin",
    ".codex-plugin/plugin.json",
    "skills",
    "skills/LEAPWare-status",
    "skills/LEAPWare-status/SKILL.md",
    "skills/LEAPWare-status/agents",
    "skills/LEAPWare-status/agents/openai.yaml",
}


def _plugin_directory(path):
    if (path / ".codex-plugin").is_dir():
        return path
    return path / "plugins" / "LEAPWare-status"


def _read_text(path, errors, description):
    if not path.is_file():
        errors.append(f"missing {description}: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def validate(plugin_dir):
    """Return one error for each LEAPWare-status acceptance invariant violated."""
    errors = []
    plugin_path = _plugin_directory(Path(plugin_dir))

    if not plugin_path.is_dir():
        return [f"plugin directory does not exist: {plugin_path}"]

    actual_paths = {
        path.relative_to(plugin_path).as_posix()
        for path in plugin_path.rglob("*")
    }
    if actual_paths != EXPECTED_PATHS:
        errors.append("package inventory must contain only the declared source files")

    manifest_path = plugin_path / ".codex-plugin" / "plugin.json"
    manifest_text = _read_text(manifest_path, errors, "plugin manifest")
    manifest = None
    if manifest_text:
        try:
            parsed_manifest = json.loads(manifest_text)
        except json.JSONDecodeError:
            errors.append("plugin manifest must contain valid JSON")
        else:
            if not isinstance(parsed_manifest, dict):
                errors.append("plugin manifest must be a JSON object")
            else:
                manifest = parsed_manifest

    if manifest is not None:
        if manifest.get("name") != "LEAPWare-status":
            errors.append("manifest name must be LEAPWare-status")
        author = manifest.get("author")
        if not isinstance(author, dict) or author.get("name") != "LEAPWare":
            errors.append("manifest author must be LEAPWare")
        if manifest.get("skills") != "./skills/":
            errors.append("manifest skills path must be ./skills/")
        interface = manifest.get("interface")
        if not isinstance(interface, dict):
            interface = {}
        if interface.get("displayName") != "LEAPWare status":
            errors.append("manifest display name must be LEAPWare status")
        if interface.get("capabilities") != []:
            errors.append("manifest capabilities must be empty")
        if interface.get("defaultPrompt") != (
            "lw-status: show the full plan, completed work and what remains."
        ):
            errors.append("manifest default prompt must preserve lw-status")

    skill_path = plugin_path / "skills" / "LEAPWare-status" / "SKILL.md"
    skill = _read_text(skill_path, errors, "status skill")
    required_skill_rules = {
        "full-plan rule": (
            "Keep all agreed milestones visible; preserve stable names and criteria across updates.",
        ),
        "unknown denominator rule": (
            "If the checklist or denominator is incomplete, label the task **Not yet measurable** "
            "and omit its numerical bar; still show known subtasks and what is missing.",
        ),
        "percentage floor rule": ("calculate `floor(100 * verified / total)`",),
        "progress-bar floor rule": ("floor(10 * verified / total)",),
        "unchecked criteria rule": (
            "A task reaches 100% and a checked parent box only when every required criterion is verified.",
            "A failed attempt leaves its outcome unchecked. Partial completion stays unchecked; "
            "state the completed portion briefly if useful.",
            "- `[ ]` **Blocked:** identify the missing prerequisite and how it can be resolved.",
            "- `[ ]` **Unverified:** reported or attempted work whose outcome is not established.",
        ),
        "optional work totals rule": (
            "Keep optional, unapproved work outside committed totals.",
        ),
        "authority boundary": (
            "A status request does not authorize external messages, deployments, new scope or "
            "background monitoring.",
        ),
    }
    for rule_name, required_texts in required_skill_rules.items():
        if not all(required_text in skill for required_text in required_texts):
            errors.append(f"missing {rule_name}")

    metadata_path = plugin_path / "skills" / "LEAPWare-status" / "agents" / "openai.yaml"
    metadata = _read_text(metadata_path, errors, "skill metadata")
    required_metadata = {
        "metadata display name": 'display_name: "LEAPWare status"',
        "metadata short description": 'short_description: "Full-plan progress in a concise checklist"',
        "$LEAPWare-status default prompt": (
            'default_prompt: "Use $LEAPWare-status to show the full plan, what is done and what remains."'
        ),
    }
    for rule_name, required_text in required_metadata.items():
        if required_text not in metadata:
            errors.append(f"missing {rule_name}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate LEAPWare-status source files.")
    parser.add_argument(
        "path",
        nargs="?",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="repository root or explicit LEAPWare-status plugin directory",
    )
    arguments = parser.parse_args()
    errors = validate(arguments.path)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("LEAPWare-status validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
