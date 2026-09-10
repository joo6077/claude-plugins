# Sprint Feedback
Feature: howto-research 6 사이클 — procedure-standards 확정 · DITA 모델 명시
Evaluated: 2026-09-10 14:20
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-howto-research-procedure-standards.md
- sha256: dcd6bf571f1372ac81f239bf1bdf33b6e9a05510fac580ba6868e88410d5cbf4
- status: active
- slug: howto-research-procedure-standards
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시경로 — 사용자가 계약 경로를 직접 지정)
- legacy_contract_used: false
- seal_status: SEAL_OK
- contract_seal_broken: n/a
- 재확인(Step 5): 일치
- status_transition: active -> done (APPROVE)

## Amendments
- amendments: 0 (사이드카 부재 확인 — find .harness -iname "sprint-amendments-howto-research-procedure-standards.md" 결과 없음)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins/2026-09.md)
- unreflected_corrections: 0 (계약 locked_at 12:10 ~ 평가 시각 구간에 해당 로그 항목 없음)
- verdict 영향: 없음

## Results

### Skill (3/3)
- [x] SK-01: `step-contract.md` 의 `<taskbody>` 인용이 strict task model 임을 명시 + 두 모델 존재 서술 — PASS
  - 근거: `howto-kit/references/step-contract.md:74-88` (awk 절 추출 측정, `strict` 2회, `two task models` 1회). L3 — 원문 대조 결과(아래 DITA 검증 참조)와 서술이 일치.
- [x] SK-02: SKILL.md DITA 인용에 조회일 + 정본 포인터 — PASS
  - 근거: `howto-kit/skills/howto/SKILL.md:81-83` (`grep -A2` 결과에 `2026-09-10`, `procedure-standards.md` 등장)
- [x] SK-03: `verify` 필수 규칙 유지 + 강화 명시 — PASS
  - 근거: `howto-kit/references/step-contract.md:47` (`verify`|**필수 (예외 없음)**| 변경 없음), `:52-57` (`### verify 를 모든 스텝에 요구하는 이유` 절에 `강화`·`stepresult` 인용 공존). 규칙이 약화되지 않았음을 diff로 확인 — 이전에도 "필수 (예외 없음)"이었고 이번에도 동일.

### Script (3/3)
- [x] SC-01: CI validate 8종 전부 exit 0 — PASS
  - 측정값(실행): validate-plugin.py=0, sync-evals.py --check-only=0, sync-docs.py --check-only=0, sync-orchestrator.py --check-only=0, run-evals.py --verbose=0(106 passed/0 failed), check-contrast-claims.py=0(어긋난 것 0), check-docs-links.py=0(358개 링크·176 등록·고아 없음), check-stale-values.py=0(133파일·되살아난 옛 값 없음)
- [x] SC-02: `howto-kit/evals/run-evals.sh` exit 0, pass=12 fail=0 — PASS
  - 측정값(실행): `EVALS total=12 pass=12 fail=0` / `EVALS_PASS` / exit 0
- [x] SC-03: `node scripts/check-docs-a11y.js docs/howto-kit/procedure-standards.html` exit 0 — PASS
  - 측정값(실행): `OK procedure-standards.html ... err=0 contrastFail=0` / `1/1 PASS` / exit 0. 정적 음성 대조: `--text3` 값이 라이트 `#656C7A`, 다크 `#948779`로 계약 낮춤값(`#7A6F64`)과 다름을 확인(discrimination: static-only, 안전조건 불충족으로 실행 변형은 생략).

### Error (4/4)
- [x] ER-01: 확정 인용 7건 각각에 출처 URL + 조회일 — PASS (enumerated 전수 확인)
  - 근거: `docs/howto/procedure-standards.md:18-25` 표에서 DITA `<cmd>`(18행) · DITA `<stepresult>`(19행) · DITA 두 모델(20행) · Google 한 스텝 한 동작(22행) · Google 결과 순서(23행) · Microsoft 번호 목록(24행) · Microsoft 명령형(25행) 7건 전부 출처열 비어있지 않음 확인. `2026-09-10` 5회 등장(`grep -c`).
- [x] ER-02: `verify` 가 표준보다 강하다는 사실 명시, 약화 없음 — PASS
  - 근거: `docs/howto/procedure-standards.md:63,65,78,109` — `should not be used for every step` 와 `강화` 토큰 공존, 표준을 안 따르는 이유(무증상 실패 데이터) 서술. **직접 재현**: DITA stepresult.html 원문 = *"...but should not be used for every step as this quickly becomes tedious."* (verbatim raw HIT, 아래 인용 대조 참조) — 인용이 정확함을 확인.
