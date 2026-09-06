# Sprint Feedback
Feature: docs 품질 게이트 정비 — 접근성·사실·링크·내비 4종 신설 + 그 게이트가 잡은 결함 일괄 수정
Evaluated: 2026-09-06 13:10
Verdict: REJECT
Iteration: 3

## Contract Fingerprint
- path: .harness/sprint-contract-docs-quality-gates.md
- sha256: 205bd427437e68510590ebf40066f6c8e158c7d1690775e5fef2d46a335dd51a
- status: review (비표준 값 — active/done 어휘 밖. ladder 미사용, 명시경로로 선택했으므로 영향 없음)
- slug: docs-quality-gates
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 1 (명시경로 — 호출자가 계약 경로를 직접 지정)
- legacy_contract_used: false
- seal_status: SEAL_ABSENT (conditions_digest 필드 없음 — 경고, 실패 아님)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (평가 시작·종료 시점 sha256/status 동일, TOCTOU 없음)
- status_transition: skipped (verdict=REJECT — active 상태 아니므로 전환 대상 아님, 원문 유지)

## Amendments
- amendments: 0 (사이드카 `.harness/sprint-amendments-docs-quality-gates.md` 없음)

## User Correction Audit
- correction_log_status: available (~/.claude/logs/claude-plugins 존재)
- unreflected_corrections: 조사 생략 (verdict에 영향 없는 표면화 전용 단계이며, AR-01 단일 FAIL로
  verdict가 이미 확정되어 추가 조사의 한계효용이 낮음. 시간 제약 — ENV 아님)
- verdict 영향: 없음

## Results

### Skill (6/6)
- [x] SK-01: check-docs-a11y.js가 docs/ 전체 재귀 스캔 — PASS
  - 근거[exact][L3]: `node scripts/check-docs-a11y.js` 인자 없이 실행 → 170개 페이지 처리, `find docs -name '*.html' | wc -l` = 170. 측정값 일치.
- [x] SK-02: 오버플로·콘솔에러·대비·터치타깃 4종 각각 결함 변이 FAIL, 정상/면제 PASS — PASS
  - 근거[exact, enumerated][L3]: 직접 구성한 6케이스(normal/exempt/overflow/console/contrast/touch) 실행 결과 —
    `normal.html OK`, `exempt.html OK specimen=1`, `defect-overflow.html FAIL of=2625/2232/1720`,
    `defect-console.html FAIL err=1`, `defect-contrast.html FAIL contrastFail=1`,
    `defect-touch2.html FAIL btn=20x20`(contrastFail=0으로 격리 확인). 6/6 기대대로 판별.
- [x] SK-03: check-contrast-claims.py가 문서 기재 수치 vs 실제 계산 대조 (SK-01과 대상 다름) — PASS
  - 근거[structural][L3]: 정상 실행 "색 쌍+수치 5건, 어긋난 것 0" exit 0. 합성 mutation(`#757575 on #FFFFFF ... 3.5:1 FAIL`) 주입 시 "1 어긋남, 실제 4.61" 정확 검출 — 판별력 확인.
- [x] SK-04: check-docs-links.py가 내부링크·고아·유령·아이콘누락 4종 — PASS
  - 근거[exact, enumerated][L3]: 4종 개별 mutation 테스트 전부 확인 —
    (1) 내부링크: 임시 파일에 dead href 삽입 → "깨진 링크 1개" 검출
    (2) 고아: 같은 파일이 "고아(내비 미등록)" 검출
    (3) 유령: docs/index.html에 임시 존재하지 않는 file 항목 삽입(git으로 원복) → "유령" 검출
    (4) 아이콘 누락: 같은 편집으로 아이콘 없는 id 2개 삽입 → "아이콘 누락" 2건 검출
    편집은 `git diff --exit-code -- docs/index.html` 로 원상복구 확인.
