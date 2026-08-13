---
phase: 4
title: "Phase 4 Harness 지원 스킬 — 확보된 외부 근거"
collected: 2026-08-13
method: codex (foreground, 직접 호출)
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라.
---

Codex

웹 검색은 6개 질의로 멈췄고, 파일 수정은 하지 않았습니다. 사용자 제시 “279건 중 244건” 총량은 글로벌 홈 데이터를 직접 재집계하지 못해 **미확인**입니다. 다만 레포 주석에는 2026-07-27 기준 “글로벌 피드백 244건”과 alias 병합 근거가 남아 있습니다.

**1. 관찰 사실**
D1. 문서-스크립트 drift는 이미 재현됩니다. [kaizen-orchestrator SKILL.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/skills/kaizen-orchestrator/SKILL.md:296)는 `<repo>/.claude/kaizen-input/insights-report.md`, `~/.claude/kaizen-input/insights-report.md` 자동 탐색과 `--insights=PATH`를 주장하지만, [collect-kaizen-data.py](/Users/jackson/Hub/10_Dev/claude-plugins/scripts/collect-kaizen-data.py:42)는 `~/.claude/usage-data/report.html` 단일 경로만 갖고, argparse도 `--output`, `--hub-dir`, `--skip-validate`뿐입니다. `python3 scripts/collect-kaizen-data.py --help`도 `--insights`가 없음을 확인했습니다.

D1의 확립된 대응은 있습니다. Python `doctest`는 문서 예제를 실행해 문서가 실제로 동작하는지 검증하는 “executable documentation” 용도라고 설명합니다: https://docs.python.org/3/library/doctest.html. `argparse`는 프로그램의 인자 스펙에서 usage/help와 오류 처리를 생성합니다: https://docs.python.org/3/library/argparse.html. Claude Code도 현재 플러그인 검증에서 frontmatter/hooks/schema를 검사하고 `--strict`로 warning을 error화할 수 있습니다: https://code.claude.com/docs/en/plugins-reference. 스킬 품질 쪽은 mgechev 가이드가 negative trigger와 discovery validation을 권합니다: https://github.com/mgechev/skills-best-practices. Anthropic 스킬 문서도 frontmatter 요구사항, validation loop, feedback loop를 명시합니다: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.

D2. 에러 은폐는 일부 고쳐졌지만 남아 있습니다. [finalize-phase.sh](/Users/jackson/Hub/10_Dev/claude-plugins/scripts/finalize-phase.sh:223)는 과거 `2>/dev/null` 은폐를 주석으로 금지하고 stderr 노출로 바뀌었습니다. 반면 [aggregation-test.sh](/Users/jackson/Hub/10_Dev/claude-plugins/harness/evals/kaizen/feedback-system/aggregation-test.sh:44)는 `yq` 미설치 시 `SKIP` 후 끝에서 “ALL TESTS PASSED”를 출력합니다. [save-test.sh](/Users/jackson/Hub/10_Dev/claude-plugins/harness/evals/kaizen/feedback-system/save-test.sh:74)는 negative test에서 stderr를 버립니다. `finalize-phase.sh --help`는 read-only 환경에서 `mktemp` 때문에 help 출력 전 실패했습니다. 추론: help path가 side-effect free가 아니라 docs-as-code 테스트 대상으로도 취약합니다.

D2의 확립된 대응도 명확합니다. Google Shell Style Guide는 오류를 stderr로 보내고, 복잡한 셸은 구조화 언어로 옮기라고 합니다: https://google.github.io/styleguide/shellguide.html. BashFAQ/105는 `set -e`가 조건문, 파이프, command substitution에서 예측 불가능하므로 명시적 에러 처리가 필요하다고 설명합니다: https://mywiki.wooledge.org/BashFAQ/105. ShellCheck SC2310/SC2312는 `set -e`가 조건부 함수 호출이나 command substitution에서 무력화/마스킹되는 패턴을 잡습니다: https://www.shellcheck.net/wiki/SC2310, https://www.shellcheck.net/wiki/SC2312. Bats는 명령의 exit status와 output을 캡처해 명시적으로 assert하는 패턴을 제공합니다: https://bats-core.readthedocs.io/en/stable/writing-tests.html. SARIF는 `executionSuccessful`과 tool notification을 별도로 두며, 실패한 run의 results를 완전한 분석 결과로 가정하지 말라고 합니다: https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html.

D3. 현재 코드는 query-time alias 방식입니다. [collect-kaizen-data.py](/Users/jackson/Hub/10_Dev/claude-plugins/scripts/collect-kaizen-data.py:48)는 writer identity에 맞춘 allowlist 병합, raw 분포 보존, fuzzy 금지를 명시합니다. [save-feedback.sh](/Users/jackson/Hub/10_Dev/claude-plugins/harness/scripts/save-feedback.sh:7)는 draft identity를 보존하면서 canonical identity를 재계산합니다. [reflect _lib-project-id.sh](/Users/jackson/Hub/10_Dev/claude-plugins/reflect-kit/hooks/_lib-project-id.sh:4)는 basename 기본, 충돌 시 hash suffix, query union을 둡니다. 좋은 방향이지만 backfill 없이 모든 reader가 같은 alias 함수를 호출해야만 맞는 구조입니다.

