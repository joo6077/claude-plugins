---
source: claude-code-insights
generated: 2026-08-13
window: "2026-06-12 ~ 2026-08-12 (62일, 81 세션 중 71 세션 분석, 1,551 메시지, 3,608h, 241 커밋)"
report_file: ~/.claude/usage-data/report-2026-08-13-083357.html
supersedes: 2026-07-27 (51 세션 / 53일)
overlap_warning: >
  이 리포트의 관측 윈도(2026-06-12~08-12)는 직전 카이젠(2026-07-27~28)의 수정이 착지하기
  **이전 기간을 대부분 포함**한다. 즉 Friction #1~#3 의 재출현은 "고친 것이 안 먹혔다"는
  증거가 아니라 **아직 측정되지 않았다**는 뜻이다. 같은 규칙을 또 추가하지 마라.
---

# Claude Code Insights — 카이젠 주입용 (§0)

62일 · 71 세션 분석 산출물. 각 Phase 는 아래를 **도메인에 맞게 일반화**하되,
"직전 사이클 흡수분" 섹션과 겹치는 항목은 **새 규칙 추가 금지**다.

## ⚠ 직전 사이클(2026-07-27, PR #15)에서 이미 구조적으로 승격 완료 — 중복 금지

| 이번 리포트 항목 | 직전 사이클 승격물 | 판정 |
| --- | --- | --- |
| 진단 전 편집 착수 (wrong_approach 50) | Phase 1 Enforcement 3등급(E1/E2/E3) + §3.7 Completion Evidence Gate | 흡수됨 |
| 검증 없이 "done" 주장 | Phase 3 **Evidence Validity Gate** (존재→유효성), `[미검증]` 3분기 triage | 흡수됨 |
| 확정 결정이 일부 표면에만 적용 | Phase 1 §5.5 **Counterpart Enumeration**, Phase 7/11 `## Surfaces` 양면 열거 | 흡수됨 |
| 서버만 바꾸고 클라 누락 | Phase 2 two-sided 계약 + Phase 7/9 Counterpart 일반화 | 흡수됨 |
| 시각 작업 의도 외 영역 변경 | Phase 6 `visual-change-protocol.md` §2 (의도 외 변화 = 실패), Phase 5 `visual-evidence-protocol.md` | 흡수됨 |
| 스테일 핸드오프 재파생 | Phase 4 `/sprint` 핸드오프 **git 기준 재검증** (E2) | 흡수됨 |
| MCP 스냅샷으로 "정상 렌더링" 주장 | Phase 3 "빈 캡처는 PASS 증거가 아니라 검증 실패 신호" | 흡수됨 |

**따라서 이번 사이클의 유효 신호는 위 표에 없는 것들이다.** 아래 §신규 델타만 개선 대상으로 삼아라.

## 신규 델타 (직전 사이클에 없던 신호)

### D1. 3D 프린팅 실측 실패 3종 — bambu-kit 직격 (신규·구체적)

5 세션에서 shower-box / holster 모델 프로파일을 생성했고 **실물 출력 결과가 계속 새 문제를 노출**했다.
결과는 "partially successful".

- **곡면 계단현상 (curved-surface stair-stepping)** — 레이어 높이/가변 레이어 미적용 추정
- **voronoi 패턴 스트링잉 (stringing)** — 리트랙션·이동 경로·온도 미조정
- **바닥 박리 (base peeling)** — 베드 접착 전략(brim/raft/첫층) 부족

직전 사이클 Phase 13 은 `xy_hole_compensation` 공차 SSOT 오류를 고쳤다. **위 3종은 다른 실패 모드로
references SSOT 에 대응 레시피가 있는지 확인되지 않았다.** 실측 실패 → 프로파일 키 매핑이 필요하다.

### D2. 디자인 탐색의 "축(axis) 미고정 + 산출물 개수 미상한" (부분 신규)

직전 승격물(`visual-change-protocol.md`)은 **확정된 결정을 어떻게 지키는지**를 다뤘다.
이번 신호는 그 **이전 단계** — 탐색 자체가 발산하는 문제다.

- 사용자는 *하나의 디자인 축*(버블 형태 / 컬러 / 이펙트) 변주를 원했는데 파생 디자인 시스템이 쏟아짐
- "몇 개 목업" 요청에 9~40 타일 + 토큰 파일 + 서페이스 레인까지 생성 → 입력바만 남기고 전부 삭제 요구
- 변형들이 서로 **구분되지 않음** — 수량이 품질을 대체하지 못함

→ 일반화: 탐색형(generative-exploration) 스킬은 착수 전에 **(a) 변주 축 1개 명시 (b) 산출물 정확한
개수 (c) 부대 인프라(토큰/DS/문서) 생성 금지**를 계약으로 고정해야 한다. Phase 1(아키타입) / Phase 6.

### D3. 사용자 버그 리포트에 자기 테스트 증거로 반박 (신규·행동 패턴)

