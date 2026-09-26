# c4c — rust-kit 특정 앱 이름 일괄 치환

- 계약: `.harness/sprint-contract-after-0924-rust-app-name.md` (17 조건, 봉인 `sha256:85bde798533363bf`, `locked_at` 2026-09-26 12:29)
- 가지: `chore/ak-c4c` (시작 커밋 `f81568d`)
- QA 판정은 아직이다. 다음 단계의 qa-evaluator 가 한다. 계약 `status` 는 `active` 그대로 두었다.

## 한 일

| 커밋 | 내용 |
| --- | --- |
| `6696bd8` | 계약 봉인. 계약 파일 하나만 실었다 (`git show --name-only` 1 개) |
| `1b3e53d` | rust-kit 14 파일에 대응표 16 행을 `apply-map.py` 로 한 번 적용. 66 줄 바뀜, 표준 오류 `rule1=1 … rule14=6 rule15=2 rule16=10` |
| 이 notes 커밋 | `.harness/.meta/after-kaizen-0926/c4c-notes.md` 하나 |

봉인 전 교차 진단(qa-evaluator)의 세 지적을 계약에 넣은 뒤 봉인했다.

1. SK-03 기대값 일부가 계약이 고치지 않는 세 파일에서 나온다 — `## 범위 경계` 에 「측정 폭」 줄을 더해
   `rust-grpc` 의 `myapp.v1` 1 · `rust-build` 의 `crate-name` 1 · `rust-docker` 의 `postgres://...` 2 와 `appdb` 주소 1 을 적었다.
   기대값과 다르면 이 세 파일부터 보라고 적었다.
2. AR-01 `seal_broken` 이 저장소 전체 계약을 잰다 — 조건 문장에 「다른 계약 봉인도 깨지지 않았다(저장소 전체 검사)」 를 넣고 실측을 적었다.
   교차 진단은 83 개를 「정식 17 · `history/` 66」 이라 했는데, 시작 판 `git archive` 사본에서 다시 세니 `.harness/` 바로 아래 82 · `history/` 1 이었다.
   합계 83 과 `SEAL_OK` 73 · `SEAL_ABSENT` 10 · `SEAL_BROKEN` 0 은 맞았다.
3. 마지막 행이 rust-preflight `:15` · `:19` 에서 조사를 빠뜨린다 — 대응표에 행 15(``fit-pal `server-preflight` `` → ``실사용 프로젝트의 `server-preflight` ``, 2 번)를 넣고
   옛 행 15 를 행 16(10 번)으로 옮겼다. `MAP` · 알려진 답 입력과 기대 출력 · SK-02 규칙별 횟수를 같이 고쳤다.

반영 뒤 봉인 전에 다시 잰 것: 표와 `MAP` 16 쌍 모두 같음 · 알려진 답 `rule1..16=1` 과 기대 출력 `cmp` 같음 ·
시작 판에 대응표를 적용한 규칙별 횟수 = 표 끝 열 · 예행 저장소 `rrepo` 를 새로 만들어 `rh/real` · `rh/good` · 변형 다섯 · `rh/gone` · `rh/none` 에 `m` 전부 — 모두 조건에 적은 값과 같았다.

## 조건별 자기 측정 (끝 판 `1b3e53d`, 봉인된 계약에서 새로 떼어 낸 세 블록)

| 조건 | 출력 |
| --- | --- |
| SK-01 | `end_lines=0 end_rc=1 base_lines=66 users_end=0 users_base=1 g1_lines=1 g1_app=0 g1_neutral=1` |
| SK-02 | `list_match=1 files=14 same=14 diff=0 others_changed=0`, 규칙별 횟수 표 끝 열과 같음, `DIFF` · `OTHER` 0 |
| SK-03 | 조건 문장의 기대 줄과 글자까지 같음 (`units=11 split=0`), `SPLIT` 0 |
| SK-04 | `rust-init=3/3 rust-feature=3/3 rust-service=2/2 rust-api=3/3 decl_rust-init=1 decl_rust-feature=1` |
| SC-00 | `release_paths=0` |
| ER-01 | `files=14 nlines_eq=14 pipes_eq=14 fences_eq=14 odd_backtick_lines=0` |
| AR-01 | `impl_files=14 exact=1 mixed_commits=0 seal_commit_files=1 seal_before_impl=1 seal_broken=0 this=SEAL_OK scope_block=1` |
| AR-02 | `consumers=23 app_hits=0 research_log=7` |
| AP-03 | `v6_rc=0` |
| AP-04 | `skills=12 name=12 fm_same=12` |
| RE-01 | `added=0` |
| RE-02 | `grpc_base=1 grpc_end=1 new_stems=myapp,` |
| DG-01 · DG-03 | `release_sh=0` |
| DG-02 | `md=14 base_warn=162 end_warn=162 new=0` |
| DG-04 | `non_md=0` |
| DG-05 | 시작 판 · 끝 판 모두 `validate-rust=0 sync-docs=0 sync-evals=0 run-evals=0 stale-values=0 docs-links=0 validate-all=0` |

