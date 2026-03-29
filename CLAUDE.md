# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Claude Code 플러그인 모노레포. 두 개의 플러그인을 포함한다:

- **harness** — 스택 무관 범용 QA 프레임워크 (Sprint Contract + QA Evaluator)
- **flutter-toolkit** — Flutter 전용 개발 워크플로우 스킬 15종

## Commands

```bash
# 플러그인 릴리스 (버전 bump + marketplace.json 갱신 + git commit/tag/push)
bash scripts/release.sh <plugin-name> <patch|minor|major>
# 예: bash scripts/release.sh harness patch

# harness 환경 검증
bash harness/scripts/env-check.sh

# flutter-toolkit evals
# evals.json (flutter-toolkit/evals/evals.json) 참조 — 15개 테스트 케이스
```

## Architecture

### Plugin Structure

각 플러그인은 동일한 레이아웃을 따른다:

```
<plugin>/
├── .claude-plugin/plugin.json   # 메타데이터 (name, version, author)
├── skills/<name>/SKILL.md       # 스킬 정의 (frontmatter + process)
├── agents/                      # 독립 에이전트 (harness만 해당)
├── hooks/                       # SessionStart/PreToolUse 훅
├── evals/                       # 테스트 픽스처 및 assertions
├── templates/                   # 초기화 템플릿
├── scripts/                     # 유틸리티 셸 스크립트
└── README.md
```

### Marketplace Registry

`.claude-plugin/marketplace.json`이 모든 플러그인을 등록한다. 릴리스 시 `scripts/release.sh`가 이 파일의 version과 description 날짜를 자동 갱신한다.

### Harness Core Flow

1. `/harness init` → `.harness/project.yaml` 생성
2. `/sprint-contract` → 구현 전 완료 조건 정의
3. 개발 수행
4. `qa-evaluator` 에이전트 → Contract 기준 APPROVE/REJECT 판정

`project.yaml`이 핵심 설정 파일: stack, commands, contract_categories, anti_patterns를 정의한다.

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
- 스킬 설계는 `docs/skill-design-guide.md`의 9가지 아키타입을 따른다
- Gotchas 섹션이 스킬에서 가장 중요한 부분 — Claude가 반복하는 실수를 방지한다
- harness evals는 `evals/test-fixtures/fixture-a~e` 디렉토리에 계약 시나리오별 테스트가 있다
- flutter-toolkit evals는 `evals/evals.json`에 15개 스킬별 assertion이 정의되어 있다
