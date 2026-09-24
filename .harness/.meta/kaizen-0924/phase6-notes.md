# 카이젠 2026-09-24 Phase 6 (design-kit) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p06-design-kit.md` (조건 30 · 기능 조건 20, 봉인 `sha256:2e3e2f264632e340` · `locked_at` 2026-09-25 06:16)
- 개정: `.harness/sprint-amendments-kaizen-0924-p06-design-kit.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase6-review.md` (1 회차 CHANGES 막는 이유 다섯 · 막지 않는 것 일곱은 초안이 반영, 2 회차 APPROVE 「봉인 전에 넣을 것」 셋은 BUILD 가 봉인 전에 반영)
- 시작 커밋 `79258900de00e621412e4c436b44028a77d7fb64`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T061814-de8c7935-31187.yaml` (`verify-feedback.sh` PASS). 초안은 `.harness/feedback-draft-p06.yaml` 로 갈라 썼다

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `57f1020` | 봉인 커밋 | 계약 1 개 |
| `7b4618c` | 규약 §0 · §2 · §3 · §4, 생성 스킬 넷 · 감사 셋 소비 쪽, 시안 개수 정합, 사실 정정, 평가 사례 | `design-kit/` 열셋 |
| `903c903` | 개정 파일에 `end_sha` (`7b4618c`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p06-design-kit` 줄이 있다. 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 내 경로만 실었다.
**FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

구현은 개선안 모의 편집(스크래치 `p6b/mock.py`, sha256 앞 16 자리 `aed436d274a907a1`)을 작업 폴더에 그대로 돌렸다 — `mock applied`, 13 파일 · 더한 줄 212 · 지운 줄 30.
`p6b/mock.py` 는 2 회차 검토의 `p6r2/mock-alt.py` 를 그대로 복사한 것이다(초안 `p6d/mock.py` 와 evals id 28 프롬프트 한 줄만 다르다).
30 조건 측정은 봉인 커밋 판 계약에서 뗀 도우미로 돌렸다 — 스크래치 `p6b/extract.sh`(계약 `회귀 게이트` 절 awk 그대로) → `p6b/k/`, `p6b/run.sh`(`TMPDIR` 를 스크래치로 두고 bash 5.3.9 로 `run_all` · `DG05` · `DG06`).
도우미 다섯의 지문이 AR-01 ② 와 같다. QA 가 같은 묶음을 다시 돌릴 수 있다.

## 바꾼 파일

- `design-kit/references/visual-change-protocol.md` — 머리의 적용 스킬 목록에 design-component · design-concept, 형제 규약 숫자 문단과 세 규약 정본 결정 한 줄,
  `## 0. 편집 전 확정 — 대상 · 되말하기 · 관례 표` 신설(대상은 화면 자체 · 두 갈래면 묻기 · 같은 역할 기존 화면 2 개 이상 · 관례 표 네 칸 · 코드 검색에 없는 부품 이름 금지 ·
  같은 역할에만 · `관례 없음` 두 경우), §2 요소 하나 지목과 Change Manifest 틀 보존 줄의 이웃 요소, §3 `### 비교 반복 순서 — 반영 확인과 스스로 고치기 상한` ·
  `### 캡처 점검 목록`, §4 승인 기록 `확정 구성` · `폐기한 대안·이유` 칸과 규칙 두 줄
- `design-kit/skills/design-mockup/SKILL.md` — Step 1 대상 · 되말하기, Step 2 승인 기록 · 관례 표 로드, Step 5 요소 하나 지목 · 틀 보존 줄 · §3 인용, Step 6 틀 두 칸과 확인 명령,
  Gotcha 10 크기 쿼리 지원 문장