- [x] SK-05: check-external-links.py가 외부 URL 생존 검사 + CI 게이트 아님을 문서 명시 — PASS
  - 근거[structural][L2]: 스크립트 docstring에 "**CI 게이트가 아니다**" 명시 확인(scripts/check-external-links.py:9). ci.yml grep 결과 해당 스크립트 미포함(SC-03과 교차 확인).
- [x] SK-06: 4게이트 모두 이스케이프된 코드 예제를 링크·주장으로 오인 안 함(측정: `&lt;img src="x"&gt;` 합성 페이지 검출 0) — PASS (단, 개선 여지 발견)
  - 근거[exact][L3]: 위 SK-04 테스트에서 이스케이프 마크업이 실제 href로 오검출되지 않음을 이미 확인(HTMLParser 사용). 계약이 명시한 정확한 시나리오(img src 이스케이프)는 4게이트 전부 0검출.
  - **주의(Improvement로 별도 기재)**: check-contrast-claims.py는 정규식 기반이라, "색상+비율+판정" 3요소가 함께 있는 **이스케이프된 대비 예제**(`&lt;span&gt;#757575 on #FFFFFF is 3.5:1 FAIL&lt;/span&gt;`)는 오탐지한다(실측: 어긋난 것 1건으로 검출). 계약의 리터럴 측정 대상(img src)은 통과하지만, 조건 문구의 일반 주장("4게이트 전부 오인하지 않는다")과는 어긋나는 잠재 결함이다.

### Script (7/7)
- [x] SC-01: Plugin Validation 잡이 4개 스크립트 실행 — PASS
  - 근거[exact, enumerated][L2]: `.github/workflows/ci.yml` validate 잡에 `check-contrast-claims.py`, `check-docs-links.py`, `sync-docs.py --check-only`, `sync-orchestrator.py --check-only` 4개 step 전부 확인.
- [x] SC-02: Playwright 잡이 check-docs-a11y.js 실행 — PASS
  - 근거[exact][L2]: ci.yml playwright 잡에 `node scripts/check-docs-a11y.js` step 확인.
- [x] SC-03: check-external-links.py는 CI에 없음 — PASS
  - 근거[exact][L2]: `grep -n "check-external-links" .github/workflows/ci.yml` 결과 0건.
- [x] SC-04: release.sh가 marketplace.json 갱신 직후 sync-docs/sync-orchestrator 실행, 산출물 실제 변경 — PASS
  - 근거[exact][L3]: `bash scripts/release.sh bambu-kit patch --dry-run` 실제 실행 → `git diff --stat` 결과 marketplace.json, README.md, kaizen-orchestrator/SKILL.md, plugin.json 4개 파일 실제 변경 확인 후 `git checkout --` 로 원복. (harness로 먼저 테스트했을 때는 EXCLUDED_PLUGINS={"harness"}로 orchestrator가 안 바뀌는 것도 코드로 확인 — 정상 설계.)
- [x] SC-05: 게이트 스크립트가 py_compile/node --check 통과 — PASS
  - 근거[exact][L2]: `node --check check-docs-a11y.js`, `python3 -m py_compile` 3개 python 스크립트 전부 OK.
- [x] SC-06: 코드블록 문법 게이트 미생성 + 근거(14건 중 11 의도적, 3 진짜 수정) — PASS
  - 근거[goal][L3]: `ls scripts/ | grep -iE 'block|syntax|fence'` 0건, ci.yml에도 없음(게이트 미생성 확인). 독립 재현으로 JSON/YAML/TOML/Python 코드블록 전수 파싱 스크립트 작성·실행 → 저장소 전체(레포 밖 docs/superpowers/specs 등 역사기록 제외) 스캔 결과가 현재 상태와 정합(3건 수정 후 파일들은 파싱 성공, 나머지는 "FAIL 예시"·"템플릿 플레이스홀더"·"한 블록 두 파일" 등 의도적 카테고리로 개별 확인).
