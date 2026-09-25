# 카이젠 2026-09-24 Phase 15 (tone-kit) — notes

- 계약: `.harness/sprint-contract-kaizen-0924-p15-tone-kit.md` (조건 23 · 기능 조건 15, 봉인 `sha256:afc0e79e2045ae87` · `locked_at` 2026-09-25 11:35)
- 개정: `.harness/sprint-amendments-kaizen-0924-p15-tone-kit.md` (조건 변경 0 건, `end_sha` 만)
- 검토: `.harness/.meta/kaizen-0924/phase15-review.md` — 1 회차 `VERDICT: CHANGES`(고칠 것 둘 · 참고 여섯)는 DRAFT 가 고칠 것 둘과 참고 1 · 5 · 6 을 반영했고,
  2 회차가 `VERDICT: APPROVE` 를 냈다. BUILD 는 봉인 전에 `## 범위 경계` 승인 대체 줄에 이 판정을 적고 2 회차 참고 1 대로 「앞 Phase notes 열두 개」 를
  「열세 개」 로 고친 것(서술 줄 셋) 말고는 계약을 고치지 않았다
- 시작 커밋 `499cc1289f0f5ae5649da601515725f49f4f1096`
- 계약 피드백: `~/.harness/feedback/contract/5a24cc99-2026-09-25T113810-de8c7935-20426.yaml` (`verify-feedback.sh` PASS). 초안은 스크래치 `p15b/feedback-draft.yaml` 에 따로 쓰고
  `HARNESS_CONTRACT_ROOT` · `HARNESS_CONTRACT` 를 명시해 저장했다 — 작업 폴더의 `.harness/feedback-draft.yaml` 은 다른 Phase 와 겹칠 수 있어 쓰지 않았다

## 커밋

| 커밋 | 내용 | 파일 |
| --- | --- | --- |
| `91ea6d7` | 봉인 커밋 | 계약 1 개 |
| `50dfd86` | K-11 새 이름 규칙 · 표 칸에서 죽어 있던 이름 게이트 넷을 코드 블록으로 · 확장자 변수 배열 | `tone-kit/` 다섯 개 |
| `c97dd20` | 원칙 9 · 이번 사이클 연구 기록 · 게이트 예시 확장자 배열 | `docs/tone/` 세 개 |
| `409434d` | 개정 파일에 `end_sha` (`c97dd20`) | 개정 1 개 |
| 이 파일의 커밋 | notes · 검토 기록 | `.harness/` 두 개 |
| 그다음 커밋 | 개정 파일에 notes 커밋 sha 로 `end_sha` 한 줄 더 | 개정 1 개 |

모든 커밋 메시지 끝 문단에 `Kaizen-Phase: kaizen-0924-p15-tone-kit` 줄이 있다. 구현 커밋은 `git add -- <파일…> && git commit -o -m … -- <파일…>` 로 내 경로만 실었다.
**FIX 가 커밋을 더할 때도 서명 줄을 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다.**

구현은 초안의 모의본(스크래치 `p15d/mock.py`, 지문 앞 16 자리 `42dde3050ac3accf` — 계약에 적힌 값)을 작업 폴더에 그대로 돌렸다(`mock applied 8` · 종료 코드 0).
돌리기 전에 `tone-kit/` · `docs/tone/` · 근거 파일이 시작 커밋과 `HEAD` 사이에 바뀌지 않았고 미커밋 변경도 없는 것을 봤다. 커밋 전 여덟 파일이 예행 저장소(`p15d/rh-none`)의
같은 경로와 바이트 단위로 같았다.
23 조건 측정은 봉인 판 계약에서 뗀 묶음으로 돌렸다 — 스크래치 `p15b/k/`(`common.sh` · `m.sh` · `lintcmp.sh`, DRAFT 판 `p15d/k/` 와 글자 그대로 같다) ·
`p15b/runall.sh`(`K` 와 `TMPDIR` 를 스크래치로 두고 공통 정의를 `.` 로 읽은 뒤 `m <조건 ID>`). QA 가 같은 묶음을 다시 돌릴 수 있다.

