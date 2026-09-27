# l3b 마크다운 경고 정리 기록

계약: `.harness/sprint-contract-after-0926-mdlint-l3b.md` (봉인 a83801884f4bbe77 · 측정 지문 2dcf946ef53a46d5, 봉인 커밋 4d65af0).
대상은 목록 `.harness/.meta/after-kaizen-0926b/l3b-files.txt` 의 67 개 파일이다. 고치지 않는 파일 28 개와 `.harness/` 는 건드리지 않았다.

## 경고 수

- 시작 판(de8c8cd): 965 건. 규칙별 MD060 818 · MD032 46 · MD025 42 · MD022 27 · MD034 9 · MD058 8 · MD031 4 · MD041 3 · MD037 2 · MD036 2 · MD028 2 · MD038 1 · MD029 1
- 자동 고침(`--fix`, 목록 파일만) 뒤: 95 건. MD060 46 · MD025 42 · MD041 3 · MD028 2 · MD036 2
- 끝: 0 건 (`lint.sh` → `LINTED=67 WARNINGS=0`)

## 규칙별로 한 일

- MD060 46 건(표 6 개): 머리 줄과 구분 줄은 글자 폭으로 맞춰져 있고 본문 줄은 안 맞은 표다. 자동 고침이 손대지 못했다. 표 줄마다 칸 사이 공백을 한 칸으로 맞추고 구분 줄을 `| --- | --- |` 꼴로 바꿨다. `planning-kit/skills/plan-reference/SKILL.md` 표의 빈 칸은 공백 하나로 뒀다. 칸 내용은 그대로다
- MD037 · MD038 · MD029: 자동 고침이 뜻을 바꿨다. `infra-kit/skills/infra-audit/SKILL.md` 의 파일 패턴 `*.yml, *.yaml` · `*.tf, *.hcl` 에서 공백을 지웠고, 같은 파일의 grep 패턴 `^## ` 끝 공백을 지웠고, `tone-kit/skills/tone-guide/SKILL.md` 의 절차 번호 `4.` 를 `1.` 로 바꿨다. 셋 다 시작 판 글자로 되돌리고 그 줄 하나만 `disable-next-line` 으로 껐다
- MD028 2 건: 출처가 다른 원문 인용 두 개씩이다(`howto-kit/references/navigation-anchors.md`). 사이 빈 줄을 `>` 로 채우면 한 인용으로 합쳐지므로, 빈 줄을 두고 두 인용을 `disable MD028` · `enable MD028` 짝으로 감쌌다
- MD036 2 건: 굵은 줄을 제목으로 바꿨다(아래 「제목 단계를 바꾼 자리」)
- MD025 42 · MD041 3: 규칙을 지키면 뜻이 바뀌는 자리라 그 제목 · 첫 줄 한 덩어리만 `disable` · `enable` 짝으로 감쌌다. planning-kit SKILL.md 12 개 · backend-kit · infra-kit SKILL.md 는 `# Gotchas` · `# Process` · `# References` 를 H1 절로 쓰고, `planning-reviewer.md` 는 H1 절 다섯 개로 짜여 있다. tone-kit reference 둘은 앞머리 `title:` 때문에 본문 첫 H1 이 둘째로 세어진다
- 나머지(MD032 · MD022 · MD034 · MD058 · MD031)는 자동 고침 그대로다. 빈 줄과 URL 꺾쇠만 바뀌었고, 목록 항목 사이에 빈 줄이 들어간 자리 · 들여쓴 코드 블록 앞뒤에 빈 줄이 들어간 자리는 0 곳이다(diff 로 확인)

## 끄기 주석

끄기 주석 수: 97

