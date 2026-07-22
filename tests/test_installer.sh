#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd -P)
installer="$repo_root/install.sh"
source_path="$repo_root/skills/truth-first-counterargument"
test_root=$(mktemp -d "${TMPDIR:-/tmp}/truth-first-counterargument-test.XXXXXX")

cleanup() {
  rm -rf -- "$test_root"
}
trap cleanup EXIT HUP INT TERM

CODEX_HOME="$test_root/codex" sh "$installer"
CODEX_HOME="$test_root/codex" sh "$installer"

installed="$test_root/codex/skills/truth-first-counterargument"
if [ ! -f "$installed/SKILL.md" ]; then
  echo "Installed SKILL.md is missing" >&2
  exit 1
fi
backup_count=$(find "$test_root/codex/skills" -maxdepth 1 -type d -name 'truth-first-counterargument.backup-*' | wc -l | tr -d ' ')
if [ "$backup_count" -ne 1 ]; then
  echo "Expected one backup after reinstall; found $backup_count" >&2
  exit 1
fi

if CODEX_HOME="$repo_root" sh "$installer" >/dev/null 2>&1; then
  echo "Source/destination overlap was not rejected" >&2
  exit 1
fi
if [ ! -f "$source_path/SKILL.md" ]; then
  echo "Overlap test damaged the active source skill" >&2
  exit 1
fi

echo "POSIX_INSTALLER_TEST_OK"
