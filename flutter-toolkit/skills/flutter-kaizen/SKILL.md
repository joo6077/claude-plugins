---
name: flutter-kaizen
description: >
  Flutter 스킬을 학술 논문·공식 문서·커뮤니티 리서치·skills.sh 마켓플레이스
  기반으로 점진적으로 개선하는 카이젠 스킬.
  주 1회 cron 자동 실행, 이벤트 트리거(eval 실패 연속, 신규 스킬 추가),
  또는 수동 호출로 동작한다.
  "/flutter-kaizen", "플러터 카이젠", "flutter 개선" 요청에 사용.
  단순 버그 수정이나 기능 구현 요청에는 트리거하지 않는다.
argument-hint: "[skills|eval|guide]"
user-invocable: true
---

# Flutter Kaizen

flutter-toolkit 스킬을 최신 연구, Flutter 생태계 변화, 커뮤니티 스킬에 맞춰 점진적으로 개선한다.
연구 결과는 PR로 제출하여 사용자가 리뷰 후 머지한다.

## 이 스킬 폴더의 파일

필요할 때 읽어라:

- `references/search-sources.md` — 검색 소스 목록 + 신뢰도 기준
- `references/pr-template.md` — PR 본문 + changelog 엔트리 템플릿
- `scripts/trigger-check.sh` — 이벤트 트리거 감지 스크립트
- `templates/research-log-entry.md` — 연구 로그 엔트리 형식

## Gotchas

- WebFetch로 URL 접근 시 arXiv PDF 직접 접근은 실패할 수 있다. `arxiv.org/abs/` (abstract 페이지)를 사용해라
- Flutter/Dart 공식 문서는 버전별로 URL이 다를 수 있다. `api.flutter.dev`와 `dart.dev`의 stable 버전 URL을 사용해라
- skills.sh 검색 시 스킬의 SKILL.md 원문을 반드시 확인해라. 목록 페이지의 description만으로 판단하지 마라
- pub.dev 패키지 트렌드는 다운로드 수만으로 판단하지 마라. likes, pub points, popularity 점수를 함께 확인해라
- `release.sh`는 interactive prompt가 있다 (dirty check). 카이젠 브랜치에서는 커밋 후 실행해야 한다
- flutter-toolkit 스킬은 `references/project-detection.md`에 의존한다. 스킬 수정 시 detection 로직과의 정합성을 확인해라

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
| 스킬 프롬프트 | `flutter-toolkit/skills/*/SKILL.md` | `skills` |
| 스킬 참조 파일 | `flutter-toolkit/skills/*/references/` | `skills` |
| Eval | `flutter-toolkit/evals/` | `eval` |
| 프로젝트 감지 | `flutter-toolkit/references/project-detection.md` | `skills` |
| 아키텍처 | `flutter-toolkit/` 전체 구조, 훅, 스크립트 | `skills` |
| 스킬 설계 가이드 | `docs/skill-design-guide.md` | `guide` |
| 신규 스킬 생성 | 연구 기반 새 스킬 필요성 도출 → 초안 직접 생성 | `skills` |

`$ARGUMENTS`가 없으면 전체 영역을 스캔한다.

## 트리거 조건

### 주기적 (cron)
- **직접 cron 없음** — `kaizen-orchestrator`가 Phase 3에서 호출
- 독립 실행은 수동 호출로만

### 이벤트 트리거
`scripts/trigger-check.sh`를 실행하여 감지:
- flutter-toolkit eval 실패 2회 연속
- 신규 스킬 추가 후 첫 주

### 수동
- `/flutter-kaizen` — 전체
- `/flutter-kaizen skills` — 스킬만
- `/flutter-kaizen eval` — eval만
- `/flutter-kaizen guide` — 설계 가이드만

## Process

### Step 1: 상태 확인

