---
feature: "카이젠 Phase 5 — flutter-toolkit 버전 사실 정정 + Primitive Substitution Gate(G1) · invalidate 경계(G2) · 위젯 테스트 하네스(G3) · 성능 환경 배제(G4)"
created: "2026-08-13 14:10"
complexity: "복잡"
conditions: 23
slug: kaizen-phase5-flutter-gates
status: active
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
conditions_digest: sha256:5853e8a469993a57
locked_at: "2026-08-13 14:10"
---

## 배경

`.harness/.meta/evidence/phase5.md` 가 이번 Phase 의 **유일한 외부 근거**다. 외부 조회 0 회.

evidence 가 지적한 것은 두 층이다.

**(1) 사실 오류.** 우리 스킬 6 표면 + 리서치 로그 4 줄이 "Freezed 3 부터 `.when`/`.map` 제거" 를
**절대 규칙**으로 단정한다. evidence 기준 이것은 거짓이다 — 제거는 3.0 의 breaking 이었고
**3.1.0 에서 `when`/`map` 이 다시 추가됐다** (최신 stable 3.2.5). 같은 유형으로 Flutter stable
버전(로컬 3.44 vs 릴리스 인덱스 최상단 3.47.0)과 Impeller 플랫폼 상태(로컬 "macOS 실험적 ·
Web/Windows/Linux 미지원" vs 3.47 부터 macOS/Linux/Windows 기본)가 낡았다.

**(2) 실측 REJECT 4 종에 대응하는 게이트 부재.** 2026-08-12 fit-pal 피드백:

- `RE-02` — "B5 구분선이 Flutter 기본 `Divider` 사용, 기존 `IFDivider` 컴포넌트 미재사용" → G1
- `LG-02` — "`groupDetailDataProvider` 가 팔레트 색상 변경 시 invalidate 되지 않아 캐시된 이전 색을
  계속 표시" (`group_preferences_body.dart:63-88` invalidate 누락) → G2
- `LG-01` / `LG-02` improvement — "16종 매핑 단위 테스트 커버리지 부족 (2종만 검증)",
  "GroupDetailPage 위젯 테스트 하네스 신설 후 … 반영 확인 테스트 추가 권장" → G3
- `/insights` D5 — 18 일 누수된 시뮬레이터 render host 가 swap 포화를 유발한 것을 앱 코드 최적화
  **전에** 규명한 성공 사례. 이 절차가 스킬에 없다 → G4

**enforcement 프레이밍.** G1 은 기존 E1 조항(`flutter-widget` §Enumerate-before-Act)이 있는데도
재발했다. 문장을 또 추가하지 않고 **E2 로 승급**한다 — 대체 후보 표(아티팩트)를 남기게 하고,
규칙 정의는 4 표면에 복제하지 않고 references SSOT 1 곳에 둔다. 나머지 G2~G4 는 직전 사이클
흡수분 표에 없는 **신규 신호**라 신설이 맞다.

## 리서치 소스 (evidence 파일 한정 — 외부 조회 0 회)

- `.harness/.meta/evidence/phase5.md` §1~§4 — G1~G4 관찰 사실 · 권장 문구 · **넣지 말 것** 목록 ·
  트레이드오프 · 열린 질문(버전 가드 필요성 포함). 인용 URL 9 종:
  `flutter/agent-plugins` · `riverpod.dev/docs/concepts2/refs` ·
  `riverpod.dev/docs/concepts2/auto_dispose` · `pub.dev/packages/flutter_riverpod/changelog` ·
  `riverpod.dev/docs/how_to/testing` · `docs.flutter.dev/perf/ui-performance` ·
  `docs.flutter.dev/testing/build-modes` · `docs.flutter.dev/perf/impeller` ·
  `docs.flutter.dev/release/release-notes` · `flutter.dev/blog/whats-new-in-flutter-3-47` ·
  `pub.dev/packages/freezed/changelog`
- `.harness/.meta/kaizen-data-pool.md` §1 — REJECT Top 20 의 `RE-02` · `LG-02` · `LG-01`,
  Improvement Top 15 의 "[LG-02] 측정-수단-미이행 … 위젯 테스트 하네스 신설"
- `.claude/kaizen-input/insights-report.md` — 직전 사이클 흡수분 표(재승격 금지) · 신규 델타 D5
  (Phase 5 직접 신호) · D3(사용자 관측 우선순위, Phase 3 정본의 kit 소비면)
- Phase 1 산출물 `harness/docs/guides/skill-design-guide.md` — §3.7 Enforcement 3 등급 + 등급 원장,
  §3.8 User-Reported Failure Gate, §5.5 Enumerate-before-Act
- Phase 3 산출물 `harness/docs/guides/qa-evaluation-guide.md` — §Canonical User-Reported Failure
  Protocol (kit reviewer 복제용 정본)
- `harness/references/contract-schema.md` v5.3 — 본 계약의 포맷 SSOT

## GAP 분석 (전부 실측 · 명령 출력 기준)

| # | 갭 | 실측 근거 (사전 측정) | 처리 |
| --- | --- | --- | --- |
| F1 | Freezed `when`/`map` 절대 제거 단정 | 10 줄 (아래 SK-01 오라클 사전 출력) | 전 표면 정정 |
| F2 | 3.44 를 현재 stable 로 단정 | 3 줄 (ER-02 오라클 사전 출력) | 3.47.0 로 정정 |
| F3 | Impeller 플랫폼 상태 낡음 | 5 줄 (ER-01 오라클 사전 출력) | 3.47 desktop 기본 반영 |
| G1 | DS 컴포넌트 대체 게이트 부재 | `flutter-screen` 템플릿이 `Scaffold/AppBar/Text` 직접 생성 · `Divider` 등 기본 위젯 사용 전 DS 검색 강제 0 건 | references SSOT + 4 표면 참조 (E2) |
| G2 | invalidate 경계 체크리스트 부재 | `flutter-provider` 에 `invalidate` 문자열 0 건 (`state-management.md` 에만 3 줄) | 파생 watch 연결 + mutation 후 영향 provider 열거 |
| G3 | widget test 하네스·coverage 조항 부재 | `tester.container()` 전 레포 0 건 · coverage 상한 조항 0 건 | 하네스 기본형 + 전수 매핑 조항 |
| G4 | 성능 환경 배제 절차 부재 | `performance.md` 에 physical device / simulator 배제 0 건 | Environment Exclusion Checklist 8 항 |
| D3 | 사용자 관측 우선순위의 kit 소비면 없음 | `flutter-audit` 이 Unverified-Evidence 정본만 인용 | User-Reported Failure 정본 인용 1 줄 |

## 범위 경계

**구현 변경 경로 17 개.** 목록은 AR-01 의 기대 집합 한 곳에서만 열거한다
(§측정 커버리지 표기의 화이트리스트 규칙). 계약 파일 자신과 `.harness/**` 는 AR-01 pathspec 에서
제외한다.

- **건드리지 않는다**: `flutter-toolkit/README.md` · `flutter-toolkit/.claude-plugin/` ·
  `flutter-toolkit/evals/` · 다른 킷 전부. Phase 5 Scope 밖이다.
- **버전 번호를 지어내지 않는다.** evidence 에 없는 릴리스 번호·수치를 새로 쓰지 않는다 (AP-01).

## 회귀 게이트

- 정정 항목은 "새 서술 추가" 가 아니라 **잔존 0 건 증명**으로 판정한다.
- 모든 오라클은 zsh · bash 양쪽에서 실행하고 출력이 같아야 한다 (DG-04).
- grep 오라클은 substring 오탐을 확인한다 — `pre-stable` 이 `stable` 에 걸리는 사례를 사전 확인했고,
  그래서 F2 오라클을 exact 문자열 집합으로 바꿨다.

## Skill

- [ ] SK-01: Freezed `.when`/`.map` 을 "제거됐다" 로 단정하고 3.1.0 재추가를 밝히지 않는 줄이
      `flutter-toolkit/` · `docs/flutter/` 전체에서 0 건이다 [exact]
      (측정: `grep -rn 'when' flutter-toolkit docs/flutter | grep -E 'map' | grep -E '제거|removed' | grep -v '3\.1\.0' | wc -l` → `0` ·
       사전 출력 `10` 이 discriminating 근거 ·
       음성 대조: 정정 문장에서 `3.1.0` 토큰을 지우면 이 측정이 FAIL 해야 한다)
- [ ] SK-02: Primitive Substitution Gate 규칙 본문이 `flutter-toolkit/references/primitive-substitution-gate.md`
      1 개 파일에만 존재하고, 4 소비 표면이 각각 그 경로를 인용한다 [exact, enumerated]
      (측정: 인용 표면 집합이 `flutter-toolkit/skills/flutter-widget/SKILL.md`,
       `flutter-toolkit/skills/flutter-screen/SKILL.md`,
       `flutter-toolkit/skills/flutter-audit/SKILL.md`,
       `flutter-toolkit/agents/widget-inspector.md` 4 개와 정확히 일치 —
       `grep -rln 'primitive-substitution-gate' flutter-toolkit | LC_ALL=C sort`)
- [ ] SK-03: 그 SSOT 가 감사 대상 위젯 목록과 **면제되는 layout primitive 목록**을 둘 다 명시한다 [exact]
      (측정: 파일에 `Divider` `Button` `Chip` `Card` `ListTile` `Switch` `TextField`
       `CircularProgressIndicator` 8 종과 `Text` `Row` `Column` `Padding` `SizedBox` 5 종이 모두 등장 ·
       면제 목록에는 "금지하지 않는다" 취지 문구가 붙는다)
- [ ] SK-04: `flutter-provider/SKILL.md` 에 (a) 파생 provider 를 `ref.watch(...select(...))` 로
      선언형 연결하라는 조항과 (b) mutation 후 영향 provider 를 열거해 `ref.invalidate` 하라는
      조항이 각각 존재한다 [structural]
      (측정: `grep -c 'select(' `, `grep -c 'ref.invalidate'` 각각 1 이상 + 본문 Read 확인)
- [ ] SK-05: `onManualInvalidation` 을 언급하는 모든 줄에 **버전 가드**(`3.4` 문자열)가 함께 있다 [exact]
      (측정: `grep -rn 'onManualInvalidation' flutter-toolkit docs/flutter | grep -v '3\.4' | wc -l` → `0` ·
       음성 대조: 가드 문자열을 지우면 FAIL)
- [ ] SK-06: Riverpod widget test 하네스 기본형(`ProviderScope` 루트 + `tester.container()`)이
      `flutter-toolkit/skills/flutter-test/SKILL.md` 와 `docs/flutter/quality/testing.md`
      2 개 파일에 모두 존재한다 [exact, enumerated]
      (측정: `grep -rln 'tester.container()' flutter-toolkit/skills/flutter-test/SKILL.md docs/flutter/quality/testing.md`
       결과가 그 2 행과 정확히 일치)
- [ ] SK-07: "N 종 매핑에서 대표 2 종만 검증 금지" 취지의 coverage 조항이 `flutter-test` 에 존재하고,
      실측 REJECT 수치(16 종 / 2 종)를 근거로 인용한다 [exact]
      (측정: `grep -n '16' flutter-toolkit/skills/flutter-test/SKILL.md` 에서 해당 줄 확인)
- [ ] SK-08: Environment Exclusion Checklist 8 항목이 `flutter-toolkit/skills/flutter-audit/SKILL.md`
      와 `docs/flutter/quality/performance.md` 양쪽에 존재한다 [exact, enumerated]
      (항목: `profile mode` · `physical device` · `simulator/emulator` · `swap` · `DevTools trace` ·
       `Impeller` · `refresh rate` · `slowest target device` ·
       측정: 두 파일 각각에서 8 토큰 전부 매치 — 누락 토큰 0)
- [ ] SK-09: "simulator/emulator/debug 결과만 있으면 앱 코드 병목으로 확정하지 말고 `[미검증]`"
      판정 규칙이 위 두 파일에 존재한다 [structural]
- [ ] SK-10: `flutter-audit` 이 Phase 3 정본 `harness/docs/guides/qa-evaluation-guide.md`
      §Canonical User-Reported Failure Protocol 을 **인용만** 하고 임계값·상태어를 재정의하지 않는다 [exact]
      (측정: 인용 1 건 존재 + 같은 파일에 `REOPENED` 정의문 0 건)

## Error

- [ ] ER-01: Impeller 플랫폼 상태의 낡은 단정이 0 건이다 [exact]
      (측정: `grep -rn -e '--enable-impeller' -e 'Web/Windows/Linux 미지원' -e 'Web/Windows/Linux: 미지원' -e 'macOS: opt-in' -e 'macOS 실험적' -e 'Android opt-in' -e 'Flutter 3.16+에서 기본 활성화' flutter-toolkit docs/flutter | grep -v '정정 2026-08-13' | wc -l` → `0` ·
       사전 출력 `5` 가 discriminating 근거)
- [ ] ER-02: Flutter 3.44 를 현재 stable 로 단정하는 줄이 0 건이다 [exact]
      (측정: `grep -rn '2026-07 stable\|2026-07 기준 stable\|stable \*\*3\.44\.7\*\*\|stable = 3\.44\.7' flutter-toolkit docs/flutter | grep -v '정정 2026-08-13' | wc -l` → `0` ·
       사전 출력 `3` · substring 오탐 확인 완료: 이 패턴은 `pre-stable` 을 잡지 않는다)
- [ ] ER-03: evidence 의 **넣지 말 것** 3 종이 금지 조항으로 명문화된다 [exact, enumerated]
      (대상: `모든 기본 위젯 금지` 과잉 규칙 · `모든 mutation 후 전체 family invalidate` ·
       `iOS simulator jank = 앱 버그` — 3 종 각각에 대해 "하지 마라" 취지 문구가 해당 표면에 존재)

## Architecture

- [ ] AR-01: 변경이 17 개 경로로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 스테이징 완료 후 ·
       측정: `git diff --cached --name-only -- flutter-toolkit docs ':(exclude).harness'` 결과가
       `flutter-toolkit/agents/widget-inspector.md`,
       `flutter-toolkit/references/flutter-ai-rules.md`,
       `flutter-toolkit/references/primitive-substitution-gate.md`,
       `flutter-toolkit/skills/flutter-api/SKILL.md`,
       `flutter-toolkit/skills/flutter-audit/SKILL.md`,
       `flutter-toolkit/skills/flutter-error/SKILL.md`,
       `flutter-toolkit/skills/flutter-hooks/SKILL.md`,
       `flutter-toolkit/skills/flutter-provider/SKILL.md`,
       `flutter-toolkit/skills/flutter-screen/SKILL.md`,
       `flutter-toolkit/skills/flutter-test/SKILL.md`,
       `flutter-toolkit/skills/flutter-transition/SKILL.md`,
       `flutter-toolkit/skills/flutter-widget/SKILL.md`,
       `docs/flutter/quality/performance.md`,
       `docs/flutter/quality/testing.md`,
       `docs/flutter/research-log.md`,
       `docs/flutter/state/state-management.md`,
       `docs/flutter/ui/animation.md` 17 행과 정확히 일치)
