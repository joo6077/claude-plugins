# Sprint Contract — Kaizen Phase 12 (reflect-kit)

- 날짜: 2026-07-27
- 브랜치: `kaizen/2026-07-27`
- 범위: `reflect-kit/` (skills 4종 · hooks · docs SSOT · README)
- 상태: DRAFT → 구현 → self-audit

## 배경 (실측)

30일 reflection 760 엔트리 중 **351건(40%)이 훅/가드 실패**이고 **54종 태그**로 파편화되어 있다.
전부 fit-pal `.claude/settings.json` 의 단일 환경 오설정(없는 스크립트 참조 + 상대경로 cwd 해석 실패)이
매 툴콜마다 재로깅된 것이다. 결과: (1) 개별 빈도가 precedence 임계 미달로 아무것도 승격되지 않음
(2) 진짜 행동 신호(API 문서 조회 스킵 18 · 스코프 크립 13 · 실앱 검증 우회 14)가 묻힘
(3) 사용자 환경 작업이 `tool_failure` 로 오귀인.

근거 문서: `.claude/kaizen-input/reflect-digest-2026-07-27.md`,
`.claude/kaizen-input/fit-pal-hook-diagnosis-2026-07-27.md`, `.claude/kaizen-input/insights-report.md` §0.

## 레이어 판단 (구현 전 확정)

| 레이어 | 역할 | 근거 |
|---|---|---|
| hook (`log-reflection.sh`) | **예방** — 분석기에 기존 태그 어휘를 주입해 재사용 유도 + 환경 오설정 결정론적 dedup | ledger 의 `post_freq` 가 `mistake_tag` 를 키로 재발을 센다. 태그가 쪼개지면 post_freq 가 구조적으로 과소집계되어 "효과 있음" 오판정이 나온다 → 쓰기 시점 수정이 근본 |
| digest | **복구** — 이미 쌓인 파편을 `canonical_tag` + `aliases` 클러스터로 묶어 precedence 적용 | 과거 로그는 소급 수정 불가. 읽기 시점 클러스터링 없이는 행동 신호(API 문서 조회 스킵 계열 6태그/15건)가 계속 임계 미달 |
| promote / kaizen | **측정** — `aliases` 합산 post_freq + 재발 시 enforcement 등급 상향 | 승격했는데 재발한 규칙에 같은 surface 를 다시 쓰는 경로만 있었다 |

디제스트 단독 해결은 기각한다 — ledger 키를 고치지 못한다.

## 완료 조건

### A. 태그 canonicalization

- **A-1** `[exact]` `hooks/log-reflection.sh` 가 `$log_dir/reflections-*.md` 에서 기존 `mistake_tag` 어휘를 **실측 수집**해 프롬프트에 주입한다. 하드코딩 태그 목록 금지.
- **A-2** `[exact]` 프롬프트에 `mistake_tag` 작성 규칙이 4항 이상 명시된다: 근본원인 1개=태그 1개 / kebab `<행동동사>-<대상>` 형태 / 기존 어휘 철자 그대로 재사용 / 단수·복수·어순·동의어 변형 금지.
- **A-3** `[structural]` A-2 에 **label collapse 반대 조항**이 함께 있다 — "새로운 종류면 새 태그를 만들고, 드문 신호를 기존 태그에 억지로 끼워넣지 마라".
- **A-4** `[exact]` `skills/reflect-digest/SKILL.md` Process 에 태그 클러스터링 단계가 있고, `canonical_tag` + `aliases` 로 표현하며 precedence 를 **cluster_freq** 로 적용한다고 명시한다. 클러스터마다 멤버 태그 + 개별 freq 감사 흔적 필수.
- **A-5** `[exact, enumerated]` ledger 스키마에 `aliases` 필드가 3곳 전부 추가된다: `skills/reflect-digest/SKILL.md`, `skills/reflect-promote/SKILL.md`, `docs/SCHEMA.md`.

### B. 환경 오설정 반복 로깅 억제

