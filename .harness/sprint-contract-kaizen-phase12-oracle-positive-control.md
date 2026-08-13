---
feature: "카이젠 Phase 12 재검증 — 정규화 오라클에 양성 대조 부착(F2) + grep 거짓음성 규약(F1) + 추출 SSOT 통합(F4) + 열 서술 정정(F3)"
created: "2026-08-13 18:20"
complexity: "중간"
conditions: 14
slug: kaizen-phase12-oracle-positive-control
status: active
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
conditions_digest: sha256:87763986f7bc35b4
locked_at: "2026-08-13 18:20"
---

## 배경

Phase 12 의 K1~K3 은 이미 착지했다 (커밋 `0fe357a` + QA blocking 해소 `a137055`). 이 스프린트는
**그 산출물을 독립 재실행해 검증하는 과정에서 드러난 결함 4 개**를 고친다. K1~K3 의 규칙 문장을
다시 추가하는 것이 아니다 — 이번 사이클 하드 프레이밍대로 **오라클의 판별력을 올린다.**

재검증으로 확인한 것 (전부 실행 결과):

| # | 결함 | 실측 |
|---|---|---|
| F1 | **grep 오라클이 참인 매치를 0 으로 보고** | 이 환경 `grep` 은 ugrep 7.5.0 이고 패턴 중간 `$` 를 앵커로 해석. 직전 계약 RE-02 측정문 `grep -c 'source "$SCRIPT_DIR/_lib-'` → **0**, `-F` → **3** (참값 3) |
| F2 | **셸·cwd 24 조합 게이트가 퇴화 입력에서 거짓 PASS** | fixture 를 `- mistake_tag:`(선행 하이픈)로 잘못 만들자 24 회 전부 `0 0 0 0 0.00 0.000 0.00` → `sort -u` 1 행 = PASS. 태그를 한 건도 세지 않은 채로 |
| F3 | 라이브러리 주석이 **3 열**이라고 서술 (실제 7 열) | `_lib-tag-canon.sh` 2 곳. `cut -f3` 을 ratio 로 읽으면 실제로는 `entries` 를 얻는다 |
| F4 | 추출 규칙(grep+sed)이 **2 곳에 중복** | 훅과 라이브러리에 같은 패턴. 한쪽만 고쳐지면 수집면과 집계면이 갈라져 K3 과소집계가 그대로 복귀 |

F1·F2 는 같은 뿌리다 — **일치성·부재만 보는 오라클은 아무것도 안 하는 구현을 통과시킨다.**
직전 사이클 사고("계약 25 조건 전부 PASS 인데 기능 파손")와 동형이므로, 대응은 문장 추가가 아니라
**양성 대조를 실행 경로에 박는 것**(E1 서술 → E3 실행)이다.

F3 은 사실 오류이므로 정정한다. F4 는 SSOT 위반이며 등가성을 먼저 증명한 뒤 통합한다
(md5 동일 확인: 실로그 13 파일 · `0de336873d8c6758d2ecb6ffb01ebb9b`).

## 리서치 소스

- `.harness/.meta/evidence/phase12.md` (유일 외부 근거 · 외부 조회 0 회)
- `reflect-kit/references/tag-canonicalization.md` §6.1 (직전 커밋이 세운 무증상 실패 규약)
- 직전 산출물: 커밋 `0fe357a` · `a137055`

## GAP 분석

| # | 현재 | 갭 | 조치 |
|---|---|---|---|
| G1 | 회귀 게이트가 셸·cwd 일치만 본다 | 0 매치 입력에서 거짓 PASS | `tag_canon_selftest` 양성 대조 신설 (접힘 4→2 단정) |
| G2 | selftest 를 아무도 호출하지 않는다 | 문서에만 있으면 안 돌아간다 | `reflect-digest` · `reflect-kaizen` 실행 블록에 부착 |
| G3 | selftest 실패의 효력이 미정 | 실패해도 집계가 진행된다 | kaizen 은 `calibration_confidence: low` 와 동일 효력 · digest 는 집계 근거 사용 금지 |
| G4 | "0 건 = PASS" grep 오라클 규약 없음 | 거짓 음성으로 위반 통과 | §6.1 규칙 7 + ugrep 실측 |
| G5 | 추출 규칙 2 곳 | 조용한 분기 | 훅이 `tag_canon_extract` 호출 |
| G6 | 주석이 3 열이라고 말한다 | 잘못된 열 인덱스 | 7 열로 정정 |

