---
feature: "카이젠 2026-09-24 Phase 15 계약 — K-11 새 이름 규칙 · 죽은 이름 게이트 넷 복구 · 확장자 변수 배열"
slug: kaizen-0924-p15-tone-kit
created: "2026-09-25 10:58"
complexity: "복잡"
conditions: 23
status: active
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:afc0e79e2045ae87
locked_at: "2026-09-25 11:35"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase15.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서 `배정` 칸이
`Phase 15` 인 행은 둘이다(`F19` · `reflect-collector:P6`). 다른 Phase 행의 비고가 Phase 15 를 가리키는 것은 없고, 러닝북 `Phase 별 추가 과제` 에도
Phase 15 줄이 없다. 앞 Phase notes 열세 개에서 tone-kit 을 넘긴 줄도 없다(`grep -l 'tone-kit\|Phase 15' .harness/.meta/kaizen-0924/phase*-notes.md` 0 개).
오케스트레이터 `Phase 별 추가 지시` 의 Phase 15 줄(공개 1차 출처 없이 강도를 올리지 않는다 · 탐지 문헌을 되살리지 않는다 · 스킬 셋 상한 ·
`references/` 하위 폴더 금지 · grep 게이트를 고치면 bash · zsh 양쪽과 합성 양성 케이스로 생존 증명)과 근거 파일 §3 현행화 점검도 입력이다.

| 키 | 내용 | 이번 처리 |
| --- | --- | --- |
| `F19` | 사용자가 모르는 한국어 말을 지어냄 (세션 `8fa13c90` · 2026-09-19 「표시훅」) | 반영 — K-11 (SK-01 ~ SK-05) |
| `reflect-collector:P6` | tone-kit K-11 — 사전에 없는 한국어 합성어를 새로 만들지 않음 | 반영 — 강도는 관측 컨벤션. 판정어는 근거 파일 권장안 2 에 따라 「사전에 없는」 대신 「처음 읽는 사람이 뜻을 짐작할 수 있는가」 (SK-01) |
| 근거 §2-2 · §4 권장안 5 | C-06(공개 멤버 doc 주석) MUST 가 출처 PREFER 를 넘는다 | 미반영 — 기록만(SK-05). 한 사이클 관심사 1 ~ 2 개(tone-kaizen Gotcha 3) 가운데 둘을 배정 키와 게이트 생존에 썼다. 다음 사이클 (ER-03) |
| 근거 §2-3 | `etc_seq=663` 이름표가 실제 내용(보도자료 작성 길잡이)보다 넓다 | K-11 근거로는 쓰지 않는다(AR-02). 이름표를 고치면 원칙 1 · 2 · 5 · 8 의 근거를 다시 봐야 해서 다음 사이클 (ER-03) |
| 근거 §3 · §4 권장안 6 ~ 8 | 문서 예시 `__` · 제스처 콜백 58 개 기준 버전 · go_router · 위키 · ESLint 주소 · Material 분리 | 기록만(SK-05). 다음 사이클 (ER-03) |

고칠 것은 두 갈래다.

1. **K-11 새 이름 규칙이 없다 (F19 · P6).** `locale-korean.md` 규칙표는 K-10 에서 끝나고(`:55`), 외래어 3원칙(§4 `:83-89`)은 음역만 다룬다.
   세션 `8fa13c90`(2026-09-19)에서 훅의 동작을 새 합성어 「표시훅」 으로 불러 사용자가 되물었다. 근거 파일 §2-1 은 영어권 문서 가이드(Microsoft ·
   Google)가 새 말 만들기를 피하라고 하지만 한글 맞춤법 제50항 해설은 사전에 없는 전문 용어도 정당한 말로 다룬다고 옮겼다. 그래서 강도는 관측 컨벤션,
   판정은 사전 등재가 아니라 처음 읽는 사람 기준이다. 리서치 문서 원칙 9 · 출처 두 곳 · 평가 사례 4 가 같은 말을 한다
2. **이름 게이트 넷이 죽어 있다 (카이젠 스킬 Step 2 `게이트 생존` 축에서 찾음).** `core-naming.md` §8 은 G-1 · G-2 · G-5 · G-6 명령을 표 칸에 적었다
   (`:218-223`). 표 칸은 `|` 를 `\|` 로 적어야 해서 그 글을 그대로 붙여 넣으면 `\|` 가 정규식의 "또는" 이 아니라 글자 `|` 로 읽힌다. 봉인 전 실측: bash · zsh 둘 다 G-1 · G-2 · G-5 는
   합성 양성 케이스에서 0 줄 · 종료 코드 1 — 이 절이 「통과」 로 읽는 값이다. G-6 은 파이프 자리의 `\|` 가 인자로 넘어가 fixture 파일의 모든 줄을 냈다.
   같은 실측에서 확장자 변수를 한 문자열(`INC="--include=*.dart --include=*.ts"`)로 두면 zsh 가 나누지 않아 0 줄이 됐다 — `core-naming.md` §8 · `core-comment.md`
   §6 · `docs/tone/overview.md` 게이트 예시 세 자리가 같은 모양이다. 나머지 게이트 25 종(주석 G1 ~ G8 · 이름 G-3 · G-4 · G-7 · G-8 · 한국어 G-1 ~ G-3 · 어댑터 10)은
   bash · zsh 모두 합성 양성 케이스를 잡았다(`회귀 게이트` 절)

이번 사이클 Phase 1 가이드 변경과 이 킷(오케스트레이터 Gotcha 「Phase 1 에서 가이드를 변경했으면 전수 체크」):

| 변경 | 이 킷의 자리 | 처리 |
| --- | --- | --- |
| §3.7 `[미검증]` 네 칸 | 없음 — `grep -rn '미검증' tone-kit` 0 줄 | 해당 없음 |
| §3.7 알려진 답 대조 | 이번에 새로 짜는 측정은 이름 게이트 블록 실행 · 확장자 둘 실행 | SC-01 이 손으로 센 답(여덟 줄)으로 잰다 |
| agent 가이드 §10 | 이 킷에 에이전트가 없다 | 해당 없음 |

## 리서치 소스

외부 조회 0 회. 아래 URL 은 전부 근거 파일 `.harness/.meta/evidence/phase15.md` 에서 가져왔다.

