---
feature: "카이젠 Phase 10 — react-kit 현행성 갱신 (템플릿 버전 4종 · Zod resolver workaround 강등 · 브라우저 지원 수치 · 표준 커버리지 공백 문서화)"
created: "2026-08-13 14:16"
complexity: "복잡"
conditions: 24
slug: kaizen-phase10-react-currency
status: active
owner_session: df1b3e15-30b3-4825-a3c4-4ac44c686e94
conditions_digest: sha256:8bdf38c0e40e4ca8
locked_at: "2026-08-13 14:16"
---

## 배경

`.harness/.meta/evidence/phase10.md` 가 이번 Phase 의 **유일한 외부 근거**다. 외부 조회 0 회.

Phase 10 은 low-signal Phase 다. `/insights` 2026-08-13 은 "Phase 10 React — 이번 리포트에 직접
신호 없음" 이라고 명시하고 (`insights-report.md:110`), 데이터풀 §1 의 REJECT Top 20 · Improvement
Top 15 도 전부 외부 Flutter/Rust 프로젝트 귀속이라 react-kit 콘텐츠 결함 신호가 0 건이다.
`validate-plugin.py react-kit` 는 V1~V8 전부 OK 다 (데이터풀 §self-audit).

따라서 **새 규칙을 만들지 않는다.** evidence 가 확인한 **stale 사실 3 군**만 정정하고, evidence 가
열거한 **표준 커버리지 공백**을 문서화한다. 공백 문서화는 원칙 완화가 아니다 — 라이브러리 0 개
원칙은 유지되고 금지 목록에서 항목을 빼지 않는다 (SK-07 이 보존을 잰다).

**정정 대상 3 군 (evidence 표 기준):**

1. **템플릿 버전 stale** — `vite ^6` (현행 major 8) · `@hookform/resolvers ^3` (현행 5.5.7) ·
   `zod ^3` (현행 major 4) · `@lingui/macro ^5` (evidence 기준 **더 이상 maintained 아님**).
   `@lingui/macro` 는 버전 올리기가 아니라 **대체 경로**가 답이다 — 우리 스킬이 이미 요구하는
   subpath 매크로(`@lingui/core/macro` · `@lingui/react/macro`)가 그 경로이므로 템플릿에서
   패키지를 뺀다. 템플릿이 스킬 본문과 이미 자기모순 상태였다.
2. **Zod v4 workaround 를 기본 전제로 유지** — evidence: `@hookform/resolvers` v5.1.0 에서 Zod 4
   지원이 들어갔고 현 npm 문서도 `zod` / `zod/v4` 예시를 제시한다. `zod/v3` alias 는 **legacy
   resolver 에 묶인 프로젝트 전용**으로 강등한다.
3. **브라우저 지원 수치 stale** — react-animation 의 "Firefox 는 플래그 필요" 서술 2 건이 낡았다.
   evidence 의 Can I Use / MDN 수치로 갱신한다.

**Lingui major 는 올리지 않는다.** evidence 는 `@lingui/core@6.6.0` 을 현행 stable 로 확인했지만
v6 는 ESM-only + Node `22.19+` 를 요구한다. 킷 전체 Node floor 상향은 이번 Phase 의 결정 대상이
아니므로 (오케스트레이터 지시 · evidence §열린 질문) v5 라인을 **명시적 compatibility pin** 으로
남기고 사유와 열린 질문을 기록한다 (SK-08 · AR-04).

## 리서치 소스 (evidence 파일 한정 — 외부 조회 0 회)

- `.harness/.meta/evidence/phase10.md` — 관찰 사실 표 8 행(React / TanStack Query / Tauri 2 /
  Tailwind / Zustand / Lingui / react-hook-form+zod / Vite), 애니메이션 원칙 검증 2 단락,
  권장안 4 항, 트레이드오프, 열린 질문 3 항. 인용 URL 은 그 파일에 실재하는 것만 쓴다.
- `.harness/.meta/kaizen-data-pool.md` §1 · §self-audit — react 귀속 REJECT 0 건 확인,
  `react-kit` V1~V8 OK 확인.
- `.claude/kaizen-input/insights-report.md:110` — "Phase 10 React 직접 신호 없음" (Triage 근거).
- `docs/kaizen/changelog.md` `[2026-07-27]` / `[2026-07-28]` — 직전 사이클 react 흡수분
  (canonical 미검증 규약 · 렌더 증거 규약 · §5.5 가드). **재승격 금지 대상**이며 이번 변경은 그
  목록과 교차하지 않는다.
