#!/usr/bin/env python3

import subprocess
import sys
from dataclasses import dataclass
from typing import Dict, List, Iterable, Tuple
from collections import defaultdict


class GitError(Exception):
    pass


@dataclass(frozen=True)
class Commit:
    sha: str
    subject: str


def run_git(args: List[str]) -> str:
    """Ejecuta un comando git y devuelve stdout."""
    try:
        result = subprocess.run(
            ["git"] + args,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise GitError(e.stderr.strip()) from e


def iter_commits(rev: str = "HEAD") -> Iterable[Commit]:
    """
    Itera commits devolviendo SHA y subject.
    """
    fmt = "%H%x00%s"
    out = run_git(["log", "--no-merges", f"--format={fmt}", rev])

    for line in out.splitlines():
        sha, subject = line.split("\x00", 1)
        yield Commit(sha=sha, subject=subject)


def patch_id(sha: str) -> str:
    """
    Calcula el patch-id de un commit.
    """
    show = run_git(["show", sha])
    pid = run_git(["patch-id", "--stable"],).strip()

    # git patch-id espera el diff por stdin,
    # así que usamos subprocess directamente
    p1 = subprocess.Popen(
        ["git", "show", sha],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    p2 = subprocess.Popen(
        ["git", "patch-id", "--stable"],
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    out, err = p2.communicate()
    if p2.returncode != 0:
        raise GitError(err.strip())

    return out.split()[0]


def find_duplicates(commits: Iterable[Commit]) -> Dict[str, List[Commit]]:
    """
    Agrupa commits por patch-id.
    """
    groups: Dict[str, List[Commit]] = defaultdict(list)

    for c in commits:
        try:
            pid = patch_id(c.sha)
            groups[pid].append(c)
        except GitError as e:
            print(f"Error en {c.sha[:7]}: {e}", file=sys.stderr)

    return {pid: cs for pid, cs in groups.items() if len(cs) > 1}


def print_report(dups: Dict[str, List[Commit]]) -> None:
    if not dups:
        print("No se encontraron commits duplicados.")
        return

    print("Commits con el mismo patch-id:\n")
    for pid, commits in dups.items():
        print(f"Patch-ID: {pid}")
        for c in commits:
            print(f"  {c.sha[:7]}  {c.subject}")
        print()


def main() -> None:
    try:
        commits = list(iter_commits())
        dups = find_duplicates(commits)
        print_report(dups)
    except GitError as e:
        print(f"Git error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
