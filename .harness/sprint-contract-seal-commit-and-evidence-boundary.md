---
feature: "봉인 시점 원문을 커밋으로 남기고 근거 경계를 한 기준으로 정리"
slug: seal-commit-and-evidence-boundary
created: "2026-09-24 09:15"
complexity: "복잡"
conditions: 19
status: active
owner_session: f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0
conditions_digest: sha256:2493939cfb28dc22
locked_at: "2026-09-24 09:58"
---

## 배경

앞 스프린트의 개정 파일이 다음 거리 4 건을 남겼고, 그중 **셋이 한 뿌리**다 —
**봉인 시점의 계약 원문이 git 에 남지 않는다.**

실측(2026-09-24, 이번 세션 계약 3 건):

| 계약 | 봉인 | 첫 커밋 | 그 커밋에 담긴 파일 수 |
| --- | --- | --- | --- |
| `validate-check-count-sync` | 14:46 | 14:48 `ab396f2` | 20 |
| `cross-diagnosis-to-parent` | 15:43 | 15:49 `cb39d89` | 10 |
| `contract-verifiability-gaps` | 09:44 | 09:47 `ac77cdc` | 5 |

셋 다 봉인 뒤 2~6 분 지나 **구현 파일과 함께** 커밋됐다. 즉 git 이 가진 가장 오래된 판이 이미
구현이 끝난 뒤 상태라, 봉인과 첫 커밋 사이에 무엇이 바뀌었는지 증명할 수 없다. 여기서 세 구멍이
나온다.

1. **"조건 줄이 가리키는 산문을 고치면 개정 파일에 남긴다" 를 기계로 판정할 수 없다.** 봉인은
   조건 줄만 덮으므로 산문을 고쳐도 `SEAL_OK` 다. 대조할 원문이 git 에 없으면 규칙은 지키자는
   말로만 남는다 — 형제 규칙인 봉인이 결정론 검사인 것과 등급이 어긋난다
2. **조용히 다시 봉인하면 `SEAL_BROKEN` 이 0 이 된다.** 조건을 고친 뒤 새 값으로 봉인하면 위반이
   사라진다. 지침은 "조용히 다시 봉인하지 마라" 로 말로만 막는다
3. 첫 커밋 이전 구간이 아예 빈다. 앞 스프린트에서 계약 68 개 중 12 개는 git 에 추적조차 되지
   않았다

**해결**: 봉인 직후 계약 파일만 **단독으로 커밋**한다. 그러면 git 이 봉인 시점 원문을 갖고,
이후 산문 변조와 재봉인이 모두 `git diff` 로 드러난다. 세 구멍이 한 절차로 닫힌다.

네 번째 거리는 성격이 다르다 — **근거 경계가 흔들린다.** 앞 스프린트가 넣은 표는 행 이름이
*누가 썼나*를 묻고 이유 칸이 *고칠 수 있나*를 물어, 둘이 갈리는 사례가 실재한다. 커밋 메시지는
"git 기록" 이라 가능 쪽인데 구현자가 쓴 글이고, 실제로 이번 세션의 커밋 메시지 하나가 사실과
달랐다. 기준을 **하나로** 정리한다.

## 리서치 소스

- `.harness/sprint-amendments-contract-verifiability-gaps.md` — 다음 거리 4 건의 근거
- `harness/references/contract-schema.md` §계약 봉인 · §Amendment 사이드카 (근거 경계 표)
- `harness/docs/guides/qa-evaluation-guide.md` — 같은 표의 사본
- `harness/skills/sprint-contract/SKILL.md` Step 6.6 — 봉인 절차의 끝
- `harness/agents/qa-evaluator.md` Step 1-e-2 — 평가자의 봉인 검증 지점
- 이번 세션 계약 3 건의 봉인 시각 대 첫 커밋 시각 실측 (위 표)

## 범위 경계

### 설계 결정

