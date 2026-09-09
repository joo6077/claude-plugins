---
feature: "howto-kit 설계 브리프 + /howto SKILL.md 초안"
slug: howto-kit-design-brief
created: "2026-09-07 16:45"
complexity: "단순"
conditions: 20
status: done
owner_session: 129c9ed3-0ef3-49fa-b0a5-6f79721d44df
conditions_digest: sha256:dee06e6878247d76
locked_at: "2026-09-07 17:35"
---

## 배경

사용자 불만 4 종(F1 비결정성 · F2 입도 부족 · F3 최신성 결여 · F4 네비게이션 경로 부재)을 고칠
새 플러그인 킷의 **설계 문서**를 만드는 스프린트다. 킷 자체의 구현은 이번 범위가 아니며 다음
세션이 수행한다.

산출물은 2 종이다.

- `docs/howto-kit/design-brief.md` — 다음 세션이 이것만 읽고 킷을 만들 수 있는 설계 정본
- `docs/howto-kit/drafts/SKILL.md` — `/howto` 스킬 초안 (실제 배포 스킬이 아니라 초안 파일)

복잡도 4 축 판정: 레이어 수 1(문서만) = 아니오 / 공개 API·계약 변경 = 아니오(배포 스킬 아님) /
**소비면 존재 = 예**(다음 세션이 이 문서를 소비해 킷을 만든다) / 회귀 위험 = 아니오(신규 파일,
기존 파일 무수정). 1 축만 "예" 이므로 **단순**.

설정 리터럴 대조 — `commands.analyze` = `bash -n scripts/release.sh`,
`commands.test` = `bash scripts/release.sh 2>&1 || true`, `diagnostics.ide_exclude` = `[]`,
카테고리 = Skill(SK) · Script(SC) · Error(ER) · Architecture(AR),
안티패턴 = AP-01 · AP-02 · AP-03 · AP-04. 전부 `project.yaml` 리터럴 그대로 전사했다.

## 리서치 소스

Codex foreground 리서치 6 축(절차 문서 작성 표준 · Google/Apple/Stripe/GitHub 딥링크 · 화면 지목
표현 · deprecation 의미론과 버전 분기 · 결정성/런북/체크리스트 · 한국 일상 절차) + 레포 감사
3 축(onboarding-kit 전수 · 개명 표면과 레포 규약 · 로컬 실패 이력). 브리프에 URL 17 개를 인용했다.

## 범위 경계

- 이번 스프린트는 **플러그인을 만들지 않는다.** `howto-kit/` 디렉토리, `plugin.json`,
  `marketplace.json`, `CLAUDE.md`, `docs/index.html` 은 건드리지 않는다.
- `onboarding-kit/` 은 읽기만 했고 수정하지 않는다.
- diff-scope baseline (2026-09-07 계약 작성 시점 1 회 실행,
  `git status --porcelain -- . ':(exclude)docs/howto-kit' ':(exclude)docs/howto-kit/*'`):
  `?? .harness/sprint-contract-howto-kit-design-brief.md` · `?? docs/bambu-calibration/` ·
  `?? result.json` 3 건. 뒤의 2 건은 **이번 세션 이전부터 존재한 미추적 파일**이며 이번 변경이
  아니다. AR-01 은 이 3 건을 기대 집합으로 삼는다.
- 커버리지 해소: AP-03 — `scripts/validate-plugin.py` V6 는 킷 디렉토리를 스캔하며 `docs/` 를
  대상에 포함하지 않는다(`grep -n "docs" scripts/validate-plugin.py` 결과에 스캔 경로 없음).
  따라서 이 조건은 산출물 2 파일에 대한 직접 fence 검사로 측정하고, 판정 의미(여는 fence 에 언어
  힌트 필수)는 AP-03 정의를 그대로 따른다.

## Skill

- [ ] SK-01: `docs/howto-kit/drafts/SKILL.md` frontmatter 에 `name` · `description` · `user-invocable` 3 필드가 모두 존재한다 [exact, enumerated] (측정: `awk 'NR==1&&/^---$/{f=1;next} f&&/^---$/{exit} f' docs/howto-kit/drafts/SKILL.md | grep -cE '^(name|description|user-invocable):'` == 3)
- [ ] SK-02: 같은 파일의 `description` 에 **비트리거 조건**이 3 건 이상 명시돼 있다 [structural, collective] (측정: `grep -c '트리거하지 않는다' docs/howto-kit/drafts/SKILL.md` >= 3)
- [ ] SK-03: 같은 파일이 500 줄 이하다 [exact] (측정: `wc -l < docs/howto-kit/drafts/SKILL.md` <= 500. 근거: Anthropic Agent Skills best practices "Keep SKILL.md body under 500 lines")
- [ ] SK-04: 같은 파일에 F1~F4 각 결함에 대응하는 장치가 본문에 명시돼 있다 — `F1` `F2` `F3` `F4` 4 개 토큰이 모두 등장한다 [exact, enumerated] (측정: `for t in F1 F2 F3 F4; do grep -qF "$t" docs/howto-kit/drafts/SKILL.md || echo "MISSING $t"; done` 출력 0 줄)

