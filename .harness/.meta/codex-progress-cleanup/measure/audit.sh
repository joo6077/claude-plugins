#!/usr/bin/env bash
set -eu
measure_dir=$(CDPATH='' cd -- "$(dirname -- "${0}")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
exec python3 "$measure_dir/audit.py" "$@"
