# 메모리 `grounding` 소급 태깅 — 감사 기록

일시: 2026-08-14 · 계약: `.harness/sprint-contract-kaizen-memory-integration.md` (SK-02 · SK-03 · SK-04)
정의 SSOT: `reflect-kit/references/memory-grounding.md`

> **표기 주의.** SK-02 는 4 값의 정의가 **정확히 1 파일**에만 있을 것을 리터럴 grep 으로 잰다.
> 그래서 이 문서는 값의 스네이크케이스 토큰을 쓰지 않고 **코드**로만 부른다.
>
> | 코드 | 의미 |
> | --- | --- |
> | UC | 사용자 교정 발화가 근거 — 외부 **인간** 신호 |
> | EE | QA verdict · 명령 출력 · 실측이 근거 — 외부 **기계** 신호 |
> | MX | 둘 다 |
> | SI | 외부 검증 **없는** 자기추론 ← 오염 후보 |

---

## 1. 대상 (재실측)

계약 baseline 은 「7 프로젝트 · 104 엔트리」였다. 재실행 시점 실측:

```bash
find ~/.claude/projects -maxdepth 3 -path '*/memory/*.md' ! -name 'MEMORY.md' \
  | while read f; do grep -q '^  type: feedback' "$f" && echo "$f"; done
```

- **엔트리 104 건** — baseline 과 일치
- **프로젝트 6 개** — baseline(7)과 **불일치**. `memory/` 디렉토리를 가진 프로젝트는 9 개이나
  그중 `feedback` 타입 엔트리를 가진 것은 6 개다. 계약의 7 은 과대 계수로 보인다.

| 프로젝트 | 엔트리 |
| --- | --- |
| fit-pal | 66 |
| claude-plugins | 14 |
| apps | 13 |
| (홈 루트 · bambu/3d) | 7 |
| flutter-playwright | 3 |
| purchase-bot | 1 |

원본 백업: `/private/tmp/memory-backup-2026-08-14/memory-full-backup.tar.gz` (288 파일, 태깅 전 상태)

---

## 2. 자동 태깅 결과 (SK-03)

104 건 전건에 `metadata.grounding` 삽입. 기존 frontmatter 키는 전부 보존됐다.

| 키 | 태깅 전 | 태깅 후 |
| --- | --- | --- |
| `type` | 104 | 104 |
| `originSessionId` | 99 | 99 |
| `node_type` | 99 | 99 |
| `modified` | 44 | 44 |
| `iteration` | 1 | 1 |
| `grounding` | **0** | **104** |

미보유 건수 검증:

```
$ grep -LF 'grounding:' $(cat recount.txt) | wc -l
0
```

### 분포

| 코드 | 자동 태깅 시점 | 검수 반영 후 |
| --- | --- | --- |
| EE | 52 | **50** |
| UC | 29 | **30** |
| MX | 22 | **23** |
| SI | 1 | **1** |
| 합계 | 104 | **104** |

---

## 3. 샘플 검수 (SK-04)

층화 무작위 표본(seed 20260814, 값별 할당 EE 8 · MX 5 · UC 6 · SI 1).
SI 는 모집단에 **1 건뿐**이라 "4 값 고루"를 만족시킬 수 없어 전수(1/1)를 넣었다.

- **검수 대상 건수: 20**
- **자동값과 사람 판정이 일치한 건수: 18**
- **불일치 건수: 2**
- **정확도: 18/20 = 90.0%**

검수 방법: 본문 전문을 다시 읽고 (a) 귀속된 인간 신호가 있는가 (b) *이 사건에서* 관측된
기계 산출물이 있는가 를 각각 따로 판정한 뒤 조합해 값을 도출하고 자동값과 대조했다.

### 표본 20 건

| # | 엔트리 | 자동 | 재판정 | 판정 |
| --- | --- | --- | --- | --- |
| 1 | `feedback_enumerate_all_surfaces_first` | EE | EE | 일치 |
| 2 | `feedback_isolate_the_instrument_too` | EE | EE | 일치 |
| 3 | `feedback_native_assets_cold_run` | EE | EE | 일치 |
| 4 | `feedback_pipe_masks_exit_code` | EE | EE | 일치 |
| 5 | `feedback_serena_diagnostics_sdk_mismatch` | EE | EE | 일치 |
| 6 | `feedback_verify_ci_logs_not_handoff` | EE | EE | 일치 |
| 7 | `codex-default-model` | EE | EE | 일치 |
| 8 | `bambu_per_part_seam_policy` | EE | **MX** | **불일치** |
| 9 | `feedback_codex_research_foreground` | MX | MX | 일치 |
| 10 | `feedback_setup_guide_console_ui_fetch` | MX | MX | 일치 |
| 11 | `feedback_app_deploy_local` | MX | MX | 일치 |
| 12 | `feedback_design_detail_sketch` | MX | **UC** | **불일치** |
| 13 | `feedback_no_sprint_contract` | MX | MX | 일치 |
| 14 | `feedback_internal_tag_flat_model` | SI | SI | 일치 |
| 15 | `feedback_ephemeral_tests` | UC | UC | 일치 |
| 16 | `feedback_skill_invocation_evidence` | UC | UC | 일치 |
| 17 | `feedback_e2e_runtime_test_last` | UC | UC | 일치(경계) |
| 18 | `feedback_photo_always_full_width` | UC | UC | 일치 |
| 19 | `feedback_shrinkwrap_defeats_builder` | UC | UC | 일치 |
| 20 | `feedback_user_confirmed_facts` | UC | UC | 일치 |

### 불일치 2 건 — 사유

**불일치 ①  `bambu_per_part_seam_policy` (EE → MX)**