## Script

- [ ] SC-00: N/A (이번 스프린트 산출물은 `docs/` 문서 2 종뿐이며 `scripts/release.sh` · `plugin.json` · `marketplace.json` 을 읽지도 쓰지도 않는다. 버전 bump 와 marketplace 등록은 킷을 실제로 만드는 다음 세션의 범위이며 브리프 §10 의 C1·C8 로 이월했다)

## Error

- [ ] ER-01: `docs/howto-kit/design-brief.md` 에 "확인 못 한 것" 섹션이 존재하고 번호 매긴 항목이 5 건 이상이다 [structural, collective] (측정: `sed -n '/^## 11\./,/^## 12\./p' docs/howto-kit/design-brief.md | grep -cE '^[0-9]+\. '` >= 5)
- [ ] ER-02: `docs/howto-kit/drafts/SKILL.md` 에 1 차 출처 조회 실패 시의 대응이 명시돼 있다 — `[미확인]` 마커와 "시도한 URL" 이 함께 등장한다 [exact, enumerated] (측정: `grep -c '\[미확인\]' docs/howto-kit/drafts/SKILL.md` >= 1 **그리고** `grep -c '시도한 URL' docs/howto-kit/drafts/SKILL.md` >= 1)
- [ ] ER-03: `docs/howto-kit/drafts/SKILL.md` 가 "출처가 없을 때 지어내지 않는다"를 명시한다 — `학습 데이터로 채우지 않는다` 문구가 등장한다 [exact] (측정: `grep -c '학습 데이터로 채우지 않는다' docs/howto-kit/drafts/SKILL.md` >= 1)

## Architecture

- [ ] AR-01: 이번 스프린트의 파일 변경이 `docs/howto-kit/` 과 이번 계약 파일에만 발생했다 [exact, enumerated] (Given: 커밋하지 않은 워킹트리 상태. 측정: `git status --porcelain -- . ':(exclude)docs/howto-kit' ':(exclude)docs/howto-kit/*'` 출력이 **정확히** `?? .harness/sprint-contract-howto-kit-design-brief.md` · `?? docs/bambu-calibration/` · `?? result.json` 3 줄과 일치. 뒤 2 건은 §범위 경계에 기록한 사전 존재 미추적 파일이다)
- [ ] AR-02: `onboarding-kit/` 아래 어떤 파일도 수정되지 않았다 [exact] (측정: `git status --porcelain -- onboarding-kit` 출력 0 줄)
- [ ] AR-03: 산출물 2 종이 `docs/howto-kit/` 아래에 있고 초안은 `drafts/` 하위에 분리돼 있다 [exact, enumerated] (측정: `test -f docs/howto-kit/design-brief.md && test -f docs/howto-kit/drafts/SKILL.md` 성공)
- [ ] AR-04: 브리프가 다음 세션용 완료 조건표를 담고 있다 — `| C<숫자>` 형태의 행이 10 건 이상이다 [structural, collective] (측정: `grep -cE '^\| C[0-9]+' docs/howto-kit/design-brief.md` >= 10)

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 산출물 2 파일의 **여는** fence 에 언어 힌트가 전부 붙어 있다 [exact, enumerated] (측정: 두 파일 각각에 대해 fence 상태기계로 여는 fence 를 판별해 언어 없는 것이 0 건. `validate-plugin.py` V6 는 `docs/` 를 스캔하지 않으므로 직접 측정한다 — §범위 경계 커버리지 해소 참조)
- [ ] AP-04: `docs/howto-kit/drafts/SKILL.md` 의 frontmatter 에 `name` 필드가 존재한다 (validate-plugin V1 이 요구하는 필드 누락 방지) [exact] (측정: SK-01 과 동일 awk 로 추출한 frontmatter 에 `^name:` 1 건 이상)

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 브리프가 `onboarding-kit` 의 재사용 가능 자산(출처 원장 프로토콜 · G2 마커 판정 · search-strategy · format-checklist 코어 섹션)을 열거하고 승계 여부를 명시했다 [structural, collective] (측정: `grep -c 'search-strategy\|format-checklist\|출처 원장' docs/howto-kit/design-brief.md` >= 3)

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상 — 이번 스프린트는 셸 스크립트를 변경하지 않았으므로 회귀 없음 확인용)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`[]` 제외 — 산출물 2 파일 대상. 단 MD025(H1 중복)는 레포 docs 91 개 전부가 frontmatter `title:` + H1 조합을 쓰는 기존 컨벤션이므로 이 조건에서 제외한다)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개 (무인자 실행은 인자 검증에서 종료되므로 릴리스가 실행되지 않는다 — `</dev/null` 로 대화형 입력을 차단해 실행할 것)
- [ ] DG-04: 실제 앱/서버 구동 시 에러 0개
