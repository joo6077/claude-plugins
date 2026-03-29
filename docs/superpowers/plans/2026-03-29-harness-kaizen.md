# Harness Kaizen Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 학술 논문·공식 문서·커뮤니티 리서치 기반으로 하네스를 주기적·자동 개선하는 kaizen 스킬 구축

**Architecture:** 스킬 폴더(SKILL.md + references/ + scripts/ + templates/)와 산출물 디렉토리(docs/kaizen/)로 구성. 주기적 cron + 이벤트 트리거로 실행되며, 연구 → 검증 → 분석 → PR 생성 파이프라인을 따른다. 기존 release.sh를 활용해 semver 버전 관리를 자동화한다.

**Tech Stack:** Bash, Markdown, Claude Code schedule (remote trigger), gh CLI

**Spec:** `docs/superpowers/specs/2026-03-29-harness-kaizen-design.md`

---

## File Structure

```
harness/skills/harness-kaizen/        # 신규 생성
├── SKILL.md                          # 메인 지시문 + 파이프라인
├── references/
│   ├── search-sources.md             # 검색 소스 목록 + 신뢰도 기준
│   └── pr-template.md               # PR 본문 템플릿
├── scripts/
│   └── trigger-check.sh             # 이벤트 트리거 감지 스크립트
└── templates/
    └── research-log-entry.md         # 연구 로그 엔트리 템플릿

docs/kaizen/                          # 신규 생성
├── research-log.md                   # 누적 연구 기록
└── changelog.md                      # 카이젠 변경 이력
```

**기존 파일 수정 없음.** 모든 변경은 신규 파일 생성.

---

### Task 1: 산출물 디렉토리 초기화 (docs/kaizen/)

**Files:**
- Create: `docs/kaizen/research-log.md`
- Create: `docs/kaizen/changelog.md`

- [ ] **Step 1: research-log.md 생성**

```markdown
# Kaizen Research Log

> 매주 연구한 소스와 채택/폐기 여부를 기록한다.
> 다음 실행 시 이 로그를 참조하여 중복 연구를 방지한다.

---

<!-- 엔트리는 최신순으로 추가 -->
```

- [ ] **Step 2: changelog.md 생성**

```markdown
# Kaizen Changelog

> harness-kaizen 스킬이 적용한 모든 변경의 이력.
> 각 엔트리는 버전, 변경 유형, 연구 근거, Before/After를 포함한다.

---

<!-- 엔트리는 최신순으로 추가 -->
```

- [ ] **Step 3: 커밋**

```bash
git add docs/kaizen/research-log.md docs/kaizen/changelog.md
git commit -m "kaizen: docs/kaizen/ 산출물 디렉토리 초기화"
```

---

### Task 2: 참조 문서 — search-sources.md

**Files:**
- Create: `harness/skills/harness-kaizen/references/search-sources.md`

- [ ] **Step 1: search-sources.md 작성**

```markdown
# 검색 소스 및 신뢰도 기준

## 소스 분류

### 학술 논문
- **검색 대상:** arXiv, ACL Anthology, IEEE Xplore, Semantic Scholar
- **키워드:** LLM agent evaluation, prompt engineering, quality assurance, agentic workflow, tool use, multi-agent, code generation verification
- **범위:** 최근 6개월 우선, 핵심 논문은 기간 무관
- **후속:** 발견한 논문의 references 섹션에서 관련 논문 추적

### 공식 소스
- **Anthropic:** docs.anthropic.com changelog, anthropic.com/research, anthropic.com/engineering
- **OpenAI:** platform.openai.com/docs changelog, openai.com/research, cookbook
- **Google DeepMind:** deepmind.google/research, cloud.google.com/vertex-ai docs

### 커뮤니티/실무
- **GitHub:** trending repos — 키워드: agent, harness, prompt, evaluation, quality
- **블로그:** Simon Willison (simonwillison.net), Lilian Weng (lilianweng.github.io), Eugene Yan (eugeneyan.com)
- **컨퍼런스:** NeurIPS, ICLR, ACL, EMNLP — 최신 proceedings
- **Changelog 모니터링:** Anthropic, OpenAI, Google의 공식 블로그/docs 업데이트 추적

## 신뢰도 기준

| 유형 | 신뢰도 | 태그 | 비고 |
|------|--------|------|------|
| Peer-reviewed 논문 | 높음 | — | 가장 신뢰 |
| 공식 블로그/docs (Anthropic, OpenAI, Google) | 높음 | — | 최신성 높음 |
| arXiv preprint | 중간 | `[preprint]` | 미검증 논문 명시 필수 |
| 유명 엔지니어 블로그 | 중간 | `[blog]` | 실전 검증된 패턴 |
| GitHub trending | 중간 | `[community]` | 커뮤니티 검증 필요 |
| 일반 블로그/포럼 | 낮음 | `[unverified]` | 다른 소스로 교차 검증 필수 |

## 최신성 기준

- 6개월 이내: 최신으로 간주
- 6개월~1년: `[dated: YYYY-MM]` 태그 부착, 후속 연구 확인
- 1년 이상: 핵심 원칙이 아니면 폐기 검토

## 중복 방지

- 매 실행 시 `docs/kaizen/research-log.md`를 먼저 읽는다
- 이미 조사한 URL은 건너뛴다
- 단, 이전 소스의 업데이트(새 버전, 후속 논문, docs 변경)는 재조사한다
```

