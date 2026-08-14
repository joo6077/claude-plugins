# Sprint Feedback
Feature: 카이젠 Phase 14 — onboarding-kit 사실 정정 4종 + Guide Conformance Gate(E3) + 미검증 카운터 canonical 전파
Evaluated: 2026-08-14 12:00
Verdict: APPROVE
Iteration: 2 (재평가 — 최초 판정이 글로벌 피드백 풀에 저장되지 못해 독립 재실행)

## 재평가 사유
최초 QA는 오케스트레이터의 structured output schema 강제로 인해 판정 자체는 실재했으나
(워크플로 저널 27건 · 트랜스크립트 63개) 글로벌 피드백 풀(`~/.harness/feedback/evaluator/`)에
저장되지 않았다. 이번 재평가는 이전 판정을 승계하지 않고 23개 조건 전부를 직접 재실행했다.

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-kaizen-phase14-onboarding-facts.md
- sha256: b9e2166145dd56e27e750fb1a6caa43724f256a44cbe02a8256bd5cc207c5733
- status: done (변경하지 않음 — 지시에 따라 유지)
- slug: kaizen-phase14-onboarding-facts
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- 선택 근거: 사용자 지정 경로 (명시)
- seal_status: SEAL_OK (recorded=6f3dd3d4fc963a30, actual=6f3dd3d4fc963a30 — zsh·bash 동일)
- 조건 수: frontmatter conditions=23, 정규식 파싱 결과=23 (일치)
- 재확인(저장 직전): 일치 (FINGERPRINT OK)
- status_transition: skipped (지시에 따라 상태 변경 금지 — 오케스트레이터가 처리)

## Amendments
- amendments: 2 (사이드카: `.harness/sprint-amendments-kaizen-phase14-onboarding-facts.md`)
- AM-01 — clarification, ER-03 원 측정문의 거짓양성(부정문 co-occurrence) 재검증 기록.
  조건 문구를 완화하지 않음. 이번 재평가는 이 amendment를 PASS 근거로 쓰지 않고 원 계약
  측정문(awk 동시출현 + `❌ Deprecated` grep)을 문자 그대로 직접 재실행해 독립 확인했다
  (결과 0건 · Read로 :62 라인 맥락 확인 — "단정"이 아니라 명시적 비단정 서술).
- AM-02 — 계약 무관 기록 (구현자의 zsh 단어분할 자기검증 실수 기록). 조건과 무관.

## User Correction Audit
- correction_log_status: available (`/Users/jackson/.claude/logs/claude-plugins/2026-08.md`)
- unreflected_corrections: 0 (2026-08-13 16:05~20:30 구간 사용자 발언은 전부 자동화 트리거
  "ㄱㄱ"와 task-notification뿐이며, onboarding-kit/phase14 방향에 대한 직접 교정 발언 없음)
- verdict 영향: 없음

## Results

### Skill (6/6)
- [x] SK-01: 미검증 마커 canonical 4분기 접미 체계 — PASS
  - 근거: `onboarding-kit/skills/setup-guide/SKILL.md` grep 결과 `미검증:ENV`=5, `미검증:INVALID`=3,
    `Canonical Unverified-Evidence Protocol`=2. L3: 34~42행을 Read, 접미 분류 정의·임계 인용·
    4요건 명세가 실제 규범 문장으로 존재 (장식적 언급 아님).
- [x] SK-02: 킷 로컬 blanket 임계 서술 0건 [exact, enumerated] — PASS
  - 근거: 3파일 개별 grep 전부 0 (`SKILL.md`=0, `format-checklist.md`=0, `search-strategy.md`=0).
- [x] SK-03: `guide_gate` 함수 + G1~G4 4토큰 — PASS
  - 근거: `grep -c 'guide_gate' SKILL.md`=4, G1_LEDGER/G2_MARKER/G3_STACKMIX/G4_DEPRECATION 각 2건.
- [x] SK-04: `guide_gate` zsh·bash 동일 출력 [goal] — PASS
  - 근거: SKILL.md에서 함수 원문 추출 후 배포 예제(`fcm-ios-setup-guide.md`, stack=flutter)에
    bash·zsh 양쪽 실행 → 5줄 출력 완전 동일(`GATE_PASS`). 음성 대조: `unset -f guide_gate` 후
    호출 시 `command not found` (exit 127)로 판별력 확인.
- [x] SK-05: Regeneration Drift 절 + guide_gate 호출 — PASS
  - 근거: SKILL.md:207 `Regeneration Drift 검사` 절이 :212 `guide_gate "$f" "$STACK"` 호출.
- [x] SK-06: Gotcha 2 "로그인"+"공개 문서" 동시 출현 — PASS
  - 근거: Gotcha 2 절(:124~133) 내 `로그인`=3건, `공개 문서`=4건.

### Error (8/8)
- [x] ER-01: `99%`/`거의 안 들어감` 0건 — PASS (grep -c = 0)
- [x] ER-02: Gotcha 3 App Store Connect + 3토큰 [exact, enumerated] — PASS
  - 근거: Gotcha 3 절 내 `App Store Connect`=4, `앱 레코드`=2, `빌드 업로드`=2, `TestFlight`=2.
- [x] ER-03: `.p12` deprecated 단정 0건 — PASS
  - 근거: `awk '/[Dd]eprecated/ && /\.p12/'` = 0행, `❌ Deprecated` = 0건. :62 라인 Read로 맥락
    확인 — "이 가이드는 1차 출처가 안내하는 .p8 흐름만 다룹니다" (비단정 서술).