- [Microsoft Style Guide — Use technical terms carefully](https://github.com/MicrosoftDocs/microsoft-style-guide/blob/main/styleguide/word-choice/use-technical-terms-carefully.md) — "Don't create a new term if an existing one serves your purpose." · 쓰면 문맥에서 정의한다 (SK-01 · SK-02 · SK-04)
- [Google developer documentation style guide — Jargon](https://developers.google.com/style/jargon) — 피해 쓸 수 있는가 → 더 구체적인 말로 → 꼭 쓰면 처음 나올 때 풀어 쓴다 (SK-04)
- [한글 맞춤법](https://korean.go.kr/kornorms/regltn/regltnView.do?regltn_code=0001) — 제50항 해설: 사전에 없는 전문 용어도 정당하다. 제2항: 단어별 띄어쓰기 (SK-01 · SK-02 · SK-04 — 판정 기준을 사전 등재로 두지 않는 근거)
- [Effective Dart: Documentation](https://dart.dev/effective-dart/documentation) · [린트 `public_member_api_docs`](https://dart.dev/tools/linter-rules/public_member_api_docs) — C-06 강도 초과 기록 (SK-05)
- [국립국어원 etc_seq=663](https://korean.go.kr/front/etcData/etcDataView.do?etc_seq=663) · [LINE 글](https://engineering.linecorp.com/ko/blog/why-are-engineers-so-bad-at-writing/) — K-11 근거로 쓰지 않는 까닭 기록 (SK-05 · AR-02)

근거 파일이 스스로 밝힌 한계를 그대로 옮긴다: Microsoft Learn 페이지 본문이 공개 저장소 판(2018)과 같은지 확인하지 않았다(§5) — `sources.md` 문단에 적는다(SK-02).
「사전에 없는 합성어는 띄어 쓴다」 를 직접 말한 온라인가나다 답변은 찾지 못했다(§5) — 인용하지 않는다. 새 합성어가 독자 이해를 해친다는 실증 연구는 없다(§5) —
그래서 한국어 쪽 근거는 세션 1 건이고 강도는 관측 컨벤션이다.

내부 입력: 데이터 풀 §0 처리 배정표 · §0-b(18 세션 — tone-kit 을 글자 그대로 언급한 행은 없고 `8fa13c90` 의 friction_detail 이 「표시훅」 원문) · §0.5(tone 그룹 없음.
general 그룹의 `feedback_plain_korean_no_jargon` 은 grounding `미분류` 라 PASS 근거로 쓰지 않는다) · 앞 Phase notes 열세 개.
`validate-plugin.py tone-kit` 는 시작 커밋에서 V1 ~ V10 전부 OK 였다(데이터 풀 §5 · 봉인 전 재실행 종료 코드 0).

## GAP 분석 · 개선안 초안

### 카이젠 스킬 절차의 분류

이 Phase 의 카이젠 스킬 `.claude/skills/tone-kaizen/SKILL.md` 를 레포 파일에서 읽어 따랐다(Step 1 현재 상태 읽기 → Step 2 격차 분석 7 축 → Step 3 우선순위
「게이트 생존 > 근거 정합 > 강도 정합 > 중복 > 문구」 · 한 사이클 1 ~ 2 관심사 → Step 4 회귀 검증 → Step 5 보고 → Step 6 커밋). Step 2 격차 표:

| # | 축 | 격차 | 근거 | 제안 |
| --- | --- | --- | --- | --- |
| 1 | 게이트 생존 | `core-naming.md` §8 G-1 · G-2 · G-5 · G-6 이 표 칸에 있어 붙여 넣으면 죽는다 | 봉인 전 실측(bash · zsh) | **이번** — 코드 블록으로 옮긴다 (SC-01 · RE-02) |
| 2 | 게이트 생존 | 확장자 변수를 한 문자열로 두면 확장자 둘에서 zsh 0 줄 — 세 자리 | 봉인 전 실측 | **이번** — 배열로 (SC-02) |
| 3 | 근거 정합 | 실측 피드백 F19 가 규칙에 없다 | 처리 배정표 · 세션 `8fa13c90` | **이번** — K-11 · 원칙 9 · 평가 사례 (SK-01 ~ SK-04) |
| 4 | 근거 정합 | `etc_seq=663` 이름표가 내용보다 넓다 — 원칙 1 · 2 · 5 · 8 이 근거로 든다 | 근거 §2-3 | 다음 사이클 |
| 5 | 강도 정합 | C-06 MUST 대 출처 PREFER | 근거 §2-2 | 다음 사이클 (기록만) |
| 6 | 축 라벨 | 코어 문서에 어댑터 · 로케일 내용 — `core-comment.md` §6 주의 사항의 한국어 멀티바이트 한 줄 | 읽기 | 판정 경계 안내라 그대로 |
| 7 | 중복 | `locale-korean.md` §2 표 grep 열과 §8 블록이 같은 패턴 — 표 칸은 `\|` | 읽기 | 실행 정본은 §8 블록(살아 있음). 다음 사이클 메모 |
| 8 | 중복 | K-11 과 K-05 가 같은 예(「표시훅」 의 「훅」)를 잡을 수 있다 | 근거 §2-1 | **이번** — 겹침을 판정 문장에 적는다 (SK-01 · SK-04) |
| 9 | 트리거 | 새 킷 셋(api · howto · 기타)과 배타성 | V4 OK · description 안 바꿈 | 해당 없음 |
| 10 | 상한 | SKILL.md 108 · 108 · 111 줄 · `references/` 1 단 · 스킬 셋 | `wc -l` · `find` | 해당 없음 |

`.claude/skills/tone-kaizen/SKILL.md` Step 1 이 「`tone-kit/templates/*.md` 8종」 이라 적었지만 실제 6 개다 — 레포 전용 파일이라 이 Phase 범위 밖(ER-03 넘김).

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 3 — 런타임 규칙 파일(`references/` 넷) · 평가 사례 · 리서치 문서 셋 |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — 스킬 셋이 런타임에 읽는 규칙표에 K-11 이 생기고, 완료 게이트 블록의 모양(표 칸 → 코드 블록, 문자열 → 배열)이 바뀐다 |
| 소비면 존재 | 이 형태를 받아 쓰는 반대편이 있는가 | 예 — 아래 Counterpart 표 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 게이트 명령 여덟과 주석 게이트 여덟의 인자 모양이 바뀐다 |

넷 가운데 셋이 「예」 이고 공개 형태 변경과 소비면이 둘 다 「예」 라 **복잡**이다. Step 2.5 Counterpart 표를 넣는다. 기능 조건은 15 개다 — 복잡 9 ~ 20 안이다
(SKILL.md Step 6.2 둘째 명령으로 이 파일을 세면 15).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 섹션 제목과 접두 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 선별, message 원문 그대로. AP-02(force push)는 이 Phase 가 밀어 넣지 않고, AP-04(frontmatter name)는 SKILL.md · agents 를 안 고쳐서 뺀다(AR-02 `skills_same=1`) |

### 1.4 편집 전 감사 (실제로 읽은 줄 — 시작 커밋 `499cc12` 판)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `tone-kit/references/locale-korean.md` | 전체 `:1-181` (`:42-55` 규칙표 K-01 ~ K-10 · `:83-89` §4 · `:139-159` §8 · `:161-170` §9 · `:172-180` §10) | K-11 없음. §4 제목은 목차 `:34` 와 이어져 있다 | SK-01 · SK-02 · ER-04 |
| `tone-kit/references/sources.md` | 전체 `:1-164` (`:15-21` 상태 표기 · `:80-92` 로케일 표) | K-11 근거 행 없음. `확인됨` 정의가 2026-08-28 한 날짜 | SK-02 |
| `tone-kit/references/core-naming.md` | `:1-40` (근거 등급 · 규칙표) · `:206-251` (§8 — `:218-223` 표 칸 명령, `:213` 문자열 `INC`, `:243-251` 오탐 triage) | 죽은 게이트 넷 · 확장자 문자열 | SC-01 · SC-02 · RE-02 |
| `tone-kit/references/core-comment.md` | 전체 `:1-175` (`:19` C-06 MUST · `:112-147` §6 — `:129` `X='--include=*.{EXT}'`, `:130-137` 따옴표 없는 `$X`) | 확장자 문자열. C-06 강도 초과(근거 §2-2) | SC-02 · C-06 은 ER-03 넘김 |
| `tone-kit/evals/evals.json` | 전체 `:1-44` (사례 셋) | K-11 사례 없음 | SK-03 |
| `docs/tone/korean-technical-writing.md` | `:1-55` (잡는 것 · 원칙 1) · `:55-180` (원칙 2 ~ 4) · `:180-370` (원칙 4 ~ 8 · 규칙 강도 · 수치 · 안티패턴 · Gotchas) | 원칙 9 없음. 원칙 1 · 2 · 5 · 8 출처가 `etc_seq=663` | SK-04 · 663 은 ER-03 넘김 |
| `docs/tone/research-log.md` | 전체 `:1-33` | 2026-08-31 한 기록뿐 | SK-05 |
| `docs/tone/overview.md` | `:1-30` · `:155-219` (`:194-202` 게이트 예시 — 문자열 `INC`) | 확장자 문자열 | SC-02 |
| `tone-kit/skills/tone-guide/SKILL.md` (읽기만) | 전체 `:1-111` (`:55-66` Step 3 조건부 로드 · `:73-89` Step 5 전수 대조) | 규칙표를 통째로 읽는다 — K-11 을 따로 이을 필요 없음 | 그대로 (AR-02 `skills_same=1`) |
| `tone-kit/skills/tone-campaign/SKILL.md` · `tone-scaffold/SKILL.md` (읽기만) | `grep -n 'locale-korean\|K-[0-9]'` — `:46` · `:105` · `:48` · `:101` | 파일을 통째로 읽고 K ID 를 나열하지 않는다 | 그대로 |
| `tone-kit/references/adapter-dart-flutter.md` (읽기만) | `:17-31` (슬롯 표) · `:237-266` (§4 게이트 열 — 코드 블록) | 게이트는 살아 있다(봉인 전 실측 10/10) | 그대로 |
| `tone-kit/README.md` (읽기만) | `:1-40` (강도 3 등급 정의 `:13-17`) | 관측 컨벤션 = 공개 근거 없음 · 코퍼스 실측만 — K-11 은 영어권 근거가 있지만 한국어 쪽은 세션 관찰뿐이라 이 정의에 맞춘 문장을 둔다 | SK-02 · SK-04 문장 |
| `.claude/skills/tone-kaizen/SKILL.md` (읽기만) | 전체 `:1-102` | Step 1 「templates 8종」 — 실제 6 | ER-03 넘김 |

구현 후보가 둘 이상이었던 곳의 선택:

- **K-11 을 어디에.** 새 절 대 §4 끝 문단. **§4 끝 문단.** 제안 원문이 §4 제목을 바꾸지 말라고 했다 — 바꾸면 목차 `:34` · 규칙표 K-05 `:50` · §4 제목 `:83` 과 문서 사이트
  거울 페이지까지 고쳐야 한다. 규칙표 행은 `(§4 끝)` 으로 가리킨다
- **판정어.** 제안 원문 「사전에 없는 한국어 합성어」 대 근거 권장안 2 「읽는 사람이 뜻을 짐작할 수 없는, 글쓴이가 새로 붙인 이름」. **뒤쪽.** 한글 맞춤법 제50항 해설이 사전에 없는
  전문 용어를 정당하게 본다 — 앞쪽이면 문제가 없는 전문 용어까지 걸린다(SK-01 `dict_word=0`)
- **평가 사례의 예.** 「표시훅」 대 음역이 안 섞인 새 합성어. **음역이 안 섞인 「차례칸」.** 「훅」 이 음역이라 K-05(SHOULD)로 판정해도 틀리지 않게 된다(근거 권장안 4).
  「표시훅」 은 규칙 문단의 실측 사례와 겹침 설명에만 둔다
- **죽은 게이트를 어떻게.** 표 칸에 이스케이프 없는 다른 표기 대 명령을 코드 블록으로. **코드 블록.** 표 칸 안에서 `|` 를 쓰려면 이스케이프가 필요해 모양을 바꿔도 같은 함정이 남는다.
  표는 ID · 규칙 · 잡는 것만 갖고, 정규식은 시작 커밋 표 칸의 것을 글자 그대로 옮긴다(RE-02)
- **확장자 여럿.** 경고 한 줄 대 배열. **배열.** `"${INC[@]}"` 는 bash 3.2 · bash 5 · zsh 에서 같게 펼쳐진다(봉인 전 실측). 경고 문장은 읽지 않으면 그만이다.
  세 자리(`core-naming.md` §8 · `core-comment.md` §6 · 개요 예시)를 한 번에 바꾼다 — 한 곳만 바꾸면 같은 함정이 남은 자리에서 다시 터진다
- **리서치 문서.** 원칙 9 를 더할지. **더한다.** K-01 ~ K-08 이 원칙 1 ~ 8 과 짝이고, 킷 파일 머리(`locale-korean.md:12`)가 근거는 원칙 문서에 있다고 말한다

### Counterpart — 바뀌는 형태를 받아 쓰는 반대편

| 파일 | 읽는 것 | 이번 처리 |
| --- | --- | --- |
| `tone-kit/skills/tone-guide/SKILL.md` Step 3 · 5 · `tone-campaign` · `tone-scaffold` | `locale-korean.md` 규칙표 전체 · `core-naming.md` §8 · `core-comment.md` §6 | 그대로 — 파일을 통째로 읽고 K ID 나 명령 줄 수를 적지 않는다(AR-02 `skills_same=1`) |
| `tone-kit/evals/evals.json` | tone-guide 동작 | 반영 — 사례 4 (SK-03) |
| `docs/tone/korean-technical-writing.md` · `docs/tone/overview.md` | 한국어 원칙 · 게이트 예시 | 반영 — SK-04 · SC-02 |
| `docs/tone-kit/korean-technical-writing.html` · `docs/tone-kit/overview.html` | 리서치 문서 거울 | Final F2 (ER-03). `scripts/detect-docs-drift.py` 가 `docs/tone/` · `tone-kit/references/` 를 `docs/tone-kit/` 로 잇는다 |
| `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md:230` | 필수 출처 7 번 이름 「국립국어원 공공언어」 | 범위 밖 — ER-03 넘김 |

### 개선안 초안

정확한 내용은 스크래치 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p15d/mock.py`
(sha256 앞 16 자리 `42dde3050ac3accf`)가 쓰는 여덟 파일 그대로다(`python3 mock.py <트리>`). mock.py 는 먼저 전부 확인하고 나서 쓴다 — 여덟 파일이 시작 커밋 판(sha256)과 같고
바꿀 글이 파일마다 정확히 한 번 나와야 하며, 하나라도 어긋나면 아무것도 쓰지 않고 `MOCK_FAIL` · 종료 코드 3 이다. 시작 커밋 판을 푼 새 사본에서 `mock applied 8` ·
종료 코드 0, 두 번째 실행은 `MOCK_FAIL start-sha …` · 종료 코드 3 을 확인했다. BUILD 는 작업 폴더에서 `python3 mock.py .` 을 돌려 `mock applied 8` 을 확인한다. 요지:

- `locale-korean.md` — 규칙표 K-11 행, §4 끝 K-11 문단(한 문단 + 목록 넷), §10 출처 세 줄 + 세션 관찰 한 줄
- `sources.md` — 상태 표기 `확인됨` 정의에 날짜 괄호 규칙, 로케일 표 세 행(`확인됨 (2026-09-24)`), K-11 이 관측 컨벤션인 까닭 한 문단
- `core-naming.md` §8 — 표는 ID · 대응 규칙 · 잡는 것, 명령 여덟은 코드 블록 하나로(G-1 ~ G-8 차례), `INC` 는 배열, 표 칸 함정 한 문장
- `core-comment.md` §6 — `X` 를 배열로, 여덟 줄의 `$X` 를 `"${X[@]}"` 로
- `evals.json` — 사례 4 (tone-guide · K-11)
- `docs/tone/korean-technical-writing.md` — 잡는 것 한 줄, 원칙 9, 안티패턴 한 행, `last_updated` · `docs/tone/research-log.md` — 이 사이클 기록 한 절, `last_updated` ·
  `docs/tone/overview.md` — 게이트 예시 배열, `last_updated`

## 범위 경계

- 이 Phase 시작 HEAD: `499cc1289f0f5ae5649da601515725f49f4f1096`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p15-tone-kit.md` 의 `end_sha:`
  마지막 값이다. 여러 Phase(13 · 14 · 16 · 17)가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 여덟이다 — 아래 블록이 그 목록이다(`harness/README.md` §커밋 안전 훅 이 정한 범위 선언 자리). `.harness/` 쪽은 이 계약 · 개정 파일 · QA 피드백 ·
  `.harness/.meta/kaizen-0924/phase15-notes.md` · `.harness/.meta/kaizen-0924/phase15-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-01 셋째 값 `verify_seal` 로 잰다.
  AR-01 다섯째 값이 이 블록과 측정 공통 정의의 `FILES` 가 같은지 잰다

```text
# sprint-scope
tone-kit/references/locale-korean.md
tone-kit/references/sources.md
tone-kit/references/core-naming.md
tone-kit/references/core-comment.md
tone-kit/evals/evals.json
docs/tone/korean-technical-writing.md
docs/tone/research-log.md
docs/tone/overview.md
.harness/
```

- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p15-tone-kit` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-01 · ER-03 · DG-06 · `m NA` 가 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-01 첫째 값과 ER-03 마지막 값은 경로로 직접 센다.
  FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로
  `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 둘이다 — `tone-kit/` 다섯 파일 한 커밋, `docs/tone/` 세 파일 한 커밋. 각각 `git add -- <파일…> && git commit -o -- <파일…>` 로 그 파일만 싣는다.
  둘 다 `harness/skills/` 를 안 건드려 `validate-post-kaizen.py` scope-isolation 에 걸리지 않는다
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: `## 1. 규칙표` · `## 4. 외래어 3원칙` · `## 8. 완료 전 대조 grep` · `## 9. 자기모순 검사` · `## 10. 출처`
  (locale-korean) · `## 로케일 — 한국어 기술 문체` (sources) · `## 8. 완료 전 대조 grep` (core-naming) · `## 6. 완료 전 대조 grep` (core-comment) · `### 8. 용어 번역표는 프로젝트가 소유한다` ·
  `### 9. 새 이름을 만들지 않는다` · `## 원칙` · `## 규칙 강도` (korean-technical-writing) · `## 2026-08-31 — 초기 이관 리서치` · `## 2026-09-24 — 카이젠 Phase 15 근거 조회` (research-log) ·
  `## 완료 게이트는 이렇게 생겼다` (overview) · 표 행 머리 `| G-` · 확장자 정의 줄 머리 `INC=(` · `D={DIR}; X=(` · `SRC=lib; INC=(`. 이름이 바뀌면 `sect` · `addts` 가
  빈 글을 내 값이 0 이 된다 — FAIL 쪽으로 틀린다
- 공유 파일(`.claude-plugin/marketplace.json` · `tone-kit/.claude-plugin/plugin.json` 버전 · 루트 `README.md` · 루트 `CLAUDE.md` · `docs/` HTML · 처리 배정표 · 감사 로그 ·
  실패 횟수 파일 · `.github/workflows/ci.yml` · `.harness/stale-values.yaml`)과 다른 Phase · 레포 전용 파일(`harness/` · `scripts/` · `.claude/skills/`)과 이 킷의 나머지
  (`tone-kit/skills/` · `tone-kit/templates/` · `tone-kit/README.md` · 나머지 `references/` 다섯)는 건드리지 않는다 — ER-03 마지막 값 · AR-01 둘째 줄.
  README 의 AUTO 구간은 스킬 frontmatter 를 읽는데 스킬을 안 고친다. 문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 harness 파일은 없다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase15-review.md` — 1 회차 `VERDICT: CHANGES`(고칠 것 둘 — ER-01 근거 파일을
  시작 커밋 판에서 읽기 · 모의 편집의 새 이름 「대안 기호」 와 G-6 「0 건」 설명, 참고 여섯)는 DRAFT 가 고칠 것 둘과 참고 1 · 5 · 6 을 반영했다(참고 2 · 3 · 4 는 1 회차가
  그대로 둬도 된다고 했다 — 4 는 notes 다음 사이클 메모로 넘긴다). 2 회차가 반영을 확인하고 `VERDICT: APPROVE` 를 냈다 — 이 계약은 그 판정 뒤에 봉인했다(BUILD, 2026-09-25).
  봉인 전에 BUILD 가 고친 곳은 이 줄과 2 회차 참고 1 의 「앞 Phase notes 열두 개」 → 「열세 개」(서술 줄 둘)뿐이다
- 오라클 한계: K-11 이 실제 대화 · 주석에서 새 이름을 줄이는지는 LLM 동작이라 결정론 측정이 없다 — 조건은 규칙 문장 · 근거 · 평가 사례가 정해진 자리에 정해진 글로
  있는지(SK-01 ~ SK-05)와 평가 사례의 구조 검사(DG-05 `run-evals.py`)까지만 건다. 평가 사례를 실제 모델로 돌려 보는 일은 이 Phase 몫이 아니다
- 오라클 해소: SK-01 ~ SK-05 — 산출물이 문서 문장 자체라 정해진 절에 정해진 문장이 있는지가 판정이다. `sect` 가 코드 펜스를 건너뛰고 절을 자르고, `toks` 가 토큰이 든 줄을 센다.
  시작 커밋 판에서 새 문장 0 을 확인했고, 더한 줄을 하나씩 지운 사본에서 조건 값이 바뀌는지 빈 줄이 아닌 더한 줄 전부에 돌려 확인했다 — 안 바뀐 줄은 조건이 요구하지 않는 줄뿐이다(`회귀 게이트` 절 `지운 사본`)
- 오라클 해소: SC-01 · SC-02 — 게이트 블록을 문서에서 그대로 뽑아 fixture 에서 bash · zsh 로 돌린 출력이다. SC-01 은 손으로 센 답(여덟 줄), SC-02 는 둘째 확장자 파일을
  찾았는지다. 시작 커밋 판이 음성 대조다
- 오라클 해소: ER-01 · ER-02 · AP-01 · DG-02 · RE-02 — 편집 전 판과 파일마다 비교한 계산이다. 각각 양성 대조가 붙어 있다
- 오라클 해소: ER-03 · AR-01 · DG-06 · `m NA` — 커밋 기록과 봉인 검증 함수를 실제로 돌린 출력이다. 예행 저장소 변형 넷이 양성 대조다
- 커버리지 해소: SK-01 ~ SK-05 · SC-01 · SC-02 · AR-02 · RE-02 — 산문의 파일 이름은 측정 `m <조건 ID>` 가 공통 정의의 변수(`$LK` · `$SRCS` · `$CN` · `$CC` · `$EV` ·
  `$KTW` · `$RL` · `$OV`)로 연다(파일과 변수의 대응은 `common.sh`). 문장 조각은 `m.sh` 의 같은 ID 갈래에 글자 그대로 있다. SC-01 의 답 여덟 줄은 `common.sh` 의
  `NAMING_ANSWER` 다. `tone-kit/skills` · `tone-kit/templates` 는 AR-02 `git diff --quiet` 의 인자다
- 커버리지 해소: ER-01 · ER-03 — `.harness/.meta/kaizen-0924/phase15-notes.md` · `.harness/.meta/evidence/phase15.md` 는 공통 정의의 `$NOTES` · `$EVID` 다. ER-03 의 넘김 문자열과
  공유 경로는 `m.sh` `ER-03)` 갈래 `toks` · `not_other` 의 인자다
- 커버리지 해소: AR-01 — `tone-kit/` · `docs/tone/` 는 `unsigned_on` 의 인자, `.harness/` 는 `scope` 블록 줄과 `verify_seal` 이 도는 폴더다
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 경고(markdownlint MD036 등)는 범위 밖이다 — DG-02 는 파일마다 규칙별 경고 수가 편집 전보다 는 규칙만 잰다(더한 줄만 세면 옆 줄에 붙는 MD022 · MD024 · MD032 를 놓친다 — 러닝북)
- notes 틀: 스크래치 `p15d/notes-mock.md` 가 ER-03 이 요구하는 글을 다 담은 예다(예행 저장소가 이 파일로 ER-01 · ER-03 을 통과했다). BUILD 는 이 틀을 채워 쓴다
- notes 에 함께 적는다(조건으로는 재지 않는 것 포함): 카이젠 스킬 Step 2 격차 표 · Step 5 보고 형식의 한 단락 · 「넘기는 것」 — `docs/tone-kit/korean-technical-writing.html` ·
  `docs/tone-kit/overview.html`(Final F2), `.claude/skills/tone-kaizen/SKILL.md`(「templates 8종」 → 6), `.claude/skills/kaizen-orchestrator/references/phase-research-templates.md`(7 번 출처 이름),
  `tone-kit/.claude-plugin/plugin.json`(버전 — Final) · 「다음 사이클 메모」 — C-06, `etc_seq=663` 이름표와 원칙 1 · 2 · 5 · 8 근거, 문서 예시 `__`(린트 `unnecessary_underscores`),
  제스처 콜백 58 개 기준 버전(3.47.5 에서도 58), go_router 예제 링크, 위키 `Style-guide-for-Flutter-repo` 이전, `material_ui` 분리, `locale-korean.md` §2 표의 grep 열(`\|`),
  `sources.md` 의 「위 표의 마지막 세 행」 문장(행이 늘면 틀린다 — 세 출처 이름으로 바꾼다)
- 측정 코드(`common.sh` · `m.sh` · `lintcmp.sh`)는 서술 절에 있어 봉인 지문이 덮지 않는다. QA 는 봉인 커밋 판과 끝 판 계약의 `## 회귀 게이트` 절을
  `diff` 해 0 줄인지부터 본다 — 봉인 뒤에 측정을 바꿨으면 그 조건 값은 믿지 않는다(검토 결과 참고 5)
- 사용자가 할 일: 없음

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 `common.sh` 와 `m.sh` 를 차례로 `.` 으로 읽은 **bash** 셸에서 돈다 — `common.sh` 는 bash 가 아니면 `NOT_BASH` 를 찍고 종료 코드 2 로 끝난다
(Claude Code 의 zsh 는 따옴표 없는 변수를 쪼개지 않고 `grep` 을 다른 검색 프로그램으로 바꿔 부른다 — Phase 5 실측). 게이트 블록을 zsh 로 돌리는 측정(SC-01 · SC-02 · ER-04)은
`m` 안에서 `zsh <파일>` 로 따로 띄운다 — 비대화형 zsh 에는 그 바꿔 부르기가 없다(봉인 전 실측: `zsh -c 'type grep'` → `grep is /usr/bin/grep`).
`m` 은 도우미 함수와 두 판 폴더가 없으면 `HELPER_MISSING` · `SNAPSHOT_MISSING` 을 내고 멈춘다 — 그래서 조건마다 `type m` 하나로 정의 확인을 대신한다. 세 블록을 각 블록 첫
`#` 주석 줄(셔뱅 다음)의 이름 그대로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다. `END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다.
`lintcmp.sh` 옆에는 `node_modules` 를 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측(2026-09-25): 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
그 밖의 준비 단계 실측(2026-09-25): `command -v zsh` → `/bin/zsh` · `/bin/bash --version` 3.2.57 · `bash` 5 (Homebrew) · `/usr/bin/grep --version` → BSD grep 2.6.0 ·
`python3` 있음 · `shasum` 있음. 측정은 `R` 이 비면 작업 폴더에서 돈다 — 예행 저장소를 잴 때만 `R` 에 그 경로를 넣는다. 두 판을 `${TMPDIR:-/tmp}/p15m.XXXXXX` 에 푸니 `TMPDIR` 를
스크래치 폴더로 두고 읽는다. 부르는 모양: `K=<도우미 폴더> bash -c '. "$K/common.sh"; . "$K/m.sh"; type m >/dev/null || exit 2; m SK-01'`.
음성 대조(시작 커밋 판)는 같은 셸에서 `V=B m <조건 ID>` 로 돈다 — 같은 측정을 `$T/B` 에 돌린다(SK-01 ~ SK-05 · SC-01 · SC-02 · AR-02 · AP-03).

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
[ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — bash -c 안에서 다시 읽는다"; exit 2; }
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다
cd "${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2
B=499cc1289f0f5ae5649da601515725f49f4f1096                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p15-tone-kit'
CF=.harness/sprint-contract-kaizen-0924-p15-tone-kit.md
AM=.harness/sprint-amendments-kaizen-0924-p15-tone-kit.md
NOTES=.harness/.meta/kaizen-0924/phase15-notes.md
EVID=.harness/.meta/evidence/phase15.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
LK=tone-kit/references/locale-korean.md
SRCS=tone-kit/references/sources.md
CN=tone-kit/references/core-naming.md
CC=tone-kit/references/core-comment.md
EV=tone-kit/evals/evals.json
KTW=docs/tone/korean-technical-writing.md
RL=docs/tone/research-log.md
OV=docs/tone/overview.md
FILES=("$LK" "$SRCS" "$CN" "$CC" "$EV" "$KTW" "$RL" "$OV")
MDF=("$LK" "$SRCS" "$CN" "$CC" "$KTW" "$RL" "$OV")
MS_URL='https://github.com/MicrosoftDocs/microsoft-style-guide/blob/main/styleguide/word-choice/use-technical-terms-carefully.md'
GG_URL='https://developers.google.com/style/jargon'
KN_URL='https://korean.go.kr/kornorms/regltn/regltnView.do?regltn_code=0001'
T=$(mktemp -d "${TMPDIR:-/tmp}/p15m.XXXXXX") || exit 2; mkdir -p "$T/B" "$T/E"
trap 'rm -rf "$T"' EXIT
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
# 풀기가 도중에 끊기면 0 을 기대하는 값이 통과로 읽힌다 — 여기서 멈춘다
git archive "$B" | tar -x -C "$T/B" && git archive "$END" | tar -x -C "$T/E" || { echo "SNAPSHOT_FAIL — 측정을 멈춘다"; exit 2; }
for f in "${FILES[@]}"; do [ -s "$T/B/$f" ] && [ -s "$T/E/$f" ] || { echo "SNAPSHOT_FAIL $f"; exit 2; }; done
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
# para <파일> <줄 앞부분> — 그 앞부분으로 시작하는 줄부터 다음 제목 전까지 (§4 끝 K-11 문단 · 목록)
para() { awk -v p="$2" '!f && index($0, p) == 1 { f = 1 } f && /^#+ / { exit } f' "$1"; }
# notrail — 끝의 빈 줄을 뗀다 (절 뒤에 새 절을 붙이면 옛 절 끝에 빈 줄이 하나 생긴다)
notrail() { awk 'NF { for (; b > 0; b--) print ""; print; next } { b++ }'; }
# toks <글> <토큰…> — 토큰마다 글 안에서 그 토큰이 든 줄 수
toks() { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
# bashblocks <글> — 글 안의 ```bash 코드 블록 본문을 차례로 이어 낸다
bashblocks() { printf '%s\n' "$1" | awk '/^```bash$/ { b = 1; next } b && /^```$/ { b = 0; next } b'; }
# tablecells <글> — `| G-` 로 시작하는 표 행
tablecells() { printf '%s\n' "$1" | grep -E '^\| G-[0-9]+ \|'; }
# barefence <파일> — 언어 힌트 없는 여는 펜스 수 (여닫기를 번갈아 센다)
barefence() { awk '/^[[:space:]]*```/{ if (!o) { o = 1; if ($0 ~ /^[[:space:]]*```[[:space:]]*$/) n++ } else o = 0 } END{print n+0}' "$1"; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
added() { for f in "${FILES[@]}"; do git diff --no-index -U0 "$T/B/$f" "$T/E/$f"; done | grep '^+' | grep -v '^+++'; }
# fixture <폴더> — 게이트 시험 입력. src 는 이름 게이트(core-naming §8)용, src2 는 주석 게이트(core-comment §6)용
fixture() { mkdir -p "$1/src" "$1/src2"
  printf '%s\n' 'final effectiveColor = a;' 'class UserRow extends StatelessWidget {}' 'class SettingsBar extends StatelessWidget {}' \
    'class AppBarX extends StatelessWidget {}' 'class ProfileBox extends StatelessWidget {}' 'class MessageBoxY {}' \
    'class BlueButton extends StatelessWidget {}' 'final x = 1;' 'for (var i = 0; i < 3; i++) {}' 'class PlayerCard {}' 'class PlayerTile {}' > "$1/src/pos.dart"
  : > "$1/src/utils.dart"
  printf '%s\n' 'final effectiveTs = 1;' > "$1/src/extra.ts"
  for f in a.dart b.ts; do printf '%s\n' '// ------------------------------' '// 노드 14644:26672 버튼' '// Color/Display Field/display-label' \
    '// from-[#111] to-[#181818]' '// 자동 생성 파일' 'const w = 440; // 440 - 40' '// 상태' > "$1/src2/$f"; done; }
# addts <변수 이름> — 확장자 정의 줄 뒤에, 문서가 쓰는 모양 그대로 두 번째 확장자(.ts)를 더한다 (배열이면 원소, 문자열이면 이어 붙이기)
addts() { awk -v v="$1" -v q="'" -v dq='"' '
  { print }
  !d && ($0 ~ ("^" v "=\\(") || $0 ~ ("; " v "=\\(")) { print v "+=(--include=" q "*.ts" q ")"; d = 1; next }
  !d && ($0 ~ ("^" v "=" q) || $0 ~ ("; " v "=" q) || $0 ~ ("^" v "=" dq) || $0 ~ ("; " v "=" dq)) { print v "=" dq "$" v " --include=*.ts" dq; d = 1 }'; }
# runin <셸> <폴더> <스크립트 글> — 그 폴더에서 스크립트를 그 셸로 돌린 표준 출력 (stderr 는 버린다)
runin() { ( cd "$2" && printf '%s\n' "$3" > "$T/run.$$.sh" && "$1" "$T/run.$$.sh" 2>/dev/null ); }
mine() { git log --format= --name-only "${1}..${2}" --grep="^${3}\$" | grep . | LC_ALL=C sort -u; }
unsigned_on() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do git log -1 --format=%B "$_c" | grep -qxF "$_s" || echo "$_c"; done; }
# not_other <base> <상한> <서명> <경로…> — 경로를 건드린 구간 안 커밋 가운데 다른 Phase 서명이 없는 커밋 (0 줄이어야 한다)
not_other() { _b=${1}; _u=${2}; _s=${3}; shift 3
  git log --format=%H "${_b}..${_u}" -- "$@" | while read -r _c; do
    _m=$(git log -1 --format=%B "$_c")
    if printf '%s\n' "$_m" | grep -qE '^Kaizen-Phase: ' && ! printf '%s\n' "$_m" | grep -qxF "$_s"; then continue; fi
    echo "$_c"; done; }
my() { mine "$B" "$END" "$SIG"; }
# scope <계약> — `## 범위 경계` 절 안, 첫 줄이 `# sprint-scope` 인 text 블록의 경로 줄
scope() { awk '/^## /{s=$0} s ~ /^## 범위 경계/ && /^```text$/{b=1; n=0; next} b && /^```$/{b=0; next} b{n++; if (n==1 && $0 != "# sprint-scope") b=0; else if (n>1) print}' "$1"; }
fm_get() { awk -v k="^$2:[[:space:]]*" 'NR==1 && /^---[[:space:]]*$/ { fm=1; next } fm && /^---[[:space:]]*$/ { exit } fm && $0 ~ k { sub(k, "", $0); print; exit }' "$1" | sed -e "s/[[:space:]]*$//" -e "s/^['\"]//" -e "s/['\"]\$//"; }
sha256_16() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; else python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())'; fi | cut -c1-16; }
contract_digest() { grep -E '^- \[[ x]\] [A-Z]{2,}-[0-9]{2}' "$1" | sed -E 's/^- \[[ x]\]/- [ ]/' | sha256_16; }
verify_seal() { rec=$(fm_get "$1" conditions_digest); rec=${rec#sha256:}; if [ -z "$rec" ]; then echo "SEAL_ABSENT $1"; return 0; fi
  act=$(contract_digest "$1"); if [ "$rec" = "$act" ]; then echo "SEAL_OK $1"; else echo "SEAL_BROKEN $1 recorded=$rec actual=$act"; fi; }
K02='(을|를) ?(처리|관리)(합니다|한다)|에 대해서?|하도록 (합니다|한다)|에 의(해|하여)|되어 있(는 경우|을 때)|(표시|적용|호출|생성|반환)(됩니다|된다)'
NAMES='fit-?pal|fit_pal|flutter[-_]playwright|playwright-mcp|chrome-devtools-mcp'
# SC-01 의 손으로 센 답 — fixture 의 src/pos.dart · src/utils.dart 에 core-naming §8 블록을 돌린 출력 (G-1 ~ G-8 차례)
NAMING_ANSWER='src/pos.dart:1:final effectiveColor = a;
src/pos.dart:2:class UserRow extends StatelessWidget {}
src/pos.dart:3:class SettingsBar extends StatelessWidget {}
src/pos.dart:5:class ProfileBox extends StatelessWidget {}
src/pos.dart:7:class BlueButton extends StatelessWidget {}
src/pos.dart:8:final x = 1;
src/utils.dart
Player -> Card Tile'
```

```bash
# m.sh — 조건마다 재는 값을 한 줄씩 낸다. common.sh 를 읽은 bash 에서 `m <조건 ID>` 로 부른다
m() {
  local E=$T/E S f fn o L X ln n
  # 도우미가 하나라도 없으면 grep -c 가 조용히 0 을 낸다 — 멈춘다
  for fn in sect para notrail toks bashblocks tablecells barefence url added fixture addts runin mine unsigned_on not_other my scope fm_get verify_seal; do
    type "$fn" >/dev/null 2>&1 || { echo "HELPER_MISSING $fn"; return 2; }; done
  [ -n "${T:-}" ] && [ -d "$T/B" ] && [ -d "$E" ] || { echo "SNAPSHOT_MISSING"; return 2; }
  L=$T/${V:-E}   # V=B 로 부르면 같은 측정을 시작 커밋 판에 돌린다 (음성 대조)
  case "$1" in
  SK-01)  # locale-korean — K-11 행 · 규칙표 차례 · §4 끝 문단 · §4 제목 그대로
    echo "row=$(grep -cxF '| K-11 | 글쓴이가 새로 붙인 이름(합성어·비유)으로 대상을 부르지 않는다. 원래 이름을 그대로 쓰거나 하는 일을 문장으로 풀어 쓴다 (§4 끝) | 관측 컨벤션 |' "$L/$LK") ids=$(sect "$L/$LK" '## 1. 규칙표' | grep -oE '^\| K-[0-9]+ ' | tr -dc '0-9\n' | awk '{ok = ok && ($1 + 0 == NR)} BEGIN{ok = 1} END{printf "%d/%d", ok, NR}')"
    S=$(sect "$L/$LK" '## 4. 외래어 3원칙')
    toks "$S" '**새 이름을 만들지 않는다 (K-11).** 대상을 부를 이름이 이미 있으면 그 이름을 쓴다 — 파일 이름, 함수·설정 키 이름, 공식 API 이름.' \
      '이름이 없으면 하는 일을 문장으로 풀어 쓴다.' \
      '- 판정 기준은 사전에 실렸는지가 아니라 **처음 읽는 사람이 뜻을 짐작할 수 있는가** 다.' \
      '한글 맞춤법 제50항 해설은 사전에 없는 전문 용어도 정당한 말로 다룬다.' \
      '- 새 이름이 꼭 필요하면 처음 나올 때 괄호로 뜻을 붙인다.' \
      '- 음역이 섞인 새 이름(`표시훅` 의 `훅`)은 3원칙의 음역 금지(K-05)에도 걸릴 수 있다.' \
      '정착 외래어인지는 §6 표로 판정하고, 둘 다 걸리면 두 규칙을 함께 적되 강도는 규칙마다 그대로 인용한다.' \
      '- 새 이름은 모양이 정해져 있지 않아 §8 에 grep 을 두지 않는다. 완료 전 전수 대조에서 규칙표의 K-11 행을 읽어 판정한다.'
    echo "title=$(grep -cx '## 4. 외래어 3원칙' "$L/$LK") toc=$(grep -cxF '4. [외래어 3원칙](#4-외래어-3원칙)' "$L/$LK") dict_word=$(grep -cF '사전에 없는 한국어 합성어' "$L/$LK") sect8_k11=$(sect "$L/$LK" '## 8. 완료 전 대조 grep' | grep -c 'K-11')" ;;
  SK-02)  # K-11 근거 — locale §10 · sources.md 로케일 표 · 상태 표기
    S=$(sect "$L/$LK" '## 10. 출처')
    toks "$S" "- [Microsoft Style Guide — Use technical terms carefully]($MS_URL) (K-11)" "- [Google developer documentation style guide — Jargon]($GG_URL) (K-11)" \
      "- [한글 맞춤법 — 제50항 해설]($KN_URL) (K-11 판정 기준)" '- 세션 관찰 (2026-09-19) — 대화에서 새 합성어 1건을 사용자가 알아듣지 못해 되물었다 (K-11)'
    S=$(sect "$L/$SRCS" '## 로케일 — 한국어 기술 문체')
    toks "$S" "| Microsoft Style Guide — Use technical terms carefully | <$MS_URL> | 확인됨 (2026-09-24) |" "| Google 개발자 문서 스타일 가이드 — Jargon | <$GG_URL> | 확인됨 (2026-09-24) |" \
      "| 한글 맞춤법 (제2항 · 제50항 해설) | <$KN_URL> | 확인됨 (2026-09-24) |" 'K-11(새 이름을 만들지 않는다)의 근거는 위 표의 마지막 세 행이다.' \
      '그래서 K-11 은 관측 컨벤션이고 판정 기준이 사전 등재가 아니다.' 'Microsoft 항목은 공개 저장소 판(파일 날짜 2018)을 읽었고, Learn 페이지 본문과 같은지는 확인하지 않았다.'
    echo "status_row=$(grep -cxF '| 확인됨 | 2026-08-28 에 접근성과 인용 문구를 확인. 괄호에 날짜가 있으면 그날 확인 |' "$L/$SRCS")" ;;
  SK-03)  # evals.json — 사례 넷, 넷째가 K-11 사례, 앞 셋은 시작 커밋 판 그대로
    python3 - "$T/B/$EV" "$L/$EV" <<'PY'
import json, sys
try:
    b = json.load(open(sys.argv[1], encoding="utf-8")); e = json.load(open(sys.argv[2], encoding="utf-8"))
except Exception as x:
    print("JSON_FAIL", type(x).__name__); sys.exit(0)
ev = e["evals"]
want = {"id": 4, "skill": "tone-guide", "prompt": "이 주석 톤 봐줘 — `// 차례칸이 비면 첫 세트로 돌아간다`",
        "expected_output": "K-11 을 관측 컨벤션으로 짚고 원래 이름이나 풀어 쓴 문장을 대안으로 제시",
        "assertions": [
            {"text": "references/locale-korean.md 를 실제로 Read 하고 K-11 행을 강도와 함께 인용한다", "type": "behavior"},
            {"text": "새로 붙인 이름을 K-11 관측 컨벤션으로 짚되 MUST 위반으로 단정하지 않는다", "type": "output"},
            {"text": "원래 이름을 그대로 쓰거나 하는 일을 문장으로 풀어 쓴 대안을 낸다", "type": "output"},
            {"text": "사전에 없다는 사실만으로 위반이라고 판정하지 않는다", "type": "behavior"}]}
c4 = [x for x in ev if x.get("id") == 4]
print("n=%d ids=%s case4=%d old_same=%d skill_name=%s" % (len(ev), ",".join(str(x.get("id")) for x in ev),
      int(len(c4) == 1 and c4[0] == want), int(ev[:3] == b["evals"][:3]), e.get("skill_name")))
PY
    ;;
  SK-04)  # korean-technical-writing — 원칙 9 자리 · 본문 · 출처 · 잡는 것 · 안티패턴 행
    awk '/^### 8\. 용어 번역표는 프로젝트가 소유한다/{a=NR} /^### 9\. 새 이름을 만들지 않는다 `\[한국어\]`$/{b=NR; n++} /^## 규칙 강도$/{c=NR} END{printf "p9=%d order=%d\n", n, (a && b && c && a < b && b < c)}' "$L/$KTW"
    S=$(sect "$L/$KTW" '### 9. 새 이름을 만들지 않는다')
    toks "$S" '대상을 부를 이름이 이미 있으면 그 이름을 쓴다. 없으면 하는 일을 문장으로 풀어 쓴다. 글쓴이가 새로 붙인 합성어·비유로 부르지 않는다.' \
      '// 차례칸이 비면 첫 세트로 돌아간다' '// 다음에 할 세트가 없으면 첫 세트로 돌아간다' '// pendingSets 가 비면 첫 세트로 돌아간다' \
      '실측은 세션 1건이다(2026-09-19) — 훅의 동작을 `표시훅` 이라는 새 합성어로 부르자 사용자가 뜻을 몰라 되물었다.' \
      '판정 기준은 사전에 실렸는지가 아니다.' '그래서 **처음 읽는 사람이 뜻을 짐작할 수 있는가** 로 가른다.' \
      '새 이름이 꼭 필요하면 처음 나올 때 괄호로 뜻을 붙인다 — Google 문서 스타일 가이드가 권하는 순서' \
      '`표시훅` 의 `훅` 처럼 음역이 섞이면 원칙 5 의 음역 금지에도 걸릴 수 있다.' \
      '**강도: 관측 컨벤션** (한국어 쪽 근거는 세션 1건 관찰뿐이다. 영어권 문서 가이드는 새 말 만들기를 피하라고 하지만 한국어 규범은 새 말 만들기를 금하지 않는다)'
    ln=$(printf '%s\n' "$S" | grep -F '> **출처:**'); echo "src_lines=$(printf '%s\n' "$ln" | grep -c .) $(toks "$ln" "$MS_URL" "$GG_URL" "$KN_URL" '세션 관찰 (2026-09-19, 1건)')"
    echo "catch=$(grep -cxF -- '- **새로 붙인 이름** — 읽는 사람이 뜻을 짐작할 수 없는 합성어·비유로 대상을 부르는 것(`차례칸`)' "$L/$KTW") anti=$(grep -cxF '| 글쓴이가 새로 붙인 이름으로 대상을 부름 (`차례칸`) | 읽는 사람이 무엇을 가리키는지부터 되묻는다. 원래 이름을 쓰거나 하는 일을 문장으로 풀어 쓴다 |' "$L/$KTW") nums=$(sect "$L/$KTW" '## 원칙' | grep -oE '^### [0-9]+\. ' | tr -dc '0-9\n' | awk 'BEGIN{ok=1} {ok = ok && ($1 + 0 == NR)} END{printf "%d/%d", ok, NR}')" ;;
  SK-05)  # research-log — 이번 사이클 기록 · 옛 기록 그대로 · 제목 겹침 없음
    S=$(sect "$L/$RL" '## 2026-09-24 — 카이젠 Phase 15 근거 조회')
    echo "head=$(grep -cx '## 2026-09-24 — 카이젠 Phase 15 근거 조회' "$L/$RL") dup=$(grep -E '^#{1,6} ' "$L/$RL" | sort | uniq -d | grep -c .) old_same=$(diff <(sect "$T/B/$RL" '## 2026-08-31 — 초기 이관 리서치' | notrail) <(sect "$L/$RL" '## 2026-08-31 — 초기 이관 리서치' | notrail) >/dev/null && echo 1 || echo 0)"
    toks "$S" '`reflect-collector:P6` · `F19`' '**K-11 신설, 관측 컨벤션.**' '**이름표가 내용보다 넓다.**' '「유형별로 알아보는 보도자료 작성 길잡이」(2021)' \
      '**강도 초과 1 건.** C-06 은 MUST 인데 원문 제목은 "PREFER writing doc comments for public APIs" 다.' '낡은 곳 목록만 남긴다' \
      '`core-naming.md` §8 의 표 칸 명령 넷(G-1 · G-2 · G-5 · G-6)이 죽어 있었다.' '명령을 코드 블록으로 옮겼다.' \
      '확장자 변수를 배열로 바꿨다.' '나머지 게이트 25 종은 bash · zsh 모두 합성 양성 케이스를 잡았다.' ;;
  SC-01)  # core-naming §8 — 표 칸에 명령 없음, 코드 블록을 bash · zsh 로 돌린 출력이 손으로 센 답과 같다
    S=$(sect "$L/$CN" '## 8. 완료 전 대조 grep')
    echo "rows=$(tablecells "$S" | grep -c .) cmd_in_table=$(tablecells "$S" | grep -cE '`(grep|find) ') escaped=$(tablecells "$S" | grep -cF '\|') ids=$(tablecells "$S" | awk -F' \\| ' '{print $1}' | tr -dc '0-9\n' | paste -sd, -)"
    fixture "$T/fx"
    for sh in bash zsh; do o=$(runin "$sh" "$T/fx" "$(bashblocks "$S")"); printf '%s=%s ' "$sh" "$([ "$o" = "$NAMING_ANSWER" ] && echo 1 || echo 0)"; done
    echo "lines=$(runin bash "$T/fx" "$(bashblocks "$S")" | grep -c .)" ;;
  SC-02)  # 확장자 변수 — 세 파일이 배열로 쓰고, 둘째 확장자를 더하면 bash · zsh 둘 다 그 파일을 찾는다
    echo "bare=$(bashblocks "$(sect "$L/$CN" '## 8. 완료 전 대조 grep')" | grep -cE '\$INC([^A-Za-z_]|$)') $(bashblocks "$(sect "$L/$CC" '## 6. 완료 전 대조 grep')" | grep -cE '\$X([^A-Za-z_]|$)') $(bashblocks "$(sect "$L/$OV" '## 완료 게이트는 이렇게 생겼다')" | grep -cE '\$INC([^A-Za-z_]|$)') arr=$(grep -cF '"${INC[@]}"' "$L/$CN") $(grep -cF '"${X[@]}"' "$L/$CC") $(grep -cF '"${INC[@]}"' "$L/$OV")"
    fixture "$T/fx"
    X=$(bashblocks "$(sect "$L/$CN" '## 8. 완료 전 대조 grep')" | addts INC)
    for sh in bash zsh; do printf 'naming_%s=%s ' "$sh" "$(runin "$sh" "$T/fx" "$X" | grep -cxF 'src/extra.ts:1:final effectiveTs = 1;')"; done; echo
    X=$(bashblocks "$(sect "$L/$CC" '## 6. 완료 전 대조 grep')")
    ln=$(printf '%s\n' "$X" | grep -E '^D=' | sed -e 's/{DIR}/src2/' -e 's/{EXT}/dart/' | addts X)
    for sh in bash zsh; do n=0; while IFS= read -r g; do
        [ "$(runin "$sh" "$T/fx" "$ln"$'\n'"$g" | grep -c '^src2/b\.ts:')" -ge 1 ] && n=$((n + 1)); done < <(printf '%s\n' "$X" | grep -E '^grep -rn')
      printf 'comment_%s=%s/%s ' "$sh" "$n" "$(printf '%s\n' "$X" | grep -cE '^grep -rn')"; done; echo
    X=$(bashblocks "$(sect "$L/$OV" '## 완료 게이트는 이렇게 생겼다')" | sed 's/^SRC=lib;/SRC=src;/' | addts INC)
    for sh in bash zsh; do printf 'overview_%s=%s ' "$sh" "$(runin "$sh" "$T/fx" "$X" | grep -cxF 'src/extra.ts:1:final effectiveTs = 1;')"; done; echo ;;
  ER-01)  # 새로 생긴 URL 이 근거 파일에 있다 — 근거 파일은 시작 커밋 판에서 읽는다 (끝 판은 .harness/ 안이라 이 Phase 가 고칠 수 있다)
    for f in "${FILES[@]}"; do comm -13 <(url < "$T/B/$f") <(url < "$E/$f"); done | sort -u | comm -23 - <(url < "$T/B/$EVID") | grep -c .
    if [ -f "$E/$NOTES" ]; then url < "$E/$NOTES" | comm -23 - <(url < "$T/B/$EVID") | grep -c .; else echo NOTES_MISSING; fi
    cmp -s "$T/B/$EVID" "$E/$EVID" && echo evid_same=1 || echo evid_same=0 ;;
  ER-02)  # 더한 줄의 번역투 6 종 · 앱 · 도구 서버 이름
    echo "added=$(added | grep -c .) k02=$(added | grep -cE "$K02") names=$(added | grep -ciE "$NAMES")" ;;
  ER-03)  # notes 문자열 · 넘김 · 다음 사이클 몫 · 공유 파일과 다른 Phase 파일을 건드린 커밋
    git cat-file -e "$END:$NOTES" 2>/dev/null && echo notes_committed=1 || echo notes_committed=0
    toks "$(cat "$E/$NOTES" 2>/dev/null)" '`reflect-collector:P6`' '`F19`' '## 바꾼 파일' '## 반영한 처리 배정표 키' '## 미반영 키와 사유' \
      '## 넘기는 것' '## changelog 한 단락' '## 킷 로그 한 단락' '## 다음 사이클 메모'
    # 넘김 · 다음 사이클 몫은 그 절 안에서 센다 — 낱말은 다른 절에도 나와 넘김 줄을 빠뜨려도 1 이 된다
    toks "$(sect "$E/$NOTES" '## 넘기는 것' 2>/dev/null)" 'docs/tone-kit/korean-technical-writing.html' 'docs/tone-kit/overview.html' \
      '.claude/skills/tone-kaizen/SKILL.md' 'phase-research-templates.md' 'plugin.json'
    toks "$(sect "$E/$NOTES" '## 다음 사이클 메모' 2>/dev/null)" 'C-06' 'etc_seq=663' 'unnecessary_underscores' '3.47.5' 'go_router' 'Style-guide-for-Flutter-repo' 'material_ui' '§2 표의 grep 열'
    not_other "$B" "$END" "$SIG" .claude-plugin/marketplace.json tone-kit/.claude-plugin/plugin.json README.md CLAUDE.md \
      .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml .claude/kaizen-input/insights-report.md \
      .github/workflows/ci.yml .harness/stale-values.yaml .claude/skills harness scripts docs/tone-kit docs/index.html \
      tone-kit/skills tone-kit/templates tone-kit/README.md | grep -c . ;;
  ER-04)  # locale-korean §9 자기모순 검사 — 끝 판 잔존 0, 킬러 패턴을 넣은 사본은 1
    S=$(sect "$L/$LK" '## 9. 자기모순 검사' | awk '/^```bash$/{b=1; next} b&&/^```$/{exit} b')
    mkdir -p "$T/sc"; cp "$L/$LK" "$T/sc/locale-korean.md"
    for sh in bash zsh; do printf '%s=%s ' "$sh" "$(runin "$sh" "$T/sc" "$S" | grep -c .)"; done
    python3 - "$T/sc/locale-korean.md" <<'PY' || { echo "NEG_EDIT_FAIL"; return 1; }
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read(); o = "- 새 이름이 꼭 필요하면 처음 나올 때 괄호로 뜻을 붙인다.\n"
if s.count(o) != 1: sys.exit(1)
open(p, "w", encoding="utf-8").write(s.replace(o, "- 새 이름에 대해서는 처음 나올 때 괄호로 뜻을 붙인다.\n"))
PY
    echo "pos=$(runin bash "$T/sc" "$S" | grep -c .)" ;;
  AR-01)  # 허용 경로 · 서명 · 봉인 · 범위 선언 블록
    unsigned_on "$B" "$END" "$SIG" tone-kit docs/tone | grep -c .
    echo "$(my | grep -v '^\.harness/' | grep -vxF -f <(printf '%s\n' "${FILES[@]}") | grep -c .) $(my | grep -cxF -f <(printf '%s\n' "${FILES[@]}"))"
    find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done \
      | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .
    verify_seal "$E/$CF" | cut -d' ' -f1
    diff <(scope "$E/$CF" | grep -vxF '.harness/' | sort) <(printf '%s\n' "${FILES[@]}" | sort) >/dev/null && echo "scope_same=1" || echo "scope_same=0"
    scope "$E/$CF" | grep -cxF '.harness/' ;;
  AR-02)  # 같은 것을 같은 자리에서 — 세 자리의 K-11 URL 이 같고, K-11 글이 663 · LINE 을 근거로 들지 않으며, 스킬은 그대로
    diff <(sect "$L/$LK" '## 10. 출처' | grep -F '(K-11' | url) <(sect "$L/$KTW" '### 9. 새 이름을 만들지 않는다' | grep -F '> **출처:**' | url) >/dev/null && a=1 || a=0
    diff <(sect "$L/$LK" '## 10. 출처' | grep -F '(K-11' | url) <(sect "$L/$SRCS" '## 로케일 — 한국어 기술 문체' | grep -F '확인됨 (2026-09-24)' | url) >/dev/null && b=1 || b=0
    echo "same_ktw=$a same_src=$b n=$(sect "$L/$LK" '## 10. 출처' | grep -F '(K-11' | url | grep -c .) cite663=$( { para "$L/$LK" '**새 이름을 만들지 않는다 (K-11).**'; sect "$L/$KTW" '### 9. 새 이름을 만들지 않는다'; } | grep -cE 'etc_seq=663|linecorp') skills_same=$(git diff --quiet "$B" "$END" -- tone-kit/skills tone-kit/templates && echo 1 || echo 0)" ;;
  AP-01)  # 더한 줄에 이 킷 플러그인 버전 값
    f=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$E/tone-kit/.claude-plugin/plugin.json")
    echo "version=$f $(added | grep -cF -- "$f")" ;;
  AP-03)  # 언어 힌트 없는 여는 펜스 — 마크다운 일곱 파일 (V6 가 안 읽는 docs/tone 셋 포함)
    for f in "${MDF[@]}"; do printf '%s ' "$(barefence "$L/$f")"; done; echo ;;
  RE-01)  # 재사용 단위 코드가 없다 — 서명 커밋이 바꾼 .harness/ 밖 파일의 확장자 (고정 목록 FILES 를 세면 늘 0 이다)
    echo "code_files=$(my | grep -v '^\.harness/' | grep -cvE '\.(md|json)$')" ;;
  RE-02)  # 옮긴 명령 넷은 시작 커밋 표 칸의 정규식을 글자 그대로 쓴다 — `\|` 를 `|` 로, `$INC` 를 배열로만 바꾼 줄이 끝 판 블록에 있다
    S=$(bashblocks "$(sect "$L/$CN" '## 8. 완료 전 대조 grep')")
    n=0; while IFS= read -r c; do printf '%s\n' "$S" | grep -qxF -- "$c" && n=$((n + 1)); done < <(tablecells "$(sect "$T/B/$CN" '## 8. 완료 전 대조 grep')" \
      | grep -oE '`grep [^`]+`' | tr -d '`' | sed -e 's/\\|/|/g' -e 's/\$INC/"${INC[@]}"/')
    echo "reused=$n/4" ;;
  DG-02)  # markdownlint — 파일마다 규칙별 경고 수가 편집 전보다 는 규칙 수
    for f in "${MDF[@]}"; do printf '%s ' "$(bash "$K/lintcmp.sh" "$T/B/$f" "$E/$f")"; done; echo ;;
  DG-05)  # 저장소 검사 — $END 판을 git 저장소로 만든 사본에서 돈다
    local G=$T/G; rm -rf "$G"; cp -R "$E" "$G"
    git -C "$G" init -q && git -C "$G" add -A && git -C "$G" -c user.name=m -c user.email=m@m commit -qm snap || return 2
    ( cd "$G" && python3 scripts/validate-plugin.py tone-kit > "$T/vp.txt" 2>&1; echo $? > "$T/vp.rc" )
    echo "$(grep -cE '^  V([1-9]|10) ' "$T/vp.txt") $(grep -E '^  V([1-9]|10) ' "$T/vp.txt" | grep -cvE -- '— OK$') rc=$(cat "$T/vp.rc")"
    ( cd "$G" && python3 scripts/sync-docs.py --check-only > "$T/sd.txt" 2>&1 ); echo "sync_docs_rc=$? $(grep -cxF '  tone-kit/README.md: 동기화됨' "$T/sd.txt")"
    ( cd "$G" && python3 scripts/sync-evals.py --check-only > "$T/se.txt" 2>&1 ); echo "sync_evals_rc=$? $(grep -cxF 'Total: 0 added, 0 orphans, 0 missing (preview)' "$T/se.txt")"
    ( cd "$G" && python3 scripts/run-evals.py tone-kit > "$T/re.txt" 2>&1 ); echo "run_evals_rc=$? $(grep -cxF 'Total: 4 passed, 0 failed' "$T/re.txt")" ;;
  DG-06)  # 사이클 검사 — 이 Phase 몫 줄만 본다. docs-site-regen 은 Final F2 몫
    python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1
    grep -E '\] . (scope-isolation|doc-contracts): ' "$T/vpk.txt" | awk '{print $5, $2}'
    awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" > "$T/viol.txt"
    echo "violators=$(grep -c . "$T/viol.txt") mine=$(while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done < "$T/viol.txt" | grep -c .)" ;;
  NA)  # N/A 줄 셋(DG-01 · DG-03 · DG-04)의 사유 측정 — 서명 커밋이 건드린 경로
    echo "DG-01=$(my | grep -c '^scripts/release.sh$') DG-04=$(my | grep -v '^\.harness/' | grep -cvE '\.(md|json)$')" ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