## 범위 경계

- **Scope**: `reflect-kit/skills/*/SKILL.md` · `reflect-kit/hooks/*.sh` · `reflect-kit/references/`
- **Scope 밖 (수정 금지)**: `reflect-kit/docs/*` · `reflect-kit/README.md` · `reflect-kit/hooks/hooks.json` ·
  `reflect-kit/scripts/*` · `reflect-kit/.claude-plugin/*` · `~/.claude/logs/**` (읽기 전용) ·
  사용자 전역 훅 설정(`~/.claude/settings.json`, `~/.claude/hooks/`) · **직전 계약
  `sprint-contract-kaizen-phase12-tag-canonicalization.md` (봉인 · 조건 문구 불변)**
- 직전 계약은 `status: active` 이나 QA 산출물이 없어 **내가 `done` 으로 전환하지 않는다** (전환 주체는
  qa-evaluator). 그래서 이 스프린트는 새 슬러그로 분리했다 — 봉인된 계약에 조건을 덧붙이지 않기 위해서다.
- Diff-Scope baseline (계약 작성 시점 실행): `git status --porcelain -- reflect-kit/` →
  `M reflect-kit/hooks/_lib-tag-canon.sh` / `M reflect-kit/hooks/log-reflection.sh` /
  `M reflect-kit/references/tag-canonicalization.md` / `M reflect-kit/skills/reflect-digest/SKILL.md` /
  `M reflect-kit/skills/reflect-kaizen/SKILL.md`

## 회귀 게이트

- 모든 grep 오라클은 `-F` 또는 이스케이프를 쓴다 (F1 자체가 이 규칙 위반으로 생겼다).
- selftest 의 **판별력**을 음성 대조로 증명한다 — 맵을 손상시키면 반드시 FAIL 해야 한다.
- 음성 대조는 `export` 로 환경변수를 넘긴다. `VAR=x . lib; func` 는 함수에 전달되지 않아
  **대조 자체가 성립하지 않는다** (재검증 중 실제로 거짓 OK 를 관측했다).
- 열거값(조합 수·경로 수)은 타이핑하지 않고 명령으로 계산한다.

## Skill

- [ ] SK-01: 결정론 pass 실행 블록에서 `tag_canon_selftest` 를 호출하는 스킬이
      `reflect-kit/skills/reflect-digest/SKILL.md`, `reflect-kit/skills/reflect-kaizen/SKILL.md`
      2 개다 [exact, enumerated]
      (측정: `grep -rlF 'tag_canon_selftest' reflect-kit/skills` 결과가 위 2 경로와 정확히 일치)
- [ ] SK-02: selftest 실패의 **효력**이 두 스킬에 각각 규정된다 [exact, enumerated]
      (측정: `grep -cF 'calibration_confidence: low' reflect-kit/skills/reflect-kaizen/SKILL.md` 결과가
      직전 대비 증가하고 selftest 문맥에 그 문자열이 존재 ·
      `grep -cF '집계 근거로 쓰지 마라' reflect-kit/skills/reflect-digest/SKILL.md` >= 1)
- [ ] SK-03: SSOT `tag-canonicalization.md` 에 규칙 6(양성 대조)과 규칙 7(grep 거짓음성)이
      각각 존재한다 [exact, enumerated]
      (측정: `grep -cF '규칙 6' reflect-kit/references/tag-canonicalization.md` >= 1 ·
      `grep -cF '규칙 7' reflect-kit/references/tag-canonicalization.md` >= 1 ·
      규칙 7 문맥에 `ugrep` 문자열 존재)

## Script

- [ ] SC-01: `tag_canon_selftest` 가 정상 맵에서 `SELFTEST_OK` 를 출력하고 rc 0 이다 [goal]
      (측정: `. <lib>; tag_canon_selftest` 출력에 `SELFTEST_OK` 포함 · rc 0 ·
       음성 대조: `tag-lemma-map.tsv` 의 `verb` 행을 제거한 맵을 `export REFLECT_TAG_LEMMA_MAP` 으로
       넘기면 이 측정이 **FAIL** 해야 한다)