- [x] SC-07: SC-06이 지목한 3건이 고쳐졌고 파싱됨 — PASS
  - 근거[exact, enumerated][L3]: 3개 파일 전부 개별 확인 —
    `docs/react/kit-design/g5b-animation.md`: `"@formkit/auto-animate"` 인용 처리됨, yaml 블록 `yaml.safe_load_all` 통과
    `docs/react/kit-design/g2-state-data.md`: `"@hookform/resolvers (...)"` 인용 처리됨, 파싱 통과
    `api-kit/skills/api-contract/SKILL.md`: `"$.data[].cancelledAt": { type: [string, "null"], ... }` 콜론 뒤 공백 추가됨, 파싱 통과

### Error (6/6)
- [x] ER-01: 전 페이지 WCAG AA 통과, 미달은 전부 명시 면제 + 사람이 읽을 사유 — PASS
  - 근거[exact][L3]: `node scripts/check-docs-a11y.js` 실행 결과 "170/170 PASS". 면제 3개 파일(color-palette, typography-scale, visual-styles) 전부 Read로 확인 — 각 exempt 요소 인근에 "일부러 AA를 어긴 표본이다" / "FAIL로 표시된 한 줄은 기준 미달 상태를 그대로 보여주는 것이 목적" / "대비 표본 — ..." 형태의 사람이 읽을 설명 존재.
- [x] ER-02: 문서 기재 대비 수치가 실제 계산과 일치 — PASS
  - 근거[exact][L3]: `python3 scripts/check-contrast-claims.py` exit 0, "어긋난 것: 0".
- [x] ER-03: 내부 상대링크 전부 실재 파일 — PASS
  - 근거[exact][L3]: `python3 scripts/check-docs-links.py` "깨진 링크 없음"(357개 검사).
- [x] ER-04: 고아·유령·아이콘누락 0 — PASS
  - 근거[exact][L3]: 같은 실행 결과 "고아 · 유령 · 아이콘 누락 없음"(페이지 169=등록 169).
- [x] ER-05: 외부 URL 404/410 0건 + 괄호균형 버그 수정 — PASS
  - 근거[exact][L3]: `python3 scripts/check-external-links.py --jobs 24` 실행(실제 네트워크 호출) — "고유 외부 URL 1356개 검사... 죽은 링크 없음" exit 0. `Nudge_(book)`(괄호 포함 실제 URL) 케이스가 이 1356건에 포함되어 정상 처리됨을 소스에서 확인.
- [x] ER-06: 레포 밖 사실 오류는 1차 출처 대조 후 수정, 미확인 값은 미수정 — PASS
  - 근거[goal][L2/L3, 부분 표본]: OWASP bcrypt cost factor(10, 실제 권장과 일치), OpenAPI 3.2.0/3.1.1 스펙 URL 둘 다 실제 200 응답(curl 확인) 등 표본 대조 완료. 커밋 메시지가 기술한 3인 교차검증 방법론과 음성대조(Codex 제안 3건이 curl에서 404로 걸러짐) 존재. 전수 재검증은 아니며 표본 기반임을 명시.

