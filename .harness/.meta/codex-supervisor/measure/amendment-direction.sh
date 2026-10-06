#!/usr/bin/env bash
# contract-schema helpers: braces protect positional arguments in skill rendering.
set -eu
amend_direction() {
  for f in "${1}" "${2}"; do [ -f "$f" ] || { echo "unknown missing_input=$f"; return 0; }; done
  added=$(comm -13 <(LC_ALL=C sort -u "${1}") <(LC_ALL=C sort -u "${2}") | grep -c . || true)
  removed=$(comm -23 <(LC_ALL=C sort -u "${1}") <(LC_ALL=C sort -u "${2}") | grep -c . || true)
  if [ "$added" -eq 0 ] && [ "$removed" -gt 0 ]; then echo "narrowing added=$added removed=$removed"
  elif [ "$added" -gt 0 ]; then echo "relaxing added=$added removed=$removed"
  else echo "unknown added=$added removed=$removed"; fi
}
amend_direction_oracle() {
  for f in "${1}" "${2}"; do [ -f "$f" ] || { echo "unknown missing_input=$f"; return 0; }; done
  added=$(comm -13 <(LC_ALL=C sort -u "${1}") <(LC_ALL=C sort -u "${2}") | grep -c . || true)
  removed=$(comm -23 <(LC_ALL=C sort -u "${1}") <(LC_ALL=C sort -u "${2}") | grep -c . || true)
  if [ "$removed" -gt 0 ]; then echo "relaxing measured_removed=$removed measured_added=$added"
  elif [ "$added" -gt 0 ]; then echo "narrowing measured_removed=0 measured_added=$added"
  else echo "unknown measured_removed=0 measured_added=0"; fi
}
case "${1:-}" in
  allowed) amend_direction "${2}" "${3}" ;;
  measured) amend_direction_oracle "${2}" "${3}" ;;
  *) echo 'usage: amendment-direction.sh allowed|measured before after'; exit 64 ;;
esac
