---
feature: "harness amend_direction — 오라클 변경 amendment 극성 규칙"
slug: harness-amend-direction-baseline-case
created: "2026-09-08 16:40"
complexity: "복잡"
conditions: 18
status: active
owner_session: 0e3335f2-8d08-4e29-8a5d-01ec6b7ed620
conditions_digest: sha256:bef0472d446badb5
locked_at: "2026-09-08 17:05"
---

## 배경

`harness/references/contract-schema.md` §Amendment 사이드카 의 `amend_direction()` 은 두 집합을
`comm` 으로 비교해 `removed>0, added=0 → narrowing` 으로 라벨한다. 이것은 입력이 **허용 집합**
(무엇이 통과하는가)일 때만 맞다. howto-kit 스프린트의 A-01 은 diff-scope 오라클의 **베이스라인**을
바꾼 amendment 였고, 그때 비교한 것은 **측정 집합**(무엇을 재는가)이었다 — 측정 집합이 줄면 통과하는
구현이 늘어나므로 실제 방향은 `relaxing` 인데 헬퍼는 `narrowing` 을 낸다. 극성이 뒤집힌다.

qa-evaluator(iter 4) 가 이것을 Improvement 로 올렸다: *"mechanical `amend_direction()` helper
(designed for allowlist-set comparisons) would mislabel A-01 as `narrowing` if applied naively to a
baseline-change amendment"*.

**공통 전제 (헤더 1 회 선언)**

- CONTRACT_ROOT 는 워크트리 `.claude/worktrees/harness-amend-direction`, 브랜치
  `fix/harness-amend-direction-baseline` (main `4fb1382` 기준, 계약 시점 커밋 0 건).
- 헬퍼는 `contract-schema.md` 코드 펜스에서 추출해 실행한다 (전 조건 공통):
  `awk '/^amend_direction\(\) \{/{p=1} p{print} p&&/^\}$/{exit}' harness/references/contract-schema.md`
  와 같은 방식으로 `amend_direction_oracle` 도 추출한다. 두 함수를 합쳐 `/tmp/hm-helper.sh` 로 두고
  `<셸> -c ". /tmp/hm-helper.sh; <함수> <파일1> <파일2>"` 로 zsh·bash 양쪽 실행한다.
- "zsh·bash 양쪽" 조건은 두 출력이 `diff` 로 동일해야 PASS 다.
- 픽스처는 `harness/evals/amend-direction/` 에 둔다. A-01 실측 집합은 git 에서 재현한 것이다:
  `measured-orig.txt` = `git diff --name-only 4fb1382..37d50a7` (제외 2 pathspec), `measured-amended.txt` =
  `54fb3b3..37d50a7` (같은 제외). `allow-3.txt`/`allow-5.txt` 는 스키마 본문의 실측 위반 사례(3 경로 → 5 경로).

## 리서치 소스

- `harness/references/contract-schema.md:781-789` — `amend_direction()` 현행 정의 (SSOT)
- `harness/agents/qa-evaluator.md:645-649` — 평가자 측 사용 규칙 ("집합형은 comm 으로 계산, 정의는 스키마")
- `harness/skills/sprint-contract/SKILL.md:69` — 작성자 측 Gotcha (같은 취지)
- `harness/docs/guides/qa-evaluation-guide.md:445-448` — 스키마가 SSOT 임을 재확인. 여기는 고치지 않는다
- `.harness/sprint-amendments-howto-kit-implementation.md` (feat/howto-kit) — A-01 원문과 comm 산출
- `.harness/sprint-feedback-howto-kit-implementation.md` (feat/howto-kit) — 평가자가 판정 반전으로 relaxing 을 확정한 기록

## GAP 분석

베이스라인 (2026-09-08, 현행 헬퍼를 A-01 실측 집합에 실행 · bash == zsh):

```text
$ amend_direction measured-orig.txt measured-amended.txt      # 측정 집합 39 → 37
narrowing added=0 removed=2                                  # ← 오라벨. 실제는 relaxing

$ amend_direction allow-3.txt allow-5.txt                     # 허용 집합 3 → 5 (스키마의 실측 위반 사례)
relaxing added=2 removed=0                                   # ← 정상. 이 동작은 유지돼야 한다

$ amend_direction empty.txt empty.txt
unknown added=0 removed=0
$ amend_direction /nonexistent/a /nonexistent/b
sort: No such file or directory (×4)  unknown added=0 removed=0   # ← 조용한 실패
```

