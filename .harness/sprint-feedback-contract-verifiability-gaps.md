# Sprint Feedback
Feature: 계약 지침의 검증 가능성 구멍 6건 메우기
Evaluated: 2026-09-23 10:05
Verdict: APPROVE
Iteration: 1

## Contract Fingerprint
- path: /Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-contract-verifiability-gaps.md
- sha256: 13fe5106cbccba6028ebc28235e5d3960843b496a836381a7184f7e773217b3d
- status: active
- slug: contract-verifiability-gaps
- contract_root: /Users/jackson/Hub/10_Dev/claude-plugins
- contract_root_unconfigured: false
- 선택 근거: ladder 2 세션소유 (owner_session == 호출 세션 f5b7f3a5-c03d-452b-b44b-fc3d15dcd1a0, 후보 1개 유일)
- legacy_contract_used: false
- seal_status: SEAL_OK (conditions_digest sha256:4d9e2acca41395be == 실측)
- contract_seal_broken: n/a
- 재확인(Step 5): 일치 (sha256/status 저장 직전 재확인 OK)
- status_transition: active -> done (APPROVE 확정 후 전환)

## Amendments
- amendments: 0 (사이드카 `.harness/sprint-amendments-contract-verifiability-gaps.md` 부재 확인)
- PASS 근거 가능: 0
- PASS 근거 불가: 0
- 집합형 direction 계산 결과: n/a (개정 없음)

## User Correction Audit
- correction_log_status: available (`~/.claude/logs/claude-plugins/2026-09.md`, 61648줄)
- unreflected_corrections: 0
  - 세션 f5b7f3a5 자신이 보낸 프롬프트는 스프린트 구간(생성 09:10~평가 시점) 중 1건뿐:
    2026-09-23T09:28:44 "ㄱㄱ" — 진행 승인 발화이며 교정 성격 아님
  - grep 으로 세션 ID가 잡힌 나머지 다건은 전부 **다른 세션**이 우리 세션 로그를 분석 대상
    transcript 본문으로 인용한 것이라 "우리 세션이 보낸 프롬프트"가 아님 (session: 필드로
    재확인해 배제)
- verdict 영향: 없음 (표면화 전용 · 미검증 카운터 비합산)

## Cross-Diagnosis Handoff

- 상태: pending-parent
- 부모가 띄울 때 넘길 것: 계약 절대경로
  `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/sprint-contract-contract-verifiability-gaps.md`
  · 이 리포트 전문(verdict + 조건별 PASS/근거 + 아래 "구멍이 실제로 막혔는가" 절)
- 부모가 물을 두 가지:
  1. 계약 조건의 원래 의도와 다르게 해석해 PASS/FAIL 을 오판한 조건이 있는가?
  2. 0건·빈 출력을 근거로 PASS 한 조건 중, 문제가 있어도 0을 냈을 측정(공허한 통과)이 있는가?
     — 특히 DG-02(마크다운 경고 카운트)가 아래에 보고한 "contract-schema.md 표 붕괴"를
     놓친 것이 그런 사례인지 판단 요청
- 교차 진단 완료 후 `cross_diagnosis_by` 를 `sprint-contract` 로 갱신, 끝내 못 띄우면 `none`

## Results

### Skill (3/3)
- [x] SK-01: 동의 근거 출처 목록에 세션 기록의 `AskUserQuestion` 쌍이 두 파일 모두 추가됐다 — PASS
  - 근거(L3): `harness/references/contract-schema.md:975` · `harness/docs/guides/qa-evaluation-guide.md:435`
    양쪽 다 "세션 기록의 `AskUserQuestion` 쌍" 행이 출처 표에 추가됨.
    측정값: contract-schema.md `AskUserQuestion` 5건, qa-evaluation-guide.md 4건 (기준: 각 >=1). 양성 대조(작성 시점 0건) 대비 활성화 확인.
- [x] SK-02: 그 추가가 요구 값 세 개(시각·세션·작업폴더)를 늘리지 않았다 — PASS
  - 근거(L3): 두 파일 모두 `grep -Fc '사용자 발언 인용 + **reflect-kit prompt 로그 앵커**(timestamp · session · cwd)'` = 1
    (contract-schema.md:975, qa-evaluation-guide.md:426). 원문 리터럴 그대로 보존, 새 출처는
    별도 표(`harness/references/contract-schema.md:975-978`)로 추가되어 기존 요구 값을 대체하지 않음.
