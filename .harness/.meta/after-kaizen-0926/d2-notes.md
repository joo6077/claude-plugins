# d2 작업 기록 — 문서 사이트 177 쪽을 공통 스타일 파일로

계약: `.harness/sprint-contract-after-0924-docs-common-css.md` (봉인 `sha256:11225a00534b06ba`, 26 조건).
가지 `chore/ak-docs`, 작업 폴더 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak-docs`.
QA 판정은 이 기록에 적지 않는다 — 다음 단계의 qa-evaluator 가 한다.

## 한 일

| 커밋 | 내용 |
| --- | --- |
| `3d84b99` | 계약 봉인 커밋 — 계약 파일 하나만 담았다 |
| `33fec27` | 공통 파일 `docs/assets/site.css` 를 만들고, docs-site 스킬의 틀 · `SKILL.md` · `css-tokens.md` 가 그 파일을 걸고 같은 규칙을 다시 적지 않게 했다 |
| `c5aae49` | 177 쪽 모두 자기 `<style>` 앞에 공통 파일 링크 한 줄을 넣었다. 쪽마다 더한 줄 1 · 뺀 줄 0 이다 |
| `6d36b2f` | 행간 1.6 스물하나 · 1.65 넷, 모두 스물다섯 쪽에서 첫 `<style>` 안 body 규칙의 행간 선언 하나만 지웠다 |

공통 파일에는 두 규칙만 있다. 보통 모드의 본문 행간 1.7, 그리고 움직임 줄이기 설정에서 애니메이션 · 전환 길이 0.01ms, 애니메이션 반복 1 회, 스크롤 `auto` 다. 반복 1 회를 더한 까닭은 공통 파일 주석에 적었다 — 길이만 줄이면 무한 반복 애니메이션이 꺼지지 않고 깜빡인다.

## 판단과 근거

- 두 단계 아래 쪽인 `docs/design-kit/examples/moodboard-taskflow.html` 은 과제 문구의 `../assets/site.css` 가 아니라 `../../assets/site.css` 를 건다. 쪽 폴더에서 공통 파일까지 상대 경로를 계산한 값이다.
- 첫 화면 `docs/index.html` 은 body 에 행간 선언이 원래 없어 계산값이 `normal` 이었다. 지울 선언이 없으니 링크 한 줄만 넣었고, 이제 공통 파일로 1.7 을 받는다.
- `docs/backend-kit/caching.html` 을 비롯한 여덟 쪽은 `html,body` 를 한 규칙에 묶어 두어서 선언을 지우면 html 쪽 행간도 함께 빠진다. 글은 모두 body 안에 있어 화면에 드러나는 차이는 body 행간뿐이다.
- 배포에서 상대 경로가 풀리는지는 저장소 안 근거인 `docs/.nojekyll` 로 판단했다 — 배포가 폴더를 가공하지 않는다. 계약 도우미가 저장소 이름 아래 하위 경로로 쪽을 내주고 대소문자를 가리는 배포 흉내로 177 쪽을 모두 열어 공통 파일 응답 200 을 확인했다.
- 검사 도구 `scripts/check-api-kit-docs.py` 는 어떤 `<link` 든 외부 리소스로 세어, 링크를 넣은 뒤 api-kit 열두 쪽이 모두 「외부 리소스 참조」 로 실패한다. 이 도구는 자동 검사 흐름과 `ci-local.sh` 어디에서도 부르지 않아 합격선 밖이라 구현을 멈추지 않았고, 과제대로 도구는 고치지 않았다. 결과 변화가 그 사유 한 가지뿐임을 재었다(`ext_only_new=12 other_change=0`). 고칠 자리는 `:34` 의 `<link\s` 가 같은 사이트 안 `assets/site.css` 를 빼게 하는 것이고, 다음 scripts 묶음 후보로 넘긴다.
- 템플릿 body 의 행간 선언도 지웠다. 새 안내 줄이 「공통 파일이 맡는 규칙은 쪽에 다시 적지 않는다」 라서, 틀이 그 규칙을 어기면 새 쪽이 따라 어긴다. 177 쪽에 원래 있던 1.7 선언과 쪽 자체 움직임 줄이기 규칙은 과제대로 그대로 두었다.

## 넘긴 것과 사유

| 항목 | 사유 |
| --- | --- |
| `check-api-kit-docs` 도구 한 줄 고치기 | `scripts/` 는 이 묶음 범위 밖이다. 위 판단 절의 자리를 다음 scripts 묶음에서 고친다 |
| 스크립트가 직접 준 움직임 여섯 쪽 | `scrollTo` · `scrollIntoView` 의 `smooth` 다섯 쪽(`design-template` · `grid-alignment` · `ratio-proportion` · `visual-hierarchy` · `kaizen-flow`)과 `.animate(` 한 쪽(`flutter-toolkit/animation`)은 CSS 로 끌 수 없다. 쪽 스크립트는 쪽 본문이라 범위 밖이다 |
| 행간 기준 1.2 ~ 1.6 두 곳 | docs-site `SKILL.md:104` 와 `design-kit/skills/design-audit/references/audit-criteria.md:10` 의 기준이 사이트 값 1.7 과 어긋난다. 기준 문서가 킷 폴더에 있어 범위 밖이다 |
| 「standalone」 글 두 곳 | docs-site `SKILL.md:5` 설명 글과 `.claude/skills/kaizen-orchestrator/SKILL.md:620` 이 옛 원칙을 적고 있다. 앞은 스킬을 부르는 낱말이라 이번 규칙과 다른 일이고, 뒤는 범위 밖 폴더다 |
| 좁은 화면 넘침 | 시작 판에서 `docs/design-kit/typography-scale.html` 이 320px 폭에서 9px 넘친다. 과제 합격선이 375 · 1280 이라 이번에는 재지 않고 넘긴다 |
| 픽셀 비교에서 뺀 긴 쪽 | `docs/harness/contract-schema.html` (31894px)은 같은 판 비교에서도 가끔 1118px 가 달라 비교 대상에서 뺐다. 원인은 확정하지 못했고 다음 묶음의 재조사 후보다 |

## 킷별 판 올림 판단

없음. 바뀐 파일은 `docs/` 쪽 177 개와 공통 파일, 레포 전용 스킬 `.claude/skills/docs-site/` 의 세 파일, `.harness/` 기록뿐이다. 어느 킷의 `plugin.json` 에도 속하지 않아 올릴 판이 없다. `python3 scripts/validate-plugin.py` 는 `Total: 14 plugins, 14 OK` · 종료 코드 0 이다.

## 문서 드리프트

`python3 scripts/detect-docs-drift.py` 결과는 13 줄이고 d1 기록과 같은 목록이다. 이 묶음은 원본 문서를 바꾸지 않아 새로 생긴 드리프트는 없다. 대응 페이지가 없는 여섯(research-log · reflect-digest · rust-kit project-detection · adapter-contract · adapter-dart-flutter · locale-korean)도 그대로다. 페이지 재생성은 하지 않았다 — 부모가 모아서 한다.

## tone-guide 결과

`tone-kit:tone-guide` 의 1 단계(규칙 불러오기)는 봉인 커밋 뒤 구현 전에, 5 단계(전수 대조)는 구현 커밋 셋 뒤에 실제로 돌렸다.

1 단계 — 오버레이 `.claude/tone-project.md` 를 읽었다(어댑터 없음 · 주석 언어 ko). 설치본 `tone-kit/0.2.0/references/` 의 `core-comment.md` · `core-antipatterns.md` · `locale-korean.md` 를 읽고 `core-naming.md` · `core-structure.md` 의 규칙표를 읽었다. 이번 작업에 걸리는 규칙은 C-01 · C-04 · C-13 · C-15, N-09, S-05 · S-12, 안티패턴 F · H, K-02 · K-03 · K-11 이다.

5 단계 — 공통 파일과 docs-site 세 파일의 더한 줄 15 줄, 그리고 이 기록에 대조했다.

| 패턴 / 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-02 번역투 킬러 패턴 6 종 | 0 | 통과 — 같은 식에 「배경색이 오버레이에 의해 적용됩니다」 한 줄을 넣으면 1 이 나와 식이 살아 있다 |
| K-04 합니다체 | 0 | 통과 |
| C-13 자화자찬 | 0 | 통과 |
| C-04 · F 구분선 블록 | 0 | 통과 |
| C-01 · C-15 새 주석 | 2 | 통과 — 공통 파일 주석 둘은 범위 제약과 반복 1 회를 빼면 생기는 실패 모드를 적은 단문이다(H 보존 범주) |
| N-09 무역할 파일명 | 0 | 통과 — `site.css` 는 사이트 전체 규칙이라는 역할을 이름에 담는다 |
| S-05 · S-12 재사용 · 같은 꼴 | 0 | 통과 — 177 쪽이 같은 파일 하나를 같은 모양의 링크 줄로 건다 |
| K-11 새 이름 | 0 | 통과 — 「공통 파일」 · 「움직임 줄이기」 는 계약과 과제가 쓰던 말이다 |
| H 보존 대상 | 0 삭제 | 통과 — 쪽 본문의 주석은 건드리지 않았다 |

## 측정 도구

- 계약에서 뗀 측정 도우미와 자기 측정 실행 파일: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/d2/self-measure.sh` (뗀 파일은 같은 폴더 `self/d2-measure.sh`)
- 구현에 쓴 편집 스크립트: 같은 폴더 `mock-edit.py` (봉인 전 모의 판에 쓴 것과 같은 파일), 커밋 스크립트 `commit1.sh` · `commit23.sh`
- 로컬 CI: `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh` — 도우미 `m DG-05` 가 이 기록을 커밋한 뒤 돌린다
