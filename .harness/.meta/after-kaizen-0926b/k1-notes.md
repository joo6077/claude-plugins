# k1 메모 — flutter-toolkit · react-kit · planning-kit 남은 것

- 계약: `.harness/sprint-contract-after-0926-kits-flutter-react-planning.md` (봉인 커밋 `6d073dd`, `conditions_digest: sha256:534198c0775e068c`, `measurement_digest: sha256:e957eecfbfa776f5`)
- 가지 `chore/ak2-k1`, 시작점 `6378948`
- 위임: 세션 `bda55d45-296c-491f-89ba-b52042d58e72`, 2026-09-26T10:09:00.557Z · 결정 답 2026-09-26T10:30:16.222Z. 사용자에게 묻지 않았다
- 계약 피드백: `/Users/jackson/.harness/feedback/contract/1a3bcba6-2026-09-26T210301-bda55d45-33407.yaml` (verify-feedback PASS, `cross_diagnosis_by: qa-evaluator`)

## 커밋

| 해시 | 자리 | 한 줄 |
| --- | --- | --- |
| `6d073dd` | `.harness` | 계약 봉인 (29 조건) |
| `59e0577` | flutter-toolkit | 미검증 규칙 v5.1 사본 · 실패 원인 가르기 · codegen 안내 정리 |
| `e3e48a9` | 루트 `CLAUDE.md` | 평가 사례 수 두 문장을 24 로 |
| `1f2bcd0` | react-kit | ViewTransition Tier 2 가르기 · 실패 원인 가르기 · 감지 스크립트 호출 |
| `38370d3` | react-kit | react-animation 제목 줄 (MD041 새 경고 없애기) |
| `1198668` | planning-kit | plan-sync-github Gotcha 4 에 GitHub 문서 버전 날짜 |
| `afb07b7` | `docs/react` | 설계 문서 여덟 현행화 · research-log 뷰 전환 줄 |
| `5e297c9` | flutter-toolkit | 실패 원인 가르기 절의 codegen 명령 줄을 단계 이름으로 (SK-08 플래그 줄 수 2 유지) |

## 항목별 결과

