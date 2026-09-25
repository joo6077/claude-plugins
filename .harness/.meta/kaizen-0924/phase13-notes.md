# 카이젠 2026-09-24 Phase 13 (bambu-kit) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p13-bambu-kit.md` (조건 29 · 기능 조건 20, 봉인 `sha256:b172964574387cbb` · `locked_at` 2026-09-25 11:31)
- 개정: `.harness/sprint-amendments-kaizen-0924-p13-bambu-kit.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase13-review.md` — 1 회차 `VERDICT: CHANGES`(고칠 것 넷)는 DRAFT 가 반영했다. 2 회차 `VERDICT: CHANGES`(새로 하나 —
  G-code 길이 알려진 답이 방향을 무시한 호 계산을 통과시킴)는 BUILD 가 봉인 전에 검토 문구 그대로 반영하고, 예행 저장소를 다시 만들어 조건 전부 · 문장 삭제 46 ·
  대조 21 · 변형 다섯을 다시 돌렸다. 3 회차 검토는 돌리지 않았다(워크플로 지시 — 남은 지적을 반영하거나 이유를 계약 `## 범위 경계` 에 적은 뒤 진행).
  권고 가운데 DG-06 문구는 반영했고, 반영하지 않은 넷과 이유는 계약 `## 범위 경계` 「검토 권고」 줄에 있다
- 시작 커밋 `499cc1289f0f5ae5649da601515725f49f4f1096`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T113454-de8c7935-2494.yaml` (`verify-feedback.sh` PASS). 초안은 스크래치 `p13b/feedback-draft.yaml` 에 따로 쓰고
  `HARNESS_CONTRACT_ROOT` · `HARNESS_CONTRACT` 를 명시해 저장했다 — 작업 폴더의 `.harness/feedback-draft.yaml` 은 다른 Phase 와 겹칠 수 있어 쓰지 않았다

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `89f0ef8` | 봉인 커밋 | 계약 1 개 |
| `c012f2b` | MakerWorld JSON 주소 먼저 · 조용히 통과하던 검사 다섯 자리 | `bambu-kit/` 여덟 개 |
| `bf92821` | 개정 파일에 `end_sha` (`c012f2b`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p13-bambu-kit` 줄이 있다. 구현 커밋은 `git add -- <여덟> && git commit -o -- <여덟>` 로 내 경로만 실었다.
**FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

구현은 초안의 모의본(스크래치 `p13d/mock.py`, 지문 앞 16 자리 `2ae88ae777c4f1d8` — 2 회차 반영 뒤 계약에 적은 값)을 작업 폴더에 그대로 돌렸다(`mock applied 36`).
돌리기 전에 `git status --short -- bambu-kit` 가 0 줄인 것을 봤고, 커밋한 여덟 파일이 예행 저장소(`p13d/rh-none`)의 같은 경로와 바이트까지 같다.
29 조건 측정은 봉인 판 계약에서 뗀 묶음으로 돌렸다 — 스크래치 `p13d/k/`(`common.sh` · `m.sh` · `fakecurl.sh` · `rule-diff.sh`, 계약 `## 회귀 게이트` 네 블록과 글자 그대로 같다) ·
`p13b/runwt.sh`(`R` 을 비워 작업 폴더를 잰다. `K` 와 `TMPDIR` 는 스크래치). QA 가 같은 묶음을 다시 돌릴 수 있다 — 이 맥 디스크 여유가 1.3 GB 안팎이라 한 번에 한 셸로 돈다.

구현 커밋 `c012f2b` 를 상한으로 둔 첫 측정에서 notes 에 기대는 둘(ER-01 둘째 줄 `NOTES_MISSING` · ER-03)을 빼고 27 개 ID 가 조건 줄의 요구값과 줄마다 같았다.
커밋 뒤 저장소 검사: `validate-plugin.py bambu-kit` 종료 코드 0(V1 ~ V10 OK · V2 SKIP) · `sync-docs.py --check-only` 0(`bambu-kit/README.md: 동기화됨`) ·
`sync-evals.py --check-only` 0 · `run-evals.py` 0(114 passed — bambu-kit 은 목록에 없다) · `validate-post-kaizen.py --since 499cc12` 0(12 PASS · 0 FAIL · 3 SKIP,
scope-isolation · doc-contracts PASS, docs-site-regen SKIP). 킷 자체 시험은 SKILL.md 음성 대조 블록이다 — SC-06 이 끝 판에서 bash · zsh 로 돌려 종료 코드 46 자리가 요구값과 같다.

## 바꾼 파일

