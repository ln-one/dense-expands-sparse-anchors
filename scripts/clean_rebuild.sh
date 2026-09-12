#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
temporary_root=$(mktemp -d "${TMPDIR:-/tmp}/desa-rebuild.XXXXXX")
trap 'rm -rf "$temporary_root"' EXIT HUP INT TERM

cd "$repo_root"
UV_PROJECT_ENVIRONMENT="$temporary_root/venv" uv sync --frozen --extra dev
UV_PROJECT_ENVIRONMENT="$temporary_root/venv" uv run --frozen python \
  scripts/reproduce_results.py --output "$temporary_root/tables"
echo "clean rebuild matches released result tables"
