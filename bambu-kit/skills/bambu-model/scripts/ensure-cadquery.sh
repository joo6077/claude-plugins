#!/usr/bin/env bash
# 전역 python3 에 CadQuery · matplotlib · numpy-stl 이 있으면 그대로 쓰고, 없을 때만 깐다
# 종료 코드: 0 쓸 수 있음 · 1 설치 뒤에도 불러오지 못함
# -I(격리 모드)를 붙이지 않는다 — 사용자 폴더(~/.local)에 깔린 의존 패키지를 못 보고 import 가 죽는다
set -uo pipefail

can_import() {
  python3 -c "import cadquery, matplotlib, stl" >/dev/null 2>&1
}

if can_import; then
  echo "있음: CadQuery $(python3 -c 'import cadquery; print(cadquery.__version__)') ($(command -v python3))"
  exit 0
fi

echo "없음 → 설치: cadquery matplotlib numpy-stl"
python3 -m pip install -q cadquery matplotlib numpy-stl
if can_import; then
  echo "설치됨: CadQuery $(python3 -c 'import cadquery; print(cadquery.__version__)')"
  exit 0
fi
echo "설치 뒤에도 불러오지 못함 — python3 -c 'import cadquery' 의 오류를 확인하라" >&2
exit 1