- [x] SK-03: 봉인 범위 서술 2 파일에 정확한 문장이 들어갔다 — PASS
  - 근거(L3): `grep -Fc '조건 줄이 가리키는 산문을 고치면 개정 파일에 남긴다'` = 1
    (contract-schema.md:260, sprint-contract/SKILL.md:704). SKILL.md 쪽은 "봉인 이후 조건 본문을
    편집하지 마라" 절(작성자용 write-once 지시)에 자연스럽게 통합돼 있어 문맥상으로도 유효함
    (SKILL.md:697-711 확인).

### Script (2/2)
- [x] SC-01: "고친 근거는 구현자가 쓰지 않은 기록에서 확인돼야 한다" 요건이 들어갔다 — PASS
  - 근거(L3): `grep -c '구현자가 쓰지 않은' harness/references/contract-schema.md` = 1
    (line 1021, "#### REJECT 를 받고 개정을 고쳐 판정을 뒤집을 때" 절). 내용은
    "세션 기록·git 기록·도구 출력에서 다시 뽑은 값=가능 / 개정 문서에 새로 쓴 설명=불가"
    표(1024-1027)로 구체화돼 있어 평가자가 그대로 따를 수 있는 절차임.
    사용자 요청 ③ 확인: 이 요건은 이번 평가에서 내가 수행한 "고친 근거를 구현자가 쓰지 않은
    git/markdownlint 실측으로 직접 재확인" 절차와 정합적이다.
- [x] SC-02: `python3 scripts/validate-plugin.py` 전체가 `14 plugins, 14 OK` · `Exit: 0` — PASS
  - 근거(L3, 직접 실행): 명령 마지막 두 줄 `Total: 14 plugins, 14 OK` / `Exit: 0` 확인.
    음성 대조는 별도로 AP-04 항목에서 SKILL.md의 `name:` 을 지우고 재실행해 확인(아래 AP-04).

### Error (2/2)
- [x] ER-01: 0 기대값인 조건 절에 "대상 파일을 열거하라"는 요구가 들어갔다 — PASS
  - 근거(L3): `grep -c '대상 파일을 열거' harness/docs/guides/contract-design-guide.md` = 2.
    `awk` 범위 확인 결과 두 매치 모두 `### 0 이 기대값인 조건 — 양성 대조 없이 잠그지 마라`
    (749행) ~ `### 예외 조항 포맷` (1001행 직전) 구간 안, 정확히는 `#### 대상 파일을 열거하라 —
    개수만 적으면 집합이 재현되지 않는다` 소제목(759행) 아래.
- [x] ER-02: "취지가 서술 부재라면 낱말 하나로 재지 마라" 정확한 문장이 들어갔다 — PASS
  - 근거(L3): `grep -Fc '취지가 서술 부재라면 낱말 하나로 재지 마라' harness/docs/guides/contract-design-guide.md` = 1
    (line 771 소제목 아래 773행). 서술은 구체적 실측 사례 2건(779-782행)을 직접 인용해 재발 방지
    의도가 뚜렷함.

### Architecture (3/3)
- [x] AR-01: 이 스프린트의 변경 파일이 4개 경로와 정확히 일치한다 — PASS
  - 근거(L3, 직접 실행): STALE_HEAD 확인 선행 — `sprint_head validate-check-count-sync` =
    `ac77cdce10a5b4b70978b052bc559ca6020cb79b` != `a9c9a0a` → not stale.
    `git diff --name-only a9c9a0a..ac77cdc -- . ':(exclude).harness/**'` 결과 정확히 4행:
    `harness/docs/guides/contract-design-guide.md`, `harness/docs/guides/qa-evaluation-guide.md`,
    `harness/references/contract-schema.md`, `harness/skills/sprint-contract/SKILL.md`.
- [x] AR-02: `.harness/` 범위 조건 권장 형태 문장 + "status 전환" 언급이 들어갔다 — PASS
  - 근거(L3): `grep -Fc 'sprint-contract*.md 에 verify_seal 을 돌려 SEAL_BROKEN 이 0 개' harness/references/contract-schema.md` = 1
    (line 565, `##### .harness/ 범위 조건 — 산출물 슬러그를 열거하지 마라` 절, 553-575행).
    `grep -c 'status 전환'` = 3. 사용자 요청 ② 확인: 판정 기준은 `SEAL_OK` 가 아니라
    `SEAL_BROKEN` 0개(line 574 "`SEAL_OK` 와 `SEAL_ABSENT` 는 **둘 다 통과**다")로 명시돼 있어
    봉인 없는 레거시 계약을 정상적으로 통과시킨다.
