---
feature: "bambu-kit 슬라이서 축 신설 · seam 정책 실측 반영"
slug: bambu-kit-slicer-axis-and-seam-policy
created: "2026-09-13 11:20"
complexity: "복잡"
conditions: 23
status: done
owner_session: 4e73ae32-a2c0-452b-8af3-84938c8dfbf0
conditions_digest: sha256:209ae5150c40cb31
locked_at: "2026-09-13 11:44"
---

## 배경

2026-09-07~13 실물 출력 3 회가 모두 **같은 위치에서 패였다.** 속도·냉각 축을 세 사이클 돌렸으나
결함 위치와 양상이 바뀌지 않았고, G-code 를 직접 떠서 재보니 원인이 두 가지였다.

하나는 **이음매(seam)가 세로로 쌓이는 것**이다. 래티스는 레이어마다 독립 폐루프가 25~59 개
생기고, 기본 `seam_position: aligned` 가 그 시작점을 층마다 같은 자리에 놓는다(인접 층 수평이동
중앙 0.069 mm).

다른 하나는 **벽이 안 들어가는 것**이다. 스트럿 국소 최소폭이 1.15~1.51 mm 인데 벽 2 겹이
요구하는 폭은 1.74 mm 라 56~90% 구간에서 두 겹이 안 들어가고, `wall_generator: classic` 이
그 자리를 갭필로 때운다(갭필 16,123 구간, 선폭 0.076~0.697 mm 로 9 배 요동).

오르카슬라이서 2.4.2 를 설치해 같은 부품을 같은 방식으로 잘라 비교한 결과, 뱀부 스튜디오에 없는
seam 세부 조정 키를 오르카가 가지고 있어 갭필을 0 으로 만들 수 있었다. 이 킷은 지금
"H2S + Bambu Studio 고정"이라 그 경로를 다룰 수 없다.

## 리서치 소스

- 오르카슬라이서 2.4.2 설치본 — 바이너리 문자열 · 시스템 프로파일 · 한국어 번역 카탈로그
- 뱀부 스튜디오 02.08.02.61 설치본 — 동일 3 종
- Codex 리서치 2 회 (조회 전용) — 오르카 위키 · 소스 코드 · 이슈 트래커
- 독립 검증 에이전트 1 회 — 슬라이스 16 회, 음성·양성 대조 포함

## GAP 분석

| 대상 | 현재 상태 | 갭 |
| --- | --- | --- |
| `plugin.json:3` | "Bambu Studio import 번들" | 슬라이서 고정 |
| `SKILL.md:3` | "다른 슬라이서에는 트리거 X — H2S + Bambu Studio 고정" | 오르카 명시 배제 |
| `SKILL.md:1298-1388` | 키 스코프 색인이 process/filament 2 종 | machine 스코프 미검사 |
| `seam-recipes.md` | 오르카 언급 7 건 전부 배제 맥락 | 슬라이서 차이 기준 문서 없음 |
| `surface-recipes.md` | 형상 클래스 축은 있음 | 벽 예산 계산 규칙 없음 |

## 범위 경계

이번 스프린트는 **문서·게이트 레이어**만 바꾼다. 실물 출력 검증은 범위 밖이며, 이 계약의
어떤 조건도 실물 출력 결과를 요구하지 않는다.

AR-01 baseline — 계약 작성 시점에 `git status --porcelain -- bambu-kit docs/bambu-kit` 를
1 회 실행했고 결과는 **0 건**이다. 따라서 구현 후 나타나는 변경은 전부 이번 스프린트 소산이다.

## 회귀 게이트

SC-01 은 기존 통과분을 깨뜨릴 수 있다. machine 스코프를 검사 대상에 넣으면 지금까지 통과하던
프로파일이 떨어질 수 있으므로, 음성 대조로 판별력을 확인한 뒤에만 적용한다.

## Skill

