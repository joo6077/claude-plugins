---
phase: 12
title: "Phase 12 reflect-kit — 확보된 외부 근거"
collected: 2026-08-13
method: codex (foreground, 직접 호출)
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치·설정 키를 지어내지 마라.
---

출처 유형: WebSearch fallback

**1. 관찰 사실**

K1. canonicalization 파편화  
- 사용자 제공 실측상 `edit-before-read` 27건, `edited-before-read` 4건인데, 현재 훅 프롬프트 예시는 소수형인 `edited-before-read`입니다: [log-reflection.sh](/Users/jackson/Hub/10_Dev/claude-plugins/reflect-kit/hooks/log-reflection.sh:161). 현재 훅은 과거 태그를 빈도 `>=2` 상위 40개로 주입하지만, 형태소/시제/동의어를 결정론적으로 정규화하지는 않습니다: [log-reflection.sh](/Users/jackson/Hub/10_Dev/claude-plugins/reflect-kit/hooks/log-reflection.sh:91).  
- Reflexion 원전은 arXiv ID `2303.11366`으로 존재합니다. 방법론은 weight update가 아니라 verbal feedback을 episodic memory에 저장해 다음 trial의 의사결정에 주입하는 구조입니다: https://arxiv.org/abs/2303.11366, https://arxiv.org/html/2303.11366  
- Sentry 지정 URL은 본문 직접 확인이 실패했습니다. 미확인: 정확한 “really bad groups” 문구. 다만 현재 `reflect-digest` 문서는 그 URL을 과잉 병합 경고 근거로 이미 인용하고 있습니다: [reflect-digest/SKILL.md](/Users/jackson/Hub/10_Dev/claude-plugins/reflect-kit/skills/reflect-digest/SKILL.md:122). 접근 가능한 getsentry 이슈는 fingerprint rules matcher가 glob 기반이라고 설명합니다: https://github.com/getsentry/sentry/issues/75567  
- Prometheus Alertmanager는 `group_by`로 묶을 라벨을 명시하며, 모든 라벨로 넘기면 aggregation을 사실상 끄는 것으로 “대개 원하지 않는 설정”이라고 설명합니다. `repeat_interval`은 기존 그룹의 반복 알림을 억제합니다: https://prometheus.io/docs/alerting/latest/configuration/  
- 닫힌 라벨 집합 관련: Artstein & Poesio는 annotator agreement가 reliability의 전제이지만 validity를 보장하지 않고, category 수가 적으면 우연 일치가 높아진다고 정리합니다. 추론: 강제 closed set은 일관성 수치를 올릴 수 있지만 새 근본원인을 기존 라벨로 collapse시킬 위험이 큽니다: https://aclanthology.org/J08-4004/

K2. 승격 규칙 재위반 증가  
- Claude Code 공식 docs상 `PreToolUse`는 tool call 직전에만 실행되며, `@` 파일 참조에는 실행되지 않습니다. `PostToolUse`는 이미 성공한 tool 뒤에 실행되어 예방이 아니라 피드백입니다. `exit 2`는 `PreToolUse`를 block하지만, `PostToolUse`에서는 stderr를 Claude에게 보여줄 뿐 이미 실행된 도구를 되돌릴 수 없습니다. timeout 난 command/http/mcp PreToolUse hook은 tool call을 막지 않습니다: https://code.claude.com/docs/en/hooks  
- 현재 plugin hooks.json에는 `UserPromptSubmit`, `PostToolUseFailure`, `Stop`만 있고 PreToolUse hard gate는 없습니다: [hooks.json](/Users/jackson/Hub/10_Dev/claude-plugins/reflect-kit/hooks/hooks.json:1). 사용자가 별도 등록한 PreToolUse가 있다면, 위반 증가 신호는 먼저 matcher/설치/timeout/exit-code/coverage 문제로 봐야 합니다.  
- alert fatigue 근거: Sendelbach & Funk는 clinical alarm의 72-99%가 false alarm이라는 연구를 요약하고, 과다 경보가 desensitization과 missed alarms로 이어질 수 있다고 설명합니다: https://pubmed.ncbi.nlm.nih.gov/24153215/

