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
    # Not `== 1`: proof/ gains a record every phase (LWP-D0 ... LWP-D5), so
    # pinning the count makes the suite fail the moment the phase it is
    # meant to prove writes its own record. The real assertion is that every
    # record present validates and that the gate record is still among them.
    assert count >= 1
    names = {p.name for p in (REPO_ROOT / "proof").glob("*.json")}
    assert "LWP-GPUB-scan.json" in names


def test_placeholder_checked_by_is_rejected():
    """`checked_by` must name a real identity, not a promise of one.

    Found by the independent D0 check: the record was carrying
    `"checked_by": "PENDING"` and `lwp_check_proof.py` passed it, because
    the only guard was string inequality with `author`.
    """
    base = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    for placeholder in (
        "PENDING",
        "pending ",
        "TODO",
        "TBD",
        "n/a",
        "unknown",
        "[pending]",
        # Round two: the first guard was an exact-word list, and the
        # independent check walked straight past it with these.
        "AWAITING-VERIFIER",
        "PLACEHOLDER",
        "REDACTED",
        "REVIEW-PENDING",
        "TO BE DETERMINED",
        "not-yet-assigned",
        "CHECKER-TBD",
    ):
        record = dict(base, checked_by=placeholder)
        errors = lwp_check_proof._validate_record(Path("proof/fake.json"), record)
        assert any("placeholder" in e for e in errors), f"{placeholder!r} was accepted"


def test_author_and_checked_by_differing_only_by_case_or_space_is_rejected():
    base = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    record = dict(base, checked_by=f"  {str(base['author']).upper()} ")
    errors = lwp_check_proof._validate_record(Path("proof/fake.json"), record)
    assert any("self-certified" in e for e in errors)


def test_a_real_identity_is_still_accepted():
    base = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    record = dict(base, checked_by="lw-verifier (sonnet), independent check, 2026-09-17")
    errors = lwp_check_proof._validate_record(Path("proof/fake.json"), record)
    assert errors == []


def test_placeholder_guard_does_not_reject_real_identities():
    """Wrongly refusing a real identity blocks an honest record.

    Round three of the independent check found `Todor Petrov` rejected for
    containing "todo" as a substring; testing that fix turned up a worse
    one, a name in a non-Latin script rejected by an ASCII-only
    "has any letters" test.
    """
    real_identities = [
        "Todor Petrov",
        "lw-verifier (sonnet), session claude-fixme-042",
        "codex",
        "claude-opus-5 session d0-skeleton-parity",
        "lw-verifier (sonnet), independent check of LWP-D0 at commit 4738831, 2026-09-17",
        "Ana Maria Nunes",
        "J. Smith",
        "Noneste Alvarez",
        "Heldana Tesfaye",
        "小林 太郎",
        "Ольга Иванова",
    ]
    rejected = [v for v in real_identities if lwp_check_proof._is_placeholder(v)]
    assert rejected == [], f"real identities wrongly rejected: {rejected}"


def test_placeholder_guard_catches_the_open_ended_template_class():
    """An all-caps slug is a template value no word list can enumerate."""
    for value in (
        "SET-BY-INDEPENDENT-CHECK",
        "AWAITING-VERIFIER",
        "PLACEHOLDER",
        "REDACTED",
        "CHECKER-TBD",
        "unverified",
        "no verifier",
        "checker unspecified",
        "N.A.",
        "???",
        "--",
    ):
        assert lwp_check_proof._is_placeholder(value), f"{value!r} was accepted"
