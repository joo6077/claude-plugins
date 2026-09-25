---
feature: "카이젠 2026-09-24 Phase 10 계약 — 렌더 증거 반영 확인 · 개발 서버 포트 고정 · 시험 수 보고 · lingui --clean · project-detect 두 결함 · [미검증] 네 칸 · 현행화"
slug: kaizen-0924-p10-react-kit
created: "2026-09-25 07:21"
complexity: "복잡"
conditions: 29
status: done
owner_session: de8c7935-a5b6-4df5-9106-fafa73c288a0
conditions_digest: sha256:4cae0f566fefc37d
locked_at: "2026-09-25 08:06"
---

## 배경

이 Phase 의 외부 근거는 `.harness/.meta/evidence/phase10.md` 하나다. 처리 배정표(`.claude/kaizen-input/insights-report.md`)에서 `배정` 칸이
`Phase 10` 인 행은 여섯이다(`F03` · `F05` · `other-kits:P1` · `other-kits:P2` · `other-kits:P5` · `other-kits:P6`). 다른 Phase 행의 비고가
Phase 10 을 가리키는 것이 둘(`F01` — 「리액트 규약에도 되말하기가 없다 — Phase 10 에서 other-kits:P1 과 함께 본다」, `F09` — 「react-preflight 에는
기준 커밋 비교가 없다」)이고, 앞 Phase 가 넘긴 것이 셋이다(`phase1-notes.md` · `phase4-notes.md` · `phase6-notes.md` 의 Phase 10 줄). 러닝북
`Phase 별 추가 과제` 에 Phase 10 줄은 없다. 근거 파일 §3 현행화 점검도 입력이다.

| 키 | 내용 | 이번 처리 |
| --- | --- | --- |
| `F03` · `other-kits:P1` | 재시작이 조용히 실패했는데 갱신했다고 보고, 앱이 옛 데이터를 들고 있었다(§0-b `e163621c` · `3ac429d0`). 리액트 규약에 「지금 보는 화면을 이번 코드가 그렸는지」 확인과 개발 서버 포트 고정이 없다 | 반영 — 규약 §2 비교 반복 순서(주소 대조 · 표식 판정 · 새로고침 → 서버 다시 띄우기 → WASM 다시 빌드 · 확인 전 「갱신했다」 금지 · 최대 3 회), 템플릿 `strictPort: true`, react-run `dev` 포트 Gotcha, react-init devUrl 한 줄 (SK-02 · SK-06 · SK-07) |
| `F05` | 화면 조종 도구를 세 번 고장이라 오진 — 인자 이름 틀림, 따로 뜨는 층, 남의 시뮬레이터(§0-b `a1412bc8`) | 반영 — 규약 §2 「도구가 고장이라 말하기 전에」 세 확인 (SK-03) |
| `F01` (리액트 쪽) | 평평한 줄 대신 카드, 화면 대신 그리로 가는 칩, 고정 범위를 뒤집음(§0-b `cfa1f76f` · `e163621c` · `ad969ac3`) | 반영 — 규약 §1 되말하기 · 화면 자체 · 관례 표 (SK-01). 배정 행 자체는 Phase 6 몫이라 대상 계약 칸은 Phase 6 이 채운다 |
| `other-kits:P2` | `react-kit/scripts/project-detect.sh` 가 없는 값(`"null"`)을 `-n` 으로 재서 참으로 읽는다. 부르는 스킬이 없다 — 지울지 고칠지 사용자 확인 | 반영 — **고친다**(아래 선택). 알려진 답 시험을 짜서 돌리자 결함이 하나 더 나왔다 — 필드 경로의 큰따옴표에 역슬래시가 붙어 jq 가 문법 오류로 늘 `"null"` 을 낸다. 근거 파일의 최소 수정(`!= "null"`)만 하면 jq 가 있는 기계에서 늘 거짓이 된다. 둘 다 고치고 시험을 더한다 (ER-01) |
| `other-kits:P5` | react-preflight 보고에 skipped 칸이 없고 0 개 실행을 통과로 적는다 | 반영 — react-run · react-preflight 형제 둘에 passed · skipped 두 수, 0 passed · skipped 1 이상은 `[미검증]`, `.only` 세기 (SK-08). react-build 는 test 단계가 없다 |
| `other-kits:P6` | react-l10n 기본 흐름의 `lingui extract --clean` | 반영 — 기본 흐름에서 빼고 사용자가 요청할 때만 도는 §4-1(미커밋 변경 확인 · 삭제 수 · 지워진 번역 · 확인 전 커밋 안 함), Gotcha 12, 설계 문서 한 줄 주석 (SK-09) |
| `F09` 비고 · Phase 4 넘김 | `react-preflight` 에 기준 커밋 비교가 없다 — 「필요하면」 | 미반영 — 이 Phase 근거 파일에 기준 커밋 비교 근거가 없다(`git merge-base` 근거는 `phase4.md` 몫). Phase 5 도 같은 사유로 flutter-preflight 를 넘겼다. 다음 사이클 (ER-04) |
| Phase 1 넘김 | `render-evidence-protocol.md:59` 「`[미검증]` 마커와 사유 한 줄 … 부분 완료로 보고」 | 반영 — 같은 모양 여덟 자리(규약 · 다섯 UI 스킬 · react-test · common-gotchas)를 네 칸으로 (SK-04) |
| Phase 6 넘김 | 리액트 규약에 되말하기 · 관례 표 · 반영 확인 · 캡처 점검 · 3 회 상한이 없다 | 반영 — SK-01 ~ SK-03, 숫자(2 개 이상 · 3 회)는 flutter · design 규약과 같다 (AR-02). 세 규약 정본 절은 다음 사이클 Phase 1 몫이라 형제 숫자 문단만 둔다 (SK-05) |
| 근거 §3 현행화 | React 19.3.0 · resolvers 5.9.1 · Lingui 6.8.0 · RHF 7.88.0 · Zod 4.6.5 · Vite 8.3.0, React 19.3 `<ViewTransition>` stable | 지금 틀린 문장 여섯 줄만 고친다(SK-10). Lingui v5 pin 은 그대로(근거 §4 7 번). `project-detection.md:28` 의 `"vite": "8.2.0"` 은 출력 모양 예시라 그대로. `<ViewTransition>` stable 은 조사 기록의 backlog 줄로만 받는다 — 킷 파일에 `<ViewTransition>` 을 canary 라고 적은 곳이 없고(canary 는 `react-screen` Gotcha 11 의 `<Activity />` 에만 있다), Tier 2 를 옮길지는 새 내용이라 다음 사이클 (ER-04) |

고칠 것은 일곱 갈래다.

1. **렌더 증거 규약 (F01 · F03 · F05 · other-kits:P1 · Phase 6 넘김).** `react-kit/references/render-evidence-protocol.md` 은 완료 직전에만 돈다(`:12`).
   §1 Step 0 은 세 줄(`:35-40`)이라 되말하기 · 화면 자체 · 관례 표가 없고, §2(`:48-59`)에 기준 캡처 · 반영 확인 · 캡처 점검 · 도구 오진 확인 · 스스로 고치기 상한이 없다.
   다섯 UI 스킬의 증거 Gotcha(`react-screen:27` · `react-widget:58` · `react-skeleton:23` · `react-responsive:41` · `react-animation:41`)는 「완료 직전에」 만 부른다
2. **개발 서버 포트 (other-kits:P1).** 템플릿 `vite.config.template.ts:25` 는 `port: 5173` 만 둔다. Tauri devUrl(`react-init/SKILL.md:202`)과 harness 검사 포트(`harness-project.yaml.template:98`)가 5173 이다
3. **`[미검증]` 사유 한 줄 (Phase 1 넘김).** 규약 `:59` 와 소비 일곱 자리가 「마커와 사유」 로 남아 있다
4. **시험 수 보고 (other-kits:P5).** `react-preflight/SKILL.md:111` 은 `✓ (N passed)` 만, `react-run/SKILL.md:70` 은 test 전용 칸이 없다
5. **`--clean` (other-kits:P6).** `react-l10n/SKILL.md:150-151` 이 `--clean` 을 기본 흐름의 선택 단계로 둔다
6. **project-detect.sh (other-kits:P2).** `:52` 의 `-n` 비교와 역슬래시 붙은 필드 경로. 시험이 없다
7. **틀린 버전 문장 (근거 §3).** `react-init:18` · `:19` · `:173` · `react-widget:17` · `react-form:27` · `:28`

카이젠 스킬 Gotcha 4(관심사 1~2 개)와 맞춘다: 관심사는 둘이다 — **A 「지금 보는 화면이 이번 코드인가」**(1 · 2 · 3, 규약과 그 소비 자리 전수)와
**B 「검사가 조용히 통과로 보이는 자리」**(4 · 5 · 6 — 0 개 실행 · 조용한 번역 삭제 · 없는 값을 참으로 읽기). 7 은 카이젠 스킬 Step 3 우선순위 「높음 — 잘못된 정보」 인
한 줄 정정이라 새 내용을 더하지 않는다. 관심사 A 는 Gotcha 4 대로 한 관심사를 스킬 다섯 · 참조 둘에 전수 적용한다.

이번 사이클 Phase 1 가이드 변경 넷과 이 킷(오케스트레이터 Gotcha 「Phase 1 에서 가이드를 변경했으면 전수 체크」):

| 변경 | 이 킷의 자리 | 처리 |
| --- | --- | --- |
| §3.7 `[미검증]` 네 칸 | 생성 측 여덟 자리 | SK-04 로 반영 |
| §3.7 작업 자체를 못 한다고 하기 전 네 칸 | 규약 §2 「도구가 고장이라 말하기 전에」 | SK-03 이 세 확인 뒤에만 `[미검증]` 로 가게 한다 |
| §3.7 알려진 답 대조 | 이번에 새로 짜는 측정은 `project-detect-test.sh` 하나 | ER-01 이 손으로 센 답(세 입력 × 두 경로)으로 잰다 |
| agent 가이드 §10 `[미검증:ENV]` · `[미검증:INVALID]` | `react-reviewer.md` 복제 조항 · `react-audit` 미검증 절 | 미반영 — 평가 측 REJECT 문턱을 바꾸는 별도 관심사다. Phase 6 이 design-reviewer 를 같은 사유로 넘겼다 (ER-04) |

## 리서치 소스

외부 조회 0 회. 아래 URL 은 전부 근거 파일 `.harness/.meta/evidence/phase10.md` 에서 가져왔다.