- `design-kit/skills/design-mockup/references/mockup-guidelines.md` — 개수는 Step 3-a 를 가리키고 숫자를 다시 적지 않음, 44×44 CSS px(AAA) · AA 24×24 · Apple HIG 44pt 구분
- `design-kit/skills/design-component/SKILL.md` — Step 0 재사용 부품 칸 세 문장
- `design-kit/skills/design-guide/SKILL.md` — Step 1 토큰 · 기존 컴포넌트 탐색과 §0 관례 표 근거, 「법적 표준」 정정
- `design-kit/skills/design-concept/SKILL.md` — Step 0 컨셉 승인 기록 로드와 폐기 안 재제안 금지, Step 7 폐기 칸과 확인 명령
- `design-kit/skills/design-audit/SKILL.md` — Step 2 Authenticity 칸, Gotcha 12 캡처 점검 목록 인용, Color · Layout 행 사실 정정
- `design-kit/skills/design-audit/references/audit-criteria.md` — Authenticity `같은 역할 관례 일치` 행, WCAG 2.2 절 제목 게시일, 법적 의무 단정 제거, `size` 쿼리, 375px 는 킷 판정값
- `design-kit/agents/design-reviewer.md` — Authenticity 같은 역할 관례 항목(모자라면 규칙 7 의 말), 규칙 9 캡처 점검 목록 인용
- `design-kit/skills/design-test/SKILL.md` — 「법적 기준」 정정
- `design-kit/skills/design-system/SKILL.md` — Gotcha 8 이름 금지 문자, Gotcha 12 Tailwind v4 발표일 · 최신판, Gotcha 14 `$schema`, Step 5 Style Dictionary v5 · Node.js 22 · v5.5.5
- `design-kit/skills/design-system/references/token-principles.md` — DTCG 2025.10 최소 예시(color · dimension 객체, `$schema` 제거)와 주의 사항
- `design-kit/evals/evals.json` — id 19 기대값 3 개, id 25 승인 기록 칸 한 줄, id 28 · 29 · 30 신설 (27 → 30 사례)

스킬 · 에이전트 frontmatter 는 그대로다(AP-04 · SK-09 `keep`). design-kit README 의 AUTO 구간은 frontmatter 를 읽으므로 `sync-docs.py design-kit --check-only` 는 「동기화됨」.

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `F01` | 규약 §0 대상(화면 자체) · 되말하기, design-mockup Step 1 (SK-01 · SK-05). 리액트 규약 쪽은 Phase 10 |
| `F04` | 규약 §3 캡처 점검 목록 · 글자 키운 캡처 · 넘침을 데이터로 재현하지 않기, 감사 두 자리 인용 (SK-03 · SK-07) |
| `design:P1` | 규약 §0 관례 표, design-mockup Step 2 · design-component Step 0 · design-guide Step 1 (SK-01 · SK-05). 대조 화면 수는 2 개 이상(결정 1) |
| `design:P2` | 부분 반영 — 규칙 방향(미지정 3 · 지정 N · 승인 상한 5)은 그대로, 어긋난 두 자리(`mockup-guidelines.md` 「5개 시안」 · evals id 19 「정확히 5개」)만 맞춤 (SK-09) |
| `design:P3` | 규약 §0 · §2 요소 하나 지목, Change Manifest 틀 보존 줄의 이웃 요소, design-mockup Step 1 · Step 5 (SK-01 · SK-05) |
| `design:P4` | 캡처 점검 목록은 규약에만 정의하고 design-audit Gotcha 12 · design-reviewer 규칙 9 는 인용만 (SK-03 · SK-07 · RE-01) |
| `design:P5` | 승인 기록 `확정 구성` · `폐기한 대안·이유` 칸, design-mockup Step 2 · design-concept Step 0 이 읽어 다시 넣지 않음 (SK-04 · SK-06). 제품 수준 폐기 결정은 경로만(결정 3) |
| `design:P6` | 규약 §3 비교 반복 순서 · 반영 확인 표식 · 스스로 고치기 최대 3 회 (SK-02 · SK-08) |
| `design:P7` | 감사 기준 Authenticity `같은 역할 관례 일치` 행, design-audit · design-reviewer (SK-07 · ER-03). 모자라면 규칙 7 의 「대상 코드에 해당 요소 부재」(결정 4) |
| 러닝북 Phase 6 | flutter 규약과 숫자 정합(2 개 이상 · 3 회) · 세 규약 정본을 harness `skill-design-guide.md` 한 절에 둔다는 결정 한 줄 (SK-08) |

