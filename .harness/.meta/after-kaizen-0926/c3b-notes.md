# c3b 문서 사이트 후속 — 작업 기록

- 가지 `chore/ak-c3b-docs-site` · 시작점 `f81568d`
- 계약 `.harness/sprint-contract-after-0924-docs-site.md` (29 조건, 봉인 `sha256:49e805fabb7bdb20`, 봉인 커밋 `e7703dc`)
- 계약 피드백 `/Users/jackson/.harness/feedback/contract/1a3bcba6-2026-09-26T140848-bda55d45-86184.yaml` (`verify-feedback.sh` PASS)
- QA 판정은 이 기록에 적지 않는다 — 다음 단계 qa-evaluator 몫이다

## 봉인 전 교차 진단 반영

qa-evaluator 교차 진단이 21 조건을 계약의 측정 도우미로 다시 재 봉인 전 값과 모두 같게 냈다. 지적 일곱은 봉인 전에 계약 원문에 넣었다.

| 지적 | 반영 |
| --- | --- |
| RE-01 · RE-02 양성 대조 없음 | 임시 복제본에서 새 `docs/` 파일과 스타일시트 링크 한 줄 → `added_files=1 ext_added=1` |
| ER-02 가 11 쪽 전체를 봄 | 의도된 제약이라고 조건에 적음. kaizen-flow 의 옛 `overflow:hidden` 두 줄은 글자 그대로 둠 |
| 원본이 바뀌면 기대값이 조용히 바뀜 | SK-01 · 02 · 03 · 04 · 08 · 12 에 원본 지문 `orch_same` (시작 판 1, 원본 한 줄 더한 복제본 0) |
| DG-05 도구가 가지 밖 | 도구 지문 `tool_same` (시작 판 1, 다른 파일 0) |
| 공통 전제의 타임라인 이름표와 SK-07 절 삭제 허용이 어긋남 | 공통 전제에 「절을 빼면 이름표 제약이 걸리지 않는다」 한 줄 |
| DG-02 태그 검사만 옛 판 대비 | 시작 판 11 쪽이 모두 0 이라 절대 기준 0 으로 통일 |
| 브라우저 실행 파일 출처 없음 | 준비 단계에 실행 파일 위치 · 실패 문구 · 복구 명령 |

## 한 일

| 커밋 | 쪽 | 내용 |
| --- | --- | --- |
| `bdb57f6` | `docs/backend-kit/api-lifecycle.html` | 좁은 화면 격자 칸 `minmax(0, 1fr)` · 카드 긴 낱말 줄바꿈 |
| `3919ddc` | `docs/design-kit/typography-scale.html` | 48px 미리보기 낱말 줄바꿈 |
| `a3ce8f4` | `docs/flutter-toolkit/theming.html` | 함정 목록 칸 `minmax(0,1fr)` · 목록 글 줄바꿈 · 카드 격자 최소 폭 `min(100%,340px)` |
| `bfde270` | `docs/rust-kit/grpc-tonic.html` | 비교 격자 칸 `minmax(0,1fr)` · 비교 상자 · 점검 목록 줄바꿈 |
| `0694e37` | `docs/rust-kit/observability.html` | 비교 격자 칸 · 점검 목록 줄바꿈 |
| `e15fad2` | `docs/rust-kit/ownership-borrowing.html` | 비교 격자 칸 · 점검 목록 · 수치 표 코드 줄바꿈 |
| `ed61b9b` | `docs/rust-kit/project-structure.html` | 비교 격자 칸 · 점검 목록 줄바꿈 |
| `5dc249f` | `docs/onboarding-kit/setup-guide.html` | `guide_gate` 함수 원문 · Drift 반복 블록 원문 |
| `0001657` | `docs/design-kit/design-concept.html` | Step 0 · 4 · 5 · 7 · 안티패턴 코드 블록 원문 |
| `f17b890` | `docs/design-kit/design-mockup.html` | Step 6 승인 기록 틀 · 확인 명령 원문 |
| `5994ee6` · `6587a04` | `docs/process/kaizen-flow.html` | 17 Phase + Final 로 다시 씀 · 옮긴 줄의 한 글자 이름 풀기 |

### 글자 간격 넘침 일곱 쪽

과제가 정한 대로 수치가 아니라 구조로 고쳤다. 기준 쪽 하나(api-lifecycle)에서 두 수단을 정하고 나머지에 같게 썼다.

- 격자 칸 `1fr` 은 글 최소 폭 밑으로 줄지 않는다 → `minmax(0,1fr)` 로 바꿔 칸이 줄게 한다
- 줄지 않는 긴 코드 낱말은 `overflow-wrap:anywhere` 로 그 자리에서 줄을 바꾼다