- [x] AR-03: 손대지 않기로 한 것이 변경되지 않았다 — PASS
  - 근거(L3, 직접 실행): STALE_HEAD 확인 통과(AR-01과 동일).
    (i) `git diff --name-only a9c9a0a..ac77cdc -- harness/evals/` = 0행
    (ii) `-- docs/kaizen/` = 0행
    (iii) `-- harness/agents/` = 0행
    (iv) `.harness/sprint-contract*.md` 67개에 `verify_seal` 실행 결과 SEAL_OK 58 · SEAL_ABSENT 9 ·
    **SEAL_BROKEN 0**. 개수는 계약 작성 시점(56/11/0)과 다르지만 계약 자신이 "산출물 추가로
    시점마다 달라지므로 총수를 고정하지 않는다"고 명시했으므로 정상.

### Anti-patterns (2/2)
- [x] AP-03: bare code fence 0건 — PASS
  - 근거(L3, 직접 실행): `python3 scripts/validate-plugin.py --check=code-fence` → 전 킷 OK
    (harness 포함 14/14). 양성 대조: 대상 2파일의 ` ``` ` 개수 실측 — SKILL.md 36건,
    contract-schema.md 72건 (기준 >=1 충족, 측정 살아있음 확인).
- [x] AP-04: 대상 파일 frontmatter 보존 — V1 FAIL 0건 — PASS
  - 근거(L3, 직접 실행 + 양성 대조): `--check=frontmatter` → 전 킷 OK (14/14).
    안전 3조건 확인 후 실행형 음성 대조 수행: `harness/skills/sprint-contract/SKILL.md`
    (git status clean, AR-01 diff 범위 내)에서 `name:` 행 삭제 → 재실행 결과
    `Total: 14 plugins, 13 OK, 1 ERROR` / `Exit: 2` (계약이 명시한 기대값과 정확히 일치).
    직후 원본 복원, `git diff --exit-code -- harness/skills/sprint-contract/SKILL.md` 로
    원상 복구 확인(diff 없음).

### Reusability (0/0, N/A 2)
- [ ] RE-01: N/A — 사유 실측 확인: AR-01의 변경 4파일 전부 `.md`, 실행 코드 0개. 사유 참(TRUE).
- [ ] RE-02: N/A — 같은 사유, 참(TRUE).

### Diagnostics (1/1, N/A 3)
- [ ] DG-01: N/A — `commands.analyze`(`bash -n scripts/release.sh`)의 대상과 AR-01의 4개 변경
      파일 교집합: `grep -c '^scripts/release.sh$'` on 4행 리스트 = 0. 사유 참(TRUE).
- [x] DG-02: 편집기와 같은 조건 마크다운 경고가 기준값을 넘지 않는다 — PASS
  - 근거(L3, 직접 실행): scratchpad에 `markdownlint-cli2@0.23.2` 설치, `{"config":{"MD013":false}}`
    설정으로 4개 대상 파일(계약이 열거한 그대로) 실행.
    측정값: 총 41건 (기준 <=41) · (파일,규칙) 조합 11개, 계약이 봉인 전 실측한 기준(41건·11조합)과
    **정확히 일치** — 늘어난 조합 0개.
- [ ] DG-03: N/A — DG-01과 동일 근거(`commands.test` 대상도 `scripts/release.sh` 하나). 사유 참(TRUE).
- [ ] DG-04: N/A — AR-01 4개 파일 전부 `.md`, 실행 진입점 0개. 사유 참(TRUE). "이 자리에 실제로
      성립하는 검사는 SC-02" — SC-02 PASS 이미 확인.

## Unverifiable Summary
- invalid_evidence: 0
- env_gaps: 0
- verified_coverage: (18 - 0) / 18 = 1.00 (임계 0.60)
- 연속 ENV 승급: 없음
- Verdict 영향: 통상 (자동 REJECT/BLOCKED 미해당)

## Discrimination (규칙 12 적용 조건만)
- 적용 조건: 없음 (동시성/인증/멱등성/입력검증/데이터유실/마이그레이션/재시도/보안경계/
  사용자보고-테스트충돌 9항 중 해당하는 조건이 이 스프린트에 없음 — 문서 전용 스프린트)

## User-Reported Failures
- 해당 없음 (이번 평가에 사용자 실패 보고 없음)

## Evidence Validity
- 검사 대상 증거: 18건 (조건별 1건 이상, PASS 13 + N/A 5)
- 무효 판정: 0건
- 셸 스니펫 실행 검증: 계약 내 셸 스니펫(sprint_head, verify_seal, markdownlint 호출, diff 명령)
  전부 이 세션(zsh 사용자 셸 하위의 Bash 도구)에서 직접 실행해 출력을 확인함.
  Bash 도구가 bash 로 스크립트를 해석하므로 bash 실행은 확인됐고, `find`/`grep` 기반이라
  zsh nomatch 문제가 될 glob 패턴은 계약 스니펫에 없음(대상 4파일이 절대경로로 명시됨).
- 양성 대조: SK-01/SK-02/SK-03/SC-01/AR-02/ER-01/ER-02 — 출처: 계약의 "봉인 전 실측한 기준값" 표
  (전부 0건 기준, 이번 측정에서 1건 이상으로 전환 확인). DG-02 — 출처: 계약의 "41건·11조합"
  기준값, 이번 측정과 정확히 일치. AP-04 — 출처: 실행형 음성 대조(계약이 직접 지정한 방법),
  `name:` 삭제 시 13 OK/1 ERROR/Exit 2 재현.
- 무효 0건, 미검증 카운터 변화 없음(누계 0)

## Summary
- Total: 13/13 evaluable conditions passed (N/A 5건은 사유 실측 참으로 확인, TOTAL에서 제외)
- Verdict: **APPROVE**

## 구멍이 실제로 막혔는가 — 문구 통과와 별개로 확인한 것

1. **동의 근거 출처 요구 값이 늘지 않았는가** — 늘지 않았다. `timestamp · session · cwd` 세 값은
   두 파일 모두 원문 그대로이고, `AskUserQuestion` 출처는 별도 표·별도 문단으로 추가됐다. 기존
   개정(A-01 등)이 이 변경으로 소급 무효가 되지 않는다.
2. **`.harness/` 범위 조건 권장 형태가 SEAL_BROKEN 0개 기준이고 레거시 계약을 통과시키는가** —
   그렇다. `SEAL_OK` 와 `SEAL_ABSENT` 를 둘 다 통과로 명시했고, 실측(이번 평가)에서도
   봉인 없는 레거시 계약 9개가 `SEAL_ABSENT` 로 정상 집계돼 통과 집합에 들어갔다.
3. **"고친 근거는 구현자가 쓰지 않은 기록에서" 요건이 평가자 자신의 재평가 절차에 적용 가능한가** —
   가능하다. 이번 평가에서 SC-01/SC-02/DG-02/AP-04 전부 "구현자의 서술"이 아니라 git 로그·
   markdownlint 출력·validate-plugin 출력을 직접 재실행해 확인했고, 이는 새로 추가된 SC-01 절이
   요구하는 바로 그 절차다.

**그런데 조건으로 잡히지 않은 부수 결함을 하나 발견했다 — Improvement 참조.**
`harness/references/contract-schema.md` 의 `direction × consent` 2축 조합표(원래
narrowing/relaxing/unknown 3행)가 이번 삽입으로 **끊어졌다.** 1013-1016행에 header+narrowing+
relaxing 행만 남고, 원래 그 표의 마지막 행이었던 `unknown` 행이 1036행에서 헤더 없이
홀로 떠 있다(1017~1035행 사이에 새 소제목 "#### REJECT 를 받고 개정을 고쳐 판정을 뒤집을 때"와
그 안의 별도 표가 끼어들었다). `git diff` 로 확인한 결과 이 파일의 변경은 전부 **순수 삽입**
(167줄 추가, 삭제 0)인데, 그 삽입 위치가 기존 표의 두 데이터 행 사이였다.

실측 대조: 같은 표가 `harness/docs/guides/qa-evaluation-guide.md`(469-473행)에는 온전하게
들어갔다(narrowing·relaxing·unknown 3행이 끊기지 않고 연속) — 그 파일은 새 절을 표
**앞**(소제목 "**2 축 조합표**" 앞)에 넣었기 때문이다. 즉 같은 내용을 두 파일에 반영하면서
한쪽만 삽입 위치를 잘못 골라 표를 깨뜨렸다 — "같은 표가 두 파일에 복제돼 있으므로 양쪽을 함께
고친다"는 이 계약 자신의 설계 결정(범위 경계 절)이 절반만 지켜진 셈이다.

영향 범위는 제한적이다 — `unknown → PASS 근거 불가` 매핑은 같은 파일 905행(direction 단독 표)
에 온전히 남아 있어 정보 자체가 사라지지는 않았다. 그리고 DG-02(markdownlint)는 이 결함을
잡지 못했다 — 헤더 없는 고립 파이프 행은 GFM 테이블로 인식되지 않아 애초에 어떤 마크다운
경고 규칙에도 걸리지 않는다. 18개 조건 중 이 결함을 잡을 조건은 없었다(계약 결함이 아니라
"조건이 다루지 않는 영역"). 그래서 FAIL로 처리하지 않았지만, 이 계약이 막으려던 바로 그 문제
유형(구멍 5: "취지를 글자 하나로 재는 조건이 통과한다" — 여기서는 "글자 하나"가 아니라 "도구가
아예 못 보는 구조적 결함")과 같은 뿌리라서 Improvement로 강하게 남긴다.

## Improvement Suggestions
- [contract-schema.md 표 구조] 측정-산출물-부재 — `harness/references/contract-schema.md:1013-1036`
  의 `direction × consent` 2축 표가 새 소제목 삽입으로 끊어졌다(narrowing/relaxing 행과
  unknown 행이 분리, unknown 행은 헤더 없이 고립). 즉시 수정 권장: `unknown` 행을 1016행
  바로 아래로 옮기거나, 새 소제목("#### REJECT 를 받고...")을 표 전체 뒤로 재배치한다
  (qa-evaluation-guide.md의 배치 방식을 그대로 따르면 된다). 재발 방지책으로 "표 중간에 새
  섹션을 삽입하지 않는다"는 규칙을 계약 작성 가이드의 편집 체크리스트에 추가하는 것을 권한다.
- [DG-02류 조건 일반] 검증경로-미기재 — 헤더 없는 고립 표 행처럼 markdownlint 가 구조적으로
  인식하지 못하는 마크다운 결함 유형은 이번 DG-02 측정 범위 밖이다. 향후 문서 전용 스프린트의
  Diagnostics 조건에 "표 행 수 보존" 류의 구조 검사(예: 표마다 헤더/데이터 행 수를 커밋 전후로
  비교)를 추가하면 이런 결함을 계약 조건으로 잡을 수 있다.

## 자기진단 (Step 6)
- l3_unreached: false (18개 조건 전부 L3 도달 — 코드/문서 경로 추적 + 실행 검증)
- bias_detected: false (구현 추종 편향 방지 위해 표 붕괴 등 계약 밖 결함도 별도 발견해 보고)
- evidence_missing: false (모든 PASS/N/A에 파일:라인 또는 직접 실행 출력 근거 있음)
- contract_misinterpret: false (Step 1.2 파싱 범위 확인 — 조건 18개, frontmatter 선언 18개 일치)
- perspective_gap: false (구현자 관점 + 평가자 관점 + "지침이 실제로 문제를 막는가"라는 사용자
  요청 관점까지 3개 관점에서 점검)

## 피드백 저장 메모
- 스크립트 경로 ladder: (1) 설치 플러그인 경로에서 발견 —
  `/Users/jackson/.claude/plugins/cache/joo6077-plugins/harness/0.10.0/scripts/save-feedback.sh`
- draft 의 `project_name`/`project_hash` 는 의도적으로 placeholder 로 제출 —
  스크립트가 CONTRACT_ROOT 기준으로 재계산해 `claude-plugins` / `1a3bcba6` 으로 덮어씀
  (stderr 경고 그대로 인용, 삼키지 않음). 원본 placeholder 는 `draft_project_name`/
  `draft_project_hash` 로 보존됨 — identity 불일치가 아니라 의도된 재계산 경로.
- 저장 경로: `/Users/jackson/.harness/feedback/evaluator/1a3bcba6-2026-09-23T100002-f5b7f3a5-8625.yaml`
- verify-feedback.sh 결과: PASS (Exit 0)
