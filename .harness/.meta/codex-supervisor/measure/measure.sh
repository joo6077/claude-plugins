#!/usr/bin/env bash
# bash / zsh; positional arguments use braces for skill argument substitution safety.
set -eu
measure_dir=$(CDPATH='' cd -- "$(dirname -- "${0}")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
exec python3 "$measure_dir/measure.py" "$@"