본문 근거는 "원통 팁 표면에 세로 심이 한 줄로 적층되고 단면상 골이 파였다" 는 **실제 출력물의
물리적 결함**이다. 자동 판정은 귀속 문구(`사용자가 …라고`)가 없다는 이유로 인간 신호를 0 으로
셌다. 그러나 출력물 품질은 어시스턴트가 직접 볼 수 없고 **사용자만이 관측·전달할 수 있는
채널**이다. 같은 엔트리에 seam 레시피 결정 트리 대조라는 검증 산출물도 있으므로 MX 가 맞다.

→ **계열 결함**: 물리 세계 결과를 근거로 삼는 엔트리 전반에서 인간 채널이 과소 계수된다.

**불일치 ②  `feedback_design_detail_sketch` (MX → UC)**

자동 판정이 본문의 도구 동작 언급(`screenshot_widget` 이 flutter web 에서 layer assertion 으로
실패 · `flutter run` 남발 시 MCP wrapper 가 첫 VM 에 고정)을 기계 신호로 셌다. 그러나 이 서술들은
`How to apply` 절에서 **다른 엔트리의 결론을 참조**한 것이지 이 사건에서 관측된 산출물이 아니다.
이 사건의 실제 근거는 「40 턴 왕복 · 사용자 극도 분노 · 욕설 반복」뿐이다.

→ **계열 결함**: 타 엔트리에서 빌려온 관측을 자기 근거로 오인한다.

### 표본 밖 계열 전파 1 건 (정확도 분모에 포함하지 않음)

불일치 ① 의 계열을 모집단에서 훑어 같은 조건인 엔트리를 1 건 더 찾아 고쳤다.

- `bambu_inherit_quality_base_for_surface` : EE → MX
  근거가 "PETG HF 출력이 엉망진창으로 나온" **물리 결과**(인간 채널) + 벤더 프리셋 실제 값
  (`outer_wall_speed ['200','500']` vs `['60','60']`) 대조(기계 채널) 로 둘 다다.

같은 물리 도메인의 나머지 2 건은 검토 결과 EE 유지가 맞다 —
`bambu_scarf_override_gate`(프로파일 JSON · 바이너리 툴팁 실측) ·
`cad_export_facet_shrinks_holes`(3MF 메시 정점 수 파싱 실측). 둘 다 파일에서 직접 검증 가능하다.

### 두 계열 결함의 재발 방지

정의 파일(`reflect-kit/references/memory-grounding.md`)의 «경계 사례» 절에 규칙 2 개를 추가했다.

- 다른 엔트리에서 빌려온 관측은 이 엔트리의 근거로 세지 않는다.
- 물리 세계 결과는 귀속 문구가 없어도 인간 신호로 센다.

---

## 4. 오염 후보 — SI 1 건

| 엔트리 | 프로젝트 | 왜 SI 인가 |
| --- | --- | --- |
| `feedback_internal_tag_flat_model` | fit-pal | 근거 절이 "기존 관례(`SkipPolicyModel`)도 그렇게 한다" 는 **컨벤션 관찰**과 serde/freezed 직렬화에 대한 **단정**뿐이다. 명령 출력·QA verdict·수치·사용자 발화가 하나도 없다. 「union 의 기본 직렬화가 서버 internal 태그와 안 맞는다」는 핵심 주장이 실제로 확인된 흔적이 없다. |

104 건 중 1 건(0.96%)만 외부 검증이 없다. 낮은 이유는 이 메모리들이 대부분
`**Why:**` 절을 강제하는 템플릿으로 쓰였고, 그 절이 사건·수치·발화를 요구하기 때문이다.

**단, 이 낮은 SI 비율을 "메모리가 깨끗하다" 로 읽지 마라.** 이번 축이 재는 것은
근거의 **존재**이지 **타당성**이 아니다. 위 불일치 ② 가 보여주듯, 근거처럼 보이는 서술이
실제로는 다른 엔트리에서 빌려온 것일 수 있다. 그런 엔트리는 EE/MX 로 태깅되지만
실질 검증 강도는 SI 에 가깝다.

---

## 5. 소비면이 알아야 할 한계

- **정확도 90% 는 표본 20 건 기준이다.** 95% 신뢰구간은 대략 68–99% 로 넓다.
  나머지 84 건에 8~10 건 규모의 오라벨이 남아 있을 수 있다.
- **`grounding` 부재와 SI 는 다르다.** 현재 미보유는 0 건이나, 새 엔트리가 추가되면
  다시 생긴다. 소비면은 «필드 없음» 을 SI 로 자동 강등하지 말고 «미태깅» 으로 다뤄라.
- **EE 안에도 강도 편차가 크다.** QA REJECT · 명령 출력 인용이 있는 건과,
  외부 문서 리서치만 있는 건(`feedback_worker_nplus1_tx_boundary` 는 Postgres 공식 문서
  근거뿐)이 같은 라벨을 단다. 강도 축이 필요하면 이번 축 위에 별도로 얹어야 한다.

---

## 6. 실행 명령 요약

```bash
# 대상 열거 + 재계수
find ~/.claude/projects -maxdepth 3 -path '*/memory/*.md' ! -name 'MEMORY.md' \
  | while read f; do grep -q '^  type: feedback' "$f" && echo "$f"; done | sort > recount.txt
wc -l < recount.txt                      # 104
sed 's|.*/projects/||; s|/memory/.*||' recount.txt | sort -u | wc -l   # 6

# 미보유 0 건 검증 (SK-03)
grep -LF 'grounding:' $(cat recount.txt) | wc -l    # 0

# 정의 1 파일 검증 (SK-02)
grep -rl 'user_' --include='*.md' --exclude-dir=.git . | grep -v '^./.harness/'
```
