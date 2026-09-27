# dr1b 기록 — 문서 페이지 다시 맞추기 B

계약: `.harness/sprint-contract-after-0926-docs-regen-b.md` (봉인 `3524cadc5bdca4e8`, 측정 지문 `589425b3414cf1e0`, 봉인 커밋 `36b7513`).

## 한 일

- 14 쪽을 지금 원본에 맞췄다. 원본이 `6378948` → `c3e45f3` 사이에 더한 줄을 쪽마다 옮기고, 원본에서 빠진 예시(`myapp-api`)는 쪽에서도 지웠다.
- 목록 PD-1 · DC-15 가 말한 design-mockup 쪽 다시 맞춤은 이 묶음이 했다. Step 0~6 새 번호, PRD 없음 자리 표, 주의사항 17 개 원문을 옮겨 낱말 비율이 0.54 에서 0.95 로 올랐다.
- 목록 KT-2(원본 글이 바뀌었는데 머리 판이 그대로)는 쪽이 원본 머리 판 번호와 날짜를 그대로 따르게 두었다. 원본 판을 올리는 일은 원본 쪽 묶음에 넘긴다.
- 11 쪽이 쪽 안에 다시 적던 움직임 줄이기 규칙을 지우고 공통 파일에 맡겼다. 두 쪽의 넘침 숨김 선언도 지웠다(cicd 카드 줄무늬는 둥근 모서리를 따로 준다).
- setup-guide 에 스타일 없는 링크가 생겨 대비 검사가 떨어졌기에 목록 안 링크에 강조색을 주었다.

## tone-guide 결과

- tone-guide 1 단계: 레포 오버레이 `.claude/tone-project.md` 를 읽었다(어댑터 없음 · 주석 언어 ko). 코어 네 파일 규칙표와 `locale-korean.md` K-01~K-11 을 불러왔다. 이번 변경에 걸리는 것은 K-02 번역투 · K-03 능동형 · K-10 대조 grep · K-11 새 이름 금지다.
- tone-guide 5 단계: 새로 더한 줄 190 개에 §8 G-1 grep 을 돌려 잔존 0 건. `합니다` 는 원문 안내 문구 인용 두 곳뿐이다. 새 주석 · 새로 지은 이름은 없다.

## 담김 값 (옛 판 → 새 판)

coverage.py(기준 `38cccd1`)와 fence2.py(기준만 `38cccd1` 로 바꾼 사본)로 잰 값이다. 두 도구 모두 모든 쪽에서 빠진 수가 0 이다.

| 쪽 | 낱말 비율 | 코드 표시 | 코드 블록 줄 |
| --- | --- | --- | --- |
| design-kit/visual-change-protocol | 0.94 → 0.96 | 71 → 72/72 | 130 → 130/136 |
| design-kit/design-mockup | 0.54 → 0.95 | 23 → 38/38 | 21 → 21/21 |
| design-kit/design-test | 0.92 → 0.93 | 66 → 70/70 | 155 → 155/155 |
| flutter-toolkit/visual-evidence-protocol | 0.94 → 0.96 | 37 → 37/37 | 10 → 10/15 |
| infra-kit/cicd | 0.94 → 0.94 | 25 → 25/25 | 7 → 7/7 |
| infra-kit/infra-test | 0.86 → 0.86 | 136 → 136/137 | 219 → 219/219 |
| onboarding-kit/setup-guide | 0.56 → 0.65 | 68 → 74/82 | 61 → 78/78 |
| onboarding-kit/format-checklist | 0.87 → 0.88 | 26 → 26/28 | 8 → 8/8 |
| react-kit/render-evidence-protocol | 0.95 → 0.96 | 64 → 64/64 | 22 → 22/24 |
| reflect-kit/reflect-digest | 0.99 → 1.00 | 197 → 198/198 | 123 → 123/123 |
| rust-kit/project-detection | 0.97 → 0.98 | 159 → 159/159 | 3 → 3/3 |
| tone-kit/dart-flutter-idioms | 0.96 → 0.96 | 177 → 177/182 | 178 → 178/211 |
| tone-kit/naming-taxonomy | 0.95 → 0.95 | 138 → 139/141 | 73 → 73/92 |
| tone-kit/adapter-dart-flutter | 1.00 → 1.00 | 203 → 203/203 | 31 → 31/31 |