```bash
#!/usr/bin/env bash
# lintcmp.sh <옛 파일> <새 파일> — 규칙마다 경고 수를 편집 전 판과 비교해 늘어난 규칙만 낸다
# 더한 줄만 세면 같은 제목 중복(MD024) · 제목 앞뒤 빈 줄(MD022) · 목록 앞뒤 빈 줄(MD032)처럼 손대지 않은 옆 줄에 붙는 새 경고를 놓친다
# 린터가 안 돌면 경고 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
cnt() {
  local o
  o=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$1" 2>&1)
  printf '%s\n' "$o" | grep -q '^Linting: 1 file' || { echo "LINT_NOT_RUN $1"; return 2; }
  printf '%s\n' "$o" | grep -oE ' (error|warning) MD[0-9]+' | awk '{print $2}' | sort | uniq -c | awk '{print $2, $1}'
}
OLD=$(cnt "$1") || { echo "$OLD"; exit 2; }
NEW=$(cnt "$2") || { echo "$NEW"; exit 2; }
join -a2 -e0 -o 0,1.2,2.2 <(printf '%s\n' "$OLD" | grep . | sort) <(printf '%s\n' "$NEW" | grep . | sort) \
  | awk '$3 > $2 { printf "%s:+%d ", $1, $3 - $2; n++ } END { print "rules_up=" n + 0 }'
```

