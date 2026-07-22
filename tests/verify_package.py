from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "truth-first-counterargument"
REQUIRED_FILES = [
    SKILL_ROOT / "SKILL.md",
    SKILL_ROOT / "agents" / "openai.yaml",
    SKILL_ROOT / "references" / "research-protocol.md",
    SKILL_ROOT / "references" / "argument-engine.md",
    SKILL_ROOT / "references" / "output-contract.md",
    SKILL_ROOT / "references" / "domain-checklists.md",
    SKILL_ROOT / "references" / "integrity-guardrails.md",
    SKILL_ROOT / "scripts" / "confidence_calibrator.py",
    SKILL_ROOT / "assets" / "case-file-template.json",
    SKILL_ROOT / "LICENSE.txt",
    REPO_ROOT / "README.md",
    REPO_ROOT / "LICENSE",
    REPO_ROOT / "VERSION",
]


def fail(message: str) -> None:
    raise AssertionError(message)


def verify_required_files() -> None:
    missing = [str(path.relative_to(REPO_ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files: " + ", ".join(missing))


def verify_frontmatter() -> None:
    text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, flags=re.S)
    if not match:
        fail("SKILL.md frontmatter is missing")
    keys = re.findall(r"^([A-Za-z_][A-Za-z0-9_-]*):", match.group(1), flags=re.M)
    if keys != ["name", "description"]:
        fail(f"SKILL.md frontmatter must contain only name and description; got {keys}")
    if "name: truth-first-counterargument" not in match.group(1):
        fail("Skill name does not match folder name")
    description_line = re.search(r"^description:\s*(.+)$", match.group(1), flags=re.M)
    if not description_line:
        fail("Skill description is missing")
    if len(description_line.group(1)) > 1024:
        fail("Skill description exceeds the 1024-character limit")
    description = match.group(1).lower()
    for phrase in [
        "buna karşı ne diyebilirim",
        "karşı argüman sun",
        "how can i refute this",
        "do not use for ordinary research",
        "ama bu nasıl olur",
    ]:
        if phrase not in description:
            fail(f"Trigger contract phrase missing from description: {phrase}")


def verify_no_placeholders() -> None:
    placeholder_tokens = ("[" + "TODO", "TODO" + ":")
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".yaml", ".json", ".py", ".ps1", ".sh"}:
            continue
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in placeholder_tokens):
            fail(f"Placeholder remains in {path.relative_to(REPO_ROOT)}")
    if (SKILL_ROOT / "README.md").exists():
        fail("README.md must stay outside the installable skill folder")


def verify_no_generated_artifacts() -> None:
    for path in REPO_ROOT.rglob("*"):
        if "__pycache__" in path.parts or path.suffix.lower() in {".pyc", ".pyo"}:
            fail(f"Generated Python artifact must not ship: {path.relative_to(REPO_ROOT)}")


def verify_json_and_triggers() -> None:
    for path in REPO_ROOT.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    cases = json.loads((REPO_ROOT / "tests" / "trigger-cases.json").read_text(encoding="utf-8"))
    if len(cases.get("positive", [])) < 12 or len(cases.get("negative", [])) < 12:
        fail("Trigger matrix needs at least 12 positive and 12 negative cases")
    positives = {entry["text"].casefold() for entry in cases["positive"]}
    negatives = {entry["text"].casefold() for entry in cases["negative"]}
    overlap = positives & negatives
    if overlap:
        fail(f"Trigger cases overlap: {sorted(overlap)}")


def verify_relative_links() -> None:
    pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for path in REPO_ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in pattern.findall(text):
            clean = target.strip().strip("<>").split("#", 1)[0]
            if not clean or re.match(r"^[a-z]+://", clean, flags=re.I) or clean.startswith("mailto:"):
                continue
            candidate = (path.parent / clean).resolve()
            if not candidate.exists():
                fail(f"Broken relative link in {path.relative_to(REPO_ROOT)}: {target}")


def verify_svg_xml() -> None:
    for path in (REPO_ROOT / "docs" / "assets").glob("*.svg"):
        ET.parse(path)


def main() -> int:
    try:
        verify_required_files()
        verify_frontmatter()
        verify_no_placeholders()
        verify_no_generated_artifacts()
        verify_json_and_triggers()
        verify_relative_links()
        verify_svg_xml()
    except (AssertionError, UnicodeDecodeError, json.JSONDecodeError, ET.ParseError) as exc:
        print(f"PACKAGE_VALIDATION_FAILED: {exc}", file=sys.stderr)
        return 1
    print("PACKAGE_VALIDATION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