- Phase 1 산출물 `harness/docs/guides/skill-design-guide.md` §3.7 enforcement 등급 —
  이번 Phase 는 신규 조항 0 건이므로 등급 상향 대상도 0 건이다.
- `harness/references/contract-schema.md` v5.3 — 본 계약의 포맷 SSOT.

## GAP 분석 (전부 실측 · 사전 명령 출력 기준)

| # | 갭 | 사전 실측 | 처리 |
| --- | --- | --- | --- |
| F1 | 템플릿 4 종 stale | `vite=^6.0.0` · `@hookform/resolvers=^3.0.0` · `zod=^3.0.0` · `@lingui/macro` 키 존재=True (python json 출력) | SC-02 |
| F2 | `zod/v3` workaround 가 기본 전제 | `grep -rn 'zod/v3' react-kit/skills \| grep -vi legacy \| wc -l` → **2** | SK-01 · SK-02 |
| F3 | scroll-driven "Firefox 플래그 필요" | `grep -c '플래그 필요' react-kit/skills/react-animation/SKILL.md` → **2** | SK-03 · SK-04 |
| F4 | View Transitions 지원 서술에 수치 없음 | `90.2%` · `Chrome/Edge 111+` 토큰 0 건 | SK-05 |
| F5 | `@lingui/macro` 설치 명령 잔존 | `grep -rn 'add .*@lingui/macro' react-kit docs/react \| wc -l` → **1** (`docs/react/kit-design/g1-scaffolding.md:162`) | ER-01 |
| F6 | `Vite 6` 를 현행으로 적는 참조 | `grep -c 'Vite 6' react-kit/references/common-gotchas.md` → **1** (G9 라이브러리 목록) | AR-01 경로에 포함 |
| G1 | 표준 커버리지 공백 미문서화 | `physics` · `inertia` · `collision` 토큰 react-animation 0 건 | SK-06 |
| — | 금지 라이브러리 목록 | 4 정전 표면 × 11 토큰 누락 **0** (사전 오라클 출력 `BANNED_MISSING=0`) | SK-07 (보존 조건) |

**신설하지 않는 것**: 새 references 파일 · 새 스킬 · 새 에이전트 · 새 규칙 조항 · 금지 목록 완화.

## 범위 경계

**구현 변경 경로 9 개.** 목록은 AR-01 의 기대 집합 한 곳에서만 열거한다
(§측정 커버리지 표기의 화이트리스트 규칙). 계약 파일 자신과 `.harness/**` 는 AR-01 pathspec 에서
제외한다.

- **건드리지 않는다**: `react-kit/README.md` · `react-kit/.claude-plugin/` · `react-kit/evals/`
  (테스트 픽스처의 `vite ^6.0.0` 3 건 포함 — Scope 밖이라 이번 Phase 에서 손대지 않고
  후속 과제로 남긴다) · `react-kit/scripts/` · 다른 킷 전부.
- **버전 번호·URL 을 지어내지 않는다.** evidence 에 없는 릴리스 번호·패치 번호를 새로 쓰지 않는다
  (AP-01). evidence 가 "Zod 최신 patch 번호는 확인 못 했다" 고 적었으므로 zod 는 major 범위
  `^4.0.0` 까지만 적는다. `@vitejs/plugin-react-swc` 의 Vite 8 호환 버전은 evidence 에 없으므로
  **근거 부족으로 이번 사이클 미반영** — 열린 질문으로만 남긴다.
- Lingui major 상향 · 킷 Node floor 상향은 **이번 Phase 의 결정 대상이 아니다** (열린 질문).

## 회귀 게이트

- 정정 항목은 "새 서술 추가" 가 아니라 **잔존 0 건 증명**으로 판정한다. 사전 출력(2 · 2 · 1)이
  discriminating 근거다.
- 모든 오라클은 zsh · bash 양쪽에서 실행하고 출력이 같아야 한다 (DG-04).
- grep 오라클의 substring 오탐을 사전 확인했다: 금지목록 보존 오라클의 `motion` 토큰은
  `framer-motion` 에도 걸리지만 **보존 방향**의 검사라 오탐이 판정을 느슨하게 만들지 않는다
  (음성 대조로 확인 — `gsap` 를 한 표면에서 지우면 `BANNED_MISSING=1`).
- 열거값(경로 수 · 조건 수 · 누락 토큰 수)은 타이핑하지 않고 명령으로 계산한다.

## Skill