- backend-kit/skills/backend-audit/SKILL.md:32 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- backend-kit/skills/backend-audit/SKILL.md:36 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- backend-kit/skills/backend-audit/SKILL.md:125 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- backend-kit/skills/backend-audit/SKILL.md:129 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- backend-kit/skills/backend-guide/SKILL.md:35 MD025 disable — `# Process (3-Step · 탐색 → 진단 → 처방)` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- backend-kit/skills/backend-guide/SKILL.md:39 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- backend-kit/skills/backend-guide/SKILL.md:86 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- backend-kit/skills/backend-guide/SKILL.md:90 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- backend-kit/skills/backend-system/SKILL.md:35 MD025 disable — `# Process (3-Step · 탐색 → 진단 → 처방)` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- backend-kit/skills/backend-system/SKILL.md:39 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- backend-kit/skills/backend-system/SKILL.md:82 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- backend-kit/skills/backend-system/SKILL.md:86 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- backend-kit/skills/backend-test/SKILL.md:14 MD041 disable — 앞머리 뒤 첫 제목이 `## Gotchas` 다. H1 을 새로 넣으면 낱말이 늘고, `# Gotchas` 로 올리면 스킬 본문 절 단계가 바뀐다
- backend-kit/skills/backend-test/SKILL.md:18 MD041 enable — 바로 위 `disable MD041` 의 짝이다 — 끄는 범위를 그 첫 줄 한 덩어리로 닫는다
- howto-kit/references/navigation-anchors.md:66 MD028 disable — 출처가 다른 원문 인용 두 개라 인용을 둘로 둔다. 사이 빈 줄을 `>` 로 채우면 한 인용으로 합쳐진다
- howto-kit/references/navigation-anchors.md:75 MD028 enable — 바로 위 `disable MD028` 의 짝이다 — 끄는 범위를 그 인용 둘로 닫는다
- howto-kit/references/navigation-anchors.md:157 MD028 disable — 출처가 다른 원문 인용 두 개라 인용을 둘로 둔다. 사이 빈 줄을 `>` 로 채우면 한 인용으로 합쳐진다
- howto-kit/references/navigation-anchors.md:165 MD028 enable — 바로 위 `disable MD028` 의 짝이다 — 끄는 범위를 그 인용 둘로 닫는다
- howto-kit/skills/howto/SKILL.md:17 MD041 disable — 앞머리 뒤 첫 줄이 스킬 소개 문장이다. H1 을 새로 넣으면 낱말이 는다
- howto-kit/skills/howto/SKILL.md:21 MD041 enable — 바로 위 `disable MD041` 의 짝이다 — 끄는 범위를 그 첫 줄 한 덩어리로 닫는다
- infra-kit/skills/infra-audit/SKILL.md:29 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- infra-kit/skills/infra-audit/SKILL.md:33 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- infra-kit/skills/infra-audit/SKILL.md:38 MD037 disable-next-line — `*.yml, *.yaml` · `*.tf, *.hcl` 은 파일 이름 패턴이다. 자동 고침이 `*` 옆 공백을 지워 `*.yml,*.yaml` 로 바꿨다 — 시작 판 글자로 되돌리고 이 줄만 끈다
- infra-kit/skills/infra-audit/SKILL.md:65 MD038 disable-next-line — 코드 조각 `^## ` 끝 공백은 grep 패턴의 일부다(H2 만 센다). 자동 고침이 `^##` 로 지워 H3 이하까지 세게 됐다 — 시작 판 글자로 되돌리고 이 줄만 끈다
- infra-kit/skills/infra-audit/SKILL.md:129 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- infra-kit/skills/infra-audit/SKILL.md:133 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- infra-kit/skills/infra-guide/SKILL.md:33 MD025 disable — `# Process (3-Step · 탐색 → 진단 → 처방)` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- infra-kit/skills/infra-guide/SKILL.md:37 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- infra-kit/skills/infra-guide/SKILL.md:78 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- infra-kit/skills/infra-guide/SKILL.md:82 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- infra-kit/skills/infra-init/SKILL.md:41 MD025 disable — `# Process (3-Step · 탐색 → 진단 → 처방)` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- infra-kit/skills/infra-init/SKILL.md:45 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- infra-kit/skills/infra-init/SKILL.md:112 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- infra-kit/skills/infra-init/SKILL.md:116 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- infra-kit/skills/infra-test/SKILL.md:15 MD041 disable — 앞머리 뒤 첫 제목이 `## Gotchas` 다. H1 을 새로 넣으면 낱말이 늘고, `# Gotchas` 로 올리면 스킬 본문 절 단계가 바뀐다
- infra-kit/skills/infra-test/SKILL.md:19 MD041 enable — 바로 위 `disable MD041` 의 짝이다 — 끄는 범위를 그 첫 줄 한 덩어리로 닫는다
- planning-kit/agents/planning-reviewer.md:15 MD025 disable — `# Inputs` 은 이 에이전트 본문의 절 제목(H1)이다. 한 절만 H2 로 낮추면 다른 H1 절과 층이 어긋나고, 전부 낮추면 파일 전체 뼈대가 바뀐다
- planning-kit/agents/planning-reviewer.md:19 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/agents/planning-reviewer.md:27 MD025 disable — `# Canonical Unverified-Evidence Protocol (정본 복제)` 은 이 에이전트 본문의 절 제목(H1)이다. 한 절만 H2 로 낮추면 다른 H1 절과 층이 어긋나고, 전부 낮추면 파일 전체 뼈대가 바뀐다
- planning-kit/agents/planning-reviewer.md:31 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/agents/planning-reviewer.md:112 MD025 disable — `# Process` 은 이 에이전트 본문의 절 제목(H1)이다. 한 절만 H2 로 낮추면 다른 H1 절과 층이 어긋나고, 전부 낮추면 파일 전체 뼈대가 바뀐다
- planning-kit/agents/planning-reviewer.md:116 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/agents/planning-reviewer.md:232 MD025 disable — `# Gotchas` 은 이 에이전트 본문의 절 제목(H1)이다. 한 절만 H2 로 낮추면 다른 H1 절과 층이 어긋나고, 전부 낮추면 파일 전체 뼈대가 바뀐다
- planning-kit/agents/planning-reviewer.md:236 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-audit/SKILL.md:27 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-audit/SKILL.md:31 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-audit/SKILL.md:149 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-audit/SKILL.md:153 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-data-model/SKILL.md:31 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-data-model/SKILL.md:35 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-data-model/SKILL.md:206 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-data-model/SKILL.md:210 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-discover/SKILL.md:30 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-discover/SKILL.md:34 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-discover/SKILL.md:113 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-discover/SKILL.md:117 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-flow/SKILL.md:27 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-flow/SKILL.md:31 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-flow/SKILL.md:138 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-flow/SKILL.md:142 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-guide/SKILL.md:23 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-guide/SKILL.md:27 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-guide/SKILL.md:86 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-guide/SKILL.md:90 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-ideate/SKILL.md:34 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-ideate/SKILL.md:38 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-ideate/SKILL.md:225 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-ideate/SKILL.md:229 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-prd/SKILL.md:30 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-prd/SKILL.md:34 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-prd/SKILL.md:166 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-prd/SKILL.md:170 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-prioritize/SKILL.md:29 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-prioritize/SKILL.md:33 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-prioritize/SKILL.md:131 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-prioritize/SKILL.md:135 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-reference/SKILL.md:33 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-reference/SKILL.md:37 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-reference/SKILL.md:200 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-reference/SKILL.md:204 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-risks/SKILL.md:28 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-risks/SKILL.md:32 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-risks/SKILL.md:118 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-risks/SKILL.md:122 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-stories/SKILL.md:29 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-stories/SKILL.md:33 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-stories/SKILL.md:154 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-stories/SKILL.md:158 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-sync-github/SKILL.md:33 MD025 disable — `# Process` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-sync-github/SKILL.md:37 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- planning-kit/skills/plan-sync-github/SKILL.md:168 MD025 disable — `# References` 은 이 스킬 본문의 절 제목(H1, `# Gotchas` · `# Process` · `# References` 짜임)이다. 낮추면 스킬 절 단계가 바뀐다
- planning-kit/skills/plan-sync-github/SKILL.md:172 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- tone-kit/references/core-antipatterns.md:7 MD025 disable — 앞머리 `title:` 이 H1 으로 세어져 본문 첫 H1 `# 안티패턴 판정 카탈로그 A~J` 이 둘째가 된다. 앞머리와 본문 제목은 둘 다 그대로 둬야 하고, 이 H1 은 `scripts/sync-docs.py` 가 README 설명으로 옮기는 첫 `# ` 줄이다
- tone-kit/references/core-antipatterns.md:11 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- tone-kit/references/locale-korean.md:10 MD025 disable — 앞머리 `title:` 이 H1 으로 세어져 본문 첫 H1 `# 한국어 축 운영 규칙 (locale-korean)` 이 둘째가 된다. 앞머리와 본문 제목은 둘 다 그대로 둬야 하고, 이 H1 은 `scripts/sync-docs.py` 가 README 설명으로 옮기는 첫 `# ` 줄이다
- tone-kit/references/locale-korean.md:14 MD025 enable — 바로 위 `disable MD025` 의 짝이다 — 끄는 범위를 그 제목 한 줄로 닫는다
- tone-kit/skills/tone-guide/SKILL.md:88 MD029 disable-next-line — 코드 블록 뒤 이어지는 절차의 넷째 단계라 번호 `4.` 가 뜻이다. 자동 고침이 `1.` 로 바꿨다 — 되돌리고 이 줄만 끈다