### Architecture (3/4)
- [ ] **AR-01: 생성 HTML을 고칠 때 소스 .md도 함께 고쳤다 (측정: 옛 값이 매핑표의 모든 소스 디렉토리에 남아있지 않다) — FAIL**
  - **근거[exact][L3]**: `docs/backend/fundamentals/api-design.md:82` 에 여전히 옛 값이 남아있다.
    ```
    > **출처:** [OpenAPI Specification 3.1.1](https://spec.openapis.org/oas/v3.1.1.html)
    ```
    같은 파일 80행(프로즈)과 103행(표)은 이미 "3.2.0"으로 고쳐져 있는데, **82행의 출처 인용 링크만 옛 값(3.1.1 / v3.1.1.html)** 그대로다. 반면 대응 HTML `docs/backend-kit/api-design.html:524`는 이미 `<a class="card-source" href="https://spec.openapis.org/oas/v3.2.0.html">OpenAPI Specification 3.2.0</a>` 로 고쳐져 있다 — **HTML은 고쳤는데 소스 .md의 이 인용 줄만 못 고친, 정확히 AR-01이 금지하는 패턴**이다.
  - 이것은 **같은 파일 안에서의 3번째 재발**이다: 1차(iteration 1) 디렉토리 누락 → 2차(iteration 2, 38254cc) 같은 파일 안 프로즈(80행) 누락 → 3차(이번) 같은 파일 안 인용 링크(82행) 누락.
  - 38254cc 커밋 메시지는 "이번 세션이 고친 값 15개를 `grep -rn "<구값>" <매핑된 전 소스> | wc -l == 0` 방법으로 전수 확인했고 전부 0"이라 주장하지만, 값 "3.1.1"에 대해 `grep -rn "3.1.1" docs/backend/`을 실행하면 이 82행이 매칭되므로 그 결과가 실제로는 0이 아니라 최소 2건(연구로그의 `[dated:]` 예외 1건 + 이 위반 1건)이었을 것이다. **주장된 grep이 실행되지 않았거나, 결과를 오독했다.**
  - 수정: `docs/backend/fundamentals/api-design.md:82`를 `> **출처:** [OpenAPI Specification 3.2.0](https://spec.openapis.org/oas/v3.2.0.html)` 로 고치고, 앞으로는 파일 전체를 `grep -n "<구값>" <파일>`로 훑어 발생 횟수(occurrence count)를 먼저 세고 그 수만큼 다 고쳤는지 확인하는 절차로 바꿀 것.
- [x] AR-02: 날짜 박힌 역사 기록 미수정 — PASS
  - 근거[exact][L3]: `git diff --name-only 8b4dc49~1 38254cc | grep -E '\.harness/history/|docs/superpowers/(plans|specs)/'` 0건. research-log.md 변경분(죽은 외부링크 URL 교체)에서 `[dated:]` 태그 붙은 행이 제거된 사례 0건(`git diff ... | grep -E '^-.*\[dated:'` 0건) — 날짜 태그 있는 행은 건드리지 않음 확인.
