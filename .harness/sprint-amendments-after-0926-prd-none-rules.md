---
slug: after-0926-prd-none-rules
created: "2026-09-26 21:35"
---

## A-01 — 코드 표시 기호 · 마침표로 끝낸 `PRD 없음` 기록을 재는 측정을 더한다

**앵커**: SK-04 (b) · SK-05 (b) · SK-06 의 검색 모양 `'PRD 없음[[:space:]]*[|]?[[:space:]]*$'` 와 SC-01 · SC-02 의 알려진 답 입력.

**무엇이 달라졌나**: QA(APPROVE) 뒤 독립 검토가 막는 결함을 찾았다. 쓰는 쪽 세 문서(design-mockup `:166` · sprint-contract `:635` ·
`/sprint` Step 0.5 문단)가 모두 줄 끝에 `` `PRD 없음` `` 을 붙이라고 코드 표시 기호째 보여 주는데, 봉인한 검색은 기호로 감싼 줄과 마침표로
끝낸 줄을 못 찾는다. 시험 입력에 그 모양이 없어 21 조건이 모두 통과했다. 구현은 `/sprint` Step 0.5 bash 블록과 plan-prd Step 0 넷째 항목에
둘째 검색 ``grep -rnE 'PRD 없음(`[.]?|[.])[[:space:]]*[|]?[[:space:]]*$'`` 를 더했다(`67cc307` harness · `5f8a092` planning-kit).
첫째 검색 줄은 글자 그대로 두었으므로 봉인 조건 SK-04 · SK-05 · SK-06 의 글자 비교는 그대로 성립한다. 두 모양은 겹치는 줄이 없다.

이 개정은 조건 줄을 고치지 않고 **측정 하나를 더한다**: 아래 블록을 계약 측정 도우미 뒤에 불러 `a01` 이 다음 값을 내야 한다.

- 기대: `cmds=2 sprint: bash=form6/rule0/err0 zsh=form6/rule0/err0 prd=form6/rule0/dup0/err0`
- 알려진 답: 시험 파일 `forms.md` 1 ~ 6 줄은 폐기 결정 여섯 모양(기호로 감싼 줄 · 기호로 감싼 표 행 · 마침표로 끝낸 줄 · 맨 표 행 · 맨 줄 · 기호 뒤 마침표)이라 6,
  7 ~ 9 줄은 규칙 설명 · QA 인용 · 안내 문장이라 0. plan-prd 는 두 명령을 따로 돌리므로 같은 줄이 두 번 나오면 안 된다(`dup0`)
- 음성 대조: `A01_DROP=1 a01`(둘째 검색 줄을 뺀 판) → `cmds=1 … form2 … prd=form2`. 고치기 전 끝점 `4a7d6f8` 에서 그냥 `a01` 을 돌려도 같은 값이었다
- 실측(2026-09-26, 끝점 `5f8a092`): 기대값 그대로. 음성 대조도 위 값 그대로

**amend_direction_oracle**: `narrowing measured_removed=0 measured_added=2` — 입력은 측정 집합(원 21 조건 ID · 개정은 그 21 개에
`A-01:forms 1-6` · `A-01:forms 7-9` 두 측정을 더한 것). 빠지는 측정이 없고 더해지기만 해서 통과하는 구현이 줄어든다. 스크립트는 스크래치
`pdfix/dir.sh`, bash · zsh 결과 같음.

**consent**: `unanchored` — 에이전트 판단으로 더했다. 좁히는 쪽이라 동의 없이도 판정 근거가 된다.

**한 모양으로 합치지 않은 이유**: 합치면 SK-04 · SK-05 · SK-06 이 재는 글자가 바뀐다. 옛 글자가 측정에서 빠지므로 위 계산으로 느슨해지는 쪽이 되어
사용자 동의가 필요하다. 겹치지 않는 둘째 줄을 더하는 쪽은 봉인 조건을 그대로 두고 막는 결함만 고친다.

