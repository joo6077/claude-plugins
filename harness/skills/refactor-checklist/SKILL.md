---
name: refactor-checklist
description: >
  리팩터링 시작 전, 대상 파일에 적용할 모든 규칙 위반을 enumerate 한 체크리스트를 산출하고 사용자 승인을 받는다.
  편집은 시작하지 않는다 — 체크리스트만 만든다. 사용자가 "리팩터링 체크리스트", "/refactor-checklist", "/refactor-widget",
  "anti-AI-tone 체크", "위반 enumerate", "리팩터 전 점검" 같은 표현을 쓸 때 트리거한다.
  체크리스트 승인 후 실제 편집은 별도 호출 (sprint-contract 또는 직접 편집).
argument-hint: "[대상 파일/폴더 경로 또는 글롭]"
user-invocable: true
---

# /refactor-checklist — Pre-Edit Batch Audit 체크리스트 산출

`/insights` 2026-05-07 fresh report Quick Win #2 ("편집 전 anti-AI-tone 체크리스트를 로드하는 /refactor-widget 스킬과 짝지으세요") 흡수. skill-design-guide v1.3.0 §3.6 Pre-Edit Batch Audit 의 도구화. fresh insight 의 Friction #1 ("규칙 기반 리팩터링에서 사전 점검 체크리스트를 건너뛰는 경향") 대응.

이름은 "/refactor-widget" 이 너무 Flutter 도메인 종속이라 stack-agnostic 한 "/refactor-checklist" 로 일반화. flutter-toolkit / react-kit / rust-kit 모두에서 호출 가능.

## Gotchas

