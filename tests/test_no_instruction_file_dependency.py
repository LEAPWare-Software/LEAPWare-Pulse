"""LWP-R4: the plugin must not depend on CLAUDE.md or AGENTS.md.

A static scan (`scripts/lwp_check_no_instruction_dep.py`, also run in CI as
its own job) finds no reference to either filename in runtime code under
`plugins/`, `core/`, or `adapters/`.

LWP-D0 note: this repo's shipped tree today is `plugins/LEAPWare-Pulse/`;
`core/` and `adapters/` do not exist until D1. The script (and this test)
must pass cleanly with those roots absent.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "scripts"))
lwp_check_no_instruction_dep = importlib.import_module("lwp_check_no_instruction_dep")


def test_scan_finds_no_reference_in_this_checkout():
    assert lwp_check_no_instruction_dep.find_violations() == []


def test_scan_passes_when_a_scan_root_is_absent(tmp_path):
    # core/ and adapters/ do not exist in this repo until D1; the scan must
    # not error or fail just because a root is missing -- it must skip it.
    (tmp_path / "plugins").mkdir()
    original_root = lwp_check_no_instruction_dep.REPO_ROOT
    try:
        lwp_check_no_instruction_dep.REPO_ROOT = tmp_path
        violations = lwp_check_no_instruction_dep.find_violations()
    finally:
        lwp_check_no_instruction_dep.REPO_ROOT = original_root
    assert violations == []


def test_scan_catches_a_planted_reference(tmp_path):
    scan_root = tmp_path / "plugins"
    scan_root.mkdir()
    planted = scan_root / "leaky.py"
    planted.write_text('"""Reads CLAUDE.md for policy."""\n', encoding="utf-8")

    original_dirs = lwp_check_no_instruction_dep.SCAN_DIRS
    original_root = lwp_check_no_instruction_dep.REPO_ROOT
    try:
        lwp_check_no_instruction_dep.REPO_ROOT = tmp_path
        lwp_check_no_instruction_dep.SCAN_DIRS = ("plugins",)
        violations = lwp_check_no_instruction_dep.find_violations()
    finally:
        lwp_check_no_instruction_dep.REPO_ROOT = original_root
        lwp_check_no_instruction_dep.SCAN_DIRS = original_dirs

    assert any("CLAUDE.md" in v for v in violations)


def test_scan_catches_a_planted_reference_to_agents_md(tmp_path):
    scan_root = tmp_path / "core"
    scan_root.mkdir()
    planted = scan_root / "leaky.py"
    planted.write_text('open("AGENTS.md")\n', encoding="utf-8")

    original_dirs = lwp_check_no_instruction_dep.SCAN_DIRS
    original_root = lwp_check_no_instruction_dep.REPO_ROOT
    try:
        lwp_check_no_instruction_dep.REPO_ROOT = tmp_path
        lwp_check_no_instruction_dep.SCAN_DIRS = ("core",)
        violations = lwp_check_no_instruction_dep.find_violations()
    finally:
        lwp_check_no_instruction_dep.REPO_ROOT = original_root
        lwp_check_no_instruction_dep.SCAN_DIRS = original_dirs

    assert any("AGENTS.md" in v for v in violations)