| ID | 결과 | 근거 |
| --- | --- | --- |
| KF-1 | 계약대로 고침 — `59e0577` · `e3e48a9` | `flutter-toolkit/evals/evals.json` 사례 24(widget-inspector, 「관례 표 없는 호출」, 단언 `건너뜀 — 관례 표 없는 호출`). 루트 `CLAUDE.md` 두 문장 24개 |
| KF-2 | 계약대로 고침 — `59e0577` | flutter-audit `## Unverified-Evidence Protocol` 을 `harness/docs/guides/qa-evaluation-guide.md` v5.1 사본으로(번호 목록 · 4 요건), 적용 메모 · 보고 틀 · Rules 에 `env_gaps` · `invalid_evidence` |
| KF-3 | 계약대로 고침 — `59e0577` | flutter-kaizen Gotchas 에 Makefile 규칙(Step 2b) 네 파일을 허용 경로에 처음부터 넣으라는 줄 |
| KF-4 codegen 안내 셋 · 사례 18 · 플래그 | 계약대로 고침 — `59e0577` | flutter-api · flutter-feature · flutter-screen 안내가 `flutter-run` `### codegen [feature]` 의 전후 삭제 수를 가리킨다. 사례 18 단언이 `$FLUTTER test`. flutter-build Gotcha 는 EX-5 대로 무시 전환 2.7.0 |
| KF-4 flutter-audit `:50` | 처리됨 — SK-01 사본 교체로 함께 | 조항 5 가 원문 v5.1 글자 그대로다 |
| KF-4 go_router 18 · auto_route 11.1 | 바깥 근거 없음 | EX 대조 결과에 이 둘이 없다. 지금 문장이 틀렸다는 근거도 없다(`.harness/.meta/kaizen-0924/phase5-notes.md:78`) |
| KRe-1 `<ViewTransition>` Tier 2 | 계약대로 고침 — `1f2bcd0` · `afb07b7` | react-animation Gotcha 15 · animation-architect-react 허용 도구 줄 · g5b §2.1b · research-log 두 줄 |
| KRe-1 `<Activity>` canary | 바깥 근거 없음 | EX-9 가 `<Activity>` 의 안정 · 실험 상태를 판정하지 못했다. react-screen Gotcha 11 은 그대로 뒀다 |
| KRe-1 react-reviewer §10 | 처리됨 | c4b 커밋 `446428a` 가 사본을 v5.1 로 옮겼다(`react-kit/agents/react-reviewer.md:169` · `:228`) |
| KRe-1 `project-detect.sh` | 계약대로 고침 — `1f2bcd0` | `react-kit/references/project-detection.md` 가 `bash "$REACT_KIT/scripts/project-detect.sh"` 를 부른다. 스크립트는 안 바꿨다. 결정은 「참조 문서가 부른다」 — 스킬마다 실행 줄을 따로 넣지 않았다(범위 경계의 의도한 좁힘) |
| KRe-1 · UD-6 설계 문서 | 계약대로 고침 — `afb07b7` | 여덟 문서 `last_updated: 2026-09-26` · 「현행화 기록」 절에 커밋 47 개. g6 strictPort · 7 단계 · passed/skipped · 실패 원인 가르기 · BLOCKED, g1 strictPort · 13 단계 틀, g5b `<ViewTransition>`, final-integration 트리 |
| KP-1 GitHub 문서 날짜 | 계약대로 고침 — `1198668` | plan-sync-github Gotcha 4 에 `2022-11-28` 지원 기한 2028-03-10 · 최신 `2026-03-10`. 링크의 `apiVersion=2022-11-28` 두 곳은 그대로 |
| KP-1 Mermaid 12 | 처리됨 | 커밋 `bbdebaf` 가 `docs/planning/flows.md:53` · `data-modeling.md:78` 을 고쳤고 EX-10 이 「맞음」 으로 판정. 열린 질문 하나 — `flows.md:53` 의 「최신 안정판」 수식어는 원문 직접 인용이 아니다(EX-10 §4) |
| KP-1 PRD 와 결정 기록(ADR) 비교 | 바깥 근거 없음 | EX-10 이 이 비교 자료를 다루지 않았다 |
| UD-1 | 그대로 유지 | build_runner `--delete-conflicting-outputs` 는 세 스킬에 각 2 줄 그대로(SK-08 `flags=[2/2 2/2 2/2]`). `react-kit/templates/` 는 안 바꿨다 |
| UD-3 | 계약대로 고침 — `59e0577` · `1f2bcd0` | flutter-preflight · react-preflight 에 `## 실패 원인 가르기` — `harness/skills/sprint/SKILL.md` Step 3 판정 표 다섯 줄 사본 + 준비 명령(`$FLUTTER pub get` · `pnpm install --frozen-lockfile`) |
| UD-6 | 계약대로 고침 — `afb07b7` | 위 KRe-1 · UD-6 줄 |

## 넘긴 것 (범위 경계 약속 셋)

- KF-2: `scripts/check-reviewer-protocol-copies.py` 의 `REVIEWERS` 목록에 flutter-audit 를 넣는 일은 `scripts/` 라 이 묶음 밖이다 — scripts 묶음으로 넘긴다. 지금은 계약 SK-01 이 같은 함수로 사본 일치를 한 번 쟀을 뿐, CI 는 flutter-audit 사본을 지키지 않는다
- KF-4: `docs/flutter/research-log.md:19` 의 2026-09-24 조사 기록(「2.16 부터 … 제거된 호환 옵션 목록으로 옮겨졌다」)은 그날 기록이라 두었다. EX-5 판정으로는 무시 전환이 2.7.0 이다 — `docs/flutter/` 는 이 계약 범위 밖이라 고치지 않았다
- UD-3: 두 preflight 절은 시작 판 `harness/skills/sprint/SKILL.md` Step 3 의 사본이다. 다른 묶음이 원문 조각이나 판정 표를 바꾸면 두 사본 동기화는 그 묶음 몫이다

## 바깥 근거 인용

- EX-5 — `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/ex/EX-5.md`, 원문 <https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md> (2.7.0 「Ignore `-d` flag」 · 2.16.0) · <https://raw.githubusercontent.com/dart-lang/build/master/build_runner/lib/src/build_runner_command_line.dart> 「Removed options, kept to not break old command lines.」
- EX-9 — `.../ex/EX-9.md`, 원문 <https://react.dev/blog/2026/09/09/react-19-3> 「We shared it as an experimental API last year, and in 19.3 it's stable and ready to use.」
- EX-10 — `.../ex/EX-10.md`, 원문 <https://docs.github.com/en/rest/about-the-rest-api/api-versions> 「The API version `2026-03-10` was released on Tue, 10 Mar 2026.」 · 「`2022-11-28` \| March 10, 2028」, <https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0>

## 킷별 버전 판단 (릴리스는 부모 몫)