- `bambu-kit/skills/bambu-print-profile/SKILL.md` — Phase 1 입력 분기 · 전체 크롤링 원칙 · 첨부 링크 찾기를 JSON 먼저로, 끝 절 「MakerWorld 읽는 순서」,
  Phase 1.0 형상 측정 자기 검사, 4.3 완료 검사의 옵션 목록 줄 수와 빈 목록 `[미검증]`, 음성 대조 절(시험 파일 23 개 전수 · 폴더와 표와 실행 줄 대조 · 빈 목록 변이),
  4.4 값 박기 · G-code 대조를 칸마다, 두 스크립트 자기 검사, 「G-code 로 길이 재기」, 점검 목록 한 줄, 머리 변경 노트, 출처 한 줄
- `bambu-kit/skills/bambu-print-profile/references/comment-analysis.md` — §4.1 JSON 먼저 · 50+ 도 전수, §4.3 · §8 · §10, 머리 날짜
- `bambu-kit/skills/bambu-print-profile/references/surface-recipes.md` — G-code 실측 세 곳에 잰 방법 줄, 머리 날짜
- `bambu-kit/scripts/option-key-probe/generate-option-list.py` — 다섯 종류 중 하나라도 0 줄이면 쓰지 않고 exit 1
- 새 시험 파일 넷 `bambu-kit/evals/gate-fixtures/` — `process-flow-ratio-over.json` · `process-scarf-ratio-over.json` · `filament-retraction-over-parent.json` · `process-elefant-foot-negative.json`

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `F30` | MakerWorld 를 헤드리스 브라우저로 긁다 막힘 — JSON 주소 셋을 먼저 부르는 「MakerWorld 읽는 순서」 (bambu:P1 과 같은 조건) |
| `bambu:P1` | 읽는 순서 네 단계 · 403 에서 기다리지 않기 · 특정 브라우저 서버 이름 삭제 · Codex 에 셸 curl · 3mf 는 사용자에게, 댓글 두 수와 두 종류, 첨부 찾기 줄 수 먼저 |
| `bambu:P2` | 값 박기 · G-code 대조가 칸마다 읽고, 두 스크립트 자기 검사 |
| `bambu:P3` | 폴더에만 있던 시험 파일 8 개와 값 규칙 시험 파일 4 개를 표와 실행 줄에, 폴더 · 표 · 실행 줄 대조, 빠진 지운 사본 둘 |
| `bambu:P4` | 빈 옵션 목록이 키 검사를 끄던 두 자리 — 완료 검사 `[미검증]` 과 생성기 exit 1, 완료 검사 뽑기 줄 수 확인, 빈 목록 변이 |
| `bambu:P5` | 「G-code 로 길이 재기」 — 호 포함 · 알려진 답 자기 검사(`G2` 3/4 호 · `G3` 1/4 호, 반지름 다름) · 점검 목록 한 줄 · surface-recipes 잰 방법 줄 |
| `bambu:P6` | 형상 측정에 가짜 3mf 셋 자기 검사 |
| `F16` · `F17` 비고 | 킷별 실제 결함 — 위 bambu:P2 ~ P6 이 그 결함이다 |

Phase 1 가이드 변경 대조(오케스트레이터 전수 점검): §3.7 알려진 답 대조는 새 측정 셋에 반영했고(형상 측정 · G-code 길이 · 받은 댓글 세기), §3.7 네 칸은 아래 넘김,
작업 자체를 못 한다고 하기 전 네 칸은 「MakerWorld 읽는 순서」 4 번이 네 단계를 다 거친 뒤에만 사용자에게 묻게 했다. bambu-kit 에는 에이전트가 없다.

## 미반영 키와 사유

처리 배정표의 Phase 13 행 일곱은 모두 반영했다. 행 안에서 이 Phase 가 못 고친 곳은 아래 넘기는 것에 적는다.
빈틈 대조 원문(gapmap `groups[1]`)에서 뺀 것은 둘 — 답글 수 세기(배열 이름이 근거 파일에 없다 → 다음 사이클 메모), P3 (e) `bambu-kaizen` 회귀 줄(레포 전용 스킬 → 넘김).

## 넘기는 것

