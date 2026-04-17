---
feature: "docs site 싱크 — 누락된 8개 페이지 생성"
created: "2026-04-17 10:37"
complexity: "복잡"
conditions: 19
---

## Skill
- [ ] SK-01: 8개 HTML 파일이 각각 지정된 경로에 존재한다 — `docs/design-kit/{apple-hig,material-design,open-source-systems,dark-mode,i18n,responsive}.html`, `docs/flutter-toolkit/flutter-ai-rules.html`, `docs/harness/plugin-validation.html` [exact, enumerated]
- [ ] SK-02: 8개 HTML 파일 모두 최소 400줄 이상의 콘텐츠를 포함한다 (hero + 원칙 카드 + 수치 테이블 + 안티패턴 bad/good + Gotchas 체크리스트 섹션 모두 포함) [structural, collective]
- [ ] SK-03: 8개 HTML 파일 모두 외부 CDN/CSS/JS/font 링크를 포함하지 않는다 — standalone HTML로 모든 스타일이 `<style>` 인라인이다 [exact, collective]
- [ ] SK-04: 8개 HTML 파일 모두 원칙 카드 하단에 소스 MD의 출처 URL(`<a class="card-source" href="URL">`)을 포함한다 — 각 페이지 최소 3개 이상의 원칙 카드에 출처 링크 존재 [structural, collective]
- [ ] SK-05: 각 페이지의 콘텐츠는 대응하는 소스 MD의 핵심 주제·수치·원칙·안티패턴을 반영한다 (MD에 존재하는 주요 섹션이 HTML에서 최소 1회 이상 언급됨) [goal]

## Script
- [ ] SC-01: N/A — 릴리스 스크립트(scripts/release.sh) 및 validate-plugin 관련 변경 없음

## Error
- [ ] ER-01: 8개 HTML 파일 모두 `python3 -m http.server`로 서빙 시 브라우저 콘솔 에러 0건, 404 에러 0건 [goal]
- [ ] ER-02: `docs/index.html`에서 8개 신규 페이지로 navigate 시 iframe 로딩 실패 없이 콘텐츠 렌더링된다 [goal]
- [ ] ER-03: 8개 HTML 파일의 `<a>` 링크 및 내부 앵커가 깨진 경로를 포함하지 않는다 (상대경로가 `docs/index.html` 기준 유효) [structural, collective]

## Architecture
- [ ] AR-01: `docs/index.html`의 categories 배열에 8개 신규 페이지 항목이 모두 등록된다 — 각 항목은 `{id, title, file}` 3필드를 포함하며 `file` 값이 `{plugin}/{page}.html` 형태의 상대경로다 [exact, enumerated]
- [ ] AR-02: `docs/index.html`의 `getIcon()` 함수에 8개 신규 페이지의 `id` 키에 대응하는 SVG 아이콘 case가 추가된다 [exact, enumerated]
- [ ] AR-03: design-kit 6개 페이지의 `:root --accent` 값은 `#E8965A` (design-kit accent), `flutter-ai-rules.html`은 `#22D3EE` (flutter-toolkit accent), `plugin-validation.html`은 `#D97757` (harness accent)로 설정된다 [exact, enumerated]
- [ ] AR-04: 각 페이지의 `body` 배경 gradient rgba 값이 `css-tokens.md` 매핑의 플러그인별 값과 일치한다 (design-kit `rgba(232,150,90,...)`, flutter-toolkit `rgba(34,211,238,...)`, harness `rgba(217,119,87,...)`) [exact, collective]
- [ ] AR-05: 8개 페이지 모두 공통 기본 토큰(`--bg`, `--surface`, `--border`, `--text`, `--radius`)을 `css-tokens.md`와 동일한 값으로 정의한다 [exact, collective]
- [ ] AR-06: 8개 페이지 모두 design-audit 7개 카테고리(Typography, Color, Spacing, Accessibility, Interaction, Motion, Authenticity) 기준 중 최소 WCAG AA 대비비 4.5:1 이상, 본문 폰트 ≥16px, 연속 동일 구조 3회 반복 없음을 충족한다 [goal]

## Anti-patterns
- [ ] AP-03: bare code fence 금지 — 모든 `<pre><code>` 블록이 의미 있는 콘텐츠를 가지며 빈 fence가 아니다 (HTML에서는 실 code block 렌더링)
- [ ] AP-05: 외부 CDN/font/script 링크 금지 — `<link rel="stylesheet" href="https://...">` 또는 `<script src="https://...">` 패턴 0회 (standalone 원칙)

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 — 신규 페이지의 공통 CSS 패턴은 `references/page-template.html` 스타일을 재사용한다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다 — 기존 `docs/{plugin}/` 페이지의 `.card`, `.grid-2`, `.section-label` 등 기본 클래스를 재사용한다

## Diagnostics
- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (해당 없음 — release.sh 미변경, 자동 PASS)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (8개 HTML 파일 + docs/index.html 대상, 스펠체크 제외)
- [ ] DG-03: 브라우저 콘솔에 에러/경고 0건 (8개 신규 페이지 및 index.html에서 navigate 테스트)
- [ ] DG-04: `python3 -m http.server` 구동 후 8개 페이지 모두 정상 렌더, iframe 표시 정상