- [ ] **Step 2: 커밋**

```bash
git add harness/skills/harness-kaizen/references/search-sources.md
git commit -m "kaizen: 검색 소스 및 신뢰도 기준 문서 추가"
```

---

### Task 3: 참조 문서 — pr-template.md

**Files:**
- Create: `harness/skills/harness-kaizen/references/pr-template.md`

- [ ] **Step 1: pr-template.md 작성**

````markdown
# Kaizen PR 본문 템플릿

> SKILL.md에서 PR 생성 시 이 템플릿을 따른다.

## 템플릿

```markdown
## Research Summary
> 이번 주 연구에서 발견한 핵심 인사이트 정리

### 조사한 소스
- [제목](URL) `[유형]` — 핵심 요약 1-2줄
- [제목](URL) `[유형]` — 핵심 요약 1-2줄

### 핵심 발견
- 발견 1: 구체적 설명 + 출처 인용
- 발견 2: 구체적 설명 + 출처 인용

---

## Changes

### 1. [개선 항목명]

**영역:** config / skill-prompt / agent-logic / eval / architecture / design-guide
**버전 영향:** patch / minor / major

**Before:**
\```
현재 코드 또는 설정 (실제 스니펫)
\```

**After:**
\```
변경된 코드 또는 설정 (실제 스니펫)
\```

**왜 개선인가:**
- 장점: ...
- 단점/트레이드오프: ...
- 근거: [출처](URL)의 Section X에서 "인용문..."

---

## Impact Summary

| 항목 | 영향도 | 리스크 | 근거 |
|------|--------|--------|------|
| 변경1 | 높음/중간/낮음 | 높음/중간/낮음 | [출처](URL) |

---

## Version Bump

**유형:** patch / minor / major
**현재:** vX.Y.Z → **다음:** vX.Y.Z
**판단 근거:** (왜 이 bump 유형인지 1줄 설명)

---

## Source Reliability

| 출처 | 유형 | 신뢰도 | 최신성 |
|------|------|--------|--------|
| 논문 A | peer-reviewed | 높음 | 2026-02 |
| Blog B | 공식 | 높음 | 2026-03 |
| Blog C | 커뮤니티 | 중간 | 2025-11 `[dated]` |
```

## changelog.md 엔트리 형식

```markdown
## [X.Y.Z] - YYYY-MM-DD

### 변경 유형: patch/minor/major (영역)

### 연구 기반
- [제목](URL) — 핵심 인사이트 1줄

### 변경 내역
- **파일경로**: 변경 설명
  - Before: 이전 동작/값
  - After: 변경 후 동작/값
  - 근거: [출처](URL)

### 버전 판단 근거
> bump 유형 선택 이유 1줄
```
````

- [ ] **Step 2: 커밋**

```bash
git add harness/skills/harness-kaizen/references/pr-template.md
git commit -m "kaizen: PR 본문 및 changelog 엔트리 템플릿 추가"
```

---

### Task 4: 이벤트 트리거 감지 스크립트

**Files:**
- Create: `harness/skills/harness-kaizen/scripts/trigger-check.sh`

- [ ] **Step 1: trigger-check.sh 작성**