**봉인 커밋은 계약 파일만 담는다.** 구현 파일이 섞이면 "봉인 시점 원문" 이라는 성질이 사라진다.
`git commit -o <계약경로>` 로 그 경로만 커밋하고, 다른 세션이 올려둔 것을 삼키지 않는다.
**봉인 직후 가장 먼저 할 git 동작이 이것이다** — 구현을 시작하기 전에 한다.

**전용 가지에서 한다.** `main` 은 보호돼 있어(검사 3 종 필수) 직접 밀어 넣을 수 없다. 봉인
커밋을 만들기 전에 `feat/<slug>` 로 옮긴다. 이 계약도 `feat/seal-commit-and-evidence-boundary`
에서 한다 — 교차 진단이 이 누락을 짚었다.

**병합할 때 스쿼시를 쓰지 마라.** 이 레포는 세 방식(병합 커밋 · 스쿼시 · 재배치)을 모두
허용하는데, **스쿼시로 병합하면 여러 커밋이 하나로 합쳐져 봉인 커밋이 `main` 기록에서
사라진다.** 그러면 이 스프린트가 만들려는 성질("봉인 시점 원문이 git 에 남아 대조 가능하다")이
통째로 무너진다 — 자기 가지에서는 QA 가 통과하는데 `main` 에서는 대조할 것이 없어진다.
`gh pr merge --merge` (병합 커밋)만 쓴다. 이번 세션이 앞서 머지한 `36a73eb` · `b9465cc` 는
부모가 2 개인 병합 커밋이라 안전했다 (실측 확인). 교차 진단이 이 위험을 짚었다.

**평가자는 그 커밋을 찾아 대조한다.** `git log --diff-filter=A` 로 계약이 처음 들어온 커밋을
찾고, 그 판본과 현재를 비교한다. 조건 줄 차이는 `SEAL_BROKEN` 이 이미 잡으므로 평가자가 새로
보는 것은 **산문 차이**와 **`conditions_digest` 자체가 바뀐 흔적**이다.

**봉인 커밋이 없는 계약은 실패가 아니다.** 지금 계약 68 여 개가 그 절차 없이 만들어졌고
12 개는 추적조차 되지 않는다. `SEAL_ABSENT` 와 같은 급으로 다룬다 — 경고이지 판정 근거가 아니다.
소급으로 만들어 넣지 마라. 없던 원문을 있는 것처럼 만드는 행위다.

**근거 경계는 "구현자가 사후에 고칠 수 있는가" 하나로 판정한다.** 기록의 **구조적 값**(시각 ·
식별자 · 해시 · 도구가 찍은 출력)은 고칠 수 없으니 근거가 되고, 그 안에 **사람이 쓴 서술**
(커밋 메시지 본문 · 개정 문서의 설명 · 계약의 실측 문장)은 고칠 수 있으니 근거가 못 된다.
행 이름을 *누가 썼나*로 두면 세션 기록 안의 자기 발언 같은 사례에서 갈린다.

**고치는 파일 4개**

```text
harness/skills/sprint-contract/SKILL.md
harness/references/contract-schema.md
harness/docs/guides/qa-evaluation-guide.md
harness/agents/qa-evaluator.md
```

**범위 밖** — 남은 거리 1 건(마크다운 경고 수가 문서 구조 붕괴에 둔감함)은 표 무결성 검사를
새로 만들어야 하고, 그것을 `validate-plugin.py` 에 V10 으로 넣으면 **검사 개수가 박힌 지시문
19 개 파일이 또 어긋난다.** 먼저 지시문에서 개수 표기를 없애는 작업이 선행이라 별 스프린트로
남긴다. **AR-03 이 이번에 만들고 양성 대조까지 확인한 고립 표 행 검사 스크립트를 그 스프린트의
출발점으로 남긴다** — 계약 본문에만 두고 버리면 다음 스프린트가 처음부터 다시 만든다
(교차 진단 지적). 옛 기록(`.harness/` · `docs/kaizen/` · `harness/evals/`)과 플러그인 배포도
범위 밖이다.

### 봉인 전 실측한 기준값

다섯 낱말·구절 전부 **현재 0 건**이다 (양성 대조가 성립한다 — 고친 뒤 1 이상이어야 한다).