이 notes 커밋은 `.harness/` 안이라 AR-01 의 `impl_files` 에 들어가지 않는다. notes 커밋 뒤 17 조건을 끝 판에서 다시 잰 값은 이 파일을 담은 다음 커밋의 「notes 커밋 뒤 재측정」 절에 적는다.

## 저장소 검사

- `python3 scripts/validate-plugin.py rust-kit` → 종료 코드 0 (V1 ~ V10 OK)
- `python3 scripts/sync-docs.py --check-only` → 0, 「모든 README가 동기화 상태」 — README 갱신 없음
- `python3 scripts/sync-evals.py --check-only` → 0 (added 0 · orphans 0 · missing 0)
- 로컬 CI(`ci-local.sh`, `TMPDIR` 은 다른 묶음과 겹치지 않게 이 세션 임시 폴더로 두었다): 23 단계 중 `rc=0` 22, `feedback-agg-test` 는 `yq` 가 없어 건너뜀. 실패 0.
  CI 파일에만 있는 줄은 설치 단계(`pip install pyyaml` · zsh 설치 · `npm ci` · playwright 설치)뿐이다.
  CI 가 남긴 `__pycache__` 두 폴더는 지웠다 (작업 폴더 변경 0 줄 확인)

## docs 와 원본이 어긋났는지 (`python3 scripts/detect-docs-drift.py --since f81568d`)

```text
rust-kit/references/project-detection.md → docs/rust-kit/project-detection.html  [NEW — 대응 HTML 없음, 신규 생성 + index.html 등록 필요]
```

이 원본에는 원래부터 대응 HTML 쪽이 없다(`docs/rust-kit/` 21 쪽에 없음). 이번 치환이 만든 어긋남이 아니라 원래 있던 빈자리다.
바뀐 SKILL.md 열두 개는 이 스크립트가 보는 대상이 아니다. `docs/rust-kit/*.html` 21 쪽에는 앱 이름이 0 건이라(AR-02) 다시 만들 쪽이 없다.
페이지를 새로 만들지는 부모가 정한다.

## 넘긴 것과 사유

- `docs/rust/research-log.md` 7 건 — 계약 범위 밖(리서치 기록). AR-02 가 그대로 7 건인지 쟀다
- rust-kit 밖 다른 킷(하네스 문서 등)과 `.harness/` 기록 속 같은 이름 — 이 계약 범위(rust-kit) 밖
- rust-test 의 `my-api` · `my-lib` — 다른 예시 블록이고 대응표 밖이라 그대로 두었다
- 계약 파일에 편집기 경고가 있다: MD041(첫 줄 제목 — 계약은 frontmatter 뒤 `## 배경` 으로 시작하는 형식) 한 건과
  MD038(코드 칸 안 앞뒤 공백) 여러 건. MD038 은 대응표 행 2 · 3 · 14 처럼 찾는 글자 끝의 공백 한 칸이 뜻을 가진 칸이라 고치면 대응표 뜻이 바뀐다.
  DG-02 는 rust-kit 14 파일만 재고, 계약은 봉인 뒤 조건 줄을 못 고치므로 그대로 둔다

## 킷별 버전 판단

- rust-kit: **patch**. 스킬 · 에이전트 · 설정 추가나 삭제 없이 문서 14 개의 글자만 바뀌었다.
  스킬이 보여 주는 예시 이름(`myapp-api` 등)이 바뀌지만 스킬이 하는 일과 부르는 말(트리거)은 그대로다
