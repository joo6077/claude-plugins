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

```bash
cd reflect-kit/hooks && . ./_lib-tag-canon.sh

# 단일 태그 → lemma key
printf '%s\n' edited-before-read ignored-required-api-doc-check | tag_canon_keys

# 클러스터 (cluster_freq \t canonical \t aliases)
tag_canon_groups ~/.claude/logs/*/reflections-*.md | head

# 파편화 7 열
tag_canon_fragmentation ~/.claude/logs/*/reflections-*.md
```

bash / zsh / sh 세 셸에서 동일 출력을 확인했다 (2026-08-13). 로그가 없는 환경에서는
`REFLECT_TAG_LEMMA_MAP` 로 맵 경로를 바꿔 fixture 로 검증할 수 있고, 맵이 없으면
`tag_canon_*` 이 **rc=3 + 순수 kebab 정규화** 로 fail-open 한다 (신호를 잃지 않는다).

## 7. 새 alias 를 추가하는 절차

1. `/reflect-digest` 의 `## 병합 보류` 또는 `## 원인 계열 (family)` 에서 후보를 고른다.
2. 두 태그의 `undesired_behavior` / `desired_behavior` 를 **원문 인용**해 같은지 확인한다.
3. 같으면 `tag-lemma-map.tsv` 에 `alias` 행을 추가하고 `reason` 열에 실측 근거(건수 포함)를 적는다.
4. `tag_canon_groups` 를 재실행해 클러스터가 실제로 합쳐졌는지 **출력으로** 확인한다.
5. 다르면 추가하지 말고 family 로만 남긴다.
