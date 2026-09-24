---
feature: "plugin-validation 문서 페이지를 기준 문서 1.3 판에 맞춰 다시 만들기"
slug: plugin-validation-page-sync
created: "2026-09-24 13:37"
complexity: "중간"
conditions: 27
status: active
owner_session: f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0
conditions_digest: sha256:0c84c3f3266af6ec
locked_at: "2026-09-24 13:50"
---

## 배경

`docs/harness/plugin-validation.html` 이 기준 문서 `harness/docs/guides/plugin-validation-guide.md`
1.1.0 판(V1~V8)에 멈춰 있다. 기준 문서는 1.3.0(V1~V10)이다. 앞 스프린트
`check-count-decouple-and-table-gate` 가 개정 파일 끝 "다음 스프린트로 남기는 것" 1 번으로 넘겼다.

페이지를 기준 문서에 맞추다 보니 **기준 문서 자체에 사실 오류**가 있다. 페이지만 고치면 다음에 다시
만들 때 틀린 값이 되살아나므로 원본도 같이 고친다.

- `--check` 체크 이름 목록이 등록된 10 개 중 8 개뿐 (`arg-substitution` · `table-integrity` 누락)
- 출력 예시에 V9 · V10 줄이 없고, 요약줄이 `Total: 7 plugins — …` 형식인데 실제 스크립트는
  `Total: 14 plugins, 14 OK` 형식이다 (`scripts/validate-plugin.py:889`)
- 출력 예시의 harness 블록이 `0 files — SKIP (no templates/)` 라고 적는데 실제로 `harness/templates/` 에 4 항목이 있다
- 수동 수정 표에 V8 · V9 · V10 이 없고 "나머지 체크(V1~V4, V7)" 라고 적혀 있다
- 킷별 예외 표가 harness · flutter-toolkit · design-kit · rust-kit 에 `templates/` 가 없다고 적는다.
  실제로는 4 · 2 · 8 · 5 개다. 페이지는 앞선 사실 정리(27f5764)에서 이미 바로잡혔고 원본만 틀리다.
  tone-kit(6 개)은 두 곳 모두 표에 없다
- "13개 킷"(실제 14) · "9개 카이젠 스킬"(페이지는 10, 실제로 §7 을 인용하는 카이젠 스킬은 11) 처럼
  개수 표기가 이미 서로 어긋났다. 앞 스프린트 방침대로 **개수를 빼고** "등록된 킷 전부" 로 쓴다
- frontmatter `scope:` 와 §2 코드 블록이 킷 7 개만 나열한다

## GAP 분석 (구현 전 점검 · 복잡도)

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 계층을 관통하나 | 1 (문서) |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌나 | 아니오 (문서 내용만) |
| 소비면 존재 | 반대편이 있나 | 예 — 카이젠 스킬 11 개가 기준 문서 §7 을 인용, `docs/index.html` 이 페이지를 iframe 으로 연다 |
| 회귀 위험 | 기존 동작이 깨질 수 있나 | 예 — 표 끊김(V10) · 가로 넘침 · 대비 |

2 축이 "예" 라 **중간**. 소비면 조건은 AR-02(index 등록) · AR-05(절 제목 유지) 로 따로 둔다.