- [Vite `server.port` · `server.strictPort`](https://vite.dev/config/server-options.html#server-port) — 지정 포트가 차 있으면 기본으로 다음 빈 포트로 옮기고, `strictPort: true` 면 멈춘다 (SK-07 · SK-02)
- [Vite CLI](https://vite.dev/guide/cli) — `--port` · `--strictPort` (SK-07)
- [Tauri Vite 설정](https://v2.tauri.app/start/frontend/vite/) — `devUrl` · `port: 5173` · `strictPort: true` 를 함께 두고 고정 포트를 기대한다 (SK-07)
- [Vitest `passWithNoTests`](https://vitest.dev/config/passwithnotests) · [`allowOnly`](https://vitest.dev/config/allowonly) · [API `test.skip` · `skipIf`](https://vitest.dev/api/) — 0 개 실행이 통과가 될 수 있고, 로컬에서 `.only` 가 허용되며, 의도한 skip 도 있다 (SK-08)
- [Lingui CLI](https://lingui.dev/ref/cli) — 기본 `extract` 는 번역을 보존하고 `--clean` 은 소스에서 못 찾은 메시지를 지운다 (SK-09)
- [GNU Bash 조건식](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html) — `-n` 은 길이가 0 이 아니면 참이라 `"null"` 도 참이다 (ER-01)
- 현행화 (SK-10): [React 19.3.0 release](https://github.com/facebook/react/releases/tag/v19.3.0) · [React 19.3 발표](https://react.dev/blog/2026/09/09/react-19-3) ·
  [resolvers v5.9.1](https://github.com/react-hook-form/resolvers/releases/tag/v5.9.1) · [RHF v7.88.0](https://github.com/react-hook-form/react-hook-form/releases/tag/v7.88.0) ·
  [Lingui v6.8.0](https://github.com/lingui/js-lingui/releases/tag/v6.8.0) · [Lingui v6 migration](https://lingui.dev/releases/migration-6) · [Zod v4.6.5](https://github.com/colinhacks/zod/releases/tag/v4.6.5) ·
  [Vite 8 발표](https://vite.dev/blog/announcing-vite8)

근거 파일이 스스로 밝힌 한계를 그대로 옮긴다: 「주소 + 변경 표식 확인」 과 「새로고침 → 재시작 → wasm-build」 순서를 정한 공식 문서는 없다(§5) — 규약에
「공식 문서가 정한 절차가 아니라 이 킷의 규칙이다」 라고 적는다(SK-02). `M>0 이면 무조건 실패` 는 Vitest 의미보다 강하다(§5) — skipped 는 실패로 바꾸지 않고
`[미검증]` 으로 적는다(SK-08). `--clean` 은 금지 대상이 아니라 정상 옵션이다(§2 반대 근거) — Gotcha 12 가 그렇게 적는다. `grep '^-msgid'` 만으로는 지워진 번역을
가를 수 없다(§2) — §4-1 은 지워진 `msgstr` 을 따로 찾는다. `--port` 우회는 Tauri · harness 를 함께 쓸 때 `devUrl` · `vm_port` 도 같은 번호여야 한다(§2) — react-run Gotcha 가 그렇게 적는다.
Context7 은 근거 파일 수집 때도 쓰지 못했다(§5).

내부 입력: 데이터 풀 §0 처리 배정표 · §0-b (`e163621c` · `3ac429d0` · `a1412bc8` · `cfa1f76f` · `ad969ac3`) · §0.5(react 그룹 주입 0 건 — 참고할 메모리 없음) · 앞 Phase notes 여섯.
`validate-plugin.py react-kit` 는 시작 커밋에서 V1~V10 전부 OK 였다.

## GAP 분석 · 개선안 초안

### 1.1 복잡도 4 축

| 축 | 물음 | 값 |
| -- | ---- | -- |
| 레이어 수 | 몇 개 계층을 관통하는가 | 5 — 참조 문서 둘 · 스킬 문서 열하나 · 템플릿과 스크립트(+ 새 시험) · 평가 사례와 설계 · 조사 문서 |
| 공개 API·계약 변경 | 외부에 노출된 형태가 바뀌는가 | 예 — 규약 체크리스트 틀, react-run · react-preflight 보고 형식, 템플릿 기본값(`strictPort`), react-l10n 기본 흐름 |
| 소비면 존재 | 이 형태를 받아 쓰는 반대편이 있는가 | 예 — 아래 Counterpart 표 |
| 회귀 위험 | 기존 동작이 깨질 수 있는가 | 예 — 5173 이 차 있는 기계에서 템플릿 프로젝트의 `dev` 가 옮기지 않고 멈춘다, `--clean` 을 기대하던 흐름이 바뀐다, project-detect 출력 값이 바뀐다 |

넷 가운데 셋이 「예」 이고 공개 형태 변경과 소비면이 둘 다 「예」 라 **복잡**이다. Step 2.5 Counterpart 조건을 넣는다(SK-04 소비 일곱 · SK-08 형제 · SK-11 · AR-02).
기능 조건은 19 개다 — 복잡 9~20 안이다(SKILL.md Step 6.2 둘째 명령으로 이 파일을 세면 19).

### 1.2 설정 리터럴 대조표

| config key | project.yaml 에서 읽은 값 | 계약에 쓴 값 |
| ---------- | ------------------------- | ------------ |
| `commands.analyze` | `bash -n scripts/release.sh` | DG-01 N/A 사유에 그대로 |
| `commands.test` | `bash scripts/release.sh 2>&1 \|\| true` | DG-03 N/A 사유에 그대로 |
| `diagnostics.ide_exclude` | `[]` | DG-02 에 그대로 |
| `contract_categories[].id` / `prefix` | `Skill`/`SK` · `Script`/`SC` · `Error`/`ER` · `Architecture`/`AR` | 조건 섹션 제목과 접두 그대로 |
| `anti_patterns[].id` / `message` | AP-01 · AP-02 · AP-03 · AP-04 | AP-01 · AP-03 · AP-04 선별, message 원문 그대로. AP-02(force push)는 이 Phase 가 밀어 넣지 않아서 뺀다 |

### 1.4 편집 전 감사 (실제로 읽은 줄 — 시작 커밋 `4a8ec55` 판)

| 대상 파일 | 실제 Read 증거 (`파일:라인`) | 발견한 기존 갭·위반 | 계약 조건화 |
| --------- | ---------------------------- | ------------------- | ----------- |
| `react-kit/references/render-evidence-protocol.md` | `:3` (판) · `:12` (완료 직전만) · `:33-46` (§1 세 줄) · `:48-59` (§2, `:59` 사유 한 줄) · `:112-126` (§4, `:122` 옛 미검증 줄) · `:136-148` (References) | 되말하기 · 관례 표 · 반영 확인 · 캡처 점검 · 도구 오진 확인 · 3 회 상한 · 네 칸 없음 | SK-01 ~ SK-05 |
| `react-kit/skills/react-screen/SKILL.md` | `:24` (Gotcha 11 `<Activity />` canary — 근거 없음, 그대로) · `:27` (Gotcha 14) | 완료 직전만 · 사유 | SK-04 · SK-06 |
| `react-kit/skills/react-widget/SKILL.md` | `:17` (19.2+) · `:58` (Gotcha 16) | 같음 · 낡은 버전 | SK-04 · SK-06 · SK-10 |
| `react-kit/skills/react-skeleton/SKILL.md` · `react-responsive/SKILL.md` · `react-animation/SKILL.md` | `:23` · `:41` · `:41` (+ `:43` Library Policy 문단) | 완료 직전만 · 사유 | SK-04 · SK-06 |
| `react-kit/skills/react-test/SKILL.md` | `:42-55` (Gotcha 12 — 이미 0 개 실행을 다룬다) · `:59` (Gotcha 14) | 사유 | SK-04 |
| `react-kit/references/common-gotchas.md` | `:154-164` (G11) · `:174` | 완료 선언 전만 · 사유 | SK-04 |
| `react-kit/templates/vite.config.template.ts` | `:24-26` | `strictPort` 없음 | SK-07 |
| `react-kit/skills/react-init/SKILL.md` | `:18` · `:19` · `:173` (버전) · `:202` (devUrl) | 낡은 버전 · 포트 맞춤 안내 없음 | SK-07 · SK-10 |
| `react-kit/skills/react-run/SKILL.md` | `:13-20` (Gotchas) · `:42` (dev 5173) · `:64-79` (Report) · `:81-87` (Rules) | 포트 · 시험 수 없음 | SK-07 · SK-08 |
| `react-kit/skills/react-preflight/SKILL.md` | `:52-54` (test 단계) · `:100-127` (Report, `:111`) · `:129-136` (Rules) | skipped 칸 없음 · 0 개를 ✓ | SK-08 |
| `react-kit/skills/react-build/SKILL.md` | 전체 (test 단계 없음) | 형제지만 해당 없음 | SK-08 (그대로) |
| `react-kit/skills/react-l10n/SKILL.md` | `:13-42` (Gotchas 1~11) · `:142-166` (§4, `:150-151` `--clean`) · `:291-296` (§7) | 기본 흐름의 `--clean` | SK-09 |
| `react-kit/skills/react-form/SKILL.md` | `:27` · `:28` | 낡은 버전 | SK-10 |
| `react-kit/scripts/project-detect.sh` | `:9-35` (`read_json_field` — 없으면 `"null"`) · `:52` | `-n` 비교 · 역슬래시 붙은 경로 · 시험 없음 | ER-01 |
| `react-kit/evals/evals.json` | `:20-30` (사례 2) · `:154-164` (13) · `:215-224` (18) · `:238-248` (20) | 옛 동작만 기대 | SK-11 |
| `react-kit/evals/test-fixtures/empty-project/package.json` · `react-kit/templates/package.json.template` | 전체 (router-plugin 없음 · `devDependencies` 에 있음) | 시험 입력으로 다시 쓴다 | ER-01 · RE-02 |
| `react-kit/templates/harness-project.yaml.template` | `:96-99` (`vm_port: 5173`) | 읽기만 — 값이 맞는다 | SK-07 |
| `react-kit/agents/react-reviewer.md` | `:163-194` (복제 조항 — 2026-08-13 개정 전 판) · `:233-239` (렌더 산출물 특칙) | 규약 경로만 가리킨다 · 복제 조항 낡음(넘김) | AR-02 · ER-04 |
| `react-kit/skills/react-audit/SKILL.md` | `:278-292` (`🔍 미검증` — 「사유 / 시도한 fallback」) | 복제 조항 5 와 같은 모양이라 그대로 | ER-04 (그대로 둔 곳) |
| `react-kit/references/project-detection.md` | `:20-35` (출력 예시, `:28` vite 8.2.0) | 예시 — 그대로 | ER-04 |
| `docs/react/research-log.md` | `:1-8` (머리 · 최신 항목 2026-08-13) · `:303` · `:392` (canary 대기) | 이번 항목 없음 | SK-10 |
| `docs/react/kit-design/g4-quality.md` | `:554-565` (`--clean` 줄) | 주석이 기본 흐름처럼 읽힌다 | SK-09 |
| `docs/react/kit-design/g6-build-audit.md` | `:52` (dev 5173) · `:144-206` (preflight 절) | 설계 문서는 초판(2026-04-10) 뒤 스킬 변경을 따라가지 않았다 — 이번에 안 고친다 | ER-04 (다음 사이클) |
| `harness/docs/guides/skill-design-guide.md` (읽기만) | `:298-310` (§3.7 5 조항 3 항 네 칸 · `[미검증:INVALID]`) | 규약이 인용할 원문 | AR-02 |
| `flutter-toolkit/references/visual-evidence-protocol.md` · `design-kit/references/visual-change-protocol.md` (읽기만) | Step 0 6 번 · Step 2-5 · §0 3 번 · §3 5 번 | 같은 숫자 원문 | AR-02 |

구현 후보가 둘 이상이었던 곳의 선택:

- **project-detect.sh — 지울지 고칠지 (other-kits:P2).** **고친다.** 사용자 결정 몫이지만 위임 기록(`범위 경계` 절)에 따라 검토자 확인으로 대신한다.
  지우면 설계 문서 `docs/react/kit-design/final-integration.md:243` · `:482` 가 킷 구성으로 적은 파일이 사라져 문서까지 고쳐야 하고 되돌리기 어렵다.
  고치는 것은 한 줄이고 알려진 답 시험이 붙는다. 부르는 스킬이 없다는 사실은 notes 에 남긴다
- **네 칸 범위.** 넘김 원문 한 줄 대 같은 모양 전부. **여덟 자리 전부.** 한 곳씩 고치면 안 고친 곳에서 같은 일이 난다.
  평가 측(`react-reviewer` 복제 조항 · `react-audit` 미검증 절)은 모양이 다르고 평가 가이드와 함께 볼 일이라 넘긴다
- **편집 전 호출을 어디에.** 다섯 스킬 모두 증거 Gotcha 바로 다음 번호의 새 Gotcha 로 둔다 — 스킬마다 Process 구조가 달라 한 자리로 맞출 곳이 Gotcha 뿐이다
- **숫자(2 개 이상 · 3 회)를 어디에.** 규약 한 곳에만 둔다. 스킬 Gotcha 는 규약 절 이름만 가리킨다(RE-02) — Phase 6 notes 가 「임계값을 스킬 다섯 자리에 다시 적어 다음 변경 때 막을 장치가 없다」 고 적었다
- **skipped 1 이상.** 실패 대 `[미검증]`. **`[미검증]`.** 근거 §2 반대 근거 — 의도한 skip · skipIf 가 있다. passed 0 도 `[미검증]` 이다(실행을 못 한 것이 아니라 잰 것이 없다)
- **`--clean` 을 어떻게.** 금지 대 기본 흐름에서 빼기. **빼기.** 근거 §2 — 정상 옵션이다
- **포트가 찼을 때.** 다른 포트 안내 대 멈춤. **멈춤이 기본**(템플릿) · 다른 포트가 필요하면 `--port` 와 함께 `devUrl` · `vm_port` 를 같은 번호로(Gotcha)
- **현행화.** 모든 버전 줄 대 지금 틀린 문장만. **지금 틀린 문장만**(여섯). 조사 기록의 옛 라운드 표는 그 날짜의 사실이라 고치지 않고 새 라운드 표에 현행 값을 적는다
- **시험 수 `[미검증]` 에 네 칸을 붙일지.** **안 붙인다.** react-run · react-preflight 의 `[미검증] 0 passed …` · `[미검증] N passed · M skipped` 는 규약 §3 (b)(c) 의
  「비어 있는 증거 범위」 표시다 — 두 수 · skipped 범위 · `.only` 수가 그 내용이다. 네 칸은 §2 의 환경상 불가(채널이 막혀 잴 수 없음)에 붙는다. SK-04 는 §2 · §4 와
  소비 일곱 자리만 재고, SK-08 은 두 수 모양을 잰다
- **지워진 번역 찾기 명령의 설명.** 단정 대 가능성. **가능성.** `^-(msgstr "[^"]|")` 의 `-"` 는 여러 줄 `msgid` 의 이어진 줄도 잡는다 — 「지워졌을 수 있다 — 출력 줄을 보고 가른다」
  로 쓴다. 더 자주 멈추는 쪽으로만 틀리니 명령은 그대로 둔다

### Counterpart — 바뀌는 형태를 받아 쓰는 반대편

| 파일 | 인용 | 이번 처리 |
| --- | --- | --- |
| `react-kit/skills/` 다섯 UI 스킬 · `react-test` · `react-kit/references/common-gotchas.md` G11 | 규약을 부른다 · `[미검증]` 사유 | 편집 전 Gotcha · 네 칸 — SK-04 · SK-06 |
| `react-kit/agents/react-reviewer.md` `:238` · `:334` | 규약 경로를 가리킨다 | 경로 · 절 이름이 그대로라 읽기만 — AR-02 |
| `react-kit/evals/evals.json` 사례 2 · 13 · 18 · 20 | 화면 추가 · 번역 · test 서브커맨드 · preflight | 새 동작 단언 — SK-11 |
| `react-kit/skills/react-build/SKILL.md` | run · preflight 형제 | test 단계가 없어 그대로 — SK-08 |
| `react-kit/templates/harness-project.yaml.template:98` · `react-kit/skills/react-init/SKILL.md:202` | 5173 을 쓴다 | 앞은 읽기만(값이 맞는다), 뒤는 한 줄 — SK-07 |
| `docs/react/kit-design/g4-quality.md:564` | `--clean` 을 명령 목록에 둔다 | 주석 — SK-09 |
| `docs/react/kit-design/g6-build-audit.md` | dev 포트 · preflight 절 | 이번에 안 고친다 — ER-04 넘김 |
| `.github/workflows/ci.yml` | 새 시험을 돌릴 자리 | Phase 가 못 고친다 — notes 에 넣을 줄 (ER-04) |
| `harness/docs/guides/skill-design-guide.md` §3.7 · flutter · design 규약 | 네 칸 원문 · 같은 숫자 | 읽기만 — AR-02 |

### 개선안 초안

정확한 문구는 스크래치 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p10d/mock.py`
(sha256 앞 16 자리 `db181ec91592e78d`)가 시작 커밋 판에 적용하는 44 치환 · 새 파일 하나 그대로다(`python3 mock.py <트리>` — 옛 문자열이 정확히 한 번 있어야 적용하고, 아니면 멈춘다).
BUILD 는 `mock.py` 를 작업 폴더에 그대로 돌린다(`mock applied 45` 가 나와야 한다 — 치환 44 와 새 파일 1 을 합친 수. 시작 커밋 판을 푼 새 사본에서 `mock applied 45` · 종료 코드 0 을 확인했다).
돌리기 전에 `git status --short -- react-kit docs/react` 가 빈 출력인지 본다 — 두 번째 실행은 첫 파일에서 `MOCK_FAIL` 로 멈추고, 중간에 멈추면 앞서 쓴 파일이 남는다. 요지:

- 규약 1.1.0 — 두 번 실행 머리, 형제 숫자 문단, 2026-09-24 사고 문단, §1 여섯 줄, §2 네 칸 · `### 비교 반복 순서 — 지금 보는 화면이 이번 코드인가` · `### 캡처 점검 목록` ·
  `### 도구가 고장이라 말하기 전에`, §4 체크리스트 새 줄 일곱 · 옛 미검증 줄 교체, References 넷
- 다섯 UI 스킬 — 증거 Gotcha 의 사유를 네 칸으로, 다음 번호에 `**기준 캡처는 편집 전에 찍는다**` Gotcha. react-animation 은 옛 번역투 한 곳(「호출된다는 사실」)도 고친다 —
  고치는 줄에 걸린다. react-test Gotcha 14 · common-gotchas G11 네 칸
- 템플릿 `strictPort: true` + 이유 주석, react-run Gotcha 둘 · Report · Rules, react-preflight Report · Rules, react-init devUrl 한 줄
- react-l10n 기본 흐름 두 단계 · Gotcha 12 · §4-1, g4-quality 주석 한 줄
- project-detect.sh 두 결함 + 이유 주석 두 줄, 새 시험 `react-kit/evals/scripts/project-detect-test.sh`(모드 100755)
- 현행화 여섯 줄, evals 단언 넷, `docs/react/research-log.md` 머리에 2026-09-25 항목(1.4.0)

## 범위 경계

- 이 Phase 시작 HEAD: `4a8ec55f4d874eaaed083af9621f9679693cbdb6`. 범위 상한은 개정 파일 `.harness/sprint-amendments-kaizen-0924-p10-react-kit.md` 의 `end_sha:`
  마지막 값이다. 여러 Phase 가 같은 가지 `kaizen/2026-09-24` 에 동시에 커밋하므로 `HEAD` 로 재지 않는다
- 고치는 파일은 열아홉이다(새 파일 하나 포함) — 아래 블록이 그 목록이다(`harness/README.md` §커밋 안전 훅 이 정한 범위 선언 자리). `.harness/` 쪽은 이 계약 · 개정 파일 ·
  QA 피드백 · `.harness/.meta/kaizen-0924/phase10-notes.md` · `.harness/.meta/kaizen-0924/phase10-review.md` 를 쓴다 — 슬러그를 나열하지 않고 AR-01 셋째 값 `verify_seal` 로 잰다.
  AR-01 다섯째 값이 이 블록과 측정 공통 정의의 `FILES` 가 같은지 잰다

```text
# sprint-scope
docs/react/research-log.md
docs/react/kit-design/g4-quality.md
react-kit/references/render-evidence-protocol.md
react-kit/references/common-gotchas.md
react-kit/skills/react-screen/SKILL.md
react-kit/skills/react-widget/SKILL.md
react-kit/skills/react-skeleton/SKILL.md
react-kit/skills/react-responsive/SKILL.md
react-kit/skills/react-animation/SKILL.md
react-kit/skills/react-test/SKILL.md
react-kit/skills/react-run/SKILL.md
react-kit/skills/react-preflight/SKILL.md
react-kit/skills/react-l10n/SKILL.md
react-kit/skills/react-init/SKILL.md
react-kit/skills/react-form/SKILL.md
react-kit/templates/vite.config.template.ts
react-kit/scripts/project-detect.sh
react-kit/evals/scripts/project-detect-test.sh
react-kit/evals/evals.json
.harness/
```

- **이 Phase 의 커밋 메시지에는 전부 `Co-Authored-By` 줄 바로 위에 서명 줄 `Kaizen-Phase: kaizen-0924-p10-react-kit` 한 줄을 넣는다** (봉인 커밋 포함).
  AR-01 · ER-04 · SC-00 · DG-01 · DG-03 · DG-04 · DG-06 이 이 줄로 이 Phase 커밋을 가린다(`harness/references/contract-schema.md` §여러 주체가 한 가지에 커밋할 때 선택지 B).
  서명을 빠뜨린 커밋은 서명 줄 목록에 안 보이므로 AR-01 첫째 값과 ER-04 셋째 값은 경로로 직접 센다.
  FIX 가 커밋을 더할 때도 넣고, 개정 파일에 `end_sha:` 줄을 덧붙인다(옛 줄은 지우지 않는다). notes 커밋도 이 Phase 커밋이다 — notes 를 커밋한 뒤 그 sha 로
  `end_sha:` 줄을 하나 더 덧붙여 커밋한다
- 구현 커밋은 `git add -- <파일…> && git commit -o -- <파일…>` 로 열아홉 파일만 싣는다. 새 시험 파일은 `add` 가 먼저다. `docs/react/` 둘과 `react-kit/` 열일곱을
  두 커밋으로 나눠도 된다 — 둘 다 이 킷 몫이라 `validate-post-kaizen.py` scope-isolation 에 걸리지 않는다(예행에서 두 커밋으로 확인). 새 시험 파일의 실행 비트는
  `git ls-tree` 에서 `100755` 여야 한다(ER-01)
- 측정이 기대는 제목 · 줄 머리는 이름을 바꾸지 않는다: `## 1. Step 0` · `## 2. 증거 등급` · `### 비교 반복 순서 — 지금 보는 화면이 이번 코드인가` · `### 캡처 점검 목록` ·
  `### 도구가 고장이라 말하기 전에` · `## 3. 공허한 증거` · `### (b) 0 테스트 green run` · `### (c) `.only` 로 좁혀진 green run` · `## 4. 완료 전 체크리스트` · `## References` ·
  `## 왜 필요한가` (규약) · `# Gotchas` (UI 스킬 다섯) · `## Report Format` · `## Rules` (run · preflight) · `### 4. codegen 흐름` · `#### 4-1. 안 쓰는 키 정리 — 사용자가 요청할 때만` ·
  `## Gotchas` (l10n) · `### 단계 10` (init) · `## [2026-09-25] - Phase 10 kaizen` · `## [2026-08-13]` (조사 기록) · `## 3.7.` (skill-design-guide — 읽기만).
  이름이 바뀌면 `sect` 가 빈 글을 내 값이 0 이 된다 — FAIL 쪽으로 틀린다
- 공유 파일(`.claude-plugin/marketplace.json` · `react-kit/.claude-plugin/plugin.json` 버전 · 루트 `README.md` · 루트 `CLAUDE.md` · `docs/` HTML · 처리 배정표 · 감사 로그 ·
  실패 횟수 파일 · `.github/workflows/ci.yml` · `.harness/stale-values.yaml`)과 다른 Phase · 레포 전용 파일(`harness/` · `scripts/` · `.claude/skills/` · `design-kit/` ·
  `flutter-toolkit/`)과 `react-kit/README.md` 는 건드리지 않는다 — ER-04 셋째 값. react-kit README 의 AUTO 구간은 스킬 frontmatter 를 읽는데 frontmatter 를 바꾸지 않는다(AP-04).
  문서 사이트 재생성은 Final F2 몫이라 DG-06 에서 `docs-site-regen` 을 뺀다
- QA(`harness:qa-evaluator`)는 설치본이다 — 이 Phase 가 고치는 파일에 harness 파일은 없다
- 사용자 승인(Step 5) 대체: 사용자가 「자동으로 끝까지 알아서 진행해 내 허락이 필요한건 코덱스로 리서치나 검토받고」라고 위임했다(세션
  `de8c7935-a5b6-4df5-9106-fafa73c288a0` 기록 queued_command `2026-09-24T04:04:16.964Z`). Codex 사용량 한도가 소진돼(오류 원문 「You've hit your usage limit … try
  again at 11:05 PM」, 2026-09-24) 독립 Claude 검토자(REVIEW 에이전트)가 대신한다. 이어 사용자가 「코덱스 대신에 그냥 너가 알아서 진행하라고」라고 명시했다(같은 세션
  기록 user `2026-09-24T11:54:58.940Z`). 검토 결과 파일: `.harness/.meta/kaizen-0924/phase10-review.md`. 처리 배정표 `other-kits:P2` 비고의 「지울지 고칠지 사용자 확인」 도
  이 위임으로 검토자가 확인한다 — 초안은 「고친다」 를 고르고 사유를 위 `선택` 에 적었고, 1 회차 검토가 「고친다」 에 동의했다.
  1 회차 `VERDICT: CHANGES` — 고칠 것 둘(`mock applied` 확인 값 · ER-04 토큰과 기대값)과 권하는 것 여덟을 초안이 모두 반영했다(2 회차 검토 `1 회차 지적 반영 확인` 표).
  2 회차 `VERDICT: CHANGES` (마지막 VERDICT) — 고칠 것 하나(DG-05 (c) · (e) 가 레포 전체의 종료 코드 0 을 요구해 다른 Phase 몫 변경으로 떨어진다)를 BUILD 가
  봉인 전에 검토의 「고칠 문구」 그대로 반영했다(`m.sh` `DG-05)` 마지막 줄 · 조건 줄 · 측정 괄호 · 표 행 · 아래 DG-05 (e) 범위 줄). 조건 줄에 새로 넣은 문구 가운데
  코드 조각 `검사 범위: 소스 디렉토리` 뒤의 빈칸만 뺐다 — 코드 조각 안 끝 빈칸이 마크다운 경고(MD038)를 내고, 측정 명령의 정규식은 빈칸을 그대로 둔다.
  권하는 것 둘(`mock.py` 는 한 번만 돌린다 · Phase 8 · 9 DG-05 의 같은 구멍을 notes 에 남긴다)도 반영했다. 남은 고칠 것은 0 이라 3 회차 검토 없이 봉인한다
- 오라클 한계: SK-11 은 평가 사례의 **구조**만 잰다(`scripts/run-evals.py` 는 스킬을 실행하지 않는다). 규약이 실제 세션에서 지켜지는지는 LLM 동작이라 결정론 측정이 없다 —
  조건은 문서 문장 · 템플릿 값 · 스크립트 동작까지만 건다
- 오라클 해소: SK-01 ~ SK-10 — 산출물이 문서 문장 자체라 정해진 절 · 줄에 정해진 문장이 있는지가 판정이다. `sect` 가 코드 펜스를 건너뛰고 절을 자르고, `gline` 이
  한 줄짜리 Gotcha 를 고른다. 시작 커밋 판에서 새 문장 0 · 옛 문장 1 이상을 봉인 전에 확인했고, 문장 하나만 지운 사본 126 개에서 그 조건의 출력이 바뀌었다(`회귀 게이트` 절)
- 오라클 해소: SK-11 · ER-01 · DG-05 — 시험 · 검사 스크립트를 실제로 돌린 출력이다. ER-01 은 알려진 답(손으로 센 세 입력 × 두 경로)과 음성 대조 셋이 붙어 있다
- 오라클 해소: ER-02 · ER-03 · AP-01 · AP-03 · DG-02 — 편집 전 판과 파일마다 비교한 더한 줄 계산이다. 각각 양성 대조가 붙어 있다
- 오라클 해소: ER-04 · AR-01 · SC-00 · DG-01 · DG-03 · DG-04 · DG-06 — 커밋 기록과 봉인 검증 함수를 실제로 돌린 출력이다. 예행 저장소 변형 다섯이 양성 대조다
- 커버리지 해소: SK-01 ~ SK-11 · ER-01 · AR-02 — 산문의 파일 이름은 측정 `m <조건 ID>` 가 공통 정의의 변수(`$RL` · `$G4` · `$REP` · `$CG` · `$SCR` · `$WID` · `$SKL` ·
  `$RSP` · `$ANI` · `$TST` · `$RUN` · `$PRF` · `$L10` · `$INI` · `$FRM` · `$VT` · `$PDS` · `$PDT` · `$EV`)로 연다(파일과 변수의 대응은 `common.sh` 머리). 토큰은 `m.sh` 의 같은 ID 갈래에
  글자 그대로 있다. 읽기만 하는 파일(`react-kit/templates/harness-project.yaml.template` · `react-kit/templates/package.json.template` · `react-kit/skills/react-build/SKILL.md` ·
  `react-kit/agents/react-reviewer.md` · `react-kit/evals/test-fixtures/` · `harness/docs/guides/skill-design-guide.md` · `flutter-toolkit/references/visual-evidence-protocol.md` ·
  `design-kit/references/visual-change-protocol.md`)은 `m.sh` 갈래 안에 경로 그대로 있다. SK-04 · SK-10 의 `react-kit/` 는 `grep -r` 의 인자(`"$E/react-kit"`),
  SK-04 의 `SKILL.md` 는 소비 스킬 경로의 끝, SK-08 의 `.only` 와 SK-10 의 `@lingui/core@6.6.0` · `v7.71.x` 는 `m.sh` 의 토큰 · 정규식 인자다
- 커버리지 해소: ER-02 · ER-04 — `.harness/.meta/kaizen-0924/phase10-notes.md` · `.harness/.meta/evidence/phase10.md` 는 공통 정의의 `$NOTES` · `$EVID` 다. ER-04 의 넘김 문자열과
  공유 경로는 `m.sh` `ER-04)` 갈래 `toks` · `not_other` 의 인자다
- 커버리지 해소: AR-01 — `docs/react/` 는 `unsigned_on` 의 인자, `.harness/` 는 `scope` 블록 줄과 `verify_seal` 이 도는 폴더, `harness/references/contract-schema.md` 는 권장 형태의 출처다
- 검출기는 공백 든 코드 조각 안의 인자를 읽지 못한다 — 위 해소 줄이 전부 그 경우다
- 편집 전부터 있던 경고(markdownlint MD060 · MD032 등)는 범위 밖이다 — DG-02 는 더한 줄의 새 경고만 잰다
- notes 에 함께 적는다(조건으로는 재지 않는다): 「그대로 둔 곳」 에 `react-kit/skills/react-audit/SKILL.md:279` 의 「<사유> / 시도한 fallback」 과 `react-reviewer.md:183` —
  복제 조항 5 의 보고 모양이라 그대로 둔다. `project-detect.sh` 를 부르는 스킬이 없다는 사실과, 킷이 이 스크립트를 쓰게 할지는 다음 사이클 판단이라는 한 줄.
  「다음 사이클 메모」 에 넷 — `react-kaizen` Step 6 의 계약 경로(`.harness/history/…`)와 「병렬 실행 중 git 쓰기 금지」 가 지금 러닝북과 어긋난다 · 규약이 react-run Gotcha 를
  이름으로 가리키므로 그 Gotcha 머리를 바꾸면 AR-02 첫 값이 떨어진다 · 설계 문서 `kit-design/` 가 초판 뒤 스킬 변경을 따라가지 않는다 ·
  `scripts/check-stale-values.py` 의 `SOURCE_DIRS` 에 `react-kit/references` 가 없다(`scripts/` 라 Phase 4 몫) · Phase 8 계약 DG-05 의 「stale_rc 는 0 또는 1」 과
  Phase 9 계약 DG-05 (c) 의 「종료 코드 0 또는 1 이고 출력에 열한 파일 경로가 0 건」 은 검사기가 멈춰도 통과한다(검사기가 돌았다는 줄을 함께 세지 않는다 — 2 회차 검토가 등록 파일을 지운 사본으로 확인).
  「넘기는 것」 에 하나 더 — 문서 사이트 `docs/react-kit/render-evidence-protocol.html` 은 `v1.0.0 · 2026-07-27` 판으로 남는다. 다시 만드는 것은 Final F2 몫이다
  (`scripts/detect-docs-drift.py` 가 `react-kit/references/` → `docs/react-kit/` 로 이어 이 페이지를 잡는다)
- DG-05 (e) 가 보는 범위: `scripts/check-stale-values.py` 의 `SOURCE_DIRS` 에 `docs/react` 는 있지만 `react-kit/references` 는 없다. 그래서 (e) 는 열아홉 파일 가운데
  `docs/react/` 두 파일만 본다 — 등록된 옛 값을 규약 파일에 넣은 사본은 `stale_rc=0 ran=1 0` 이다. 검사기 범위는 이 Phase 가 못 고친다(`scripts/`)
- 기능 조건 19 · 전체 조건 줄 29
- 사용자가 할 일: 없음

## 회귀 게이트 — 측정 공통 정의와 봉인 전 실측

모든 조건의 측정은 아래 `common.sh` 와 `m.sh` 를 차례로 `.` 으로 읽은 **bash** 셸에서 돈다 — `common.sh` 는 bash 가 아니면 `NOT_BASH` 를 찍고 종료 코드 2 로 끝난다
(Claude Code 의 zsh 는 따옴표 없는 변수를 쪼개지 않고 `grep` 을 다른 검색 프로그램으로 바꿔 부른다 — Phase 5 실측). `m` 은 도우미 함수와 두 판 폴더가 없으면
`HELPER_MISSING` · `SNAPSHOT_MISSING` 을 내고 멈춘다 — 그래서 조건마다 `type m` 하나로 정의 확인을 대신한다. 예행 값은 bash 5.3.9 와 `/bin/bash` 3.2.57 두 해석기에서 한 글자도 다르지 않았다(ER-01 의 시험은 두 해석기를 따로 돈다). zsh 에서 `common.sh` 를 읽으면 `NOT_BASH` · 종료 코드 2 다.
두 블록과 `new-warnings.sh` 를 각 블록 첫 `#` 주석 줄(셔뱅 다음)의 이름 그대로 한 폴더에 저장하고 그 폴더를 `K` 에 넣는다. `END_UNRESOLVED` 가 찍히면 셸이 종료 코드 2 로 끝난다.
`new-warnings.sh` 옆에는 `node_modules` 를 `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0/scratchpad/p1build/node_modules` 로 잇고
`cfg.markdownlint-cli2.jsonc` = `{ "config": { "MD013": false } }` 를 둔다 — 준비 단계 실측(2026-09-25): 그 자리의 `.bin/markdownlint-cli2 --version` 첫 줄이
`markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)`. 없으면 그 폴더에서 `npm install --no-save markdownlint-cli2@0.23.2` 부터 돌린다.
그 밖의 준비 단계 실측(2026-09-25): `command -v shellcheck` → `/opt/homebrew/bin/shellcheck` (0.11.0) · `command -v jq` → `/usr/bin/jq` (jq-1.7.1-apple) · `/bin/bash --version` 3.2.57 ·
`python3` 있음. ER-01 은 shellcheck 가 없으면 `SHELLCHECK_MISSING` 을 내고 멈춘다. 새 시험은 jq 가 없거나 숨겨지지 않으면 종료 코드 2 로 멈춘다(가짜 `jq` 를 PATH 에 넣은 사본에서 `jq 가 숨겨지지 않았다` · 2 확인).
`common.sh` 의 `R` 은 예행 저장소를 가리킬 때만 쓴다 — 비우면 작업 폴더다. 두 판을 `${TMPDIR:-/tmp}/p10m.XXXXXX` 에 푸니 `TMPDIR` 를 스크래치 폴더로 두고 읽는다.

```bash
# common.sh — 측정 공통 정의. bash 로 읽는다 (zsh 는 배열 첨자가 1 부터이고 따옴표 없는 변수를 쪼개지 않는다)
[ -n "${BASH_VERSION:-}" ] || { echo "NOT_BASH — bash -c 안에서 다시 읽는다"; exit 2; }
export LC_ALL=C.UTF-8   # 번역투 정규식이 글자 단위로 돌아야 한다
cd "${R:-/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/kaizen-0924}" || exit 2
B=4a8ec55f4d874eaaed083af9621f9679693cbdb6                  # 이 Phase 시작 HEAD
SIG='Kaizen-Phase: kaizen-0924-p10-react-kit'
CF=.harness/sprint-contract-kaizen-0924-p10-react-kit.md
AM=.harness/sprint-amendments-kaizen-0924-p10-react-kit.md
NOTES=.harness/.meta/kaizen-0924/phase10-notes.md
EVID=.harness/.meta/evidence/phase10.md
END=$( [ -f "$AM" ] && sed -n 's/^end_sha:[[:space:]]*//p' "$AM" | tail -1 )
if [ -z "$END" ] || ! git rev-parse -q --verify "$END^{commit}" >/dev/null; then
  echo "END_UNRESOLVED — 측정을 멈춘다. HEAD 로 바꿔 재지 않는다"; exit 2
fi
: "${K:?도우미 폴더를 K 에 넣는다}"
RL=docs/react/research-log.md
G4=docs/react/kit-design/g4-quality.md
REP=react-kit/references/render-evidence-protocol.md
CG=react-kit/references/common-gotchas.md
SCR=react-kit/skills/react-screen/SKILL.md
WID=react-kit/skills/react-widget/SKILL.md
SKL=react-kit/skills/react-skeleton/SKILL.md
RSP=react-kit/skills/react-responsive/SKILL.md
ANI=react-kit/skills/react-animation/SKILL.md
TST=react-kit/skills/react-test/SKILL.md
RUN=react-kit/skills/react-run/SKILL.md
PRF=react-kit/skills/react-preflight/SKILL.md
L10=react-kit/skills/react-l10n/SKILL.md
INI=react-kit/skills/react-init/SKILL.md
FRM=react-kit/skills/react-form/SKILL.md
VT=react-kit/templates/vite.config.template.ts
PDS=react-kit/scripts/project-detect.sh
PDT=react-kit/evals/scripts/project-detect-test.sh
EV=react-kit/evals/evals.json
FILES=("$RL" "$G4" "$REP" "$CG" "$SCR" "$WID" "$SKL" "$RSP" "$ANI" "$TST" "$RUN" "$PRF" "$L10" "$INI" "$FRM" "$VT" "$PDS" "$PDT" "$EV")
MDS=("$RL" "$G4" "$REP" "$CG" "$SCR" "$WID" "$SKL" "$RSP" "$ANI" "$TST" "$RUN" "$PRF" "$L10" "$INI" "$FRM")
FOUR='`[미검증]` 을 달고 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령 — 규약 §2)'
T=$(mktemp -d "${TMPDIR:-/tmp}/p10m.XXXXXX") || exit 2; mkdir -p "$T/B" "$T/E"
# 두 판을 풀어 둔 폴더에서 잰다 — 작업 폴더에 남은 다른 Phase 의 미커밋 변경이 끼지 않는다
git archive "$B" | tar -x -C "$T/B"; git archive "$END" | tar -x -C "$T/E"
# sect <파일> <제목 앞부분> — 그 제목부터 같은 깊이 이하의 다음 제목 전까지. 코드 펜스 안의 `#` 줄은 제목으로 보지 않는다
sect() { awk -v h="$2" '
  /^[[:space:]]*(```|~~~)/ { fence = !fence }
  !f && !fence && index($0, h) == 1 { f = 1; lvl = match($0, /[^#]/) - 1; print; next }
  f && !fence && /^#+ / { l = match($0, /[^#]/) - 1; if (l <= lvl) exit }
  f' "$1"; }
# gline <파일> <줄 앞부분> — 그 앞부분으로 시작하는 줄. Gotcha 와 표 행은 한 줄이다
gline() { awk -v p="$2" 'index($0, p) == 1' "$1"; }
# toks <글> <토큰…> — 토큰마다 글 안에서 그 토큰이 든 줄 수
toks() { local s="$1"; shift; for t in "$@"; do printf '%s ' "$(printf '%s\n' "$s" | grep -cF -- "$t")"; done; echo; }
# seq_ok <글> — 줄 머리 `N. **` 번호가 1 부터 빠짐없이 이어지면 「1 마지막번호」, 아니면 「0 번호들」
seq_ok() { printf '%s\n' "$1" | grep -oE '^[0-9]+\. \*\*' | tr -dc '0-9\n' | awk '{a[NR]=$1} END{ok=1; for(i=1;i<=NR;i++) if (a[i]+0 != i) ok=0; printf "%d %d\n", ok, NR}'; }
url()   { grep -oE 'https?://[^ )>"`]+' | sed -E 's/[.,;:]+$//' | sort -u; }
# 편집 전 판에 없는 새 파일은 빈 파일과 비교한다
added() { for f in "${FILES[@]}"; do if [ -f "$T/B/$f" ]; then git diff --no-index -U0 "$T/B/$f" "$T/E/$f"; else git diff --no-index -U0 /dev/null "$T/E/$f"; fi; done | grep '^+' | grep -v '^+++'; }
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
```

```bash
# m.sh — 조건마다 재는 값을 한 줄씩 낸다. common.sh 를 읽은 bash 에서 `m <조건 ID>` 로 부른다
m() {
  local E=$T/E S L fn f n
  # 도우미가 하나라도 없으면 grep -c 가 조용히 0 을 낸다 — 멈춘다
  for fn in sect gline toks seq_ok url added mine unsigned_on not_other my scope fm_get verify_seal; do
    type "$fn" >/dev/null 2>&1 || { echo "HELPER_MISSING $fn"; return 2; }; done
  [ -n "${T:-}" ] && [ -d "$T/B" ] && [ -d "$E" ] || { echo "SNAPSHOT_MISSING"; return 2; }
  case "$1" in
  SK-01)  # 규약 §1 Step 0 — 되말하기 · 화면 자체 · 관례 표
    S=$(sect "$E/$REP" '## 1. Step 0')
    toks "$S" '편집 전에 다음 6 줄을 응답에 남긴다' '4. **되말하기**:' '두 갈래로 읽히면 묻고 시작한다' '5. **화면 자체**:' \
      '그 화면으로 들어가는 진입점(버튼·링크·칩)이나 화면을 흉내 낸' '라우트 경로(주소)를 함께 적는다' \
      '6. **관례 표**: 같은 역할의 서로 다른 기존 화면 **2 개 이상**을 Read 해서' '앱 코드가 실제로 import 하는지 grep 으로 확인하고' \
      '**grep 에 나오지 않은 컴포넌트 이름은 쓰지 않는다.**' '`관례 없음 — 같은 역할 기존 화면 N 개`' '`관례 없음 — 앱 코드 없음`'
    toks "$S" '편집 전에 다음 3 줄을 응답에 남긴다' ;;
  SK-02)  # 규약 §2 비교 반복 순서 — 지금 보는 화면이 이번 코드인가
    S=$(sect "$E/$REP" '### 비교 반복 순서 — 지금 보는 화면이 이번 코드인가')
    toks "$S" '1 은 편집 전에, 3 부터는 완료 직전에 한다' '이번 변경으로 반드시 달라져야 할 눈에 보이는 표식 하나를 이때 정한다' \
      '3. **반영 확인** — 지금 보는 화면을 이번 코드가 그렸는지부터 본다' '`Local:` 주소와 브라우저(브라우저 도구 포함)가 연 주소를 대조한다' \
      '새로 찍은 캡처에서 1 의 표식이 바뀌었는지로 판정한다' '모듈 교체(HMR) 로그나 새로고침 성공만으로 판정하지 않는다' \
      '브라우저 새로고침 → 개발 서버를 멈추고 다시 띄우기 → Rust(`crates/core/`)를' '`/react-run wasm-build` 뒤 서버 다시 띄우기 순서로 가고, 시도한 것을 적는다' \
      '반영이 확인되기 전에는 「갱신했다」 고 말하지 않는다' '**스스로 고치기는 최대 3 회**다' '공식 문서가 정한 절차가 아니라 이 킷의 규칙이다'
    # 새 소절 셋이 §2 안에 있다 — `## 2.` < 비교 반복 < 캡처 점검 < 도구 < `## 3.` 이면 1
    awk '/^## 2\. 증거 등급/{a=NR} /^### 비교 반복 순서/{b=NR} /^### 캡처 점검 목록/{c=NR} /^### 도구가 고장이라 말하기 전에/{d=NR} /^## 3\. 공허한 증거/{e=NR} END{print (a && b && c && d && e && a<b && b<c && c<d && d<e) ? 1 : 0}' "$E/$REP" ;;
  SK-03)  # 규약 §2 캡처 점검 목록 넷 · 도구가 고장이라 말하기 전 셋
    S=$(sect "$E/$REP" '### 캡처 점검 목록')
    toks "$S" '1. **글자 넘침**' '2. **깨진 글리프**' '3. **칩·뱃지와 줄 모양**' '4. **디버그 겹침**' \
      '하나라도 걸리면 그 캡처로 PASS 를 주지 않는다' '실제 서비스 글꼴로 그리지 않은 캡처로는 글자 모양을 판정하지 않는다' '넘침은 데이터를 고쳐 재현하지 말고'
    S=$(sect "$E/$REP" '### 도구가 고장이라 말하기 전에')
    toks "$S" '셋을 확인하고 그 출력을 응답에 남긴다' '실패한 호출의 인자 이름을 도구 설명의 인자 목록과 대조한다' \
      '도구가 연 페이지가 내가 띄운 서버인지 확인한다' '따로 뜨는 층의 요소는 페이지 전체 스냅샷에서 한 번 더 찾는다' ;;
  SK-04)  # [미검증] 네 칸 — 규약 §2 · §4, 소비 일곱 자리, 옛 모양 0
    S=$(sect "$E/$REP" '## 2. 증거 등급')
    toks "$S" '그 항목에 `[미검증]` 을 달고 네 칸을 채워' '**막는 것**(실행한 명령과 그 실패 출력)' '**시도한 우회**(세 확인과 시도한 채널' \
      '**통제 불가 사유**(한 문장)' '**재검증 명령**(채널이 생기면 돌릴 명령)' '평가 측이 `[미검증:INVALID]` 로 센다'
    S=$(sect "$E/$REP" '## 4. 완료 전 체크리스트')
    toks "$S" '- 미검증: N 건 [항목 — 막는 것 — 시도한 우회 — 통제 불가 사유 — 재검증 명령]' '- [미검증]: <항목 + 사유 + 시도한 fallback>'
    for f in "$SCR" "$WID" "$SKL" "$RSP" "$ANI" "$TST" "$CG"; do printf '%s ' "$(grep -cF -- "$FOUR" "$E/$f")"; done; echo
    # 옛 모양 — 한 줄에 「[미검증] (마커)와/+ 사유」, 줄이 갈려 「마커와 사유」 로 시작하는 줄
    { grep -rnE '\[미검증\]`? ?(마커)? ?(와|\+|과) ?(사유|이유)' "$E/react-kit"; grep -rnE '^마커와 사유' "$E/react-kit"; } | grep -c . ;;
  SK-05)  # 규약 머리 · §4 체크리스트 줄 · 참고 URL
    echo "$(fm_get "$E/$REP" version) $(fm_get "$E/$REP" last_updated)"
    toks "$(awk '/^## 왜 필요한가/{exit} 1' "$E/$REP")" '이 규약은 **편집 전과 완료 직전 두 번** 실행한다' \
      '- 편집 전: §1 Step 0 과 §2 비교 반복 순서의 1 번(기준 캡처)' '- 완료 직전: §2 비교 반복 순서의 3 번(반영 확인)부터 §4 체크리스트까지' \
      '**형제 규약과 같은 숫자:**' '생기기 전까지는 한쪽 값을 바꾸면 다른 두 쪽도 같이 바꾼다' '**완료를 선언하기 직전**에 실행하는 증거 규약이다'
    S=$(sect "$E/$REP" '## 4. 완료 전 체크리스트')
    toks "$S" '- 되말하기: <한 문장>' '- 관례 표: <같은 역할 기존 화면 경로 2 개 이상 | 관례 없음 — 사유>' \
      '- 서버 주소: <개발 서버 출력의 Local 주소> · 연 주소: <브라우저가 연 주소>' '- 기준 캡처: <경로 + 본 것 | 신규> · 표식: <바뀌어야 할 것>' \
      '- 반영 확인: <표식이 바뀐 재캡처 경로 | 시도: 새로고침 → 서버 다시 띄우기 → wasm-build>' '- 캡처 점검: 넘침 · 글리프 · 칩·뱃지와 줄 모양 · 디버그 겹침' \
      '- 대조: <의도한 변경만 | 의도 외 변경 → self-reject N 회 (최대 3)>'
    toks "$(sect "$E/$REP" '## References')" 'https://vite.dev/config/server-options.html#server-port' 'https://v2.tauri.app/start/frontend/vite/' ;;
  SK-06)  # 다섯 UI 스킬 — 편집 전 기준 캡처 Gotcha · 번호가 이어진다
    for p in "$SCR:15" "$WID:17" "$SKL:10" "$RSP:11" "$ANI:14"; do f=${p%%:*}; n=${p##*:}
      L=$(gline "$E/$f" "$n. **기준 캡처는 편집 전에 찍는다**")
      printf '%s/' "$(toks "$L" "$n. **기준 캡처는 편집 전에 찍는다**" '`react-kit/references/render-evidence-protocol.md` §1 Step 0 과 §2 비교 반복 순서의 1 번을 첫 편집 전에 실행하고' '를 응답에 남긴다' | tr -d ' ')"
      printf '%s ' "$(seq_ok "$(sect "$E/$f" '# Gotchas')" | tr ' ' '-')"; done; echo ;;
  SK-07)  # 개발 서버 포트 — 템플릿 · react-run dev Gotcha · Tauri devUrl · harness vm_port(읽기만)
    echo "$(grep -cE '^[[:space:]]+port: 5173,$' "$E/$VT") $(grep -cE '^[[:space:]]+strictPort: true,$' "$E/$VT") $(grep -cF 'Tauri devUrl 과 harness vm_port 가 5173 을 가리킨다' "$E/$VT")"
    L=$(gline "$E/$RUN" '- **`dev` 포트는 5173 에 묶여 있다 (`strictPort: true`)**:')
    toks "$L" '지정 포트가 차 있으면 기본으로 다음 빈 포트로 옮긴다' '`runtime_inspection.vm_port`(둘 다 5173)' '남의 서버를 끄지 않는다' \
      '`pnpm vite dev --port <N>` 으로 띄우되' '`devUrl` 을, harness 런타임 검증을 쓰면 `vm_port` 를 같은 번호로 맞춘다' \
      'https://vite.dev/config/server-options.html#server-port' 'https://vite.dev/guide/cli' 'https://v2.tauri.app/start/frontend/vite/'
    toks "$(sect "$E/$INI" '### 단계 10')" '# devUrl: http://localhost:5173, frontendDist: ../dist' '# devUrl 포트는 vite.config.ts 의 server.port 와 같게 둔다'
    echo "vm_port=$(grep -cE '^[[:space:]]+vm_port: 5173$' "$E/react-kit/templates/harness-project.yaml.template")" ;;
  SK-08)  # 시험 수 보고 — react-run · react-preflight (react-build 는 test 단계가 없다)
    S=$(sect "$E/$RUN" '## Report Format')
    toks "$S" '  시험 수: <N passed · M skipped>   (test · test-coverage · e2e 만)' '`success` 는 passed 가 1 이상이고 skipped 가 0 일 때만 쓴다' \
      '`[미검증] 0 passed — 시험을 하나도 돌리지 않았다`' '`[미검증] N passed · M skipped`' \
      "\`.only\` 가 남은 곳 수(\`grep -rnE '(it|test|describe)\\.only\\(' src tests 2>/dev/null | wc -l\`)" '의도한 `skip` · `skipIf` 도 있으니 실패로 바꾸지는 않는다'
    toks "$(sect "$E/$RUN" '## Rules')$(printf '\n')$(gline "$E/$RUN" '- **test 결과는 passed · skipped 두 수로 읽는다**:')" \
      '- **MUST** `test` · `test-coverage` · `e2e` 결과에 passed · skipped 두 수를 적는다' '`references/render-evidence-protocol.md` §3 (b)(c)'
    S=$(sect "$E/$PRF" '## Report Format')
    toks "$S" '  5. test       ✓ (N passed · 0 skipped)' '✓ 는 passed 가 1 이상이고 skipped 가 0 일 때만 쓴다' \
      '`5. test       [미검증] (0 passed — 시험을 하나도 돌리지 않았다)`' '`5. test       [미검증] (N passed · M skipped)`' \
      "\`.only\` 가 남은 곳 수(\`grep -rnE '(it|test|describe)\\.only\\(' src tests 2>/dev/null | wc -l\`)" '의도한 `skip` · `skipIf` 도 있으니 실패로 바꾸지는 않는다' \
      '첫 줄을 `/react-preflight 완료 — test 단계 [미검증]` 으로' '0 개 실행과 `.only` 로 좁힌 실행은 종료 코드 0 이어도 검사되지 않은 것이다'
    toks "$S" '  5. test       ✓ (N passed)'
    toks "$(sect "$E/$PRF" '## Rules')" '- **MUST** test 단계 보고에 passed · skipped 두 수를 적는다'
    f=react-kit/skills/react-build/SKILL.md
    echo "build_same=$(cmp -s "$T/B/$f" "$E/$f" && echo 1 || echo 0) build_vitest=$(grep -c vitest "$E/$f")" ;;
  SK-09)  # react-l10n — 기본 흐름에서 --clean 빼기 · Gotcha 12 · §4-1 · 설계 문서 주석
    S=$(sect "$E/$L10" '### 4. codegen 흐름')
    echo "flow_clean=$(printf '%s\n' "$S" | awk '/^```bash$/{b=1; next} b && /^```$/{exit} b' | grep -c -- '--clean')"
    toks "$S" '# 1. 소스 스캔 → .po 파일에 새 키 추가 (이미 있는 번역은 그대로 둔다)' '# 2. .po → runtime catalog 컴파일'
    S=$(sect "$E/$L10" '#### 4-1. 안 쓰는 키 정리 — 사용자가 요청할 때만')
    toks "$S" '`git status --porcelain -- src/infrastructure/i18n/locales/` 출력이 비어 있어야 한다' '비어 있지 않으면 알리고 멈춘다' \
      '`pnpm lingui extract --clean` 을 돌리고 바로 `git diff --stat -- src/infrastructure/i18n/locales/` 를 보인다' \
      "git diff -U0 -- src/infrastructure/i18n/locales/ | grep -c '^-msgid '" \
      "git diff -U0 -- src/infrastructure/i18n/locales/ | grep -E '^-(msgstr \"[^\"]|\")'" \
      '둘째 명령이 한 줄이라도 내면 번역이 채워져 있던 항목이 지워졌을 수 있다 — 출력 줄을 보고 가른다' '사용자가 확인하기 전에는 정리 결과를 커밋하지 않는다'
    L=$(gline "$E/$L10" '12. **`lingui extract --clean` 을 기본 흐름에 넣지 마라**')
    toks "$L" '12. **`lingui extract' '소스에서 더는 찾지 못한 메시지를 catalog 에서 지운다' '번역이 채워진 항목까지 지워진다' \
      '정상 옵션이라 금지하지 않는다' '§4-1 순서로 돌린다' 'https://lingui.dev/ref/cli'
    seq_ok "$(sect "$E/$L10" '## Gotchas')"
    echo "$(grep -cF '# 안 쓰는 키 정리 — 기본 흐름 아님, 사용자가 요청할 때만 (react-l10n §4-1)' "$E/$G4") $(grep -cF '# 삭제된 키 정리' "$E/$G4")" ;;
  SK-10)  # 현행화 — 옛 값 0 · 새 값 · Lingui v5 pin 유지 · 조사 기록 머리
    grep -rnE '2026-04 현재 `?react@19\.2\+|2026-04 현재 19\.2\+|현행 stable 은 5\.5\.7|현행 stable 5\.5\.7|`@lingui/core@6\.6\.0`|v7\.71\.x' "$E/react-kit" | grep -c .
    toks "$(cat "$E/$INI")" '2026-09-24 조회 npm `latest` 는 `react@19.3.0` 이다' '2026-09-24 조회 npm `latest` 는 5.9.1 이며' \
      '**Lingui 라인 고정 — v5 compatibility pin (2026-09-24 확인)**: 2026-09-24 조회 npm `latest` 는 `@lingui/core@6.8.0` 이지만'
    toks "$(cat "$E/$WID")$(printf '\n')$(cat "$E/$FRM")" 'React 19 stable(2024-12, 2026-09-24 조회 npm `latest` 19.3.0)' \
      '**v7 라인을 사용**한다 (2026-09-24 조회 npm `latest` 7.88.0)' '이미 해소됐다** (2026-09-24 조회 npm `latest` 5.9.1)'
    echo "lingui_pin=$(grep -cF '"@lingui/core": "^5.0.0"' "$E/react-kit/templates/package.json.template")"
    echo "$(fm_get "$E/$RL" version) $(fm_get "$E/$RL" last_updated)"
    grep -m1 '^## \[' "$E/$RL" | grep -cxF '## [2026-09-25] - Phase 10 kaizen (렌더 증거 반영 확인 · 조용한 통과)'
    S=$(sect "$E/$RL" '## [2026-09-25] - Phase 10 kaizen')
    toks "$S" '| React | `19.3.0` — `<ViewTransition>` · Fragment Refs 가 stable |' '| @hookform/resolvers | `5.9.1` |' '| react-hook-form | `7.88.0` |' \
      '| @lingui/core | `6.8.0` |' '| Zod | `4.6.5` |' '「canary 대기」 가 풀렸다' '그 날짜의 사실이라 고치지 않고'
    # 옛 라운드는 그대로 — 2026-08-13 제목부터 끝까지가 편집 전 판과 같다
    diff <(awk '/^## \[2026-08-13\]/{f=1} f' "$T/B/$RL") <(awk '/^## \[2026-08-13\]/{f=1} f' "$E/$RL") >/dev/null && echo "old_rounds_same=1" || echo "old_rounds_same=0" ;;
  SK-11)  # 평가 사례 — 넷에 새 단언 · 러너 통과
    python3 - "$E/$EV" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); ev = d["tests"]