| 재는 것 | 파일 | 지금 |
| --- | --- | --- |
| `Step 6.7` | `sprint-contract/SKILL.md` | 0 |
| `봉인 커밋` | `contract-schema.md` | 0 |
| `사람이 쓴 서술` | `contract-schema.md` | 0 |
| `사람이 쓴 서술` | `qa-evaluation-guide.md` | 0 |
| `봉인 커밋` | `qa-evaluator.md` | 0 |

- `python3 scripts/validate-plugin.py` — **14 plugins, 14 OK · Exit: 0**
- 편집기와 같은 조건의 마크다운 경고 — 대상 4 개 합 **56 건 · (파일,규칙) 조합 9 개**
  (markdownlint-cli2 0.23.2 · `MD013` 끔). 대상은 위 4 개 파일 전부다
- 기준 커밋 — `b9465cc`
- 이 계약 자신의 봉인 커밋 — 새 절차를 스스로 따른다 (AR-04 가 잰다)

### 측정 환경 주의

이 맥의 `grep` 은 ugrep 7.8.4 로 `-r` 출력에 `./` 접두를 붙이지 않는다. 셸 변수를 따옴표 없이
펼치면 zsh 가 쪼개지 않아 파일을 못 찾고 `2>/dev/null` 이 그 오류를 삼켜 조용히 0 이 된다.
여러 파일을 돌릴 때는 목록을 파일에 담아 `while read` 로 돌린다.

문서에 절을 끼워 넣을 때는 **표·목록 중간에 들어가지 않는지** 삽입 전후로 뼈대를 찍어 비교한다.
앞 스프린트에서 표를 끊었고 마크다운 경고 수는 그것을 잡지 못했다 (같은 파일 세 커밋 다 14 건).

### 상한 ref 해석

```bash
sprint_head() {  # 이 레포 관례(feat/<slug> · PR 머지)
  m=$(git log --merges --format=%H --grep="from joo6077/feat/${1}" -1)
  [ -n "$m" ] && { echo "$m"; return 0; }
  git rev-parse --verify -q "feat/${1}" && return 0
  echo "UNRESOLVED feat/${1}" >&2; return 1
}
SH=$(sprint_head seal-commit-and-evidence-boundary) || exit 1
[ "$SH" = "$(git rev-parse b9465cc)" ] && { echo "STALE_HEAD"; exit 1; }
```

### 커버리지 해소

커버리지 해소: AR-01 — 산문의 4 개 경로를 측정 절이 같은 표기로 열거한다.
커버리지 해소: SK-02 · ER-01 — 같은 내용이 들어가는 두 파일을 측정 절이 각각 이름으로 든다.
커버리지 해소: DG-02 — 대상 4 개를 측정 절이 경로로 열거한다 (앞 스프린트 A-03 의 교훈).

## Skill

- [ ] SK-01: `harness/skills/sprint-contract/SKILL.md` 에 봉인 직후 계약만 단독 커밋하는
      단계가 `Step 6.7` 로 들어갔다 [exact]
      (그 절이 담아야 할 것 셋: (a) 전용 가지(`feat/<slug>`)로 옮긴다 (b) `git commit -o` 로
      계약 경로만 커밋한다 (c) 병합할 때 스쿼시를 쓰지 마라 — 봉인 커밋이 합쳐져 사라진다 ·
      측정: `grep -Fc 'Step 6.7' harness/skills/sprint-contract/SKILL.md` 가 1 이상이고,
      `awk '/^### 6.7/,/^### 7/'` 로 절을 잘라 (a) `grep -c 'feat/'` ≥ 1
      (b) `grep -c 'commit -o'` ≥ 1 (c) `grep -c '스쿼시'` ≥ 1)

      양성 대조: 고치기 전 `Step 6.7` 은 **0 건**이다 (작성 시점 실측).

