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
        "unverified",
        "no verifier",
        "checker unspecified",
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


def test_placeholder_guard_catches_values_with_no_identity_in_them():
    for value in ("N.A.", "???", "--", "   "):
        assert lwp_check_proof._is_placeholder(value), f"{value!r} was accepted"


def test_an_arbitrary_slug_is_not_caught_and_that_is_the_documented_contract():
    """`SET-BY-INDEPENDENT-CHECK` carries no marker word, so the word list
    does not catch it -- and the rule that used to, by shape, rejected
    DEPENDABOT and MACDONALD along with it.

    This is not a gap being papered over: a draft record omits
    `checked_by` entirely rather than filling it with a slug, and the
    required-field check refuses that with no guessing at all. Asserted
    here so the contract is explicit rather than assumed.
    """
    assert not lwp_check_proof._is_placeholder("SET-BY-INDEPENDENT-CHECK")

    record = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    record.pop("checked_by")
    assert any(
        "missing required field 'checked_by'" in e
        for e in lwp_check_proof._validate_record(Path("proof/fake.json"), record)
    )


def test_placeholder_guard_accepts_bot_names_and_all_caps_surnames():
    """No 'looks like a template slug' rule, deliberately.

    Round four of the independent check: an all-caps-slug rule rejected
    DEPENDABOT, GITHUB-ACTIONS-BOT, CODEQL, the surnames MACDONALD and
    OBRIEN, and KIM-MINJI. Bot accounts and real names are exactly what a
    checked_by field holds.
    """
    for value in (
        "DEPENDABOT",
        "GITHUB-ACTIONS-BOT",
        "CODEQL",
        "MACDONALD",
        "OBRIEN",
        "KIM-MINJI",
        "CLAUDE-OPUS-5",
        "SESSION-4F3C-2026",
        "AI",
        "OK",
    ):
        assert not lwp_check_proof._is_placeholder(value), f"{value!r} wrongly rejected"


def test_an_omitted_checked_by_is_the_structural_guard():
    """The guard that cannot be fooled by phrasing: leave the field out.

    A draft proof record omits `checked_by` entirely, so it fails the
    required-field check until a real identity is written in. The
    placeholder word list is a convenience net under this, not the
    mechanism itself.
    """
    record = json.loads((FIXTURES / "valid.json").read_text(encoding="utf-8"))
    record.pop("checked_by")
    errors = lwp_check_proof._validate_record(Path("proof/fake.json"), record)
    assert any("missing required field 'checked_by'" in e for e in errors)
