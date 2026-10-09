#!/usr/bin/env bash
# bash / zsh; positional arguments use braces for skill argument substitution safety.
set -eu
measure_dir=$(CDPATH='' cd -- "$(dirname -- "${0}")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
case "${1:-}" in
  스크립트-12|스크립트-13|스크립트-14|스크립트-15|스크립트-16|스크립트-17|스크립트-18|스크립트-19)
    exec python3 "$measure_dir/amendment.py" "$@"
    ;;
esac
exec python3 "$measure_dir/measure.py" "$@"