- [ ] SK-02: 봉인 커밋 절차가 **두 파일**에 정의됐다 [exact, enumerated]
      (대상 2 곳: `harness/references/contract-schema.md`(정의) ·
      `harness/agents/qa-evaluator.md`(평가자가 그것을 찾아 대조하는 절차) ·
      측정: 두 파일 각각에 `grep -Fc '봉인 커밋'` 이 1 이상)

      양성 대조: 고치기 전 두 파일 모두 **0 건**이다 (작성 시점 실측).

- [ ] SK-03: 봉인 커밋이 없는 옛 계약을 **실패로 보지 않는다**는 문구가
      `contract-schema.md` 에 있다 [exact]
      (지금 계약 68 여 개가 그 절차 없이 만들어졌고 12 개는 추적조차 되지 않는다.
      `SEAL_ABSENT` 와 같은 급으로 다뤄야 한다 ·
      측정: `grep -Fc '소급으로 만들어 넣지 마라' harness/references/contract-schema.md`
      가 1 이상)

      양성 대조: 고치기 전 **0 건**이다 (작성 시점 실측).

## Script

- [ ] SC-01: 평가자가 봉인 커밋을 찾는 명령이 `qa-evaluator.md` 에 실려 있고 **그대로 돌아간다**
      [exact]
      (Given: AR-04 의 단독 커밋이 이미 만들어진 뒤 — 그 전에는 (b) 가 0 을 낸다.
      두 조건은 **같은 커밋 하나**로 동시에 만족된다 (교차 진단이 이 순서 얽힘을 짚었다) ·
      측정: 그 파일에서 `git log --diff-filter=A` 를 담은 코드 블록을 찾아
      (a) `grep -c 'diff-filter=A'` 가 1 이상
      (b) 그 명령을 이 계약 파일 경로로 떠서 실행해 커밋 해시 1 개가 나온다)

      양성 대조: 이 계약은 새 절차를 따라 봉인 직후 단독 커밋되므로 그 명령이 해시를 낸다.
      앞 스프린트 계약 3 건에 같은 명령을 걸면 구현 파일이 섞인 커밋이 나온다 — 절차 전과 후가
      구별된다.

- [ ] SC-02: `python3 scripts/validate-plugin.py` 전체가 `14 plugins, 14 OK` · `Exit: 0` 이다
      [goal]
      (측정: 그 명령의 마지막 두 줄. 기준값과 같아야 한다)

      음성 대조: 대상 파일 중 `harness/agents/qa-evaluator.md` 의 여는 fence 에서 언어 힌트를
      지우면 V6 이 FAIL 하고 `14 OK` 가 깨진다. 이 측정은 파일 내용을 직접 읽으므로 구현을
      지워도 통과하는 형태가 아니다.

## Error

- [ ] ER-01: 근거 경계 기준이 **"구현자가 사후에 고칠 수 있는가" 하나로** 정리됐고, 두 파일에
      같은 문구가 들어갔다 [exact, enumerated]
      (대상 2 곳: `harness/references/contract-schema.md` ·
      `harness/docs/guides/qa-evaluation-guide.md` ·
      측정: 두 파일 각각에 `grep -Fc '사람이 쓴 서술'` 이 1 이상)

      양성 대조: 고치기 전 두 파일 모두 **0 건**이다 (작성 시점 실측).

- [ ] ER-02: 커밋 메시지가 **어느 쪽인지** 그 표에 명시됐다 [exact]
      (교차 진단이 애매한 사례로 든 것이고, 실제로 이번 세션 커밋 메시지 하나가 사실과 달랐다.
      구조적 값(해시 · 시각 · diff)은 근거가 되고 **메시지 본문은 안 된다** ·
      측정: `grep -Fc '커밋 메시지 본문' harness/references/contract-schema.md` 가 1 이상)

      양성 대조: 고치기 전 **0 건**이다 (작성 시점 실측).

## Architecture

- [ ] AR-01: 이 스프린트의 변경 파일이 위 4 개 경로와 정확히 일치한다 [exact, enumerated]
      (Given: 이 스프린트의 커밋이 끝난 뒤 · **`STALE_HEAD` 확인을 먼저 통과** ·
      측정: `git diff --name-only b9465cc..$(sprint_head seal-commit-and-evidence-boundary) --
      . ':(exclude).harness/**'` 의 출력이 4 행이고 각 줄이 위 목록에 있다.
      `UNRESOLVED` 나 `STALE_HEAD` 면 `HEAD` 로 떨어지지 말고 사용자에게 묻는다)

