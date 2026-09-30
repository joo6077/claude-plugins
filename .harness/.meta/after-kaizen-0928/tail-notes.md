# tail — 연결 판정 · 전환 효과 · Mermaid 그려짐 기록

- 계약: `.harness/sprint-contract-after-0929-tail.md` (26 조건, 봉인 커밋 cec171b7, 측정 도우미 커밋 16a90598)
- 작업 폴더: `.claude/worktrees/ak3-tail`, 가지 `chore/ak3-tail`, 시작 판 c6cfcd09
- 출처: `rest-notes.md` 「남긴 것」 절의 약점 셋과 남은 일 둘(본문 배경 전환 · Mermaid 그려 보기)

## 항목별 결과

| 항목 | 한 일 | 커밋 |
| --- | --- | --- |
| (1) 가짜 연결 넷 | `scripts/check-api-kit-docs.py` 가 연결 판정을 `plugin_utils` 에서 불러 쓴다. `data-rel` · `data-href` 처럼 앞에 글자나 `-` 가 붙은 이름은 다른 속성으로 보고, `rel` 낱말에 `alternate` 가 있거나 `media` 가 화면용(없음 · `all` · `screen`)이 아니면 연결로 치지 않는다. 시험 `scripts/test-check-api-kit-docs.py` 에 경우 6 ~ 9 | a2670d07 |
| (2) 물음표 값 | `href="../assets/site.css?v=2"` 는 물음표 뒤를 떼고 주소 끝을 봐 연결로 센다. 시험 경우 10 | a2670d07 |
| (3) 공통 CSS 검사 | `scripts/check-docs-common-css.py` 도 같은 판정 `site_css_stylesheet_links` 를 불러 써 `preload` · `site.css.bak` 을 더는 세지 않는다. 시험 경우 8 을 더하고, 경우 5 가 임시 저장소에 `plugin_utils.py` 도 복사한다 | a2670d07 |
| (1) ~ (3) CI 이름 | `validate` 묶음 두 시험 단계 이름을 「열 경우」 · 「여덟 경우」 로 | 9cb20391 |
| (4) 본문 배경 전환 | 공통 파일 `docs/assets/site.css` 의 `prefers-reduced-motion` 블록에 `html,body{transition-duration:0s !important}` 한 줄. 쪽 47 개는 건드리지 않았고 움직임 허용 설정의 전환은 그대로다 | 07038fc6 |
| (5) Mermaid 그려짐 | 새 검사 `scripts/check-docs-mermaid.js` (종료 코드 0 통과 · 1 안 그려진 예시 · 2 못 돌림 · 3 예시 0 개)와 시험 `scripts/test-check-docs-mermaid.js` 네 경우. Mermaid 12.0.0 을 `devDependencies` 에 범위 기호 없이 넣고, 검사 · 시험을 CI `playwright` 묶음 `npm ci` 뒤에 등록 | a2670d07 · 7025ebb3 · 9cb20391 |
| (5) 종료 코드 표 | `harness/evals/gate-exit-codes.md` 소비처 표에 `scripts/check-docs-mermaid.js` 줄 | 042f27e9 |
| (5 딸림) flows 문장 | `docs/planning/flows.md` 의 「12 에서 렌더해 확인하지 않았다」 를 검사 이름과 12.0.0 으로 바꿨다. 쪽 `docs/planning-kit/flows.html` 의 머리 · 굵은 글 · 표 한 줄 · 비교 카드를 같이 맞췄고, 여섯 사실(12.0.0 · 2026-09-10 · 비시험판 · 2026-09-28 · 두 출처 주소)은 그대로 둔다 | d30f9614 · 8226d92d |

## 다시 잰 값 (2026-09-30, `npm ci` 뒤 W 맨 위 폴더)

| 조건 | 값 |
| --- | --- |
| 스크립트-01 | `test_tail=[경우 10 개 중 통과 10]` · `base_rc=1 base_fails=5` · `ci_ok=1` |
| 스크립트-02 | `test_tail=[경우 8 개 중 통과 8]` · `검사한 쪽 206 · 어긋난 쪽 0 · 못 읽은 쪽 0` · `base_ok=1` |
| 스크립트-03 | `cases=12 right=12 agree=12 all_ok=1` |
| 스크립트-04 | `쪽 3 · 예시 9 · 안 그려진 예시 0` · `ref=[pages=3 examples=9 bad=0]` · `broken_rc=1` |
| 스크립트-05 | `경우 4 개 중 통과 4` · `stub_rc=1` · `ci_ok=1` |
| 오류-01 | `listed=47 same_set=1 pages=47 bad=0 rcs=0,0,0 ok=1` |
| 오류-02 | `pages=47 moving=47 rc=0 ok=1` |

나머지 조건 값과 종료 코드는 이 기록을 커밋한 뒤 다시 재어 QA 에 넘긴다(구조-05 · 구조-08 은 이 기록 커밋까지 보아야 한다).

## 판단