```bash
# === A-01 측정 시작 ===
# 쓰는 법: 계약 측정 도우미를 source 한 뒤 이 블록을 source 하고 `a01`. A01_DROP=1 이면 둘째 검색 줄을 빼고 잰다(음성 대조)
a01() {
  lines_sh
  [ "${A01_DROP:-0}" = 1 ] && { grep -v 'PRD 없음(`' "$T/lines.sh" > "$T/l2.sh"; mv "$T/l2.sh" "$T/lines.sh"; }
  F=$T/forms; mkdir -p "$F/.harness"
  git -C "$F" init -q && git -C "$F" -c user.name=t -c user.email=t@t commit -q --allow-empty -m init
  printf '%s\n' '- 시간대 · 이유 · 범위 · 흔적 `PRD 없음`' '| 시간대 | 이유 | 범위 | 흔적 | `PRD 없음` |' \
    '- 시간대 · 이유 · 범위 · 흔적 — PRD 없음.' '| 시간대 | 이유 | 범위 | 흔적 | PRD 없음 |' '- 시간대 — PRD 없음' \
    '- 언어 · 이유 · 범위 · 흔적 · `PRD 없음`.' \
    '그 기능의 PRD 가 없으면 줄 끝에 `PRD 없음` 을 붙인다.' '- 근거: `PRD 없음` 1 줄 확인' \
    '다음 시안 전에는 줄 끝이 `PRD 없음` 인 줄을 읽는다.' > "$F/.harness/forms.md"
  r=""; for sh in bash zsh; do
    (cd "$F" && "$sh" "$T/lines.sh" >"$T/o" 2>"$T/e")
    r="$r $sh=form$(grep -c 'forms.md:[1-6]:' "$T/o" || true)/rule$(grep -c 'forms.md:[7-9]:' "$T/o" || true)/err$(grep -c . "$T/e" || true)"
  done
  sec '## Step 0:' '## Step 1:' "$E/$PRD" | grep -F '4. **`PRD 없음` 기록**' \
    | grep -oE "grep -rnE '[^']*' [.]harness [.]design 2>/dev/null" > "$T/prd.sh"
  [ "${A01_DROP:-0}" = 1 ] && { grep -v 'PRD 없음(`' "$T/prd.sh" > "$T/p2.sh"; mv "$T/p2.sh" "$T/prd.sh"; }
  (cd "$F" && bash "$T/prd.sh" >"$T/o" 2>"$T/e")
  echo "cmds=$(grep -c . "$T/prd.sh" || true) sprint:$r prd=form$(grep -c 'forms.md:[1-6]:' "$T/o" || true)/rule$(grep -c 'forms.md:[7-9]:' "$T/o" || true)/dup$(sort "$T/o" | uniq -d | grep -c . || true)/err$(grep -c . "$T/e" || true)"
}
# === A-01 측정 끝 ===
```

## A-02 — 계약 `범위 경계` 의 「design-mockup Step 2 가 계약 범위 경계를 읽기」 줄을 이렇게 읽는다

**앵커**: 계약 `## 범위 경계` 표의 그 행 「계약에만 있고 승인 기록에 없는 결정은 원래부터 Step 2 가 못 읽는다(이 계약이 만든 빈틈이 아니다)」.

**무엇이 달라졌나**: 독립 검토 2번이 이 말이 틀렸다고 짚었다. 바꾸기 전 design-mockup `:166` 은 네 칸 결정을 승인 기록 폐기 칸에 적게 했고
Step 2 가 그 칸을 읽어(`:59`) 시안에서 막았다(`:66`). 폐기 칸을 계약 경로만으로 바꾼 이 계약이 만든 빈틈이다 — 경로를 따라 읽으라는 말은
승인 뒤에 도는 Step 6(`:166`)에만 있다. 처리(「바꾸지 않음 · notes 에 남김」)는 그대로다. Step 2 를 고치면 SK-01 (a) 「차이가 모두 Step 6 절 안」
을 벗어나므로 부모에게 넘긴다. notes 「이 계약의 판단」 에 정정을 적었다.

**amend_direction**: `unchanged` — 산문 사유 한 구절의 정정이다. 조건 · 측정 · 허용 경로가 그대로라 통과하는 구현 집합이 바뀌지 않는다.
