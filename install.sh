#!/usr/bin/env sh
set -eu

skill_name="truth-first-counterargument"
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_path="$script_dir/skills/$skill_name"
destination_root="${CODEX_HOME:-$HOME/.codex}/skills"
destination_path="$destination_root/$skill_name"

if [ ! -d "$source_path" ]; then
  echo "Skill source not found: $source_path" >&2
  exit 1
fi

mkdir -p "$destination_root"
source_real=$(CDPATH= cd -- "$source_path" && pwd -P)
destination_root_real=$(CDPATH= cd -- "$destination_root" && pwd -P)
destination_path="$destination_root_real/$skill_name"

case "$destination_path/" in
  "$source_real/"|"$source_real/"*)
    echo "Unsafe install path overlap: source=$source_real destination=$destination_path" >&2
    exit 1
    ;;
esac
case "$source_real/" in
  "$destination_path/"|"$destination_path/"*)
    echo "Unsafe install path overlap: source=$source_real destination=$destination_path" >&2
    exit 1
    ;;
esac

stage_path="$destination_root_real/.$skill_name.installing-$$"
if [ -e "$stage_path" ]; then
  echo "Staging path already exists: $stage_path" >&2
  exit 1
fi

cleanup_stage() {
  if [ -e "$stage_path" ]; then
    rm -rf -- "$stage_path"
  fi
}
trap cleanup_stage EXIT HUP INT TERM

cp -R "$source_real" "$stage_path"
find "$stage_path" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
find "$stage_path" -depth -type d -name '__pycache__' -exec rm -rf -- {} \;
backup_path=""
if [ -e "$destination_path" ]; then
  timestamp=$(date +%Y%m%d-%H%M%S)-$$
  backup_path="$destination_path.backup-$timestamp"
  mv "$destination_path" "$backup_path"
  echo "Existing install backed up to: $backup_path"
fi

if ! mv "$stage_path" "$destination_path"; then
  if [ -n "$backup_path" ] && [ ! -e "$destination_path" ] && [ -e "$backup_path" ]; then
    mv "$backup_path" "$destination_path"
  fi
  echo "Install failed; previous installation was restored when possible." >&2
  exit 1
fi
trap - EXIT HUP INT TERM
echo "Installed $skill_name to: $destination_path"
echo "Restart Codex so the skill list refreshes."