- [ ] SK-01: `zod/v3` alias 를 언급하는 스킬 본문 줄이 전부 legacy 한정 문맥이다 [exact]
      (측정: `grep -rn 'zod/v3' react-kit/skills | grep -vi 'legacy' | wc -l` → `0` ·
       사전 출력 `2` 가 discriminating 근거 ·
       음성 대조: 정정 문장에서 `legacy` 토큰을 지우면 이 측정이 FAIL 해야 한다)
- [ ] SK-02: Zod 4 공식 지원 하한이 2 개 스킬에 각각 명시된다 [exact, enumerated]
      (측정: `grep -rlF 'resolvers@5.1.0' react-kit/skills | LC_ALL=C sort` 결과가
       `react-kit/skills/react-form/SKILL.md`,
       `react-kit/skills/react-init/SKILL.md` 2 행과 정확히 일치)
- [ ] SK-03: scroll-driven 서술에 "플래그 필요" 계열 단정이 0 건이다 [exact]
      (측정: `grep -c '플래그 필요' react-kit/skills/react-animation/SKILL.md` → `0` ·
       사전 출력 `2`)
- [ ] SK-04: scroll-driven 지원 수치가 evidence 값으로 갱신된다 [exact, enumerated]
      (측정: `react-kit/skills/react-animation/SKILL.md` 에서 `85.43%`, `115+`, `26+`, `156+`
       4 토큰이 모두 매치 — 누락 토큰 0)
- [ ] SK-05: same-document View Transitions 지원 수치가 evidence 값으로 갱신되고
      cross-document 는 limited 로 구분된다 [exact, enumerated]
      (측정: `react-kit/skills/react-animation/SKILL.md` 에서 `90.2%`, `111+`, `18+`, `144+`,
       `cross-document` 5 토큰이 모두 매치 — 누락 토큰 0)
- [ ] SK-06: 표준만으로 커버되지 않는 공백 8 종이 react-animation 에 각각 명시된다
      [exact, enumerated]
      (측정: `react-kit/skills/react-animation/SKILL.md` 에서 `physics`, `inertia`, `collision`,
       `sortable`, `keyboard`, `live-region`, `Lottie`, `cross-document` 8 토큰이 공백 섹션
       본문에 모두 매치 — 누락 토큰 0 · 처리 경로 3 종(직접 구현 · fallback · 사전 렌더 자산)이
       같은 섹션에 존재)
- [ ] SK-07: 금지 라이브러리 11 종이 4 정전 표면에 전부 보존된다 (삭제 0) [exact, enumerated]
      (측정: 아래 스니펫 출력이 `BANNED_MISSING=0` ·
       음성 대조: 사본에서 `gsap` 를 지우면 `BANNED_MISSING=1` — 사전 실행으로 확인 완료)

```sh
miss=0
for f in react-kit/skills/react-animation/SKILL.md \
         react-kit/agents/animation-architect-react.md \
         react-kit/skills/react-audit/SKILL.md \
         react-kit/references/common-gotchas.md; do
  for t in motion framer-motion dnd-kit react-spring react-transition-group \
           react-dnd react-beautiful-dnd gsap lottie-react auto-animate animate.css; do
    grep -qF -- "$t" "$f" || { printf 'MISSING %s %s\n' "$f" "$t"; miss=$((miss+1)); }
  done
done
printf 'BANNED_MISSING=%s\n' "$miss"
```

- [ ] SK-08: react-init Lingui 단계가 (a) `@lingui/macro` 미설치 사유와 (b) v5 compatibility pin
      사유를 함께 명시한다 [exact]
      (측정: `react-kit/skills/react-init/SKILL.md` 의 Lingui 단계에서 `maintained`,
       `22.19`, `ESM-only`, `compatibility pin` 4 토큰이 모두 매치)

## Script

- [ ] SC-01: `react-kit/templates/package.json.template` 이 유효 JSON 으로 파싱된다 [exact]
      (측정: `python3 -c "import json;json.load(open('react-kit/templates/package.json.template'))"`
       exit code `0`)
- [ ] SC-02: 템플릿 의존성 4 항이 evidence 표 기준으로 갱신된다 [exact, enumerated]
      (측정: python 으로 `devDependencies.vite` == `^8.0.0` ·
       `dependencies["@hookform/resolvers"]` == `^5.1.0` · `dependencies.zod` == `^4.0.0` ·
       `"@lingui/macro" not in devDependencies` — 4 항 전부 `True` ·
       사전 출력 `^6.0.0` / `^3.0.0` / `^3.0.0` / 키 존재)
- [ ] SC-03: 템플릿의 다른 의존성 범위는 변경되지 않는다 [exact]
      (Given: 커밋 직전 스테이징 완료 후 ·
       측정: `git diff --cached --numstat -- react-kit/templates/package.json.template` 의
       추가/삭제가 `3` / `4` 와 정확히 일치)