- 판정 자리는 새 파일이 아니라 기존 `scripts/plugin_utils.py` 다. 두 검사가 따로 들고 있다가 한쪽은 `preload` 를, 다른 쪽은 `data-rel` 을 연결로 센 일이 이번 결함의 뿌리라, 한 함수를 둘이 부르게 했다.
- 추적 쪽 206 개는 모두 `rel="stylesheet"` 한 모양이라 판정을 조여도 걸린 쪽이 없었다.
- 본문 배경은 쪽 47 개를 고치지 않고 공통 파일 한 줄로 풀었다. 쪽마다 전환 줄을 지우면 움직임 허용 설정의 전환까지 사라진다(오류-02 가 그 모양을 잡는다).

## 킷 버전 판단

- harness — 바뀐 것은 `harness/evals/gate-exit-codes.md` 표 한 줄뿐이다. 스킬 · 에이전트 · 훅 · 스크립트 동작이 그대로라 올리지 않는다. 다음 harness 릴리스에 같이 실린다.
- planning-kit — 레포 뿌리 `docs/` 쪽과 원본만 바뀌었고 킷 폴더 변화가 없다. 올리지 않는다.
- 레포 뿌리 `scripts/` · `package.json` · `.github/` 는 킷이 아니다.
- 릴리스는 이 묶음 밖이다.

## tone-guide

- 1 단계: 레포 `tone-kit/references/` 의 `core-comment.md` · `core-naming.md` · `core-structure.md` · `core-antipatterns.md` 와 `locale-korean.md` 를 읽었다. 오버레이 `.claude/tone-project.md` — 어댑터 없음, 주석 언어 ko. 걸리는 규칙은 C-01 · C-07 · N-08 · S-03 · S-04 · K-02 · K-10.
- 5 단계: 바뀐 줄 276 줄(`.harness` · `package-lock.json` 제외)에 §8 G-1 번역투 여섯 모양 grep 0 건(K-02 · K-10). 새 줄의 한 글자 이름 0 건 — `check-api-kit-docs.py` 의 `r` · `f` · `u` 와 `plugin_utils.py` 의 `p` 는 시작 판부터 있던 줄이라 손대지 않았다(N-08 SHOULD, 최소 변경). 새 주석(공용 판정 · 공통 CSS 한 줄 · CI 두 단계 · Mermaid 검사 머리)은 모두 무엇이 틀렸었는지와 까닭을 적는다(C-01). 판정 함수는 두 검사가 함께 부르는 것이라 그대로 넘기기만 하는 래퍼가 아니다(S-04).

## 남긴 것

- QA 판정은 APPROVE(26 조건 중 PASS 22 · N/A 4, 직접 확인 26/26). 리포트와 계약 `status: done` 은 커밋 d028f726 에 담았다.
- 독립 검토가 넘긴 약점 하나(막지 않음). `scripts/check-docs-mermaid.js` 는 `<pre>` 첫 줄이 Mermaid 그림 종류 이름으로 시작할 때만 예시로 센다. 그래서 `flowchart LR` 을 `flowchat LR` 로 잘못 쓰거나, Mermaid 정상 문법인 `---` / `title: x` / `---` 머리말을 앞에 붙이면 그 예시를 「안 그려짐」으로 잡지 않고 아예 빼고 센다. `flows.html` 사본에서 두 경우 모두 `예시 3`(원래 4) · 종료 코드 0 이었다. 이번에 고치지 않은 까닭 — 고치기 전에는 그려 보는 검사 자체가 없었으니 전보다 못 잡게 된 것은 아니고, 지금 레포의 예시 9 개는 grep 으로 센 `<pre>` 9 곳과 맞아 빠진 예시가 없다. 봉인 뒤 판정을 넓히면 계약 범위 밖 변경이 된다. 고칠 방법은 예시마다 이미 붙은 `aria-label="Mermaid … 예시"` 로 예시를 찾게 하거나 쪽별 예시 수를 못박는 것이다. 그때 이 두 모양을 시험 `scripts/test-check-docs-mermaid.js` 의 음성 경우로 더한다.
- 같은 약점 때문에 `flows.md` · `flows.html` 의 「이 예시는 검사가 12.0.0 으로 그려 본다」 는 그림 종류 이름이 깨진 경우에는 맞지 않는다. 위 수정과 함께 풀린다.
- `docs/planning/research-log.md:45` 와 쪽 `docs/planning-kit/research-log.html:249` 의 「12 에서 렌더해 보지는 않았다」 는 그때의 기록이라 그대로 뒀다.
- 원본 `.md` · 스킬 파일의 `mermaid` 코드 울타리(`docs/planning/ideation.md` 의 `mindmap` 셋 · `planning-kit/skills/` 의 아홉)는 문서 쪽에 예시로 실려 있지 않아 새 검사가 보지 않는다. 원본까지 그려 보려면 검사가 `.md` 울타리를 읽게 넓혀야 한다.
- rest 계약의 `m 구조-02` 는 `렌더해 확인하지 않았다` 를 찾으므로 이 판에서 `md_keys_ok=0` 이 된다. 그 계약은 끝났고 이번에 일부러 지운 문장이라 고치지 않는다.
- 판 번호 올리기 · 합치기 · push 는 하지 않았다.