| 킷 | 올림 | 이유 |
| --- | --- | --- |
| flutter-toolkit | minor | flutter-audit 보고 틀에 두 카운터가 생겼고(보고 모양 변경), flutter-preflight 에 새 절차 절, 평가 사례 하나 추가 |
| react-kit | minor | react-preflight 새 절차 절 · react-animation 새 판정 규칙(Gotcha 15) · 감지 절차가 스크립트를 부름 |
| planning-kit | patch | Gotcha 한 줄에 사실만 더했다 |

## 문서 사이트 드리프트 (재생성은 부모 몫)

`python3 scripts/detect-docs-drift.py --since 6378948` (끝점에서 실행, 종료 코드 0) 가 낸 페이지 열 개 — 모두 NEW(대응 HTML 없음):

- `docs/react-kit/final-integration.html`
- `docs/react-kit/g1-scaffolding.html`
- `docs/react-kit/g2-state-data.html`
- `docs/react-kit/g3-performance.html`
- `docs/react-kit/g4-quality.html`
- `docs/react-kit/g5-ui-patterns.html`
- `docs/react-kit/g5b-animation.html`
- `docs/react-kit/g6-build-audit.html`
- `docs/react-kit/research-log.html`
- `docs/react-kit/project-detection.html`

주의: 이미 있는 페이지 이름은 `docs/react-kit/scaffolding.html` · `state-data.html` · `performance.html` · `quality.html` · `ui-patterns.html` · `animation.html` · `build-audit.html` · `integration.html` 이다. 도구가 원본 파일 이름(`g1-` 접두)을 그대로 쓰는 탓에 이 여덟을 STALE 대신 NEW 로 낸 것으로 보인다 — 새 페이지를 만들기 전에 기존 페이지를 다시 만드는 쪽인지 문서 사이트 묶음이 정해야 한다. flutter-toolkit · planning-kit 에서 바꾼 파일은 도구가 대응 페이지를 내지 않았다.

## tone-guide 대조

1 단계: `tone-kit:tone-guide` 를 Skill 로 불렀고, 규칙은 이 가지의 `tone-kit/references/` 를 읽었다 — `.claude/tone-project.md`(어댑터 없음 · 주석 언어 ko), `locale-korean.md` 전문, `core-comment.md` · `core-naming.md` · `core-structure.md` 규칙표, `core-antipatterns.md` 요약표.

5 단계: 대상은 `git diff -U0 6378948 HEAD -- '*.md' '*.json' ':(exclude).harness/*'` 의 더한 줄 302 줄.

| 규칙 | 건수 | 판정 |
| --- | --- | --- |
| K-02 · §8 G-1 번역투 여섯 | 1 | 통과 — 1 건(「적용된다」)은 flutter-audit 의 v5.1 사본 줄이라 글자 그대로 옮겨야 한다(SK-01) |
| K-04 · §8 G-2 `합니다`체 | 0 | 통과 |
| K-03 능동형 · 주체 직설 | 리뷰 | 통과 — 새 절은 「~를 센다 · 돌린다 · 가른다」 꼴 |
| K-05 외래어 | 리뷰 | 통과 — 공식 이름(`<ViewTransition>` · `strictPort` · `startTransition`)은 원문 그대로 |
| K-06 · A 이름 번역 주석 | 0 | 통과 — 코드 주석을 더하지 않았다 |
| K-10 대조 grep · 자기모순 검사 | 실행 | 이 표가 결과다. 자기모순 잔존 0 건(사본 줄 제외) |
| K-11 새로 만든 이름 | 0 | 통과 — 「실패 원인 가르기」 는 sprint Step 3 의 원래 이름, 「기준 원본」 은 풀어 쓴 말 |
| C-01 · C-02 why 만 | 리뷰 | 통과 — Gotcha 줄마다 이유(무엇이 깨지는지)를 붙였다 |
| C-10 · C-13 툴 참조 · 자화자찬 | 0 | 통과 |
| H 보존 | 리뷰 | 통과 — 지운 줄은 옛 다섯 조항 · 옛 build_runner 문장 · g6 `8. audit` 둘 · forwardRef 예시뿐, 모두 새 문장으로 바뀌었다 |
| S-12 같은 자리 같은 모양 (관측 컨벤션) | 2 | 주의 — react-animation · plan-sync-github 의 `# Gotchas` 를 `## Gotchas` 로 낮췄다. react-kit 은 21 스킬 중 7 개가 이미 `## Gotchas` 라 섞여 있었고, planning-kit 은 12 개 모두 `# Gotchas` 라 plan-sync-github 만 달라졌다. 아래 「남은 것」 첫 줄 |
| 쉬운 말 목록 | 리뷰 | 더한 줄에 목록 낱말이 여덟 번 나오지만 모두 기존 줄의 나머지(「스키마」 · 표 칸 「코드 스캐폴딩」) 이거나 v5.1 사본 글자다. flutter-audit 머리 인용에서 새로 쓴 문장의 「정본」 은 QA 1 차 지적 뒤 「원문」 으로 바꿨다(`7c51d87`). 첫 줄 「정본(SSOT)」 은 시작 판부터 있던 줄이다 |