- [x] ER-04: Swift 코드펜스 + `FirebaseApp.configure()` 0건 — PASS (둘 다 0)
- [x] ER-05: "네이티브 코드 없음 ≠ Xcode 설정 없음" 명시 — PASS
  - 근거: `Capability`=6, `Background Modes`=5, `Xcode 프로젝트`=3. :90행이 구분을 명시적으로 서술.
- [x] ER-06: Firebase 콘솔 라벨 6종 [exact, enumerated] — PASS
  - 근거: `Cloud Messaging`=5, `iOS app configuration`=2, `APNs authentication key`=5,
    `DevOps & Engagement`=2, `New campaign`=2, `Send test message`=3 (전부 >=1).
- [x] ER-07: GCP 리다이렉트 호스트 기록 — PASS (`docs.cloud.google.com` in search-strategy.md = 1)
- [x] ER-08: 하드코딩 버전 핀 0건 — PASS (semver caret 패턴 = 0)

### Architecture (5/5)
- [x] AR-01: 변경 4경로 + 계약 정확히 일치 [exact, enumerated] — PASS
  - 근거: `git diff --name-only b52c8bf^ b52c8bf -- onboarding-kit docs/onboarding-kit
    .harness/sprint-contract-...md` = 계약이 명시한 5개 경로와 `diff` 비교 exit 0 (집합 완전 일치).
- [x] AR-02: Step 수=출처 수, 둘 다 >0 — PASS
  - 근거: steps=8, ledger=8. 음성 대조: 출처 줄 1개 제거 시 ledger=7로 불일치 재현 확인.
- [x] AR-03: `guide_gate` 실행 결과 `GATE_PASS` [goal] — PASS
  - 근거: SK-04와 동일 실행에서 마지막 줄 `GATE_PASS`. 음성 대조: 출처 줄 제거본에서
    `G1_LEDGER FAIL steps=8 ledger=7` → `GATE_FAIL` 재현.
- [x] AR-04: `docs/onboarding-kit/*.html` 0건 변경 — PASS
  - 근거: `git show --name-only --format= b52c8bf | grep -c '^docs/onboarding-kit/.*\.html$'` = 0
    (현재 HEAD 기준으로도 0, 후속 F1 커밋 1c6216b은 onboarding-kit/docs 경로 무변경 확인).
- [x] AR-05: 예제 제목에 `Flutter` 토큰 — PASS (1행 `# FCM 푸시 알림 설정 가이드 — Flutter (iOS / Apple)`)

### Anti-patterns (2/2)
- [x] AP-03: bare 여는 code fence 신규 도입 0건 — PASS
  - 근거: 5개 변경 파일 전체를 Python으로 상태 트레이스(open/close 페어링) — bare 여는 펜스
    0건. diff상 후보 4곳(라인 46/268/329/515)은 전부 닫는 펜스로 확인(스코프 밖).
    `validate-plugin.py`의 V6 code-fence 검사도 독립적으로 0 bare 확인 (DG-01 결과와 교차).
- [x] AP-01: SKILL.md·references 하드코딩 버전 합계 0 — PASS

### Reusability (1/1)
- [x] RE-01: 미검증 프로토콜 harness canonical 인용, 킷 재정의 0 — PASS
  - 근거: 3파일 전부 `harness/docs/guides/qa-evaluation-guide.md` 앵커 인용 확인
    (`grep -l`로 3파일 모두 매치). SK-02와 짝으로 임계 재정의 0건 재확인.

### Diagnostics (1/1)
- [x] DG-01: `validate-plugin.py onboarding-kit` Exit 0 — PASS
  - 근거: 실행 출력 `Total: 1 plugins, 1 OK / Exit: 0`. echo $?=0.

## Unverifiable Summary
- 총 미검증 건수: 0
- Verdict 영향: 없음 (임계 미도달)

## Evidence Validity
- 검사 대상 증거: 23건 (조건별 1건 이상, 다수 조건은 grep + Read + 실행 3단계 결합)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: guide_gate 관련 2개 조건(SK-04·AR-03)을 zsh·bash 양쪽 직접 실행,
  나머지는 grep/git/python 단일 셸 무관 명령이라 이식성 이슈 없음
- 무효 0건 — 미검증 카운터 변동 없음

## Summary
- Total: 23/23 conditions passed
- Verdict: APPROVE
- 이 재평가는 최초 판정을 검증 없이 승계하지 않고, 23개 조건 전부를 직접 명령 실행 +
  Read 맥락 확인 + 4건의 음성 대조로 재확인했다. 결함을 발견하지 못했으며, 이는
  고무도장이 아니라 독립 재실행의 결과다.

## Improvement Suggestions
- [SK-02] 결함 유형: 범위-경계-불완전 — `evals.json`은 계약 scope상 "수정 금지"라 조건
  대상에서 제외됐지만, 그 description 필드에는 여전히 "2 건 이상이면 부분 완료" 킷 로컬
  임계 서술이 남아있다. 다음 사이클에서 evals.json 서술도 canonical 인용으로 정합 검토 권장.
- [orchestrator] 결함 유형: 산출물-경로-부재 — structured output schema를 QA 서브에이전트에
  강제하면 Step 8(피드백 저장) 같은 부가 실행 단계가 스키마 만족과 함께 조용히 스킵될 수
  있다. 출력 스키마에 `feedback_saved_path` 필드를 강제 포함시켜 저장 여부를 계약 자체에
  편입할 것을 권장 (이번 재평가의 근본원인 재발 방지).