두 극성은 대칭이다: 허용 집합에 **추가** = 완화, 측정 집합에서 **제거** = 완화. 헬퍼 하나로 둘을
다루려면 호출자가 환산해야 하는데, 그 환산이 사람이 틀리는 지점이다 (실측: 내가 A-01 에서 틀렸다).
그래서 환산 규칙을 산문으로 적는 것에 그치지 않고 **측정 집합 전용 헬퍼**를 둔다 — 기계 판정이
절차 판정보다 낫다.

소비면 (Step 2.5):
- `harness/agents/qa-evaluator.md` Step 3.3 — 평가자에게 "어느 헬퍼를 쓸지" 를 알려야 한다
- `harness/skills/sprint-contract/SKILL.md` Gotcha — 작성자에게 같은 것
- `docs/harness/contract-schema.html` · `docs/harness/qa-evaluation-guide.html` — HTML 미러. **비범위** (docs-site 사이클)
- `harness/README.md` — `AUTO:evals` 블록이 있으면 새 픽스처 디렉토리로 갱신될 수 있다 → sync-docs 실행 (SC-03)

## 범위 경계

- **비범위**: `qa-evaluation-guide.md` (SSOT 참조만 하므로 변경 불필요) · `docs/` 전체 · 스키마 버전 번호 상향
  (다른 세션의 `fix/contract-schema-unmeasured-oracle` 이 v5.4 를 선점하고 있어 번호 충돌을 피한다 —
  헤더에는 날짜 항목만 추가한다) · `amend_direction()` 본체 수정 (허용 집합 케이스는 옳다).
- diff-scope 베이스라인은 `4fb1382` (계약 시점 `4fb1382..HEAD` 경로 0 건). 워크트리는 이 세션 전용이라
  제외 pathspec 없음. 허용목록에 슬러그 산출물 3 종을 전부 넣는다.
- 커버리지 해소: SC-01·SC-02·ER-01·ER-02 — 산문의 픽스처 파일명과 측정의 파일명이 같은 백틱 표기다.

## 회귀 게이트

`amend_direction()` 의 출력은 바이트 단위로 바뀌지 않아야 한다 (SC-02). 전 킷 `validate-plugin.py`
와 `sync-docs.py --check-only` 가 새로 FAIL 하지 않아야 한다 (SC-03).

## Skill

- [ ] SK-01: `harness/references/contract-schema.md` 의 `## Amendment 사이드카` 섹션(다음 `## ` 헤더 전까지)에
      (a) `amend_direction` 의 입력이 **허용 집합**이라는 극성 규칙과 (b) 오라클(베이스라인·제외 pathspec·측정 명령)을
      바꾸는 amendment 는 **측정 집합**을 `amend_direction_oracle` 에 넣는다는 규칙이 산문으로 있다 [structural]
      (측정: `awk '/^## Amendment 사이드카/{p=1;next} /^## /{p=0} p' harness/references/contract-schema.md` 출력에
      `허용 집합` ≥1, `측정 집합` ≥1, `amend_direction_oracle` ≥1)
- [ ] SK-02: 같은 섹션에 A-01 실측 사례가 worked example 로 있다 — 측정 집합 39 → 37, 헬퍼 출력
      `relaxing measured_removed=2 measured_added=0`, 그리고 같은 입력을 `amend_direction` 에 넣으면
      `narrowing` 이 나온다는 대조 [exact]
      (측정: 위 awk 범위 출력에 `A-01`, `measured_removed=2`, `narrowing added=0 removed=2` 세 문자열 모두 존재)
- [ ] SK-03: 소비면 2 파일 `harness/agents/qa-evaluator.md` 와 `harness/skills/sprint-contract/SKILL.md` 가 각각
      `amend_direction_oracle` 을 **언급**하고 스키마를 SSOT 로 가리키되, 함수 본체를 **재정의하지 않는다**
      [structural, enumerated]
      (측정: 두 파일 각각 `grep -c 'amend_direction_oracle'` ≥1 이고 `grep -c 'amend_direction_oracle() {'` = 0)

## Script

- [ ] SC-01: 스키마에서 추출한 `amend_direction_oracle` 이 `harness/evals/amend-direction/measured-orig.txt` 와
      `harness/evals/amend-direction/measured-amended.txt` 에 대해 `relaxing measured_removed=2 measured_added=0` 을
      출력한다. zsh·bash 양쪽 [exact, enumerated]
      (측정: 2 벌 출력 첨부 + diff 빈 출력)
      음성 대조: 같은 두 파일을 `amend_direction` 에 넣으면 `narrowing added=0 removed=2` — 극성 반전이 곧 구현이며,
      반전을 제거하면 이 측정이 FAIL 한다. 베이스라인이 정확히 그 상태다.