- [ ] AR-02: 손대지 않기로 한 것이 변경되지 않았다 [exact]
      (Given: 위와 같음 ·
      측정: 같은 구간에서 (i) `harness/evals/` 0 행 (ii) `docs/kaizen/` 0 행
      (iii) `scripts/validate-plugin.py` 0 행 — 표 무결성 검사는 별 스프린트다
      (iv) `.harness/sprint-contract*.md` 에 `verify_seal` 을 돌려 `SEAL_BROKEN` 이 0 개.
      `SEAL_OK` 와 `SEAL_ABSENT` 는 둘 다 통과이며 `-maxdepth` 를 걸지 않는다)

      양성 대조: (iv) 는 작성 시점에 계약 전체에 돌려 `SEAL_BROKEN` 0 을 확인한다. 경로 패턴
      3 종은 `git ls-files` 에 걸면 1 이상이 나온다 — 추적 파일이 실재한다. 총수는 산출물
      추가로 시점마다 달라지므로 고정하지 않는다.

- [ ] AR-03: 문서 삽입이 표를 끊지 않았다 — 대상 4 개 파일에 **고립 표 행 0 개** [exact]
      (앞 스프린트에서 실제로 끊었고 마크다운 경고 수가 못 잡았다. 아래 스크립트를 그대로
      써서 잰다. **고립 판정**: 코드 블록 밖의 표행(`^|`) 중, 바로 위가 표행이 **아니고**
      바로 아래도 헤더 구분선(`^|` 이고 `|-: ` 만으로 이뤄진 줄)이 **아닌** 행)

      ```python
      # /tmp/isolated.py — 인자로 받은 파일마다 고립 표 행을 센다
      import io, sys
      def isolated_rows(path):
          lines = io.open(path, encoding='utf-8').read().split('\n')
          keep = []; infence = False
          for i, l in enumerate(lines, start=1):
              if l.startswith('```'): infence = not infence; continue
              if infence: continue
              keep.append((i, l))
          hits = []
          for k, (n, l) in enumerate(keep):
              if not l.startswith('|'): continue
              prev_is_table = k > 0 and keep[k-1][1].startswith('|')
              nxt = keep[k+1][1] if k+1 < len(keep) else ''
              next_is_sep = nxt.startswith('|') and set(nxt) <= set('|-: ')
              if not prev_is_table and not next_is_sep: hits.append((n, l[:62]))
          return hits
      for p in sys.argv[1:]:
          h = isolated_rows(p)
          print("%-52s 고립 %d 개" % (p, len(h)))
          for n, l in h: print("    %d: %s" % (n, l))
      ```

      양성 대조: 앞 스프린트 커밋 `ac77cdc` 시점의 `contract-schema.md` 를 떠서 같은 검사를
      걸면 **고립 1 개(1036 줄 `| \`unknown\` |` 행)** 가 나온다 — 그때 실제로 끊겼던 자리다.
      작성 시점에 실행해 확인했고 지금 4 개 파일은 전부 0 이다. 대조가 0 이면 검사가 죽은 것이다.

      ```bash
      git show ac77cdc:harness/references/contract-schema.md > /tmp/old-schema.md
      python3 /tmp/isolated.py /tmp/old-schema.md   # 고립 1 개 여야 한다
      ```

