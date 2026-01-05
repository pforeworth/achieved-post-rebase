import hashlib
from pathlib import Path
from collections import defaultdict
from typing import Dict, List


def file_hash(path: Path, block_size: int = 8192) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()


def find_duplicates(root: Path) -> Dict[str, List[Path]]:
    groups: Dict[str, List[Path]] = defaultdict(list)

    for p in root.rglob("*"):
        if p.is_file():
            try:
                groups[file_hash(p)].append(p)
            except OSError:
                pass  # archivo no legible

    return {h: files for h, files in groups.items() if len(files) > 1}


def main() -> None:
    root = Path(".")
    dups = find_duplicates(root)

    if not dups:
        print("No hay archivos duplicados.")
        return

    print("Archivos duplicados:\n")
    for h, files in dups.items():
        print(f"Hash: {h[:12]}...")
        for f in files:
            print(f"  {f}")
        print()


if __name__ == "__main__":
    main()