계약 GAP 표가 적은 원인과 실제 원인이 두 쪽에서 달랐다. theming 은 표가 아니라 함정 목록 칸이, typography-scale 은 표가 아니라 48px 미리보기의 `Typography` 낱말이 넓혔다. 표는 둘 다 가로 스크롤 상자 안이라 문서 폭을 밀지 않았다. 실제 원인 쪽을 고쳤다.

ER-01 이 재는 375px 밖에서도 같은 부류 결함이 보여 함께 고쳤다. project-structure 의 비교 상자가 768 · 1280 에서 코드 상자를 카드 밖으로 100px 넘게 밀어냈다(글자 간격과 무관, 시작 판에도 있음). theming 카드 격자는 375px 에서 5px 삐져나왔다. 같은 rust-kit 네 쪽은 CSS 가 같아 네 쪽에 같은 선언을 넣었다.

재 본 값 — 일곱 쪽 모두 +0.06em · 375px 넘침 0, 375 · 768 · 1280 과 글자 간격 있음 · 없음 여섯 경우에서 상자 밖으로 삐져나온 글 0.

### 원본 담김 낮은 세 쪽

| 쪽 | 코드 블록 줄 | 코드 표시 빠짐 | 낱말 비율 |
| --- | --- | --- | --- |
| setup-guide | 1/61 → 61/61 | 0 | 0.55 → 0.57 |
| design-concept | 3/47 → 47/47 | 0 | 0.44 → 0.48 |
| design-mockup | 15/20 → 20/20 | 0 | 0.55 → 0.55 |

design-concept 의 승인 기록은 기존 정의 목록을 그대로 두고 원본 틀을 그 아래 따로 실었다. 정의 목록은 한눈에 읽는 요약이고 원본 틀은 복사해 쓰는 글이라 둘 다 남겼다.

### FN-80 kaizen-flow

원본을 `.claude/skills/kaizen-orchestrator/SKILL.md` 로 삼았다. 페이지 제목 · 호출 문법 · 흐름이 모두 이 스킬을 그리고, docs-site 매핑 표의 `process (공유)` 행 원본 칸 「(내부 문서)」 는 이 스킬 폴더 밖에 따로 원본이 없다는 뜻이다. 매핑 표 자체는 `.claude/skills/docs-site/` 안이라 고치지 않았다.

- 실행 흐름 — Step 0 · 0.5 · 0.6 카드, Phase 1~4 카드, 킷 Phase 13 개를 「동시에 3 개까지」 묶음으로, Final 카드에 F1 · F2 · F3 · F3.5 · F4
- 공통 실행 패턴 — 원본 10 걸음, 동시 3 개 제한, 서명 줄
- 호출 문법 — `phase10` ~ `phase17` 추가, 완료 전제 괄호를 원본대로
- 시뮬레이터 — 표 기반으로 다시 짰다. Phase 1~4 차례, 킷 Phase 3 개씩, Final 다섯 걸음. 로그 앞 칸은 지어낸 분 값 대신 단계 이름. 결과 값은 예시라고 안내 글에 적었다
- 트리거 표 — 첫 행 범위를 `Phase 1→2→…→17→Final` 로, 나머지 개별 카이젠 열 개를 한 행에 더했다

### 타임라인

절을 남겼다. 옛 판의 분 단위 값(P1 15m 등, 합계 150 분)은 원본에 없어 모두 뺐다. 칸 너비는 차례만 나타낸다고 절 안내 글에 적었다. 시간 근거로는 저장소 기록 `.harness/.meta/orchestrator-audit-log.md` 2026-08-13 사이클 방법론 관찰의 「직렬 추정 13 시간 → 배치 3 병렬 4~5 시간」 만 인용했다. 새 수치는 지어 넣지 않았다.

### dark-only

11 쪽은 모두 어두운 테마 전용(`check-docs-a11y.js` 가 `theme=dark-only` 로 보고)이다. 밝은 테마 규칙을 새로 넣는 일은 공통 틀 변경이라 넘겼다. ER-03 은 지금 방식 그대로 브라우저 색 설정 두 가지에서 잰다.

## 넘긴 것

