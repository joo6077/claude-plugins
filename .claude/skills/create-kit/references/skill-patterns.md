# Kit Skill Patterns

모든 kit은 동일한 3스킬 + 1에이전트 패턴을 따른다. design-kit, backend-kit, infra-kit 모두 이 구조.

## 패턴 개요

```
{kit-name}/
├── .claude-plugin/plugin.json
├── skills/
│   ├── {kit-name}-guide/       ← 가벼운 리뷰·조언
│   ├── {kit-name}-audit/       ← 체계적 감사
│   └── {kit-name}-{system|init}/  ← 프로젝트 세팅
├── agents/
│   └── {kit-name}-reviewer.md  ← audit가 호출하는 독립 평가자
├── evals/
└── README.md
```

## 패턴 1: guide 스킬 (가벼운 리뷰)

**역할:** 개발 중 코드/설명에 대해 원칙 기반 가이드 제공. 가벼운 리뷰.

```yaml
---
name: {kit-name}-guide
description: >
  개발 중 {도메인} 코드/설명을 받아 관련 원칙을 참조하여 가이드한다.
  스택 무관 — 원칙과 이유만 설명하고 구현은 프로젝트에 맞게.
  "{키워드1}", "{키워드2}", "이것 괜찮아?" 같은 가벼운 리뷰 시 트리거.
  체계적 전수 검사에는 트리거하지 않는다 — {kit-name}-audit 사용.
argument-hint: "[file-path or description]"
user-invocable: true
---

# Gotchas
1. **스택별 코드 제시 금지** — 원칙만 설명, 특정 프레임워크 코드 금지
2. **주관적 피드백 금지** — 반드시 출처가 있는 원칙을 근거로
3. **카테고리 과잉 방지** — 맥락에 관련된 원칙만
4. **리서치 문서 없이 답변 금지** — principle-index.md 통해 문서 읽은 후 답변

# Process
## Step 1: 맥락 파악
| 카테고리 | 키워드 |
|----------|--------|
| {cat1}   | {kw}  |

## Step 2: 원칙 참조
references/principle-index.md에서 카테고리의 문서 경로 찾아 읽기

## Step 3: 가이드 제시
**원칙:** {이름}
**근거:** {설명 + 수치}
**권장:** {개선 방향}
> **출처:** [이름](URL)

# References
- references/principle-index.md
```

**references/principle-index.md:** 카테고리별 문서 경로 매핑 (상대경로)

## 패턴 2: audit 스킬 (체계적 감사)

**역할:** 파일/디렉토리 전체를 카테고리별 PASS/FAIL로 감사. reviewer 에이전트를 호출.

```yaml
---
name: {kit-name}-audit
description: >
  {도메인} 코드/설정을 원칙 기준으로 체계적으로 감사한다.
  카테고리별 PASS/FAIL 판정과 근거를 포함한 리포트를 생성한다.
  {kit-name}-reviewer 에이전트를 Agent 도구로 호출하여 독립 평가한다.
  "감사", "검수", "audit", "품질 검사" 같은 요청 시 트리거.
  {다른 도메인} 검사에는 트리거하지 않는다 — {다른 kit} 사용.
argument-hint: "<target-path>"
user-invocable: true
---

# Gotchas
1. **{다른 도메인} 평가 금지** — 이 kit 범위만
2. **{구체적 체크 강제 금지}** — 원칙만 강제
3. **{프로덕션/개발 구분}** — 상황에 맞게
4. **{보안/핵심 영역 생략 금지}**

# Process
## Step 1: 대상 범위 결정
- 파일 경로 → 해당 파일
- 디렉토리 → 하위 전체
- 미지정 → git diff 기준

## Step 2: reviewer 에이전트 호출
- subagent_type: {kit-name}-reviewer
- prompt: "다음 파일을 {도메인} 원칙 기준으로 평가하라: [목록]"

## Step 3: 리포트 생성
| 카테고리 | 판정 | 근거 |
|----------|------|------|
| Cat1 | PASS/FAIL | 파일:라인 + 원칙 |

## Step 4: 최종 판정
- 모든 PASS → **APPROVE**
- 1개 이상 FAIL → **REJECT** + 개선 사항

# References
- references/audit-criteria.md
```