- [ ] AR-04: **이 계약 자신이 새 절차를 따랐다** [exact]
      (Given: 전용 가지 `feat/seal-commit-and-evidence-boundary` 로 옮긴 뒤, 구현을 시작하기
      **전에** 계약만 단독 커밋 — `main` 은 보호돼 직접 밀어 넣을 수 없다 ·
      측정: `git log --diff-filter=A --format='%h' --
      .harness/sprint-contract-seal-commit-and-evidence-boundary.md` 로 첫 커밋을 찾고,
      `git show --name-only --format='' <해시>` 의 파일 수가 **1** 이며 그것이 이 계약 경로다 ·
      **병합은 `gh pr merge --merge` 로 한다** — 스쿼시로 합치면 이 커밋이 `main` 기록에서
      사라져 조건이 통과해도 성질이 남지 않는다 (교차 진단 지적))

      양성 대조: 앞 스프린트 계약 3 건에 같은 측정을 걸면 파일 수가 20 · 10 · 5 다
      (작성 시점 실측). 1 이 아니면 절차를 안 따른 것이므로 이 측정은 구별력이 있다.

## Anti-patterns

- [ ] AP-03: bare code fence 0 건 — 여는 fence 에 언어 힌트가 있다
      (유효 대상은 4 개 중 V6 이 보는 3 개다 — `harness/skills/sprint-contract/SKILL.md` ·
      `harness/references/contract-schema.md` · `harness/agents/qa-evaluator.md`.
      `harness/docs/` 1 개는 V6 범위 밖이다 (`scripts/validate-plugin.py:516-519`) ·
      측정: `python3 scripts/validate-plugin.py --check=code-fence` 가 전 킷 OK)

      양성 대조: 세 파일의 `^```” 개수를 봉인 전에 실측해 1 이상임을 확인한다.

- [ ] AP-04: frontmatter 가 보존됐다 — V1 FAIL 0 건
      (유효 대상은 V1 이 보는 2 개다 — `harness/skills/sprint-contract/SKILL.md` 와
      `harness/agents/qa-evaluator.md`. V1 은 `skills/*/SKILL.md` 와 `agents/*.md` 만 본다 ·
      측정: `python3 scripts/validate-plugin.py --check=frontmatter` 가 전 킷 OK)

      양성 대조: 그중 하나의 `name:` 을 지우고 같은 명령을 돌리면 `13 OK, 1 ERROR · Exit 2` 가
      난다 (앞 스프린트에서 실측된 방식). 지운 뒤 되돌린다.

## Reusability

- [ ] RE-01: N/A (산출물이 지침 문서 문구뿐이라 재사용 단위 코드가 0 개다.
      측정: 변경 4 개 파일이 전부 `.md` 이고 실행 코드 0 개)
- [ ] RE-02: N/A (같은 사유 — 재사용할 컴포넌트·함수·모듈이 산출물에 없다)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 로 그 한 파일만 잰다 —
      이번 변경 파일과 교집합 0 개. 측정: AR-01 의 4 행에
      `grep -c '^scripts/release.sh$'` 이 0)
- [ ] DG-02: 편집기와 같은 조건으로 잰 마크다운 경고가 기준값을 넘지 않는다
      (기준 56 건 · (파일,규칙) 조합 9 개 · **대상은 아래 4 개 전부**를 열거한다 —
      `harness/skills/sprint-contract/SKILL.md` · `harness/references/contract-schema.md` ·
      `harness/docs/guides/qa-evaluation-guide.md` · `harness/agents/qa-evaluator.md` ·
      측정: scratchpad 에 `npm install --no-save markdownlint-cli2@0.23.2` 후 설정
      `{"config":{"MD013":false}}` 를 `--config` 로 넘겨 4 개를 돌린다. 총 건수 ≤ 56 이고,
      출력을 `파일 규칙ID` 로 정규화해 `sort | uniq -c` 한 집계에서 기준보다 건수가 늘어난
      조합이 0 개. 줄 번호는 밀리므로 집계로 비교한다.
      **이 조건은 AR-03 을 대신하지 못한다** — 앞 스프린트에서 표가 끊긴 동안에도 이 수치는
      세 커밋 내리 같았다)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 로 그 한 파일만
      돌린다 — 이번 변경 파일과 교집합 0 개. 측정: DG-01 과 같음)
- [ ] DG-04: N/A (산출물에 구동할 앱·서버가 없다. 측정: 변경 4 개 파일에 실행 진입점 0 개).
      이 자리에 실제로 성립하는 검사는 SC-02 다