구현 커밋 `c97dd20` 을 상한으로 둔 첫 측정에서 notes 에 기대는 둘(ER-01 둘째 줄 `NOTES_MISSING` · ER-03)을 빼고 나머지 ID 가 조건 줄의 값과 같았다.
커밋 뒤 저장소 검사: `validate-plugin.py tone-kit` 종료 코드 0(V1 ~ V10 OK) · `validate-plugin.py`(전체) 0 · `Total: 14 plugins, 14 OK` · `sync-docs.py --check-only` 0 ·
`sync-evals.py --check-only` 0 · `run-evals.py` 0(115 passed) · `run-evals.py tone-kit --verbose` 의 `PASS eval #4 (tone-guide): 4 assertions` ·
`validate-post-kaizen.py --since 499cc12` 0(scope-isolation · doc-contracts PASS, docs-site-regen SKIP). 등록된 검사 목록은
`frontmatter templates refs triggers placeholders code-fence plugin-json hook-exec arg-substitution table-integrity` 다.

## 카이젠 스킬 Step 2 격차 표

| # | 축 | 격차 | 처리 |
| --- | --- | --- | --- |
| 1 | 게이트 생존 | `core-naming.md` §8 G-1 · G-2 · G-5 · G-6 이 표 칸에 있어 붙여 넣으면 죽는다 | 이번 — 코드 블록으로 (SC-01 · RE-02) |
| 2 | 게이트 생존 | 확장자 변수를 한 문자열로 두면 확장자 둘에서 zsh 0 줄 — 세 자리 | 이번 — 배열로 (SC-02) |
| 3 | 근거 정합 | 실측 피드백 F19 가 규칙에 없다 | 이번 — K-11 · 원칙 9 · 평가 사례 (SK-01 ~ SK-04) |
| 4 | 근거 정합 | `etc_seq=663` 이름표가 내용보다 넓다 — 원칙 1 · 2 · 5 · 8 이 근거로 든다 | 다음 사이클 |
| 5 | 강도 정합 | C-06 MUST 대 출처 PREFER | 다음 사이클 (기록만) |
| 6 | 축 라벨 | `core-comment.md` §6 주의 사항의 한국어 멀티바이트 한 줄 | 판정 경계 안내라 그대로 |
| 7 | 중복 | `locale-korean.md` §2 표 grep 열과 §8 블록이 같은 패턴 | 실행은 §8 블록. 다음 사이클 메모 |
| 8 | 중복 | K-11 과 K-05 가 같은 예를 잡을 수 있다 | 이번 — 겹침을 판정 문장에 적음 |
| 9 | 트리거 | 새 킷 셋과 배타성 | V4 OK · description 안 바꿈 |
| 10 | 상한 | SKILL.md 줄 수 · `references/` 1 단 · 스킬 셋 | 해당 없음 |

## tone-kaizen 사이클 1 (2026-09-25)

| # | 축 | 변경 | 근거 |
| --- | --- | --- | --- |
| 1 | 근거 정합 | K-11 새 이름을 만들지 않는다(관측 컨벤션) · 원칙 9 · 평가 사례 4 | 처리 배정표 `F19` · `reflect-collector:P6`, 근거 파일 §2-1 |
| 2 | 게이트 생존 | 이름 게이트 G-1 · G-2 · G-5 · G-6 을 표 칸에서 코드 블록으로 | 봉인 전 실측 — bash · zsh 0 건 · 종료 코드 1, G-6 은 전 줄 |
| 3 | 게이트 생존 | 확장자 변수 세 자리를 배열로 | 봉인 전 실측 — 한 문자열이면 zsh 0 건 |

회귀: 등록된 검사 전부 OK · evals 4/4 PASS · 배타성 위반 0 (V4 OK, description 안 바꿈).
다음 사이클 이월: 아래 `## 다음 사이클 메모`.

## 바꾼 파일

- `tone-kit/references/locale-korean.md` — 규칙표 K-11 행(관측 컨벤션) · §4 끝 K-11 문단(판정은 처음 읽는 사람 기준 · 괄호로 뜻 · K-05 겹침 · §8 에 grep 없음) · §10 출처 셋과 세션 관찰
- `tone-kit/references/sources.md` — `확인됨` 표기에 날짜 괄호 규칙 · 로케일 표 세 행 `확인됨 (2026-09-24)` · K-11 이 관측 컨벤션인 까닭 한 문단
- `tone-kit/references/core-naming.md` — §8 표는 ID · 대응 규칙 · 잡는 것만, 명령 여덟은 코드 블록 하나로(G-1 ~ G-8 차례), `INC` 를 배열로, 표 칸 함정 한 문장
- `tone-kit/references/core-comment.md` — §6 `X` 를 배열로, 여덟 줄의 `$X` 를 `"${X[@]}"` 로
- `tone-kit/evals/evals.json` — 사례 4 (tone-guide · K-11, 예는 음역이 안 섞인 `차례칸`)
- `docs/tone/korean-technical-writing.md` — 잡는 것 한 줄 · 원칙 9 · 안티패턴 한 행 · `last_updated`
- `docs/tone/research-log.md` — `## 2026-09-24 — 카이젠 Phase 15 근거 조회` 절 · `last_updated`
- `docs/tone/overview.md` — 게이트 예시 `INC` 를 배열로 · `last_updated`