## 제목 단계를 바꾼 자리

- tone-kit/references/adapter-dart-flutter.md:209 굵은 줄 → H4 「판정」 — 강조로 쓴 제목(MD036)을 바로 위 제목(H3 「3.11 이벤트 콜백 어휘 (D-15)」)보다 한 단계 아래 제목으로 바꿨다. 읽는 도구 확인: `git grep -l -E '\*\*판정\*\*|#### 판정' -- ':(exclude)*.md' ':(exclude).harness'` → 없음. 낱말 「판정」 만으로는 파일 100 여 개가 걸려 굵은 꼴 · 제목 꼴 그대로를 찾았다. `docs/tone-kit/adapter-dart-flutter.html` 은 docs-site 가 만든 html 사본이라 제목 단계를 읽지 않는다
- tone-kit/references/core-naming.md:139 굵은 줄 → H3 「N-12 · SHOULD · 어휘 축」 — 강조로 쓴 제목(MD036)을 바로 위 제목(H2 「6. 프레임워크 어휘 우선」)보다 한 단계 아래 제목으로 바꿨다. 읽는 도구 확인: `git grep -F -l -- 'N-12 · SHOULD · 어휘 축' -- ':(exclude)*.md' ':(exclude).harness'` → 없음

## 측정 도구 결함 (봉인된 `meaning.py`)

