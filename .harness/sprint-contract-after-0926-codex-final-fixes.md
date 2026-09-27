---
feature: "Codex 최종 점검 지적 고침 (onboarding G5 CRLF · design-mockup Step 번호)"
slug: after-0926-codex-final-fixes
created: "2026-09-27 18:26"
complexity: "복잡"
conditions: 20
status: active
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:26c72dfbcc4e6f88
measurement_digest: sha256:ffe639f290b0e037
locked_at: "2026-09-27 18:30"
---

## 배경

- 출처: Codex 최종 점검 `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/after-kaizen-0926b/codex-review-2.md` 의 결함 둘.
- (1) 막아야 함 — `onboarding-kit/skills/setup-guide/SKILL.md` 124 줄의 G5 검사(막는 요구 세 칸) awk 가 줄 끝 `\r` 을 지우지 않는다. CRLF 가이드에서는 표 머리 마지막 칸이 `우회\r` 가 되어 표를 못 알아보고, 빈 칸이 있어도 `G5_BLOCKING PASS rows=0` 으로 통과시킨다.
- (2) 고치면 좋음 — `design-kit/references/visual-change-protocol.md` 223 줄이 승인 기록 폐기 칸 규칙을 「`design-mockup` Step 6」 으로 가리킨다. 지금 Step 6 은 Figma 전송이고 승인 기록은 `design-kit/skills/design-mockup/SKILL.md` 152 줄 `## Step 5: 승인 기록 생성 (확정 시 필수)` 이다.
- 작업 폴더 W=`/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/ak2-cx2` (가지 `chore/ak2-cx2`, 출발 커밋 `ff28c75398e0909b77232d7173523542c36aa576`). 아래 측정은 전부 W 에서 돈다.
- 공통 전제 (모든 조건에 적용): 이 맥 zsh · BSD sed · ugrep · BSD awk. 임시 파일은 `S=/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/cx2` 아래에만 만든다. 구간 상한은 `U=$(git -C "$W" rev-parse --verify refs/heads/chore/ak2-cx2) || exit 2` 로 구한다 (`HEAD` 금지). 커밋 구간을 재는 조건은 구현 커밋이 모두 끝난 뒤에 잰다.

## GAP 분석

Pre-Edit 감사 (실제로 연 자리):

| 대상 파일 | 연 자리 | 발견 | 조건 |
| --- | --- | --- | --- |
| `onboarding-kit/skills/setup-guide/SKILL.md` | 54~148 줄 `guide_gate` | G5 awk(124~139)만 줄 끝을 `$`·완전 일치로 본다. G1(64 줄 awk) · G3 · G4(108 줄 awk)는 줄 앞 일치라 CRLF 에 영향 없음 — 픽스처 9 개 LF/CRLF 대조에서 G1~G4 출력이 전부 같았다 | SK-01 · SK-02 · ER-01 |
| `onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` | 전체 | `gate_cases` 에 없는 픽스처를 고아로 실패 처리한다. 러너 자체는 고칠 것 없음 | SK-03 |
| `onboarding-kit/skills/setup-guide/evals/evals.json` | `gate_cases` 11 건 | 전부 LF 입력. CRLF 입력 0 건 | SK-03 · SK-05 |
| `docs/onboarding-kit/setup-guide.html` | 319~338 줄 | `guide_gate` 함수 사본이 실려 있다 (빈 줄 빼고 SKILL.md 와 89 줄 일치, 차이 0) | SK-04 |
| `design-kit/references/visual-change-protocol.md` | 223 줄 | ``(`design-mockup` Step 6)`` — 틀린 번호 | AR-01 |
| `docs/design-kit/visual-change-protocol.html` | 687 줄 | `(<code>design-mockup</code> Step 6)` — 같은 문장 사본 | AR-01 |
| `design-kit/skills/design-mockup/SKILL.md` | 152 · 183 줄 | Step 5 = 승인 기록, Step 6 = Figma 전송. 폐기 칸 `PRD 없음` 규칙은 Step 5 본문(171 줄 근처)에 있다 | AR-01 |

복잡도 4 축: 레이어 1 (문서·검사 스크립트) · 공개 계약 변경 예 (G5 판정 결과가 CRLF 입력에서 바뀐다) · 소비면 예 (docs 페이지 사본 · 평가 러너) · 회귀 위험 예 (LF 입력 판정) → 공개 계약 변경과 소비면이 둘 다 예라 복잡.

## 범위 경계