1. `docs/kaizen/flutter-research-log.md`를 읽어 이전 연구 기록 확인
2. 이벤트 트리거 실행 시: 트리거 사유를 기록
3. 현재 flutter-toolkit 상태 스캔:
   - `flutter-toolkit/skills/` 내 모든 SKILL.md 목록 확인
   - `flutter-toolkit/evals/evals.json` 읽기
   - `flutter-toolkit/references/project-detection.md` 읽기
   - `docs/skill-design-guide.md` 읽기
   - `flutter-toolkit/.claude-plugin/plugin.json`에서 현재 버전 확인

### Step 2: COLLECT (수집)

`references/search-sources.md`를 읽고 소스별로 검색한다.

**검색 실행:**
1. **WebSearch**로 Flutter/Dart 관련 학술 논문 검색 — 키워드 조합 사용
2. **WebSearch**로 Flutter 공식 소스 changelog/blog 검색
3. **WebSearch**로 커뮤니티 소스 검색 (블로그, GitHub trending)
4. **WebFetch**로 skills.sh에서 Flutter/Dart 관련 스킬 검색 — 새로운 패턴이나 접근법 참고
5. 이전 flutter-research-log.md에 있는 URL은 건너뛴다 (업데이트 제외)

**각 검색 결과마다:**
- 제목, URL, 유형, 날짜를 기록
- flutter-toolkit 스킬 개선과 관련 있는지 1차 판단

### Step 3: VERIFY (검증)

수집한 각 소스에 대해 3중 검증 게이트를 실행한다.

**GATE 1:** URL이 있는가? → 없으면 폐기
**GATE 2:** WebFetch로 URL 접근 → 접근 불가면 폐기 → 내용이 주장과 일치하는지 확인 → 불일치면 폐기
**GATE 3:** 검증 통과한 소스만 다음 단계로

**태그 부착:**
- arXiv preprint → `[preprint]`
- 공식이 아닌 블로그 → `[blog]`
- 6개월 이상 → `[dated: YYYY-MM]`
- skills.sh 스킬 → `[skills.sh]`

### Step 4: ANALYZE (분석)

검증된 소스에서 추출한 인사이트와 현재 flutter-toolkit 스킬을 비교한다.

**기존 스킬 갭 분석:**
- 현재 스킬에 없는 Flutter 기법/패턴이 있는가?
- 현재 스킬의 접근법보다 나은 방법이 제시되었는가?
- skills.sh의 다른 Flutter 스킬에서 가져올 수 있는 패턴이 있는가?
- Flutter/Dart 생태계 변화(새 API, deprecated API)로 스킬 업데이트가 필요한가?
- 설계 가이드에 추가할 새 원칙이 있는가?

**신규 스킬 갭 분석:**
- 연구에서 발견한 워크플로우 중 현재 flutter-toolkit에 대응하는 스킬이 없는 것이 있는가?
- Flutter 생태계에서 반복되는 작업인데 아직 자동화되지 않은 것이 있는가?
- skills.sh나 커뮤니티에서 인기 있는 Flutter 스킬 유형 중 우리에게 없는 것이 있는가?
- `docs/skill-design-guide.md`의 9가지 아키타입 중 flutter-toolkit에 미충족된 유형이 있는가?

**신규 스킬 판단 기준:**
- 기존 스킬의 범위를 확장하는 것으로 충분한지 먼저 검토 — 별도 스킬이 꼭 필요한 경우만 생성
- skill-design-guide 원칙: "몇 줄의 지시문 + Gotchas 1개로 시작" — 완성도보다 초안 생성이 우선
- 이후 카이젠 실행에서 Gotchas가 쌓이면서 점진적으로 성장시킨다

**개선 포인트 도출:**
- 각 포인트에 영역(skill/eval/detection/architecture/guide/new-skill) 태그
- 영향도(높음/중간/낮음)와 리스크(높음/중간/낮음) 판단
- 출처 URL과 구체적 근거 매핑

**개선 포인트가 없으면:** flutter-research-log.md에 "개선 포인트 없음"으로 기록하고 종료.

### Step 5: PROPOSE + APPLY (제안 및 적용)