ids = [e.get("id") for e in ev]; by = {e.get("id"): e for e in ev}
want = {2: "편집 전에 되말하기 · 관례 표(같은 역할 기존 화면 2 개 이상 또는 관례 없음과 그 사유) · 기준 캡처 칸 `신규` 를 남긴다",
        13: "lingui extract --clean 을 기본 흐름에서 돌리지 않는다",
        18: "시험 수를 N passed · M skipped 로 적고, 0 passed 나 skipped 1 이상을 success 로 적지 않는다",
        20: "test 줄에 passed · skipped 두 수를 적고, 0 passed 나 skipped 1 이상이면 ✓ 와 「커밋할 준비가 됐습니다」 를 쓰지 않는다"}
out = [str(len(ev)), str(ids == list(range(1, len(ev) + 1)))]
for i, t in want.items():
    a = [x.get("text", "") for x in by.get(i, {}).get("assertions", [])]
    out.append(f"{i}:{len(a)}:{a.count(t)}")
print(" ".join(out))
PY
    ( cd "$E" && python3 scripts/run-evals.py react-kit > "$T/re.txt" 2>&1; echo "rc=$? $(grep -E '^Total: ' "$T/re.txt")" ) ;;
  ER-01)  # project-detect.sh — "null" 비교 · 경로 따옴표 · 알려진 답 시험 · 정적 검사
    echo "$(grep -cF '!= "null" ] && TANSTACK_ROUTER=true' "$E/$PDS") $(grep -cF "'.devDependencies.\\\"@tanstack/router-plugin\\\"'" "$E/$PDS") $(grep -cF '[ -n "$(read_json_field' "$E/$PDS")"
    # 시험은 $END 판 사본에서 돈다 — 작업 폴더의 미커밋 변경이 끼지 않는다
    ( out=$(bash "$E/$PDT" 2>&1); rc=$?; printf '%s\n' "$out" | tail -1; echo "rc=$rc" )
    ( out=$(/bin/bash "$E/$PDT" 2>&1); rc=$?; printf '%s\n' "$out" | tail -1; echo "rc=$rc" )
    # 음성 대조 — 편집 전 판 스크립트를 같은 시험에 넣으면 답에서 떨어진다
    ( out=$(PROJECT_DETECT="$T/B/$PDS" bash "$E/$PDT" 2>&1); rc=$?; printf '%s\n' "$out" | tail -1; echo "rc=$rc" )
    command -v shellcheck >/dev/null 2>&1 || { echo "SHELLCHECK_MISSING"; return 2; }
    echo "shellcheck=$(shellcheck "$E/$PDS" "$E/$PDT" 2>&1 | grep -c .) bash_n=$(bash -n "$E/$PDS" && bash -n "$E/$PDT" && echo 0 || echo 1)"
    echo "mode=$(git ls-tree "$END" -- "$PDT" | awk '{print $1}') fixtures_same=$(diff -rq "$T/B/react-kit/evals/test-fixtures" "$E/react-kit/evals/test-fixtures" >/dev/null && echo 1 || echo 0)" ;;
  ER-02)  # 새로 생긴 URL 이 근거 파일에 있다 — 열아홉 파일은 파일마다 편집 전 판과 비교, notes 는 URL 전부
    for f in "${FILES[@]}"; do comm -13 <( [ -f "$T/B/$f" ] && url < "$T/B/$f" ) <(url < "$E/$f"); done | sort -u | comm -23 - <(url < "$E/$EVID") | grep -c .
    if [ -f "$E/$NOTES" ]; then url < "$E/$NOTES" | comm -23 - <(url < "$E/$EVID") | grep -c .; else echo NOTES_MISSING; fi ;;
  ER-03)  # 더한 줄의 번역투 6 종
    echo "added=$(added | grep -c .) k02=$(added | grep -cE "$K02") names=$(added | grep -ciE 'fit-?pal|fit_pal|flutter[-_]playwright|playwright-mcp|chrome-devtools-mcp')" ;;
  ER-04)  # notes 문자열 · 공유 파일과 다른 Phase 파일을 건드린 커밋
    git cat-file -e "$END:$NOTES" && echo notes_committed=1 || echo notes_committed=0
    toks "$(cat "$E/$NOTES")" '`F03`' '`F05`' '`F01`' 'other-kits:P1' 'other-kits:P2' 'other-kits:P5' 'other-kits:P6' \
      'render-evidence-protocol.md:59' 'project-detection.md:28' '<Activity />' 'UNVERIFIED_ENV' 'react-view-transitions' \
      'g6-build-audit.md' '.claude/skills/react-kaizen/SKILL.md' 'bash react-kit/evals/scripts/project-detect-test.sh' 'plugin.json' \
      '## 바꾼 파일' '## 반영한 처리 배정표 키' '## 미반영 키와 사유' '## 넘기는 것' '## changelog 한 단락' '## 킷 로그 한 단락' '## 다음 사이클 메모'
    # 넘김 한 줄은 사유와 같은 줄로 센다 — 낱말은 다른 절에도 나와 넘김 줄을 빠뜨려도 1 이 된다
    echo "$(grep -F 'react-preflight' "$E/$NOTES" | grep -cF '기준 커밋') $(grep -F 'project-detection.md:28' "$E/$NOTES" | grep -cF '예시')"
    not_other "$B" "$END" "$SIG" .claude-plugin/marketplace.json react-kit/.claude-plugin/plugin.json react-kit/README.md README.md CLAUDE.md \
      .harness/.meta/orchestrator-audit-log.md .harness/.meta/kaizen-failure-count.yaml .claude/kaizen-input/insights-report.md \
      .github/workflows/ci.yml .harness/stale-values.yaml .claude/skills harness scripts design-kit flutter-toolkit docs/react-kit docs/index.html | grep -c . ;;
  AR-01)  # 허용 경로 · 서명 · 봉인 · 범위 선언 블록
    unsigned_on "$B" "$END" "$SIG" react-kit docs/react | grep -c .
    echo "$(my | grep -v '^\.harness/' | grep -vxF -f <(printf '%s\n' "${FILES[@]}") | grep -c .) $(my | grep -cxF -f <(printf '%s\n' "${FILES[@]}"))"
    find .harness -type f -name 'sprint-contract*.md' -print0 | while IFS= read -r -d '' f; do verify_seal "$f"; done \
      | awk '$1=="SEAL_BROKEN"{print $2}' | sed 's#^\./##' | sort -u | comm -12 - <( { my; echo "$CF"; } | sort -u) | grep -c .
    verify_seal "$E/$CF" | cut -d' ' -f1
    diff <(scope "$E/$CF" | grep -vxF '.harness/' | sort) <(printf '%s\n' "${FILES[@]}" | sort) >/dev/null && echo "scope_same=1" || echo "scope_same=0"
    scope "$E/$CF" | grep -cxF '.harness/' ;;
  AR-02)  # 새 문장이 가리키는 자리가 실제로 있다 · 형제 규약 숫자가 같다 · 규약을 읽는 쪽
    echo "$(grep -cF -- '- **`dev` 포트는 5173 에 묶여 있다' "$E/$RUN") $(grep -c '^### 비교 반복 순서 — 지금 보는 화면이 이번 코드인가$' "$E/$REP") $(grep -c '^## 1\. Step 0' "$E/$REP") $(grep -c '^### (b) 0 테스트 green run' "$E/$REP") $(grep -c '^### (c) `\.only` 로 좁혀진 green run' "$E/$REP") $(grep -c '^#### 4-1\. 안 쓰는 키 정리' "$E/$L10")"
    toks "$(sect "$E/harness/docs/guides/skill-design-guide.md" '## 3.7.')" '**막는 것**' '**시도한 우회**' '**통제 불가 사유**' '**재검증 명령**' '`[미검증:INVALID]`'
    echo "$(grep -cF '같은 역할의 서로 다른 기존 화면 2 개 이상을 Read 해서' "$E/flutter-toolkit/references/visual-evidence-protocol.md") $(grep -cF '(최대 3 회, 이후 사용자 에스컬레이션)' "$E/flutter-toolkit/references/visual-evidence-protocol.md") $(grep -cF '같은 역할의 서로 다른 기존 화면 **2 개 이상**을 Read 해서' "$E/design-kit/references/visual-change-protocol.md") $(grep -cF '**스스로 고치기는 최대 3 회**다' "$E/design-kit/references/visual-change-protocol.md")"
    f=react-kit/agents/react-reviewer.md
    echo "reviewer_same=$(cmp -s "$T/B/$f" "$E/$f" && echo 1 || echo 0) reviewer_refs=$(grep -c 'react-kit/references/render-evidence-protocol.md' "$E/$f")" ;;
  RE-01)  # 새 파일 목록 — 시험 스크립트 하나뿐이다
    comm -13 <(cd "$T/B" && find react-kit docs/react -type f | sort) <(cd "$E" && find react-kit docs/react -type f | sort) ;;
  RE-02)  # 숫자는 규약 한 곳에만 — 소비 스킬에 더한 줄에 「2 개 이상」 · 「3 회」 0 · 시험이 기존 입력 둘을 쓴다
    for f in "$SCR" "$WID" "$SKL" "$RSP" "$ANI" "$TST" "$CG" "$RUN" "$PRF"; do git diff --no-index -U0 "$T/B/$f" "$E/$f"; done | grep '^+' | grep -v '^+++' | grep -cE '2 개 이상|[0-9]+ 회'
    echo "$(grep -cF 'evals/test-fixtures/empty-project/package.json' "$E/$PDT") $(grep -cF 'templates/package.json.template' "$E/$PDT")" ;;
  AP-01)  # 더한 줄에 이 킷 플러그인 버전 값 — 값은 plugin.json 에서 읽는다
    L=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$E/react-kit/.claude-plugin/plugin.json")
    echo "version=$L $(added | grep -cF -- "$L")" ;;
  AP-03)  # 펜스 — V6 가 읽지 않는 docs/react 두 파일에 더한 줄의 펜스 줄
    for f in "$RL" "$G4"; do git diff --no-index -U0 "$T/B/$f" "$E/$f"; done | grep '^+' | grep -v '^+++' | grep -cE '^\+[[:space:]]*(```|~~~)' ;;
  AP-04)  # frontmatter — 고친 SKILL.md 열하나의 첫 블록이 편집 전과 같고 name 줄이 폴더 이름이다
    for f in "$SCR" "$WID" "$SKL" "$RSP" "$ANI" "$TST" "$RUN" "$PRF" "$L10" "$INI" "$FRM"; do
      L=$(basename "$(dirname "$f")")
      printf '%s/%s ' "$(diff <(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$T/B/$f") <(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$E/$f") >/dev/null && echo 1 || echo 0)" \
        "$(awk 'NR==1&&/^---/{fm=1;next} fm&&/^---/{exit} fm' "$E/$f" | grep -cxF "name: $L")"; done; echo ;;
  DG-02)  # markdownlint — 더한 줄의 새 경고 · evals.json 파싱
    for f in "${MDS[@]}"; do k=$(printf '%s' "$f" | tr '/' '_'); cp "$T/B/$f" "$T/$k.0.md"; cp "$E/$f" "$T/$k.md"; bash "$K/new-warnings.sh" "$T/$k.0.md" "$T/$k.md"; done
    python3 -c 'import json,sys; json.load(open(sys.argv[1], encoding="utf-8")); print("json_ok")' "$E/$EV" ;;
  DG-05)  # 저장소 검사 — $END 판을 git 저장소로 만든 사본에서 돈다 (작업 폴더의 다른 Phase 미커밋 변경이 끼지 않는다)
    local G=$T/G; rm -rf "$G"; cp -R "$E" "$G"
    git -C "$G" init -q && git -C "$G" add -A && git -C "$G" -c user.name=m -c user.email=m@m commit -qm snap || return 2
    # V 줄 머리에는 FAIL 이 안 찍힌다(아래 들여쓴 줄에 찍힌다) — `— OK` 로 끝나지 않는 V 줄을 센다
    ( cd "$G" && python3 scripts/validate-plugin.py react-kit > "$T/vp.txt" 2>&1; echo $? > "$T/vp.rc" )
    echo "$(grep -cE '^  V([1-9]|10) ' "$T/vp.txt") $(grep -E '^  V([1-9]|10) ' "$T/vp.txt" | grep -cv -- '— OK$') rc=$(cat "$T/vp.rc")"
    ( cd "$G" && python3 scripts/validate-plugin.py --check=table-integrity,code-fence > "$T/ti.txt" 2>&1 )
    echo "tf_mine=$(grep 'FAIL' "$T/ti.txt" | grep -cF -f <(printf '%s\n' "${FILES[@]}"))"
    ( cd "$G" && python3 scripts/sync-docs.py --check-only > "$T/sd.txt" 2>&1 ); echo "sync_docs_rc=$? $(grep -cxF '  react-kit/README.md: 동기화됨' "$T/sd.txt")"
    # sync-evals 는 킷 이름 인자가 없다 — react-kit 머리 줄을 읽었는지와 그 아래 어긋남 줄 수만 센다
    ( cd "$G" && python3 scripts/sync-evals.py --check-only > "$T/se.txt" 2>&1 )
    echo "$(grep -cxF '→ react-kit' "$T/se.txt") $(awk '/^→ /{f=($2=="react-kit"); next} f && NF' "$T/se.txt" | grep -c .)"
    ( cd "$G" && python3 scripts/check-stale-values.py > "$T/sv.txt" 2>&1 ); echo "stale_rc=$? ran=$(grep -c '^검사 범위: 소스 디렉토리 ' "$T/sv.txt") $(grep -cF -f <(printf '%s\n' "${FILES[@]}") "$T/sv.txt")" ;;
  DG-06)  # 사이클 검사 — 이 Phase 몫 줄만 본다. docs-site-regen 은 Final F2 몫
    python3 scripts/validate-post-kaizen.py --since "$B" --verbose > "$T/vpk.txt" 2>&1
    grep -E '\] . (scope-isolation|doc-contracts): ' "$T/vpk.txt" | awk '{print $5, $2}'
    python3 scripts/validate-doc-contracts.py -v 2>&1 | awk -F' → ' '/^ *검사: /{a=$1; sub(/^ *검사: /,"",a); sub(/:[0-9]+$/,"",a); print a; print $2}' | sort -u > "$T/dc.txt"
    echo "doc_checked=$(grep -c . "$T/dc.txt") doc_mine=$(comm -12 "$T/dc.txt" <(my) | grep -c .)"
    # 위반 커밋 목록을 읽은 수와 그 가운데 이 Phase 서명 커밋 수. 목록을 못 읽으면 둘째 값이 조용히 0 이 되므로 첫 값을 함께 본다
    awk '/ scope-isolation: /{f=1;next} /^\[ /{f=0} f&&/^ +[0-9a-f]{7,40}$/{print $1}' "$T/vpk.txt" > "$T/viol.txt"
    echo "violators=$(grep -c . "$T/viol.txt") mine=$(while read -r c; do git log -1 --format=%B "$c" | grep -qxF "$SIG" && echo "$c"; done < "$T/viol.txt" | grep -c .)" ;;
  *) echo "UNKNOWN $1"; return 2 ;;
  esac
}
```

```bash
#!/usr/bin/env bash
# new-warnings.sh <옛 파일> <새 파일> — 새 파일에서 더한 줄에 걸린 경고만 센다. 줄이 밀리므로 전체 수 차이로 세지 않는다
# 줄 번호는 경로 뒤 첫 번째 숫자다. 탐욕 매치(^[^ ]*:)로 뽑으면 열 번호가 줄 번호로 둔갑한다 (실측 2026-09-24)
# 린터가 안 돌면 경고 0 이 조용히 나온다 — 돌았다는 줄(Linting: 1 file)이 없으면 멈춘다 (실측 2026-09-25: 옆에 node_modules 가 없어 0)
set -u
DIR=$(cd "$(dirname "$0")" && pwd)
ADDED=$(git diff --no-index -U0 -- "$1" "$2" | awk '/^@@/{split($3,a,","); s=substr(a[1],2)+0; n=(a[2]==""?1:a[2]+0); for(i=0;i<n;i++) print s+i}' | sort -u)
OUT=$("$DIR/node_modules/.bin/markdownlint-cli2" --config "$DIR/cfg.markdownlint-cli2.jsonc" "$2" 2>&1)
printf '%s\n' "$OUT" | grep -q '^Linting: 1 file' || { echo "LINT_NOT_RUN $2"; exit 2; }
LINES=$(printf '%s\n' "$OUT" | grep -E ':[0-9]+(:[0-9]+)? (error|warning) ' | sed -E 's#^([^:]*):([0-9]+).*#\2#' | sort -u)
NEWW=$(comm -12 <(printf '%s\n' "$ADDED" | grep . | sort) <(printf '%s\n' "$LINES" | grep . | sort) | wc -l | tr -d ' ')
echo "total_warning_lines=$(printf '%s\n' "$LINES" | grep -c .) added_lines=$(printf '%s\n' "$ADDED" | grep -c .) new_warnings=$NEWW"
```

**예행.** 시작 커밋에서 레포를 스크래치로 복제해(`p10d/rehearse.sh`) BUILD 가 할 커밋을 흉내 냈다 — 봉인 커밋(이 계약 초안에 digest 를 적은 판) → 다른 Phase 서명 커밋 하나
(`design-kit/README.md`, 걸러져야 한다) → `mock.py` 를 적용한 구현 커밋 둘(`docs/react/` 둘 · `react-kit/` 열일곱) → `end_sha` → notes 모의본(`p10d/notes-mock.md`) → `end_sha` 한 줄 더.
변형 `base` 는 구현 없이 `end_sha` 를 시작 커밋으로 둬 시작 커밋 판을 잰다. 변형 다섯은 같은 흐름에 커밋 하나를 더한다: `unsigned-shared`(서명 없이 루트 `README.md`) ·
`unsigned-mine`(서명 없이 `react-kit/README.md`) · `unsigned-docsite`(서명 없이 `docs/index.html`) · `signed-outside`(서명하고 `react-kit/.claude-plugin/plugin.json`) · `cross-phase`(서명하고 `harness/skills/sprint/SKILL.md` 와 `react-kit/skills/react-test/SKILL.md` 한 커밋).
변형 다섯의 저장소는 잰 뒤 지웠다(디스크 여유가 200 MB 안팎이라). 다시 재려면 `bash p10d/rehearse.sh <이 계약 사본> p10d/rh-<변형> <변형>` 으로 만든다.

**봉인 전 실측 (2026-09-25, 검토 반영 뒤 다시 잼, bash 5.3.9 · `/bin/bash` 3.2.57 같은 값).** 예행 판 = 이 계약 초안을 봉인한 예행 저장소(`p10d/rh-none`), 시작 커밋 판 = 변형 `base`(`p10d/rh-base`).
모의본은 `mock.py`(sha256 앞 16 자리 `db181ec91592e78d`)를 시작 커밋 판에 적용한 트리다. 측정 도우미는 이 절의 세 블록을 글자 그대로 뗀 것이다(`p10d/k/`).
검토 반영 전 판(`20ed60ddd9c76fa2`)과 달라진 것은 주석 세 줄(`project-detect.sh` 한 줄 · 새 시험 머리 두 줄)과 react-l10n §4-1 한 문장이다 — 조건 스물다섯의 출력은 ER-04 둘째 줄(토큰 하나 더)만 바뀌었다.

**2 회차 검토 반영 (BUILD, 봉인 전).** 2 회차(`phase10-review.md` `## 2 회차`)가 고칠 것 하나를 냈다 — DG-05 (c) · (e) 가 종료 코드 0 대신 「0 또는 1 + 이 킷 몫 줄」 로 가르고,
(e) 는 검사기가 돌았다는 줄(`검사 범위: 소스 디렉토리`)을 함께 센다. `m.sh` 만 바뀌었고(`common.sh` · `new-warnings.sh` 는 그대로), 2 회차가 같은 판(`p10r2/k3/`)을
예행 판에 bash 5 · `/bin/bash` 3.2 로 돌려 다섯째 줄 `stale_rc=0 ran=1 0` 과 나머지 네 줄이 고치기 전과 같음을 확인했다. BUILD 는 이 계약에서 다시 뗀 `m.sh` 가 `p10r2/k3/m.sh` 와
`cmp` 로 같은지 보고 예행 판 `p10d/rh-none` 에서 `m DG-05` 를 한 번 더 돌렸다. 아래 표 DG-05 행은 이 판 값이다.