```bash
#!/usr/bin/env bash
# ── Kaizen Event Trigger Check ──
# Usage: bash trigger-check.sh <harness-dir>
# Exit codes:
#   0 = 트리거 발생 (stdout에 사유 출력)
#   1 = 트리거 없음
#   2 = 에러

set -eo pipefail

HARNESS_DIR="${1:-.harness}"
SKILLS_DIR="${2:-harness/skills}"
HISTORY_DIR="$HARNESS_DIR/history"

# ── 유틸리티 ──
trigger_found() {
  echo "TRIGGER: $1"
  exit 0
}

# ── Check 1: REJECT 2회 연속 ──
check_consecutive_rejects() {
  [ -d "$HISTORY_DIR" ] || return

  local reject_count=0
  # history 디렉토리에서 최근 2개 feedback 파일 확인
  local recent_feedbacks
  recent_feedbacks=$(find "$HISTORY_DIR" -name "*sprint-feedback*" -type f 2>/dev/null | sort -r | head -2)

  [ -z "$recent_feedbacks" ] && return

  while IFS= read -r file; do
    if grep -qi "Verdict:.*REJECT" "$file" 2>/dev/null; then
      reject_count=$((reject_count + 1))
    fi
  done <<< "$recent_feedbacks"

  # 현재 sprint-feedback.md도 확인
  if [ -f "$HARNESS_DIR/sprint-feedback.md" ]; then
    if grep -qi "Verdict:.*REJECT" "$HARNESS_DIR/sprint-feedback.md" 2>/dev/null; then
      reject_count=$((reject_count + 1))
    fi
  fi

  [ "$reject_count" -ge 2 ] && trigger_found "QA Evaluator REJECT ${reject_count}회 연속"
}

# ── Check 2: Anti-pattern 3회 이상 반복 ──
check_repeated_antipatterns() {
  [ -d "$HISTORY_DIR" ] || return

  local all_feedbacks
  all_feedbacks=$(find "$HISTORY_DIR" -name "*sprint-feedback*" -type f 2>/dev/null)
  [ -f "$HARNESS_DIR/sprint-feedback.md" ] && all_feedbacks="$all_feedbacks $HARNESS_DIR/sprint-feedback.md"

  [ -z "$all_feedbacks" ] && return

  # Anti-pattern ID 추출 후 3회 이상 반복된 것 찾기
  local repeated
  repeated=$(echo "$all_feedbacks" | xargs grep -h "AP-[0-9]*.*FAIL" 2>/dev/null \
    | grep -oP 'AP-\d+' \
    | sort | uniq -c | sort -rn \
    | awk '$1 >= 3 { print $2 " (" $1 "회)" }')

  [ -n "$repeated" ] && trigger_found "Anti-pattern 반복: $repeated"
}

# ── Check 3: 신규 스킬 추가 (7일 이내) ──
check_new_skills() {
  [ -d "$SKILLS_DIR" ] || return

  local new_skills
  new_skills=$(git log --diff-filter=A --name-only --since="7 days ago" -- "$SKILLS_DIR/*/SKILL.md" 2>/dev/null | grep "SKILL.md" || true)

  [ -n "$new_skills" ] && trigger_found "신규 스킬 추가: $new_skills"
}

# ── 실행 ──
check_consecutive_rejects
check_repeated_antipatterns
check_new_skills

# 트리거 없음
exit 1
```

- [ ] **Step 2: 실행 권한 부여**

```bash
chmod +x harness/skills/harness-kaizen/scripts/trigger-check.sh
```

- [ ] **Step 3: 스크립트 문법 검증**

Run: `bash -n harness/skills/harness-kaizen/scripts/trigger-check.sh`
Expected: 출력 없음 (문법 에러 없음)

- [ ] **Step 4: 커밋**

```bash
git add harness/skills/harness-kaizen/scripts/trigger-check.sh
git commit -m "kaizen: 이벤트 트리거 감지 스크립트 추가"
```

---

### Task 5: 연구 로그 엔트리 템플릿

**Files:**
- Create: `harness/skills/harness-kaizen/templates/research-log-entry.md`

- [ ] **Step 1: research-log-entry.md 작성**

```markdown
# 연구 로그 엔트리 템플릿

> SKILL.md에서 research-log.md에 엔트리 추가 시 이 형식을 따른다.

## 형식

```markdown
## YYYY-MM-DD

**트리거:** cron / event (사유) / manual (영역)

### 조사한 소스

| # | 제목 | URL | 유형 | 신뢰도 | 결과 |
|---|------|-----|------|--------|------|
| 1 | 제목 | URL | peer-reviewed/공식/blog/community | 높음/중간/낮음 | 채택/폐기 |

### 채택한 인사이트

- **인사이트 1:** 설명 — 적용 영역: config/skill/agent/eval/architecture/guide
- **인사이트 2:** 설명 — 적용 영역: ...

