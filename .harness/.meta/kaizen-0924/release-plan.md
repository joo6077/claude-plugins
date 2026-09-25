# 카이젠 2026-09-24 — 릴리스 계획

Final 계약(`kaizen-0924-final`)은 킷 `plugin.json` · `.claude-plugin/marketplace.json` 의 판 번호와 날짜를 건드리지 않는다(러닝북 「버전」 절).
오케스트레이터 Step F4 1 번과 체크리스트 버전 두 줄을 이 파일로 대신한다. 직전 사례(2026-09-23)처럼 카이젠 PR 을 합친 뒤 `main` 에서 킷마다 `scripts/release.sh` 를 돌린다.

단계 규칙 — 기능 추가 = minor, 고침만 = patch. 한 킷에 Phase 와 Final 후속 계약이 다른 단계를 적었으면 큰 쪽을 쓴다.
판 번호는 이 파일에 적지 않는다 — 올릴 때 `release.sh` 가 그 킷 `plugin.json` 에서 읽는다.

## 킷마다 단계와 근거

| 킷 | 단계 | 근거 |
| --- | --- | --- |
| `harness` | minor | `.harness/.meta/kaizen-0924/phase3-notes.md` 「검증 레벨/루브릭 변경 … minor」 · `phase4-notes.md` 「스킬 절차 추가와 훅 동작 변경이라 minor」 (harness followups 는 patch 로 봤지만 큰 쪽) |
| `flutter-toolkit` | minor | `.harness/.meta/kaizen-0924/phase5-notes.md` 「스킬 프롬프트 · eval 기준 변경이라 minor」 |
| `design-kit` | minor | `.harness/.meta/kaizen-0924/phase6-notes.md` 규약 절 셋 · 승인 기록 칸 둘 · 감사 행 · 평가 사례 셋 |
| `backend-kit` | minor | `.harness/.meta/kaizen-0924/phase7-notes.md` 새 Gotcha 둘 · 감사 기준 두 행 |
| `infra-kit` | minor | `.harness/.meta/kaizen-0924/phase8-notes.md` Gotcha · 평가 사례 · 보고 형태(네 칸) |
| `rust-kit` | minor | `.harness/.meta/kaizen-0924/phase9-notes.md` Gotcha 둘 · 절차 하나 · 판정 형식 · 평가 사례 |
| `react-kit` | minor | `.harness/.meta/kaizen-0924/phase10-notes.md` 규약 틀 · 보고 형식 · 템플릿 기본값 · react-l10n 기본 흐름 |
| `planning-kit` | minor | `.harness/.meta/kaizen-0924/phase11-notes.md` PRD 산출물 틀(비범위 표) · 뒤 단계 스킬 동작 |
| `reflect-kit` | minor | `.harness/.meta/kaizen-0924/phase12-notes.md` 훅 동작 · 폴더 이름 규칙 · digest 출력 틀 |
| `bambu-kit` | minor | `.harness/.meta/kaizen-0924/phase13-notes.md` MakerWorld 읽는 순서 · G-code 길이 재기 블록 · 자기 검사 · 시험 파일 |
| `onboarding-kit` | minor | `.harness/.meta/kaizen-0924/phase14-notes.md` Gotcha 9 · 게이트 평가 러너 · 평가 사례 |
| `tone-kit` | minor | `.harness/.meta/kaizen-0924/phase15-notes.md` K-11 새 규칙(관측 컨벤션) · 이름 게이트 복구 |
| `api-kit` | minor | `.harness/.meta/kaizen-0924/phase16-notes.md` 판정 줄 양쪽 값 · 판정 불가 수 · 브라우저 확인 단계 |
| `howto-kit` | patch | `.harness/.meta/kaizen-0924/phase17-notes.md` 게이트 스크립트를 자식 셸에서 찾게 고침 · 러너 셸 확대 — 새 기능이 아니다 |

kit followups(`.harness/.meta/kaizen-0924/f1-kit-followups-notes.md` §Final 에 넘기는 것 (b))는 킷 열둘을 patch 로 봤다. Phase 판정과 합쳐 큰 쪽을 썼고 howto-kit 만 patch 로 남는다.
planning-kit 은 kit followups 기준으로는 연구 기록만 바뀌었지만 Phase 11 이 스킬 다섯과 에이전트 하나를 바꿔 minor 다.

## 돌릴 명령 (카이젠 PR 을 합친 뒤 `main` 에서)

```bash
bash scripts/release.sh harness minor
bash scripts/release.sh flutter-toolkit minor
bash scripts/release.sh design-kit minor
bash scripts/release.sh backend-kit minor
bash scripts/release.sh infra-kit minor
bash scripts/release.sh rust-kit minor
bash scripts/release.sh react-kit minor
bash scripts/release.sh planning-kit minor
bash scripts/release.sh reflect-kit minor
bash scripts/release.sh bambu-kit minor
bash scripts/release.sh onboarding-kit minor
bash scripts/release.sh tone-kit minor
bash scripts/release.sh api-kit minor
bash scripts/release.sh howto-kit patch
```

돌리기 전에 볼 것:

- 열린 릴리스 PR 이 있는지 먼저 본다 — 서로 쌓인 릴리스 가지가 있으면 같은 킷 판 번호가 갈린다
- `release.sh --dry-run` 도 `plugin.json` · `marketplace.json` 을 실제로 고친다(스크립트 안내 문구). 미리 보려면 돌린 직후 되돌린다
- 킷마다 한 번씩만 돌린다 — 돌릴 때마다 그 킷 판 번호가 오른다

## 배포 뒤 확인

- reflect-kit: 새 판이 설치된 뒤 설치본 Stop 훅이 실제로 reflections 를 적는지 한 번 본다 — `collect_status 1` 출력의 기록된 세션이 1 이상이어야 한다
  (`.harness/.meta/kaizen-0924/phase12-notes.md` §넘기는 것. Phase 12 계약은 가짜 분석기로만 쟀고, 설치본이 옛 판인 동안 수집은 계속 멈춰 있다)
- CI: harness followups 가 넣은 러너 여섯의 첫 우분투 실행 결과와 시간(F1H-82)을 PR 에서 본다