### 봉인 전 실측 (2026-09-25)

검토(`.harness/.meta/kaizen-0924/phase15-review.md`) 반영 뒤 예행 저장소와 변형 여섯을 새로 만들어 아래 값을 전부 다시 쟀다 — 바뀐 값은 ER-01 셋째 줄 `evid_same` 과
새로 넣은 양성 대조 두 줄(ER-01 근거 파일 · RE-01)뿐이다.

예행 저장소는 `rehearse.sh`(스크래치 `p15d/`)가 작업 폴더를 복제해 시작 커밋 `499cc12` 에서 BUILD 가 할 커밋을 흉내 낸 것이다 — 봉인 커밋(서명) · 다른 Phase 서명 커밋
하나(`api-kit/README.md`, 걸러져야 한다) · 구현 두 커밋(`mock.py` 적용, `tone-kit/` 다섯 · `docs/tone/` 셋) · `end_sha` · notes(`notes-mock.md`) · `end_sha` 다시.
측정은 전부 `R=<예행 저장소> K=<도우미 폴더> bash -c '. "$K/common.sh"; . "$K/m.sh"; …'` 로 돌렸다.
대조 스크립트는 같은 스크래치 폴더의 `rehearse.sh`(예행 저장소와 변형 `none` · `base` · `unsigned-mine` · `signed-outside` · `cross-phase` · `nonotes`) · `runall.sh`(조건 전부) · `ctl.sh`(모드 `neg` · `raw` · `mut` · `del`) · `re01-pos.sh`(RE-01 양성 대조)다.