### 폐기 사유 (해당 시)

- **소스 N:** 폐기 사유 (URL 접근 불가 / 내용 불일치 / 신뢰도 부족 / 하네스 무관)

### PR

- PR URL 또는 "개선 포인트 없음"
```
```

- [ ] **Step 2: 커밋**

```bash
git add harness/skills/harness-kaizen/templates/research-log-entry.md
git commit -m "kaizen: 연구 로그 엔트리 템플릿 추가"
```

---

### Task 6: 메인 스킬 파일 — SKILL.md

**Files:**
- Create: `harness/skills/harness-kaizen/SKILL.md`

- [ ] **Step 1: SKILL.md 작성**

```markdown
---
name: harness-kaizen
description: >
  하네스 엔지니어링을 학술 논문·공식 문서·커뮤니티 리서치 기반으로
  점진적으로 개선하는 카이젠 스킬.
  주 1회 cron 자동 실행, 이벤트 트리거(REJECT 연속, anti-pattern 반복,
  신규 스킬 추가), 또는 수동 호출로 동작한다.
  "/harness-kaizen", "하네스 개선", "카이젠" 요청에 사용.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: "[config|skills|guide]"
user-invocable: true
---

# Harness Kaizen

하네스 프레임워크를 최신 연구와 실무 기법에 맞춰 점진적으로 개선한다.
연구 결과는 PR로 제출하여 사용자가 리뷰 후 머지한다.

## 이 스킬 폴더의 파일

필요할 때 읽어라:

- `references/search-sources.md` — 검색 소스 목록 + 신뢰도 기준
- `references/pr-template.md` — PR 본문 + changelog 엔트리 템플릿
- `scripts/trigger-check.sh` — 이벤트 트리거 감지 스크립트
- `templates/research-log-entry.md` — 연구 로그 엔트리 형식

## Gotchas

- WebFetch로 URL 접근 시 arXiv PDF 직접 접근은 실패할 수 있다. `arxiv.org/abs/` (abstract 페이지)를 사용해라
- GitHub trending은 페이지 구조가 자주 바뀐다. WebSearch로 "github trending {키워드}"를 검색하는 게 더 안정적이다
- Anthropic docs changelog는 단일 URL이 없을 수 있다. WebSearch로 "anthropic docs changelog site:docs.anthropic.com" 검색해라
- 논문 제목만으로 검색하면 동명 논문이 나올 수 있다. 반드시 저자명 또는 arXiv ID를 함께 확인해라
- `release.sh`는 interactive prompt가 있다 (dirty check). 카이젠 브랜치에서는 커밋 후 실행해야 한다

## 핵심 제약: 할루시네이션 절대 불가

**출처 없는 주장은 어떤 경우에도 반영하지 않는다.**

3중 검증 게이트를 반드시 통과해야 한다:
1. **GATE 1 — 출처 존재:** 모든 주장에 URL 필수. 없으면 즉시 폐기
2. **GATE 2 — 출처 접근:** WebFetch로 URL 접근 + 내용이 주장과 일치하는지 확인. 실패 시 폐기
3. **GATE 3 — 증거 첨부:** PR에 출처 URL + 인용 원문 포함. 사용자가 원문 대조 가능해야 함

**추가 안전장치:**
- arXiv preprint → `[preprint]` 태그
- 블로그 → 작성자 신뢰도 표기 (공식 vs 개인)
- 6개월 이상 된 정보 → `[dated: YYYY-MM]` 태그

**이 게이트를 우회하고 싶은 생각이 들면 멈춰라:**
- "이건 널리 알려진 사실이니 출처 없어도 된다" → 아니다. 출처를 찾아라
- "URL은 안 되지만 내용은 맞다" → 검증 불가능하면 폐기다
- "비슷한 내용의 다른 출처가 있으니 괜찮다" → 그 다른 출처를 사용해라

## 개선 대상 범위

| 영역 | 대상 | 인수 필터 |
|------|------|-----------|
| 하네스 설정 | `.harness/project.yaml`, `procedures/` | `config` |
| 스킬 프롬프트 | `harness/skills/*/SKILL.md` | `skills` |
| 에이전트 로직 | `harness/agents/qa-evaluator.md` | `skills` |
| Eval | `harness/evals/` | `skills` |
| 아키텍처 | `harness/` 전체 구조, 훅, 스크립트 | `config` |
| 설계 가이드 | `docs/skill-design-guide.md` | `guide` |

`$ARGUMENTS`가 없으면 전체 영역을 스캔한다.

## 트리거 조건

### 주기적 (cron)
- 매주 월요일 09:00 KST
- Claude Code schedule (remote trigger) 사용

### 이벤트 트리거
`scripts/trigger-check.sh`를 실행하여 감지:
- QA Evaluator REJECT 2회 연속
- 같은 anti-pattern 3회 이상 반복
- 신규 스킬 추가 후 첫 주

### 수동
- `/harness-kaizen` — 전체
- `/harness-kaizen config` — 설정만
- `/harness-kaizen skills` — 스킬만
- `/harness-kaizen guide` — 설계 가이드만

## Process

### Step 1: 상태 확인

1. `docs/kaizen/research-log.md`를 읽어 이전 연구 기록 확인
2. 이벤트 트리거 실행 시: 트리거 사유를 기록
3. 현재 하네스 상태 스캔:
   - `.harness/project.yaml` 읽기
   - `harness/skills/` 내 모든 SKILL.md 목록 확인
   - `harness/agents/qa-evaluator.md` 읽기
   - `docs/skill-design-guide.md` 읽기
   - `harness/.claude-plugin/plugin.json`에서 현재 버전 확인

### Step 2: COLLECT (수집)

`references/search-sources.md`를 읽고 소스별로 검색한다.

**검색 실행:**
1. **WebSearch**로 학술 논문 검색 — 키워드 조합 사용
2. **WebSearch**로 공식 소스 changelog/blog 검색
3. **WebSearch**로 커뮤니티 소스 검색
4. 이전 research-log.md에 있는 URL은 건너뛴다 (업데이트 제외)

**각 검색 결과마다:**
- 제목, URL, 유형, 날짜를 기록
- 하네스 개선과 관련 있는지 1차 판단

### Step 3: VERIFY (검증)

수집한 각 소스에 대해 3중 검증 게이트를 실행한다.

**GATE 1:** URL이 있는가? → 없으면 폐기
**GATE 2:** WebFetch로 URL 접근 → 접근 불가면 폐기 → 내용이 주장과 일치하는지 확인 → 불일치면 폐기
**GATE 3:** 검증 통과한 소스만 다음 단계로

**태그 부착:**
- arXiv preprint → `[preprint]`
- 공식이 아닌 블로그 → `[blog]`
- 6개월 이상 → `[dated: YYYY-MM]`

### Step 4: ANALYZE (분석)

검증된 소스에서 추출한 인사이트와 현재 하네스 상태를 비교한다.

**갭 분석:**
- 현재 하네스에 없는 기법/패턴이 있는가?
- 현재 방식보다 나은 접근법이 제시되었는가?
- 설계 가이드에 추가할 새 원칙이 있는가?

**개선 포인트 도출:**
- 각 포인트에 영역(config/skill/agent/eval/architecture/guide) 태그
- 영향도(높음/중간/낮음)와 리스크(높음/중간/낮음) 판단
- 출처 URL과 구체적 근거 매핑

**개선 포인트가 없으면:** research-log.md에 "개선 포인트 없음"으로 기록하고 종료.

### Step 5: PROPOSE + APPLY (제안 및 적용)

1. **브랜치 생성:**
   - 버전 결정: 개선 항목 중 가장 높은 bump 유형 선택
     - docs, config 튜닝, Gotchas 추가 → patch
     - 스킬 프롬프트 변경, eval 기준 변경, 새 procedure → minor
     - 아키텍처 변경, 에이전트 로직 대폭 수정 → major
   - 새 버전 계산
   - 브랜치명: `kaizen/{새버전}-{YYYY-MM-DD}`

```bash
git checkout -b kaizen/{새버전}-{YYYY-MM-DD}
```

2. **변경 적용:**
   - 각 개선 포인트에 해당하는 파일을 수정
   - 변경마다 커밋: `kaizen: {변경 설명}`

3. **버전 업데이트:**
   - `harness/.claude-plugin/plugin.json`의 version 필드 업데이트
   - `.claude-plugin/marketplace.json`의 description에서 `[vX.Y.Z · 날짜]` 업데이트
   - `docs/kaizen/changelog.md`에 엔트리 추가 (`references/pr-template.md`의 changelog 형식 따름)

4. **research-log.md 업데이트:**
   - `templates/research-log-entry.md` 형식으로 이번 연구 결과 기록

5. **PR 생성:**
   - `references/pr-template.md`를 읽고 해당 형식으로 PR 본문 작성
   - PR 제목: `[{bump유형}] {핵심 변경 요약}`

```bash
git push -u origin kaizen/{새버전}-{YYYY-MM-DD}
gh pr create --title "[{bump}] {요약}" --body "$(cat <<'EOF'
{pr-template.md 형식에 맞춘 본문}
EOF
)"
```

6. **git tag는 PR 머지 후** 사용자가 `/release`로 처리한다. 카이젠은 tag를 생성하지 않는다.

## 버전 판단 가이드

| 변경 영역 | bump | 예시 |
|-----------|------|------|
| docs, config 튜닝, anti-pattern 추가, Gotchas 추가 | **patch** | project.yaml에 anti-pattern 1개 추가 |
| 스킬 프롬프트 변경, eval 기준 변경, 새 procedure 추가 | **minor** | sprint-contract 스킬의 프로세스 단계 수정 |
| 아키텍처 변경, 에이전트 로직 대폭 수정, breaking change | **major** | qa-evaluator 평가 방식 전면 교체 |

**혼합 변경 시:** 가장 높은 bump 유형을 따른다 (config patch + skill minor = minor).

## 추적 규칙

| 항목 | 규칙 | 예시 |
|------|------|------|
| 커밋 메시지 | `kaizen:` prefix | `kaizen: sprint-contract few-shot 판단 로직 추가` |
| 브랜치명 | 버전 + 날짜 | `kaizen/0.4.0-2026-04-07` |
| PR 제목 | bump 유형 명시 | `[minor] sprint-contract 복잡도 판단 개선` |
```

- [ ] **Step 2: 커밋**

```bash
git add harness/skills/harness-kaizen/SKILL.md
git commit -m "kaizen: 메인 스킬 파일 (SKILL.md) 추가"
```

---

### Task 7: cron 스케줄 설정

**Files:** 없음 (Claude Code schedule 명령 실행)

- [ ] **Step 1: 주간 스케줄 등록**

Claude Code의 `/schedule` 기능을 사용하여 등록한다:

```
Schedule name: harness-kaizen-weekly
Cron: 0 0 * * 1   (매주 월요일 00:00 UTC = 09:00 KST)
Prompt: /harness-kaizen
Project: C:\Users\khjoo\Desktop\Developments\01_Work\claude-plugins
```

- [ ] **Step 2: 등록 확인**

스케줄이 정상 등록되었는지 확인한다.

---

### Task 8: 통합 테스트 — 수동 dry-run

**Files:** 없음 (검증만 수행)

- [ ] **Step 1: 스킬 파일 구조 검증**

```bash
# 모든 파일이 올바른 위치에 있는지 확인
ls -la harness/skills/harness-kaizen/SKILL.md
ls -la harness/skills/harness-kaizen/references/search-sources.md
ls -la harness/skills/harness-kaizen/references/pr-template.md
ls -la harness/skills/harness-kaizen/scripts/trigger-check.sh
ls -la harness/skills/harness-kaizen/templates/research-log-entry.md
ls -la docs/kaizen/research-log.md
ls -la docs/kaizen/changelog.md
```

Expected: 7개 파일 모두 존재

- [ ] **Step 2: SKILL.md frontmatter 검증**

SKILL.md의 frontmatter가 올바른 YAML인지 확인:
- `name: harness-kaizen` 존재
- `description:` 트리거 조건 포함
- `user-invocable: true` 존재

- [ ] **Step 3: trigger-check.sh 실행 테스트**

```bash
# 트리거 없는 상태에서 exit 1이 나오는지 확인
bash harness/skills/harness-kaizen/scripts/trigger-check.sh .harness harness/skills
echo "Exit code: $?"
```

Expected: exit code 1 (트리거 없음)

- [ ] **Step 4: /harness-kaizen 수동 실행 테스트**

`/harness-kaizen`을 실행하여:
1. Step 1 (상태 확인)이 정상 동작하는지
2. Step 2 (COLLECT)에서 WebSearch가 결과를 반환하는지
3. Step 3 (VERIFY)에서 3중 게이트가 작동하는지
4. 전체 파이프라인이 끝까지 실행되는지

확인 후 이슈가 있으면 SKILL.md의 Gotchas에 추가한다.

- [ ] **Step 5: 최종 커밋**

dry-run에서 발견된 수정사항이 있으면 커밋:

```bash
git add -A harness/skills/harness-kaizen/
git commit -m "kaizen: dry-run 피드백 반영"
```