- [ ] SC-02: selftest 가 손상된 맵 3 종에서 전부 rc 1 을 낸다 — 판별력 증명 [exact, enumerated]
      (Given: `export REFLECT_TAG_LEMMA_MAP` 으로 전달 ·
       측정: 맵 부재(`/nonexistent`) · `verb` 행 제거 · `verb-synonym` 행 제거 3 케이스 각각 rc 1 이고
       출력에 `SELFTEST_FAIL` 포함 · 3 케이스의 `clusters` 값이 정상(2)과 다름)
- [ ] SC-03: selftest 출력이 `{set -u 유·무} × {bash·zsh·sh} × {cwd 4 종}` 전 조합에서 동일하다
      [exact, enumerated]
      (측정: 조합 수를 명령으로 산출(`2*3*4`)해 그 횟수만큼 실행 · 출력을 `sort -u` 했을 때 1 행 ·
       그 1 행이 `SELFTEST_OK` 이다 — 퇴화 출력이 아님을 함께 단정)
- [ ] SC-04: 훅 어휘 생성 경로 3 종이 추출 통합 후에도 동작한다 [goal]
      (측정: 어휘 생성 구간을 원문 그대로 추출해 실행 — (a) 정상: `canonical  (freq N)  ← ...` 행 존재 ·
       (b) `REFLECT_TAG_LEMMA_MAP=/nonexistent`: `warn:lemma-map-unreadable` 1 행 + 어휘 블록 비어 있지 않음 ·
       (c) 빈 디렉토리: `(없음 — 첫 수집)` 포함 · 셸 오류 0 행 ·
       음성 대조: `tag_canon_extract` 호출을 지우면 (a) 의 행이 사라져야 한다)
- [ ] SC-05: 추출 규칙(`mistake_tag` grep 패턴)이 `reflect-kit/hooks/` 안에서 라이브러리 1 곳에만
      존재한다 [exact]
      (측정: `grep -rlF 'mistake_tag:' reflect-kit/hooks` 결과가 `_lib-tag-canon.sh` 1 행 ·
       등가 증명: 실로그 전량에 대해 통합 전 인라인 추출과 `tag_canon_extract` 의 md5 가 동일)
- [ ] SC-06: 변경 셸 스크립트 2 개가 `shellcheck` 0 findings 이고 `bash -n` 을 통과한다
      [exact, enumerated]
      (측정: `shellcheck reflect-kit/hooks/_lib-tag-canon.sh reflect-kit/hooks/log-reflection.sh`
       출력 0 행 + exit 0 · 두 파일 각각 `bash -n` exit 0)

## Architecture

- [ ] AR-01: 변경이 정확히 5 경로로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 working tree ·
       측정: `git status --porcelain -- reflect-kit/` 의 경로 집합이
       `reflect-kit/hooks/_lib-tag-canon.sh`, `reflect-kit/hooks/log-reflection.sh`,
       `reflect-kit/references/tag-canonicalization.md`,
       `reflect-kit/skills/reflect-digest/SKILL.md`,
       `reflect-kit/skills/reflect-kaizen/SKILL.md` 와 정확히 일치)
- [ ] AR-02: 사실 정정 — 라이브러리에서 파편화 출력을 3 열로 서술하는 문장이 **0 건**이다 [exact]
      (측정: `grep -cF 'clusters \t ratio' reflect-kit/hooks/_lib-tag-canon.sh` == 0 ·
       대조: 7 열을 서술하는 줄이 1 행 이상 존재)
- [ ] AR-03: 직전 계약 파일의 조건 문구가 변경되지 않았다 (봉인 유지) [exact]
      (측정: `git diff --name-only -- .harness/sprint-contract-kaizen-phase12-tag-canonicalization.md`
       결과 0 행)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py reflect-kit` 가 V1~V8 전부 OK, exit 0
- [ ] DG-02: `python3 scripts/sync-docs.py reflect-kit --check-only` 가 동기화 필요 0 건