**끝 판(변형 `none`)** — 조건 스물셋이 요구값 그대로다:

```text
SK-01  row=1 ids=1/11 | 1 1 1 1 1 1 1 1 | title=1 toc=1 dict_word=0 sect8_k11=0
SK-02  1 1 1 1 | 1 1 1 1 1 1 | status_row=1
SK-03  n=4 ids=1,2,3,4 case4=1 old_same=1 skill_name=tone-kit
SK-04  p9=1 order=1 | 1 1 1 1 1 1 1 1 1 1 | src_lines=1 1 1 1 1 | catch=1 anti=1 nums=1/9
SK-05  head=1 dup=0 old_same=1 | 1 1 1 1 1 1 1 1 1 1
SC-01  rows=8 cmd_in_table=0 escaped=0 ids=1,2,3,4,5,6,7,8 | bash=1 zsh=1 lines=8
SC-02  bare=0 0 0 arr=7 8 3 | naming_bash=1 naming_zsh=1 | comment_bash=8/8 comment_zsh=8/8 | overview_bash=1 overview_zsh=1
ER-01  0 | 0 | evid_same=1
ER-02  added=121 k02=0 names=0
ER-03  notes_committed=1 | 1 1 1 1 1 1 1 1 1 | 1 1 1 1 1 | 1 1 1 1 1 1 1 1 | 0
ER-04  bash=0 zsh=0 pos=1
AR-01  0 | 0 8 | 0 | SEAL_OK | scope_same=1 | 1
AR-02  same_ktw=1 same_src=1 n=3 cite663=0 skills_same=1
AP-01  version=0.1.0 0
AP-03  0 0 0 0 0 0 0
RE-01  code_files=0
RE-02  reused=4/4
DG-02  rules_up=0 ×7
DG-05  10 0 rc=0 | sync_docs_rc=0 1 | sync_evals_rc=0 1 | run_evals_rc=0 1
DG-06  scope-isolation: PASS | doc-contracts: PASS | violators=0 mine=0
NA     DG-01=0 DG-04=0
```

