"""Shape checks for .github/rulesets/*.json (LWP-R5).

Not a call to GitHub -- these are the properties lwp_apply_rulesets.py and
the GitHub rulesets API both depend on, checked without any network access
so a malformed ruleset fails fast in `pytest`, not at apply time.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RULESETS_DIR = REPO_ROOT / ".github" / "rulesets"
CI_YML = REPO_ROOT / ".github" / "workflows" / "ci.yml"

REQUIRED_TOP_LEVEL_KEYS = {"name", "target", "enforcement", "bypass_actors", "conditions", "rules"}


def _ruleset_paths() -> list[Path]:
    return sorted(RULESETS_DIR.glob("*.json"))


def _main_ruleset() -> dict:
    return json.loads((RULESETS_DIR / "main.json").read_text(encoding="utf-8"))


def _ci_job_names() -> set[str]:
    """The exact job names ci.yml's `test` job produces, e.g.
    "test (windows-latest, 3.10)" -- must match what GitHub reports as the
    status check context for each matrix leg.
    """
    text = CI_YML.read_text(encoding="utf-8")
    match = re.search(r"^  test:\n(.*?)(?=^  [A-Za-z_-]+:\n|\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, f"no 'test:' job found in {CI_YML}"
    job_text = match.group(1)

    def matrix_list(key: str) -> list[str]:
        m = re.search(rf"^\s*{re.escape(key)}:\s*\[([^\]]*)\]", job_text, re.MULTILINE)
        assert m, f"no '{key}:' matrix list found in the test job"
        return [item.strip().strip('"').strip("'") for item in m.group(1).split(",") if item.strip()]

    os_list = matrix_list("os")
    python_versions = matrix_list("python-version")
    return {f"test ({os}, {version})" for os in os_list for version in python_versions}


def test_at_least_one_ruleset_exists():
    assert _ruleset_paths(), f"no *.json files under {RULESETS_DIR}"


def test_each_ruleset_has_required_top_level_keys():
    for path in _ruleset_paths():
        data = json.loads(path.read_text(encoding="utf-8"))
        missing = REQUIRED_TOP_LEVEL_KEYS - data.keys()
        assert not missing, f"{path.name} missing top-level keys: {missing}"


def test_each_ruleset_is_active_with_empty_bypass_actors():
    for path in _ruleset_paths():
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["enforcement"] == "active", f"{path.name}: enforcement must be 'active'"
        assert data["bypass_actors"] == [], f"{path.name}: bypass_actors must be empty (no bypass actors)"


def test_each_ruleset_targets_the_default_branch():
    for path in _ruleset_paths():
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["target"] == "branch", f"{path.name}: target must be 'branch'"
        include = data["conditions"]["ref_name"]["include"]
        assert "~DEFAULT_BRANCH" in include, f"{path.name}: must target ~DEFAULT_BRANCH"


def test_each_ruleset_has_unique_rule_types():
    for path in _ruleset_paths():
        data = json.loads(path.read_text(encoding="utf-8"))
        rules = data["rules"]
        assert isinstance(rules, list) and rules, f"{path.name}: rules must be a non-empty list"
        types = [rule["type"] for rule in rules]
        assert len(types) == len(set(types)), f"{path.name}: duplicate rule types: {types}"


def test_main_ruleset_blocks_deletion_and_non_fast_forward():
    data = _main_ruleset()
    types = {rule["type"] for rule in data["rules"]}
    assert "deletion" in types, "main.json must block branch deletion"
    assert "non_fast_forward" in types, "main.json must block non-fast-forward pushes"


def test_pull_request_rule_requires_squash_only_when_present():
    for path in _ruleset_paths():
        data = json.loads(path.read_text(encoding="utf-8"))
        for rule in data["rules"]:
            if rule["type"] != "pull_request":
                continue
            params = rule["parameters"]
            assert params["allowed_merge_methods"] == ["squash"], (
                f"{path.name}: pull_request rule must allow only squash merges"
            )


def test_merge_queue_rule_uses_squash_and_allgreen_when_present():
    for path in _ruleset_paths():
        data = json.loads(path.read_text(encoding="utf-8"))
        for rule in data["rules"]:
            if rule["type"] != "merge_queue":
                continue
            params = rule["parameters"]
            assert params["merge_method"] == "SQUASH", f"{path.name}: merge_queue must use SQUASH"
            assert params["grouping_strategy"] == "ALLGREEN", (
                f"{path.name}: merge_queue must use ALLGREEN grouping"
            )
            for key in (
                "min_entries_to_merge",
                "max_entries_to_merge",
                "max_entries_to_build",
                "check_response_timeout_minutes",
            ):
                assert key in params, f"{path.name}: merge_queue missing '{key}'"


def test_required_status_checks_rule_lists_nonempty_contexts_when_present():
    for path in _ruleset_paths():
        data = json.loads(path.read_text(encoding="utf-8"))
        for rule in data["rules"]:
            if rule["type"] != "required_status_checks":
                continue
            params = rule["parameters"]
            assert params["strict_required_status_checks_policy"] is True
            checks = params["required_status_checks"]
            assert checks, f"{path.name}: required_status_checks list is empty"
            for check in checks:
                assert check.get("context"), f"{path.name}: a status check is missing 'context'"


def test_main_ruleset_required_status_checks_equal_ci_job_names():
    """LWP-R5: the ruleset must require EXACTLY the CI job names ci.yml
    produces -- not a subset, not a superset, and not stale names left
    over from renaming a matrix leg.
    """
    data = _main_ruleset()
    required_rule = next(rule for rule in data["rules"] if rule["type"] == "required_status_checks")
    required_contexts = {check["context"] for check in required_rule["parameters"]["required_status_checks"]}
    assert required_contexts == _ci_job_names(), (
        f"ruleset required checks {required_contexts} != ci.yml job names {_ci_job_names()}"
    )


def test_main_ruleset_has_no_bypass_actors():
    data = _main_ruleset()
    assert data["bypass_actors"] == []