- [x] AR-03: 색을 바꿔 대비 수치를 맞추지 않음 — PASS
  - 근거[exact][L3]: color-palette.html, accessibility.html, typography-scale.html의 diff를 직접 대조 — hex 색상값(#0d0d14, #757575, #595959, #a0a0b8, #1a1a2e, #c0c0c0 등) 전부 불변, 변경된 것은 표시된 비율 숫자와 badge class(pass/fail)뿐.
- [x] AR-04: 삭제 페이지 4개는 소스 없고 미등록이며 -guide판으로 대체 — PASS
  - 근거[exact][L3]: `docs/harness/{agent,contract,qa-evaluation,skill}-design.html` 4개 파일 부재 확인, `harness/docs/guides/`에 대응 plain .md 없음(guide.md만 존재), `docs/index.html`의 동일 id들이 전부 `*-guide.html`을 가리키도록 등록되어 있음 확인.

### Diagnostics (2/2)
- [x] DG-01: 게이트 11종 전부 exit 0 — PASS
  - 근거[exact][L3]: 11개 전부 개별 실행 — contrast-claims(exit0), docs-links(exit0), validate-plugin(exit0, 13/13), api-kit-docs(exit0, 12/12), run-evals(exit0, 106/106), sync-docs --check-only(exit0), sync-orchestrator --check-only(exit0), sync-evals --check-only(exit0), a11y(exit0, 170/170), playwright(exit0, 143 passed), harness save-test(exit0, ALL TESTS PASSED).
- [x] DG-02: 워킹트리 클린, main 대비 커밋만 존재 — PASS (환경 노이즈 존재, 근거로 격리 확인)
  - 근거[structural][L3]: 평가 세션 시작 시점 `git status --porcelain` 결과 0건(클린) 확인. 평가 도중 **이 계약과 무관한 동시편집 세션**(`sprint-contract-harness-core-defects.md`, owner_session=`44c7700e-...`)이 같은 워킹트리에서 3개 파일(harness-core-defects 계약·피드백·amendments)을 능동적으로 수정하는 것을 관측했다. `git status --porcelain -- ':!.harness/sprint-contract-harness-core-defects.md' ':!.harness/sprint-feedback-harness-core-defects.md' ':!.harness/sprint-amendments-harness-core-defects.md'` 는 0건(클린). 이 3개 파일은 docs-quality-gates 스프린트의 커밋 범위(8b4dc49~1..38254cc)에 포함되지 않는 별개 계약 파일이므로 DG-02 판정 대상에서 제외한다. **다만 이 관측 자체가 harness의 공유 워킹트리 병렬 세션 리스크(parallel-sprint-safety)의 실측 재현이므로 기록해 둔다.**

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: 25/25 = 1.00 (임계 0.60 충족)
- Verdict 영향: 통상 (미검증 카운터 무관 — AR-01 실제 FAIL 1건으로 REJECT 확정)

## Discrimination
- 규칙 12(9항 카테고리) 해당 조건 없음 — 이 계약의 조건들은 정적 파서/렌더 검사 게이트이며 동시성·인증·멱등성 등 9항목에 해당하지 않음. 다만 SK-02/SK-04/SK-06/SC-06/SC-07/ER-05는 자발적으로 mutation 기반 판별력 확인을 수행했다(결과는 각 조건 근거 참조).

## Summary
- Total: 24/25 conditions passed
- Verdict: **REJECT**
- AR-01이 이번에도(3회 연속, 같은 파일 안에서만 2회 연속) 재발했다. 원인은 매번 같다 — "고친 자리"를 확인하고 "옛 값이 남았는지"는 전수 확인하지 않은 것. 이번엔 한 파일 안에 같은 사실(OpenAPI 버전)이 3곳(요약표·프로즈·출처 인용)에 흩어져 있었는데 그중 인용 링크 1곳을 또 놓쳤다.
- 수정 우선순위: (1) `docs/backend/fundamentals/api-design.md:82`의 출처 링크를 3.2.0/v3.2.0.html로 수정 (2) 수정 후 `grep -n "3\.1\.1" docs/backend/fundamentals/api-design.md`가 0건인지 재확인 (3) 이번 기회에 15개 값 전부를 파일별 occurrence count 방식(`grep -c`)으로 재확인 — 이번 조사에서 다른 14개 값은 위반을 찾지 못했으나, "첫 발생만 확인"하는 습관이 반복되고 있어 전수 count 확인을 습관화할 것.

## Improvement Suggestions
- [AR-01] 측정-방법-불충분 — "값 하나당 `grep -rn "<구값>" <파일>` 결과가 0" 이 아니라 "먼저 `grep -c "<구값>" <파일>`로 그 파일 안의 발생 횟수 N을 구하고, N개 발생 위치를 전부 Read로 열어 고쳤는지 개별 확인"으로 방법을 구체화할 것. "고친 자리만 재확인"하는 뒤집힌 검증(옛 값이 아니라 새 값의 존재만 확인)이 3회 연속 재발의 근본 원인이다.
- [SK-06] 측정-범위-편협 — 계약의 리터럴 측정("img src 이스케이프")은 4게이트가 통과하지만, check-contrast-claims.py는 "색상+비율+판정" 패턴이 이스케이프된 예제에서 오탐지한다(실측 1건). 다음 계약에서는 게이트별로 적합한 이스케이프 예제(대비 게이트는 색상+비율+판정 조합)를 명시할 것.
- [DG-02] 환경-공유리스크-실측 — 병렬 세션이 같은 워킹트리에서 무관한 계약 파일을 동시 수정하는 상황이 실제로 재현됐다(harness-core-defects 세션). DG-02 같은 "워킹트리 클린" 조건은 향후 `git status --porcelain -- <이 스프린트가 손댄 파일만>` 형태의 pathspec 한정 측정으로 계약 문구를 구체화할 것을 권장.
