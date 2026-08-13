# mistake_tag 정규화 — reflect-kit 공유 SSOT

> `log-reflection.sh`(수집) · `reflect-digest`(집계) · `reflect-promote`(승격) ·
> `reflect-kaizen`(효과 측정) 네 표면이 **같은 그룹 키**를 쓰기 위한 정본.
> 알고리즘·규약은 이 문서, 매핑 데이터는 `tag-lemma-map.tsv`, 실행 구현은
> `../hooks/_lib-tag-canon.sh` 하나뿐이다. **어느 것도 다른 곳에 복제하지 마라.**

## 0. 왜 필요한가 — 측정 버그이지 리포팅 문제가 아니다

ledger 의 `post_freq` 는 태그를 키로 재발을 센다. 같은 근본원인이 여러 표기로 갈라지면
`post_freq` 가 구조적으로 과소집계되고, **실패한 규칙이 "효과 있음" 으로 남아 강등되지 않는다.**
집계 키 선택 자체가 신호 품질을 결정한다는 점은 Alertmanager 의 `group_by` 설계가 보여준다 —
모든 라벨로 그룹핑하면 사실상 aggregation 을 끄는 것이고, 그것은 대개 원하는 설정이 아니다
(<https://prometheus.io/docs/alerting/latest/configuration/>).

**2026-08-13 실측** (`~/.claude/logs/*/reflections-*.md` 전량, `_lib-tag-canon.sh` 로 계산):

| 항목 | 값 |
| --- | --- |
| 전체 엔트리 | 4,691 |
| 원시 distinct 태그 | 2,639 |
| lemma 클러스터 | 2,578 |
| singleton 클러스터 | 2,279 (**singleton_share 0.884**) |
| `skipped-required-api-doc-check` 원시 단독 | 71 |
| 같은 lemma 클러스터 합산 | **110** (+39 회수, 원시 대비 55% 과소집계였다) |
| `edit-before-read` / `edited-before-read` | 51 / 4 → 클러스터 55 |

## 1. 정규화 파이프라인 (결정론적 — LLM 앞단)

LLM 은 새 alias 후보의 **근거를 설명하게만** 하고, 최종 병합은 아래 결정론 규칙 + 감사표로 고정한다.

1. **표기 정규화** — lowercase · 따옴표/백틱 제거 · `공백 _ . : /` → `-` · `[a-z0-9-]` 외 제거 ·
   연속 `-` 축약 · 앞뒤 `-` 제거
2. **verb** — 선두 세그먼트 형태소 정규화 (`edited|editing|edits → edit`). 순수 morphology, 의미 판단 없음
3. **verb-synonym** — 선두 동사 의미 동의어 (`ignore → skip`). **의미 판단이 들어가므로 감사 대상**
4. **synonym** — 비선두 세그먼트 표기 정규화 (복수형 · `pretooluse → pretool`)
5. **alias** — 전체 키 병합. `from`/`to` 는 2~4 적용 **이후의 lemma key** 로 적는다

산출물은 `lemma_key` 다. **`lemma_key` 는 집계용 그룹 키이지 표시용 태그가 아니다.**

**필드 이름(`mistake_tag`) 과 그 줄 패턴도 이 SSOT 에 포함된다.** 수집면(훅 프롬프트가 분석기에게
"이 키로 출력하라" 고 지시하는 문자열)과 집계면(추출기·환경 dedup 게이트가 파싱하는 문자열)이
각자 리터럴을 박아 두면, 한쪽만 바뀌는 순간 추출이 0 건이 되고 어휘 주입이 통째로 빈다 — 에러
한 줄 없이. 정본은 `../hooks/_lib-tag-canon.sh` 의 `tag_canon_field`(이름) ·
`tag_canon_line_re`(grep/sed BRE) · `tag_canon_awk_re`(awk 동적 정규식) 세 접근자이고, 훅은
**접근자로만** 참조한다 (§6.1 규칙 8).

## 2. canonical / alias / raw 의 분리

| 이름 | 정의 | 쓰임 |
| --- | --- | --- |
| `raw_tag` | 분석기가 실제로 쓴 원문 표기 | 감사·재현용. 절대 버리지 않는다 |
| `lemma_key` | §1 파이프라인 출력 | **집계·`post_freq` 의 유일한 키** |
| `canonical_tag` | 같은 `lemma_key` 안에서 **최빈 raw_tag** (동률이면 최근) | 사람이 읽는 대표 이름 · 훅 프롬프트 주입 |
| `aliases` | 같은 `lemma_key` 의 나머지 raw_tag + 개별 freq | 감사표 |
| `family` | 병합하지 않은 채 묶어 **보고만** 하는 상위 계열 | §4 |

- canonical 은 **최빈 표기**를 쓴다. 최빈이 아닌 표기를 canonical 로 강제하려면 ledger 엔트리에
  수동 override 사유를 남긴다. (실사용과 맞는 대신 나중에 이름을 바꾸기 어렵다 — 트레이드오프.)
- `aliases` 는 손으로 고르지 않는다. **`lemma_key` 클러스터의 멤버 전체**가 곧 aliases 다.
  손으로 고르면 비워지고, 비면 `post_freq` 가 과소집계된다.

## 3. 닫힌 라벨 집합을 만들지 마라

- hard enum 금지. 강제 closed set 은 annotator agreement 수치만 올리고 **새 근본원인을 기존
  라벨로 collapse** 시킨다 (Artstein & Poesio: agreement 는 reliability 의 전제일 뿐 validity 를
  보장하지 않고, category 수가 적으면 우연 일치가 올라간다 — <https://aclanthology.org/J08-4004/>).
- 대신 **known canonical 우선 · 새 tag 허용 · 새 tag 에는 `new_tag_reason` 필요**.
- 운영 부담(alias 감사)은 늘지만 새 실패 모드가 보존된다. 이것이 의도된 트레이드오프다.

## 4. family — 합치지 않고 보고만 하는 계열

`stale X` 계열처럼 **표기가 닮았다고 무조건 합치면 안 되는** 묶음이 있다.

- **alias 조건**: `undesired_behavior` 와 `desired_behavior` 가 **둘 다 같을 때만** alias 로 묶는다.
- remediation 이 다르면 alias 가 아니라 **family 로만 보고**한다. 합산 금지, `post_freq` 반영 금지.
- family 판별은 결정론적 문자열 규칙이다: 태그를 `-` 로 쪼갠 세그먼트에 `stale` 이 있으면
  `stale-context-reference` family.
- 2026-08 실측 family 구성원 (전부 remediation 이 다르다 — 위젯 재조회 / MCP 재연결 / 인스펙터
  재바인딩 / 진단 오라클 재실행 / VM 재부착 / 태스크 재확인):
  `used-stale-widget-ref`(4) · `used-stale-mcp-connection` · `used-stale-inspector-ref` ·
  `used-stale-diagnostics-oracle` · `reused-stale-vm-attachment` · `retried-stale-vm-connection` ·
  `pursued-stale-task` · `left-stale-references` · `kept-stale-widget` · `answered-stale-task`

Sentry 의 fingerprint 규칙도 자주 바뀌는 값으로 그룹핑하면 나쁜 그룹이 만들어진다고 경고한다
(matcher 가 glob 기반이라는 설명: <https://github.com/getsentry/sentry/issues/75567>).
**주의**: 이전 판본이 Sentry 문서에서 직접 인용하던 한 문구는 2026-08-13 재확인에 실패했다.
확인되지 않은 직접 인용은 쓰지 않는다 — 1 차 근거는 위 Prometheus `group_by` 쪽으로 옮긴다.

## 5. 파편화 지표 — `fold_ratio` 로 판정하지 마라

`tag_canon_fragmentation` 이 내는 7 열 중 두 지표의 역할이 다르다.

| 지표 | 정의 | 재는 것 | 2026-08-13 전량 실측 |
| --- | --- | --- | --- |
| `fold_ratio` | raw_distinct / clusters | **정규화기가 얼마나 접었는가** | 1.02 |
| `singleton_share` | freq==1 클러스터 / 전체 클러스터 | **어휘가 얼마나 파편화됐는가** | **0.884** |

`fold_ratio` 는 클러스터링이 **아무것도 못 묶으면 1.00** 이 되어 "정상" 으로 읽힌다 —
파편화 탐지기로 쓸 수 없다. 어휘 파편화 판정은 `singleton_share` 로 한다.

- 임계 **`singleton_share > 0.70`** 은 **hypothesis** 다. 2026-08-13 baseline 0.884 를 기준점으로
  `/reflect-kaizen` 이 calibrate 한다. 외부 연구 근거 없음 — 운영 데이터로만 조정한다.
- 임계 초과 상태에서 나온 `post_freq` 는 과소집계이므로, ledger calibration 을
  `low-confidence` 로 표시하고 **`post_freq == 0` demotion 후보를 내지 않는다.**

## 6. 실행 오라클 (문서에 그렇게 적혀 있다 = 증거 아님)

**절대경로로 source 하라. `cd` 로 맞춰 놓고 `. ./_lib-...` 하지 마라** — 아래 §6.1 참조.

```bash
. "<repo>/reflect-kit/hooks/_lib-tag-canon.sh"    # 또는 "${CLAUDE_PLUGIN_ROOT}/hooks/..."

# 양성 대조 — 아래 측정을 신뢰하기 전에 먼저 돌린다 (§6.1 규칙 6)
tag_canon_selftest

# 단일 태그 → lemma key
printf '%s\n' edited-before-read ignored-required-api-doc-check | tag_canon_keys

# 클러스터 (cluster_freq \t canonical \t aliases)
tag_canon_groups ~/.claude/logs/*/reflections-*.md | head

# 파편화 7 열
tag_canon_fragmentation ~/.claude/logs/*/reflections-*.md
```

bash / zsh / sh 세 셸에서 동일 출력을 확인했다 (2026-08-13, cwd 4 종 × 셸 3 종 = 12 회 실행
→ `sort -u` 1 행). 로그가 없는 환경에서는 `REFLECT_TAG_LEMMA_MAP` 로 맵 경로를 바꿔 fixture 로
검증할 수 있고, 맵이 없으면 `tag_canon_*` 이 **rc=3 + 순수 kebab 정규화** 로 fail-open 한다
(신호를 잃지 않는다).

### 6.1 셸·cwd 무관성은 검증 대상이다 (무증상 실패 전례)

정규화 라이브러리가 자기 위치를 **cwd 로 추측하면**, 같은 입력이 셸·작업 디렉토리 조합마다
다른 답을 낸다. 에러가 나지 않고 숫자만 달라지므로 눈으로는 잡히지 않는다.

- **전례 (2026-08-13, Phase 12 QA)**: `tag_canon_map_path()` 가 `${BASH_SOURCE[0]}` 에 의존했는데
  **zsh 는 이 배열을 채우지 않는다.** `dirname ""` → `.` → cwd 로 떨어져, cwd 가 `hooks/` 가 아닌
  모든 호출에서 맵을 못 읽고 조용히 순수 kebab 정규화로 전환됐다.
  동일 fixture: bash `5 3 6 1 1.67 0.333 2.00` vs zsh `5 5 6 4 1.00 0.800 1.20`.
  당시 문서·스킬이 모두 `cd .../hooks && . ./_lib-tag-canon.sh` 관용구를 쓰고 있어서
  **우연히 cwd 가 맞을 때만 통과**했고, 3 셸 검증이 그 사실을 가렸다.
- **규칙 1** — 라이브러리는 `REFLECT_TAG_LEMMA_MAP` → 자기 위치(bash `BASH_SOURCE` /
  zsh `%x`) → `CLAUDE_PLUGIN_ROOT` 순으로 해석하고, **어느 단계에서도 cwd 를 쓰지 않는다.**
  전부 실패하면 조용히 넘어가지 않고 stderr 에 경고한 뒤 fail-open 한다.
- **규칙 2** — 호출부는 **절대경로로 source** 한다. `cd` 로 cwd 를 맞춰 두는 관용구는
  라이브러리의 결함을 가리므로 쓰지 않는다.
- **규칙 3** — 3 셸 회귀 검증은 **cwd 를 바꿔 가며** 돌린다. 같은 cwd 에서 3 번 돌리면
  cwd 의존 결함은 절대 드러나지 않는다.
- **규칙 4** — 파일 인자에 글롭을 쓸 때 zsh 는 매치 0 건이면 `nomatch` 로 명령을 통째로
  죽인다. 스크립트에서는 `find ... -name 'reflections-*.md'` 로 열거해 넘긴다
  (`log-reflection.sh` 가 그렇게 한다).
- **규칙 5** — 라이브러리 안의 외부 변수는 전부 `${VAR:-}` 로 받는다. 같은 사이클에 발견된
  **두 번째 무증상 실패**가 이것이었다: `set -u` 를 쓰는 호출자에서 `$REFLECT_TAG_LEMMA_MAP`
  이 unbound 로 함수를 중도 이탈시키면 호출자는 빈 경로를 받아 조용히 순수 kebab 정규화로
  떨어진다 (`5 3 6 1 …` → `5 5 6 4 …`). 회귀 검증은 `set -u` 유/무 **양쪽**으로 돌린다.

- **규칙 6 — 일치성 게이트는 양성 대조로 시작한다.** 24 회 실행을 `sort -u` 로 비교하는 게이트는
  **입력이 0 매치면 거짓 PASS 한다.** 추출이 0 건이면 모든 셸이 `0 0 0 0 0.00 0.000 0.00` 을
  내므로 `sort -u` 가 1 행이 되고 "전 셸 일치" 로 읽힌다.
  **전례 (2026-08-13, Phase 12 재검증)**: fixture 를 `- mistake_tag:`(선행 하이픈)로 만든 상태에서
  24 회 전부 그 값이었고 게이트는 PASS 였다 — 태그를 한 건도 세지 않은 채로. 일치성만 보는
  오라클은 **아무것도 안 하는 구현을 통과시킨다.** 그래서 게이트는 `tag_canon_selftest` 로
  시작한다 (접힘 4→2 + canonical 최빈형 + 추출 4 건을 함께 단정하고, 실패하면 사유를 출력한다).

```bash
. "<repo>/reflect-kit/hooks/_lib-tag-canon.sh" && tag_canon_selftest
# SELFTEST_OK raw=4 clusters=2 canonical=edit-before-read

# selftest 의 판별력을 확인할 때는 반드시 export 로 넘긴다 (아래 주의 참조)
( export REFLECT_TAG_LEMMA_MAP=/nonexistent; . "<repo>/reflect-kit/hooks/_lib-tag-canon.sh"
  tag_canon_selftest )   # → SELFTEST_FAIL fold raw=4 clusters=4
```

**주의 — `VAR=x . lib; func` 로 음성 대조를 돌리지 마라.** 명령 앞 변수 할당은 그 명령에만
붙는다. `.`(source)는 특수 빌트인이라 셸에 따라 할당이 남기도 하고 남지 않기도 해서,
**뒤이어 호출하는 함수는 그 변수를 못 볼 수 있다.** 2026-08-13 재검증에서 실제로
`REFLECT_TAG_LEMMA_MAP=/nonexistent . lib; tag_canon_selftest` 가 `SELFTEST_OK` 를 냈고,
"맵이 없어도 통과한다 = selftest 가 오라클이 아니다" 로 잘못 읽힐 뻔했다. `export` 로 넘기면
같은 조건이 정상적으로 `SELFTEST_FAIL` 이다 (위 실측). 음성 대조가 통과하면 **구현을 의심하기
전에 대조 자체가 성립했는지** 확인하라.

- **규칙 7 — "0 건" 을 PASS 로 삼는 grep 오라클은 `-F` 를 쓰거나 메타문자를 이스케이프한다.**
  substring 오탐(거짓 양성)만 조심하면 된다고 생각하기 쉬운데, 반대 방향인 **거짓 음성**이 더
  위험하다 — "0 건" 이 곧 PASS 인 조건에서 패턴이 잘못되면 **위반이 있어도 통과**한다.
  **전례 (2026-08-13)**: 이 환경의 `grep` 은 ugrep 7.5.0 이고 패턴 **중간의 `$` 를 앵커로
  해석**한다. Phase 12 계약 RE-02 의 측정문이 그 경로였다 —
  `grep -c 'source "$SCRIPT_DIR/_lib-'` 는 **0** 을 내지만 `grep -cF` 와 `grep -c '...\$...'` 는
  **3** 을 낸다 (참값은 3). 오라클이 참인 매치를 0 으로 보고한 것이다.
  변수 표기(`$VAR`)·`.`·`*`·`[` 를 문자 그대로 찾을 때는 `-F` 를 기본으로 쓴다.

- **규칙 8 — "N 곳에만 존재" 를 재는 오라클은 대상을 역할이 구별되는 형태로 좁히고,
  더 나아가 그 문자열을 코드에서 지워라.** 규칙 7 의 `-F` 는 **거짓 음성**만 막는다. 반대로
  패턴이 너무 넓으면 **거짓 양성**이 나서 중복이 아닌 것을 중복으로 센다.
  **전례 (2026-08-13, Phase 12 오라클 스프린트)**: `grep -rlF 'mistake_tag:' reflect-kit/hooks`
  가 2 행을 냈는데 두 번째 매치는 추출 규칙이 아니라 **LLM 프롬프트 안의 YAML 스키마 예시**
  였다 — `-F` 를 지켰는데도 substring 오탐에 걸린 것이다. 이때 오라클을
  `'^[[:space:]]*mistake_tag:'` 로 좁히면 측정은 통과하지만 **리터럴은 여전히 두 곳에 남는다**
  (측정만 조용해지고 결함은 남는다).
  두 방향을 한 번에 없애는 방법은 **문자열 자체를 한 곳으로 옮기는 것**이다. 이름과 패턴을
  라이브러리 접근자(§1)로만 참조하면 "1 곳에만 존재" 가 문서상의 주장이 아니라 **`-F` 로
  곧바로 확인되는 사실**이 되고, 한쪽만 바뀌는 무증상 실패가 원천적으로 불가능해진다.

- **규칙 9 — 훅 코드 조각을 떼어 돌리는 프로브는 실 로그 버킷을 `log_dir` 로 받지 않는다.
  그리고 정리 여부는 한 버킷이 아니라 `~/.claude/logs` **전체**를 훑어 확인한다.**
  `log_hook_error`(`_lib-project-id.sh`)는 **디렉토리가 존재하기만 하면** 아무 검사 없이
  `"$log_dir/.errors.log"` 에 append 한다 — 프로브에 실 버킷 경로를 넘기면 사용자 로그가 조용히
  오염된다. 프로브는 `mktemp -d` 로 만든 복제 버킷에 `reflections-*.md` 를 복사해 돌리고,
  세션 식별자를 고정(`session_id=probe` 등)해 사후 감사가 가능하게 한다.
  **전례 (2026-08-13, Phase 12 오라클 스프린트)**: SC-04 프로브를 실 버킷에 대고 돌려
  `fit-pal/.errors.log` 에 `session=probe` 4 행이 들어갔다. 이를 지운 뒤 **그 한 버킷만 다시 보고**
  "잔여 0 행" 이라고 사이드카에 적었는데, 같은 프로브가 `coupon-stl` 에도 2 행을 남기고 있었다
  (해당 파일은 프로브가 **새로 만든** 것이라 파일 전체가 산출물이었다). 한 버킷 감사를 전역
  결론으로 쓴 것이 오류였다 — QA 가 `grep -rF` 로 전 버킷을 훑어 잡았다.
  감사·복구 절차는 다음 세 가지를 **모두** 만족해야 한다.
  1. 감사 범위를 명령으로 열거한다 — `find ~/.claude/logs -mindepth 1 -maxdepth 1 -type d | wc -l`
     로 버킷 수를 산출하고 `grep -rlF 'session=<probe id>' ~/.claude/logs` 로 전수 검색한다.
  2. 오염 파일이 **프로브가 생성한 것**이면 비우지 말고 지운다. `stat -f '%SB'` 로 birth 가
     프로브 시각과 같고 비-프로브 행이 0 이면 파일 부재가 원래 상태다.
  3. 사이드카에는 "잔여 0 행" 이 아니라 **감사 범위·명령·출력**을 적는다. 범위를 적지 않은
     완료 선언은 다음 사람이 검증할 수 없다.

현재 회귀 게이트 실측: `tag_canon_selftest` → `SELFTEST_OK` · 이어서
`{set -u 유·무} × {bash·zsh·sh} × {cwd 4 종}` = **24 회 실행 → `sort -u` 1 행** (2026-08-13).
프로브 잔여물 전수 감사 실측 (2026-08-13, 11 버킷 · 49 파일):
`grep -rlF 'session=probe' ~/.claude/logs` → **0 파일**.

## 7. 새 alias 를 추가하는 절차

1. `/reflect-digest` 의 `## 병합 보류` 또는 `## 원인 계열 (family)` 에서 후보를 고른다.
2. 두 태그의 `undesired_behavior` / `desired_behavior` 를 **원문 인용**해 같은지 확인한다.
3. 같으면 `tag-lemma-map.tsv` 에 `alias` 행을 추가하고 `reason` 열에 실측 근거(건수 포함)를 적는다.
4. `tag_canon_groups` 를 재실행해 클러스터가 실제로 합쳐졌는지 **출력으로** 확인한다.
5. 다르면 추가하지 말고 family 로만 남긴다.