- 고치는 G 검사는 onboarding-kit 의 `guide_gate` 안에서만 찾는다. 다른 킷(howto-kit 의 G1~G6 등)은 이번 범위 밖이다.
- `docs/superpowers/plans/2026-04-06-design-kit-new-skills.md` 764 줄 「design-mockup Process Step 2」 는 2026-04 계획 기록이라 고치지 않는다. `.claude/kaizen-input/insights-report.md` 92 줄 「design-mockup Step 1」 은 지금 번호(화면 요구사항 파악)와 맞아 고치지 않는다.
- 버전 올리기 · 릴리스 · 푸시는 하지 않는다.
- 커버리지 해소: AR-01 — 측정 절의 세 명령이 산문의 세 파일을 하나씩 잰다. 검출기가 백틱 안 백틱 때문에 측정 절 경로를 못 읽었다.
- 커버리지 해소: AR-02 — 측정이 `grep -rlE` 한 번으로 레포 전체를 덮고, 확장 결과 4 개 파일을 조건 안에 열거했다.
- 커버리지 해소: AR-03 — 측정 `git diff --name-only` 가 pathspec `.` 으로 레포 전체를 덮는다. 6 경로는 기대 집합이다.
- 커버리지 해소: DG-02 — 측정 명령의 `<파일>` 자리에 산문이 열거한 세 파일을 하나씩 넣는다.
- 교차 진단 지적 반영 (AR-04 서명 줄): 이 계약의 구현자는 작업 지시 공통 전제가 정한 서명 줄 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>` 을 쓰는 세션이다. 교차 진단을 돌린 평가자 세션의 서명 줄(다른 모델 이름)은 구현 커밋과 무관하다. AR-04 는 구현 커밋의 마지막 줄만 잰다.

## 회귀 게이트

측정 도구 두 개. 평가자는 아래를 `$S` 아래 파일로 저장해 쓴다 (봉인 전 이 맥에서 실행해 본 판이다).

(A) `$S/crlf-parity.sh` — LF 픽스처마다 CRLF 변환본을 만들어 두 셸에서 출력이 같은지 센다.

```bash
#!/bin/bash
# 사용: bash crlf-parity.sh <레포> <SKILL.md 경로> <임시 폴더>
R=${1}; SK=${2}; T=${3}
F=$R/onboarding-kit/skills/setup-guide/evals/fixtures
mkdir -p "$T" || exit 2
awk '/^guide_gate\(\) \{/{p=1} p{print} p&&/^\}$/{exit}' "$SK" > "$T/gate.sh"
tail -1 "$T/gate.sh" | grep -qx '}' || { echo EXTRACT_FAIL; exit 2; }
same=0; diff=0
for f in $(find "$F" -maxdepth 1 -type f -name '*.md' | sort); do
  n=$(basename "$f")
  if LC_ALL=C grep -q $'\r$' "$f"; then continue; fi
  sed 's/$/\r/' "$f" > "$T/crlf-$n"
  for sh in bash zsh; do
    a=$($sh -c ". '$T/gate.sh'; guide_gate '$f' flutter")
    b=$($sh -c ". '$T/gate.sh'; guide_gate '$T/crlf-$n' flutter")
    if [ "$a" = "$b" ]; then same=$((same+1)); else diff=$((diff+1)); echo "DIFF $sh $n"; fi
  done
done
echo "PARITY same=$same diff=$diff"
```

- 알려진 답: LF 픽스처 9 개 × 셸 2 개 = 18 쌍. 고치기 전(ff28c75) 실제값 `PARITY same=12 diff=6` (DIFF: gate-blocking-ok · gate-fail-blocking-empty · gate-fail-blocking-nourl, 셸마다). 줄 끝 `\r` 을 지운 시험판 실제값 `PARITY same=18 diff=0`. 둘 다 종료 코드 0.

(B) `$S/fn-diff.py` — SKILL.md 의 `guide_gate` 와 docs 페이지 사본을 빈 줄을 빼고 줄 단위로 대조한다.

```python
# 사용: python3 fn-diff.py <레포> [SKILL 대신 비교할 파일]
import difflib, html, re, sys
root = sys.argv[1]
src = sys.argv[2] if len(sys.argv) > 2 else root + "/onboarding-kit/skills/setup-guide/SKILL.md"
def fn(text):
    out, on = [], False
    for l in text.split("\n"):
        if l.startswith("guide_gate() {"): on = True
        if on and l.strip(): out.append(l)
        if on and l == "}": break
    return out
