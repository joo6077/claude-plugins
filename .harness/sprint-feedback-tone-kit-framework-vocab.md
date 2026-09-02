# Sprint Feedback
Feature: tone-kit 프레임워크 어휘 우선 규칙 (framework-vocab amendment)
Evaluated: 2026-09-02 15:20
Verdict: APPROVE
Iteration: 4

## Contract Fingerprint
- path: .harness/sprint-amendments-tone-kit-framework-vocab.md
- sha256: 5924e7bc9be776fbc72c5c054bf7b5d3a8cf0320eda776019d1eada07b32586e
- status: <none:no-frontmatter>
- slug: tone-kit-framework-vocab
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: 명시 경로 (사용자가 이 iteration 의 평가 대상으로 직접 지정. 표준 ladder 의 `sprint-contract*.md` 패턴과 파일명이 다름 — 아래 계약 스키마 편차 참조)
- legacy_contract_used: false
- seal_status: unavailable (이 파일은 봉인 마커를 쓰지 않는 pre-seal 계약 — 경고, 차단 아님)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (sha256 동일, 평가 시작~종료 간 TOCTOU 없음)
- status_transition: skipped (frontmatter status 필드 없음 — 전환 대상 아님)

### 계약 스키마 편차 (경고, FAIL 아님)
이 파일은 `sprint-amendments-<slug>.md` 명명 규약을 쓰지만 실질적으로는 base(50)+prior-amendment(25)에
20개 조건을 추가하는 **독립 평가 대상 계약**으로 4회 연속 사용되고 있다. frontmatter(`status`/`owner_session`/
`conditions: 20`)가 없어 표준 ladder(Step 1-c)로는 자동 탐지되지 않는다. 사용자가 매 iteration 명시 경로로
지정해왔기 때문에 지금까지는 문제가 없었지만, `sprint-contract-tone-kit-framework-vocab.md` 로 정식 승격하고
frontmatter(`status: active`, `conditions: 20`)를 붙이는 것을 권장한다 (Improvement 참조).

## Amendments
- amendments: 0 (이 파일 자체가 이번 iteration 의 평가 대상 계약이며, 이 계약의 조건을 수정하는 별도 사이드카는 없음)

## User Correction Audit
- correction_log_status: unavailable (reflect-kit 로그 버킷 탐색 결과 이 프로젝트 대응 디렉토리 없음 — read-union glob 0건)
- unreflected_corrections: 0
- verdict 영향: 없음

## Results

### FV — 프레임워크 어휘 (9/9)
- [x] FV-01: `core-naming.md` 에 코어 원칙 N-12 존재 — 강도 SHOULD, 축 어휘 — PASS
  - 근거: `tone-kit/references/core-naming.md:41` `| N-12 | 이벤트·상태 어휘는 프레임워크가 이미 정의했으면 그것을 따른다 — 새로 만들지 않는다 | SHOULD | 어휘 |`
- [x] FV-02: 우선순위가 `프레임워크 공식 어휘 > 프로젝트 관례 > 새로 만든 말` 로 명시 — PASS
  - 근거: `tone-kit/references/core-naming.md:146` (§6 프레임워크 어휘 우선, 우선순위 코드블록) 문구 일치
- [x] FV-03: 이름 결정 절차에 "프레임워크가 이미 이름을 정했는가" 선행 단계 존재 — PASS
  - 근거: `tone-kit/references/core-naming.md:196` `**0단계 — 프레임워크가 이미 이름을 정했는가?** 정했으면 그것을 쓰고 아래 절차를 건너뛴다 (N-12).`
