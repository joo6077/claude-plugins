# Reflect Digest — project=all (2026-06-27 ~ 2026-07-27, 30d)

대상 프로젝트: 2개 (fit-pal 747엔트리 / purchase-bot 13엔트리) · claude-plugins reflection 없음
총 엔트리: 760개 · 파싱 실패 6블록

## 요약
- primary_category: {'wrong_approach': 109, 'tool_failure': 479, 'repeated_error': 39, 'misunderstanding': 133}
- severity: {'medium': 402, 'low': 315, 'high': 43}
- 4축: scope={'project': 479, 'session': 261, 'global': 20} · risk={'medium': 453, 'low': 269, 'high': 38} · proc={'single_rule': 644, 'multi_step_procedure': 116} · enforce={'hard_gate': 205, 'soft_reminder': 555}

## ⚠️ 노이즈 경보 — hook-script 태그 파편화
- `missing-*-hook-script(s)` / `*-guard-hook` 계열 **54개 태그, 307엔트리 (40%)**
- 전부 '가드 훅이 없다'는 동일 의미인데 reflect Stop-hook 분석기가 mistake_tag 정규화를 못해 파편화 → 개별 빈도가 임계치 미달로 승격 실패.
- **근본 원인은 fit-pal `.claude/settings.json`이 미배포 훅 스크립트를 참조하는 단일 환경 오설정**이 매 툴콜마다 반복 로깅된 것. Claude 행동 신호 아님.
- **→ reflect-kaizen 신호**: Stop-hook 분석 프롬프트에 (1) tag canonicalization, (2) '없는 훅 추가' 반복 meta-제안 억제 규칙 필요.

## 행동 신호 클러스터 (hook-noise 제외, 태그 dedup)
| 클러스터 | 합산빈도 | usc | 매핑 |
|---|---:|:---:|---|
| API 문서 조회 스킵 (Context7/Codex) | 18 | ✅ | 글로벌 CLAUDE.md 기술최신화 (재위반) → hook 강화 |
| 최소변경 위반 / 스코프크립 (색상·보더·단일위젯·클라이언트) | 13 | ✅ | 가드레일 §2 (재위반) → CLAUDE.md/hook |
| 실앱/MCP 검증 우회 · 오버클레임 | 14 | ✅ | verification-before-completion (글로벌) + fit-pal MCP 규약 |
| harness sprint-contract 결함 | 5 | ✅ | **contract-kaizen (Phase 2)** |
| harness qa-evaluator/feedback 결함 | 4 | — | **evaluator/harness-kaizen (Phase 3/4)** |
| rust-kit 결함 | 2 | — | **rust-kaizen (Phase 9)** |
| flutter-toolkit 결함 | 1 | — | **flutter-kaizen (Phase 5)** |

## 승격 후보 (precedence — reflect-promote 대상, digest는 리포트만)
규칙 #0 fast-track (user_stated_constraint 재위반) 태그:
- `skipped-required-api-doc-check` (freq 9) → fast-track: project CLAUDE.md + hook 병기
- `missing-official-doc-lookup-for-external-api` (freq 2) → fast-track: project CLAUDE.md + hook 병기
- `not-actually-single-widget` (freq 2) → fast-track: project CLAUDE.md
- `ignored-local-app-deploy-instruction` (freq 2) → fast-track: project CLAUDE.md + hook 병기
- `preserve-original-colors` (freq 1) → fast-track: project CLAUDE.md
- `open-browser-request-treated-as-diagnosis` (freq 1) → fast-track: project CLAUDE.md
- `browser-approved-colors-ignored` (freq 1) → fast-track: project CLAUDE.md
- `ignored-visual-correction` (freq 1) → fast-track: project CLAUDE.md + hook 병기
- `research-before-edit-ignored` (freq 1) → fast-track: project CLAUDE.md + hook 병기
- `ignored-client-scope-after-correction` (freq 1) → fast-track: project CLAUDE.md + hook 병기
- `ignored-client-scope-expansion` (freq 1) → fast-track: project CLAUDE.md + hook 병기
- `single-widget-morph-violated` (freq 1) → fast-track: project CLAUDE.md + hook 병기

## 스킬 × 실수 교차 (hook-noise 제외 실제 결함)
- `flutter-toolkit:flutter-provider`: ignored-required-api-doc-lookup:1, mismatched-provider-skill:1, edit-before-read:1, invalid-lock-version-check:1
- `flutter-toolkit:flutter-widget`: scan-animation-direction-mismatch:1, preserve-original-colors:1, flutter-web-restart-failure:1, ignored-docs-research-requirement:1
- `flutter-toolkit:flutter-hooks`: false-positive-static-verification:1, skipped-required-api-doc-check:1, missing-harness-save-feedback-script:1, skipped-mandatory-skill-process:1
- `rust-kit:rust-test`: unavailable-sendmessage-tool:2, unreliable-exit-status-capture:1, bypass-run-guard-by-cwd:1, port-already-in-use:1
- `rust-kit:rust-service`: edit-before-read:1, external-api-doc-lookup-skipped:1, missing-official-doc-lookup-for-external-api:1, unreliable-piped-exit-code-capture:1
- `rust-kit:rust-api`: research-before-edit-ignored:1, cargo-test-wrong-target:1, distroless-builder-glibc-mismatch:1
- `harness:sprint-contract`: ignored-read-first-handoff:1, skipped-pre-edit-audit:1, ignored-project-commands:1, invalid-diff-oracle:1
- `rust-kit:rust-model`: wrong-line-doc-comment-fix:1, broken-pipeline-exit-capture:1
- `rust-kit:rust-middleware`: feedback-script-location-mismatch:1, feedback-schema-validation-failed:1, unsupported-git-status-option:1, wrong-infra-path-assumption:1
- `ship`: deploy-request-diverted-to-release-notes:1, write-before-read:1, deployment-request-treated-as-release-notes:1, unverified-release-version-assumption:1
- `superpowers:systematic-debugging`: catalog-opened-in-simulator:1, real-app-verification-required:1, unavailable-mobile-network-log-tool:1, zsh-unmatched-glob:1
- `sprint-contract`: complexity-by-file-count:1, cwd-contract-path-drift:1, write-without-read:1, config-command-mismatch:1