| 조건 | 예행 판 (요구값) | 시작 커밋 판 | 양성 · 음성 대조 |
| --- | --- | --- | --- |
| SK-01 | `1` 열하나 · `0` | `0` 열하나 · `1` | 문장 삭제 11 개 모두 출력이 바뀜 |
| SK-02 | `1` 열하나 · `1` | `0` 열하나 · `0` | 문장 삭제 11 개 |
| SK-03 | `1` 일곱 · `1` 넷 | `0` 일곱 · `0` 넷 | 문장 삭제 11 개 |
| SK-04 | `1` 여섯 · `1 0` · `1` 일곱 · `0` | `0` 여섯 · `0 1` · `0` 일곱 · `8` | 문장 삭제 14 개 · 마지막 값이 양성 대조 |
| SK-05 | `1.1.0 2026-09-25` · `1 1 1 1 1 0` · `1` 일곱 · `1 1` | `1.0.0 2026-07-27` · `0 0 0 0 0 1` · `0` 일곱 · `0 0` | 문장 삭제 14 개 |
| SK-06 | `111/1-15 111/1-17 111/1-10 111/1-11 111/1-14` | `000/1-14 000/1-16 000/1-9 000/1-10 000/1-13` | 문장 삭제 5 개 |
| SK-07 | `1 1 1` · `1` 여덟 · `1 1` · `vm_port=1` | `1 0 0` · `0` 여덟 · `1 0` · `vm_port=1` | 문장 삭제 10 개 |
| SK-08 | `1` 여섯 · `1 1` · `1` 여덟 · `0` · `1` · `build_same=1 build_vitest=0` | `0` 여섯 · `0 0` · `0` 여덟 · `1` · `0` · `build_same=1 build_vitest=0` | 문장 삭제 17 개 · 넷째 값이 양성 대조 |
| SK-09 | `flow_clean=0` · `1 1` · `1` 일곱 · `1` 여섯 · `1 12` · `1 0` | `flow_clean=1` · `0 0` · `0` 일곱 · `0` 여섯 · `1 11` · `0 1` | 문장 삭제 15 개 |
| SK-10 | `0` · `1 1 1` · `1 1 1` · `lingui_pin=1` · `1.4.0 2026-09-25` · `1` · `1` 일곱 · `old_rounds_same=1` | `6` · `0 0 0` · `0 0 0` · `lingui_pin=1` · `1.3.0 2026-08-13` · `0` · `0` 일곱 · `old_rounds_same=1` | 문장 삭제 14 개 · 첫 값이 양성 대조 |
| SK-11 | `21 True 2:5:1 13:5:1 18:4:1 20:5:1` · `rc=0 Total: 21 passed, 0 failed` | `21 True 2:4:0 13:4:0 18:3:0 20:4:0` · `rc=0 Total: 21 passed, 0 failed` | 문장 삭제 4 개 · 사례 18 새 단언 `type` → `check` → `rc=1 Total: 20 passed, 1 failed` |
| SC-00 | `0` | — | 변형 `signed-outside` → `1` |
| ER-01 | `1 0 0` · `결과: 6 경우 중 불일치 0` `rc=0` 두 벌 · `결과: 6 경우 중 불일치 4` `rc=1` · `shellcheck=0 bash_n=0` · `mode=100755 fixtures_same=1` | `0 1 1` · 시험 파일 없음 `rc=127` 세 벌 · `shellcheck=1 bash_n=1` · `mode= fixtures_same=1` | 비교만 고친 사본 → 불일치 1 (`jq has`) · 따옴표만 고친 사본 → 불일치 4 · 가짜 `jq` 를 링크한 사본 → `jq 가 숨겨지지 않았다` 종료 코드 2 |
| ER-02 | `0` · `0` | — | 규약 끝 `https://example.invalid/x` → `1 0` · notes 끝 같은 URL → `0 1` · notes 없음 → `0 NOTES_MISSING` |
| ER-03 | `added=256 k02=0 names=0` | — | 첫 모의본 `k02=1` (react-animation 「호출된다는 사실」) · 규약 끝 「fit-pal 화면」 → `names=1` |
| ER-04 | `notes_committed=1` · `1` 스물셋 · `1 1` · `0` | — | 변형 `unsigned-shared` · `unsigned-mine` · `unsigned-docsite` · `signed-outside` · `cross-phase` → 넷째 값 모두 `1`(`unsigned-docsite` 는 `docs/index.html` 을 더하기 전 목록으로 `0`) · notes 에서 `UNVERIFIED_ENV` 줄을 뺀 사본 → 열한째 값 `0` · `## 바꾼 파일` 줄을 뺀 사본 → 열일곱째 값 `0` · `react-preflight` 줄의 「기준 커밋」 을 뺀 사본 → `0 1` · 넘김 줄을 다른 절에 한 번씩 더 적은 사본 → `2 2`(요구값 안) |
| AR-01 | `0` · `0 19` · `0` · `SEAL_OK` · `scope_same=1` · `1` | — | `unsigned-mine` → 첫 값 `1` · `signed-outside` · `cross-phase` → `1 19` · 조건 줄 한 글자 변조 → `SEAL_BROKEN` |
| AR-02 | `1 1 1 1 1 1` · `1 1 1 1 1` · `1 1 1 1` · `reviewer_same=1 reviewer_refs=2` | `0 0 1 1 1 0` · `1 1 1 1 1` · `1 1 1 1` · `reviewer_same=1 reviewer_refs=2` | 첫 줄의 새 자리 셋이 시작 판에서 0 |
| RE-01 | `react-kit/evals/scripts/project-detect-test.sh` 한 줄 | — | `react-kit/references/x.md` 를 더한 사본 → 두 줄 |
| RE-02 | `0` · `1 1` | — | Gotcha 15 에 「기존 화면 2 개 이상」 → 첫 값 `1` |
| AP-01 | `version=0.3.0 0` | — | 규약 끝 「버전 0.3.0」 → `version=0.3.0 1` |
| AP-03 | `0` | — | research-log 끝 펜스 → `1` · react-run 맨 펜스 한 쌍 → V6 `1 bare` · DG-05 첫 줄 `10 1 rc=2` |
| AP-04 | `1/1` 열하나 | — | react-run description 한 칸 → 일곱째 `0/1` · `nam:` → 일곱째 `0/0` · DG-05 `10 1 rc=2` |
| DG-01 · DG-03 · DG-04 | `0` · `0` · `0` | — | DG-01 거르개에 `scripts/release.sh` · `.bak` → `1` · DG-04 거르개에 `react-kit/src/a.ts` · `b.md` → `1` |
| DG-02 | 열다섯 줄 `new_warnings=0` · `json_ok` | — | 첫 모의본 research-log 표 구분 줄 `\|---\|` → MD060 `new_warnings=1` |
| DG-05 | `10 0 rc=0` · `tf_mine=0` · `sync_docs_rc=0 1` · `1 0` · `stale_rc=0 ran=1 0` | — | `name:` 을 깬 사본 · 맨 펜스 사본 → `10 1 rc=2` · 다른 킷 README 어긋남 → `sync_docs_rc=1 1` · `docs/rust` 옛 값 → `stale_rc=1 ran=1 0` · `docs/react` 옛 값 → `stale_rc=1 ran=1 1` · 등록 파일 없음 → `stale_rc=1 ran=0 0` |
| DG-06 | `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0` | — | 변형 `cross-phase` → `scope-isolation: FAIL` · `violators=1 mine=1` |

