#!/usr/bin/env python3
"""check-stale-values.py — 정정한 값의 옛 형태가 소스에 되살아났는지 본다.

문서 사이트는 소스 `.md` → 생성 HTML 파이프라인이다. 생성물만 고치면 다음 재생성이
조용히 되돌린다. 2026-09-06 하루에 이 실수가 **세 번** 재발했다.

  1 차  design-kit·harness·api 소스만 맞추고 backend·infra 를 빠뜨렸다
  2 차  같은 파일 안 "OpenAPI 3.1.1" 두 곳 중 표만 고치고 프로즈를 놓쳤다
  3 차  같은 파일 안 출처 인용 링크 한 줄을 또 놓쳤다

세 번 다 원인이 같다 — **"고친 자리" 를 확인하고 "옛 값이 남았는지" 를 확인하지 않았다.**
게다가 2 차 확인에 쓴 셸 sweep 은 zsh 가 따옴표 없는 변수를 단어 분할하지 않아
디렉토리를 하나도 못 찾았고, 그 `0` 을 "없음" 으로 읽어 커밋 메시지에 증거로 적었다.
`0` 은 "위반 없음" 과 "검사 안 됨" 을 구분해 주지 않는다.

그래서 이 스크립트는 **먼저 검사 범위를 출력한다.** 파일 0 개면 그 자체로 실패다.

등록부: `.harness/stale-values.yaml` — 값마다 `old`/`new`/`note`, 그리고 고치면 안 되는
자리는 `allow` 에 경로와 사유를 적는다 (날짜 박힌 기록 · 개명 이력 설명 · 다른 뜻의 동형 문자열).

Usage:
    python3 scripts/check-stale-values.py
    python3 scripts/check-stale-values.py --json

exit 0 = 되살아난 옛 값 없음, 1 = 있음, 2 = 검사 범위가 비었음(설정 오류).
"""
import json
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
REGISTRY = REPO / ".harness" / "stale-values.yaml"

# `.claude/skills/docs-site/SKILL.md` 의 소스→출력 매핑표에 대응하는 소스 디렉토리.
# 매핑이 늘면 여기도 늘려야 한다 — 그래서 아래에서 존재 여부를 검사하고 없으면 경고한다.
SOURCE_DIRS = [
    "design-kit/docs/design", "design-kit/references",
    "harness/docs/guides", "harness/references",
    "flutter-toolkit/references",
    "docs/backend", "docs/infra", "docs/tone", "docs/api",
    "docs/rust", "docs/react", "docs/planning",
]


def main() -> int:
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    values = reg.get("values", [])

    files, missing_dirs = [], []
    for d in SOURCE_DIRS:
        p = REPO / d
        if not p.exists():
            missing_dirs.append(d)
            continue
        files += sorted(p.rglob("*.md"))

    as_json = "--json" in sys.argv
    if not as_json:
        print(f"검사 범위: 소스 디렉토리 {len(SOURCE_DIRS) - len(missing_dirs)}/{len(SOURCE_DIRS)} · "
              f"파일 {len(files)} 개 · 등록값 {len(values)} 개")
        for d in missing_dirs:
            print(f"  경고: 없는 소스 디렉토리 {d}")

    if not files:
        print("ERROR: 검사 대상 파일이 0 개다. 범위 설정이 잘못됐다 — 이 상태의 '위반 0' 은 무의미하다.",
              file=sys.stderr)
        return 2

    text = {f: f.read_text(encoding="utf-8", errors="replace").splitlines() for f in files}
    findings = []
    for v in values:
        old = v["old"]
        allow = {a["path"] for a in v.get("allow", [])}
        for f, lines in text.items():
            rel = str(f.relative_to(REPO))
            if rel in allow:
                continue
            for i, line in enumerate(lines, 1):
                if old in line:
                    findings.append({"old": old, "new": v.get("new", ""), "file": rel, "line": i})

    if as_json:
        print(json.dumps({"files": len(files), "values": len(values), "findings": findings},
                         ensure_ascii=False, indent=1))
    elif findings:
        print(f"\n되살아난 옛 값 {len(findings)} 건:")
        for x in findings:
            print(f"  {x['file']}:{x['line']}  {x['old']!r} -> {x['new']!r}")
        print("\n예외로 둘 자리면 .harness/stale-values.yaml 의 allow 에 사유와 함께 등록하라.")
    else:
        print("\n되살아난 옛 값 없음")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