## 반영한 처리 배정표 키

| 키 | 반영 |
| --- | --- |
| `F19` | 세션 `8fa13c90`(2026-09-19)의 새 합성어를 규칙으로 — K-11 · 원칙 9 · 평가 사례 4 |
| `reflect-collector:P6` | K-11 을 관측 컨벤션으로 넣었다. 판정어는 근거 파일 권장안 2 에 따라 「사전에 없는」 대신 「처음 읽는 사람이 뜻을 짐작할 수 있는가」 (한글 맞춤법 제50항 해설이 사전에 없는 전문 용어를 정당하게 본다) |

카이젠 스킬 Step 2 `게이트 생존` 축에서 찾은 것(처리 배정표 밖): 이름 게이트 넷 복구 · 확장자 변수 배열 — 오케스트레이터 Phase 15 지시(bash · zsh 양쪽과 합성 양성 케이스)대로 SC-01 · SC-02 가 두 셸로 잰다.

### Phase 1 결과 대조 (오케스트레이터 Gotcha 「Phase 1 에서 가이드를 변경했으면 전수 체크」)

| Phase 1 변경 | tone-kit 에서 본 자리 | 처리 |
| --- | --- | --- |
| §3.7 `[미검증]` 네 칸 | 없음 (`grep -rn '미검증' tone-kit` 0 줄) | 해당 없음 |
| §3.7 알려진 답 대조 | 새로 짠 측정 — 이름 게이트 블록 실행 · 확장자 둘 실행 | SC-01 이 손으로 센 답 여덟 줄로 잰다 |
| agent 가이드 §10 | 이 킷에 에이전트가 없다 | 해당 없음 |

## 미반영 키와 사유

- 처리 배정표 키 가운데 미반영은 없다(배정 `Phase 15` 행은 `F19` · `reflect-collector:P6` 둘)
- 근거 파일 §2-2 · §4 권장안 5 (C-06 MUST 가 출처 PREFER 를 넘는다) — tone-kaizen Gotcha 3(한 사이클 관심사 1 ~ 2 개) 가운데 둘을 배정 키와 게이트 생존에 썼다. research-log 에 기록만
- 근거 파일 §2-3 (`etc_seq=663` 이름표) — K-11 근거로는 쓰지 않았다(AR-02 `cite663=0`). 이름표를 고치면 원칙 1 · 2 · 5 · 8 근거를 다시 봐야 해서 다음 사이클
- 근거 파일 §3 · §4 권장안 6 ~ 8 (현행화 목록) — research-log 에 낡은 곳 목록만 남겼다
- 평가 사례 4 를 실제 모델로 돌려 보는 일 — LLM 실행이라 이 Phase 몫이 아니다(계약 판정 한계). `run-evals.py` 는 구조만 잰다

## 넘기는 것

| 파일 | 할 일 | 맡을 곳 |
| --- | --- | --- |
| `docs/tone-kit/korean-technical-writing.html` | 원칙 9 · 잡는 것 · 안티패턴 행이 들어간 리서치 문서를 다시 만든다 | Final F2 |
| `docs/tone-kit/overview.html` | 게이트 예시 `INC` 배열 판으로 다시 만든다 | Final F2 |
| `.claude/skills/tone-kaizen/SKILL.md` | Step 1 의 「`tone-kit/templates/*.md` 8종」 — 실제 6 개. 레포 전용 파일이라 이 Phase 범위 밖 | Final |
| `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md` | `:230` 필수 출처 7 번 이름 「국립국어원 공공언어」 — 실제 내용은 보도자료 작성 길잡이(근거 §2-3) | Final |
| `tone-kit/.claude-plugin/plugin.json` | 버전 (이 Phase 는 버전을 적지 않았다 — AP-01) | Final |

## changelog 한 단락