s = fn(open(src, encoding="utf-8").read())
h = open(root + "/docs/onboarding-kit/setup-guide.html", encoding="utf-8").read()
d = fn(html.unescape(re.sub(r"<[^>]+>", "", h)))
diff = [x for x in difflib.unified_diff(s, d, lineterm="", n=0) if x[:1] in "+-" and not x.startswith(("+++", "---"))]
print("skill_lines=%d html_lines=%d diff_lines=%d" % (len(s), len(d), len(diff)))
for x in diff[:10]: print(x)
```

- 봉인 전 실제값: 지금 레포 `skill_lines=89 html_lines=89 diff_lines=0`. SKILL.md 에만 `\r` 지우는 줄을 넣은 시험판과 대조하면 `diff_lines=1` (양성 대조).

봉인 전 음성 대조 기록 (고치기 전 판 ff28c75, CRLF 로 바꾼 `gate-fail-blocking-empty.md`):

```text
bash · zsh 동일:
G1_LEDGER PASS steps=1 ledger=1
G2_MARKER PASS bare=0 invalid=0 env=0
G3_STACKMIX PASS stack=flutter swift_fence=0
G4_DEPRECATION PASS unsourced_boxes=0
G5_BLOCKING PASS rows=0
GATE_PASS
```

같은 LF 원본은 `G5_BLOCKING FAIL rows=2 empty=1 nourl=0` · `GATE_FAIL`. 고치기 전 SKILL.md 에 CRLF 픽스처와 `gate_cases` 1 건을 더한 사본에서 러너는 `EVALS declared=12 ran=12 fail=1` · `EVALS_FAIL` 이었다.

봉인 전 기존 검사 기준값: `ci-local.sh` 25 단계 rc=0 (feedback-agg-test 는 yq 가 없어 SKIP), 그 스크립트 밖 CI 단계 `check-api-kit-docs.py` · `detect-docs-drift.py --check-table` · `check-cause-table-copies.py` · `measure-helpers-test.sh` 4 개 rc=0. `run-gate-evals.sh` 는 `EVALS declared=11 ran=11 fail=0`.

## Skill

- [ ] SK-01: Given 구현 커밋 뒤 W 의 SKILL.md, When 회귀 게이트 (A) 의 추출 방식으로 뽑은 `guide_gate` 를 `sed 's/$/\r/'` 로 CRLF 로 바꾼 `onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-blocking-empty.md` 에 `flutter` 로 bash · zsh 각각 돌리면, Then 두 셸 모두 다섯째 줄이 `G5_BLOCKING FAIL rows=2 empty=1 nourl=0` 이고 여섯째 줄이 `GATE_FAIL` 이다 [exact]. 측정: `sed 's/$/\r/' <픽스처> > $S/crlf-empty.md` 로 사본을 만든 뒤 `bash -c ". $S/p/gate.sh; guide_gate $S/crlf-empty.md flutter"` 와 같은 명령을 zsh 로도 (`$S/p/gate.sh` 는 SK-02 의 (A) 가 뽑아 둔 함수). 음성 대조: 고치기 전 판(ff28c75) 은 두 셸 모두 `G5_BLOCKING PASS rows=0` · `GATE_PASS` 였다 — G5 awk 의 `\r` 지우기를 빼면 이 측정이 FAIL 한다.
- [ ] SK-02: Given 구현 커밋 뒤, When `bash $S/crlf-parity.sh "$W" "$W/onboarding-kit/skills/setup-guide/SKILL.md" $S/p` 를 돌리면, Then 마지막 줄이 정확히 `PARITY same=18 diff=0` 이고 종료 코드 0 이다 — 즉 LF 픽스처 9 개 전부에서 LF 와 CRLF 의 G1~G5 출력 여섯 줄이 두 셸 모두 같다 [exact]. 음성 대조: 고치기 전 판은 `PARITY same=12 diff=6` (gate-blocking-ok 가 CRLF 에서 `rows=0` 으로 줄어든 것 포함) 이다. 알려진 답: 9 × 2 = 18.
- [ ] SK-03: Given 구현 커밋 뒤, When `TMPDIR=$S/tmp sh onboarding-kit/skills/setup-guide/evals/run-gate-evals.sh` 를 돌리면, Then 끝 두 줄이 `EVALS declared=12 ran=12 fail=0` 과 `EVALS_PASS` 이고 종료 코드 0 이다 (기존 11 건 + CRLF 음성 입력 1 건, 고아 픽스처 0 건) [exact]. 음성 대조: 고치기 전 SKILL.md 에 같은 픽스처 · 같은 `gate_cases` 항목만 더한 사본은 `EVALS declared=12 ran=12 fail=1` · `EVALS_FAIL` 이었다.
- [ ] SK-04: Given 구현 커밋 뒤, When `python3 $S/fn-diff.py "$W"` 를 돌리면, Then 첫 줄이 `diff_lines=0` 을 담는다 — docs 페이지 `docs/onboarding-kit/setup-guide.html` 의 `guide_gate` 사본이 고친 SKILL.md 함수와 빈 줄 빼고 같다 [exact]. 양성 대조: SKILL.md 만 고치고 페이지를 그대로 두면 `diff_lines=1` 이 나온다 (봉인 전 시험판으로 실측).
- [ ] SK-05: `onboarding-kit/skills/setup-guide/evals/evals.json` 의 `gate_cases` 에 `fixture` 가 `fixtures/gate-fail-blocking-empty-crlf.md` 인 항목이 정확히 1 개 있고, 그 `stack` 이 `flutter` 이며 `expect` 가 `G1_LEDGER PASS steps=1 ledger=1` · `G2_MARKER PASS bare=0 invalid=0 env=0` · `G3_STACKMIX PASS stack=flutter swift_fence=0` · `G4_DEPRECATION PASS unsourced_boxes=0` · `G5_BLOCKING FAIL rows=2 empty=1 nourl=0` · `GATE_FAIL` 여섯 줄이다. 그리고 커밋된 그 픽스처의 모든 줄이 CRLF 로 끝난다 [exact]. 측정: `git -C "$W" show "$U:onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-blocking-empty-crlf.md" > $S/fx.md; wc -l < $S/fx.md; LC_ALL=C grep -c $'\r$' $S/fx.md` — 두 수가 같고 10 이상. 항목은 `python3 -c` 로 json 을 읽어 확인.

## Script

- [ ] SC-00: N/A (이번 변경 파일에 `scripts/release.sh` · `marketplace.json` 이 없다 — 버전 올리기는 범위 밖. 측정: 아래 AR-03 의 변경 목록에 `scripts/` · `.claude-plugin/` 경로 0 개)

## Error

- [ ] ER-01: Given 구현 커밋 뒤, When CRLF 로 바꾼 `fixtures/gate-fail-blocking-nourl.md` 에 SK-01 과 같은 방식으로 bash · zsh 각각 돌리면, Then 두 셸 모두 `G5_BLOCKING FAIL rows=1 empty=0 nourl=1` 과 `GATE_FAIL` 이 나온다 — 출처 칸에 주소가 없는 CRLF 표도 막힌다 [exact]. 음성 대조: 고치기 전 판은 두 셸 모두 `G5_BLOCKING PASS rows=0` · `GATE_PASS` 였다.

## Architecture

- [ ] AR-01: Given 구현 커밋 뒤, `design-kit/references/visual-change-protocol.md` 의 폐기 칸 `PRD 없음` 문장이 ``(`design-mockup` Step 5)`` 로 끝나고, `docs/design-kit/visual-change-protocol.html` 의 같은 문장이 `(<code>design-mockup</code> Step 5)` 로 끝나며, `design-kit/skills/design-mockup/SKILL.md` 의 `## Step 5: 승인 기록 생성 (확정 시 필수)` 줄은 그대로다 [exact, enumerated]. 측정: `grep -cF '(`design-mockup` Step 5)' design-kit/references/visual-change-protocol.md` 를 작은따옴표 그대로 돌린 값 → 1, `grep -cF '(<code>design-mockup</code> Step 5)' docs/design-kit/visual-change-protocol.html` → 1, `grep -cxF '## Step 5: 승인 기록 생성 (확정 시 필수)' design-kit/skills/design-mockup/SKILL.md` → 1. 양성 대조: 지금 레포에서 앞의 두 명령은 0 이고 같은 자리 `Step 6` 로 바꾼 명령은 각각 1 이다.
- [ ] AR-02: Given 구현 커밋 뒤, `grep -rlE 'design-mockup.*Step [1-9]' --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.harness .` (W 에서) 이 내는 파일 집합이 정확히 `.claude/kaizen-input/insights-report.md` · `docs/superpowers/plans/2026-04-06-design-kit-new-skills.md` · `design-kit/references/visual-change-protocol.md` · `docs/design-kit/visual-change-protocol.html` 4 개이고, 같은 조건의 `grep -rnE 'design-mockup.*Step 6'` 은 0 줄이다 [exact, enumerated]. 양성 대조: 봉인 전 `design-mockup.*Step 6` 은 2 줄(위 셋째 · 넷째 파일)이다.
- [ ] AR-03: Given 구현 커밋이 모두 끝난 뒤, `git -C "$W" diff --name-only ff28c75398e0909b77232d7173523542c36aa576.."$U" -- . ':(exclude).harness'` 의 결과가 정확히 다음 6 경로와 일치한다: `onboarding-kit/skills/setup-guide/SKILL.md` · `onboarding-kit/skills/setup-guide/evals/evals.json` · `onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-blocking-empty-crlf.md` · `docs/onboarding-kit/setup-guide.html` · `design-kit/references/visual-change-protocol.md` · `docs/design-kit/visual-change-protocol.html` [exact, enumerated]. 생성물 없음 (이 6 경로는 전부 손으로 쓰는 파일이다). 봉인 전 기준값: 같은 명령을 상한 `ff28c75` 로 돌리면 0 줄.
- [ ] AR-04: Given 구현 커밋이 모두 끝난 뒤, `git -C "$W" rev-list --no-merges ff28c75..$U` 의 커밋 가운데 `.harness/` 밖 파일을 담은 커밋마다 (a) 그 파일이 전부 `onboarding-kit/` · `docs/onboarding-kit/` 묶음이거나 전부 `design-kit/` · `docs/design-kit/` 묶음이고 (b) 메시지 마지막 줄이 `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>` 이며, 합친 커밋은 0 개다 [exact]. 측정: 커밋마다 `git show --name-only --format= <c>` 와 `git log -1 --format=%B <c> | sed '/^$/d' | tail -1`, 그리고 `git rev-list --merges ff28c75..$U | grep -c .` → 0.
- [ ] AR-05: Given 구현 커밋 뒤, `TMPDIR=$S/ci bash /Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-tools/ci-local.sh "$W"` 의 요약에서 `rc=0` 이 25 줄이고 `rc=0` 이 아닌 줄은 `feedback-agg-test SKIP (yq 없음)` 하나뿐이며, 그 스크립트 밖 CI 단계 `python3 scripts/check-api-kit-docs.py` · `python3 scripts/detect-docs-drift.py --check-table` · `python3 scripts/check-cause-table-copies.py` · `bash harness/evals/measure/measure-helpers-test.sh` 4 개가 W 에서 모두 종료 코드 0 이다 [exact, enumerated]. 봉인 전 기준값이 같다 (회귀 게이트 절).

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수. 측정: `python3 scripts/validate-plugin.py onboarding-kit --check=code-fence` 와 `python3 scripts/validate-plugin.py design-kit --check=code-fence` 가 둘 다 종료 코드 0
- [ ] AP-04: SKILL.md frontmatter 에서 name 필드 누락 금지. 측정: `python3 scripts/validate-plugin.py onboarding-kit --check=frontmatter` 종료 코드 0