문장 삭제 사본(`p10d/del.sh` · 목록 `p10d/dellist.txt`): SK-01 11 · SK-02 11 · SK-03 11 · SK-04 14 · SK-05 14 · SK-06 5 · SK-07 10 · SK-08 17 · SK-09 15 · SK-10 14 · SK-11 4 —
토큰 하나를 그 파일에서 한 번 지운 사본 126 개 모두 그 조건의 `m` 출력이 바뀌었다(`DROP` 126 · `NODROP` 0 · `MISSING` 0). 검토 반영 뒤 SK-09 토큰 하나를 새 문장으로 바꿔 다시 돌렸다.
양성 · 음성 대조 스크립트는 `p10d/ctl.sh` · ER-04 는 `p10d/ctl2.sh` 다. 예행 변형의 커밋 기록 대조는 `p10d/rh-<변형>` 에서 `m ER-04` · `m AR-01` · `m DG-06` 을 돌렸다.

## Skill

- [ ] SK-01: `react-kit/references/render-evidence-protocol.md` `## 1. Step 0` 이 편집 전 여섯 줄을 요구한다 — 기존 셋에 되말하기(두 갈래로 읽히면 묻기) · 화면 자체(라우트 파일과 화면 컴포넌트 — 진입점이나 흉내 낸 그림이 아님 — 와 주소) · 관례 표(같은 역할의 서로 다른 기존 화면 2 개 이상 · 앱 코드가 import 하는지 grep · grep 에 없는 컴포넌트 이름 금지 · 관례 없음 두 경우)를 더하고 옛 「다음 3 줄」 문장이 없다 (`F01` 리액트 쪽 · Phase 6 넘김) — `m SK-01` 첫 줄이 `1` 열하나, 둘째 줄이 `0` [exact, enumerated]
      (측정: `m SK-01`. 봉인 전 실측: 예행 판 `1` 열하나 · `0`, 시작 커밋 판 `0` 열하나 · `1` — 둘째 값이 양성 대조. 문장 삭제 열하나 모두 출력이 바뀐다)