- [x] ER-03: ISO·verification 규정이 리터럴 `확인 실패`로 원장에 남고 시도 URL 열거 — PASS
  - 근거: `howto-kit/references/provenance-notes.md:226-237` — ISO 행·verification 행 각각 `확인 실패` 리터럴 등장, ISO 시도 URL 3개 + verification 시도 URL 2개(각 항목 1개 이상 충족). 직접 재현: `https://www.iso.org/standard/77451.html`, `.../70880.html` 실제로 HTTP 403 + 5438바이트(≈5.3KB, 문서 서술 "5.5KB 스텁"과 근사) Cloudflare 챌린지 스텁 응답 확인 — 접근 차단 주장이 사실임을 직접 검증.
- [x] ER-04: 검증 함정 대조기의 실측(`raw=miss`/`norm=HIT`)이 남음 — PASS, **직접 재현 성공**
  - 근거: `docs/howto/procedure-standards.md:133` `raw=miss norm=HIT`, 어느 인용인지(Google "State the action first and the result second") 명시.
  - 재현: `curl developers.google.com/style/procedures` 원문에서 해당 문장이 `...the result\n    second.`로 줄바꿈+들여쓰기로 분리되어 있음을 직접 확인. 단순 정규식 exact-match는 MISS, 공백 정규화(개행+들여쓰기 collapse) 후에는 HIT. 계약의 ER-04 주장이 정확히 재현됨.

### Architecture (6/6)
- [x] AR-01: `docs/howto/procedure-standards.md` 존재 — PASS (`test -f` 성공)
- [x] AR-02: 리서치 문서 6종 개별 존재 — PASS (enumerated 전수, 6개 각각 `test -f` 성공: deep-links.md, ui-anchoring.md, branch-catalog.md, deprecation-policy.md, changelog-feeds.md, procedure-standards.md). 부가 확인(계약 범위 밖, 보고 목적): `docs/index.html`에 6종 전부 등록됨 — `howto-deep-links`/`howto-ui-anchoring`/`howto-branch-catalog`/`howto-deprecation-policy`/`howto-changelog-feeds`/`howto-procedure-standards` 각 count=2 (pages 배열 1 + getIcon 1).
- [x] AR-03: HTML 미러 존재 + `docs/index.html`에 동일 id로 2곳(pages/getIcon) 등록 — PASS
  - 근거: `docs/index.html:574`(`id: 'howto-procedure-standards'`, pages 배열 file: 항목), `:680`(getIcon 매핑). `grep -c`=2.
- [x] AR-04: accent/text3/localStorage 토큰 5개 리터럴 전부 등장 — PASS (enumerated 전수)
  - 근거: `docs/howto-kit/procedure-standards.html:11-12`(dark `--text3:#948779`, `--accent:#F59E0B`), `:20-21`(light `--text3:#656C7A`, `--accent:#B45309`), `dk-theme` count=2. 다크/라이트 블록 위치까지 확인(L3).
- [x] AR-05: 400줄 이상 + 외부 리소스 0건 — PASS
  - 측정값: `wc -l`=410 (기준: >=400). 외부 리소스 로드 패턴 매치=0.
- [x] AR-06: 변경 범위가 선언 경로와 정확히 일치 — PASS
  - 측정 상태: `origin/main...HEAD` (계약이 명시한 Given 그대로 사용). scoped(`docs howto-kit .harness` 제외 `.claude/worktrees` `result.json`) 결과와 전체 diff 결과가 `diff` 명령으로 바이트 단위 완전 일치(exit 0), 8개 파일 모두 동일.

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 0건 — PASS (`validate-plugin.py --check=code-fence` 전체 14 플러그인 `V6 code-fence 0 bare — OK`, exit 0)
- [x] AP-04: frontmatter name 필드 누락 없음 — PASS (`validate-plugin.py` 전체 실행 `14 plugins, 14 OK`, exit 0)

### Reusability (2/2)
- [x] RE-01: 재사용 가능 컴포넌트를 private으로 만들지 않음 — PASS (이번 스프린트는 신규 재사용 컴포넌트를 만들지 않음 — 문서·HTML 미러만 추가)
- [x] RE-02: HTML 미러가 `deprecation-policy.html` 토큰/토글 구조 재사용 — PASS
  - 근거: `diff`로 두 파일의 상위 40행(CSS 토큰 블록) 거의 동일(title만 차이), 테마 토글 스크립트의 `dk-theme` localStorage 키 사용 패턴이 두 파일에서 동일하게 재현됨(`deprecation-policy.html:455,466` vs `procedure-standards.html:391,402`).

### Diagnostics (4/4)
- [x] DG-01: `bash -n scripts/release.sh` 워닝 0개 — PASS (exit 0)
- [x] DG-02: N/A — 계약 명시 사유(IDE 진단 MCP 부재 + `commands.lint: null`) 확인됨(`project.yaml` 대조), 대체 검증 AP-03/04 PASS로 충족
- [x] DG-03: 콘솔 로그 에러/예외 0개 — PASS (`bash scripts/release.sh 2>&1`은 인자 누락 usage 메시지만 출력, 에러/예외 없음)
- [x] DG-04: N/A — 계약 명시 사유(플러그인 모노레포, 앱/서버 없음) 확인됨, SC-03 a11y 게이트로 대체 검증 완료