K3. post_freq 구조적 과소집계  
- 문서상으로는 이미 `mistake_tag + aliases` 합산을 요구합니다: [SCHEMA.md](/Users/jackson/Hub/10_Dev/claude-plugins/reflect-kit/docs/SCHEMA.md:115), [reflect-promote/SKILL.md](/Users/jackson/Hub/10_Dev/claude-plugins/reflect-kit/skills/reflect-promote/SKILL.md:178).  
- 그런데 K1 실측처럼 alias가 누락되면 `post_freq`가 canonical 단독 키가 되어 재발을 과소집계합니다. 추론: 이건 Goodhart형 실패입니다. 측정 단위가 근본원인이 아니라 표면 태그가 되면서, 실패한 규칙이 “효과 있음”으로 남습니다. Prometheus의 `group_by` 설계가 보여주듯 집계 키 선택 자체가 신호 품질을 결정합니다: https://prometheus.io/docs/alerting/latest/configuration/

**2. 권장안**

- `log-reflection.sh`의 canonical 예시는 즉시 기본형 `edit-before-read`로 바꾸는 것이 맞습니다. 원칙은 `<lemma-verb>-<object>`입니다. 예: `edited|editing|edit -> edit`, `skipped|skip -> skip`, `used|use -> use`.  
- known tags 주입은 raw tag 목록이 아니라 `canonical_tag -> aliases(freq)` 형태로 넣어야 합니다. canonical은 기본적으로 최빈 태그를 쓰고, 최빈이 아닌 표기를 canonical로 강제하려면 수동 override 사유를 ledger에 남겨야 합니다.  
- deterministic normalization pass를 LLM 앞에 둡니다: lowercase, quote trim, kebab normalize, verb lemma map, synonym map, explicit alias table. LLM은 새 alias 후보의 근거를 설명하게만 하고, 최종 병합은 결정론적 규칙+감사표로 고정합니다.  
- `stale X` 계열은 무조건 하나로 합치지 마세요. `undesired_behavior`와 `desired_behavior`가 같은 경우에만 alias로 묶고, remediation이 다르면 `stale-context-reference` 같은 family만 별도 보고하십시오.  
- 닫힌 라벨 집합을 hard enum으로 넣지 마세요. 대신 “known canonical 우선, 새 tag 허용, 새 tag에는 `new_tag_reason` 필요”가 안전합니다. closed set은 새 원인을 기존 라벨로 흡수해 agreement만 높일 수 있습니다.  
- `reflect-promote`에는 “이미 hook/CLAUDE.md에 승격했는데 post_freq가 증가” 분기를 추가해야 합니다. 이 경우 같은 문구 재승격이 아니라 `hook_coverage_audit`로 라우팅합니다: hook installed, matcher, event type, path normalization, exit code 2, timeout, executable, dependency, fired/blocked counters를 확인.  
- API 문서 확인 규칙은 단순 경고가 아니라 “Edit/Write/Bash 변경 직전, 이번 turn/session에 공식 docs 조회 증거가 없으면 block”처럼 eligibility denominator가 분명해야 합니다. PostToolUse는 예방 surface가 아닙니다.  
- `reflect-kaizen`은 파편화 지표가 임계 초과일 때 ledger calibration을 invalid/low-confidence로 표시해야 합니다. 이 상태에서 `post_freq==0` demotion 후보를 내면 안 됩니다.  
- 집계는 `raw_tag`, `canonical_tag`, `aliases`, `root_cause_id`, `family`를 분리하십시오. 효과 측정은 `root_cause_id` 또는 canonical+aliases 합산으로 하고, raw tag는 감사용으로 보존합니다.

**3. 트레이드오프**

- open vocabulary + alias 감사는 운영 부담이 늘지만, 새 실패 모드를 보존합니다. closed label set은 편하지만 label collapse와 false consistency가 큽니다.  
- hard gate는 위반을 줄일 수 있지만 false positive가 많으면 alert fatigue가 생깁니다. 그래서 gate에는 fired/blocked/bypassed/timeout 지표가 필요합니다.  
- canonical을 최빈 태그로 잡으면 실사용과 맞지만, 나중에 더 좋은 이름으로 바꾸기 어렵습니다. 수동 override는 가능하되 alias migration 근거를 남겨야 합니다.

**4. 열린 질문**

- 사용자가 등록한 `skipped-required-api-doc-check` PreToolUse 훅의 실제 위치, matcher, exit code, timeout, 실행권한, fired 로그가 필요합니다.  
- `stale-widget-ref`, `stale-mcp-connection`, `stale-inspector-ref`, `stale-diagnostics-oracle`의 `undesired_behavior/desired_behavior` 샘플이 필요합니다. 같은 root cause인지 family만 같은지 아직 미확정입니다.  
- Sentry 지정 URL의 정확한 “really bad groups” 원문은 이번 접근에서 직접 확인하지 못했습니다.  
- 2026-08 실측 로그 원본은 현재 sandbox 밖이라 독립 재집계하지 못했습니다.