| 대상 파일 | 실제로 읽은 자리 | 발견한 갭 | 조건 |
| --------- | ---------------- | --------- | ---- |
| `docs/harness/plugin-validation.html` | `:95` "8-카테고리" · `:153` "V1 ~ V8" · `:253` `--check` 값 8 개 · `:296` `plugins —` · `:574-575` V9 · V10 을 예정으로 적음 · `:96,102,117` "13개 킷" · `:485` "10개 카이젠" | V9 · V10 카드 · 예시 · 이력 없음 | SK-01 · SK-02 · SK-05 · SK-06 · ER-01 · ER-04 |
| `harness/docs/guides/plugin-validation-guide.md` | `:482-483` 체크 이름 8 개 · `:487-513` 출력 예시 V8 까지 · `:536` "나머지 체크(V1~V4, V7)" · `:540-546` 수동 수정 표 · `:562-567` 템플릿 "없음" · `:19,33` "13개 킷" · `:577` "9개 카이젠" · `:5` scope 7 킷 | 원본 사실 오류 | SK-03 · SK-06 · ER-02 · ER-03 · ER-04 · ER-05 |
| `scripts/validate-plugin.py` | `:889` 요약줄 `Total: {', '.join(parts)}` · `:916` `--help` 가 등록 표에서 이름을 뽑음 | 사실 기준 (고치지 않음) | SK-02 · SK-03 · SK-06 |
| `docs/index.html` | `file: 'harness/plugin-validation.html'` 1 · 아이콘 키 1 | 없음 | AR-02 |

## 범위 경계

- 바꾸는 파일은 둘이다: `docs/harness/plugin-validation.html`, `harness/docs/guides/plugin-validation-guide.md`
- `docs/index.html` 은 이미 등록돼 있어 건드리지 않는다 (등록 1 · 아이콘 키 1, 봉인 전 실측)
- 기준 문서의 **절 제목은 바꾸지 않는다.** 카이젠 스킬 11 개가 "§7" 을 인용하고, 페이지 카드가 "§3.8" 을 인용한다
- 기준 문서의 기존 마크다운 경고(MD036 29 · MD025 1)는 이번 범위 밖이다. 늘리지만 않는다
- 페이지의 `<style>` 블록은 바꾸지 않는다 — 새 내용은 기존 클래스(`.v-card` · `.card` · `.compare` · `.table-wrap` · `.checklist`)로 짠다
- 기준 문서 버전은 1.3.1 로 올리고 변경 이력에 한 줄 적는다 (사실 정정)
- 배포: PR 을 병합 커밋으로 합치면 GitHub Pages(`main` · `/docs`)가 페이지를 다시 올린다. 기준 문서가
  harness 킷 안에 있으므로 harness patch 릴리스를 함께 한다. 릴리스 커밋은 이 스프린트 구간 밖이다

### 봉인 전 실측값 (2026-09-24, 기준 커밋 390dea8)

- 페이지 V 배지 8 개(V1~V8) · `card-source` 8 개 · 1 행 594 줄 · 외부 리소스 0 · `--accent:#D97757`
- 페이지 `--check` 값 8 개 · 기준 문서 `--check` 체크 이름 8 개 · 등록 표 10 개
- 변경 이력 버전: 페이지 {1.0.0, 1.1.0} · 기준 문서 {1.0.0, 1.1.0, 1.2.0, 1.3.0}
- `[0-9]+개 킷` (변경 이력 행 제외): 페이지 3 · 기준 문서 2. `[0-9]+개 카이젠`: 페이지 1 · 기준 문서 1
- `plugins —` 옛 요약줄: 페이지 1 · 기준 문서 1. harness 블록 `no templates/`: 페이지 1 · 기준 문서 1
- 기준 문서 `나머지 체크(V1~V4, V7)`: 1. `| harness | \`templates/\` 없음`: 1
- tone-kit 카탈로그 행: 페이지 0 · 기준 문서 0
- 기준 문서 마크다운 경고(markdownlint-cli2 0.23.2 · MD013 끔 — 편집기와 같은 설정): MD025 1 · MD036 29 · MD040 2
- `node scripts/check-docs-a11y.js docs/harness/plugin-validation.html` → `of=0/0/0 err=0 contrastFail=0` · `1/1 PASS`
- 변경 범위 명령 기준값: 구현 전이라 0 줄

### 공통 정의