그 밖에 받은 것 — 근거 파일 §3 · §4-9 · §4-10 현행화(DTCG 2025.10 예시 · Style Dictionary v5 · Tailwind v4 날짜 · WCAG 2.2 게시일 · 크기 쿼리 · 375px · 44×44), 카이젠 스킬 Step 4(evals).

## 미반영 키와 사유

- `design:P2 방향` — 사용자 확인 목록으로 넘긴다. 한 프로젝트 기억(「여러 개 다 만들어 나란히」 · 「시안 추가는 승인 대기 말고 바로 구현」)이 design-mockup 개수 계약 · 매트릭스 사전 합의와 반대 방향이다. 규칙 방향을 바꿀지는 사용자가 정한다
- `F20` — 제품 수준 폐기 결정 자리는 Phase 11 이 정한다. 정해지면 design-kit 승인 기록 폐기 칸이 그 경로를 적는다(규약 §4 규칙 둘째 줄)
- `UNVERIFIED_ENV` — design-audit · design-reviewer 가 옮겨 둔 미검증 정본이 2026-08-13 개정 전 판이다(`design-reviewer.md` 의 `UNVERIFIED_ENV` 0 건, backend-reviewer 7 건 · backend-audit 3 건). 판정 규칙(REJECT 문턱)을 바꾸는 별도 관심사라 다음 사이클 Phase 6 으로. 바꿀 자리 다섯: design-reviewer 규칙 8 · 최종 판정, design-audit Gotcha 11 · Step 4 · Step 5, evals id 21
- `design-mockup Step 0` — 형제 스킬 셋은 `## Step 0: 자동 감지 및 로드` 인데 design-mockup 만 `## Step 2` 다. 옮기면 Gotcha 13 의 「Step 6」 · evals 가 함께 바뀐다. 다음 사이클 Phase 6
- `§3.7 네 칸` — skill-design-guide §3.7 의 `[미검증]` 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 규약 §3 「캡처 실패 → `[미검증]`」 줄과 design-reviewer 의 접미 없는 `[미검증]` 15 줄에 붙이는 일. Phase 1 이 agent 가이드 §10 을 `[미검증:ENV]` · `[미검증:INVALID]` 분류로 다시 쓴 것도 같은 일이라 `UNVERIFIED_ENV` 와 함께 다음 사이클 Phase 6
- `Material 3` — 근거 파일 §5 에서 조회하지 않은 Material 3 Expressive · Apple HIG 2026. 다음 사이클 근거 파일 조회 목록에 넣는다

## 넘기는 것 (명시적 미완)

| 대상 | 누가 | 할 일 |
| --- | --- | --- |
| `harness/docs/guides/skill-design-guide.md` | 다음 사이클 Phase 1 | 세 규약(design-kit visual-change-protocol · flutter-toolkit visual-evidence-protocol · react-kit render-evidence-protocol)이 같이 쓰는 규칙의 정본 절 신설(계약 결정 2). 그 절이 생기면 design-kit 규약 머리의 「그 절은 아직 없다」 줄을 그 절 인용으로 바꾼다 |
| `flutter-toolkit/references/visual-evidence-protocol.md` | 다음 사이클 Phase 5 | 위 정본 절을 가리키고 스택 몫(채널 · 도구 · 명령)만 남긴다. 숫자(2 개 이상 · 3 회)는 이번에 design-kit 쪽을 맞췄다 |
| `react-kit/references/render-evidence-protocol.md` | Phase 10 | 리액트 규약에 되말하기 · 관례 표 · 반영 확인 · 캡처 점검 · 3 회 상한이 없다(F01 · F03 리액트 쪽). 다음 사이클엔 정본 절 인용 |
| `design-kit/README.md` 의 ``버전: `0.1.0` `` | Final | plugin.json 은 `0.4.0` 이다. 버전 줄을 맞추거나 지운다 |
| `docs/design/research-log.md` | Final | 아래 「킷 로그 한 단락」 을 옮긴다. 저장소 맨 위 `docs/` 라 Phase 6 범위 밖이다 |
| `design-kit/.claude-plugin/plugin.json` | Final | design-kit 버전(지금 0.4.0). 규약 절 셋 · 승인 기록 칸 둘 · 감사 행 하나 · 평가 사례 셋이 더해졌다 |
| `docs/` HTML | Final F2 | design-kit 규약 · 감사 기준 페이지가 있으면 다시 만든다 |
| `F20` | Phase 11 | 폐기 결정 기록 자리를 하나로 정한다 |

