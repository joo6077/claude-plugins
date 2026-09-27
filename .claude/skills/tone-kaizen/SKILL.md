---
name: tone-kaizen
description: >
  tone-kit 스킬 3종과 references 9종의 품질을 docs/tone/ 리서치 문서 기준으로 주기 개선한다.
  이 레포 개발용 스킬이며 tone-kit 플러그인에 포함되지 않는다.
  harness-kaizen, rust-kaizen 과 동일한 패턴.
  "/tone-kaizen", "톤 카이젠", "tone-kit 개선" 같은 요청 시 트리거.
  리서치 문서 갱신에는 트리거하지 않는다 — /tone-research 를 사용한다.
argument-hint: ""
user-invocable: true
---

# Tone Kaizen

`tone-kit` 스킬·references 를 리서치 문서 기준으로 개선한다.

# Gotchas

1. **리서치 문서에 근거가 없는 개선은 하지 마라** — 추측으로 Gotchas 를 늘리면 스킬이 길어지기만 한다. 모든 변경은 `docs/tone/` 의 원칙이나 실측 피드백을 근거로 한다.
2. **규칙 강도를 조용히 올리지 마라** — `관측 컨벤션` 을 `MUST` 로 승격하려면 공개 1차 출처가 새로 생겨야 한다. 승격 시 근거 URL 을 함께 넣는다.
3. **한 사이클에 1~2개 surface 만 수정하라** — scope-creep 판정은 파일 수가 아니라 관심사 수 기준이다.
4. **description 변경은 사용자 승인을 받아라** — 트리거 어휘를 바꾸면 배타성이 깨질 수 있다. 변경 시 substring containment 를 다시 계산한다 (V4 는 set intersection 만 본다).
5. **grep 패턴을 고쳤으면 실행하라** — 서술만 바꾸고 넘어가면 죽은 가드가 된다. bash·zsh 양쪽에서 돌리고, 준수 상태에서 0건이 정상인 패턴은 합성 양성 케이스로 살아 있음을 증명한다.
6. **스킬 3개 상한을 유지하라** — 새 기능이 필요하면 기존 3개에 흡수할 수 없는지 먼저 검토한다. audit 을 별도 스킬로 분리하지 마라 — 규칙 보유 스킬은 자기 audit 을 내장한다.
7. **references 하위 디렉토리를 만들지 마라** — 검증 스크립트의 glob 과 문서 동기화가 1-level 만 본다.
8. **어댑터를 추측으로 추가하지 마라** — 위반 실측이 없는 스택에 어댑터를 만드는 것은 이 킷 자신의 원칙 위반이다.

# Process

## Step 1. 현재 상태 읽기

- `tone-kit/skills/*/SKILL.md` 3종
- `tone-kit/references/*.md` 9종
- `tone-kit/templates/*.md` 6종
- `docs/tone/*.md` 11종 (리서치 문서 8종 + overview · research-log · templates)
- 글로벌 피드백에 tone-kit 관련 항목이 있으면 함께 읽는다

## Step 2. 격차 분석

| 축 | 확인 |
|---|---|
| 근거 정합 | 리서치 문서의 원칙 중 references 에 반영되지 않은 것 |
| 강도 정합 | references 의 강도가 리서치 문서의 출처 강도를 넘는 항목. 먼저 아래 블록으로 모든 규칙 행의 강도를 읽었는지 확인한다 |
| 축 라벨 | 코어 문서에 어댑터·로케일 내용이 섞였는지 |
| 게이트 생존 | grep 패턴이 실제로 실행되고 양성을 잡는지 |
| 중복 | 같은 규칙이 두 파일에 정의됐는지 (SSOT 위반) |
| 트리거 | 신규 킷 등장으로 배타성이 깨졌는지 |
| 상한 | SKILL.md 500줄 · references 1-level |

격차를 표로 낸다: `| # | 축 | 격차 | 근거 | 제안 |`