측정 셸을 `/bin/bash` 3.2(PATH 앞에 `/bin`)로 바꿔 SC-01 · SC-02 · SK-01 을 다시 돌려도 같은 값이었다 — 게이트 블록 안의 배열 펼침과 `+=` 가 3.2 에서도 돈다.
같은 끝 판에서 `python3 scripts/validate-plugin.py`(전체 킷)는 `Total: 14 plugins, 14 OK` · 종료 코드 0, `run-evals.py tone-kit --verbose` 는 `PASS eval #4 (tone-guide): 4 assertions` 를 포함해
`Total: 4 passed, 0 failed` 였다(카이젠 스킬 Step 4 명령). 등록된 검사 목록(`grep -oE '"[a-z-]+": check_v[0-9]+' scripts/validate-plugin.py`)은
`frontmatter templates refs triggers placeholders code-fence plugin-json hook-exec arg-substitution table-integrity` 열이다.

**시작 커밋 판(`V=B m …` · 변형 `base`)** — 기능 조건이 전부 요구값에서 벗어난다:

```text
SK-01  row=0 ids=1/10 | 0 0 0 0 0 0 0 0 | title=1 toc=1 dict_word=0 sect8_k11=0
SK-02  0 0 0 0 | 0 0 0 0 0 0 | status_row=0
SK-03  n=3 ids=1,2,3 case4=0 old_same=1 skill_name=tone-kit
SK-04  p9=0 order=0 | 0 ×10 | src_lines=0 0 0 0 0 | catch=0 anti=0 nums=1/8
SK-05  head=0 dup=0 old_same=1 | 0 ×10
SC-01  rows=8 cmd_in_table=5 escaped=4 ids=1,2,3,4,5,6,7,8 | bash=0 zsh=0 lines=3
SC-02  bare=3 8 3 arr=0 0 0 | naming_bash=0 naming_zsh=0 | comment_bash=8/8 comment_zsh=0/8 | overview_bash=1 overview_zsh=0
ER-01  0 | NOTES_MISSING | evid_same=1   ER-02  added=0 k02=0 names=0   ER-03  notes_committed=0 | 0 … | 0
ER-04  bash=0 zsh=0 NEG_EDIT_FAIL   AR-01  0 | 0 0 | 0 | SEAL_OK | scope_same=1 | 1
AR-02  same_ktw=1 same_src=1 n=0 cite663=0 skills_same=1        RE-02  reused=0/4
DG-05  10 0 rc=0 | sync_docs_rc=0 1 | sync_evals_rc=0 1 | run_evals_rc=0 0
```

AP-01 · AP-03 · RE-01 · DG-02 · DG-06 · `m NA` 는 시작 커밋 판에서도 요구값이다 — 「해를 끼치지 않았다」 를 재는 조건이라 그렇다. 각각의 양성 대조는 아래에 있다.

**표 칸 명령을 그대로 붙여 넣었을 때 (시작 커밋 판 `ctl.sh raw`)** — fixture `src/` 에서 `SRC=src` · `INC="--include=*.dart"` 를 앞에 두고:

