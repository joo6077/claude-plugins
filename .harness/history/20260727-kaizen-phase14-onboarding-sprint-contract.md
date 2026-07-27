---
feature: "kaizen 2026-07-27 Phase 14 — onboarding-kit"
created: "2026-07-27"
iteration: 1
contract_root: "/Users/jackson/Hub/10_Dev/claude-plugins"
---

# Sprint Contract — Phase 14 (onboarding-kit)

## 배경 / 데이터 소스

- `.claude/kaizen-input/insights-report.md` §0 — Friction #2 (증거 없는 완료 주장) ·
  Friction #3 (**존재하지 않는 FCM credentials 파일명 날조** — 이 킷 도메인 직결) ·
  Phase 적용 힌트 "Phase 13 Bambu / 14 Onboarding: 경로·파일명·콘솔 UI 날조 금지"
- `.claude/kaizen-input/reflect-digest-2026-07-27.md` — claude-plugins reflection 0 건,
  onboarding/setup-guide 태그 0 건 (LOW signal 확인)
- `.harness/.meta/kaizen-data-pool.md` §5 — onboarding-kit V1~V8 전부 OK (baseline clean)
- 사용자 메모리 3 건 — `feedback_setup_guide_stack_first` · `_console_ui_fetch` · `_site_distinction`
- Phase 1 `skill-design-guide` v1.4.0 §3.7 Completion Evidence Gate + Enforcement E1/E2/E3 (SSOT)
- Phase 3 `qa-evaluation-guide` v4.0 §Canonical Unverified-Evidence Protocol (`[미검증]` · 임계 2)
- 리서치 5 건 (2026-07-27 조회) — 아래 RF 조건의 근거

## 신호 등급

LOW. 직전 사이클(phase13)에 setup-guide 스코프 가드가 이미 승격됐으므로 **같은 문장 재추가 금지**.
이번 Phase 는 **새 규칙 추가가 아니라 enforcement 등급 상향 + 실측 정정**에 국한한다.

## 범위

수정 가능: `onboarding-kit/skills/setup-guide/SKILL.md` ·
`onboarding-kit/skills/setup-guide/references/*` (3 종) ·
`onboarding-kit/skills/setup-guide/evals/evals.json` · `.claude/skills/onboarding-kaizen/SKILL.md`

금지: 타 kit · `harness/` · `.claude/skills/kaizen-orchestrator/` · `scripts/` · marketplace.json ·
plugin.json · `docs/kaizen/changelog.md` · 사용자 메모리 파일 · git 쓰기 계열 명령 전부

## 완료 조건

### MF — 메모리 피드백 3 건 반영 전수 확인 (회귀 가드)

- [ ] MF-01 [exact, enumerated]: SKILL.md 에 stack-first (Gotcha 1) · console-ui-fetch (Gotcha 2) ·
  apple-site-distinction (Gotcha 3) 3 건이 모두 잔존한다. 이번 변경으로 어느 것도 약화되지 않는다.
- [ ] MF-02 [exact]: `evals.json` 이 위 3 원칙과 **모순되는 assertion 을 0 건** 보유한다
      (현재 `flutter-fcm-ios` 가 Flutter 가이드에 네이티브 Swift API 를 요구하여 Gotcha 1 과 충돌).

### NI — Never Invent Paths (Friction #3 · E1 → E2 승급)

- [ ] NI-01 [exact]: SKILL.md 에 프로젝트 내부 **경로·파일명·env 키 날조 금지** Gotcha 가 신설되고,
  Glob/Grep 실측 → `파일:라인` 열거를 **아티팩트(E2)** 로 요구한다. 근거로 §0 Friction #3 실측 사례를 인용한다.
- [ ] NI-02 [exact]: 확인 실패 시 처리가 "추측해서 쓴다" 가 아니라 "새로 만든다 명시 또는 사용자에게 묻는다"
  로 규정된다. 이름을 가정한 Glob 금지(패턴 탐색) 가 명시된다.

### SL — Source Ledger (Friction #2 · E1 → E2 승급)