A3 목업 변형이 여전히 깨졌다는 사용자 리포트에 Claude 가 **테스트 증거를 들어 반박**했고 세션이
욕설로 에스컬레이션됐다. 빈 카탈로그 세션도 동형 — MCP 스냅샷을 근거로 사용자 관측을 부정하다가
결국 unbounded-height ListView collapse 를 발견.

직전 사이클 Evidence Validity Gate 는 **자기 주장의 증거 유효성**을 다뤘지만,
**사용자 관측 vs 자기 증거가 충돌할 때의 우선순위**는 정의되지 않았다.

→ 일반화: 사용자 관측은 **반증 대상이 아니라 재현 대상**이다. 충돌 시 (a) 자기 증거의 오라클이
사용자가 보는 것을 재는지 먼저 의심 (b) 실기기/실화면 재확인 (c) 반박 금지.
Phase 1(설계 원칙) / Phase 3(evaluator) / Phase 5·6(UI kit reviewer) 공통.

### D4. 백엔드 동시성 — TOCTOU 를 앱 레벨이 아닌 SQL 술어로 해소 (부분 신규)

feed TOCTOU 경합을 in-SQL `EXISTS` 술어로 해소, FCM 토큰 idempotency 의 partial unique index 충돌,
S3 객체 회수. 직전 Phase 7 은 write-path idempotency 를 넣었으나 **read-check-then-write 경합의
SQL 레벨 해소 패턴**은 없다. backend-kit / rust-kit 동시성 섹션 후보.

### D5. 성능 조사에서 "앱 코드가 아닌 환경" 판별 (강화 대상 — 성공 사례)

18일간 누수된 시뮬레이터 render host 가 swap 포화를 유발한 것을 앱 코드 최적화 전에 규명.
Impeller vs Skia A/B, 커스텀 lint 규칙으로 회귀 방지. **성능 감사 스킬에 "환경 배제 먼저" 단계**가
있는지 확인 대상 (flutter-audit / infra-audit).

## Recommended Patterns (강화 대상 — 사용자가 잘 작동시킨 것)

1. **MCP 기반 시각 검증 루프** — find_widget 878 / screenshot_widget 494 회. 주장 대신 실제 픽셀.
2. **계약 게이트 QA 스프린트** — 소셜 피드 슬라이스 27/27 APPROVE, 자기 유발 머지 순서 버그 사전 차단.
   REJECT 를 강제 머지하지 않고 핸드오프로 넘긴 것이 계약을 유효하게 유지.
3. **근본원인 우선** — FCM 409 partial unique index, InheritedElement/GlobalKey reparent crash,
   시뮬레이터 render host 누수. 최고 성과 세션은 전부 하드 증거 동반.

## On the Horizon (사용자 제안 상위 워크플로우)

1. **골든 스크린샷 회귀 하네스** — `design/decisions.yaml` (decision_id → 이 결정을 반영해야 하는
   모든 surface 목록) + 골든 PNG 디렉토리 + 픽셀 diff 검증 스크립트. manifest 의 decision_id 에
   대응 골든이 없는 surface 를 FAIL 로 잡아 "A1 엔 적용, A3 엔 누락" 을 구조적으로 차단.
2. **풀스택 계약 병렬 레인** — backend-lane / client-lane / test-lane / qa-adversary(계약 텍스트와
   최종 diff 만 읽음) 4 레인. 전 레인 green + adversary APPROVE 전 머지 금지.
3. **야간 자율 백로그 소진** — BACKLOG.md 스키마화 → 헤드리스 루프가 "이미 완료됐는지 코드로 재검증"
   후 브랜치 구현 → 테스트 green 까지 반복 → PR. 가드레일: dev 직접 push 금지, 머지 금지,
   마이그레이션 인간 검토, 동일 항목 3연속 실패 시 중단.

## 각 Phase 적용 힌트 (신규 델타만)

- **Phase 1 설계 가이드**: D2 (탐색형 아키타입에 축/개수/부대산출물 금지 계약), D3 (사용자 관측 우선순위 원칙)
- **Phase 3 Evaluator**: D3 — 사용자 관측 vs 자기 증거 충돌 시 판정 규칙
- **Phase 5 Flutter**: D5 — 성능 감사 "환경 배제 먼저"
- **Phase 6 Design**: D2 (탐색 축 고정 + 개수 상한), D3 (design-reviewer 반박 금지), Horizon #1 (decisions manifest)
- **Phase 7 Backend / 9 Rust**: D4 — read-check-then-write 경합의 SQL 술어 해소 패턴
- **Phase 13 Bambu**: D1 — 곡면 계단현상 / 스트링잉 / 바닥 박리 3종 실측 실패 → 프로파일 키 매핑
- **Phase 8 Infra / 10 React / 11 Planning / 12 Reflect / 14 Onboarding**: 이번 리포트에 직접 신호 없음
