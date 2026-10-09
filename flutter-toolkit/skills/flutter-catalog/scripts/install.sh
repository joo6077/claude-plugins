#!/usr/bin/env bash
# flutter-catalog 틀을 Flutter 프로젝트에 깐다.
# 사용: install.sh [--add-deps] <프로젝트 폴더>
# 깔 파일이 하나라도 이미 있으면 아무것도 쓰지 않고 1 로 끝난다.
# --add-deps: analyzer · yaml 이 직접 의존성에 없으면 이미 잠긴 판으로 개발 의존성에 넣는다.
set -euo pipefail

ADD_DEPS=0
if [ "${1:-}" = "--add-deps" ]; then ADD_DEPS=1; shift; fi
PROJECT=${1:?사용: install.sh [--add-deps] <프로젝트 폴더>}
TEMPLATES="$(cd "$(dirname "${BASH_SOURCE[0]}")/../templates" && pwd)"

[ -f "$PROJECT/pubspec.yaml" ] || { echo "pubspec.yaml 없음: $PROJECT" >&2; exit 1; }
PACKAGE=$(awk '/^name:/{print $2; exit}' "$PROJECT/pubspec.yaml")

TARGETS=()
while IFS= read -r src; do
  TARGETS+=("${src%.tmpl}")
done < <(cd "$TEMPLATES" && find . -type f | sed 's#^\./##' | LC_ALL=C sort)

sort_imports() {  # sort_imports <파일> — 이어진 import 'package:…' 줄 묶음을 이름순으로
  python3 - "$1" <<'PY'
import sys
path = sys.argv[1]
lines = open(path, encoding='utf-8').read().split('\n')
out, block = [], []
for line in lines + [None]:
    if line is not None and line.startswith("import 'package:"):
        block.append(line)
        continue
    out.extend(sorted(block)); block = []
    if line is not None:
        out.append(line)
open(path, 'w', encoding='utf-8').write('\n'.join(out))
PY
}

EXISTING=0
for rel in "${TARGETS[@]}"; do
  if [ -e "$PROJECT/$rel" ]; then echo "이미 있음: $rel" >&2; EXISTING=1; fi
done
if [ "$EXISTING" = 1 ]; then
  echo "아무것도 쓰지 않았다. 지우거나 옮긴 뒤 다시 깔아라." >&2
  exit 1
fi

for rel in "${TARGETS[@]}"; do
  src="$TEMPLATES/$rel"; [ -f "$src" ] || src="$src.tmpl"
  mkdir -p "$(dirname "$PROJECT/$rel")"
  sed "s/{{package}}/$PACKAGE/g" "$src" > "$PROJECT/$rel"
  # 프로젝트 이름에 따라 package: 가져오기 순서가 바뀌므로 깐 뒤 이름순으로 다시 놓는다.
  case "$rel" in *.dart) sort_imports "$PROJECT/$rel";; esac
  echo "깔았다: $rel"
done

direct() {  # direct <패키지> — dependencies · dev_dependencies 에 직접 적혀 있으면 0
  awk -v p="$1" '/^(dependencies|dev_dependencies):/{f=1;next} /^[^ #]/{f=0} f && $1==p":"{found=1} END{exit !found}' "$PROJECT/pubspec.yaml"
}

if ! direct flutter_hooks; then
  echo "주의: flutter_hooks 가 직접 의존성에 없다. 놀이터 화면이 쓴다 — fvm flutter pub add flutter_hooks" >&2
fi

if [ "$ADD_DEPS" = 1 ]; then
  for dep in analyzer yaml; do
    direct "$dep" && continue
    ver=$(awk -v p="  $dep:" '$0==p{f=1;next} f&&/version:/{gsub(/"/,"",$2); print $2; exit}' "$PROJECT/pubspec.lock" 2>/dev/null || true)
    [ -n "$ver" ] || ver=any
    [ "$ver" = any ] || ver="^$ver"
    python3 - "$PROJECT/pubspec.yaml" "$dep" "$ver" <<'PY'
import re, sys
path, dep, ver = sys.argv[1:4]
text = open(path, encoding='utf-8').read()
line = f"  {dep}: {ver}\n"
if re.search(r'^dev_dependencies:\s*$', text, re.M):
    text = re.sub(r'^dev_dependencies:\s*\n', lambda m: m.group(0) + line, text, count=1, flags=re.M)
else:
    text = text.rstrip('\n') + '\n\ndev_dependencies:\n' + line
open(path, 'w', encoding='utf-8').write(text)
PY
    echo "개발 의존성에 넣었다: $dep $ver"
  done
fi

echo "다음: catalog/widgets.yaml 을 채우고 fvm dart run tool/catalog_gen.dart"