| 항목 | 사유 |
| --- | --- |
| FN-79 css-tokens 매핑 표에 howto-kit accent | 표가 `.claude/skills/docs-site/` 안이라 이 묶음 범위 밖 |
| 공통 틀 177 쪽 `prefers-reduced-motion` · 행간 | 사용자 결정 대기(핸드오프 §C4 5 번). 11 쪽에도 새로 넣지 않았다 |
| 11 쪽 밝은 테마 | 위와 같은 공통 틀 변경 |
| docs-site 매핑 표 `process (공유)` 행 원본 칸 | `.claude/skills/docs-site/` 범위 밖. 이 기록의 FN-80 근거를 매핑 결정 때 쓰면 된다 |

## c4d 와 겹치는 곳

다른 묶음 c4d 가 가지 `chore/ak-c4d` 커밋 `4c079fa` 로 원본 `design-kit/skills/design-mockup/SKILL.md` 를 고쳤다. 이 가지에는 아직 없다. 계약대로 지금 원본 기준으로 맞췄다. 두 가지가 합쳐지면 페이지에 없는 원본 줄이 둘 생긴다.

- Step 0 감지 대상의 `.planning/prd-*.md` 줄
- Step 6 승인 기록 틀의 바뀐 「폐기한 대안·이유」 줄

그때 design-mockup 페이지를 새 원본 글자로 다시 맞추고 SK-11 을 다시 잰다.

## 킷별 버전 판단

올릴 킷이 없다. 바뀐 파일은 `docs/` 아래 11 쪽과 `.harness/` 기록뿐이다. `docs/` 는 어느 플러그인 폴더에도 속하지 않아 `plugin.json` 판을 올릴 대상이 없다.

## docs 드리프트

원본 문서를 바꾸지 않았다. `python3 scripts/detect-docs-drift.py --since f81568d --verbose` → `No docs drift since f81568d` (종료 코드 0).

## tone-guide 대조

1 단계에서 불러온 규칙 — 코어 `core-comment.md` · `core-naming.md` · `core-structure.md` · `core-antipatterns.md`, 주석 언어가 한국어라 `locale-korean.md`. 어댑터는 없다(`.claude/tone-project.md`), 스택 고유 대조 목록은 돌리지 않았다. 대상은 11 쪽의 더해진 줄과 이 기록이다.

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01 · C-02 what 주석 · 이름 반복 | 0 | 통과 — 새 주석은 kaizen-flow CSS 절 이름표 하나 |
| C-04 · F 구분선 블록 (G1) | 0 | 통과 |
| C-09 섹션 라벨 항목 수 | 0 | 통과 — `/* Kit phases — 동시에 도는 묶음 */` 아래 규칙 다섯 |
| C-10 디자인 툴 참조 (G2 · G3 · G4) | 0 | 통과 |
| C-12 계산 근거 (G6) | 0 | 통과 |
| C-13 자화자찬 (G5) | 0 | 통과 |
| G7 · G8 짧은 마커 · 끝 번역 주석 | 0 | 통과 |
| N-07 · E fallback 접두사 | 0 | 통과 |
| N-08 한 글자 이름 | 1 → 0 | 옮긴 콜백 인자 `c` 를 `card` · `conn` 으로 고침(`6587a04`). 남은 `i` 는 반복문 차례 변수라 허용, `delay` 의 `r` 은 손대지 않은 옛 줄 |
| S-03 · S-04 추출 | 0 | 통과 — 새 함수 `runSerialPhase` · `runKitBatch` · `clearFlow` 는 각자 책임이 있고 받은 값을 그대로 넘기기만 하지 않는다 |
| S-06 헬퍼 체인 (관측 컨벤션) | 1 | 알고 둔 한 단 — `runSerialPhase` · `runKitBatch` 가 옛 표시 함수 `activate` · `log` · `complete` 를 부른다. Phase 마다 되풀이되던 블록 열일곱을 줄이는 대가로 두었다. 강도가 관측 컨벤션이라 위반으로 단정하지 않는다 |
| S-12 · S-13 같은 부류 같은 패턴 | 0 | 통과 — 기준 쪽 하나로 두 수단을 정한 뒤 일곱 쪽에 같게 적용 |
| S-14 옮기면서 개선 | 0 | 통과 — 시뮬레이터를 옮기며 Phase 마다 되풀이되던 로그 블록을 표 기반 반복으로 줄임 |
| K-02 번역투 여섯 패턴 (§8 G-1) | 0 | 통과 — 11 쪽 더해진 줄 전체 |
| K-04 종결형 `합니다` | 0 | 통과 |
| K-05 음역 · K-11 새 이름 | 0 | 통과 — 「킷 Phase」 는 원본 낱말, 타임라인 「준비」 칸은 범례에 Step 0 · 0.5 · 0.6 이라고 풀어 적음 |
| H 보존 주석 | 0 삭제 | 통과 — 지운 주석 없음 |