- 다른 킷: 변경 없음

## 톤 규칙 대조 (tone-kit:tone-guide 1 단계 · 5 단계)

1 단계: `.claude/tone-project.md`(어댑터 없음 · 주석 언어 ko)를 읽고 `core-comment.md` · `core-naming.md` · `core-structure.md` · `core-antipatterns.md` · `locale-korean.md` 를 읽었다.
어댑터가 없어 스택별 검사는 쓰지 않고 코어와 한국어 규칙만 댔다.

5 단계: 바뀐 줄(추가 66 줄 · 삭제 66 줄)과 바뀐 파일 전체를 대상으로 돌렸다.

| 패턴 / 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-02 번역투 여섯(locale §8 G-1) — 추가 줄 | 0 | 통과 |
| K-02 번역투 — 바뀐 파일 전체 | 시작 판 5 · 끝 판 5 | 통과 — 새로 생긴 것 0, 다섯은 이번에 안 건드린 줄 |
| K-04 · locale G-2 doc `합니다`체 | 0 | 통과 (`///` doc 없음) |
| K-07 · locale G-3 라벨 파손 · G-4 `- 반환값:` | 0 · 0 | 통과 (라벨 없음) |
| K-11 새로 만든 이름 | 「실사용 프로젝트」 57 · 「서버 규칙」 34 | 통과 — 처음 읽는 사람도 뜻을 짐작하는 풀어 쓴 말이다. 합성어나 비유가 아니다 |
| K-05 외래어 · 음역 | 새 음역 0 | 통과 |
| C-10 디자인 툴 참조 (core §6 G2 · G3 · G4) | 0 · 3 · 0 | 통과 — G3 세 건은 `https://` 주소와 코드 주석 속 파일 경로이고 같은 줄이 시작 판에도 있다 |
| C-12 계산 근거 (G6) | 1 | 통과 — 주소 뒤 날짜가 걸린 것, 시작 판에도 같은 줄 |
| C-04 · C-13 · G1 · G5 · G7 · G8 | 0 | 통과 |
| C-01 · C-02 · C-15 — 바뀐 주석 두 줄 (`# 추가 deny (2026 실사용 프로젝트 세트)`, `// … 별도 myapp-migration 바이너리`) | 2 | 통과 — 이름만 바뀌었고 주석이 하는 말은 그대로 |
| N-01 ~ N-12 이름 | `myapp` · `myapp-api` · `myapp-migration` | 통과 — rust-grpc 의 `myapp.v1` 과 같은 계열(N-10), 한 글자 이름 0 (N-08) |
| S-01 ~ S-14 구조 | — | 해당 없음 (구조 변경 없음) |
| 안티패턴 A ~ J | — | 해당 없음. H(좋은 주석)로 볼 줄을 지운 것 0 — 이번 변경은 줄을 지우지 않았다 (ER-01 `nlines_eq=14`) |
| locale §9 자기모순 검사 — 이번에 계약에 더한 줄 | 0 | 통과 |

## 측정 도구 경로

- 임시 폴더: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/c4c/`
  - `impl/measure-real.sh` — 봉인된 계약에서 세 블록을 새로 떼어 이 가지에 `m` 전부를 돌린다. 출력은 `impl/measure-real.out`
  - `impl/verify1.sh` — 표와 `MAP` 대조 · 알려진 답 · 시작 판 규칙별 횟수 · SK-03 파일별 출처 · 계약 봉인 83 개 세기
  - `impl/rerun.sh` · `rehearse.sh` · `rehearse2.sh` · `rehearse3.sh` · `run-m.sh` — 예행 저장소 `rrepo/` 와 변형 가지
  - `impl/tone5.sh` — 톤 5 단계 대조
  - `ci/ci-local/summary.txt` — 로컬 CI 요약
  - `mdlint/node_modules/.bin/markdownlint-cli2` — DG-02 가 쓰는 markdownlint-cli2 0.23.2
- 계약 피드백: `/Users/jackson/.harness/feedback/contract/1a3bcba6-2026-09-26T123014-bda55d45-31568.yaml` (`verify-feedback.sh` PASS)