- [x] FV-04: `adapter-dart-flutter.md` 에 D-15 + 슬롯 `event_vocabulary` + 제스처 어휘 절 존재 — PASS
  - 근거: `tone-kit/references/adapter-dart-flutter.md:28`(슬롯 `event_vocabulary`) · `:51`(D-15 규칙표) · `:170`(### 3.11 이벤트 콜백 어휘 (D-15))
- [x] FV-05: 제스처 콜백 표가 SDK 실측 근거(`gesture_detector.dart` 3.38.4)와 함께 실림. 단계 축 `Down → Start → Update/MoveUpdate → End/Up → Cancel` 명시 — PASS
  - 근거: `tone-kit/references/adapter-dart-flutter.md:174-178`(단계 축) · `:180`(콜백 58개, SDK 3.38.4). 재현 명령을 로컬 Flutter SDK(`~/fvm/versions/3.38.4/packages/flutter/lib/src/widgets/gesture_detector.dart`)에 실제 실행: `grep -v '^\s*///' ... | sort -u | wc -l` → **58** (문서 primary 수치와 일치)
  - 계약 편차 주석: 이 조건의 계약 원문(`.harness/sprint-amendments-tone-kit-framework-vocab.md:33`)은 괄호 안 수치를 "59개"로 적고 있으나, 이는 iteration 1 작성 당시의 미정제 수치로 보인다. 사용자가 이번 iteration 재평가 지시에서 명시적으로 "재현 명령을 그대로 실행해 58이 나오는가"를 검증 기준으로 재확인했고, 문서·SDK 실측·사용자 지시 3자가 일치하므로 58을 1차 수치로 판정했다. 상세는 Improvement 참조
- [x] FV-09: 59 라는 수의 세는 기준과 재현 명령이 문서에 실림. 제스처 접두사 없는 내부 recognizer 콜백 8종 제외 사실 명시 — PASS
  - 근거: `tone-kit/references/adapter-dart-flutter.md:182`(세는 기준 산문 + 재현 명령 코드블록 184-188) · `:190`(`grep -v` 누락 시 59, 차이 1건은 `onForcePress`) · `:192`(8종 제외 목록 명시, 8종+59=67 서술)
  - 재현 검증: 주석 포함 시 wc -l → **59**(diff 확인 결과 차이는 정확히 `onForcePress` 1건, 문서 서술과 일치) / 8종(`onDown`·`onStart`·`onUpdate`·`onEnd`·`onCancel`·`onPeak`·`onPointerDown`·`onPointerPanZoomStart`) 유니온 후 → **67** (문서 서술과 일치)
- [x] FV-06: `dart-typedef.md` 에서 킷 발명 접미사 집합(Changed·Tap·Blur·Submit 나열)이 프레임워크 어휘 우선으로 교체됨 — PASS
  - 근거: `tone-kit/templates/dart-typedef.md:27` "이벤트 형태는 새로 만들지 말고 프레임워크 어휘를 쓴다..." — 4종 나열 소멸, §3.11 참조로 대체. 전체 파일에 `Changed`·`Tap`·`Blur`·`Submit` 4종 나열형 0건 (Grep 확인)
- [x] FV-07: 도메인 이벤트 예외 명시 — 공식 대응 없으면 프로젝트가 명명. 판정식이 "프레임워크가 이미 아는 이벤트인가" — PASS
  - 근거: `tone-kit/references/adapter-dart-flutter.md:231` `**예외** — ... 판정식은 "이 이벤트를 프레임워크가 이미 알고 있는가" 다.` / `tone-kit/references/core-naming.md:182` 적용 범위 절
- [x] FV-08: 강도가 MUST 로 승격되지 않음 — SHOULD 가 상한 — PASS
  - 근거: `tone-kit/references/core-naming.md:41,139` N-12 강도 `SHOULD` 명시, MUST 문자열 이 규칙 문맥에 없음 (Grep 확인)

### FC — 정합 (4/4)
- [x] FC-01: 운영 문서(references/)와 근거 문서(docs/tone/)가 같은 규칙을 말함 — PASS
  - 근거: `docs/tone/templates.md:143` ↔ `docs/tone-kit/templates.html:540` `{Event}` 설명 문구 완전 일치(`onChanged`·`onTapDown`·`onLongPressStart`·`onSubmitted`, N-12·D-15 인용) — Iteration 3 FAIL 재현 안 됨
  - 전수 스윕: `grep -rn "Blur" tone-kit/ docs/tone/ docs/tone-kit/` → 0건. `Changed…Tap…(Blur|Submit)` 나열형 패턴 → 0건. (git HEAD 버전에서는 동일 패턴이 매치되어 grep 자체의 유효성 확인됨 — 공허한 0 아님)
- [x] FC-02: 어댑터 슬롯 표가 references ↔ docs/tone/dart-flutter-idioms.md 양쪽 일치 (event_vocabulary 포함) — PASS
  - 근거: `naming_suffix`·`event_vocabulary` 두 슬롯 행 모두 `tone-kit/references/adapter-dart-flutter.md:27-28` ↔ `docs/tone/dart-flutter-idioms.md:634-635` 문자 단위 대조 완료(내용 일치, 표현만 references가 terse·docs가 확장형인 기존 패턴 유지)
- [x] FC-03: naming-taxonomy 의 "taxonomy 는 업계 표준이 아니다" 경고와 모순 없음 — 컴포넌트 접미사(합성)와 이벤트 어휘(프레임워크가 정함)를 구분해 설명 — PASS
  - 근거: `docs/tone/naming-taxonomy.md:27` "합성이 필요한 자리와 그렇지 않은 자리는 다르다. 컴포넌트 접미사(...)는 단일 권위가 없어서... 합성했다. 반면 이벤트 콜백 어휘는 프레임워크가 이미 정해 뒀다 — 합성할 자리가 아니다." / `:437` 기존 "업계 표준 아니다" 경고문 그대로 보존 (삭제 없음)
- [x] FC-04: HTML 2페이지가 갱신된 md 를 반영 (제스처 표 실림) — PASS
  - 근거: `docs/tone-kit/dart-flutter-idioms.html:1134-1246` 제스처별 공식 콜백 표 + `58개(3.38.4)` source-badge 존재. `docs/tone-kit/naming-taxonomy.html:592` N-12/D-15/event_vocabulary 인용 확인. 두 HTML 모두 div 태그 밸런스 정상(balanced=True, python re 카운트)

### ER3 — 게이트 (7/7)
- [x] ER3-01: `validate-plugin.py` 12 plugins 12 OK · exit 0 — PASS
  - 근거: 직접 실행 출력 `Total: 12 plugins, 12 OK / Exit: 0` (tone-kit 포함 전 항목 OK)
- [x] ER3-02: `run-evals.py` 전체 PASS — PASS
  - 근거: 직접 실행 출력 `Total: 106 passed, 0 failed`, exit 0
- [x] ER3-03: `sync-docs` · `sync-orchestrator` drift 0 — PASS
  - 근거: `sync-docs.py --check-only` → "모든 README가 동기화 상태입니다" exit 0 / `sync-orchestrator.py --check-only` → "이미 동기화됨 (11 plugins)" exit 0
- [x] ER3-04: TODO/TBD/FIXME 0건 · 언어 없는 코드펜스 0건 — PASS
  - 근거: 변경 파일(git diff --name-only) 전수 grep `TODO|TBD|FIXME` → 0건. 코드펜스는 단순 `^```$` grep이 닫는 펜스까지 오매칭하는 문제가 있어, 여는/닫는 펜스를 depth 추적으로 정확히 분리하는 python 검사로 재검증 → bare opening fence 0건 (validate-plugin V6 tone-kit "0 bare — OK" 결과와 일치)
- [x] ER3-05: 프로젝트 고유 식별자 0건 — PASS
  - 근거: 변경 파일 전수 `grep -niE "app_kiosk|Adm[A-Z]|claude-plugins|jackson"` → 0건 (Iteration 3 feedback에서 확립된 동일 패턴 재사용)
- [x] ER3-06: 타 킷 디렉토리 수정 0건 — PASS
  - 근거: `git status --porcelain` 전수 확인 — 수정분은 `docs/tone/` · `docs/tone-kit/` · `tone-kit/` · `.gitignore` 뿐. flutter-toolkit/design-kit/backend-kit/infra-kit/rust-kit/react-kit/planning-kit/reflect-kit/bambu-kit/onboarding-kit 미터치. (평가 도중 `.playwright-mcp/*`·`v1-light.png` 신규 untracked 파일이 관찰됐으나 킷 디렉토리 밖 루트 아티팩트이고 이번 계약의 평가 대상 파일도 아님 — ER3-06 판정에 영향 없음. 병렬 작업 흔적으로 추정, 참고 기록만 남김)
- [x] ER3-07: 기존 출처·강도 라벨 삭제 0건 + 강도 분포 카드 수치 일치 — PASS
  - 근거(수치): `docs/tone-kit/dart-flutter-idioms.html:1429-1433` 강도 분포 카드 `0/15`·`7/15`·`8/15`. adapter-dart-flutter.md D-01~D-15 15개 규칙 직접 카운트 → MUST=0, SHOULD=7(D-01·02·07·09·12·13·15), 관측컨벤션=8(D-03·04·05·06·08·10·11·14) — 카드 수치와 정확히 일치
  - 근거(CSS): `.dist`·`.dist-row`·`.dist-label`·`.dist-track`·`.dist-fill`·`.dist-val` 전부 같은 파일 219-226행에 정의됨
  - 근거(삭제 없음): 6개 md 소스 파일 + 2개 HTML 전수 대상 `git diff` 로 `강도[:：·]|출처[:：]` 삭제 라인 검색 → 0건. `https://` URL 대조(HEAD vs working tree) → 6개 md + 2개 html 전부 URL 집합 완전 동일(diff 0줄)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 — 이 20개 조건은 전부 문서 내용 일치·수치 재현·게이트 스크립트 실행 판정이며, 규칙 12의 9개 카테고리(동시성 가드/인증/멱등성/입력검증/데이터유실/마이그레이션/재시도·중복제거/보안경계/사용자보고-테스트충돌)에 해당하지 않음

## User-Reported Failures
- 해당 없음 (이번 iteration에 새로 보고된 사용자 실패 없음, FC-01은 Iteration 3의 자체 QA FAIL이었고 REOPENED 대상 아님)

## Evidence Validity
- 검사 대상 증거: 20건 (조건별 1건)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 실행 6건(FV-05/FV-09 SDK 재현 명령 3종 실제 실행, ER3-01~05 게이트 스크립트 5종 실제 실행) · zsh/bash 양쪽 확인: bash 로 통일 실행(이 세션 셸이 bash 서브프로세스로 구동됨, Bash 도구 특성상 zsh 별도 재실행은 생략 — 대상 스니펫이 플랫폼 의존 glob 을 쓰지 않아 리스크 낮음) · 미실행 0건
- 무효 0건 → 미검증 카운터 합산 없음

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (20 - 0) / 20 = 1.00 (임계 0.60 충족)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (전 조건 직접 검증 완료)

## Summary
- Total: 20/20 conditions passed
- Verdict: APPROVE
- Iteration 3 FAIL(FC-01)이 완전히 수정됐고, 요청받은 "전파 완전성" 전수 재점검(운영문서 ↔ 근거문서, 근거문서 ↔ HTML 2종, Blur/구접미사 전체 스윕, 강도·출처 라벨 삭제 여부, URL 보존)에서 새로운 누락·회귀 0건 확인. FV-05/FV-09의 SDK 실측 수치(58/59/67)는 로컬 Flutter 3.38.4 SDK 소스에 대해 문서의 재현 명령을 직접 실행해 3개 수치 모두 정확히 재현됨.

## Improvement Suggestions
- [FV-05] 측정-상태-모호 — 계약 원문(`.harness/sprint-amendments-tone-kit-framework-vocab.md:33`)의 "제스처 접두 고유 콜백 59개"를 "58개(주석 제외 1차 수치 — grep -v '^\s*///' 필수. 주석 포함 시 59, 그 중 1건은 `onForcePress`)"로 갱신해 조건 문구와 실제 올바른 수치를 일치시킬 것. 이번 iteration은 사용자의 실시간 지시(58 검증)와 SDK 실측이 일치해 PASS 처리했으나, 계약 원문의 stale 수치가 다음 evaluator에게 반복적으로 같은 판단 부담을 지운다
- [계약 스키마] 검증경로-미기재 — `sprint-amendments-tone-kit-framework-vocab.md`가 4 iteration 연속 독립 평가 대상으로 쓰이고 있음에도 `sprint-contract-*.md` 명명 규약과 frontmatter(`status`/`slug`/`conditions`)가 없어 표준 ladder(Step 1-c)로 자동 탐지되지 않는다. `sprint-contract-tone-kit-framework-vocab.md`로 정식 승격하거나, 최소한 frontmatter(`status: active`→APPROVE 후 `done`, `conditions: 20`)를 추가할 것을 권장
- [일반] Iteration 1~3의 REJECT 판정이 `.harness/`에 별도 sprint-feedback 파일로 영속화되지 않아 이번 evaluator가 과거 판정 근거를 직접 대조할 수 없었다(사용자 서술에만 의존). 다음부터는 REJECT 시에도 Step 5 산출물을 남겨 iteration 간 근거 연속성을 확보할 것
