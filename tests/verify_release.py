from __future__ import annotations

import sys
import zipfile
from pathlib import Path, PurePosixPath


REPO_ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = REPO_ROOT / "dist" / "truth-first-counterargument.zip"
ROOT = PurePosixPath("truth-first-counterargument")
ALLOWED = {"SKILL.md", "LICENSE.txt", "agents", "references", "scripts", "assets"}
REQUIRED = {
    ROOT / "SKILL.md",
    ROOT / "LICENSE.txt",
    ROOT / "agents" / "openai.yaml",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    try:
        if not ARCHIVE.is_file():
            fail(f"Release archive is missing: {ARCHIVE}")
        with zipfile.ZipFile(ARCHIVE) as archive:
            names = [PurePosixPath(name.replace("\\", "/")) for name in archive.namelist()]
            file_names = {name for name, info in zip(names, archive.infolist()) if not info.is_dir()}
            for name in names:
                if name.is_absolute() or ".." in name.parts:
                    fail(f"Unsafe archive path: {name}")
                if not name.parts or name.parts[0] != str(ROOT):
                    fail(f"Archive entry is outside the skill root: {name}")
                if len(name.parts) > 1 and name.parts[1] not in ALLOWED:
                    fail(f"Unexpected top-level skill entry: {name}")
                if "__pycache__" in name.parts or name.suffix.lower() in {".pyc", ".pyo"}:
                    fail(f"Generated Python artifact in release: {name}")
            missing = REQUIRED - file_names
            if missing:
                fail("Required release entries missing: " + ", ".join(map(str, sorted(missing))))
            bad_zip_entry = archive.testzip()
            if bad_zip_entry:
                fail(f"Corrupt ZIP member: {bad_zip_entry}")
    except (AssertionError, OSError, zipfile.BadZipFile) as exc:
        print(f"RELEASE_VALIDATION_FAILED: {exc}", file=sys.stderr)
        return 1
    print("RELEASE_VALIDATION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