## Error

- [ ] ER-01: `@lingui/macro` 를 **설치**하는 명령이 0 건이다 [exact]
      (측정: `grep -rn 'add .*@lingui/macro' react-kit docs/react | wc -l` → `0` ·
       사전 출력 `1`)
- [ ] ER-02: `@lingui/macro` 를 **금지·감지**하는 룰은 3 표면에 그대로 보존된다
      [exact, enumerated]
      (측정: `grep -rlF '@lingui/macro' react-kit/agents/react-reviewer.md react-kit/skills/react-audit/SKILL.md react-kit/templates/harness-project.yaml.template | LC_ALL=C sort`
       결과가 `react-kit/agents/react-reviewer.md`,
       `react-kit/skills/react-audit/SKILL.md`,
       `react-kit/templates/harness-project.yaml.template` 3 행과 정확히 일치)

## Architecture

- [ ] AR-01: 변경이 정확히 9 경로로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 스테이징 완료 후 ·
       측정: `git diff --cached --name-only -- react-kit docs ':(exclude).harness'` 결과가
       `docs/react/kit-design/g1-scaffolding.md`,
       `docs/react/research-log.md`,
       `react-kit/agents/animation-architect-react.md`,
       `react-kit/references/common-gotchas.md`,
       `react-kit/references/project-detection.md`,
       `react-kit/skills/react-animation/SKILL.md`,
       `react-kit/skills/react-form/SKILL.md`,
       `react-kit/skills/react-init/SKILL.md`,
       `react-kit/templates/package.json.template` 9 행과 정확히 일치)
- [ ] AR-02: `docs/react/research-log.md` 최상단에 `## [2026-08-13] - Phase 10 kaizen` 라운드가
      추가되고 frontmatter `last_updated` 가 `2026-08-13` 이다 [exact]
- [ ] AR-03: research-log 의 낡은 Zod workaround 서술이 전부 정정 포인터를 갖는다 [exact]
      (측정: `grep -n 'zod/v3' docs/react/research-log.md | grep -v '정정 2026-08-13' | wc -l`
       → `0` · 사전 출력 `3` ·
       음성 대조: 포인터 하나를 지우면 이 측정이 FAIL 해야 한다)
- [ ] AR-04: 열린 질문 3 종이 신규 라운드에 기록된다 [exact, enumerated]
      (측정: `docs/react/research-log.md` 의 2026-08-13 라운드에서 `Node 22.19`,
       `plugin-react-swc`, `Rolldown` 3 토큰이 모두 매치)

## Anti-patterns

- [ ] AP-01: 이번 커밋이 새로 도입한 버전 토큰·URL 이 전부 evidence 파일에 실재한다 (날조 0) [exact]
      (측정: `git diff --cached -U0 -- react-kit docs` 의 추가 줄에서 뽑은 신규 버전 토큰·`https://`
       URL 집합이 `.harness/.meta/evidence/phase10.md` 에 존재 — 수작업 대조 결과 미출처 0 건)
- [ ] AP-03: 변경 파일 전체에 bare code fence 가 0 건이다 [exact]
      (측정: `python3 scripts/validate-plugin.py react-kit` V6 `0 bare` +
       변경된 `docs/react/*.md` 에서 bare fence 0)

## Reusability

- [ ] RE-01: 표준 커버리지 공백 목록의 **정의**는 1 개 파일에만 존재하고 에이전트는 경로를
      인용만 한다 [exact]
      (측정: `grep -rln 'inertia' react-kit | LC_ALL=C sort` 결과가
       `react-kit/agents/animation-architect-react.md`,
       `react-kit/skills/react-animation/SKILL.md` 2 행이며, 그중 에이전트 쪽 매치 줄은
       8 종 목록을 재열거하지 않고 스킬 경로를 인용한다)
- [ ] RE-02: 신규 파일·신규 디렉토리 생성이 0 건이다 [exact]
      (측정: `git status --porcelain -- react-kit docs/react | grep -c '^??'` → `0`)

## Diagnostics

- [ ] DG-01: `python3 scripts/validate-plugin.py react-kit` 이 FAIL 0 으로 통과한다 [exact]
- [ ] DG-02: `python3 scripts/sync-docs.py --check-only react-kit` 이 Scope 밖 파일 갱신을
      요구하지 않는다 [exact]
- [ ] DG-04: 위 모든 grep / python 오라클을 zsh 와 bash 에서 실행한 출력이 동일하다 (diff 0) [exact]