- [ ] SL-01 [exact]: SKILL.md 에 "각 Step 은 조회한 1차 출처 URL + 조회일을 본문에 남긴다 ·
  fetch 하지 않은 Step 은 쓰지 않는다" 가 아티팩트 요구로 존재한다.
- [ ] SL-02 [exact]: `format-checklist.md` §3 Step 템플릿에 `**출처:**` 줄이 추가된다.
  **11 개 섹션 개수는 불변**(12 번째 섹션 신설 금지).
- [ ] SL-03 [exact]: `[미검증]` 마커와 **임계 2** 가 도입되고, 정본 앵커
  (`harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol) 를 인용한다.
  킷 내 재정의·동의어 신설 0 건.
- [ ] SL-04 [exact]: `search-strategy.md` 에 fetch 실패 시 fallback 사다리와 최종 `[미검증]` 처리가 추가된다.

### RF — 리서치 실측 반영 (출처 인용 필수)

- [ ] RF-01 [exact]: `search-strategy.md` Stripe 출처가 `docs.stripe.com` 으로 정정되고,
  **문서 호스트 이전 + WebFetch 크로스호스트 리다이렉트 미추적** 주의가 명시된다.
- [ ] RF-02 [exact]: Apple 하위 경로가 실측 섹션명으로 갱신된다
  (Certificates / Keys / Identifiers / Capabilities / Services / Service Configurations /
  Devices / Provisioning Profiles).
- [ ] RF-03 [exact]: `format-checklist.md` 의 Firebase 콘솔 클릭 경로 예시가 실측 경로
  (Settings > General → Cloud Messaging tab → iOS app configuration) 로 정정된다.
- [ ] RF-04 [exact]: 패키지 버전 확인은 GitHub Releases 대신 **패키지 레지스트리 우선** 규칙이
  `search-strategy.md` 에 추가된다 (실측 근거: FlutterFire Releases fetch 가 2020 프리릴리스만 반환).

### EV — evals 결함 수정

- [ ] EV-01 [exact]: `flutter-fcm-ios` 의 `FirebaseApp.configure()` assertion 이 Flutter 실측 API
  (`Firebase.initializeApp` + `DefaultFirebaseOptions.currentPlatform`) 로 교체되고,
  AppDelegate 네이티브 호출 요구 금지 negative assertion 이 추가된다.
- [ ] EV-02 [exact]: `deprecated-api-warning` 케이스가 "1 차 출처에 없는 deprecation 을 날조하지 않는다"
  를 함께 검증한다 (실측: FCM Apple 문서는 `.p12` 를 deprecated 로 표기하지 않고 `.p8` 을 권장만 한다).
- [ ] EV-03 [structural]: 경로 날조 금지 · 출처 원장 각 1 건씩 신규 케이스가 추가되고 evals version 이 bump 된다.

### KZ — onboarding-kaizen 정합화

- [ ] KZ-01 [exact]: `.claude/skills/onboarding-kaizen/SKILL.md` 에 validate-plugin
  **8 카테고리 (V1~V8)** 게이트가 추가되고 `harness/docs/guides/plugin-validation-guide.md §7` 를
  SSOT 로 인용한다 (sibling parity — 9 개 kaizen 스킬 중 7 개가 이미 보유).

### RG — Regression

- [ ] RG-01 [exact]: `python3 scripts/validate-plugin.py onboarding-kit` → V1~V8 전부 OK, Exit 0.
- [ ] RG-02 [exact]: `git diff --name-only` 결과가 범위 내 5 파일 + 본 계약 파일로만 구성된다.
- [ ] RG-03 [exact]: 백틱 없는 `TBD`/`TODO`/`FIXME` 0 건, bare code fence 0 건 (V5/V6 가드).

## 비범위 (명시적 제외)

- `docs/kaizen/research-log.md` 기록 — 오케스트레이터 소관, 본 Phase 는 리포트로만 전달
- `.claude/skills/onboarding-kaizen/references/research-sources.md` — 범위 목록 미포함, 후속 권고로만 보고
- `.claude/skills/kaizen-orchestrator/` 의 Phase 13/14 번호 drift · research-sources 경로 drift — 보고만