```text
bash lines=0 rc=1 | zsh lines=0 rc=1 | G-1  grep -rnE '\b(effective\|resolved)[A-Z]' …
bash lines=0 rc=1 | zsh lines=0 rc=1 | G-2  grep -rnE 'class [A-Za-z]*(Row\|Cell)…
bash lines=0 rc=1 | zsh lines=0 rc=1 | G-5  grep -rnE 'class [A-Za-z]*(Blue\|Red\|…
bash lines=11 rc=0 | zsh lines=11 rc=0 | G-6  … \| grep -vE 'for \('   ← fixture 열한 줄 전부
bash lines=1 rc=0 | zsh lines=1 rc=0 | G-7  find …                      ← 살아 있다 (\| 없음)
확장자 둘을 한 문자열(INC="--include=*.dart --include=*.ts")로: bash 2 줄 · zsh 0 줄
```

나머지 게이트 25 종의 생존은 스크래치 `p15/gs/run.sh` 가 문서의 명령을 손으로 옮겨 돌려 쟀다(옮긴 명령 25 개가 시작 커밋 판 문서의 명령 줄과 글자로 같다 — 검토 결과 6) — bash · zsh 모두 주석 `cG1=1 cG2=1 cG3=1 cG4=1 cG5=1 cG6=2 cG7=2 cG8=2`,
이름 `nG3=1 nG4=1 nG7=1 nG8=1`, 한국어 `kG1=2 kG2=1 kG3=1`, 어댑터 `a01` ~ `a10` 전부 1 (합성 양성 케이스 파일 한 벌).

**양성 대조 (`ctl.sh mut` — 끝 판 사본을 한 군데 망가뜨림, 측정 뒤 되돌림)**

```text
ER-01  근거 파일에 없는 URL 한 줄을 research-log 사본에      → 1
ER-01  같은 URL 을 끝 판 근거 파일 사본에도 덧붙임            → 1 0 evid_same=0
ER-01  research-log 만 되돌림 (근거 파일 사본은 그대로)      → 0 0 evid_same=0
ER-02  K-11 목록 한 줄을 「에 대해서는」 문장으로             → added=121 k02=1 names=0
AP-01  research-log 사본에 v0.1.0 한 줄                       → version=0.1.0 1
DG-02  research-log 사본에 옛 제목 한 번 더                   → MD024:+1 rules_up=1 (그 파일만)
AR-01  계약 사본의 SK-01 조건 줄 한 글자 변조                  → SEAL_BROKEN
DG-04  거르개에 tone-kit/scripts/a.sh 한 줄                   → 1
DG-01  거르개에 scripts/release.sh · scripts/release.sh.bak   → 1
RE-01  예행 사본에 서명 커밋으로 tone-kit/scripts/a.sh 더함    → code_files=1 (같은 사본 m NA → DG-04=1)
되돌린 뒤 다시 잰 값: ER-01=0 0 evid_same=1 · ER-02 k02=0 · AP-01 0
```

ER-04 는 양성 대조를 측정 안에 넣었다(`pos=1`).

**예행 변형 (AR-01 · ER-03)**

```text
unsigned-mine   (서명 없이 tone-kit/README.md)            AR-01 1 | 0 8 | …   ER-03 … | 1
signed-outside  (서명하고 tone-kit plugin.json)            AR-01 0 | 1 8 | …   ER-03 … | 1
cross-phase     (서명하고 harness 파일 + tone-kit 파일)    AR-01 0 | 2 8 | …   ER-03 … | 1
nonotes         (notes 커밋 없음)                          ER-03 notes_committed=0 | 0 … | 0
```

**지운 사본 (`ctl.sh del`)** — 더한 줄을 하나씩 지운 사본에서 그 조건 값이 바뀌는지 빈 줄이 아닌 더한 줄 전부에 돌렸다.

```text
SK-01 locale-korean.md  changed=6 unchanged=4   ← 안 바뀐 넷은 §10 출처 줄 — SK-02 가 잰다
SK-02 locale-korean.md  changed=4 unchanged=6   ← 안 바뀐 여섯은 K-11 행 · §4 문단 — SK-01 이 잰다
SK-02 sources.md        changed=5 unchanged=0
SK-04 korean-technical-writing.md  changed=14 unchanged=4   ← last_updated · 코드 예 머리 주석 셋(// Bad — … · // Good — … 둘)
SK-05 research-log.md   changed=9 unchanged=4   ← last_updated · 표 구분선 · 「변화 없음」 두 행
```

locale-korean 의 더한 줄 열은 SK-01 · SK-02 가운데 하나가 반드시 잡는다. 안 바뀐 나머지는 조건이 요구하지 않는 줄뿐이다.

**준비 단계 (값 면제와 별개로 돌려 본 것)** — `command -v bash` → `/opt/homebrew/bin/bash`(5.3.9) · `/bin/bash` 3.2.57 · `command -v zsh` → `/bin/zsh`(5.9) ·
`zsh -c 'type grep'` · `bash -c 'type grep'` → 둘 다 `grep is /usr/bin/grep`(BSD grep 2.6.0) · markdownlint-cli2 v0.23.2 · `shasum` 있음 · `python3` 3.14.3.
`mock.py` 는 시작 커밋 판을 푼 새 사본에서 `mock applied 8` · 종료 코드 0, 같은 사본에 두 번째로 돌리면 `MOCK_FAIL start-sha tone-kit/references/locale-korean.md` · 종료 코드 3 이다.
검토 반영 뒤 지금 가지 끝(`3a348d6`)을 푼 새 사본에서도 같은 두 값이다(`tone-kit` · `docs/tone` 은 시작 커밋 뒤 바뀐 커밋 0).

## Skill

- [ ] SK-01: `tone-kit/references/locale-korean.md` 에 K-11 이 관측 컨벤션으로 들어간다 — (a) `## 1. 규칙표` 에 행 `| K-11 | 글쓴이가 새로 붙인 이름(합성어·비유)으로 대상을 부르지 않는다. 원래 이름을 그대로 쓰거나 하는 일을 문장으로 풀어 쓴다 (§4 끝) | 관측 컨벤션 |` 이 1 줄이고 규칙표 ID 가 K-01 부터 K-11 까지 빠짐없이 이어진다 (b) `## 4. 외래어 3원칙` 절에 K-11 문단 조각 여덟(제목 문장과 원래 이름 셋 · 이름이 없으면 문장으로 · 판정은 처음 읽는 사람 기준 · 제50항 해설 · 괄호로 뜻 · K-05 겹침 · §6 표 판정과 강도 인용 · §8 에 grep 없음과 규칙표 행으로 판정)이 각각 1 줄 (c) §4 제목 줄과 목차 줄은 1 줄씩 그대로이고, 제안 원문의 판정어 「사전에 없는 한국어 합성어」 는 파일 전체에 0, `## 8. 완료 전 대조 grep` 절에 `K-11` 은 0 이다. 음성 대조: 시작 커밋 판은 첫 줄이 `row=0 ids=1/10`, 둘째 줄이 `0` 여덟이다 (`reflect-collector:P6` · `F19`) — `m SK-01` 세 줄이 `row=1 ids=1/11` · `1 1 1 1 1 1 1 1` · `title=1 toc=1 dict_word=0 sect8_k11=0` [exact, enumerated]
- [ ] SK-02: K-11 근거가 두 파일에 같은 글로 있다 — `tone-kit/references/locale-korean.md` `## 10. 출처` 에 넷(Microsoft · Google · 한글 맞춤법 줄에 각각 `(K-11` 표시, 세션 관찰 2026-09-19 줄), `tone-kit/references/sources.md` `## 로케일 — 한국어 기술 문체` 에 여섯(세 행 `확인됨 (2026-09-24)` · 「위 표의 마지막 세 행」 문장 · 관측 컨벤션이고 판정 기준이 사전 등재가 아닌 까닭 · Learn 페이지 본문 미확인), `## 검증 상태 표기` 의 `확인됨` 행이 「괄호에 날짜가 있으면 그날 확인」 을 담는다. 음성 대조: 시작 커밋 판은 셋 다 0 이다 (`reflect-collector:P6` · 근거 권장안 3) — `m SK-02` 세 줄이 `1 1 1 1` · `1 1 1 1 1 1` · `status_row=1` [exact, enumerated]
- [ ] SK-03: `tone-kit/evals/evals.json` 이 JSON 으로 읽히고 사례가 넷(id `1,2,3,4`)이며, 사례 4 가 tone-guide 의 K-11 사례 — 프롬프트 「이 주석 톤 봐줘 — `// 차례칸이 비면 첫 세트로 돌아간다`」, 기대 출력, assertion 넷(locale-korean 을 Read 하고 K-11 을 강도와 함께 인용 · 관측 컨벤션으로 짚되 MUST 로 단정하지 않음 · 원래 이름이나 풀어 쓴 문장 대안 · 사전에 없다는 사실만으로 위반 판정하지 않음)이 `m.sh` `SK-03)` 갈래의 `want` 와 글자 그대로 같다 — 이고, 사례 1 ~ 3 은 시작 커밋 판과 같다. 음성 대조: 시작 커밋 판은 `n=3 ids=1,2,3 case4=0` (`reflect-collector:P6` — 제안 원문의 평가 사례, 근거 권장안 4 로 음역이 안 섞인 예) — `m SK-03` 이 `n=4 ids=1,2,3,4 case4=1 old_same=1 skill_name=tone-kit` [exact]
- [ ] SK-04: `docs/tone/korean-technical-writing.md` 에 원칙 9 가 선다 — (a) 제목 `` ### 9. 새 이름을 만들지 않는다 `[한국어]` `` 이 1 개이고 `### 8. 용어 번역표는 프로젝트가 소유한다` 뒤 · `## 규칙 강도` 앞에 있다 (b) 그 절에 열 조각(요약 문장 · Bad 한 줄 · Good 두 줄 · 세션 실측 2026-09-19 · 사전 기준 아님 · 처음 읽는 사람 기준 · 괄호와 Google 순서 · 원칙 5 겹침 · 강도 관측 컨벤션과 그 까닭)이 각각 1 줄 (c) 그 절의 출처 줄이 하나이고 Microsoft · Google · 한글 맞춤법 URL 과 「세션 관찰 (2026-09-19, 1건)」 을 담는다 (d) `이 문서가 잡는 것` 줄 · `## 안티패턴` 행이 하나씩이고 `## 원칙` 절 번호가 1 부터 9 까지 이어진다. 음성 대조: 시작 커밋 판은 `p9=0 order=0` · `0` 열 · `src_lines=0 …` · `catch=0 anti=0 nums=1/8` (`F19` · `reflect-collector:P6` — 킷 규칙의 근거 문서) — `m SK-04` 네 줄이 `p9=1 order=1` · `1 1 1 1 1 1 1 1 1 1` · `src_lines=1 1 1 1 1` · `catch=1 anti=1 nums=1/9` [exact, enumerated]
- [ ] SK-05: `docs/tone/research-log.md` 에 이 사이클 기록이 남는다 — 제목 `## 2026-09-24 — 카이젠 Phase 15 근거 조회` 1 개 · 파일 안 같은 제목 겹침 0 · `## 2026-08-31 — 초기 이관 리서치` 절이 시작 커밋 판과 같고, 새 절에 열 조각(배정 키 둘 · K-11 신설 · 663 이름표 · 663 실제 제목 · C-06 강도 초과와 원문 제목 · 현행화 목록 · 죽은 이름 게이트 넷 · 코드 블록으로 옮김 · 배열 · 나머지 25 종)이 각각 1 줄이다. 음성 대조: 시작 커밋 판은 `head=0` · `0` 열 (카이젠 스킬 Step 5 보고 · 오케스트레이터 Gotcha 「per-kit research-log」) — `m SK-05` 두 줄이 `head=1 dup=0 old_same=1` · `1 1 1 1 1 1 1 1 1 1` [exact, enumerated]

## Script