| 자리 | 남은 것 | 사유 · 맡을 곳 |
| --- | --- | --- |
| `.claude/skills/bambu-kaizen/SKILL.md` | Step 2 「fallback 체인 · MakerWorld Cloudflare」 점검 줄, 회귀 검증에 음성 대조 블록 실행 줄 (bambu:P1 · bambu:P3 (e)) | 레포 전용 스킬이라 이 Phase 범위(`bambu-kit/`) 밖 — 다음 사이클 |
| `.claude/skills/bambu-research/SKILL.md` | 「Cloudflare 우회」 · Playwright 1 순위 문구 (bambu:P1) | 같은 사유 |
| `docs/bambu-kit/bambu-print-profile.html` | 옛 읽는 순서 두 자리 (bambu:P1) | 문서 사이트는 Final F2 가 다시 만든다 |
| `feat/bambu-kit-orca-h2s-feedback` (QA 승인 · 안 올라감) | 같은 SKILL.md 의 4.3 · 음성 대조 표 · 4.4 자리를 고친다 | 이 Phase 가 먼저 합쳐지면 그 가지를 다시 올릴 때 SKILL.md 충돌을 풀어야 한다 — 표에 machine-*.json 네 줄이 더해진다 |
| `[미검증]` 네 칸 (Phase 1 가이드 변경) | 생성 측 자리 다섯, 시작 커밋 판 줄 번호 — `SKILL.md:806` · `SKILL.md:1072` · `SKILL.md:1209` · `SKILL.md:1706` · `references/failure-recipes.md:150` | 카이젠 스킬 Step 3 관심사 상한을 처리 배정표 두 관심사가 채웠다 — 다음 사이클 |
| 현행화 (근거 파일 §3) | `bambu-fields-baseline.md` 안정판 2.6 → 2.8.2.61 · beta 표기, `materials.md` PLA Pure, `SKILL.md` 릴리스 현황 줄 | references 대량 갱신은 `/bambu-research` 소관 (phase-research-templates Phase 13) |
| 금지 키 · `compatible_printers` · 메타필드 · 숫자 타입 | FAIL 시험 파일 0 개 | 다음 사이클 — 한 파일 한 위반으로 |
| `.github/workflows/ci.yml` | 넣을 줄 없음 — bambu-kit 음성 대조는 설치된 슬라이서(`/Applications` 의 BambuStudio · OrcaSlicer)가 있어야 돈다 | 리눅스 자동 검사에서는 못 돈다 |
| `bambu-kit/.claude-plugin/plugin.json` · marketplace | 버전 | Final |

## changelog 한 단락

bambu-kit 이 MakerWorld 모델을 읽을 때 브라우저보다 JSON 주소를 먼저 부르게 했다. 화면 없는 브라우저는 모델 페이지에서 `Just a moment...` · 403 으로 막혔고,
같은 모델의 JSON 주소 셋(모델 · 프로파일 목록 · 댓글)은 200 이었다. 댓글은 offset 으로 끝까지 받고 두 수(`commentCount` · `total`)를 함께 적는다. 조용히
통과하던 검사 다섯 자리도 막았다 — 값 박기와 G-code 대조가 첫 칸만 읽던 것, 표에도 실행 줄에도 없던 시험 파일 8 개, 비어 있는 옵션 목록이 키 검사를 끄던 것,
호를 빠뜨리던 G-code 길이 재기, 정답을 모르는 형상 측정. 새 측정마다 손으로 답을 센 입력으로 먼저 돌려 보게 했다.

## 킷 로그 한 단락

2026-09-25 Phase 13 — MakerWorld JSON 주소 셋은 공식 문서가 없어 `[관측 2026-09-24]` 로 적었다:
[design](https://makerworld.com/api/v1/design-service/design/1186414) ·
[instances](https://api.bambulab.com/v1/design-service/design/1186414/instances) ·
[commentandrating](https://api.bambulab.com/v1/comment-service/commentandrating?designId=1186414&offset=0&limit=100).
가짜 3mf 의 최소 구조는 [3MF Core 1.4.0](https://github.com/3MFConsortium/spec_core/blob/1.4.0/3MF%20Core%20Specification.md) 을 따랐다.
근거 파일이 밝힌 한계 — 403 에서 기다리지 말라는 공식 지침은 없다(킷의 운영 규칙으로 적었다), 두 댓글 수가 무엇을 세는지 근거가 없다, 3mf 받기의 로그인 요구는 확인하지 못했다.

## 다음 사이클 메모

- `.claude/skills/bambu-kaizen/SKILL.md` Step 4 회귀 검증에 음성 대조 블록을 원문 그대로 뽑아 돌리는 줄을 더한다 — 지금은 `validate-plugin.py` 만 돈다
- 댓글 답글 배열 이름은 근거 파일에 없다 — 다음 실측 때 이름을 적고 받는 법 블록이 답글 수까지 세게 한다
- 받는 법 블록의 측정에 모델 주소 403 경우를 더한다 — 실제로 막힌 쪽은 `makerworld.com` 이다. 검토자가 가짜 `curl` 로 돌려 블록이 요청 4 번 뒤 `FAIL` · 종료 코드 1 로
  멈추는 것은 이미 봤다(검토 1 회차 권고)
- 킷 블록들이 `mktemp` 폴더를 남긴다 — 새 빈 목록 변이의 `$EMPTY` 도 같다. 블록 끝 정리 줄을 블록 전체에 한 번에 더한다(한 블록만 고치면 규칙이 갈린다)
- G-code 길이 알려진 답은 봉인 전 검토가 두 번 고쳤다 — 반원(방향을 뒤집어도 같은 길이) → 1/4 호 둘(방향을 무시해도 같은 길이) → `G2` 3/4 호 · `G3` 1/4 호(반지름 다름).
  알려진 답은 흔한 실수를 넣은 사본에서 값이 떨어지는지 봉인 전에 돌려야 한다 — `harness/docs/guides/skill-design-guide.md` §3.7 에 한 줄 둘지 Phase 1 이 본다
