# ex 묶음 기록 — 바깥 원문 대조 반영 (A5 ~ A13)

- 계약: `.harness/sprint-contract-after-0928-external-facts.md` (29 조건, 봉인 커밋 `45dc0d7`, 조건 지문 `sha256:72ee727e080b7190` · 측정 지문 `sha256:755b6e62692e0170`)
- 기준 판 `e78ea2f`, 가지 `chore/ak3-ex`. 근거는 `ex/A5.md` ~ `ex/A13.md` (Codex, 2026-09-28 조회) 하나다. 새로 조회하지 않았다.
- QA 판정은 하지 않았다. 계약 `status` 는 `active` 그대로다.

## 항목별 결과

| 항목 | 한 일 | 커밋 |
| --- | --- | --- |
| A5 | design-system SKILL 의 Material 3 Expressive 문단을 m3.material.io 원문대로 고쳤다. `Android 16` · `tonal palette 정교화` · `컬러 토큰 세트` · `variable font axes` 를 빼고, primitive 매핑은 저장소 관례라고 밝히고, 공식 주소 넷과 조회일을 붙였다 | `1fbcc0f` |
| A6 | flutter-screen 의 go_router 줄을 18.0.1 로, flutter-transition 의 auto_route 줄을 11.2.0 으로 고쳤다. `notifyRootObserver: false` 복원 설명과 「컴파일 에러」 단정은 원문에 없어 뺐고 11.1.0 의 `animatePageTransition` 폐기 예정을 더했다 | `3dcde22` |
| A7 | OpenTofu 하한을 mocking 1.8+ · write-only 1.11+ 로 고쳤다 (킷 세 파일 · infra-test 페이지). cicd.md 원칙 7 과 페이지에 GitLab `sha` · Buildkite `commit` 조회를 적었다. 조사 기록에 2026-09-28 정정 절을 더하고 페이지에 새 절 · 목차 · 출처 주소 모음(103 → 108)을 맞췄다 | `ba38466` · `010a9de` |
| A8 | 백엔드 감사 두 행 — 오프셋 없는 벽시계 문자열에 `format: date-time` 이면 FAIL, IANA 칸 · 순간 하나 저장 FAIL 은 이 킷 규칙. database.md 원칙 10 과 페이지에 같은 사실과 출처 | `e7257b0` · `45ab0e5` |
| A9 | react-screen Gotcha 11 의 canary 단정을 빼고 React 19.2 발표 글을 출처로 달았다 | `ca86f4c` |
| A10 | flows.md 와 페이지에 2026-09-28 npm latest 12.0.0 재확인과 주소. planning 조사 기록에 PRD · ADR 비교 절 (우선하라는 원문은 찾지 못했다). 조사 기록 페이지는 두지 않는 결정 그대로 | `3f7466b` |
| A11 | C-06 강도를 MUST 에서 SHOULD 로 (core-comment · comment-economy md/페이지 · templates md/페이지). 국립국어원 자료 이름표를 「유형별로 알아보는 보도자료 작성 길잡이」 로 (8 파일, sources 상태는 「확인됨 (2026-09-28) — 제목 · 등록일만」). 예시의 `__` 를 `_` 로 (4 파일) | `06c1b7d` · `218a572` |
| A12 | setup-guide 평가 사례 두 개의 조회일 · 갱신일, FCM Apple 새 주소, 상태 값 `documented` · `not_mentioned`. FCM iOS 예시 가이드와 페이지의 서비스 계정 줄에 ADC 우선과 출처 두 개 | `c16daee` · `b1ccae9` |
| A13 | 에이전트 설계 가이드와 페이지 — 「하드 리밋」 을 「플랫폼 기본 상한」 으로, 두 값이 환경 변수로 바뀌는 기본값임을 적고, 「상한에 걸리면 Agent 도구가 실패한다」 를 뺐다. 출처 두 줄에 2026-09-28 재조회 | `bf04301` · `031f096` |

## 자기 측정 (TIP 기준, 2026-09-28)