§9 자기모순 검사 — 이 기록 본문에 번역투 여섯 패턴 0 건.

## 다음 사이클 메모

QA 는 APPROVE(`982e299`), 독립 검토는 판정을 뒤집을 결함 0 이었다. 아래는 독립 검토가 남긴 것 가운데 이 가지에서 고치지 않은 것이다.

1. **c1b 와 합칠 때 kaizen-flow 를 다시 맞춘다.** 가지 `chore/ak-c1b-harness-docs` 가 이 쪽의 원본 `.claude/skills/kaizen-orchestrator/SKILL.md` 를 커밋 다섯 개(`afff36a` 등)로 고친다. 킷 13 개의 `**범위:**` 줄에 agents · hooks · evals · docs 폴더가 더해지고 F2 매핑 표가 빠진다. 합치면 원본 지문 `orch_same` 이 0 이 되어 SK-01 · 02 · 03 · 04 · 08 · 12 측정이 멈춘다. 그 원본으로 재면 SK-08 은 `lost=1`(`flutter-toolkit/evals/`)이고, 킷 카드 13 개 가운데 12 개의 범위 칸이 새 범위 줄보다 좁다. 옛 판 Phase 5 카드에 있던 `flutter-toolkit/evals/evals.json` 표시를 새로 쓰면서 뺐는데, 지금 원본에 그 글자가 없어서 SK-08 이 못 잡았다. 합친 뒤 `docs/process/kaizen-flow.html` 의 킷 카드 범위 칸(403 ~ 545 줄)과 Phase 5 카드를 새 원본 글자로 맞추고 위 조건을 다시 잰다. 위 「c4d 와 겹치는 곳」 의 design-mockup 과 같은 처리다.
2. **design-concept 나쁜 예 코드 앞 공백 세 칸.** `docs/design-kit/design-concept.html:277` 이 `<pre><code>   | Accent | #E8965A |` 로 시작한다. 원본 `design-kit/skills/design-concept/SKILL.md:24-26` 은 코드 블록을 여는 줄 · 닫는 줄 · 내용 줄이 똑같이 들여쓰여 있어 내용은 0 칸이 맞다. 옆 좋은 예 칸은 0 칸이라 나란히 보면 줄이 어긋난다. 공백을 빼고 SK-10 을 다시 잰다.
3. **320px 에서 남은 넘침.** 계약 폭은 375 라 판정 대상이 아니었다. 시작 판(34 ~ 76px)보다 크게 줄었지만 두 곳이 남았다.
   - `docs/design-kit/typography-scale.html` — 글자 간격과 상관없이 9px 넘친다. `.responsive-container` (CSS 179 줄, 마크업 577 줄)
   - `docs/flutter-toolkit/theming.html` — 글자 간격 +0.06em 일 때 `ColorScheme.fromSeed(seedColor` 코드 한 줄이 카드 밖으로 잘린다
   - 320 을 기준 폭에 넣을지는 공통 틀 결정(핸드오프 §C4 5 번)과 같이 정한다
4. **`__pycache__` 가 `ci-local.sh` 를 돌릴 때마다 생긴다.** QA 가 `ci-local.sh` 를 돌리며 `flutter-toolkit/evals/scenario-report/__pycache__/` 와 `flutter-toolkit/skills/flutter-scenario-report/scripts/__pycache__/` 를 남겼다. 이 가지에서는 지웠다. 루트 `.gitignore` 는 `scripts/__pycache__/` 만 적어 루트의 `scripts/` 에만 걸린다. 모든 깊이의 `__pycache__/` 를 무시할지 정한다.
5. **쉬운 말.** 쉬운 말 목록에 걸리는 낱말이 두 곳 있었다. 이 기록 N-08 줄의 것은 「반복문 차례 변수」 로 고쳤다. 커밋 `5dc249f` 본문의 것은 커밋 이력을 다시 써야 해서 두었다.

독립 검토의 재현 스크립트는 임시 폴더 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/rev/` 의 `merged-orch.sh`(1 번) · `run-clip.sh` · `clip.js`(3 번)다.

## 측정 도구

- 계약 측정 도우미 작업본 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/c3b-measure.sh` (교차 진단 반영 뒤 계약에서 다시 뗀 판은 같은 폴더 `c3b-w/m2.sh`)
- 핸드오프 도구 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/` 의 `coverage.py` · `fence2.py` · `ci-local.sh`
- 넘침 원인을 찾은 보조 스크립트 `c3b-w/diag3.js` · `c3b-w/spill3.js` (같은 임시 폴더, 계약 조건 측정에는 쓰지 않음)