- **B-1** `[exact, enumerated]` YAML 스키마에 `actionability: claude_behavior | user_environment` 필드가 추가되고 4곳에 반영된다: `hooks/log-reflection.sh` 프롬프트, `skills/reflect-digest/SKILL.md`, `docs/SCHEMA.md`, `docs/DESIGN.md`.
- **B-2** `[exact]` `hooks/log-reflection.sh` 에 **LLM 호출 없는** 결정론적 dedup 게이트가 있다. `actionability: user_environment` 블록의 `mistake_tag` 가 억제 창 안에 이미 기록됐으면 append 하지 않는다.
- **B-3** `[structural]` dedup 게이트는 **fail-open** 이다: `actionability` 누락·파싱 실패·awk 비정상 종료 시 원본 블록을 보존한다. `claude_behavior` 블록은 어떤 경우에도 억제되지 않는다.
- **B-4** `[exact]` 억제된 사건이 유실되지 않는다 — `.env-issues.tsv` 에 `tag / first_seen / last_seen / count` 를 유지하고, digest 가 이를 읽어 "환경 액션 아이템" 으로 보고한다.
- **B-5** `[exact]` `bash -n hooks/log-reflection.sh` 통과 + dedup 게이트 **실제 실행 테스트** 증거 (억제 케이스 · 보존 케이스 · 필드 누락 fail-open 케이스 3종).

### C. "없는 훅 추가" meta-제안 억제

- **C-1** `[exact]` 프롬프트에 "`user_environment` 면 `desired_behavior` 에 환경 수정 지시를 쓰지 말고 Claude 가 그 상황에서 무엇을 보고했어야 하는가를 써라" 규칙이 있다.
- **C-2** `[exact]` digest SKILL 에 `user_environment` 후보를 precedence/승격 파이프라인에서 **제외**하고 별도 섹션으로 라우팅하는 Gotcha + 안티패턴이 있다.
- **C-3** `[exact]` promote SKILL 에 `user_environment` 후보 승격 금지 조항이 있다.

### D. 재발 시 enforcement 등급 상향

- **D-1** `[exact]` promote SKILL 에 재발 시 등급 상향 경로가 있고 `harness/docs/guides/skill-design-guide.md` §3.7 을 SSOT 로 인용한다. E1/E2/E3 의 **재정의·동의어 금지**.
- **D-2** `[exact]` 승급 임계가 SSOT 와 동일하다: 재발 2회 → E2, 3회 이상 또는 비가역·신뢰 손상 → E3.
- **D-3** `[exact, enumerated]` ledger 에 `enforcement_level` 필드가 3곳 전부 추가된다: digest SKILL, promote SKILL, `docs/SCHEMA.md`.
- **D-4** `[exact]` `skills/reflect-kaizen/SKILL.md` 의 verdict 목록에 `enforcement-escalation` 이 포함되고, `post_freq` 측정이 `aliases` 를 합산한다고 명시한다.

### E. digest 실측 관측 3건

- **E-1** `[exact]` digest 출력 포맷에 `파싱 실패: N 블록` 라인이 **필수**다 (0 이어도 생략 금지).
- **E-2** `[exact]` 단일 프로젝트 점유율 임계(≥ 60%) 초과 시 편중 경고 라인이 필수이고, precedence rule #3(global 판정) 보정 절차가 명시된다.
- **E-3** `[exact]` digest 데이터 소스 목록에 `.env-issues.tsv` 가 추가된다.

### F. 정합성 · 회귀

- **F-1** `[exact]` `[미검증]` 마커를 재정의하거나 동의어(`미확인`, `N/A`, `TBD`, `unverified`)를 만들지 않는다. 필요 시 `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol 정본 인용만.
- **F-2** `[exact]` `python3 scripts/validate-plugin.py reflect-kit` 8 카테고리 전부 OK.
- **F-3** `[exact]` 범위 밖 파일 변경 0건 (`git status --short` 로 확인). `git add/commit/tag/push` 실행 0회.
- **F-4** `[exact]` bare code fence 0건 (모든 fence 에 언어 태그).

## 비-목표

- fit-pal 레포 수정 — 범위 밖. 진단서만 존재.
- `~/.claude/logs/` 실제 로그 데이터 수정·삭제 — 읽기 전용.
- `harness/`, 다른 kit, orchestrator, marketplace.json, plugin.json 수정.
- 새 primary_category 신설 — `actionability` 1필드로 해결 (스키마 최소 확장).
- `docs/SCHEMA.md` §5 Project ID 포맷 staleness(v0.2.0 표기) 수정 — 별개 관심사, 리포트만.
