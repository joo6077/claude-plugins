# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Claude Code 플러그인 모노레포. 세 개의 플러그인을 포함한다:

<!-- AUTO:summary -->
- **harness** — 스택 무관 범용 QA 프레임워크 (Sprint Contract + QA Evaluator)
- **flutter-toolkit** — Flutter 전용 개발 워크플로우 스킬 18종
- **design-kit** — 스택 무관 UI/UX 디자인 플러그인 (디자인 시스템 세팅 + 실시간 가이드 + 감사)
- **backend-kit** — 스택 무관 백엔드 개발 가이드, 감사, 아키텍처 세팅 플러그인
- **infra-kit** — 스택 무관 인프라/DevOps 가이드, 감사, 초기 세팅 플러그인
- **rust-kit** — Rust 전용 백엔드 개발 워크플로우 플러그인 — 프로젝트 스캐폴딩, API 생성, 모델 관리, 빌드/테스트/감사 자동화
- **react-kit** — React + Vite + Tauri 2 + Rust WASM 전용 개발 워크플로우 플러그인 — 21종 스킬 + 3 에이전트, 라이브러리 0개 애니메이션, Clean Architecture, Strict TypeScript 강제
- **planning-kit** — 스택 무관 제품 기획 플러그인 — 소크라테스식 질문, PRD, 우선순위, 리스크, 개념 데이터 모델(Mermaid), GitHub 프로젝트 동기화
- **reflect-kit** — 개인 Claude Code 사용자의 대화 피드백 → 학습 → 재주입 파이프라인 kit. Reflexion 방법론을 개인 레벨에 적용하여 세션 중 발생한 오해·반복 실수·잘못된 접근을 구조화 로그로 수집하고 빈도·위험도·절차성 기준으로 CLAUDE.md / memory / skill / hook에 승격한다.
- **bambu-kit** — Bambu Lab H2S용 자동 process+filament JSON 생성 — MakerWorld URL/모델 분석 → 소재 추천 → seam 전략 → Bambu Studio import 번들
- **onboarding-kit** — 스택 무관 외부 서비스 셋업 가이드 자동 생성 — 그 시점 최신 정보 기반 step-by-step 가이드 (Firebase, GCP, AWS, FCM, OAuth, Stripe 등)
- **tone-kit** — 스택 무관 코딩 톤·유지보수성 게이트 — 주석 경제성, 역할 기반 네이밍, 추출 임계치, 한국어 기술 문체, 템플릿 스캐폴딩, 파일 단위 정리 캠페인
- **api-kit** — 실제 응답을 SSOT로 삼는 블랙박스 API 계약 검증 킷 — 탐색 실행, 스냅샷 봉인, 계약 추출, 회귀 diff, 정적 뷰어
- **howto-kit** — 사람이 손으로 하는 절차를 어느 화면 → 어느 메뉴 → 어느 항목 → 무슨 값 → 어떻게 확인까지 끊지 않고 안내하는 스택·도메인 무관 킷
<!-- /AUTO:summary -->

## Commands

```bash
# 문서 동기화 (스킬/에이전트/설정 변경 후 README 갱신)
python scripts/sync-docs.py              # 전체 동기화
python scripts/sync-docs.py harness      # 특정 플러그인만
python scripts/sync-docs.py --check-only # 변경 필요 여부만 확인
python scripts/sync-docs.py --dry-run    # 미리보기

# 플러그인 릴리스 (버전 bump + marketplace.json 갱신 + git commit/tag/push)
bash scripts/release.sh <plugin-name> <patch|minor|major>
# 예: bash scripts/release.sh harness patch

# harness 환경 검증
bash harness/scripts/env-check.sh

# 피드백 시스템 테스트
bash harness/evals/kaizen/feedback-system/save-test.sh
bash harness/evals/kaizen/feedback-system/aggregation-test.sh

# 카이젠 수동 실행
# /kaizen — 전체 10 Phase 오케스트레이션 (설계 가이드 → contract → evaluator → harness → flutter → design → backend → infra → rust → react → Final)
# /contract-kaizen — sprint-contract만 개선
# /evaluator-kaizen — qa-evaluator만 개선

# flutter-toolkit evals
# evals.json (flutter-toolkit/evals/evals.json) 참조 — 19개 테스트 케이스

# 플러그인 검증 (8-카테고리 자동 검사)
python3 scripts/validate-plugin.py                          # 전체 킷
python3 scripts/validate-plugin.py react-kit                # 특정 킷
python3 scripts/validate-plugin.py --check=refs,placeholders # 특정 체크
python3 scripts/validate-plugin.py --fix                    # 자동 수정 (placeholders + code-fence 만)
# 가이드: harness/docs/guides/plugin-validation-guide.md
```