`.github/workflows/ci.yml` 에 넣을 줄은 없다 — 새 평가 사례는 CI 가 이미 돌리는 `run-evals.py` 안에 있다.
공유 파일(marketplace · plugin.json · 루트 README · 루트 CLAUDE.md · `docs/` HTML · 감사 로그 · 실패 횟수 파일 · 처리 배정표)은 건드리지 않았다(AR-01 `shared=0`).

## changelog 한 단락

design-kit 의 공유 규약(`references/visual-change-protocol.md`)이 편집 전에 세 가지를 응답에 남기게 한다 — 바꿀 화면의 파일 경로와 라우트(화면을 가리키면 진입점이 아니라
그 화면 자체), 요소 이름과 배치까지 넣은 한 문장 되말하기(두 갈래로 읽히면 먼저 묻기), 같은 역할의 서로 다른 기존 화면 2 개 이상에서 뽑은 관례 표(줄 모양 · 칩·뱃지 ·
아이콘 뜻 · grep 으로 확인한 재사용 부품). 「이 칩만」 처럼 요소 하나를 지목한 요청도 속성 하나 지목과 같은 부분 변경 규칙을 따르고 이웃 요소는 보존 목록에 오른다.
시각 산출물을 고칠 때는 기준 캡처에서 바뀌어야 할 표식을 정하고, 재캡처에서 그 표식이 바뀌었는지로 반영을 판정하며, 스스로 고치기는 최대 3 회다. 캡처마다 글자 넘침 ·
깨진 글리프 · 칩·뱃지와 줄 모양 · 디버그 겹침 넷을 보고, 넘침은 데이터를 고치지 말고 글자를 키워(웹 200%, 앱 최대) 한 장 더 찍는다. 승인 기록에 확정 구성 · 폐기한
대안 칸이 생겼고 design-mockup · design-concept 은 그 기록을 읽어 폐기한 안을 다시 넣지 않는다. 감사 기준 Authenticity 에 같은 역할 관례 일치 행이 생겼다(역할이 다른
화면은 대조하지 않는다). 숫자는 flutter-toolkit 규약과 같고, 세 규약이 같이 쓰는 규칙의 정본은 harness 설계 가이드 한 절에 두기로 했다. 시안 개수가 어긋난 두 자리를
미지정 3 규칙에 맞췄고, DTCG 예시를 2025.10 규격 형태로, Style Dictionary 안내를 v5 로, WCAG 2.2 게시일 · 크기 쿼리 · 44×44 표기를 바로잡았다. 평가 사례가 30 개가 됐다.

## 킷 로그 한 단락 (design-kit)