## 조건 자기 측정 (끝점 기준, 계약 측정 도우미)

측정 도우미 사본: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/k1/m.sh` (계약 「회귀 게이트」 블록을 뗀 것). 작업 폴더 판을 재는 보조 `runwt.sh`, 마크다운 새 경고 `mdwt.sh` 도 같은 폴더에 있다. 로컬 CI 는 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh`.

끝점 `6f421dd`(이 줄을 더하기 직전 커밋)에서 `m` 으로 잰 값. 출력 원문: 같은 폴더 `final-measure-2.out`.

| 조건 | 값 | 기대 |
| --- | --- | --- |
| SK-01 | `clauses=1 req=1 prov=1 old=0 md029=1/1` | 맞음 |
| SK-02 | `env_gaps=3 invalid=3 rep_env=1 rep_inv=1 rule_old=0 rule_inv=1 l3_4req=1` | 맞음 |
| SK-03 | `cases=24 ids_ok=1 skip_case=1 case16_same=1` · `Total: 24 passed, 0 failed` 종료 코드 0 | 맞음 |
| SK-04 | `cases=24 commands=24개 conventions=24개` | 맞음 |
| SK-05 | `1` | 맞음 |
| SK-06 | `api=1 feature=1 screen=1` | 맞음 |
| SK-07 | `flutter_test=1 dart_verify=0 skill=flutter-test` | 맞음 |
| SK-08 | `old216=0 joined=1 flags=[2/2 2/2 2/2]` | 맞음 (중간에 `2/3` 이 나와 `5e297c9` 로 고쳤다) |
| SK-09 · SK-10 | 둘 다 `sec=24 prov=1 rows=5/5 merge_base=2 wt=1 prep=2` | 맞음 |
| SK-11 | `gotcha=1 wrapper=6/7 agent=1` | 맞음 (「남은 것」 첫 줄 참조) |
| SK-12 | `call=1 keys_same=1 nkeys=11 script_changed=0` | 맞음 |
| SK-13 | `1` · `apiVersion=2022-11-28` 2 | 맞음 (「남은 것」 첫 줄 참조) |
| SK-14 | `row=2 canary_wait=0 v193=2` | 맞음 |
| SK-15 | 여덟 줄 모두 `lu=1 … miss=0` (commits 9 · 7 · 2 · 6 · 3 · 5 · 9 · 6 = 47) | 맞음 |
| SK-16 | `dev_strict=1 step8=0 passed=1 skipped=1 split=1 verdict=1` · `g1_tpl=1 g1_strict=4 vt=4 fi_link=2 rep=2,2,2,2,2,3,` | 맞음 |
| ER-01 | `flutter=[0 1 1] react=[0 1 1]` | 맞음 |
| AR-01 | `changed=25 extra=0 multi_top=0 flutter=8 react=4 planning=1 docs_react=9 root=1` | 맞음 (이 줄을 더한 뒤 다시 잰다) |
| AR-02 | `committed=1` 과 스물셋 모두 1 이상 · `rc=0 pages=10 miss=0` | 맞음 (이 줄을 더한 뒤 다시 잰다) |
| AP-03 · AP-04 | validate-plugin 종료 코드 0 · 0 | 맞음 |
| SC-00 · RE-01 · DG-01 · DG-03 | 0 · 0 줄 · 0 · 0 | 맞음 |
| DG-02 | `md_new=0 json_bad=0` | 맞음 |
| DG-05 | 끝점 `6f421dd`, 작업 폴더 깨끗, `rc=0` 25 줄 · 나머지 한 줄 `feedback-agg-test SKIP (yq 없음)` (요약: 같은 폴더 `ci-final/ci-local/summary.txt`) | 맞음 |

## QA 1 차 REJECT 뒤 고친 것