- [ ] SC-02: 회귀 — `amend_direction` 이 `harness/evals/amend-direction/allow-3.txt` 와
      `harness/evals/amend-direction/allow-5.txt` 에 대해 여전히 `relaxing added=2 removed=0` 을 출력하고 (zsh·bash),
      `amend_direction()` 함수 본체가 베이스라인과 **바이트 단위로 동일**하다 [exact, enumerated]
      (측정: 2 벌 출력 첨부 + `git show 4fb1382:harness/references/contract-schema.md` 에서 추출한 함수와 HEAD 에서
      추출한 함수의 `diff` 가 빈 출력)
- [ ] SC-03: `python3 scripts/validate-plugin.py harness` FAIL 0 건, 인자 없는 전 킷 실행에서 `harness` 원인 새 FAIL 0 건,
      `python3 scripts/sync-docs.py harness` 후 `python3 scripts/sync-docs.py --check-only` exit 0 [goal]
      (측정: 명령 출력 전문. 스크립트는 **워크트리의 `scripts/`** 를 쓴다 — 메인 체크아웃 스크립트를 부르면 다른 파일을 잰다)

## Error

- [ ] ER-01: 두 입력이 모두 빈 파일이면 `amend_direction_oracle` 이 `unknown measured_removed=0 measured_added=0` 을
      출력하고 stderr 가 비어 있다. zsh·bash 양쪽 [exact]
      (측정: `harness/evals/amend-direction/empty.txt` 2 회 전달, stdout·stderr 2 벌)
- [ ] ER-02: 입력 경로 중 하나라도 존재하지 않으면 `amend_direction_oracle` 이 `unknown missing_input=<경로>` 를
      출력하고 stderr 에 `No such file` 이 0 건이며 return 0 이다 — 베이스라인의 조용한 실패(sort 에러 4 줄 뒤 unknown)를
      명시 실패로 바꾼다. zsh·bash 양쪽 [exact]
      (측정: `/nonexistent/a` 전달, stdout·stderr·rc 2 벌)

## Architecture

- [ ] AR-01: 이번 스프린트의 커밋 변경 경로가 아래 허용목록 접두 안에만 있다 [exact, enumerated]
      Given: 구현 커밋 완료 후
      허용: `harness/references/contract-schema.md` · `harness/agents/qa-evaluator.md` ·
      `harness/skills/sprint-contract/SKILL.md` · `harness/evals/amend-direction/` · `harness/README.md` ·
      `.harness/sprint-contract-harness-amend-direction-baseline-case.md` ·
      `.harness/sprint-feedback-harness-amend-direction-baseline-case.md` ·
      `.harness/sprint-amendments-harness-amend-direction-baseline-case.md`
      (측정: `git diff --name-only 4fb1382..HEAD` 각 줄이 위 8 접두 중 하나에 매치, 매치 안 되는 줄 0 건.
      제외 pathspec 없음. 계약 시점 베이스라인: 0 경로)
- [ ] AR-02: 스키마 헤더(1~20 행)의 갱신 이력에 `2026-09-08` 항목이 추가되고, 이 diff 가 `v5.4`·`v5.5` 문자열을
      **새로 추가하지 않는다** (다른 세션 브랜치와의 버전 번호 충돌 회피). HTML 미러 2 파일
      (`docs/harness/contract-schema.html` · `docs/harness/qa-evaluation-guide.html`)은 갱신하지 않는다 —
      명시적 미완이며 완료 보고에 적는다 [exact, enumerated]
      (측정: `sed -n '1,20p' harness/references/contract-schema.md | grep -c '2026-09-08'` ≥1 ·
      `git diff 4fb1382..HEAD -- harness/references/contract-schema.md | grep -cE '^\+.*v5\.[45]'` = 0 ·
      `git diff --name-only 4fb1382..HEAD -- docs/` 빈 출력)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수
      (측정: `python3 scripts/validate-plugin.py harness --check=code-fence` 가 V6 OK)
- [ ] AP-04: `SKILL.md` / `agents/*.md` frontmatter 에서 `name` 필드 누락 없음
      (측정: `python3 scripts/validate-plugin.py harness --check=frontmatter` 가 V1 OK)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (제외 목록 없음)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개 — N/A (harness 는 실행 가능한 앱/서버가 아니라 스킬·에이전트·references
      문서다. 헬퍼 실행(SC-01·SC-02·ER-01·ER-02)이 런타임 검증을 대신한다)