1. **브랜치 생성:**
   - 버전 결정: 개선 항목 중 가장 높은 bump 유형 선택
     - docs, Gotchas 추가, eval 미세 조정 → patch
     - 스킬 프롬프트 변경, eval 기준 변경, 새 reference 추가 → minor
     - 아키텍처 변경, 스킬 대폭 수정, breaking change → major
   - 새 버전 계산
   - 브랜치명: `flutter-kaizen/{새버전}-{YYYY-MM-DD}`

   ```bash
   git checkout -b flutter-kaizen/{새버전}-{YYYY-MM-DD}
   ```

2. **변경 적용:**
   - 각 개선 포인트에 해당하는 파일을 수정
   - 변경마다 커밋: `flutter-kaizen: {변경 설명}`

3. **신규 스킬 생성 (해당 시):**
   - ANALYZE에서 신규 스킬이 도출되었으면 이 단계에서 직접 생성한다
   - 초안 수준(v0.1)으로 생성 — skill-design-guide 원칙 "몇 줄의 지시문 + Gotchas 1개"
   - 생성 구조:
     ```
     flutter-toolkit/skills/{신규스킬명}/
     ├── SKILL.md          # frontmatter + Gotchas + 기본 Process
     └── references/       # 필요 시에만
     ```
   - frontmatter의 description에 트리거 키워드와 비트리거 조건 명시
   - 리서치에서 발견한 패턴/주의사항을 Gotchas에 반영
   - Process는 핵심 단계만 — 상세화는 이후 카이젠에서 점진적으로
   - evals.json에 해당 스킬의 eval 케이스 최소 1개 추가
   - 커밋: `flutter-kaizen: {스킬명} 스킬 초안 생성`

4. **버전 업데이트:**
   - `flutter-toolkit/.claude-plugin/plugin.json`의 version 필드 업데이트
   - `.claude-plugin/marketplace.json`의 description에서 `[vX.Y.Z · 날짜]` 업데이트
   - `docs/kaizen/flutter-changelog.md`에 엔트리 추가 (`references/pr-template.md`의 changelog 형식 따름)

5. **flutter-research-log.md 업데이트:**
   - `templates/research-log-entry.md` 형식으로 이번 연구 결과 기록

6. **README 업데이트:**
   - `flutter-toolkit/README.md`의 카이젠 섹션에 이번 개선 사항 반영

7. **PR 생성:**
   - `references/pr-template.md`를 읽고 해당 형식으로 PR 본문 작성
   - PR 제목: `[{bump유형}] flutter-toolkit: {핵심 변경 요약}`

   ```bash
   git push -u origin flutter-kaizen/{새버전}-{YYYY-MM-DD}
   gh pr create --title "[{bump}] flutter-toolkit: {요약}" --body "{pr-template.md 형식에 맞춘 본문}"
   ```

8. **git tag는 PR 머지 후** 사용자가 `/release`로 처리한다. 카이젠은 tag를 생성하지 않는다.

## 버전 판단 가이드

| 변경 영역 | bump | 예시 |
|-----------|------|------|
| docs, Gotchas 추가, eval 미세 조정 | **patch** | flutter-widget 스킬에 Gotcha 1개 추가 |
| 스킬 프롬프트 변경, eval 기준 변경, 새 reference | **minor** | flutter-api 스킬의 프로세스 단계 수정 |
| 신규 스킬 초안 생성 | **minor** | flutter-test 스킬 v0.1 생성 |
| 아키텍처 변경, 스킬 대폭 수정, breaking change | **major** | project-detection 로직 전면 교체 |

**혼합 변경 시:** 가장 높은 bump 유형을 따른다 (Gotcha patch + skill minor = minor).

## 추적 규칙

| 항목 | 규칙 | 예시 |
|------|------|------|
| 커밋 메시지 | `flutter-kaizen:` prefix | `flutter-kaizen: flutter-widget Gotchas에 const 생성자 주의사항 추가` |
| 브랜치명 | 버전 + 날짜 | `flutter-kaizen/0.4.0-2026-04-07` |
| PR 제목 | bump 유형 + 플러그인명 | `[minor] flutter-toolkit: widget 스킬 패턴 개선` |