**references/audit-criteria.md:** 카테고리별 PASS/FAIL 체크리스트 (기준 | PASS 조건 | 출처)

## 패턴 3: system/init 스킬 (프로젝트 세팅)

**역할:** 프로젝트에 해당 도메인의 기반을 세팅. 기존 설정 있으면 개선점 제안.

- **system 버전** (design-kit, backend-kit): 아키텍처/토큰 체계 세팅
- **init 버전** (infra-kit): 초기 인프라 세팅

```yaml
---
name: {kit-name}-{system|init}
description: >
  프로젝트에 {도메인} 기반을 세팅한다.
  기존이 있으면 리서치 기준과 비교하여 개선점 제안.
  "세팅", "init", "초기화" 같은 요청 시 트리거.
  단순 수정에는 트리거하지 않는다.
argument-hint: "[project-path]"
user-invocable: true
---

# Gotchas
1. **스택/벤더 강제 금지** — 기존 환경 먼저 감지
2. **기존 설정 덮어쓰기 금지** — 분석 후 개선점만
3. **과도한 복잡도 경고** — 프로젝트 규모 고려
4. **요청 범위 벗어나지 마라**

# Process
## Step 1: 프로젝트 감지
{도메인 관련 파일 탐색}

## Step 2: 카테고리별 세팅
references/{system-principles|init-checklist}.md 참조

## Step 3: 규격 문서 출력
각 카테고리:
1. 현재 상태 — 있으면 분석, 없으면 "미설정"
2. 권장 규격 — 리서치 기반
3. 개선 사항 — 차이점

# References
- references/{system-principles|init-checklist}.md
```

## 패턴 4: reviewer 에이전트

**역할:** audit 스킬이 호출하는 읽기 전용 독립 평가자.

```yaml
---
name: {kit-name}-reviewer
description: >
  {도메인} 코드/설정을 원칙 기준으로 독립 평가한다.
  {kit-name}-audit 스킬에서 Agent 도구로 위임받아 실행된다.
  카테고리별 PASS/FAIL 판정과 근거를 반환한다.
  단독 실행하지 않는다 — 반드시 {kit-name}-audit을 통해 호출.
tools: Read, Grep, Glob
model: sonnet
---

# {Kit-name} Reviewer

{도메인} 원칙 기준으로 평가하는 읽기 전용 에이전트.
코드를 수정하지 않는다. 결함을 찾는 것이 유일한 역할이다.

## 핵심 규칙
1. **{도메인} 원칙만 판정** — 다른 영역은 평가 대상 아님
2. **이진 판정** — PASS/FAIL만 존재, "부분적 준수" 없음
3. **근거 필수** — 모든 FAIL에 `파일:라인` + 출처(원칙명, URL)
4. **칭찬 금지** — 긍정 평가 없음
5. **1 FAIL = REJECT**

## 평가 카테고리
{N개 카테고리 순서대로}

### 1. {카테고리}
- {체크 항목}
- {체크 항목}

## 평가 기준 참조
- {kit-name}/skills/{kit-name}-audit/references/audit-criteria.md

## 출력 포맷
| 카테고리 | 판정 | 파일:라인 | 근거 | 출처 |
|----------|------|-----------|------|------|

**최종 판정:** APPROVE / REJECT
**FAIL 수:** N개
```

## 주요 규칙

1. **tools는 Read, Grep, Glob만** — reviewer는 읽기 전용
2. **model은 sonnet** — 분석에는 sonnet 충분, opus는 합성/판단에만
3. **description에 "단독 실행하지 않는다"** — audit 스킬이 호출해야만 동작
4. **평가 기준은 audit-criteria.md로 외부화** — 스킬과 에이전트가 같은 기준 공유

## 기존 kit 참고

- `design-kit/` — 최초 패턴
- `backend-kit/` — system 버전 + 12개 리서치 문서
- `infra-kit/` — init 버전 + 12개 리서치 문서
