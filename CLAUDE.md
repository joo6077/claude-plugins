# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Claude Code 플러그인 모노레포. 세 개의 플러그인을 포함한다:

<!-- AUTO:summary -->
- **harness** — 스택 무관 범용 QA 프레임워크 (Sprint Contract + QA Evaluator)
- **flutter-toolkit** — Flutter 전용 개발 워크플로우 스킬 18종
- **design-kit** — 스택 무관 UI/UX 디자인 플러그인 (디자인 시스템 세팅 + 실시간 가이드 + 감사)
<!-- /AUTO:summary -->

## Commands

```bash
# 플러그인 릴리스 (버전 bump + marketplace.json 갱신 + git commit/tag/push)
bash scripts/release.sh <plugin-name> <patch|minor|major>
# 예: bash scripts/release.sh harness patch

# harness 환경 검증
bash harness/scripts/env-check.sh

# 피드백 시스템 테스트
bash harness/evals/kaizen/feedback-system/save-test.sh
bash harness/evals/kaizen/feedback-system/aggregation-test.sh

# 카이젠 수동 실행
# /kaizen — 전체 6 Phase 오케스트레이션
# /contract-kaizen — sprint-contract만 개선
# /evaluator-kaizen — qa-evaluator만 개선

# flutter-toolkit evals
# evals.json (flutter-toolkit/evals/evals.json) 참조 — 19개 테스트 케이스
```

## Architecture

### Plugin Structure

각 플러그인은 동일한 레이아웃을 따른다:

```
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

### Harness Core Flow

1. `/harness init` → `.harness/project.yaml` 생성
2. `/sprint-contract` → 구현 전 완료 조건 정의
3. 개발 수행
4. `qa-evaluator` 에이전트 → Contract 기준 APPROVE/REJECT 판정
5. 자기진단 + 교차 진단 → 글로벌 피드백 저장 (`~/.harness/feedback/`)

`project.yaml`이 핵심 설정 파일: stack, commands, contract_categories, anti_patterns를 정의한다.

### Kaizen Orchestration

6 Phase 순서: 설계 가이드 → contract-kaizen → evaluator-kaizen → harness-kaizen → flutter-kaizen → design-kaizen. 각 Phase는 자체 리서치를 수행하며 독립 서브에이전트로 실행한다.

가이드 문서 (`docs/guides/`): `skill-design-guide.md`, `agent-design-guide.md`, `contract-design-guide.md`, `qa-evaluation-guide.md`. 공유 참조 (`harness/references/`): `contract-schema.md` (계약 포맷), `feedback-schema.yaml` (피드백 스키마). 피드백 스크립트: `harness/scripts/feedback-path.sh`, `save-feedback.sh`, `verify-feedback.sh`, `trigger-check-common.sh`.

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

## Key Conventions

- 모든 문서와 커밋 메시지는 한국어 사용
- 스킬 설계는 `docs/guides/skill-design-guide.md`의 9가지 아키타입을 따른다
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