- [ ] SC-01: `tone-kit/references/core-naming.md` `## 8. 완료 전 대조 grep` 의 게이트 여덟이 코드 블록에서 산다 — (a) 표 행이 여덟(G-1 ~ G-8 차례)이고 그 가운데 `grep` · `find` 명령을 담은 행 0 · `\|` 를 담은 행 0 (b) 그 절의 bash 코드 블록을 이어 `fixture` 폴더에서 bash 와 zsh 로 돌린 표준 출력이 둘 다 손으로 센 답 `NAMING_ANSWER`(G-1 ~ G-8 이 한 줄씩 — `common.sh`)와 글자 그대로 같다. 알려진 답: fixture `src/pos.dart` 열한 줄 · `src/utils.dart` 빈 파일 · 기대 여덟 줄, 봉인 전 실제값 bash · zsh 모두 여덟 줄 일치. 음성 대조: 시작 커밋 판은 `rows=8 cmd_in_table=5 escaped=4` · `bash=0 zsh=0 lines=3`(블록에 G-3 · G-4 · G-8 뿐)이고, 시작 커밋 표 칸의 G-1 · G-2 · G-5 를 그대로 붙여 넣으면 bash · zsh 모두 0 줄 · 종료 코드 1, G-6 은 fixture 열한 줄 전부다(`회귀 게이트` 절) (카이젠 스킬 Step 2 `게이트 생존` · 오케스트레이터 Phase 15 지시 「bash · zsh 양쪽 + 합성 양성 케이스」) — `m SC-01` 두 줄이 `rows=8 cmd_in_table=0 escaped=0 ids=1,2,3,4,5,6,7,8` · `bash=1 zsh=1 lines=8` [exact]
- [ ] SC-02: 확장자 변수가 세 자리 모두 배열이다 — (a) `core-naming.md` §8 · `tone-kit/references/core-comment.md` `## 6. 완료 전 대조 grep` · `docs/tone/overview.md` `## 완료 게이트는 이렇게 생겼다` 의 bash 코드 블록에 따옴표 없는 `$INC` · `$X` 인자가 0 이고, 배열 펼침(`"${INC[@]}"` · `"${X[@]}"` · `"${INC[@]}"`)이 파일에 7 · 8 · 3 줄 (b) 각 블록의 확장자 정의 줄 뒤에 문서 모양 그대로 둘째 확장자(`.ts`)를 더해 `fixture` 에서 돌리면 bash · zsh 둘 다 `.ts` 파일을 찾는다 — 이름 게이트 G-1 이 `src/extra.ts:1:final effectiveTs = 1;` 1 줄, 주석 게이트 여덟이 전부 `src2/b.ts` 를 1 줄 이상, 개요 예시 G-1 이 같은 1 줄. 음성 대조: 시작 커밋 판은 `bare=3 8 3 arr=0 0 0` · `naming_bash=0 naming_zsh=0` · `comment_bash=8/8 comment_zsh=0/8` · `overview_bash=1 overview_zsh=0` 이다 (카이젠 스킬 Step 2 `게이트 생존` — zsh 는 따옴표 없는 변수를 나누지 않는다) — `m SC-02` 네 줄이 `bare=0 0 0 arr=7 8 3` · `naming_bash=1 naming_zsh=1` · `comment_bash=8/8 comment_zsh=8/8` · `overview_bash=1 overview_zsh=1` [exact]

## Error

- [ ] ER-01: 여덟 파일에 새로 생긴 URL 과 `.harness/.meta/kaizen-0924/phase15-notes.md` 의 URL 이 전부 시작 커밋 판의 외부 근거 파일 `.harness/.meta/evidence/phase15.md` 에 있고, 끝 판 근거 파일이 시작 커밋 판과 같다 — 근거 파일은 .harness 폴더 안이라 이 Phase 가 고칠 수 있으므로 끝 판에서 읽지 않는다. 여덟 파일은 파일마다 편집 전 판과 비교한다. 양성 대조: 근거 파일에 없는 URL 한 줄을 research-log 사본에 더하면 첫 값 1, 같은 URL 을 끝 판 근거 파일 사본에도 덧붙이면 첫 값은 그대로 1 이고 셋째 값이 `evid_same=0` (러닝북 — 근거 파일에 없는 URL 을 지어내지 마라 · notes 킷 로그의 출처 URL 은 근거 파일에서만) — `m ER-01` 세 줄이 `0` · `0` · `evid_same=1` [exact, enumerated]
- [ ] ER-02: 여덟 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열 — `common.sh` `K02`)과 특정 앱 · 화면 조종 도구 이름(`fit-?pal` · `fit_pal` · `flutter[-_]playwright` · `playwright-mcp` · `chrome-devtools-mcp`, 대소문자 무시)이 0 건이다. 양성 대조: 더한 줄 하나를 「에 대해서는」 이 든 문장으로 바꾼 사본은 `k02=1` (러닝북 말투 규칙 · K-02) — `m ER-02` 가 `added=N k02=0 names=0` 이고 N 은 1 이상 [exact]
- [ ] ER-03: 이 Phase 범위 밖과 미반영 몫을 명시적 미완으로 넘기고 공유 파일 · 다른 Phase 파일 · 이 킷의 나머지를 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase15-notes.md` 가 `$END` 에 커밋돼 있고 (a) 처리 배정표 키 `reflect-collector:P6` · `F19` 와 러닝북 절 제목 일곱(`## 바꾼 파일` · `## 반영한 처리 배정표 키` · `## 미반영 키와 사유` · `## 넘기는 것` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모`)이 각각 1 줄 이상 (b) `## 넘기는 것` 절 안에 넘김 다섯(`docs/tone-kit/korean-technical-writing.html` · `docs/tone-kit/overview.html` · `.claude/skills/tone-kaizen/SKILL.md` · `phase-research-templates.md` · `plugin.json`)이 각각 1 줄 이상 (c) `## 다음 사이클 메모` 절 안에 여덟(`C-06` · `etc_seq=663` · `unnecessary_underscores` · `3.47.5` · `go_router` · `Style-guide-for-Flutter-repo` · `material_ui` · `§2 표의 grep 열`)이 각각 1 줄 이상 (d) 공유 파일 · `harness/` · `scripts/` · `docs/tone-kit/` · `docs/index.html` · `.claude/skills/` · `tone-kit/skills/` · `tone-kit/templates/` · `tone-kit/README.md` · `tone-kit/.claude-plugin/plugin.json` 을 건드린 구간 안 커밋 가운데 다른 Phase 서명이 없는 것이 0 이다. 양성 대조: 예행 변형 `nonotes` → `notes_committed=0`, `signed-outside` → 마지막 값 1 (근거 권장안 5 ~ 8 · Counterpart 미완) — `m ER-03` 다섯 줄이 `notes_committed=1` · 아홉 값 전부 1 이상 · 다섯 값 전부 1 이상 · 여덟 값 전부 1 이상 · `0` [exact, enumerated]
- [ ] ER-04: `locale-korean.md` `## 9. 자기모순 검사` 의 명령을 그 절에서 그대로 뽑아 `$END` 판 사본에 bash · zsh 로 돌리면 잔존이 0 줄이다 — K-11 문단이 번역투를 더하지 않았다. 양성 대조: 그 사본의 K-11 목록 한 줄을 「에 대해서는」 이 든 문장으로 바꾸면 1 줄 (K-10 MUST — 규칙 문서를 쓴 뒤 자기 본문에 6 종을 돌린다) — `m ER-04` 가 `bash=0 zsh=0 pos=1` [exact]

## Architecture

- [ ] AR-01: 이 Phase 의 변경이 허용 경로 안에 머물고, 범위 선언 블록이 그 경로와 같으며, 이 계약이 봉인돼 있다 — `tone-kit/` · `docs/tone/` 를 건드린 구간 안 커밋이 전부 서명했고, 서명 커밋이 고친 `.harness/` 밖 경로가 여덟 파일뿐이며(여덟 전부 포함), 서명 커밋이 건드린 계약 가운데 봉인이 깨진 것이 0, 이 계약이 `SEAL_OK`, `## 범위 경계` 의 `# sprint-scope` 블록이 여덟 경로와 `.harness/` 한 줄이다. 양성 대조: 예행 변형 `unsigned-mine` → 첫 값 `1` · `signed-outside` · `cross-phase` → 둘째 줄 첫 값 `1` 이상 · 조건 줄 한 글자 변조 → `SEAL_BROKEN` — `m AR-01` 여섯 줄이 `0` · `0 8` · `0` · `SEAL_OK` · `scope_same=1` · `1` [exact, enumerated]
- [ ] AR-02: 같은 규칙을 같은 근거로 말한다 — (a) `locale-korean.md` §10 의 K-11 줄 URL 집합이 `docs/tone/korean-technical-writing.md` 원칙 9 출처 줄의 URL 집합, `sources.md` 로케일 표 `확인됨 (2026-09-24)` 행의 URL 집합과 각각 같고 셋이다 (b) `locale-korean.md` K-11 문단과 원칙 9 절에 `etc_seq=663` · `linecorp` 가 0 이다(근거 권장안 3 — 두 출처는 이 규칙을 말하지 않는다) (c) `tone-kit/skills/` · `tone-kit/templates/` 가 시작 커밋과 같다 — 스킬 셋은 규칙표와 게이트 절을 통째로 읽어 K-11 과 새 블록을 따로 이을 자리가 없다. 음성 대조: 시작 커밋 판은 `same_ktw=1 same_src=1 n=0`(빈 집합끼리 같다 — 그래서 `n=3` 을 함께 잰다) — `m AR-02` 가 `same_ktw=1 same_src=1 n=3 cite663=0 skills_same=1` [exact]

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 여덟 파일에 더한 줄에 tone-kit `plugin.json` 의 `version` 값(`$END` 판에서 읽는다)이 0 건이다 — 이 Phase 는 킷 버전을 적지 않고 Final 이 올린다. Flutter 3.47.5 · go_router 18.0.1 같은 외부 도구 판은 날짜를 단 조회 기록이라 이 패턴의 대상이 아니다. 양성 대조: 더한 줄에 `v0.1.0` 을 넣은 사본은 1 — `m AP-01` 이 `version=0.1.0 0` [exact]
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: V6 가 읽는 `references/` 넷은 DG-05 의 V6 줄이 보고, V6 가 안 읽는 `docs/tone/` 셋까지 마크다운 일곱 파일 모두 같은 여닫기 방식으로 센 언어 힌트 없는 여는 펜스가 0 이다 — `m AP-03` 이 `0 0 0 0 0 0 0` [exact]

## Reusability

- [ ] RE-01: N/A (산출물에 재사용 단위 코드가 없다 — 바뀐 여덟 파일이 규칙 문서 · 평가 사례 · 리서치 문서뿐이다. 측정: `type m >/dev/null || exit 2;` 뒤 `m RE-01` 이 `code_files=0`. 게이트 명령은 문서 안 코드 블록이라 SC-01 · SC-02 가 실행으로 잰다)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: 코드 블록으로 옮긴 이름 게이트 넷(G-1 · G-2 · G-5 · G-6)은 새로 짜지 않고 시작 커밋 표 칸의 명령을 `\|` → `|` · `$INC` → `"${INC[@]}"` 두 가지만 바꿔 글자 그대로 쓴다 — 바꾼 네 줄이 끝 판 블록에 한 줄씩 그대로 있다. K-11 은 음역 판정을 다시 정의하지 않고 K-05 · §6 표를 가리킨다(SK-01) — `m RE-02` 가 `reused=4/4` [exact]

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type m >/dev/null || exit 2;` 뒤 `m NA` 의 `DG-01=0`. 게이트 블록의 실제 실행은 SC-01 · SC-02)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 일곱 파일마다 규칙별 경고 수를 편집 전 판과 비교해 는 규칙이 0 이고 린터가 열네 번 다 돌았다(`LINT_NOT_RUN` 0). `evals.json` 은 SK-03 이 JSON 으로 읽는다. 편집 전부터 있던 경고는 `범위 경계` 절에 적은 대로 범위 밖이다. 양성 대조: `research-log.md` 사본에 옛 제목 `## 2026-08-31 — 초기 이관 리서치` 를 한 번 더 넣으면 그 파일이 `MD024:+1 rules_up=1` — `m DG-02` 가 `rules_up=0` 일곱 [exact]
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 `m NA` 의 `DG-01=0`. 실제 시험은 SC-01 · SC-02 · DG-05 `run-evals.py`)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — 바뀐 파일이 전부 `.md` · `.json` 이다. 측정: `m NA` 의 `DG-04=0` — 서명 커밋이 건드린 `.harness/` 밖 경로 가운데 `.md` · `.json` 이 아닌 것. 양성 대조: 같은 거르개에 `tone-kit/scripts/a.sh` 한 줄을 넣으면 1)
- [ ] DG-05: 저장소 검사가 이 킷을 문제로 가리키지 않는다 — `$END` 판을 git 저장소로 만든 사본에서 (a) `scripts/validate-plugin.py tone-kit` 출력에 `V1` ~ `V10` 열 줄이 있고 전부 `— OK` 로 끝나며 종료 코드 0 (b) `scripts/sync-docs.py --check-only` 가 종료 코드 0 에 `  tone-kit/README.md: 동기화됨` 1 줄 (c) `scripts/sync-evals.py --check-only` 가 종료 코드 0 에 `Total: 0 added, 0 orphans, 0 missing (preview)` 1 줄 (d) `scripts/run-evals.py tone-kit` 가 종료 코드 0 에 `Total: 4 passed, 0 failed` 1 줄 — `m DG-05` 네 줄이 `10 0 rc=0` · `sync_docs_rc=0 1` · `sync_evals_rc=0 1` · `run_evals_rc=0 1` [exact]
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 499cc1289f0f5ae5649da601515725f49f4f1096` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록을 한 개 이상 읽었고 그 안에 이 Phase 서명 커밋이 없을 때 이 조건은 PASS 다 — `m DG-06` 의 `scope-isolation` · `doc-contracts` 줄과 `violators=N mine=0` [goal]