- `P=docs/harness/plugin-validation.html` · `G=harness/docs/guides/plugin-validation-guide.md`
- 등록 표 이름: `grep -oE '"[a-z-]+": check_v[0-9]+' scripts/validate-plugin.py | sed -E 's/"([a-z-]+)".*/\1/' | sort`
- `--help` 체크 이름 (실행 출력): `python3 scripts/validate-plugin.py --help | sed -n 's/^체크 이름: //p' | tr ',' '\n' | tr -d ' ' | sort` — 봉인 전 실측 10 개, 등록 표 이름과 같다
- 구간 상한 (이 레포 관례 — `feat/<slug>` 가지 + `Merge pull request #N from joo6077/feat/<slug>`):

```bash
sprint_head() {  # 머지됐으면 머지 커밋의 가지 쪽 부모, 아니면 가지 끝
  m=$(git log --merges --format=%H --grep="from joo6077/feat/${1}" -1)
  [ -n "$m" ] && { git rev-parse "$m^2"; return 0; }
  git rev-parse --verify -q "feat/${1}" && return 0
  echo "UNRESOLVED feat/${1}" >&2; return 1
}
```

- 오라클 해소: SK-04 — 재는 것이 문서의 변경 이력 자체다. 실행으로 대조할 동작이 없다
- 오라클 해소: SK-05 — 재는 것이 문서의 향후 계획 목록 자체다. 실행으로 대조할 동작이 없다
- 오라클 해소: AR-05 — 기준 커밋의 절 제목과 대조한다. 절 제목을 인용하는 소비자(카이젠 스킬 11 개)가 깨지지 않았는지가 취지다
- 실행 결과와 대조하는 조건: SK-02 · SK-03(`--help` 출력) · SK-06(`validate-plugin.py` 실제 출력) · ER-03(`ls` 실제 항목 수) · SC-01~03 · DG-04
- AP-02 주의: 측정이 명령 **글자**를 보므로, 강제 푸시 문구를 인자로 담은 명령(양성 대조 재실행 · 그 문구를 쓰는 편집)을 봉인 뒤에 돌리면 오탐이 난다. 양성 대조는 봉인 전에 끝냈다 — 임시 기록 3 줄 중 강제 푸시 2 줄 → 2
- 양성 대조 실측(봉인 전, 임시 사본): AR-03 외부 스크립트 1 줄 → 1 · AR-05 `## 7.` 제목 변경 → 2 (`diff` 원출력은 4 줄 — 그래서 `^[<>]` 줄만 센다) · AP-01 `v0.12.1` 삽입 → 1 · RE-02 스타일 한 줄 삽입 → 1
- 봉인 전 교차 진단(qa-evaluator 1 회)이 짚어 고친 것: ER-03 `$n[^0-9]` 가 zsh 에서 `bad math expression` 으로 죽음 → `${n}` · `diff` 출력 줄 수 표기가 모호 → `^[<>]` 줄 수로 · ER-05(a) 실행 명령 없음 → 한 줄 명령 · DG-02 도구 판 고정 · AR-04 400 하한이 늘 참 → 594 로

### 설계 결정

- 개수 표기(킷 수 · 카이젠 스킬 수)는 고치지 않고 **뺀다.** 킷이 늘 때마다 낡는다 — 이미 페이지 13 · 문서 13 · 실제 14 로 갈렸다
- 킷 이름 나열은 빼고 "marketplace.json 에 등록된 킷 전부" 로 쓴다. 나열하려면 14 개 전부여야 한다 (ER-05)
- 출력 예시는 "형식 예시" 로 둔다. 현재 버전 번호를 박지 않는다 (AP-01) — 릴리스할 때마다 낡는다

## Skill

- [ ] SK-01: Given 페이지 §3 · When 검사 카드를 세면 · Then V1~V10 열 개가 있고, 옛 개수 표기가 0 건이다 [exact, enumerated]
      (측정 (a): `grep -oE '<div class="v-badge">V[0-9]+</div>' $P | grep -oE 'V[0-9]+' | sort -V -u | paste -sd, -` 가 `V1,V2,V3,V4,V5,V6,V7,V8,V9,V10` ·
       (b): `grep -cE '8-카테고리|V1 ~ V8|8가지 카테고리|V1~V8 검증' $P` 가 0 · 양성 대조: 봉인 전 (a) 8 개 · (b) 4)
