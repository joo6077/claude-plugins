# lt 묶음 기록 — 마크다운 남은 경고 · 깨진 코드 블록 · 목록 · 밀린 줄 참조 (A1 · B18 · B19 · B20)

- 계약: `.harness/sprint-contract-after-0928-markdown-rest.md` (28 조건, 봉인 커밋 `b53f607`, 조건 지문 `sha256:fce06290475f8679` · 측정 지문 `sha256:aabae5a87f521872`). 측정 묶음 커밋 `37c6386`.
- 기준 판 `e500a63`, 가지 `chore/ak3-lt`. QA 판정은 하지 않았다. 계약 `status` 는 `active` 그대로다.

## 항목별 결과

| 항목 | 한 일 | 커밋 |
| --- | --- | --- |
| A1 | 시험 입력 21 파일을 뺀 여덟 파일의 경고 177 건을 0 으로. 표 구분 줄 칸 띄움, 목록 앞 빈 줄, 굵은 글 이름표 끝에 쌍점, 두 번 이상 빈 줄 지움, 첫 제목 넣기, 겹친 제목 이름 바꾸기. 그려진 모양(목록 촘촘함 · 목록 · 인용 · 표 · 코드 블록 수)은 그대로다 | `ba7e7eb` · `1bec949` · `067e867` · `7278b7a` · `b6d7ef3` · `44b618a` · `5694d8b` |
| B18 | 아홉 파일의 바깥 코드 블록 28 곳을 백틱 넷으로 바꾸고 안쪽 여닫이를 짝으로 맞췄다. 울타리를 끄던 block 꼴 주석을 지웠다(과제 제목 단계 MD001 짝만 남김). 이 과정에서 드러난 겹친 제목에는 next-line 주석을 달았다 | `5694d8b` · `9a95ed8` |
| B19 | 열 파일에서 목록 안 코드 블록 앞뒤 빈 줄을 next-line MD031 주석으로 바꿔 경고 정리 전 판 `c3e45f3` 과 같은 촘촘한 목록으로. `infra-audit` 은 목록을 끊던 주석 줄을 항목 들여쓰기로 옮겼다 | `1bec949` · `88e3ef0` · `7278b7a` · `1951824` · `b5924fd` · `43f3e34` · `f621dd3` · `9a95ed8` |
| B20 | git 줄 대응으로 따라간 줄 참조 23 곳과 같은 참조를 싣는 페이지 셋(`docs/backend-kit/research-log.html` · `docs/howto-kit/overview.html` · `docs/harness/plugin-validation.html`) | `067e867` · `7278b7a` · `5694d8b` |

## 뺀 시험 입력 21 파일 (A1)

모두 시험 입력이다. 시험이 파일 글자 그대로를 입력으로 쓰고, 경고 자체가 시험이 재는 모양이라 고치면 시험 뜻이 바뀐다.