## DITA "two task models" 원문 직접 검증 (사용자 지시 항목 3)
- `taskbody.html` 원문 직접 조회(curl) 결과, *"Beginning with DITA 1.2, the DTD and Schema packages distributed by OASIS contain two task models. The general task model allows two additional elements... The strict task model maintains the order and cardinality of the DITA 1.0 and 1.1 content model."* 및 *"this constraint is used in the default task distributed by OASIS."* 모두 verbatim 확인 (raw HIT).
- `cmtct.html` (콘텐츠 모델 부록, 킷이 원래 인용했던 URL) 원문에서 strict 모델 시퀀스 `<prereq>?, <context>?, (<steps>|<steps-unordered>)?, <result>?, ..., <postreq>?`와 general 모델 `(<prereq>|<context>|<section>)*, (<steps>|<steps-unordered>|<steps-informal>)?, <result>?, ..., <postreq>*`를 각각 직접 확인 — 순서/개수 고정 vs 자유·다중 인스턴스 허용이라는 문서의 구분이 정확함.
- 결론: **킷의 원래 인용은 오류가 아니라 불완전함이었다**는 이번 스프린트의 판정이 정확하다. ER-04/SK-01의 처리는 타당.

## 하류 갱신 누락 조사 (사용자 지시 항목 7 — 자체 전수 탐색)
- `grep -rln DITA howto-kit/ docs/`로 DITA 인용 파일 전수 탐색: `step-contract.md`(수정됨), `skills/howto/SKILL.md`(수정됨), `docs/howto/procedure-standards.md`(신규), `docs/howto-kit/procedure-standards.html`(신규), **`docs/howto/design-brief.md`(부분 수정)**.
- **발견**: `docs/howto/design-brief.md:237`에 `<prereq>?, <context>?, (<steps>|<steps-unordered>)?` 모델을 여전히 모델명 명시 없이 인용하고 있다. 이 문서는 "설계 시점 스냅샷이라 고치지 않는다"고 명시된 `drafts/SKILL.md`와 달리, frontmatter가 "다른 세션이 이 문서만 읽고 킷을 만들 수 있게 하는 설계 정본"이라 밝히는 활성 참조 문서이며, 이번 스프린트에서 실제로 401행(ISO 항목)은 갱신되었다. GAP 분석 표는 design-brief.md의 변경 범위를 401행(ISO)으로만 한정했고 237행(DITA taskbody 모델)은 다루지 않았다.
- 이 건은 24개 조건 중 어느 것도 문자 그대로 요구하지 않으므로(SK-01은 `step-contract.md`만, GAP 표는 design-brief.md의 변경을 401행으로 명시적으로 한정) **조건 FAIL로 처리하지 않는다.** 다만 계약 스코프의 완전성 결함으로 Improvement에 기록한다.

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (24 - 0) / 24 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 없음 (전 조건 실측 완료)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 — 이번 스프린트는 문서/리서치 콘텐츠이며 동시성 가드·인증·멱등성·입력검증·데이터유실·마이그레이션·재시도·보안경계·사용자보고충돌 어느 항목에도 해당하지 않는다.

## User-Reported Failures
- 보고 없음.

## Evidence Validity
- 검사 대상 증거: 24건 (조건별) + 인용 8건 원문 대조 + DITA 두 모델 원문 대조 2건
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 해당 없음 (이 계약에는 사용자 대상 셸 스니펫 문서가 없음 — HTML/MD 리서치 산출물)
- 원문 인용 재현: 8/8건 실제 URL을 curl로 조회하여 원문 대조 완료 (DITA cmd, DITA stepresult, DITA taskbody 두 모델×2, Google 액션 우선, Google 결과 순서[raw=miss/norm=HIT 재현], Microsoft 번호 목록, Microsoft 명령형[raw HIT, 정상 텍스트 추출 시])
- 무효 0건은 미검증 카운터에 영향 없음

## Summary
- Total: 24/24 conditions passed
- Verdict: APPROVE
- 특이사항: 계약 조건 자체는 전부 충족하나, `docs/howto/design-brief.md:237`의 DITA taskbody 인용이 이번 사이클의 모델 명시 갱신에서 누락되었다(계약 스코프 밖). 다음 사이클/후속 작업에서 정리 권장.

## Improvement Suggestions
- [GAP분석-완전성] 측정-산출물-부재 — `docs/howto/design-brief.md:237`의 `<prereq>?, <context>?, (<steps>|<steps-unordered>)?` DITA 인용에도 SK-01과 동일하게 "strict task model" 명시 + `procedure-standards.md` 정본 포인터를 추가하는 후속 조건을 다음 계약에 명시할 것.