- [ ] SK-02: 페이지의 `--check` 값 목록이 스크립트가 실제로 받는 체크 이름과 정확히 같은 집합이다 [exact, enumerated]
      (측정: `grep -F '<code>--check</code> 값:' $P | grep -oE '<code>[a-z-]+</code>' | sed -E 's#</?code>##g' | grep -vx -- '--check' | sort` 과
       §공통 정의의 `--help` 체크 이름을 `diff` 한 출력의 `grep -cE '^[<>]'` 가 0 · 그리고 그 목록을 쉼표로 이어 `python3 scripts/validate-plugin.py harness --check=<목록>` 을 실제로 돌려 종료 코드 0
       (모르는 이름이면 스크립트가 `알 수 없는 체크 이름` 으로 2 를 낸다) · 양성 대조: 봉인 전 `arg-substitution` · `table-integrity` 2 줄 차이 · `--check=bogus` 는 종료 코드 2)
- [ ] SK-03: 기준 문서의 `--check` 체크 이름 목록이 스크립트가 실제로 받는 체크 이름과 정확히 같은 집합이다 [exact, enumerated]
      (측정: `awk '/^`--check` 에 사용하는 체크 이름:/{getline; print}' $G | grep -oE '`[a-z-]+`' | tr -d '`' | sort` 과 §공통 정의의 `--help` 체크 이름을 `diff` 한 출력의 `grep -cE '^[<>]'` 가 0 ·
       그리고 그 목록으로 `python3 scripts/validate-plugin.py harness --check=<목록>` 을 실제로 돌려 종료 코드 0 · 양성 대조: 봉인 전 2 줄 차이 · `--check=bogus` 는 종료 코드 2)
- [ ] SK-04: 기준 문서와 페이지의 변경 이력 버전 집합이 같은 기대값이고, 기준 문서 frontmatter 버전이 새 이력 버전과 같다 [exact, enumerated]
      (측정: 기준 문서 `awk '/^## 8\. 변경 이력/,0' $G | grep -oE '^\| 20[0-9-]+ \| [0-9]+\.[0-9]+\.[0-9]+' | grep -oE '[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | paste -sd, -` ·
       페이지 `grep -oE '<tr><td>20[0-9-]+</td><td>[0-9]+\.[0-9]+\.[0-9]+</td>' $P | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | sort -V | paste -sd, -` ·
       두 출력이 모두 `1.0.0,1.1.0,1.2.0,1.3.0,1.3.1` · `grep -m1 '^version:' $G` 출력이 `version: 1.3.1`)
- [ ] SK-05: 페이지 "다음 갱신 예정" 목록이 V11 · V12 둘이고 이미 만든 V9 · V10 을 예정으로 적지 않는다 [exact, enumerated]
      (측정: `awk '/다음 갱신 예정/,/<\/ul>/' $P | grep -oE '<strong>V[0-9]+</strong>' | grep -oE 'V[0-9]+' | paste -sd, -` 가 `V11,V12` · 양성 대조: 봉인 전 `V9,V10`)
- [ ] SK-06: 페이지와 기준 문서의 출력 예시가 스크립트의 실제 출력과 같은 줄 머리(검사 번호 + 이름)를 같은 순서로 담고, 요약줄이 실제 형식이다 [exact, enumerated]
      (측정: 실제 `python3 scripts/validate-plugin.py harness | grep -oE '^  V[0-9]+ [a-z-]+' | paste -sd, -` 와,
       각 파일 `$P` · `$G` 의 `awk '/=== harness ===/,/^$/' <파일> | grep -oE '^  V[0-9]+ [a-z-]+' | paste -sd, -` 가 같다 ·
       같은 방식으로 `=== react-kit ===` 블록도 실제 `validate-plugin.py react-kit` 과 같다 ·
       각 파일 `grep -cE '^Total: [0-9]+ plugins, '` 이 1 이상 · `grep -c 'plugins —'` 가 0 ·
       양성 대조: 봉인 전 두 파일 모두 harness · react-kit 블록이 V8 에서 끝나 V9 · V10 이 빠진다 · `plugins —` 페이지 1 · 기준 문서 1)