D3의 확립된 대응은 “canonical id + external/legacy IDs + dual-write + backfill + read-path verification”입니다. Segment 문서는 userId를 lifetime identity로 쓰며 anonymousId와 userId를 연결하고, 기존 userId를 나중에 바꿀 수 없으며 historical event logs는 그대로 남는다고 설명합니다: https://segment-docs.netlify.app/docs/connections/spec/best-practices-identify/. Segment Identity Resolution은 persistent `segment_id`와 여러 externalID 연결 모델을 씁니다: https://segment-docs.netlify.app/docs/unify/identity-resolution/externalids/. Stripe의 online migration 문서는 dual-write, read-path 전환, write-path 전환, old data 제거 4단계와 backfill, old/new read 비교를 설명합니다: https://stripe.com/blog/online-migrations. Sentry fingerprinting은 같은 fingerprint로 grouping하지만 grouping 규칙은 과소/과잉 병합 위험이 있어 감사 가능해야 합니다: https://docs.sentry.io/concepts/data-management/event-grouping/fingerprint-rules/.

**2. 권장안**
D1 조치: `validate-plugin.py` 또는 별도 `scripts/validate-doc-contracts.py`에 “문서 주장 ↔ 실제 인터페이스” 체크를 추가하십시오. Python 스크립트는 `build_arg_parser()`를 import해 option set을 추출하고, SKILL.md에는 자유문장 대신 `docs-contract` fenced YAML로 `script`, `options`, `input_candidates`, `exit_codes`를 선언하게 합니다. CI는 이 YAML과 argparse `_actions`, 상수/함수 반환값을 대조합니다.

D1 조치: `collect-kaizen-data.py --help` snapshot test, `--insights PATH` positive/negative test, “repo/global insights candidate 우선순위” fixture test를 Bats 또는 pytest로 추가하십시오. 문서의 command block은 doctest류 실행 대상으로 분리하고 expected status를 명시합니다.

D1 조치: Claude Code 현재 스키마 drift 방지를 위해 `claude plugin validate ./harness --strict`를 CI optional lane에 두고, 기존 V4 trigger 중복 검사는 유지하되 mgechev식 positive/negative trigger 사례 3개씩을 frontmatter validation fixture로 추가합니다.

D1 넣지 말 것: 전체 Markdown 자연어를 regex로 추론하지 마십시오. “문서만 고치기”도 금지입니다. 실제 source of truth는 parser/manifest여야 합니다.

D2 조치: 게이트 exit taxonomy를 고정하십시오. 예: `0=pass`, `1=policy_violation`, `2=usage_or_infra_error`, `3=no_data_not_run`. `tool_missing`, `parse_failed`, `permission_denied`는 violation count 0이 아니라 `execution_successful=false`/`not_run`입니다.

D2 조치: `2>/dev/null`은 금지 기본값으로 두고, 허용 시 `capture stderr -> assert/log` 패턴만 허용하십시오. Negative test는 stderr를 버리지 말고 “실패해야 하며 특정 에러 메시지가 있어야 한다”를 assert합니다. `aggregation-test.sh`의 `yq` 부재는 Python fallback 또는 exit 2로 바꾸는 것이 맞습니다.

D2 조치: `--help`는 모든 스크립트에서 최상단 인자 처리 후 즉시 출력되게 하십시오. `mktemp`, `cd`, marketplace 읽기, 쓰기 가능한 TMP 의존은 help 이후로 내려야 합니다. ShellCheck는 기본 룰과 함께 SC2310/SC2312 optional 룰을 켭니다.

D2 넣지 말 것: `set -euo pipefail`만으로 “fail loud”가 됐다고 간주하지 마십시오. `command -v tool || echo WARN; exit 0`도 게이트에서는 금지입니다.

D3 조치: alias allowlist를 코드 상수가 아니라 `identity-aliases.yaml` 같은 감사 가능한 테이블로 분리하십시오. 필드에는 `canonical_id`, `alias`, `evidence_type`, `evidence_note`, `first_seen`, `last_seen`, `count`, `status`, `do_not_merge_reason`을 둡니다.

D3 조치: raw YAML은 append-only로 보존하되, backfill 산출물은 별도 normalized index로 만드십시오. 예: `.harness/.meta/feedback-index.jsonl`에 `canonical_project_id`, `raw_project_name`, `raw_project_hash`, `identity_generation`, `source_file`, `backfilled_at`을 기록합니다. 모든 집계 reader는 이 index 또는 단일 normalizer만 사용하게 CI로 강제합니다.

D3 조치: 새 write path는 이미 `draft_project_name` 보존 + canonical 재계산을 하므로 유지하되, `identity_schema_version`을 명시하고 dual-write 기간 종료 조건을 둡니다. backfill 완료율, alias hit rate, unknown legacy rate를 data pool에 출력하십시오.

D3 넣지 말 것: fuzzy name merge, `project_hash` 단독 병합, alias-only 영구 운영, raw name 삭제, 원본 로그 파괴적 rewrite는 피하십시오.

**3. 트레이드오프**
계약 manifest를 두면 문서 작성 비용은 늘지만, drift를 CI에서 기계적으로 잡을 수 있습니다. 반대로 parser help를 regex로만 비교하면 빠르지만 help 문구 변경에 취약합니다.

tool 부재를 exit 2로 올리면 로컬 개발에서 빨간 빌드가 늘 수 있습니다. 대신 “optional check”를 명시적으로 분리해야 합니다.

backfill index는 저장소와 유지비가 늘지만, alias-only보다 reader 누락과 과소집계 위험이 작습니다. 원본 YAML rewrite는 단순하지만 감사성과 롤백성이 나쁩니다.

**4. 열린 질문**
`/insights`의 canonical 입력은 `.claude/kaizen-input/insights-report.md`입니까, 아니면 현재 스크립트의 `~/.claude/usage-data/report.html`입니까?

CI에서 보장할 도구는 `python3+PyYAML`만인가요, `yq`, `claude plugin validate`, `shellcheck`, `bats`까지 포함인가요?

legacy feedback은 원본 rewrite를 절대 금지하고 normalized index만 만들까요, 아니면 승인된 migration script로 일부 backfill rewrite를 허용할까요?