- SK-01 ~ SK-16: 조건마다 적힌 명령을 그대로 돌려 전부 기대값과 같았다. SK-14 음성 대조(끝 `}` 를 지운 사본)는 JSON 명령 종료 코드 1.
- ER-01: `newurls.sh` 출력 0 줄, 종료 코드 0. 음성 대조 — `docs/planning/flows.md` 에 `https://z.example.com/new` 를 더한 떠 있는 커밋(가지는 안 옮김)에 돌리면 1.
- AR-01: BAD 0 · 커밋 수 1 이상. AR-02: 범위 밖 경로 0. AR-03: 14 페이지 공통 CSS 링크 각 1, `check-docs-a11y.js` `14/14 PASS`.
- AP-03 · AP-04: `validate-plugin.py` 두 검사 종료 코드 0. DG-01: 0. DG-02: md 23 파일 경고 0 (나쁜 줄을 붙인 사본은 4 · 종료 코드 1).
- SC-01: `ci-local.sh` 25 단계 rc=0 · `feedback-agg-test SKIP (yq 없음)` 한 줄. CI 파일에만 있는 여섯 단계 전부 rc=0. `npx playwright test` 두 묶음(design-kit 156 · api-kit 8) 전부 통과.
- 톤: tone-kit `locale-korean.md` §8 G-1 · G-2 를 더한 줄 216 줄에 돌려 0 건.

## 킷 버전 판단

바뀐 킷은 design-kit · flutter-toolkit · infra-kit · backend-kit · react-kit · tone-kit · onboarding-kit · harness(가이드 문서만) 여덟이다. 모두 문장 정정이라 patch 로 본다. tone-kit 은 C-06 강도가 내려갔지만 새 규칙이 아니라 기존 규칙의 강도를 원문에 맞춘 것이라 patch 로 둔다. 릴리스는 합친 뒤 main 에서 한다 (이 묶음에서는 하지 않았다).

## 남은 것

- `design-kit/docs/design/systems/material-design.md` 와 그 페이지의 「Android 16」 — 그 문서가 따로 단 Android Developers Blog 출처를 대조하지 않았다. 그 출처를 조회해야 판정할 수 있다.
- `docs/flutter/architecture/routing.md:85-86` 의 `(_, __)` — A11 은 tone 예시만 물었다. 같은 Dart 3.7 사실이라 flutter 문서 정리 때 같이 고치면 된다.
- setup-guide 평가 사례 `deprecation-claim-fidelity` 의 단정 줄 `guide_includes('.p8')` · `guide_recommends('APNs 인증 키(.p8)')` — 새 FCM 문서는 `.p8` 확장자도 「recommended」 강도도 쓰지 않는다 (ex A12 §4). 단정을 바꾸려면 Apple 의 APNs 키 공식 문서를 따로 조회해야 해서 이번에는 출처 칸과 상태 값만 고쳤다.
- ex 파일이 「추론」 으로 낸 새 규칙은 넣지 않았다 — 벽시계 문자열 모양 고정(`YYYY-MM-DDTHH:mm:ss`), PRD · ADR 경계 규칙, setup-guide 조회일 · 갱신일 분리 규칙, 서비스 계정 선택 나무 전체. 넣으려면 사용자가 킷 규칙으로 정해야 한다.
- 국립국어원 자료는 제목 · 등록일만 확인했다. 첨부 PDF 본문이 원칙 1 · 2 · 5 · 8 을 실제로 뒷받침하는지는 미확인이다.
- 역사 기록은 고치지 않았다 — `.harness/.meta` 의 leftovers · phase notes, `docs/tone/research-log.md:44`, `docs/infra/research-log.md` 2026-09-24 절의 「다음 사이클 후보」 줄. 2026-09-28 정정 절이 그 줄을 정정한다.
- 작업 폴더에 계약 피드백 초안 `.harness/feedback-draft-after-0928-external-facts.yaml` 이 추적 안 된 채 남아 있다 (저장본은 `~/.harness/feedback/contract/1a3bcba6-2026-09-28T110000-bda55d45-97400.yaml`, 검증 PASS).