`meaning.py` 의 SPACING 은 파일마다 처음 다른 글줄 하나만 센다(`check_file` 이 첫 차이에서 멈춘다). `infra-kit/skills/infra-audit/SKILL.md` 에는 자동 고침의 공백 삭제가 두 자리(`*.yml, *.yaml` 줄 · `^## ` 코드 조각) 있었는데, 첫 측정은 앞 자리만 `SPACING=1` 로 냈다. 코드 조각만 따로 뽑아 시작 판과 맞대는 임시 검사(scratch 의 `spans.py`)로 뒷자리를 찾았고, 둘 다 되돌린 뒤 두 검사 모두 0 이다. 측정 묶음은 봉인돼 있어(SC-02) 고치지 않았다. 다음 묶음의 `meaning.py` 는 다른 줄을 전부 내야 한다.

## 남은 것

- 목록 밖 경고: 고치지 않는 파일 28 개의 경고 45 건은 이 묶음 밖이라 그대로다
- 바꾼 md 에 짝이 있는 docs html 페이지(`docs/tone-kit/adapter-dart-flutter.html` · `docs/tone-kit/naming-taxonomy.html` 등)는 다시 만들지 않았다. 바뀐 것은 모양뿐이라 페이지 내용과 어긋나지 않는다
- QA 판정은 아직이다