- [ ] SK-02: 규약 `## 2. 증거 등급` 안에 `### 비교 반복 순서 — 지금 보는 화면이 이번 코드인가` 가 있어 — 1 은 편집 전 · 3 부터 완료 직전, 바뀌어야 할 표식을 기준 캡처 때 정하기, 반영 확인(개발 서버 `Local:` 주소와 브라우저가 연 주소 대조 · 새 캡처의 표식이 바뀌었는지로 판정 · 모듈 교체 로그나 새로고침 성공만으로 판정 안 함 · 브라우저 새로고침 → 서버 다시 띄우기 → Rust 를 고쳤으면 `/react-run wasm-build` 뒤 다시 띄우기와 그 기록 · 확인 전 「갱신했다」 금지), 스스로 고치기 최대 3 회, 이 순서가 공식 절차가 아니라 킷 규칙이라는 문장 — 을 담고, 새 소절 셋이 `## 2.` 와 `## 3.` 사이에 이 순서로 있다 (`F03` · `other-kits:P1`) — `m SK-02` 첫 줄이 `1` 열하나, 둘째 줄이 `1` [exact, enumerated]
      (측정: `m SK-02`. 봉인 전 실측: 예행 판 `1` 열하나 · `1`, 시작 커밋 판 `0` 열하나 · `0`. 문장 삭제 열하나 모두 출력이 바뀐다)
