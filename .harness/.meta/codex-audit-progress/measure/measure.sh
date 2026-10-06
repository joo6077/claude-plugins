#!/usr/bin/env bash
set -eu
measure_dir=$(CDPATH='' cd -- "$(dirname -- "${0}")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
if [ "${1-}" = "스킬-02" ]; then
  exec python3 "$measure_dir/amendment1.py" "$@"
fi
exec python3 "$measure_dir/measure.py" "$@"