2026-09-24 Phase 6 — design-kaizen. 트리거 orchestrator-phase-6. 처리 배정표 `F01` · `F04` · `design:P1` ~ `design:P7` 아홉 행과 러닝북 Phase 6 추가 과제(flutter 규약과 숫자 · 세 규약
정본 결정), 근거 파일 §3 현행화 열 줄을 규약 한 곳 정의 · 스킬은 인용 구조로 묶었다. 근거:
[WCAG 2.2](https://www.w3.org/TR/WCAG22/) (Recommendation 2024-12-12 — SC 3.2.4 같은 기능의 일관된 식별 → 관례 일치는 같은 역할 한정, SC 1.4.4 텍스트 200%, SC 1.4.10 320 CSS px Reflow,
SC 2.5.8 AA 24×24 · SC 2.5.5 AAA 44×44, 「2026 법적 타겟」 근거 없음),
[W3C DTCG Format Module 2025.10](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/) (이름에 `{` `}` `.` 금지 · color `$value` 는 `colorSpace` · `components` 객체 ·
dimension `$value` 는 `value` · `unit` 객체 · 그룹 속성에 `$schema` 없음),
[Tailwind CSS v4.0](https://tailwindcss.com/blog/tailwindcss-v4) (2025-01-22, 기본 팔레트 `rgb` → `oklch`) · [v4.3.3](https://github.com/tailwindlabs/tailwindcss/releases/tag/v4.3.3) (2026-07-16),
[Style Dictionary v5.0.0](https://github.com/style-dictionary/style-dictionary/releases/tag/v5.0.0) · [v5.5.5](https://github.com/style-dictionary/style-dictionary/releases/tag/v5.5.5) (2026-09-20) ·
[v5 Migration](https://styledictionary.com/versions/v5/migration/) (Node.js 22 이상),
[MDN Container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries) · [MDN 호환 데이터 container-type](https://github.com/mdn/browser-compat-data/blob/main/css/properties/container-type.json)
(`size` 는 유효한 값, 크기 쿼리 Chrome 105 · Firefox 110 · Safari 16).
근거 파일이 밝힌 한계 — 「같은 역할 기존 화면 정확히 2 개/3 개」 · 「스스로 고치기 정확히 3 회/5 회」 를 정하는 외부 표준은 없어 숫자는 형제 규약 정합과 운영 비용으로 고른
레포 결정이다. Material 3 Expressive · Apple HIG 2026 · DTCG `$schema` URL · Figma Variables 의 OKLCH 지원은 조회하지 않았다.

## 다음 사이클 메모

- `임계값 다시 정의` — 규약 머리는 「여기 정의된 임계값·용어를 자기 문서에서 다시 정의하지 않는다」 인데 「2 개 이상」 · 「3 회」 가 스킬 · 감사 다섯 자리에 다시 적혔다.
  SK-08 은 이번 한 번만 맞춰 보고 다음 변경 때 막을 장치는 없다. 아울러 SK08 정규식은 조사 붙은 꼴 「기존 화면이 N 개 미만」 을 세지 않는다 — 새 글의 세 자리(규약 §0 ·
  audit-criteria 새 행 · design-reviewer 새 항목)가 그 꼴이다. 이번 판정은 모두 2 라 맞다(2 회차 검토 실측). 다음 사이클 정규식 후보 `'기존 화면이? \**[0-9]+ ?개'`
  (모의본에서 아홉 자리 모두 2). 한 자리만 숫자를 두고 나머지는 규약 §0 · §3 을 가리키게 줄이는 쪽이 근본 해법이다
- token-principles 새 줄 「Figma 쪽 hex 병기 관행은 `SKILL.md` Gotcha 12 를 따른다」 가 가리키는 design-system Gotcha 12 에는 「Figma Variables는 OKLCH 미지원」 이
  그대로 남는다. 계약 리서치 소스 절은 Figma 의 OKLCH 지원을 확인하지 않아 강하게 쓰지 않는다고 적었다 — token-principles 에서 지운 단정이 다른 파일을 가리키는 꼴로 남았다.
  다음 사이클 근거 파일 조회 목록에 넣는다
- `UNVERIFIED_ENV` · `§3.7 네 칸` · `design-mockup Step 0` · `Material 3` — 위 「미반영 키와 사유」 에 적은 넷이 다음 사이클 Phase 6 의 첫 후보다
- `.claude/skills/design-kaizen/SKILL.md` Gotcha 6 형제 대조 표에 「편집 전 확정 · 비교 반복 순서 · 캡처 점검 목록」 을 design · flutter · react 세 규약 행으로 더할 만하다.
  레포 전용 파일이라 이 Phase 범위 밖이다
- 계약 오라클 경고 훅(`~/.claude/hooks/lint-contract-oracle.sh`)이 DG-06 을 산문 grep 으로 잡았다 — 측정 절 백틱 안의 절 이름(`회귀 게이트`)이 한글이라 잡힌 오탐이다.
  훅은 `오라클 해소:` 줄을 읽지 않아 해소 줄이 있어도 계속 경고한다. 사용자 전역 훅이라 이 레포 카이젠 범위 밖이다
- 계약 피드백 자기진단 `implementation_leakage` 가 true — 조건 줄에 측정 도우미 이름이 들어갔다. Phase 7 과 같은 모양이다
- 평가 사례 28 · 29 · 30 은 구조만 잰다 — 실제 스킬로 돌려 답이 assertion 을 채우는지는 결정론 측정이 없다