## Script

- [ ] SC-01: 페이지가 문서 접근성 검사를 통과한다 — 375 · 768 · 1280px 가로 넘침 0, 콘솔 에러 0, 대비 미달 0 [exact]
      (측정: `node scripts/check-docs-a11y.js docs/harness/plugin-validation.html` 출력이 `of=0/0/0 err=0 contrastFail=0` 을 담고 마지막 줄 `1/1 PASS` · 종료 코드 0)
- [ ] SC-02: 검증 스크립트가 전 킷 통과한다 — 기준 문서의 표가 끊기지 않았다(V10) [exact]
      (측정: `python3 scripts/validate-plugin.py` 끝 두 줄이 `Total: 14 plugins, 14 OK` · `Exit: 0`)
- [ ] SC-03: 레포 문서 검사 세 개가 모두 종료 코드 0 이다 [exact, enumerated]
      (측정: `scripts/check-contrast-claims.py` · `scripts/check-docs-links.py` · `scripts/check-stale-values.py` 를 각각 `python3` 으로 돌려 종료 코드가 0)

## Error

- [ ] ER-01: 페이지 §6 에 V9 · V10 의 나쁜 예 · 좋은 예 짝이 하나씩 있다 [exact, enumerated]
      (측정: `grep -c 'compare-label">✗ V9'` · `grep -c 'compare-label">✓ V9'` · `grep -c 'compare-label">✗ V10'` · `grep -c 'compare-label">✓ V10'` 이 `$P` 에서 각각 1)
- [ ] ER-02: 수동 수정 목록이 `--fix` 대상이 아닌 검사 전부(V1 · V2 · V3 · V4 · V7 · V8 · V9 · V10)를 담는다 — 페이지와 기준 문서 둘 다 [exact, enumerated]
      (측정: 페이지 `awk '/<h3>수동 수정<\/h3>/,/<\/ul>/' $P | grep -oE '<strong>V[0-9]+</strong>' | grep -oE 'V[0-9]+' | sort -V | paste -sd, -` ·
       기준 문서 `awk '/^### 수동 수정/,/^### 카이젠 위임/' $G | grep -oE '^\| V[0-9]+ \|' | grep -oE 'V[0-9]+' | sort -V | paste -sd, -` 가 둘 다 `V1,V2,V3,V4,V7,V8,V9,V10` ·
       `grep -cF '나머지 체크(V1~V4, V7)' $G` 가 0 · 양성 대조: 봉인 전 페이지 `V8` 까지 · 기준 문서 `V7` 까지 · 문구 1)
- [ ] ER-03: 킷별 예외 표가 `templates/` 를 가진 킷 6 개 — `harness` · `flutter-toolkit` · `design-kit` · `rust-kit` · `react-kit` · `tone-kit` — 의 항목 수를 실제와 같게 적는다. 페이지와 기준 문서 둘 다 [exact, enumerated]
      (측정: 킷 `k` 마다 `n=$(ls -1 $k/templates | wc -l | tr -d ' ')` 로 실제 수를 구하고, 페이지 `grep "<tr><td>$k</td>" $P | grep -cE "<code>templates/</code> ${n}[^0-9]"` 과
       기준 문서 `grep -E "^\| $k \|" $G | grep -cE "\`templates/\` ${n}[^0-9]"` 이 각각 1 · 봉인 전 실제 수: 4 · 2 · 8 · 5 · 9 · 6 ·
       양성 대조: 봉인 전 페이지 tone-kit 0 · 기준 문서 harness · flutter-toolkit · design-kit · rust-kit · tone-kit 0)
