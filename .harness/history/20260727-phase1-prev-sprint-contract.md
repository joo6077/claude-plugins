---
feature: "인사이트 마찰 패턴 → durable rule 승격"
created: "2026-06-05 10:36"
complexity: "중간"
conditions: 11
---

## Skill
- [ ] SK-01: flutter-extract SKILL.md Gotchas에 "추출 전 추상화 레벨(평함수/위젯/provider) 확정·합의, 단순 로직 자동 위젯화 금지, 위치 불명확 시 새 폴더 발명 전 확인" Gotcha 1줄이 추가되어 있다 [structural] (측정: `grep -c "추상화 레벨" flutter-toolkit/skills/flutter-extract/SKILL.md` ≥ 1)
- [ ] SK-02: flutter-provider SKILL.md Gotchas에 "요청 범위 넘는 캐시/추상화/스캐폴딩 임의 추가 금지 — 최소 구현 우선" Gotcha 1줄이 추가되어 있다 [structural] (측정: `grep -c "최소 구현" flutter-toolkit/skills/flutter-provider/SKILL.md` ≥ 1)
- [ ] SK-03: kit Gotcha에 프로젝트-특정 금지(ValueNotifier/useState)를 박지 않는다 — 두 편집 파일에 "ValueNotifier" 문자열이 없다 [exact, enumerated] (측정: `grep -c "ValueNotifier" flutter-extract/SKILL.md flutter-provider/SKILL.md` = 0/0)

## Script
- [ ] SC-01: 신규 memory 파일 2개(feedback_skill_invocation_evidence, feedback_minimal_change_no_overeng)마다 MEMORY.md 포인터 1줄이 대응 추가되어 있다 [structural, enumerated] (측정: 신규 .md 수 2 == MEMORY.md 신규 라인 수 2)
- [ ] SC-02: 글로벌 CLAUDE.md 신규 추가는 포인터 섹션 1개(헤더 1 + 본문 1 + 공백)로 5줄 이하다 — 실제 룰은 별도 파일에 위치 [exact] (측정: 추가된 "아키텍처 가드레일" 섹션 라인 수 ≤ 5)

## Error
- [ ] ER-01: 글로벌 CLAUDE.md 추가 규칙이 기존과 중복/모순되지 않는다 — "ValueNotifier"는 0건(룰 파일에만 존재), "스킬 호출"은 1건만 등장 [exact] (측정: `grep -c`)
- [ ] ER-02: 신규 memory name 슬러그(feedback-skill-invocation-evidence, feedback-minimal-change-no-overeng)가 기존 14개 파일과 겹치지 않는다 [exact, enumerated]

## Architecture
- [ ] AR-01: 크로스프로젝트 하드 가드레일(no ValueNotifier/useState·최소변경·리팩토링위치·스킬호출증거)은 `~/.claude/rules/architecture-guardrails.md`에 정의되고, 글로벌 CLAUDE.md는 on-demand 조회 포인터로 참조한다 [goal] (측정: 룰 파일 존재 + CLAUDE.md에 파일 경로 참조 1건)
- [ ] AR-02: 이 레포 특정 메타 교훈(스킬 호출 증거, 과잉설계 방지)은 프로젝트 memory에 type: feedback로 위치한다 [structural]
- [ ] AR-03: 신규 memory frontmatter는 name/description/metadata.type 3필드를 모두 보유한다 [structural, enumerated]

## Anti-patterns
- [ ] AP-03: 편집/생성한 SKILL.md에 bare code fence가 없다 (validate-plugin V6 OK)
- [ ] AP-04: 편집한 flutter-extract/flutter-provider SKILL.md frontmatter의 name 필드가 유지된다

## Reusability
- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다 (N/A — 룰/문서 승격 작업, 신규 컴포넌트 없음)
- [ ] RE-02: 프로젝트에 이미 동일/유사 규칙이 있으면 새로 만들지 않고 기존을 갱신했다 (Pre-Edit Audit으로 kit Gotcha 비중복 확인 완료)

## Diagnostics
- [ ] DG-01: validate-plugin flutter-toolkit 워닝 0개 (변경 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개
- [ ] DG-03: 측정 명령 실행 시 에러 0개
- [ ] DG-04: N/A — 런타임 구동 없는 문서/룰 승격