## 캡처

캡처 폴더: `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/dr1b/caps`

- 14 쪽 × 320 · 375 · 1280 × dark · light 84 장이다. 커밋하지 않았다.
- design-mockup Step 0 · Step 5, setup-guide 주의사항 절을 따로 잘라 눈으로 확인했다. 넘침 · 잘림은 없었다.

## 넘긴 것

- 목록 DC-12(어두운 테마 전용 쪽의 밝은 테마)는 이 묶음 범위 밖이다. 해당 쪽은 visual-change-protocol · design-test · visual-evidence-protocol · cicd · infra-test · format-checklist · render-evidence-protocol 일곱이다. 밝은 테마 설정으로 열어도 어두운 화면으로 그려진다.
- setup-guide 는 원문을 풀어 쓴 문장이 많아 낱말 비율이 0.65 에 머문다. 뜻은 담았고 옛 판보다 높다. 원문을 더 옮기려면 다음 다시 맞추기 때 한다.
- 원본을 더 고칠 다른 묶음(KR-1 · KR-3 · VS-21 등)이 합쳐진 뒤 `python3 scripts/detect-docs-drift.py --since <합친 기준>` 으로 다시 맞출 쪽을 뽑는다.
- 이웃 묶음 dr1a 와 대상 집합이 겹치지 않는지는 dr1a 계약이 채워진 뒤 부모가 한 번 더 대조한다.

## 검토 뒤 고친 것

- 검토에서 onboarding 두 쪽이 한 쪽 안에서 게이트 숫자가 어긋난다고 짚었다. setup-guide 의 수치 표 두 줄과 끝 점검 목록, format-checklist 의 제목 · 보고 규약 · 통과 예시 출력 · 끝 점검 목록을 원본대로 G1~G5 · 6 줄 · 5 가지로 고쳤다. format-checklist 에는 G5 설명 줄을 더했다.
- 두 쪽에서 `G1~G4` · `5 줄` · `5줄` · `4 가지` 를 다시 찾으면 0 건이다. 담김 값은 고치기 전과 같다(setup-guide 0.65, format-checklist 0.88).
- 범위 밖 쪽 search-strategy 에도 `guide_gate G1~G4` 가 남아 있다. 짝 목록에 없는 쪽이라 이번에는 두고 다음 묶음에 넘긴다.

## 남은 것

독립 검토가 막지 않는 것으로 본 결함이다. 이번 묶음에서는 고치지 않았다.

- setup-guide 가 원본 인라인 코드 82 개 가운데 8 개를 옮기지 못했다(`harness/docs/guides/skill-design-guide.md` · `.env.local` · `.env.production` · `com.<앱이름>.app` · `references/project-detection.md` · `/insights` 등). 원본 254 줄 「지금 만들 수 없다고 결론 내릴 때도 §3.7 조항 3 의 네 칸을 적는다」 규칙과 40 · 42 줄의 §3.7 연결도 쪽에 없다. 옛 판에도 없던 것이라 계약 위반은 아니다. 다음 다시 맞추기 때 옮긴다.
- 원본 오류를 그대로 옮긴 것이 하나 있다. `design-kit/references/visual-change-protocol.md:223` 과 그 쪽 687 줄이 「PRD 없음」 규칙을 design-mockup Step 6 이라고 가리킨다. design-mockup SKILL.md 에서 Step 6 은 Figma 전송이고 이 규칙은 Step 5(171 줄)에 있다. 원본부터 고친 뒤 쪽을 따라 맞춘다.
- 범위 밖 쪽 `docs/onboarding-kit/search-strategy.html:513` 에 `guide_gate G1~G4` 옛 값이 남아 있다(위 「검토 뒤 고친 것」과 같은 건).
- `design-test.html` 에서 쪽 안 움직임 줄이기 규칙을 지우면서 `.feat-card:hover{transform:none}` 도 사라졌다. 움직임을 줄인 설정이어도 카드에 올리면 순간 이동한다. 공통 파일이 전환 시간은 줄여 주므로 사소하다.
- DG-05 재는 명령의 전제(`W==TIP && clean`)가 QA 가 스스로 바꾸는 계약 status 한 줄과 부딪혔다. 다음 계약은 비교 범위에서 `.harness/` 를 빼거나 status 줄을 전제에서 뺀다.