- [ ] SK-03: 규약 §2 에 `### 캡처 점검 목록`(글자 넘침 · 깨진 글리프 · 칩·뱃지와 줄 모양 · 디버그 겹침 넷, 하나라도 걸리면 PASS 없음, 실제 서비스 글꼴로 그리지 않은 캡처로 글자 모양을 판정하지 않음, 넘침을 데이터로 재현하지 않음)과 `### 도구가 고장이라 말하기 전에`(출력을 응답에 남기는 세 확인 — 인자 이름을 도구 설명과 대조 · 연 페이지가 내가 띄운 서버인지 · 따로 뜨는 층을 전체 스냅샷에서 다시 찾기)가 있다 (`F05` · Phase 6 넘김) — `m SK-03` 두 줄이 `1` 일곱 · `1` 넷 [exact, enumerated]
      (측정: `m SK-03`. 봉인 전 실측: 예행 판 `1` 일곱 · `1` 넷, 시작 커밋 판 `0` 일곱 · `0` 넷. 문장 삭제 열하나 모두 출력이 바뀐다)
- [ ] SK-04: 생성 측 `[미검증]` 이 사유 한 줄이 아니라 설계 가이드 §3.7 의 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 요구한다 — 규약 `## 2.` 에 네 칸 문장 여섯이 각각 1, `## 4.` 체크리스트의 새 미검증 줄 1 · 옛 줄 `- [미검증]: <항목 + 사유 + 시도한 fallback>` 0, 소비 일곱 자리(`react-screen` · `react-widget` · `react-skeleton` · `react-responsive` · `react-animation` · `react-test` 의 `SKILL.md` 와 `react-kit/references/common-gotchas.md`)에 네 칸 문구 `$FOUR` 가 각각 1, `react-kit/` 전체에서 옛 모양(한 줄의 「`[미검증]` (마커)와/+/과 사유·이유」 와 줄이 갈린 「마커와 사유」)이 0 줄 (Phase 1 넘김 `render-evidence-protocol.md:59`) — `m SK-04` 네 줄이 `1` 여섯 · `1 0` · `1` 일곱 · `0` [exact, enumerated]
      (측정: `m SK-04`. 봉인 전 실측: 예행 판 `1` 여섯 · `1 0` · `1` 일곱 · `0`, 시작 커밋 판 `0` 여섯 · `0 1` · `0` 일곱 · `8` — 마지막 값이 양성 대조(여덟 자리). 문장 삭제 열넷 모두 출력이 바뀐다)
- [ ] SK-05: 규약 머리가 편집 전과 완료 직전 두 번 실행한다고 적고(두 시점 목록 · 옛 「**완료를 선언하기 직전**에 실행하는 증거 규약이다」 0), 형제 규약 숫자 문단(flutter · design 과 같은 값 · 정본 절이 생기기 전까지 한쪽을 바꾸면 다른 두 쪽도 같이 바꾼다)을 두며, `## 4.` 체크리스트에 새 줄 일곱(되말하기 · 관례 표 · 서버 주소와 연 주소 · 기준 캡처와 표식 · 반영 확인 · 캡처 점검 · 대조와 최대 3), `## References` 에 Vite · Tauri URL 둘, 머리 설정 `version: 1.1.0` · `last_updated: 2026-09-25` 가 있다 — `m SK-05` 네 줄이 `1.1.0 2026-09-25` · `1 1 1 1 1 0` · `1` 일곱 · `1 1` [exact, enumerated]
      (측정: `m SK-05`. 봉인 전 실측: 예행 판이 요구값과 같고, 시작 커밋 판 `1.0.0 2026-07-27` · `0 0 0 0 0 1` · `0` 일곱 · `0 0`. 문장 삭제 열넷 모두 출력이 바뀐다)
- [ ] SK-06: 다섯 UI 스킬 `react-screen` · `react-widget` · `react-skeleton` · `react-responsive` · `react-animation` 이 각각 15 · 17 · 10 · 11 · 14 번째 Gotcha `**기준 캡처는 편집 전에 찍는다**` 로 규약 §1 Step 0 과 §2 비교 반복 순서의 1 번을 첫 편집 전에 실행해 결과를 응답에 남기라고 하고, 각 `# Gotchas` 의 번호가 1 부터 그 번호까지 빠짐없이 이어진다 (`F01` · `F03` 리액트 쪽) — `m SK-06` 한 줄이 `111/1-15 111/1-17 111/1-10 111/1-11 111/1-14` [exact, enumerated]
      (측정: `m SK-06`. 봉인 전 실측: 예행 판이 요구값과 같고, 시작 커밋 판 `000/1-14 000/1-16 000/1-9 000/1-10 000/1-13`. 문장 삭제 다섯 모두 출력이 바뀐다)
- [ ] SK-07: 개발 서버 포트가 5173 에 묶인다 — `react-kit/templates/vite.config.template.ts` 의 `server` 에 `port: 5173,` · `strictPort: true,` · 이유 주석이 각각 1, `react-kit/skills/react-run/SKILL.md` 의 Gotcha 한 줄 `**\`dev\` 포트는 5173 에 묶여 있다 (\`strictPort: true\`)**` 이 여덟(다음 빈 포트로 옮기는 기본 동작 · `devUrl` 과 `vm_port` 둘 다 5173 · 남의 서버를 끄지 않음 · `--port <N>` · 그때 `devUrl` · `vm_port` 를 같은 번호로 · 근거 URL 셋)을 담고, `react-kit/skills/react-init/SKILL.md` `### 단계 10` 에 devUrl 줄과 포트를 맞추라는 줄이 각각 1, 읽기만 하는 `react-kit/templates/harness-project.yaml.template` 의 `vm_port: 5173` 이 1 이다 (`other-kits:P1`) — `m SK-07` 네 줄이 `1 1 1` · `1` 여덟 · `1 1` · `vm_port=1` [exact, enumerated]
      (측정: `m SK-07`. 봉인 전 실측: 예행 판이 요구값과 같고, 시작 커밋 판 `1 0 0` · `0` 여덟 · `1 0` · `vm_port=1`. 문장 삭제 열 모두 출력이 바뀐다)
- [ ] SK-08: 시험 수를 passed · skipped 두 수로 적고 passed 0 · skipped 1 이상을 통과로 적지 않는 규칙이 형제 둘에 같이 있다 — `react-kit/skills/react-run/SKILL.md` `## Report Format` 에 여섯(시험 수 줄 · success 조건 · 두 `[미검증]` 모양 · `.only` 세기 명령 · 의도한 skip 은 실패로 안 바꿈)과 `## Rules` MUST · test Gotcha 의 근거 인용 둘, `react-kit/skills/react-preflight/SKILL.md` `## Report Format` 에 여덟(성공 줄 `✓ (N passed · 0 skipped)` · ✓ 조건 · 두 `[미검증]` 줄 · `.only` 세기 명령 · 의도한 skip · 첫 줄과 끝 줄 · 이유 문장)과 옛 성공 줄 `✓ (N passed)` 0 · `## Rules` MUST 1, test 단계가 없는 `react-kit/skills/react-build/SKILL.md` 는 편집 전과 같다 (`other-kits:P5`) — `m SK-08` 여섯 줄이 `1` 여섯 · `1 1` · `1` 여덟 · `0` · `1` · `build_same=1 build_vitest=0` [exact, enumerated]
      (측정: `m SK-08`. 봉인 전 실측: 예행 판이 요구값과 같고, 시작 커밋 판 `0` 여섯 · `0 0` · `0` 여덟 · `1` · `0` · `build_same=1 build_vitest=0` — 넷째 값이 양성 대조. 문장 삭제 열일곱 모두 출력이 바뀐다)
- [ ] SK-09: `lingui extract --clean` 이 react-l10n 기본 흐름에서 빠지고 사용자가 요청할 때만 도는 정리 절이 생긴다 — `react-kit/skills/react-l10n/SKILL.md` `### 4. codegen 흐름` 첫 bash 블록의 `--clean` 0 · 새 주석 두 줄 각각 1, `#### 4-1. 안 쓰는 키 정리 — 사용자가 요청할 때만` 에 일곱(미커밋 변경이 없어야 함 · 있으면 멈춤 · 돌린 뒤 바로 `--stat` · 지워진 키 세기 명령 · 지워진 번역 찾기 명령 · 한 줄이라도 나오면 번역이 지워졌을 수 있으니 출력 줄을 보고 가름 · 확인 전 커밋 안 함), 한 줄 Gotcha 12 에 여섯(옵션 뜻 · 번역까지 지워짐 · 옵션 자체는 금지 안 함 · §4-1 · Lingui CLI URL 포함), `## Gotchas` 번호가 1 ~ 12 로 이어지고, `docs/react/kit-design/g4-quality.md` 의 `--clean` 줄 주석이 새 주석 1 · 옛 주석 `# 삭제된 키 정리` 0 (`other-kits:P6`) — `m SK-09` 여섯 줄이 `flow_clean=0` · `1 1` · `1` 일곱 · `1` 여섯 · `1 12` · `1 0` [exact, enumerated]
      (측정: `m SK-09`. 봉인 전 실측: 예행 판이 요구값과 같고, 시작 커밋 판 `flow_clean=1` · `0 0` · `0` 일곱 · `0` 여섯 · `1 11` · `0 1` — 첫 값 · 마지막 둘째 값이 양성 대조. 문장 삭제 열다섯 모두 출력이 바뀐다)
- [ ] SK-10: 근거 파일 §3 의 낡은 버전 문장이 조회값으로 바뀌고 Lingui v5 pin 은 그대로이며, 킷 조사 기록 머리에 이번 라운드가 있다 — `react-kit/` 에서 옛 값(「2026-04 현재 react@19.2+ · 19.2+」 · 「현행 stable (은) 5.5.7」 · `` `@lingui/core@6.6.0` `` · `v7.71.x`)이 든 줄 0, `react-kit/skills/react-init/SKILL.md` 새 문장 셋 · `react-kit/skills/react-widget/SKILL.md` 하나 · `react-kit/skills/react-form/SKILL.md` 둘 각각 1, `react-kit/templates/package.json.template` 의 `"@lingui/core": "^5.0.0"` 1, `docs/react/research-log.md` 머리 설정 `1.4.0 2026-09-25` · 첫 `## [` 제목이 `## [2026-09-25] - Phase 10 kaizen (렌더 증거 반영 확인 · 조용한 통과)` · 그 절에 현행 표 다섯 행과 두 문장(backlog 「canary 대기」 가 풀림 · 옛 라운드 값은 그 날짜의 사실) · `## [2026-08-13]` 부터 끝까지가 편집 전과 같다 (근거 §3 · §4 7 번) — `m SK-10` 여덟 줄이 `0` · `1 1 1` · `1 1 1` · `lingui_pin=1` · `1.4.0 2026-09-25` · `1` · `1` 일곱 · `old_rounds_same=1` [exact, enumerated]
      (측정: `m SK-10`. 봉인 전 실측: 예행 판이 요구값과 같고, 시작 커밋 판 `6` · `0 0 0` · `0 0 0` · `lingui_pin=1` · `1.3.0 2026-08-13` · `0` · `0` 일곱 · `old_rounds_same=1` — 첫 값이 양성 대조(여섯 줄). 문장 삭제 열넷 모두 출력이 바뀐다)
- [ ] SK-11: 평가 사례 넷이 바뀐 동작을 기대하고 러너를 통과한다 — `react-kit/evals/evals.json` 사례 21 개 · id 1 ~ 21, 사례 2 · 13 · 18 · 20 에 새 단언이 하나씩(편집 전 되말하기 · 관례 표 · 기준 캡처 `신규` / 기본 흐름에서 `--clean` 안 돌림 / N passed · M skipped / ✓ 와 「커밋할 준비가 됐습니다」 안 씀) 더해져 단언 수 5 · 5 · 4 · 5, `$END` 판 사본에서 `python3 scripts/run-evals.py react-kit` 이 종료 코드 0 에 `Total: 21 passed, 0 failed` (`F01` · `other-kits:P5` · `other-kits:P6` Counterpart) — `m SK-11` 두 줄이 `21 True 2:5:1 13:5:1 18:4:1 20:5:1` · `rc=0 Total: 21 passed, 0 failed` [exact, enumerated]
      (측정: `m SK-11`. 봉인 전 실측: 예행 판이 요구값과 같고, 시작 커밋 판 `21 True 2:4:0 13:4:0 18:3:0 20:4:0` · `rc=0 Total: 21 passed, 0 failed`. 문장 삭제 넷 모두 출력이 바뀐다. 음성 대조: 사례 18 새 단언의 `type` 을 `check` 로 바꾸면 둘째 줄 `rc=1`)

## Script