강도 칸은 글자 그대로 맞대지 않는다 — `관측 컨벤션 (성능 근거는 SHOULD 수준)` 처럼 뒤에 글이 붙은 행(`adapter-dart-flutter.md` D-04)을 못 읽은 채 「63 개만 판정」 이 된 적이 있다. 칸 위치는 파일마다 다르다(세 칸 표 · 네 칸 표). 행 번호 모양으로 거르지 않는다 — `D-04` 꼴만 세면 `core-antipatterns.md` 의 `A` ~ `J` 행이 통째로 빠진 채 「다 읽었다」 가 된다. 저장소 폴더에서 돌리고 `unread` 가 0 이 아니면 그 행부터 본다.

```bash
# 강도 칸 앞머리 판정 — 강도 칸이 MUST · SHOULD · 관측 컨벤션 · 합성 으로 시작하면 읽은 것으로 센다
verdicts=$(find tone-kit/references -maxdepth 1 -type f -name '*.md' | sort | while IFS= read -r doc; do
  awk -F'|' -v doc="$(basename "$doc")" '
    /^\|/ && /\| *강도 *\|/ { col = 0; for (i = 1; i <= NF; i++) { cell = $(i); gsub(/^ +| +$/, "", cell); if (cell == "강도") col = i }; next }
    col && /^\| *:?-+/ { next }
    col && /^\|/ {
      id = $(2); gsub(/^ +| +$/, "", id); cell = $(col); gsub(/^ +| +$/, "", cell)
      if (cell ~ /^(MUST|SHOULD|관측 컨벤션|합성)/) print "READ"; else print "UNREAD " doc ":" id " " cell
      next
    }
    !/^\|/ { col = 0 }
  ' "$doc"
done)
read_n=$(printf '%s\n' "$verdicts" | grep -c '^READ$')
unread=$(printf '%s\n' "$verdicts" | grep '^UNREAD ')
unread_n=$(printf '%s' "$unread" | grep -c .)
echo "rules=$((read_n + unread_n)) read=$read_n unread=$unread_n"
[ -n "$unread" ] && printf '%s\n' "$unread"
```

## Step 3. 개선 적용

우선순위: 게이트 생존 > 근거 정합 > 강도 정합 > 중복 > 문구.

한 사이클에 1~2 surface. 나머지는 다음 사이클로 넘기고 그 사실을 보고에 남긴다.

## Step 4. 회귀 검증 (필수)

```bash
python3 scripts/validate-plugin.py tone-kit
python3 scripts/validate-plugin.py
python3 scripts/sync-evals.py --check-only
python3 scripts/run-evals.py tone-kit --verbose
python3 scripts/sync-docs.py --check-only
```

`validate-plugin.py tone-kit` 은 **등록된 검사 전부 OK** 여야 한다 (목록은 아래 명령으로 얻는다).

description 을 고쳤으면 substring containment 를 수동 계산한다 — V4 는 set intersection 만 검사한다.

grep 패턴을 고쳤으면 bash·zsh 양쪽에서 실행하고 합성 양성 케이스로 생존을 증명한다.

등록된 검사 목록은 개수를 적지 말고 **명령으로 얻는다.** 검사가 늘어도 이 문서를 고칠 일이 없다.

```bash
grep -oE '"[a-z-]+": check_v[0-9]+' scripts/validate-plugin.py | sed -E 's/"([a-z-]+)".*/\1/'
```

## Step 5. 보고

```text
## tone-kaizen 사이클 N (YYYY-MM-DD)

| # | 축 | 변경 | 근거 |
|---|---|---|---|

회귀: 등록된 검사 전부 OK · evals N/N PASS · 배타성 위반 0
다음 사이클 이월: ...
```

## Step 6. 커밋

```text
chore(tone-kaizen-cycle<N>): [개선 내용 요약]
```

# References

- ../../../docs/tone/ — 리서치 문서 8종 (overview · research-log · templates 제외, 개선 근거)
- ../../../tone-kit/references/adapter-contract.md — 어댑터 추가 조건
- ../../../harness/docs/guides/skill-design-guide.md — 스킬 설계 규칙
