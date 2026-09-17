"""Tests for scripts/lwp_check_proof.py against tests/fixtures/proof/.

These fixtures live under tests/fixtures/proof/, never under the real
proof/ directory -- proof/ is proof of a real deliverable, not test data.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import lwp_check_proof  # noqa: E402

FIXTURES = REPO_ROOT / "tests" / "fixtures" / "proof"


def _load(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_valid_record_has_no_errors():
    errors = lwp_check_proof._validate_record(FIXTURES / "valid.json", _load("valid.json"))
    assert errors == []


def test_self_certified_record_is_rejected():
    errors = lwp_check_proof._validate_record(FIXTURES / "self_certified.json", _load("self_certified.json"))
    assert any("self-certified" in e for e in errors)


def test_exit_mismatch_record_is_rejected():
    errors = lwp_check_proof._validate_record(FIXTURES / "exit_mismatch.json", _load("exit_mismatch.json"))
    assert any("expect_exit" in e for e in errors)


def test_missing_field_record_is_rejected():
    errors = lwp_check_proof._validate_record(FIXTURES / "missing_field.json", _load("missing_field.json"))
    assert any("unproven" in e for e in errors)


def test_gate_record_valid_has_no_errors(tmp_path):
    gate = {
        "gate": "G-PUB",
        "item": "pre-publication history scan",
        "date": "2026-09-17",
        "verifier": "independent verifier run",
        "checks": [{"id": "no-copied-blocks", "result": "pass", "detail": "clean"}],
        "verdict": "publishable",
    }
    errors = lwp_check_proof._validate_record(tmp_path / "LWP-GATE-x.json", gate)
    assert errors == []


def test_gate_record_publishable_with_a_failing_check_is_rejected(tmp_path):
    gate = {
        "gate": "G-PUB",
        "item": "pre-publication history scan",
        "date": "2026-09-17",
        "verifier": "independent verifier run",
        "checks": [{"id": "no-copied-blocks", "result": "fail", "detail": "found a copied block"}],
        "verdict": "publishable",
    }
    errors = lwp_check_proof._validate_record(tmp_path / "LWP-GATE-y.json", gate)
    assert any("cannot be publishable" in e for e in errors)


def test_record_matching_neither_schema_is_reported_not_skipped(tmp_path):
    errors = lwp_check_proof._validate_record(tmp_path / "mystery.json", {"nothing": "recognizable"})
    assert any("matches neither" in e for e in errors)


def test_real_proof_directory_validates_clean():
    """The real proof/ directory holds proof/LWP-GPUB-scan.json, a gate
    record (fields: gate, item, date, verifier, checks, verdict), plus the
    two schema files (schema.json for phase records, gate-schema.json for
    gate records) and README.md. Routing by record shape (see this
    script's module docstring) finds the gate record valid against
    proof/gate-schema.json; schema.json and gate-schema.json are excluded
    from scanning as records, not validated as records themselves.
    """
    errors, count = lwp_check_proof.validate_all()
    assert errors == []
    assert count == 1