## Reusability

- [ ] RE-01: N/A (산출물이 검사 함수 한 줄 수정 · 평가 입력 · 문서 문장뿐이라 새로 만드는 재사용 단위 코드가 없다. 측정: AR-03 의 6 경로가 md · json · html 뿐)
- [ ] RE-02: 새 측정·평가 장치를 만들지 않고 기존 `run-gate-evals.sh` 와 `gate_cases` 목록에 입력 1 건을 등록해 CRLF 음성 입력을 돌린다. 측정: AR-03 의 결과에 `run-gate-evals.sh` 가 없고 SK-03 의 `declared=12`

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: AR-03 명령 출력에 `scripts/release.sh` 0 줄)
- [ ] DG-02: Given 구현 커밋 뒤, 편집기 마크다운 검사와 같은 설정(markdownlint-cli2 0.23.2, MD013 끔)으로 잰 경고가 `onboarding-kit/skills/setup-guide/SKILL.md` · `design-kit/references/visual-change-protocol.md` 두 파일 합계 4 건 이하(봉인 전 4 건: MD024 둘 · MD041 · MD032)이고 `onboarding-kit/skills/setup-guide/evals/fixtures/gate-fail-blocking-empty-crlf.md` 는 0 건이다 [exact, enumerated]. 측정: `cd $S/mdl && npm install --no-save markdownlint-cli2@0.23.2` 뒤 `echo '{ "config": { "MD013": false } }' > $S/mdl/.markdownlint-cli2.jsonc; ./node_modules/.bin/markdownlint-cli2 --config .markdownlint-cli2.jsonc <파일> 2>&1 | grep -c ' error MD'`. 양성 대조: 언어 힌트 없는 코드 울타리 한 개짜리 임시 파일이 같은 명령에서 MD040 1 건을 낸다 (봉인 전 실측).
- [ ] DG-03: N/A (commands.test 는 `bash scripts/release.sh` 이고 이번 변경 파일과 교집합 0 개. 대신 SK-03 이 게이트 평가 러너를 돌린다)
- [ ] DG-04: N/A (변경 파일에 실행 진입점 0 개 — md · json · html. 게이트 함수의 실제 실행은 SK-01 · SK-02 · ER-01 이 두 셸로 잰다)