- [ ] SK-01: `bambu-kit/.claude-plugin/plugin.json` 과 `bambu-kit/skills/bambu-print-profile/SKILL.md` 양쪽에서 오르카 배제 문구가 제거되고 두 슬라이서를 모두 다룬다는 문구가 있다 [exact, enumerated] (측정: 두 파일 각각 `grep -c '슬라이서(OrcaSlicer/PrusaSlicer)에는 트리거 X'` == 0 이고 `grep -c 'OrcaSlicer'` >= 1)
- [ ] SK-02: `references/bambu-fields-baseline.md` 에 슬라이서별 키 차이 기준 섹션이 신설되고, 한쪽에만 있는 키를 오르카 전용 3 개 이상 · 뱀부 전용 3 개 이상 각각 열거한다 [structural] (측정: 섹션 헤더 1 건 이상 + 두 방향 각 행 수 >= 3)
- [ ] SK-03: `references/seam-recipes.md` 에 `seam_slope_conditional` 을 `0` 으로 두어야 하는 이유가 실측 수치와 함께 있다 [exact] (측정: `grep -c 'seam_slope_conditional'` >= 1 이고 같은 섹션 안에 `0%` 문자열 1 건 이상)
- [ ] SK-04: 경사 길이가 `min(설정값, 루프둘레)` 로 잘린다는 사실과 설정값을 루프 둘레보다 작게 잡아야 한다는 규칙이 `references/seam-recipes.md` 에 명시된다 [structural] (측정: 클램프 서술 1 건 + 규칙 문장 1 건)
- [ ] SK-05: `seam_position: random` 을 기본 처방으로 쓰지 않는 근거가 출처와 함께 `references/seam-recipes.md` 에 있다 [structural] (측정: 근거 문단 1 건 이상 + 출처 URL 1 건 이상)
- [ ] SK-06: `references/surface-recipes.md` 에 피처 폭 대비 벽 예산 계산식과 `wall_generator` 전환 기준이 있다 [exact] (측정: `line_width` 와 `wall_loops` 를 함께 쓴 계산식 1 건 + `arachne` 전환 조건 문장 1 건)

## Script

- [ ] SC-01: `SKILL.md` 의 키 스코프 대조가 `process` · `filament` · `machine` 3 종을 본다 [exact] (측정: 스코프 색인 코드 블록에 `machine` 문자열 존재 + 불일치 시 오류 경로 존재) 음성 대조: machine 분기를 지우면 `retraction_minimum_travel` 을 process 에 넣은 픽스처가 통과로 바뀐다
- [ ] SC-02: 유효하지 않은 enum 값이 조용히 강등되는 것을 잡는 음성 대조 절차가 `SKILL.md` 에 있다 [structural] (측정: 가짜 값 주입 후 산출물에서 소멸하는지 확인하는 절차 문단 1 건 이상)
- [ ] SC-03: `python3 scripts/validate-plugin.py bambu-kit` 가 exit 0 으로 통과한다 [goal] (측정: 명령 실행 후 `echo $?` == 0)
- [ ] SC-04: `bambu-kit/evals/gate-fixtures/` 에 machine 스코프 위반 1 개 · enum 강등 1 개 = 2 개 이상 픽스처가 신규 추가된다 [exact, enumerated] (측정: `git status --porcelain -- bambu-kit/evals/gate-fixtures` 의 신규 파일 수 >= 2)

## Error

- [ ] ER-01: 슬라이서를 판별하지 못했을 때의 폴백이 `SKILL.md` 에 정의되고 추측 금지가 명시된다 [structural] (측정: 폴백 문단 1 건 + 금지 문장 1 건)
- [ ] ER-02: 키 스코프 판정 불가(설치본 경로 없음) 시 `[미검증]` 처리 경로가 `SKILL.md` 에 명시된다 [structural] (측정: 해당 분기 서술 1 건 이상)

## Architecture

- [ ] AR-01: 변경 범위가 한정된다. Given: 계약 봉인 후 구현 완료 시점. `git status --porcelain -- bambu-kit docs/bambu-kit` 결과가 `bambu-kit/skills/bambu-print-profile/SKILL.md` · `bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md` · `bambu-kit/skills/bambu-print-profile/references/seam-recipes.md` · `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` · `bambu-kit/.claude-plugin/plugin.json` · `bambu-kit/README.md` · `bambu-kit/evals/gate-fixtures/` 하위 · `docs/bambu-kit/` 하위 이내이고 그 밖 0 건이다 [exact, enumerated]
- [ ] AR-02: 소비면이 동기화된다. `.claude-plugin/marketplace.json` · 루트 `README.md` · `CLAUDE.md` 3 파일이 슬라이서 축 신설을 반영한다 [exact, enumerated] (측정: 3 파일 각각 `grep -c 'Orca'` >= 1)
- [ ] AR-03: 파생 HTML 3 종 `docs/bambu-kit/bambu-print-profile.html` · `docs/bambu-kit/seam-recipes.html` · `docs/bambu-kit/surface-recipes.html` 이 소스 변경을 반영한다 [exact, enumerated] (측정: 3 파일 각각 `grep -c 'Orca'` >= 1)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 모든 코드 펜스에 언어 힌트가 있다 (측정: `python3 scripts/validate-plugin.py --check=code-fence` exit 0)
- [ ] AP-04: `SKILL.md` 머리말에 `name` 필드가 유지된다

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 것을 private 으로 만들지 않았다
- [ ] RE-02: 이미 존재하는 references 파일을 새로 만들지 않고 해당 섹션을 확장한다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0 개 (변경/생성 파일 대상)
- [ ] DG-02: 편집기 진단 워닝/인포 0 개 (제외 없음)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0 개
- [ ] DG-04: 수정된 스킬을 실제 1 회 실행해 process + filament JSON 생성까지 에러 0 개