- [ ] AR-02: `docs/flutter/research-log.md` 의 정정 대상 historical 줄이 전부
      `[정정 2026-08-13]` 주석을 달고 있다 [exact]
      (측정: `grep -nE '(when.*map|map.*when).*제거|Impeller 상태|Impeller 진행 상황|stable \*\*3\.44\.7\*\*' docs/flutter/research-log.md | grep -v '정정 2026-08-13' | wc -l` → `0` ·
       음성 대조: 주석 하나를 지우면 이 측정이 FAIL 해야 한다)
- [ ] AR-03: `docs/flutter/research-log.md` 최상단에 `## [2026-08-13] — Phase 5 kaizen` 라운드가
      추가되고 frontmatter `last_updated` 가 `2026-08-13` 이다 [exact]

## Anti-patterns

- [ ] AP-03: 변경 파일 전체에 bare code fence(``` 뒤 언어 힌트 없음)가 0 건이다 [exact]
      (측정: `python3 scripts/validate-plugin.py flutter-toolkit` 통과 + 변경된 `docs/flutter/*.md`
       에서 `grep -cE '^\`\`\`$'` 합계 0)
- [ ] AP-01: 이번 커밋이 새로 도입한 버전 토큰·URL 이 전부 evidence 파일에 존재한다 [exact]
      (측정: `git diff --cached -U0` 의 추가 줄에서 뽑은 신규 `https://` URL 집합이
       `.harness/.meta/evidence/phase5.md` 또는 기존 본문에 실재 — 날조 0 건)

## Reusability

- [ ] RE-01: 4 소비 표면이 Gate 위젯 목록을 각자 재열거하지 않는다 [exact]
      (측정: `CircularProgressIndicator` 를 게이트 목록으로 열거하는 파일이
       `primitive-substitution-gate.md` 1 개뿐 — 소비 표면 4 개에서 목록 재열거 0 건)
- [ ] RE-02: 신규 reference 가 기존 SSOT 패턴(`visual-evidence-protocol.md` 인용 방식)을 따른다 [structural]

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py flutter-toolkit` 이 FAIL 0 으로 통과한다 [exact]
- [ ] DG-02: `python3 scripts/sync-docs.py --check-only` 가 Scope 밖 파일 갱신을 요구하지 않는다 [exact]
- [ ] DG-04: 위 모든 grep 오라클을 zsh 와 bash 에서 실행한 출력이 동일하다 (diff 0) [exact]
