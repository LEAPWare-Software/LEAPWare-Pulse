#!/usr/bin/env python3
"""lwp-worktrees: enforce LWP-R9 (worktree location).

Rule (LWP-R9): every linked worktree of the repository is under
``<repo>/.worktrees/<branch>``; ``.gitignore`` contains ``.worktrees/``; no
sibling folder next to the repository is a worktree of it or a clone of the
same ``origin``; ``AGENTS.md`` and ``CLAUDE.md`` both state the rule.

Checks performed, all against ``--repo`` (default: the current directory's
repository):

1. ``git worktree list --porcelain`` -- every entry after the first (the
   main worktree) must resolve to a path under ``<toplevel>/.worktrees/``.
2. The immediate siblings of ``<toplevel>`` (nothing deeper) are scanned for:
   - a ``.git`` file (a linked worktree's gitdir pointer) that points back
     into this repository's ``.git/worktrees/``;
   - a ``.git`` directory (an ordinary clone) whose ``remote.origin.url``
     matches this repository's own.
3. ``.gitignore`` at the toplevel contains a ``.worktrees/`` entry.
4. ``AGENTS.md`` and ``CLAUDE.md`` at the toplevel both state the rule.

Standard library only. Exits 0 and prints ``lwp-worktrees check passed`` when
every check passes; otherwise exits 1 and names every offending path.
"""

from __future__ import annotations

import argparse
import configparser
import os
import subprocess
import sys
from pathlib import Path


def _run_git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _norm(path: Path) -> str:
    """Normalize a path for cross-platform comparison."""
    return os.path.normcase(os.path.normpath(str(path.resolve())))


def _toplevel(repo: Path) -> Path | None:
    result = _run_git(repo, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def _origin_url(repo: Path) -> str | None:
    result = _run_git(repo, "config", "--get", "remote.origin.url")
    if result.returncode != 0:
        return None
    url = result.stdout.strip()
    return url or None


def _parse_worktree_list(porcelain: str) -> list[Path]:
    """Return the ``worktree`` path of every block, in order."""
    paths: list[Path] = []
    for block in porcelain.split("\n\n"):
        for line in block.splitlines():
            if line.startswith("worktree "):
                paths.append(Path(line[len("worktree ") :]))
                break
    return paths


def check_worktree_locations(repo: Path, toplevel: Path, errors: list[str]) -> None:
    result = _run_git(repo, "worktree", "list", "--porcelain")
    if result.returncode != 0:
        errors.append(f"'git worktree list --porcelain' failed: {result.stderr.strip()}")
        return

    worktrees = _parse_worktree_list(result.stdout)
    if not worktrees:
        errors.append("'git worktree list --porcelain' returned no worktrees")
        return

    # The first entry is always the main worktree; everything after it is linked.
    allowed_root = _norm(toplevel / ".worktrees")
    for linked in worktrees[1:]:
        normed = _norm(linked)
        if normed != allowed_root and not normed.startswith(allowed_root + os.sep):
            errors.append(
                f"linked worktree outside <toplevel>/.worktrees/: {linked}"
            )


def check_siblings(repo: Path, toplevel: Path, errors: list[str]) -> None:
    parent = toplevel.parent
    if not parent.is_dir():
        return

    repo_git_worktrees = _norm(toplevel / ".git" / "worktrees")
    origin_url = _origin_url(repo)

    for sibling in sorted(parent.iterdir()):
        if _norm(sibling) == _norm(toplevel):
            continue
        if not sibling.is_dir():
            continue

        sibling_git = sibling / ".git"
        if sibling_git.is_file():
            try:
                content = sibling_git.read_text(encoding="utf-8").strip()
            except OSError:
                continue
            if content.startswith("gitdir:"):
                gitdir = content[len("gitdir:") :].strip()
                gitdir_path = Path(gitdir)
                if not gitdir_path.is_absolute():
                    gitdir_path = sibling / gitdir_path
                normed_gitdir = _norm(gitdir_path)
                if normed_gitdir == repo_git_worktrees or normed_gitdir.startswith(
                    repo_git_worktrees + os.sep
                ):
                    errors.append(
                        f"sibling folder is a linked worktree of this repository: {sibling}"
                    )
        elif sibling_git.is_dir():
            sibling_config = sibling_git / "config"
            if not sibling_config.is_file() or origin_url is None:
                continue
            parser = configparser.ConfigParser()
            try:
                parser.read(sibling_config, encoding="utf-8")
            except configparser.Error:
                continue
            section = None
            for name in parser.sections():
                if name == '"origin"' or name.strip().startswith('remote "origin"'):
                    section = name
                    break
                if name.startswith("remote ") and "origin" in name:
                    section = name
                    break
            if section is not None and parser.has_option(section, "url"):
                sibling_url = parser.get(section, "url").strip()
                if sibling_url and sibling_url == origin_url:
                    errors.append(
                        f"sibling folder is a clone of the same origin: {sibling}"
                    )


def check_gitignore(toplevel: Path, errors: list[str]) -> None:
    gitignore = toplevel / ".gitignore"
    if not gitignore.is_file():
        errors.append(".gitignore is missing")
        return
    content = gitignore.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines()]
    if ".worktrees/" not in lines and ".worktrees" not in lines:
        errors.append(".gitignore does not contain .worktrees/")


def _states_rule(text: str) -> bool:
    lowered = text.lower()
    return ".worktrees/" in lowered and "sibling" in lowered


def check_instruction_files(toplevel: Path, errors: list[str]) -> None:
    for name in ("AGENTS.md", "CLAUDE.md"):
        path = toplevel / name
        if not path.is_file():
            errors.append(f"{name} is missing")
            continue
        content = path.read_text(encoding="utf-8")
        if not _states_rule(content):
            errors.append(f"{name} does not state the worktree-location rule")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Enforce LWP-R9 worktree location.")
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to the repository to check (default: current directory).",
    )
    args = parser.parse_args(argv)

    repo = Path(args.repo)
    toplevel = _toplevel(repo)
    if toplevel is None:
        print(f"lwp-worktrees: '{repo}' is not a git repository", file=sys.stderr)
        return 1

    errors: list[str] = []
    check_worktree_locations(repo, toplevel, errors)
    check_siblings(repo, toplevel, errors)
    check_gitignore(toplevel, errors)
    check_instruction_files(toplevel, errors)

    if errors:
        print("lwp-worktrees check failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("lwp-worktrees check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