- **본 스킬은 편집을 절대 하지 않는다.** 체크리스트만 산출 → 사용자 승인 → 편집은 별도 호출. 본 스킬이 직접 Edit/Write 하면 Pre-Edit Batch Audit 의 의미가 사라진다 — N 회 round-trip 을 막기 위함.
- **체크리스트 항목은 (a) 파일/라인 (b) 위반 규칙 식별자 (c) 권장 조치 3 요소를 모두 포함.** 빠지면 항목 자체가 ambiguous.
- **체크리스트 산출 후 "혹시 누락된 영역이 있는가?" meta-audit 1회.** 사용자 승인 직전 self-check.
- **스택/도메인 별 규칙 리스트 자동 로드 — 경로는 ladder 로 해석한다.** 규칙 소스를 레포 상대경로로만 적으면 킷을 **플러그인으로 설치한 프로젝트에서는 항상 부재**다. Step 1 의 ladder (`${CLAUDE_PLUGIN_ROOT}` → 레포 → 마켓플레이스 설치본) 로 `test -f` 판정하여 실제 존재하는 경로를 쓴다. qa-evaluator Step 8 이 쓰는 것과 **동일한 규약**이며 새 동의어를 만들지 마라.
- **로드 실패한 규칙 소스는 `[미검증]` 으로 표기하고, 그 카테고리를 "위반 0" 으로 보고하지 마라.** 규칙 파일을 못 읽어 검사하지 못한 것과 검사해서 위반이 없는 것은 다르다. 빈 결과를 통과로 읽는 것이 이번 사이클 최상위 마찰(`/insights` Friction #2)의 실제 사고 형태였다 — 체크리스트 머리말에 로드된 소스와 `[미검증]` 소스를 **각각 파일명으로** 나열한다.
- **사용자가 "그냥 편집해" 라고 하면 본 스킬을 강제 invoke 하지 마라.** Pre-Edit Batch Audit 는 3+ 파일 변경 또는 1+ 규칙군 검사가 필요할 때 의미가 있다. 1 파일 단순 수정에 본 스킬을 거는 것은 over-process.
- **체크리스트가 빈 결과 (0 위반) 이어도 보고하라.** 침묵하면 사용자가 검사를 안 한 줄 안다. "0 위반 — 진행 가능" 명시.

## Process

### Step 0: 대상 식별

인자(`$ARGUMENTS`)로 받은 경로/글롭을 해석. 글롭 매칭 결과 0 건이면 사용자에게 명확화 요청. 결과 50+ 파일이면 사용자에게 범위 좁힐지 확인.

### Step 1: 스택 + 규칙 리스트 자동 감지

```bash
ls pubspec.yaml package.json Cargo.toml 2>/dev/null
test -f .harness/project.yaml && cat .harness/project.yaml
```

스택별 규칙 출처 (`{kit}` / `{rel}` 은 아래 표에서 정한다):

| 감지 마커 | 킷 (`{kit}`) | 규칙 소스 상대경로 (`{rel}`) |
|----------|--------------|------------------------------|
| `pubspec.yaml` | flutter-toolkit | `references/flutter-ai-rules.md` |
| `package.json` + `vite.config.*` | react-kit | `references/` |
| `Cargo.toml` | rust-kit | `references/` |
| (그 외) | harness | `references/cross-kit-principles.md` |

여기에 **항상** `{프로젝트 루트}/.harness/project.yaml` 의 `anti_patterns` 를 더한다.

**경로 해석 ladder (E3 — `test -f` 로 결정론적 판정).** 위에서부터 존재하는 첫 경로를 쓴다:

```bash
# (1) 설치된 플러그인 — ${CLAUDE_PLUGIN_ROOT} 는 스킬 본문에서 치환된다 (본 킷 자신일 때)
RULES="${CLAUDE_PLUGIN_ROOT}/{rel}"
# (2) 플러그인 모노레포/체크아웃에서 직접 작업 중일 때
[ -f "$RULES" ] || RULES="{repo_root}/{kit}/{rel}"
# (3) 마켓플레이스 설치본 직접 탐색 (치환 실패 또는 타 킷 참조)
[ -f "$RULES" ] || RULES="$(ls -1d "$HOME"/.claude/plugins/marketplaces/*/{kit}/{rel} 2>/dev/null | head -1)"
[ -n "$RULES" ] && [ -e "$RULES" ] && echo "RESOLVED: $RULES" || echo "MISSING: {kit}/{rel}"
```

`MISSING` 이 나온 소스는 **로드 실패**다. 해당 규칙 카테고리는 검사하지 않은 것이므로 체크리스트에 `[미검증] {kit}/{rel} — 소스 부재로 미검사` 로 명시하고, 위반 0 으로 집계하지 마라.

### Step 2: 대상 파일 전수 read-only 스캔

각 대상 파일을 Read 로 통째 읽고, 규칙별로 위반 발견. **Edit/Write 절대 사용 금지.**

규칙 카테고리 예시 (스택별 가변):

- 토큰 마이그레이션 (Flutter: bodyMSemiBold → bodyMedium 등)
- 위젯/컴포넌트 선택 (Stack vs Column, Row vs Wrap, etc.)
- 불필요한 null 분기 / 하드코드 값 / manual gap (SizedBox)
- import 정리 / unused 변수 / 매직 넘버
- anti-AI-tone (과도한 주석, 중복 변수, 추론 가능한 네이밍)
- Figma 토큰 검증 (시각 디자인 작업 시)

### Step 3: 체크리스트 산출

```markdown
# Pre-Edit Batch Audit Checklist

대상: <인자>
스택: <감지 결과>
스캔 파일: N
규칙 카테고리: M
로드된 규칙 소스: <해석된 절대경로 나열>
[미검증] 규칙 소스: <MISSING 으로 판정된 소스 나열 — 없으면 "없음">


## 위반 항목

- [ ] [V01] `lib/widgets/x.dart:42` — Rule R1 (TextStyle migration)
  - 위반: bodyMSemiBold 잔존
  - 조치: bodyMedium + fontWeight FontWeight.w600 로 마이그레이션
- [ ] [V02] `lib/widgets/x.dart:88` — Rule R3 (Stack vs Column)
  - 위반: Stack 으로 충분히 Column 가능
  - 조치: Column + MainAxisAlignment.start
...

## meta-audit

스캔 시 누락된 영역 점검:
- 인접 파일 (lib/widgets/x_test.dart) 도 동일 규칙 위반 가능 → 추가 스캔 필요?
- 다른 규칙 카테고리 (예: l10n key) 도 적용?

## 다음 단계 (사용자 결정)

승인 시 → /sprint 또는 직접 편집으로 V01~V0N 일괄 처리
범위 조정 → 항목 추가/제거 후 재제출
```

### Step 4: 사용자 응답 대기

체크리스트만 보고하고 종료. 편집은 사용자 승인 후 별도 호출.

## References

- `harness/docs/guides/skill-design-guide.md` §3.6 — Pre-Edit Batch Audit + Scope-Bound Edits
- `harness/docs/guides/skill-design-guide.md` §3.7 — Completion Evidence Gate (검사 못 한 것을 통과로 읽지 않기)
- `harness/agents/qa-evaluator.md` Step 8 — 동일한 경로 해석 ladder 규약 (용어 재사용, 동의어 금지)
- `harness/skills/sprint/SKILL.md` — 본 스킬과 짝. /sprint 는 본 스킬을 Step 2 의 일부로 호출 가능
- `~/.claude/usage-data/report-ko.html` — `/insights` Quick Win #2 (본 스킬의 source of truth)
- 스택별 규칙 소스: flutter-toolkit/references/, react-kit/references/, rust-kit/references/