## Architecture

### Plugin Structure

각 플러그인은 동일한 레이아웃을 따른다:

```text
<plugin>/
├── .claude-plugin/plugin.json   # 메타데이터 (name, version, author)
├── skills/<name>/SKILL.md       # 스킬 정의 (frontmatter + process)
├── agents/                      # 독립 에이전트
├── hooks/                       # SessionStart/PreToolUse 훅 (선택)
├── evals/                       # 테스트 픽스처 및 assertions
├── references/                  # 공유 참조 문서 (선택, 스킬 내부에 둘 수도 있음)
├── templates/                   # 초기화 템플릿 (선택)
├── scripts/                     # 유틸리티 셸 스크립트 (선택)
└── README.md
```

### Marketplace Registry

`.claude-plugin/marketplace.json`이 모든 플러그인을 등록한다. 릴리스 시 `scripts/release.sh`가 이 파일의 version과 description 날짜를 자동 갱신한다.

### 문서 자동 동기화

`scripts/sync-docs.py`가 SKILL.md frontmatter, agents/*.md, plugin.json, hooks.json 등에서 데이터를 추출하여 README의 `<!-- AUTO:xxx -->` 마커 사이를 자동 갱신한다. PostToolUse 훅(`.claude/settings.json`)이 Edit/Write 후 `--check-only`를 실행하여 동기화 필요 시 알림한다.

### Harness Core Flow

1. `/harness init` → `.harness/project.yaml` 생성
2. `/sprint-contract` → 구현 전 완료 조건 정의
3. 개발 수행
4. `qa-evaluator` 에이전트 → Contract 기준 APPROVE/REJECT 판정
5. 자기진단 + 교차 진단 → 글로벌 피드백 저장 (`~/.harness/feedback/`)

`project.yaml`이 핵심 설정 파일: stack, commands, contract_categories, anti_patterns를 정의한다.

### Kaizen Orchestration

Phase 순서: 설계 가이드 → contract-kaizen → evaluator-kaizen → harness-kaizen → flutter-kaizen → design-kaizen → backend-kaizen → infra-kaizen → rust-kaizen → react-kaizen → … → tone-kaizen (Phase 15). 각 Phase는 자체 리서치를 수행하며 독립 서브에이전트로 실행한다. 전체 Phase 완료 후 Final 단계에서 교차 정합성 검증을 수행한다.

가이드 문서 (`harness/docs/guides/`): `skill-design-guide.md`, `agent-design-guide.md`, `contract-design-guide.md`, `qa-evaluation-guide.md`. 공유 참조 (`harness/references/`): `contract-schema.md` (계약 포맷), `feedback-schema.yaml` (피드백 스키마). 피드백 스크립트: `harness/scripts/feedback-path.sh`, `save-feedback.sh`, `verify-feedback.sh`, `trigger-check-common.sh`.

### Skill Format

모든 스킬은 `SKILL.md` 파일 하나로 구성된다:

```yaml
---
name: skill-name
description: >
  트리거 키워드 포함 설명
argument-hint: "[optional]"
user-invocable: true
---
```

본문에는 Gotchas(반복 실수 방지), Process(단계별 실행), References(참조 파일) 섹션이 있다.

### Flutter Toolkit Integration

flutter-toolkit 스킬들은 `references/project-detection.md`를 통해 프로젝트 환경을 자동 감지한다 (FVM 래퍼, 아키텍처 패턴, 의존성 등). harness의 `.harness/project.yaml`과 연동하여 commands와 anti_patterns를 공유한다.

## Skills Reference

킷별 스킬·에이전트 전체 목록은 각 킷의 `README.md` 를 본다 — `scripts/sync-docs.py` 가 SKILL.md frontmatter 에서 자동 생성·동기화하므로 그쪽이 SSOT 다. 이 파일에는 목록만 봐서는 읽히지 않는 설계 의도만 남긴다.

### 공통 패턴

- **guide / audit / system·init / test 4종** — backend-kit, infra-kit 의 기본 골격. design-kit 은 여기에 concept·reference·mockup·component 를 더해 8종이다
- **audit 은 전용 reviewer 에이전트를 호출한다** (`design-reviewer` `backend-reviewer` `infra-reviewer` `rust-reviewer` `react-reviewer` `api-reviewer` `howto-reviewer`). 읽기 전용 독립 평가이므로 단독 실행하지 않는다
- **run → build → preflight → audit 4단 빌드 체인** — flutter-toolkit, rust-kit, react-kit 공통. run 이 프리미티브, build 는 wrapper, preflight 가 pre-commit 게이트, audit 이 quick/deep 감사다
- **`<kit>-kaizen` / `<kit>-research`** — 전자는 스킬 품질 개선, 후자는 외부 1차 출처 폴링. 역할을 섞지 않는다

### 킷별 특이사항

- **harness** — `/sprint-contract` → 개발 → `qa-evaluator` 가 기본 사이클. 트리거 조건은 아래 "Harness 트리거 규칙" 참조
- **react-kit** — 애니메이션 **라이브러리 0개 원칙**. `/react-audit` 의 Library Policy 카테고리가 빌드 게이트로 강제한다
- **api-kit** — `pin` 은 값 고정이 아니라 **경로별 명시 assertion** 이다. 타입은 멀쩡한데 값만 망가진 회귀를 잡는다. 비교 기준선은 RFC 8785 JCS
- **howto-kit** — **G5(말단 액션)·G6(입도)이 이 킷의 존재 이유.** G3 는 대상 플랫폼을 선언하지 않으면 PASS 가 아니라 FAIL 이다. 출처 등급제(`관측`/`문서`/`추정`/`미확인`)가 "검증 불가 → 침묵" 을 대체한다
- **tone-kit** — 규칙 강도 3등급(MUST / SHOULD / 관측 컨벤션). 3축 레이어(스택 / 언어 / 프로젝트). 어댑터는 위반 실측이 있는 `dart-flutter` 하나만 채운다
- **bambu-kit** — 도구형 1스킬 킷이라 guide/audit/system 3종 패턴을 적용하지 않는다. H2S + AMS HT + AMS 2 Pro + Bambu Studio v2.6.0+ 환경 한정
- **reflect-kit** — 훅 3종(UserPromptSubmit / PostToolUseFailure / Stop)이 로그를 모으고 `/reflect-digest` → `/reflect-promote` 로 승격한다

`.claude/skills/` 의 이 레포 전용 카이젠·리서치 스킬은 세션 시작 시 자동으로 목록에 오르므로 여기 중복 기재하지 않는다.

## Key Conventions

- 모든 문서와 커밋 메시지는 한국어 사용
- 스킬 설계는 `harness/docs/guides/skill-design-guide.md`의 아키타입 카탈로그를 따른다
- Gotchas 섹션이 스킬에서 가장 중요한 부분 — Claude가 반복하는 실수를 방지한다
- harness evals는 `evals/test-fixtures/fixture-a~e` 디렉토리에 계약 시나리오별 테스트가 있다
- flutter-toolkit evals는 `evals/evals.json`에 19개 스킬별 assertion이 정의되어 있다

## Harness 트리거 규칙

이 레포에서 작업할 때 아래 키워드가 사용자 요청에 포함되면 harness의 sprint-contract 스킬 + qa-evaluator 에이전트 세트를 실행한다:

- **계약 키워드**: sprint-contract, sc, 계약, contract, 완료 조건, 스프린트, sprint, 조건 정의, 완료 기준, ㄱㅈ
- **QA 키워드**: qa, qa-evaluator, 검증, 평가, 판정, approve, reject, 검수, 품질 확인, 판정해줘, QA 돌려줘, QA 피드백
- **구현 키워드**: 구현해줘, 개발해줘, 기능 만들어줘, 화면 추가, 페이지 추가, 작업해줘, 착수, 코딩해줘, 기능 추가, 새 기능, feature, 리팩터링, refactor, API 연동, 엔드포인트 추가, 모듈 추가, 서비스 추가, ㄱㅎ, ㅊㄱ
- **조건부 키워드**: 만들어줘, 추가해줘, 생성해줘 — "기능"과 함께 나올 때만 트리거. 단독 사용 시 다른 스킬(create-skill, flutter-widget 등) 우선

실행 순서: `/sprint-contract` → 개발 → `qa-evaluator` 에이전트.
단순 수정(색상 변경, 오타 수정, 1파일 변경)에는 트리거하지 않는다.

원본 위치:
- 에이전트: `harness/agents/qa-evaluator.md`
- 스킬: `harness/skills/sprint-contract/SKILL.md`
- `.claude/`에 복사본을 두지 않는다 — harness 플러그인 원본만 사용

## Platform Gotchas (Windows)

- `python3`은 Windows Store 스텁일 수 있음 — `python3 -c "pass"`로 실제 동작 확인 후 사용. 안 되면 `python`으로 fallback
- Python에서 한국어 포함 파일 읽을 때 `encoding='utf-8'` 필수 (기본 cp949 에러)
- bash 스크립트에서 `sha256sum` 미설치 가능 — `python -c "import hashlib; ..."` 또는 `openssl dgst -sha256`으로 fallback