- [ ] ER-04: 금방 낡는 개수 표기가 없다 — 킷 수와 카이젠 스킬 수를 두 파일 어디에도 숫자로 적지 않는다 (변경 이력 행 제외) [exact]
      (측정: `grep -vE '^\s*<tr><td>20[0-9]{2}-' $P | grep -cE '[0-9]+ ?개 (킷|카이젠)'` 과 `grep -vE '^\| 20[0-9]{2}-' $G | grep -cE '[0-9]+ ?개 (킷|카이젠)'` 이 둘 다 0 ·
       양성 대조: 봉인 전 페이지 4 · 기준 문서 3)
- [ ] ER-05: 두 파일이 틀린 킷 정보를 적지 않는다 — (a) 킷 이름을 나열하는 자리는 등록된 14 킷 전부를 적거나 아예 나열하지 않는다 (b) 출력 예시의 harness 블록이 `templates/` 없음이라 적지 않는다 [exact]
      (측정 (a): 페이지 `awk '/<h3>적용 범위<\/h3>/,/<\/div>/' $P` · 기준 문서 `grep -m1 '^scope:' $G` · 기준 문서 `awk '/^## 2\. 적용 범위/,/^### 실행 명령/' $G` 세 구간 각각에서
       출력을 `python3 -c "import json,re,sys;ks=[p['name'] for p in json.load(open('.claude-plugin/marketplace.json'))['plugins']];t=sys.stdin.read();print(sum(1 for k in ks if re.search(r'(?<![a-z-])'+re.escape(k)+r'[/\"]',t)))"` 에 넣어
       (등록된 킷 이름 중 바로 뒤에 `/` 나 `"` 가 붙어 나온 것의 수) 각각 0 또는 14 ·
       (b): `awk '/=== harness ===/,/^$/' $P | grep -c 'no templates/'` 와 같은 명령의 `$G` 판이 둘 다 0 ·
       양성 대조: 봉인 전 (a) 13 · 7 · 7 · (b) 1 · 1)

## Architecture

- [ ] AR-01: Given 이 스프린트 커밋이 끝난 뒤 · 변경 파일이 정확히 2 개로 한정된다 [exact, enumerated]
      (측정: `git diff --name-only 390dea8..$(sprint_head plugin-validation-page-sync) -- . ':(exclude).harness/**' | sort` 가 기대 집합 `docs/harness/plugin-validation.html` · `harness/docs/guides/plugin-validation-guide.md` 두 줄과 일치.
       `sprint_head` 는 §공통 정의. `UNRESOLVED` 면 `HEAD` 로 떨어지지 말고 판정 보류)
- [ ] AR-02: 페이지가 문서 사이트 목록에 그대로 등록돼 있다 [exact]
      (측정: `grep -c "file: 'harness/plugin-validation.html'" docs/index.html` 이 1 · `grep -cE "'plugin-validation'\s*:" docs/index.html` 이 1)
- [ ] AR-03: 페이지가 harness 색(`--accent:#D97757`)을 쓰고 외부 CSS · JS 를 불러오지 않는다 [exact]
      (측정: `grep -c -- '--accent:#D97757' $P` 가 1 · `grep -cE '<(link|script)[^>]+(src|href)="https?://' $P` 가 0 ·
       양성 대조: 임시 사본에 `<script src="https://x.invalid/a.js"></script>` 한 줄을 넣으면 1)
- [ ] AR-04: 페이지가 문서 사이트 하한(400 줄)을 지키며 기존보다 줄지 않고, V9 근거 카드가 공식 문서 출처를 단다 [exact]
      (측정: `wc -l < $P` 가 594 이상 (봉인 전 594 — 400 하한은 이미 넘으므로 줄지 않음을 잰다) · `grep -c 'class="card-source" href="https://code.claude.com/docs/en/skills"' $P` 가 1 이상 · `grep -c 'class="card-source"' $P` 가 10 이상)