tone-kit — 한국어 규칙에 K-11 「새 이름을 만들지 않는다」 를 관측 컨벤션으로 넣었다. 대상을 부를 이름이 있으면 그 이름을 쓰고, 없으면 하는 일을 문장으로 풀어 쓴다.
판정 기준은 사전에 실렸는지가 아니라 처음 읽는 사람이 뜻을 짐작할 수 있는가다. 리서치 문서 원칙 9 와 평가 사례 4 가 같은 말을 한다.
`core-naming.md` §8 의 이름 게이트 넷(G-1 · G-2 · G-5 · G-6)은 표 칸에 적혀 붙여 넣으면 `\|` 가 글자로 읽혀 0 건이나 파일 전 줄을 냈다 — 명령을 코드 블록으로 옮겼다.
확장자 변수는 한 문자열이면 zsh 가 나누지 않아 확장자 둘에서 0 건이 됐다 — `core-naming.md` §8 · `core-comment.md` §6 · 개요 예시 세 자리를 배열로 바꿨다.

## 킷 로그 한 단락

2026-09-24 Phase 15 — K-11 근거: Microsoft 문서 스타일 가이드는 이미 있는 말로 충분하면 새 말을 만들지 말라고 한다
(<https://github.com/MicrosoftDocs/microsoft-style-guide/blob/main/styleguide/word-choice/use-technical-terms-carefully.md>).
Google 문서 스타일 가이드는 피해 쓸 수 있는가 → 더 구체적인 말로 → 꼭 쓰면 처음 나올 때 풀어 쓴다는 순서를 권한다(<https://developers.google.com/style/jargon>).
한글 맞춤법 제50항 해설은 사전에 없는 전문 용어도 정당한 말로 다룬다 — 그래서 판정 기준을 사전 등재로 두지 않았다(<https://korean.go.kr/kornorms/regltn/regltnView.do?regltn_code=0001>).
C-06 강도 초과 기록의 원문은 <https://dart.dev/effective-dart/documentation> · <https://dart.dev/tools/linter-rules/public_member_api_docs> 다.
`etc_seq=663`(<https://korean.go.kr/front/etcData/etcDataView.do?etc_seq=663>)은 보도자료 작성 길잡이라 K-11 근거로 쓰지 않았다.

## 다음 사이클 메모

- C-06(공개 멤버 doc 주석) MUST 대 출처 PREFER — Effective Dart 는 PREFER, 린트 설명은 DO 라 출처끼리도 어긋난다. 강도를 SHOULD 로 낮출지 본다
- `etc_seq=663` 이름표 「국립국어원 공공언어 자료」 가 실제 내용(보도자료 작성 길잡이, 2021)보다 넓다 — 원칙 1 · 2 · 5 · 8 의 근거를 다시 본다
- 문서 예시의 `__` 두 곳(`docs/tone/overview.md` 등) — Dart 3.7 부터 `_` 를 여러 번 쓸 수 있어 `(_, _)` 로. 린트 `unnecessary_underscores`
- 제스처 콜백 58 개의 기준 버전 표기(3.38.4) — Flutter 3.47.5 원본에서도 58 개로 같다. 기준 버전을 3.47.5 로 올리거나 두 판에서 같다고 적는다
- go_router 예제 링크(`sources.md` 의 16.3.0 예제) — 최신은 18.0.1 이다. 17.0.0 에 깨지는 변경이 있고 18.0.0 은 `material_ui` 로 옮겼다 — 예제를 다시 읽고 바꾼다
- 위키 `Style-guide-for-Flutter-repo` 가 저장소 `docs/contributing/` 로 옮겨졌다 — `sources.md` 의 「주의 (위키 이전 이력 있음)」 줄을 새 주소로
- `material_ui` 분리 공지 — SDK 저장소에는 파일이 아직 있어 링크를 지금 바꿀 근거가 부족하다. `sources.md` 에 주의 표기와 날짜만 남길지 본다
- `locale-korean.md` §2 표의 grep 열은 표 칸이라 `\|` 로 적혀 있다 — 붙여 넣으면 죽는다. 실행은 §8 블록이 한다. 표 열을 없애거나 §8 을 가리키게 한다
- `sources.md` 로케일 절의 「위 표의 마지막 세 행」 — 행이 늘면 틀린다. 세 출처 이름으로 바꾼다
- `save-feedback.sh` 가 이 워크트리에서 `project_name: 'kaizen-0924'`(워크트리 이름)를 적었다 — Phase 4 · Phase 12 몫과 같은 문제