QA 가 끝점 `e4f63d8` 에서 찾은 여섯 건과 처리. 커밋은 `729c110`(react-kit) · `899d2ab`(docs/react) · `7c51d87`(flutter-toolkit).

| # | 지적 | 처리 |
| --- | --- | --- |
| 1 | `project-detection.md` 가 「시험이 11 키를 지킨다」 고 적었는데 시험은 `tanstackRouter` 하나만 잰다 | 고침 — 시험은 `tanstackRouter` 값만 재고 나머지 키를 재는 시험은 없다고 적었다. `final-integration.md` 트리 주석도 같은 뜻으로 |
| 2 | `final-integration.md` Quickstart 번호가 1 · 2 · 4 · 5 · 6 | 고침 — 1~5 로 이었다 |
| 3 | react-animation 본문(1 절 티어 표 · 5.1 절)에 `<ViewTransition>` 길이 없다 | 고침 — 티어 표 T2 칸에 두 길을 적고, 5.1 절에 「이 길은 래퍼 가드를 거치지 않는다 · §3.4 CSS 규칙을 두고 두 시점 캡처로 확인 · 못 하면 `[미검증]`」 을 더했다. CSS 규칙이 `<ViewTransition>` 에도 먹는지는 EX-9 에 없어 바깥 근거 없음으로 적었다 |
| 4 | flutter-audit 보고 틀에 결론 줄이 없고 끝 줄 · 환경 배제 판정 · Rules 가 옛 한 카운터 표기 | 고침 — 끝 줄을 `env_gaps N · invalid_evidence N` 로, 결론 줄(통과 · 통과 아님 · 검증 부족)을 더했다. 환경 배제 판정 · 보고 틀 · Rules 줄은 4 요건에 따라 `:ENV` · `:INVALID` 로, Evidence Validity 무효 합산처는 `invalid_evidence` 로 |
| 5 | react-animation · plan-sync-github 의 `# Gotchas` → `## Gotchas` 와 새 H1 은 최소 변경 위반 | 그대로 둠 — 되돌리면 SK-11 · SK-13 측정(`secx '## Gotchas'`)이 절을 못 찾는다. 측정 머리를 `# Gotchas` 로 바꾸는 개정은 되돌린 판이 옛 측정에서 FAIL 하고 새 측정에서 PASS 하므로 느슨해지는 쪽이라 위임으로 동의할 수 없다. 되돌릴지는 사용자가 정한다 — 아래 「남은 것」 첫 줄 |
| 6 | 새로 쓴 문장의 「정본」 | 고침 — 「원문」 |

다시 잰 값(끝점 `7c51d87`, 계약 측정 도우미 `m`): SK-02 `env_gaps=6 invalid=7 rep_env=1 rep_inv=1 rule_old=0 rule_inv=1 l3_4req=1` · SK-11 `gotcha=1 wrapper=6/8 agent=1` · SK-12 `call=1 keys_same=1 nkeys=11 script_changed=0` · AR-01 `changed=25 extra=0 multi_top=0` · AR-02 `rc=0 pages=10 miss=0` · DG-02 `md_new=0 json_bad=0`. 나머지 조건 값은 위 표와 같다. 출력 원문: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/k1fix/`.

## 남은 것

- **SK-11 · SK-13 측정이 시작 판에서 죽어 있었다.** 두 조건의 측정은 `secx '## Gotchas'` 인데 react-animation · plan-sync-github 의 머리는 `# Gotchas` 였다. 그래서 시작 판 `gotcha=0` · `0` 은 「줄이 없다」 가 아니라 「절을 못 찾았다」 였다(양성 대조가 없던 조건). 조건 문장이 「`## Gotchas` 절에」 라고 적었으므로, 측정을 바꾸는 개정(통과 집합이 넓어지는 쪽이라 위임으로 동의할 수 없다) 대신 두 파일의 머리를 `## Gotchas` 로 낮추고 MD041 이 새로 걸리지 않게 H1 제목 줄(`# React Animation` · `# Plan Sync GitHub`)을 앞에 뒀다. QA 가 이 처리를 받아들일지, planning-kit 12 스킬의 머리 모양과 달라진 것을 되돌리고 개정으로 갈지 판단해야 한다
- flutter-audit 사본은 CI 가 지키지 않는다 — 위 「넘긴 것」 KF-2 줄
- `docs/flutter/research-log.md:19` 의 2.16 문장 — 위 「넘긴 것」 KF-4 줄
- 문서 사이트 페이지 열 개 재생성 · 기존 여덟 페이지와의 이름 대응 — 위 드리프트 절