- [ ] AR-05: 기준 문서의 절 제목이 바뀌지 않았다 — 카이젠 스킬이 "§7", 페이지가 "§3.8" 을 인용한다 [exact]
      (측정: `diff <(git show 390dea8:$G | grep -E '^#{2,3} ') <(grep -E '^#{2,3} ' $G) | grep -cE '^[<>]'` 가 0 · 양성 대조: 임시 사본에서 `## 7. 카이젠 연동` 을 바꾸면 2)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — 출력 예시가 harness 의 현재 버전 번호를 박지 않는다 [exact]
      (측정: `V=$(python3 -c "import json;print(json.load(open('harness/.claude-plugin/plugin.json'))['version'])")` 뒤 `grep -cF "v$V" $P $G` 가 둘 다 0 ·
       양성 대조: 임시 사본에 `v$V` 를 넣으면 1)
- [ ] AP-02: force push 금지 — 이 세션이 봉인 뒤 실행한 명령에 강제 푸시가 0 건이다 [exact]
      (측정: 세션 기록 `~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0.jsonl` 의 `tool_use` 중 이름이 `Bash` 이고
       `timestamp` 가 봉인 시각 이후인 것의 `command` 에서 `git push` 와 함께 `--force` 나 단독 `-f` 옵션이 든 것을 세어 0 ·
       양성 대조: 같은 모양의 한 줄짜리 임시 기록에 `git push --force` 를 넣으면 1)

## Reusability

- [ ] RE-01: N/A (산출물이 문서 두 개뿐이라 재사용 단위 코드가 없다. 측정: AR-01 목록의 확장자가 `.html` · `.md` 뿐)
- [ ] RE-02: 페이지가 기존 스타일을 재사용한다 — `<style>` 블록이 기준 커밋과 바이트 단위로 같다 [exact]
      (측정: `diff <(git show 390dea8:$P | sed -n '/<style>/,/<\/style>/p') <(sed -n '/<style>/,/<\/style>/p' $P) | grep -cE '^[<>]'` 가 0 ·
       양성 대조: 임시 사본의 `<style>` 안에 한 줄을 넣으면 1)

## Diagnostics

- [ ] DG-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: AR-01 목록에 `scripts/release.sh` 0 줄. 대신 SC-02 가 전 킷 검증을 잰다)
- [ ] DG-02: 기준 문서의 마크다운 경고가 기준값보다 늘지 않는다 — 규칙별로 MD025 1 이하 · MD036 29 이하 · MD040 2 이하 · 그 밖의 규칙 0 [exact]
      (측정: 내용이 `{ "config": { "MD013": false } }` 인 설정 파일로 `npx --yes markdownlint-cli2@0.23.2 --config <설정 파일> $G 2>&1 | grep -oE 'MD[0-9]+/[a-z-]+' | sort | uniq -c`.
       0.23.3 도 이 파일에 같은 값을 낸다 — 봉인 전 교차 진단이 두 판을 대조했다)
- [ ] DG-03: N/A (commands.test 는 `bash scripts/release.sh 2>&1 || true` — 릴리스 스크립트라 문서 변경을 재지 않는다. 측정: AR-01 목록에 `scripts/` 0 줄)
- [ ] DG-04: 실제 브라우저에서 문서 사이트를 열어 이 페이지 항목을 누르면 iframe 에 새 페이지가 뜬다 — 제목 "플러그인 검증 가이드" 와 V 배지 10 개가 보이고 콘솔 에러가 0 이다 [exact]
      (측정: `python3 -m http.server` 로 레포 루트를 띄우고 Playwright MCP 로 `/docs/index.html` 을 연 뒤 `[data-id="plugin-validation"]` 를 눌러
       iframe 문서의 `h1` 글자와 `.v-badge` 수를 읽고 `browser_console_messages` 의 error 수를 센다.
       도구가 안 되면: `node` 로 같은 동작을 하는 Playwright 스크립트 · 그것도 안 되면 `[미검증]`)