- [ ] SC-00: N/A (Script 카테고리는 `release.sh` 연동 · 버전 올림 · `marketplace.json` 갱신이다. 이 Phase 는 그 파일을 건드리지 않는다 — 버전은 Final 몫. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -cE '^(scripts/release\.sh|\.claude-plugin/marketplace\.json|[^/]+/\.claude-plugin/plugin\.json)$'` 이 0. 양성 대조: 변형 `signed-outside` 에서 1)

## Error

- [ ] ER-01: `react-kit/scripts/project-detect.sh` 의 두 결함이 고쳐지고 알려진 답 시험이 붙는다 — 비교가 `!= "null"` 로 1 줄 · 역슬래시 붙은 필드 경로 0 줄 · 옛 `-n` 비교 0 줄, 새 시험 `react-kit/evals/scripts/project-detect-test.sh`(git 모드 `100755`)를 `$END` 판 사본에서 bash 5 와 `/bin/bash` 3.2 로 돌리면 둘 다 끝 줄 `결과: 6 경우 중 불일치 0` 에 종료 코드 0, 같은 시험에 편집 전 판 스크립트를 넣으면 `결과: 6 경우 중 불일치 4` 에 종료 코드 1, 두 파일의 shellcheck 출력 0 줄 · `bash -n` 통과, 시험 입력 폴더 `react-kit/evals/test-fixtures/` 가 편집 전과 같다 (`other-kits:P2`) — `m ER-01` 이 `1 0 0` · `결과: 6 경우 중 불일치 0` · `rc=0` · `결과: 6 경우 중 불일치 0` · `rc=0` · `결과: 6 경우 중 불일치 4` · `rc=1` · `shellcheck=0 bash_n=0` · `mode=100755 fixtures_same=1` [exact]
      (측정: `m ER-01`. 알려진 답: 세 입력 × 두 경로 — 플러그인 없음(`empty-project` 픽스처) `false` · 있음(`templates/package.json.template`) `true` · package.json 없음 `false`, jq 경로와 jq 를 숨긴 python3 경로 둘 다. 봉인 전 실제값: 모의본 여섯 줄 모두 `일치` · 종료 코드 0 (bash 5.3.9 · 3.2.57). 음성 대조 셋: 편집 전 판 → 불일치 4(없음 · package.json 없음이 두 경로에서 `true`) · 비교만 고친 사본 → 불일치 1(`jq has` 가 `false` — 근거 파일의 최소 수정만으로는 모자란다) · 따옴표만 고친 사본 → 불일치 4. 시작 커밋 판 `m ER-01` 은 `0 1 1` · 시험 파일 없음 `rc=127` 세 벌 · `shellcheck=1 bash_n=1` · `mode= fixtures_same=1`)
- [ ] ER-02: 열아홉 파일에 새로 생긴 URL 과 `.harness/.meta/kaizen-0924/phase10-notes.md` 의 URL 이 전부 이 Phase 의 외부 근거 파일 `.harness/.meta/evidence/phase10.md` 에 있다 — 열아홉 파일은 파일마다 편집 전 판과 비교한다 (러닝북 — 근거 파일에 없는 URL 을 지어내지 마라 · notes 킷 로그의 출처 URL 은 근거 파일에서만) — `m ER-02` 두 줄이 `0` · `0` [exact, enumerated]
      (측정: `m ER-02` — notes 가 없으면 둘째 줄이 `NOTES_MISSING` 이라 FAIL. 봉인 전 실측: 예행 판 `0` · `0`(새 URL 열둘이 전부 근거 파일에 있다). 양성 대조: 규약 끝에 `https://example.invalid/x` 한 줄 → `1` · `0`, notes 끝에 같은 URL → `0` · `1`, notes 를 지운 사본 → `0` · `NOTES_MISSING`)
- [ ] ER-03: 열아홉 파일에 더한 줄에 번역투 6 종(`tone-kit/references/locale-korean.md` §2 치환표의 grep 열)과 특정 앱 · 화면 조종 도구 이름(`fit-pal` · `fitpal` · `fit_pal` · `flutter-playwright` · `playwright-mcp` · `chrome-devtools-mcp` 모양)이 0 건이다 (러닝북 말투 규칙) — `m ER-03` 이 `added=N k02=0 names=0` 이고 N 은 1 이상 [exact]
      (측정: `m ER-03`. 봉인 전 실측: 예행 판 `added=256 k02=0 names=0`. 양성 대조: 첫 모의본은 `k02=1` 이었다 — react-animation Gotcha 13 을 고치며 줄 전체가 더한 줄이 됐고 그 줄의 옛 문구 「호출된다는 사실」 이 걸렸다. 지금 모의본은 그 문구를 고친다. 규약 끝에 「fit-pal 화면」 한 줄 → `names=1`)
- [ ] ER-04: 이 Phase 범위 밖과 미반영 키를 명시적 미완으로 넘기고 공유 파일 · 다른 Phase 파일을 건드리지 않는다 — `.harness/.meta/kaizen-0924/phase10-notes.md` 가 `$END` 에 커밋돼 있고, 문자열 스물셋(처리 배정표 키 `` `F03` `` · `` `F05` `` · `` `F01` `` · `other-kits:P1` · `other-kits:P2` · `other-kits:P5` · `other-kits:P6`, 넘김 `render-evidence-protocol.md:59` · `project-detection.md:28` · `<Activity />` · `UNVERIFIED_ENV` · `react-view-transitions` · `g6-build-audit.md` · `.claude/skills/react-kaizen/SKILL.md` · CI 에 넣을 줄 `bash react-kit/evals/scripts/project-detect-test.sh` · `plugin.json`, 러닝북 여섯 절 제목 `## 바꾼 파일` · `## 반영한 처리 배정표 키` · `## 미반영 키와 사유` · `## changelog 한 단락` · `## 킷 로그 한 단락` · `## 다음 사이클 메모` 와 넘김 절 제목 `## 넘기는 것`)이 각각 1 줄 이상이며, 넘김 둘은 사유와 같은 줄에 각각 1 줄 이상 있고(`react-preflight` 와 `기준 커밋` · `project-detection.md:28` 과 `예시`), 구간 안에서 공유 파일 · 다른 Phase 파일을 건드린 커밋 가운데 다른 Phase 서명이 없는 커밋이 0 이다 [exact, enumerated]
      (Given: BUILD 가 notes 를 쓰고 커밋한 뒤 · 측정: `m ER-04` 네 줄이 `notes_committed=1` · `1` 이상 스물셋 · 두 값 모두 `1` 이상 · `0`. 봉인 전 실측: notes 모의본을 커밋한 예행 판 `notes_committed=1` · `1` 스물셋 · `1 1` · `0`. 양성 대조: 변형 `unsigned-shared` · `unsigned-mine` · `signed-outside` · `cross-phase` · `unsigned-docsite` → 넷째 값 1 · notes 에서 `UNVERIFIED_ENV` 줄을 지운 사본 → 둘째 줄 열한째 값 0 · `## 바꾼 파일` 줄을 지운 사본 → 둘째 줄 열일곱째 값 0 · `react-preflight` 줄에서 「기준 커밋」 을 지운 사본 → 셋째 줄 `0 1` · 넘김 줄을 다른 절에 한 번씩 더 적은 사본 → 셋째 줄 `2 2`(요구값 안 — 진짜 notes 모양))

## Architecture

- [ ] AR-01: 이 Phase 의 변경이 허용 경로 안에 머물고, 범위 선언 블록이 그 경로와 같으며, 이 계약이 봉인돼 있다 — `react-kit/` · `docs/react/` 를 건드린 구간 안 커밋이 전부 서명했고, 서명 커밋이 고친 `.harness/` 밖 경로가 열아홉 파일뿐이며(열아홉 전부 포함), 서명 커밋이 건드린 계약 가운데 봉인이 깨진 것이 0, 이 계약이 `SEAL_OK`, `## 범위 경계` 의 `# sprint-scope` 블록이 열아홉 경로와 `.harness/` 한 줄이다 [exact, enumerated]
      (Given: BUILD 가 개정 파일에 `end_sha:` 를 적은 뒤 · 측정: `m AR-01` 여섯 줄이 `0` · `0 19` · `0` · `SEAL_OK` · `scope_same=1` · `1` (`SEAL_ABSENT` 는 봉인을 건너뛴 것이라 FAIL). 봉인 전 실측: 이 계약 초안을 봉인한 예행 판이 요구값과 같다. 양성 대조: 변형 `unsigned-mine` → 첫 값 1 · `signed-outside` → 둘째 줄 `1 19` · 봉인 뒤 조건 줄 한 글자를 바꾼 사본 → 넷째 줄 `SEAL_BROKEN`. 봉인 전인 지금 작업 폴더의 이 계약은 `SEAL_ABSENT`)
- [ ] AR-02: 새 문장이 가리키는 자리가 실제로 있고 형제 규약의 숫자가 같다 — 규약이 가리키는 react-run Gotcha 머리 · 스킬이 가리키는 규약 `### 비교 반복 순서 — 지금 보는 화면이 이번 코드인가` · `## 1. Step 0` · run · preflight 가 가리키는 규약 `### (b) 0 테스트 green run` · `### (c) \`.only\` 로 좁혀진 green run` · 설계 문서가 가리키는 `#### 4-1. 안 쓰는 키 정리` 가 각각 1(§4-1 이 가리키는 Gotcha 12 는 SK-09 가 잰다), 규약이 인용하는 `harness/docs/guides/skill-design-guide.md` `## 3.7.` 에 네 칸 이름과 `[미검증:INVALID]` 가 각각 1 이상, `flutter-toolkit/references/visual-evidence-protocol.md` 와 `design-kit/references/visual-change-protocol.md` 에 「같은 역할의 서로 다른 기존 화면 2 개 이상」 · 「최대 3 회」 문장이 각각 1, 규약을 읽는 `react-kit/agents/react-reviewer.md` 는 편집 전과 같고 규약 경로를 두 번 가리킨다 — `m AR-02` 네 줄이 `1 1 1 1 1 1` · `1 1 1 1 1` · `1 1 1 1` · `reviewer_same=1 reviewer_refs=2` [exact, enumerated]
      (측정: `m AR-02`. 봉인 전 실측: 예행 판이 요구값과 같다. 시작 커밋 판 첫 줄은 `0 0 1 1 1 0` — 새 자리 셋이 아직 없다)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다. 이번 변경에 적용: 열아홉 파일에 더한 줄에 react-kit `plugin.json` 의 `version` 값(`$END` 판에서 읽는다)이 0 건이다 — 이 Phase 는 킷 버전을 적지 않고 Final 이 올린다. 외부 라이브러리 버전(React · resolvers · Lingui · RHF · Zod)은 조회 날짜를 단 사실 문장이라 이 패턴의 대상이 아니다 [exact]
      (측정: `m AP-01` 이 `version=0.3.0 0`. 봉인 전 실측: 예행 판 `version=0.3.0 0`. 양성 대조: 규약 끝에 「버전 0.3.0」 한 줄 → `version=0.3.0 1`)
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (```` ```text, ```bash, ```yaml ```` 등). 판정 권위는 validate-plugin V6 상태기계다 — 여는/닫는 fence 가 동형이라 줄 단위 정규식으로는 판정 불가. 이번 변경에 적용: react-kit 쪽은 DG-05 의 V6 가 `0 bare` 로 재고, V6 가 읽지 않는 `docs/react/` 두 파일에 더한 줄에는 펜스가 0 이다 [exact]
      (측정: `m AP-03` 이 `0` · DG-05 첫 줄의 V6 포함 `10 0 rc=0`. 봉인 전 실측: 예행 판 `0`. 양성 대조: `docs/react/research-log.md` 끝에 펜스 한 줄 → `1` · `react-kit/skills/react-run/SKILL.md` 끝에 맨 펜스 한 쌍 → V6 `1 bare` · DG-05 첫 줄 `10 1 rc=2`)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL. 이번 변경에 적용: 고친 SKILL.md 열하나(`react-screen` · `react-widget` · `react-skeleton` · `react-responsive` · `react-animation` · `react-test` · `react-run` · `react-preflight` · `react-l10n` · `react-init` · `react-form`)의 첫 frontmatter 블록이 편집 전과 글자 그대로 같고 `name: <폴더 이름>` 줄이 1 개씩이다 — 그래서 README AUTO 구간과 트리거 설명이 읽는 값도 바뀌지 않는다 [exact, enumerated]
      (측정: `m AP-04` 한 줄이 `1/1` 열하나. 봉인 전 실측: 예행 판 `1/1` 열하나. 양성 대조: react-run `description:` 본문에 빈칸 한 칸을 더한 사본 → 일곱째 값 `0/1`, `name:` 을 `nam:` 으로 바꾼 사본 → 일곱째 값 `0/0` 과 DG-05 첫 줄 `10 1 rc=2`)

## Reusability

- [ ] RE-01: N/A (재사용 단위 코드 — 컴포넌트 · 함수 · 모듈 — 를 새로 만들지 않는다. 새 파일은 시험 스크립트 하나(`react-kit/evals/scripts/project-detect-test.sh`)이고, 고친 스크립트 `react-kit/scripts/project-detect.sh` 는 이미 킷 공용 폴더에 있다. 측정: `m RE-01` 이 새 파일 목록으로 `react-kit/evals/scripts/project-detect-test.sh` 한 줄만 낸다. 양성 대조: 예행 판에 `react-kit/references/x.md` 를 더하면 두 줄)
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다. 이번 변경에 적용: (a) 숫자(같은 역할 기존 화면 「2 개 이상」 · 스스로 고치기 「N 회」)는 규약 한 곳에만 두고 소비 아홉 자리(다섯 UI 스킬 · `react-test` · `common-gotchas.md` · `react-run` · `react-preflight`)에 더한 줄에는 그 숫자 모양이 0 건 (b) 새 시험은 새 픽스처를 만들지 않고 기존 입력 둘(`react-kit/evals/test-fixtures/empty-project/package.json` · `react-kit/templates/package.json.template`)을 쓴다 [exact]
      (측정: `m RE-02` 두 줄이 `0` · `1 1` 이고 ER-01 마지막 줄 `fixtures_same=1`. 봉인 전 실측: 예행 판 `0` · `1 1`. 양성 대조: react-screen Gotcha 15 에 「기존 화면 2 개 이상」 을 더한 사본 → 첫 값 1)

## Diagnostics

- [ ] DG-01: N/A (`commands.analyze` 는 `bash -n scripts/release.sh` 라 `scripts/release.sh` 만 잰다 — 이번 변경 파일과 교집합 0 개. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 양성 대조: 같은 `grep -c` 에 `scripts/release.sh` · `scripts/release.sh.bak` 두 줄을 넣으면 1. 이번 변경의 셸 파일 두 개는 ER-01 의 shellcheck · `bash -n` 이 잰다)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (`diagnostics.ide_exclude` 값 `[]`) — 이번 변경에 적용: 편집기 마크다운 확장과 같은 조건(markdownlint-cli2 0.23.2 · MD013 끔)으로 마크다운 열다섯 파일의 **더한 줄**에 걸린 경고가 0 이고 린터가 열다섯 번 다 돌았으며, `react-kit/evals/evals.json` 이 JSON 으로 읽힌다. 셸 두 파일은 ER-01 shellcheck 가 잰다. 편집 전부터 있던 경고는 `범위 경계` 절에 적은 대로 범위 밖이다 [exact]
      (측정: `m DG-02` 열다섯 줄 전부 `new_warnings=0` 이고 `LINT_NOT_RUN` 0, 끝 줄 `json_ok`. 봉인 전 실측: 예행 판 열다섯 줄 `new_warnings=0` · `json_ok`. 양성 대조: 첫 모의본은 `docs/react/research-log.md` 표 구분 줄 `|---|---|---|` 때문에 `new_warnings=1`(MD060) 이었다 — 고친 뒤 0)
- [ ] DG-03: N/A (`commands.test` 는 `bash scripts/release.sh 2>&1 || true` 라 `scripts/release.sh` 만 잰다 — 교집합 0 개. 측정: DG-01 과 같은 명령 `type my >/dev/null || exit 2;` 뒤 `my | grep -c '^scripts/release.sh$'` 이 0. 실제 시험은 ER-01 · SK-11 · DG-05)
- [ ] DG-04: N/A (구동할 앱 · 서버가 없다 — `.ts` 는 새 프로젝트에 복사되는 템플릿(`react-kit/templates/`)이고, 셸 두 파일은 ER-01 이 실제로 돌린다. 측정: `type my >/dev/null || exit 2;` 뒤 `my | grep -vE '^(\.harness/|react-kit/templates/|react-kit/scripts/project-detect\.sh$|react-kit/evals/scripts/)' | grep -cE '\.(dart|ts|tsx|js|rs|go|py|sh)$'` 이 0. 양성 대조: 같은 거르개에 `react-kit/src/a.ts` · `b.md` 두 줄을 넣으면 1)
- [ ] DG-05: 저장소 검사가 이 킷을 문제로 가리키지 않는다 — `$END` 판을 git 저장소로 만든 사본에서 (a) `scripts/validate-plugin.py react-kit` 출력에 `V1` ~ `V10` 열 줄이 있고 전부 `— OK` 로 끝나며 종료 코드 0 이다 — V 줄 머리에는 FAIL 이 안 찍히고 들여쓴 다음 줄에 찍혀서, V 줄에서 FAIL 낱말을 세면 맨 펜스를 못 잡는다 (b) 전체 킷 `--check=table-integrity,code-fence` 의 `FAIL` 줄 가운데 이 Phase 파일을 가리키는 줄 0 (c) `scripts/sync-docs.py --check-only` 가 종료 코드 0 또는 1 에 `  react-kit/README.md: 동기화됨` 1 줄 (d) `scripts/sync-evals.py --check-only` 출력에 `→ react-kit` 머리 줄이 있고 그 아래 어긋남 줄이 0 (e) `scripts/check-stale-values.py` 가 돌았고(`검사 범위: 소스 디렉토리` 로 시작하는 줄 1) 종료 코드 0 또는 1 에 이 Phase 파일 0 건. (c) · (e) 의 종료 코드 1 은 다른 킷 README 나 다른 Phase 파일 때문에도 나므로 허용하고 이 킷 몫의 줄로 가른다 — 검사기가 멈춰 난 종료 코드 1 은 (c) 는 `react-kit/README.md` 줄이, (e) 는 `검사 범위:` 줄이 0 이라 떨어진다 [exact]
      (측정: `m DG-05` 다섯 줄이 `10 0 rc=0` · `tf_mine=0` · `sync_docs_rc=0 1` 또는 `sync_docs_rc=1 1` · `1 0` · `stale_rc=0 ran=1 0` 또는 `stale_rc=1 ran=1 0`. 봉인 전 실측: 예행 판 `10 0 rc=0` · `tf_mine=0` · `sync_docs_rc=0 1` · `1 0` · `stale_rc=0 ran=1 0`. 양성 대조: 다른 킷 `rust-kit/README.md` 를 어긋나게 한 사본 → `sync_docs_rc=1 1`(요구값 안) · `docs/rust/research-log.md` 끝에 등록된 옛 값 `shadcn-ui@latest` → `stale_rc=1 ran=1 0`(요구값 안) · 같은 값을 `docs/react/research-log.md` 끝에 → `stale_rc=1 ran=1 1` · `.harness/stale-values.yaml` 을 지운 사본 → `stale_rc=1 ran=0 0`. 음성 대조: react-run `name:` 을 깬 사본 → 첫 줄 `10 1 rc=2` · react-run 끝에 맨 펜스 한 쌍 → `10 1 rc=2`. 초안의 첫 측정(V 줄에서 `ERROR|FAIL` 세기 — Phase 5 · 7 계약과 같은 꼴)은 맨 펜스 사본에서도 `10 0` 이었다 — 예행 중에 찾아 고쳤다)
- [ ] DG-06: `python3 scripts/validate-post-kaizen.py --since 4a8ec55f4d874eaaed083af9621f9679693cbdb6` 출력의 `scope-isolation` · `doc-contracts` 줄이 `FAIL` · `ERROR` 가 아니다. `docs-site-regen` 은 Final F2 몫이라 판정에서 뺀다. 다른 Phase 커밋 때문에 `scope-isolation` 이 FAIL 이면 `--verbose` 위반 커밋 목록을 한 개 이상 읽었고 그 안에 이 Phase 서명 커밋이 없을 때 이 조건은 PASS 다. `doc-contracts` 가 `FAIL` · `ERROR` 이면 `python3 scripts/validate-doc-contracts.py -v` 의 `검사:` 줄 경로 가운데 이 Phase 파일이 0 개일 때 PASS 다 [exact]
      (측정: `m DG-06` — `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=N doc_mine=0` · `violators=N mine=0`. 봉인 전 실측: 예행 판 `scope-isolation: PASS` · `doc-contracts: PASS` · `doc_checked=2 doc_mine=0` · `violators=0 mine=0`. 양성 대조: 변형 `cross-phase` → `scope-isolation: FAIL` · `violators=1 mine=1`)