| 경로 | 이유 |
| --- | --- |
| `harness/evals/test-fixtures/fixture-a/contract.md` | 시험 입력 — `harness/evals/test-fixtures/README.md` 절차가 `fixture-*/contract.md` 를 계약 평가 입력으로 연다 |
| `harness/evals/test-fixtures/fixture-b/contract.md` | 시험 입력 — `harness/evals/test-fixtures/README.md` 절차가 `fixture-*/contract.md` 를 계약 평가 입력으로 연다 |
| `harness/evals/test-fixtures/fixture-c/contract.md` | 시험 입력 — `harness/evals/test-fixtures/README.md` 절차가 `fixture-*/contract.md` 를 계약 평가 입력으로 연다 |
| `harness/evals/test-fixtures/fixture-d/contract.md` | 시험 입력 — `harness/evals/test-fixtures/README.md` 절차가 `fixture-*/contract.md` 를 계약 평가 입력으로 연다 |
| `harness/evals/test-fixtures/fixture-e/contract.md` | 시험 입력 — `harness/evals/test-fixtures/README.md` 절차가 `fixture-*/contract.md` 를 계약 평가 입력으로 연다 |
| `howto-kit/evals/fixtures/fail-g3-domainmix.md` | 시험 입력 — `howto-kit/evals/evals.json` 이 게이트 G1 ~ G6 판정 입력으로 연다 |
| `howto-kit/evals/fixtures/fail-g4-deprecation-ko.md` | 시험 입력 — `howto-kit/evals/evals.json` 이 게이트 G1 ~ G6 판정 입력으로 연다 |
| `howto-kit/evals/fixtures/fail-g4-korean-abolish-unsourced.md` | 시험 입력 — `howto-kit/evals/evals.json` 이 게이트 G1 ~ G6 판정 입력으로 연다 |
| `howto-kit/evals/fixtures/fail-g4-korean-delete-unsourced.md` | 시험 입력 — `howto-kit/evals/evals.json` 이 게이트 G1 ~ G6 판정 입력으로 연다 |
| `howto-kit/evals/fixtures/fail-g4-korean-shutdown-unsourced.md` | 시험 입력 — `howto-kit/evals/evals.json` 이 게이트 G1 ~ G6 판정 입력으로 연다 |
| `howto-kit/evals/fixtures/fail-g5-nonterminal.md` | 시험 입력 — `howto-kit/evals/evals.json` 이 게이트 G1 ~ G6 판정 입력으로 연다 |
| `howto-kit/evals/fixtures/fail-g6-granularity.md` | 시험 입력 — `howto-kit/evals/evals.json` 이 게이트 G1 ~ G6 판정 입력으로 연다 |
| `howto-kit/evals/fixtures/pass-fcm-ios.md` | 시험 입력 — `howto-kit/evals/evals.json` 이 게이트 G1 ~ G6 판정 입력으로 연다 |
| `howto-kit/evals/fixtures/pass-g4-completion-phrase-not-deprecation.md` | 시험 입력 — `howto-kit/evals/evals.json` 이 게이트 G1 ~ G6 판정 입력으로 연다 |
| `howto-kit/evals/fixtures/pass-g4-delete-action-not-deprecation.md` | 시험 입력 — `howto-kit/evals/evals.json` 이 게이트 G1 ~ G6 판정 입력으로 연다 |
| `howto-kit/evals/fixtures/pass-g4-korean-delete-sourced.md` | 시험 입력 — `howto-kit/evals/evals.json` 이 게이트 G1 ~ G6 판정 입력으로 연다 |
| `howto-kit/evals/fixtures/pass-g4-korean-sourced.md` | 시험 입력 — `howto-kit/evals/evals.json` 이 게이트 G1 ~ G6 판정 입력으로 연다 |
| `howto-kit/evals/fixtures/pass-g4-retention-notice-not-deprecation.md` | 시험 입력 — `howto-kit/evals/evals.json` 이 게이트 G1 ~ G6 판정 입력으로 연다 |
| `onboarding-kit/skills/setup-guide/evals/fixtures/gate-g4-ko-sourced.md` | 시험 입력 — `onboarding-kit/skills/setup-guide/evals/evals.json` 이 가이드 게이트 판정 입력으로 연다 |
| `onboarding-kit/skills/setup-guide/evals/fixtures/gate-g4-ko-unsourced.md` | 시험 입력 — `onboarding-kit/skills/setup-guide/evals/evals.json` 이 가이드 게이트 판정 입력으로 연다 |
| `onboarding-kit/skills/setup-guide/evals/fixtures/gate-ok-flutter.md` | 시험 입력 — `onboarding-kit/skills/setup-guide/evals/evals.json` 이 가이드 게이트 판정 입력으로 연다 |

## 글이 바뀐 줄 (A1, 새 판 `경로:줄`)

공백만이 아니라 글자가 바뀐 줄이다. 표 구분 줄은 대시 수가 바뀌어 여기에 든다 — 뜻은 같고 칸 띄움만 다르다.

- `api-kit/skills/api-ui/SKILL.md:14` — 첫 제목을 머리 설정 바로 아래로 옮김 (MD041). 옛 자리 38 줄은 지움
- `api-kit/skills/api-ui/SKILL.md:45` — 표 구분 줄 칸 띄움 (MD060)
- `api-kit/skills/api-ui/SKILL.md:58` — 표 구분 줄 칸 띄움 (MD060)
- `api-kit/skills/api-ui/SKILL.md:115` — 표 구분 줄 칸 띄움 (MD060)
- `api-kit/skills/api-ui/SKILL.md:128` — 표 구분 줄 칸 띄움 (MD060)
- `api-kit/skills/api-ui/SKILL.md:174` — 표 구분 줄 칸 띄움 (MD060)
- `api-kit/skills/api-ui/SKILL.md:249` — 첫 제목이 위로 가 둘째 큰 제목이 되지 않게 한 단계 내림 (MD025)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:729` — 굵은 글 이름표 끝에 쌍점 (MD036). 제목으로 바꾸지 않아 목차가 그대로다
- `bambu-kit/skills/bambu-print-profile/SKILL.md:737` — 굵은 글 이름표 끝에 쌍점 (MD036). 제목으로 바꾸지 않아 목차가 그대로다
- `bambu-kit/skills/bambu-print-profile/SKILL.md:745` — 굵은 글 이름표 끝에 쌍점 (MD036). 제목으로 바꾸지 않아 목차가 그대로다
- `bambu-kit/skills/bambu-print-profile/SKILL.md:752` — 굵은 글 이름표 끝에 쌍점 (MD036). 제목으로 바꾸지 않아 목차가 그대로다
- `bambu-kit/skills/bambu-print-profile/SKILL.md:776` — 표 구분 줄 칸 띄움 (MD060)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:817` — 표 구분 줄 칸 띄움 (MD060)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:959` — 표 구분 줄 칸 띄움 (MD060)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:986` — 표 구분 줄 칸 띄움 (MD060)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:1018` — 표 구분 줄 칸 띄움 (MD060)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:1049` — 표 구분 줄 칸 띄움 (MD060)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:1058` — 표 구분 줄 칸 띄움 (MD060)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:1084` — 표 구분 줄 칸 띄움 (MD060)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:1109` — 표 구분 줄 칸 띄움 (MD060)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:1262` — 표 구분 줄 칸 띄움 (MD060)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:1296` — 표 구분 줄 칸 띄움 (MD060)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:1344` — 두 인용 사이 빈 줄 경고(MD028). 인용 둘을 따로 두려고 사이에 설명 주석
- `bambu-kit/skills/bambu-print-profile/SKILL.md:1399` — 표 구분 줄 칸 띄움 (MD060)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:2115` — 굵은 글 이름표 끝에 쌍점 (MD036). 제목으로 바꾸지 않아 목차가 그대로다
- `bambu-kit/skills/bambu-print-profile/SKILL.md:2582` — 표 구분 줄 칸 띄움 (MD060)
- `bambu-kit/skills/bambu-print-profile/SKILL.md:2614` — 표 구분 줄 칸 띄움 (MD060)
- `design-kit/references/visual-change-protocol.md:211` — 같은 이름 「규칙」 제목을 절 이름으로 구분 (MD024). 페이지 소제목도 같게
- `design-kit/references/visual-change-protocol.md:526` — 같은 이름 「규칙」 제목을 절 이름으로 구분 (MD024). 페이지 소제목도 같게
- `harness/references/contract-schema.md:527` — 표 구분 줄 칸 띄움 (MD060)
- `harness/references/contract-schema.md:543` — 표 구분 줄 칸 띄움 (MD060)
- `howto-kit/skills/howto-audit/SKILL.md:17` — 첫 줄 제목 넣기 (MD041)
- `howto-kit/skills/howto-doc/SKILL.md:15` — 첫 줄 제목 넣기 (MD041)
- `onboarding-kit/skills/setup-guide/SKILL.md:8` — 첫 줄 제목 넣기 (MD041)

## 넣은 next-line 주석 (새 판 `경로:줄`)

block 꼴 끄기는 하나도 더하지 않았다. 아래는 모두 다음 한 줄만 끄는 주석이다.

- `.claude/kaizen-input/per-project-feedback.md:141` — MD024 — 프로젝트마다 같은 이름 소제목(`sprint-contract.md (excerpt)` 등)이 되풀이되는 사본이라 이름을 바꿀 수 없다. 울타리를 고치자 드러났다
- `.claude/kaizen-input/per-project-feedback.md:168` — MD024 — 프로젝트마다 같은 이름 소제목(`sprint-contract.md (excerpt)` 등)이 되풀이되는 사본이라 이름을 바꿀 수 없다. 울타리를 고치자 드러났다
- `.claude/kaizen-input/per-project-feedback.md:227` — MD024 — 프로젝트마다 같은 이름 소제목(`sprint-contract.md (excerpt)` 등)이 되풀이되는 사본이라 이름을 바꿀 수 없다. 울타리를 고치자 드러났다
- `.claude/kaizen-input/per-project-feedback.md:253` — MD024 — 프로젝트마다 같은 이름 소제목(`sprint-contract.md (excerpt)` 등)이 되풀이되는 사본이라 이름을 바꿀 수 없다. 울타리를 고치자 드러났다
- `.claude/kaizen-input/per-project-feedback.md:302` — MD024 — 프로젝트마다 같은 이름 소제목(`sprint-contract.md (excerpt)` 등)이 되풀이되는 사본이라 이름을 바꿀 수 없다. 울타리를 고치자 드러났다
- `.claude/kaizen-input/per-project-feedback.md:330` — MD024 — 프로젝트마다 같은 이름 소제목(`sprint-contract.md (excerpt)` 등)이 되풀이되는 사본이라 이름을 바꿀 수 없다. 울타리를 고치자 드러났다
- `.claude/skills/docs-site/SKILL.md:124` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `.claude/skills/docs-site/SKILL.md:128` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `bambu-kit/skills/bambu-print-profile/SKILL.md:2107` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `bambu-kit/skills/bambu-print-profile/SKILL.md:2112` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `bambu-kit/skills/bambu-print-profile/references/comment-analysis.md:153` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `bambu-kit/skills/bambu-print-profile/references/comment-analysis.md:157` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `flutter-toolkit/skills/flutter-hooks/SKILL.md:126` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `flutter-toolkit/skills/flutter-kaizen/SKILL.md:209` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `flutter-toolkit/skills/flutter-kaizen/SKILL.md:215` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `harness/skills/sprint-contract/SKILL.md:408` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `harness/skills/sprint-contract/SKILL.md:416` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `harness/skills/sprint-contract/SKILL.md:864` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `harness/skills/sprint-contract/SKILL.md:886` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `infra-kit/skills/infra-audit/SKILL.md:38` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `react-kit/skills/react-skeleton/SKILL.md:39` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `react-kit/skills/react-skeleton/SKILL.md:43` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `reflect-kit/skills/reflect-digest/SKILL.md:139` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `reflect-kit/skills/reflect-digest/SKILL.md:243` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `reflect-kit/skills/reflect-digest/SKILL.md:254` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `reflect-kit/skills/reflect-promote/SKILL.md:126` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `reflect-kit/skills/reflect-promote/SKILL.md:144` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `rust-kit/skills/rust-docker/SKILL.md:210` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `rust-kit/skills/rust-docker/SKILL.md:214` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `rust-kit/skills/rust-docker/SKILL.md:216` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다
- `rust-kit/skills/rust-docker/SKILL.md:220` — MD031 — 목록 안 코드 블록을 촘촘하게 두려고 빈 줄 대신 넣었다. 빈 줄을 넣으면 목록 항목이 문단으로 그려진다

## 고치지 않은 것 (이유)

- `.claude/kaizen-input/` 의 줄 참조 13 곳 — 다른 프로젝트 `.harness` 기록을 2026-04-24 에 떠 온 사본이다. 가리키는 파일이 이 저장소에 없어 git 줄 대응으로 따라갈 수 없고, 사본을 고치면 원래 기록과 달라진다. 이 폴더에서 바꾼 것은 `per-project-feedback.md` 의 울타리 · 주석 · 빈 줄뿐이다 (B18).
- `docs/howto/design-brief.md:23` 의 `qa-evaluation-guide.md:1009-1013` 과 `docs/howto/design-brief.md:370` 의 `…:1004-1013` — 가리키던 줄이 지워져 git 줄 대응으로 새 자리를 구할 수 없다. 뜻으로 새 자리를 고르면 추측이라 두었다.
- `.claude/skills/react-kaizen/SKILL.md` — markdown-it 로 그리면 울타리 깨짐 다섯 칸이 모두 0 이고, 4 번 항목도 `c3e45f3` 에서 이미 문단으로 그려져 경고 정리가 바꾼 것이 없다. `harness/skills/sprint-contract/SKILL.md` 도 울타리는 멀쩡해 B19 목록 두 곳만 고쳤다.
- `.harness` 안 지난 계약 · 피드백의 줄 참조 520 곳 — 결정 기록(decisions.md)대로 묶음 rec 몫이다.

## 자기 측정 (TIP 기준, 2026-09-28)

조건마다 적힌 명령을 그대로 zsh 에서 돌렸다 (`TMPDIR` 은 scratch).

- 통과: SK-02 (다른 파일 0 · 21 줄 모두 1 이상) · SK-03 (`TOTAL 0 0 0`, 기록 빠짐 0) · SK-04 (아홉 파일 0 · 레포 전체 삼킨 줄 0 · 안 닫힘 0) · SK-05 (`SITES 28 28` · rc=0) · SK-06 (other 0) · SK-07 (`0 0 2 0 0 6 0 0 0`, MD001 밖 0) · SK-08 (열 파일 모두 0 · `TOTAL 0 0 0` · 넓은 비교 2 열 0) · SK-09 (fence 0 · other 0) · SK-10 (`REFS 31 31` · rc=0) · SK-11 (넷 모두 1 이상 · 다른 사본 0) · SC-01 (열여섯 값 모두 봉인 때와 같다) · SC-03 (`4/4 PASS` · 공통 CSS 링크 각 1) · ER-01 (blockdir 0) · ER-02 (기록 빠짐 0) · ER-03 (더한 제목 셋 모두 페이지에 1) · AR-01 (BAD 0) · AR-02 (범위 밖 0) · AR-03 (SEAL_BROKEN 0 · 지난 기록 변경 0) · AP-03 · AP-04 (`Total: 14 plugins, 14 OK`) · RE-02 (0) · DG-01 (0).
- 실패: SK-01 은 4 (기대 0 — 시험 입력 쪽은 90 으로 같다), DG-02 도 4. 넷 모두 `docs/react/kit-design/final-integration.md:457` 이다 (남은 것 첫 줄).
- SC-02: `ci-local.sh` 25 단계 rc=0 · `feedback-agg-test SKIP (yq 없음)` 한 줄. CI 파일에만 있는 아홉 명령 모두 종료 코드 0 (api-kit 문서 12/12 · 문서 흐름 표 어긋남 0 · 원인 표 사본 0 · 검토 규약 사본 0 · 측정 도움 시험 실패 0 · bambu 게이트 24 · 주소 읽기 5 · 결정 게이트 21 불일치 0 · playwright 8 passed).
- 톤: tone-kit `locale-korean.md` §8 G-1 · G-2 를 더한 줄 988 줄에 돌렸다. G-1 한 건은 `docs/backend/research-log.md` 의 원래 문장(줄 번호만 바꾼 줄)이라 새 글이 아니다. G-2 0.

## 킷 버전 판단

바뀐 킷은 api-kit · bambu-kit · design-kit · flutter-toolkit · harness · howto-kit · infra-kit · onboarding-kit · react-kit · reflect-kit · rust-kit 열하나다. 모두 스킬 · 참조 문서의 마크다운 모양과 줄 참조 숫자만 바뀌었고 동작 규칙은 그대로라 patch 로 본다. 릴리스는 합친 뒤 main 에서 한다 (이 묶음에서는 하지 않았다).

## 남은 것

- `docs/react/kit-design/final-integration.md:457` 표 구분 줄 `|------|------|` 의 MD060 경고 4 건. B18 로 바깥 코드 블록을 바로 닫자 원래 코드 블록 밖이던 표가 다시 표로 그려지면서 드러났다. 고치려면 그 줄의 칸 띄움을 바꿔야 하는데, 계약 SK-06 이 아홉 파일에서 울타리 · 주석 · 빈 줄 밖의 줄 변경을 0 으로 묶었다. next-line 주석은 표 둘째 줄에 걸 수 없고(표가 끊긴다, scratch 실측), 파일 전체 끄기는 ER-01 의 뜻을 우회한다. 그래서 두었고 DG-02 는 이 파일에서 4 가 남는다. SK-06 을 「표 구분 줄 칸 띄움 한 줄」 만큼 넓히는 개정은 조건을 느슨하게 하는 쪽이라 사용자 동의가 따로 필요하다.

## 2 회차 계약

- 계약: `.harness/sprint-contract-after-0928-markdown-rest-r2.md` (28 조건, 봉인 커밋 `b16b136b`, 조건 지문 `sha256:ae224dc595515f00` · 측정 지문 `sha256:fbb99435ba5a3964`, 봉인 2026-09-28 14:01). 1 회차 계약은 `status: superseded` (`d5a665cd`), 1 회차 QA 리포트는 `d4b7a833` (REJECT — SK-01 · DG-02).
- 바꾼 것: 1 회차 SK-06 측정이 표 구분 줄 수정을 막아 SK-01 · DG-02 와 동시에 통과할 수 없었다. 2 회차 SK-06 은 칸 띄어쓰기 · 대시 수만 바뀐 표 구분 줄을 허용하고, 더한 줄과 지운 줄이 짝이 맞는지를 잰다.
- 구현: `27dad4ff` — `docs/react/kit-design/final-integration.md:457` 을 `|------|------|` 에서 `| ---- | ---- |` 로. 복제본 `lt-r2` 의 고친 판 `40a99bb0` 과 차이가 같다. 대응 페이지 `docs/react-kit/integration.html` 은 HTML 표라 구분 줄이 없어 바꿀 것이 없다 (`detect-docs-drift.py` 는 이 파일을 그 페이지에 짝지어 보여 줄 뿐 어긋남 표시는 없다).
- 교차 진단 지적 셋과 처리: (1) SK-01 · DG-02 가 봉인 시점에 4 · 4 — 위 구현 커밋으로 0. (2) AR-01 서명 줄이 모델 이름을 글자 그대로 박았다 — 이 세션 서명과 같아 BAD 0. (3) SK-06 이 통과 집합을 넓힌다 — 아래 남은 것.

### 자기 측정 (2 회차, 끝 판 `27dad4ff` 기준 · 이 기록 커밋 전, 2026-09-28)

조건에 적힌 명령을 그대로 떼어 한 스크립트로 돌렸다 (scratch `r2-measure.sh`, SC-03 만 bash).

| 조건 | 값 | 기대 |
| --- | --- | --- |
| SK-01 | 0 · 90 | 0 · 90 |
| SK-02 | 다른 파일 0 · notes 있음 · 21 줄 모두 1 이상 | 같음 |
| SK-03 | `TOTAL 0 0 0` · 기록 빠짐 0 | 같음 |
| SK-04 | 아홉 파일 0 (파일 줄 9) · 전체 끝 줄 `TOTAL 0 0 0 69 1 1 2294` (2 · 3 열 0 · 0) | 0 · 0 · 0 |
| SK-05 | `SITES 28 28` · rc=0 · FAIL/BADANCHOR 0 | 같음 |
| SK-06 | `SEP 2 0 0`, line-kinds other 2 | bad 0 · unmatched 0 · n = other |
| SK-07 | `0 0 2 0 0 6 0 0 0` · MD001 밖 0 · 0 | 같음 |
| SK-08 | 열 파일 모두 0 · `TOTAL 0 0 0` · 넓은 비교 2 열 0 | 같음 |
| SK-09 | fence 0 · other 0 | 0 · 0 |
| SK-10 | `REFS 31 31` · rc=0 | 같음 |
| SK-11 | 7 · 1 · 1 · 1 · 다른 사본 0 | 1 이상 · 0 |
| SC-01 | 열여섯 값 모두 봉인 때와 같다 | 같음 |
| SC-02 | `ci-local.sh` 25 단계 rc=0 · SKIP 은 `feedback-agg-test SKIP (yq 없음)` 한 종류 (단계 목록과 끝 줄에 두 번 찍힘) · 아홉 명령 모두 rc=0 | 같음 |
| SC-03 | `4/4 PASS` · 공통 CSS 링크 각 1 | k/k |
| ER-01 | blockdir 0 | 0 |
| ER-02 | 기록 빠짐 0 | 0 |
| ER-03 | 더한 제목 셋 모두 페이지에 1 | 1 이상 |
| AR-01 | BAD 0 · 커밋 21 | 0 · 1 이상 |
| AR-02 | 0 | 0 |
| AR-03 | `10 SEAL_ABSENT` · `120 SEAL_OK` (BROKEN 없음) · 0 · 0 | 없음 · 0 · 0 |
| AP-03 · AP-04 | `Total: 14 plugins, 14 OK` · rc=0 | 같음 |
| RE-02 · DG-01 · DG-02 | 0 · 0 · 0 | 0 |

- SC-03 측정의 `$P` 는 zsh 에서 쪼개지지 않아 파일 넷이 한 경로로 붙고 검사기가 죽는다. bash 에서 돌리면 위 값이다. 조건 뜻은 bash 로 잰 값이다.
- 그 밖 검사: `python3 scripts/validate-plugin.py` 14 OK · `sync-docs.py --check-only` rc=0 · `sync-evals.py --check-only` rc=0.
- 이 기록 커밋 뒤 끝 판이 바뀌므로 notes 를 읽는 조건(SK-02 · SK-03 · SK-11 · ER-02)과 AR-01 은 커밋 뒤 한 번 더 잰다.

### 톤 대조 (tone-guide 5 단계)

어댑터 없음 · 주석 언어 한국어 (`.claude/tone-project.md`). 바꾼 것은 표 구분 줄 한 줄과 이 기록 · 계약 산문뿐이다.

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| C-01~C-14 (주석) | 0 | 해당 없음 — 주석을 더하거나 지우지 않았다 |
| N-01~N-12 (이름) | 0 | 해당 없음 — 새 이름 없음 |
| S-01~S-14 (구조) | 0 | 해당 없음 — 코드 추출 없음 |
| 안티패턴 A~J | 0 | 통과 — H(보존 대상) 지운 것 없음 |
| `locale-korean.md` §8 G-1 (처리합니다 · 에 대해 · 하도록 합니다 · 에 의해 · 되어 있는 경우 · 과한 수동태) | 0 | 통과 — 이 절 · 계약 범위 경계 더한 줄 |
| §8 G-2 | 0 | 통과 |

### 킷 버전 판단 (2 회차)

2 회차에서 더 바뀐 킷은 없다 (`docs/` 한 줄은 킷 밖). 1 회차 판단(열하나 킷 patch, 릴리스는 합친 뒤 main 에서)을 그대로 둔다.

### 남은 것 (2 회차)

- 사용자 확인 한 줄: 2 회차 SK-06 은 「바뀐 줄은 울타리 · 주석 · 빈 줄뿐」 에 「칸 띄어쓰기 · 대시 수만 고친 표 구분 줄」 을 더해 통과 집합을 넓혔다. decisions.md 가 정한 길(느슨하게 하는 개정 대신 2 회차 계약)을 따랐지만 이 조건 하나만 콕 집은 동의는 받지 않았다.
- QA 판정은 APPROVE(28 조건 중 PASS 24 · 해당 없음 4 · FAIL 0). 리포트와 계약 `status: done` 은 `04779954` 로 커밋했다.
- SC-03 재는 명령 결함: `P=$(git diff --name-only ...)` 를 따옴표 없이 넘겨 zsh 에서는 경로 넷이 한 덩어리로 붙어 `check-docs-a11y.js` 가 깨진다. 계약 공통 정의(「zsh · bash 같은 결과」)와 어긋난다. bash 로 돌리면 `4/4 PASS`. 다음에 비슷한 조건을 쓸 때 경로 목록을 `xargs` 나 배열로 넘길 것. 봉인된 계약은 고치지 않았다.
- 독립 검토: 막는 결함 0. 지적한 커밋 안 된 `status` 변경은 `04779954` 로 풀렸다.
- 앞 절 「남은 것」 의 457 행 항목은 2 회차 구현 `27dad4ff` 로 풀렸다.
