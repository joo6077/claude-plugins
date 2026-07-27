# Sprint Contract — Kaizen Phase 8 (infra-kit)

- 날짜: 2026-07-27
- 브랜치: kaizen/2026-07-27
- 범위: `infra-kit/**`, `docs/infra/research-log.md`, `.claude/skills/infra-kaizen/SKILL.md`
- 판정 모드: 병렬 Phase 실행 — git add/commit/tag 금지, 오케스트레이터가 직렬 커밋

## 배경

Step 0.6 선별에서 infra-kit 은 LOW signal 로 분류됐다. 억지 변경 금지가 기본 방침이나, 아래 두
축은 실측 근거가 있어 NO_CHANGE 로 넘길 수 없다고 판단했다.

1. **Phase 1/3/4 정합화 부채** — Phase 3 이 `infra-reviewer` 를 canonical drift 대상으로 실명
   지목했다("2 건 + CONDITIONAL APPROVE"). 정합화는 선택이 아니라 지시다.
2. **exit-code 캡처 3 회 반복** — digest 의 `broken-pipeline-exit-capture` /
   `unreliable-piped-exit-code-capture` / `unreliable-exit-status-capture` 3 종. 조사 결과
   infra-test 가 사용자에게 **생성해 주는 샘플 검증 스크립트 자체에 동일 결함 3 건**이 있음을
   실행으로 확인했다. 스킬이 결함을 재생산하고 있으므로 문서 개선이 아니라 버그 수정이다.

## 리서치 소스 (Phase 8 템플릿 6 종 전수 + 신호 C/B 근거 2 종)

Context7 는 OAuth 미인증으로 사용 불가 — 전부 WebFetch 직접 조회.

1. <https://kubernetes.io/docs/concepts/security/pod-security-admission/> — PSA `v1.25 [stable]`,
   라벨 `pod-security.kubernetes.io/<MODE>: <LEVEL>` (MODE=enforce|audit|warn,
   LEVEL=privileged|baseline|restricted), `-version` 라벨은 선택. **현행 기준과 일치 → 변경 불필요.**
2. <https://developer.hashicorp.com/terraform/language/ephemeral> — ephemeral 블록 / write-only
   인수 / `ephemeral = true` 변수. state·plan 양쪽에서 완전 누락 보장, `locals` 참조 시 재귀 적용.
   문서 최신 표기 v1.15.x. **현행 기준과 일치 → 변경 불필요.**
3. <https://opentofu.org/docs/v1.11/language/state/encryption/> — key provider 6 종(PBKDF2/AWS
   KMS/GCP KMS/Azure Vault/OpenBao/External(experimental)), method 는 AES-GCM 만 프로덕션.
   PBKDF2 기본 600,000 iteration(최소 200,000). **현행 기준과 일치 → 변경 불필요.**
4. <https://slsa.dev/provenance> — 현재 스펙 v1.2 Approved. build provenance / source provenance
   2 종 분리. **현행 기준과 일치 → 변경 불필요.**
5. <https://docs.sigstore.dev/cosign/verifying/attestation/> — `cosign verify-attestation`,
   CUE/Rego `--policy`. 검증은 predicate 부분만 대상. **v3 전용 플래그(`--bundle` 등)는 이 페이지에
   기재 없음 → audit-criteria 의 Cosign v3 서술을 강화하지 않는다(추측 금지).**
6. <https://opentelemetry.io/docs/specs/status/> — traces API/SDK/protocol Stable, logs
   bridge API·SDK·protocol Stable, metrics API/protocol Stable·SDK Mixed, profiles protocol
   Development. **"3 신호 stable" 서술 유지 가능 → 변경 불필요.**
7. <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax> — 비-Windows
   기본 셸은 `bash -e {0}` (**pipefail 없음**), `shell: bash` 명시 시에만
   `bash --noprofile --norc -eo pipefail {0}`. → 신호 C 의 1 차 원인 근거.
8. <https://docs.docker.com/build/building/best-practices/> — RUN 파이프는 마지막 명령의 exit code
   만 평가하므로 `set -o pipefail &&` 선행 필요. digest 핀닝은
   `FROM alpine:3.21@sha256:...` 형태를 권장하되 **수동 유지보수·자동 보안패치 포기라는 트레이드오프를
   명시** → audit-criteria 의 "고정 태그 **또는** digest" 현행 표현이 문서와 정합 → 변경 불필요.

## 실행 증거 — infra-test Step 5 샘플 스크립트 결함 3 건

`infra-test/SKILL.md` Step 5 가 사용자 프로젝트에 생성하도록 제시하는 `tests/ci-validation.sh`
원문을 그대로 재현해 실행했다.

- E1. **third-party SHA 핀닝 검사 false negative** — `grep -v "actions/"` 가 first-party 뿐 아니라
  `aws-actions/*`, `google-github-actions/*` 까지 제외한다. 미핀닝 3 건 중 1 건만 검출:
  입력 `actions/checkout@v4` · `aws-actions/configure-aws-credentials@v4` ·
  `google-github-actions/auth@v2` · `docker/build-push-action@v6` → 출력은
  `docker/build-push-action@v6` 한 줄뿐.
- E2. **exit code 미전파** — WARN 을 출력하고도 스크립트 최종 exit 은 0 (`SCRIPT_EXIT=0` 실측).
  마지막 명령이 `echo` 라 실패가 CI 게이트로 전달되지 않는다. "검증 스크립트" 를 자칭하면서
  실제로는 항상 통과한다.
- E3. **unmatched glob false FAIL** — `for f in .github/workflows/*.yml` 에 매칭 파일이 없으면
  루프가 리터럴 패턴 1 회로 돌아 `python3 ... open('.github/workflows/*.yml')` 이 던지고
  `exit 1`. 워크플로가 없는 프로젝트에서 "YAML syntax error" 를 오보한다 (실측: 루프가
  `checking ./wfempty/*.yml` 1 회 실행).
- 반증 확인: `set -e` 가 `A && { ... }` 형태에서 A 실패 시 스크립트를 종료시킨다는 가설은 **거짓**
  으로 확인됨 (`EXIT=0`). 해당 가설에 근거한 수정은 하지 않는다.

## GAP 표

| # | GAP | 근거 | 대상 | Enforcement 판정 |
|---|-----|------|------|------------------|
| G1 | `infra-reviewer` §9 가 canonical 5 조항과 불일치 — 마커 동의어 금지·3 분기(FAIL/도구부재/증거무효)·생성자 주장 배제·집계 의무가 전부 부재 | Phase 3 `qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol (drift 실명 지목) | `agents/infra-reviewer.md` | 정본 복제 (등급 재정의 금지, §3.7 SSOT 준수) |
| G2 | 감사 도구 부재(hadolint/actionlint/kubeconform/cosign 미설치) 또는 `audit-criteria.md` 로드 실패를 "위반 0" 으로 집계하는 것을 막는 규칙 없음 | Phase 4 `refactor-checklist` 원칙 + canonical 조항 2·5 + insights Friction #2 | `skills/infra-audit/SKILL.md` | E2 — 리포트 머리말 아티팩트(로드/미검증 소스 파일명 나열) |
| G3 | infra-test 샘플 스크립트 결함 3 건 (E1/E2/E3 위 실행 증거) | digest 3 회 반복 + 실행 재현 | `skills/infra-test/SKILL.md` | 버그 수정 + E2 Gotcha |
| G4 | pipefail 부재 규칙 없음 — GH Actions 기본 셸에 pipefail 미포함, Dockerfile RUN 파이프도 마지막 exit code 만 평가 | 신규 리서치 7·8 | `skills/infra-test`, `skills/infra-init`, `references/audit-criteria.md` | E1 (infra-kit 최초 도입) |
| G5 | infra-kaizen 이 validate-plugin 을 "7 카테고리" 로 표기 (3 곳) — 실측은 V1~V8 8 개 | Phase 4 전달 + `validate-plugin.py infra-kit` 실행 출력 | `.claude/skills/infra-kaizen/SKILL.md` | 사실 정정 |
| G6 | infra-kaizen Gotcha 4 의 scope-creep 이 "스킬 개수" 기준 | Phase 4: unit(관심사) 기준 | 동상 | 문구 정정 |
| G7 | infra-kaizen Gotcha 8 의 Phase 감사 목록에 Phase 1 v1.4.0 §3.7 / E1~E3 / §5.5 미포함 | Phase 1 결과 | 동상 | 목록 갱신 |
| G8 | infra-test Step 7/8 이 실행 증거(명령+출력) 없이 완료 보고 허용 | Phase 1 §3.7 5 조항 | `skills/infra-test/SKILL.md` | E1 |

### 변경하지 않기로 한 것 (억지 변경 방지 기록)

- 이미지 digest 강제 승급 — Docker 공식 문서가 트레이드오프를 명시하므로 "고정 태그 또는 digest"
  현행 표현이 옳다.
- Cosign v3 전용 플래그 서술 강화 — 조회한 공식 페이지에 근거 없음.
- PSA / ephemeral / OpenTofu encryption / SLSA / OTel 기준 문구 — 조회 결과 전부 현행과 일치.
- `port-already-in-use`, `wrong-infra-path-assumption` — 단발 태그이고 infra-kit 산출물과
  인과가 연결되지 않아 이번 사이클 미반영.
- `distroless-builder-glibc-mismatch` — 실재하는 결함 클래스이나 이번 사이클에 1 차 출처를
  확보하지 못했다. 추측 서술 금지 원칙에 따라 미반영, 다음 사이클 후보로 research-log 에 기록.
- Counterpart Conditions 의 evaluator 측 대응 절 — 의도된 부재 (parity item 12). 만들지 않는다.

## 완료 조건

| ID | 카테고리 | 조건 | 검증 방법 |
|----|----------|------|-----------|
| C-01 | 정합성 | `infra-reviewer.md` 가 canonical 5 조항을 **문구 변형 없이** 포함하고, 자체 임계값·마커 재정의가 0 건이다 | `qa-evaluation-guide.md` 418~448 행과 diff 대조 |
| C-02 | 정합성 | `infra-reviewer.md` 의 CONDITIONAL APPROVE 는 "`[미검증]` 1 건 + FAIL 0" 에만 유효하다고 명시된다 | Grep |
| C-03 | 정합성 | evaluator 측 Counterpart Conditions 대응 절을 **새로 만들지 않았다** | Grep `Counterpart` = 0 건 |
| C-04 | 정확성 | infra-audit 에 "도구 미설치·규칙 소스 로드 실패 → 위반 0 집계 금지 + `[미검증]` 표기 + 머리말에 로드/미검증 소스 파일명 나열" 규칙이 존재한다 | Grep + Step 3 머리말 포맷 확인 |
| C-05 | 정확성 | infra-test Step 5 샘플 스크립트에서 E1/E2/E3 3 결함이 모두 제거되고, 수정본이 실제로 의도대로 동작한다 | 수정본을 fixture 로 실행하여 미핀닝 3 건 검출 + 비영 exit + 빈 glob 무오보 확인 |
| C-06 | 정확성 | pipefail 규칙이 infra-test Gotcha · infra-init Gotcha · audit-criteria CI/CD rule 3 면에 출처 URL 과 함께 존재한다 | 3 파일 Grep |
| C-07 | 정확성 | `.claude/skills/infra-kaizen/SKILL.md` 에 "7 카테고리" 표기가 0 건이고 V1~V8 로 정정됐다 | `grep -c "7 카테고리"` = 0 |
| C-08 | 회귀 방지 | `python3 scripts/validate-plugin.py infra-kit` 이 V1~V8 전부 OK, Exit 0 | 명령 실행 출력 인용 |
| C-09 | 회귀 방지 | 범위 밖 파일(다른 kit, `harness/`, marketplace.json, plugin.json, `docs/kaizen/changelog.md`) 변경 0 건 | `git status --short` 읽기 전용 확인 |
| C-10 | 문서 | `docs/infra/research-log.md` 에 `## [2026-07-27] - Phase 8 kaizen` 엔트리 + URL 5 건 이상 | Grep |

## 비범위

- git add/commit/tag/push/finalize (오케스트레이터 담당)
- `plugin.json` / `marketplace.json` 버전 bump
- 다른 kit 및 `harness/` 하위 전체
- `scripts/validate-plugin.py` (아래 V5 블로커의 실제 수정 위치이나 범위 밖)

## Self-Audit 결과 (2026-07-27)

| ID | 판정 | 증거 |
|----|------|------|
| C-01 | PASS | 정본 `qa-evaluation-guide.md:431-446` 과 `infra-reviewer.md` 복제본 `diff -u` → 차이 0 (16 lines byte-identical) |
| C-02 | PASS | `infra-reviewer.md:73` "1 건 + FAIL 0" · `infra-audit/SKILL.md:89` "정확히 1 건" |
| C-03 | PASS | `grep -rc "Counterpart" infra-kit/` → 0 건 (신설 없음) |
| C-04 | PASS | `infra-audit/SKILL.md:27` Gotcha 12 + Step 3a 머리말 4 줄(`:50`, `:52`) |
| C-05 | PASS | SKILL.md 에서 스크립트를 추출해 3 fixture 재실행 — bad `exit=1` (미핀닝 3/3 검출) · good `exit=0` · empty `SKIP exit=0`. `bash -n` 구문 OK |
| C-06 | PASS | `pipefail` 이 infra-test · infra-init · audit-criteria 3 파일 모두에 출처 URL 과 함께 존재 |
| C-07 | PASS | `grep -c "7 카테고리"` → 0 |
| C-08 | **FAIL** | `validate-plugin.py infra-kit` → V1·V3·V4·V6·V7·V8 OK, V2 SKIP, **V5 FAIL 1 건**, Exit 2. 상세는 아래 |
| C-09 | PASS | 변경 파일 7 개 + 신규 1 개 전부 범위 내. `infra-kit/skills/infra-guide/SKILL.md` 는 무변경(억지 변경 없음). 다른 kit 의 modified 는 병렬 Phase 5/6/7/9 산출물 |
| C-10 | PASS | `## [2026-07-27] - Phase 8 kaizen` 1 건 + 고유 URL 8 건 |

### C-08 상세 — V5 는 Phase 8 단독 결함이 아니라 **cross-phase 블로커**다

```text
V5 placeholders    1 found
  FAIL infra-kit/agents/infra-reviewer.md:66 — 1. **마커는 `[미검증]` 하나로 통일한다.**
       동의어(미확인, N/A, TBD, unverified) 를 만들지 않는다.
```

원인: `scripts/validate-plugin.py:49` 의 `PLACEHOLDER_PATTERN = re.compile(r'\b(TODO|TBD|FIXME)\b')`
이 **canonical 조항 1 이 "쓰지 마라" 고 열거한 금지 동의어 목록 안의 `TBD`** 를 미완성
placeholder 로 오탐한다. Phase 3 이 "문구 변형 없이 복제" 를 지시했으므로 이 토큰은 제거할 수 없다.

동일 사이클 실측 — **canonical 을 복제한 4 개 서피스가 전부 같은 이유로 red**:

| 서피스 | V5 |
| ------ | -- |
| `infra-kit/agents/infra-reviewer.md` (Phase 8) | 1 found |
| `design-kit/agents/design-reviewer.md` (Phase 6) | 1 found |
| `rust-kit/agents/rust-reviewer.md` (Phase 9) | 1 found |
| `flutter-toolkit/skills/flutter-audit/SKILL.md` (Phase 5) | 2 found |

**Phase 8 의 판단:** 로컬에서 문구를 바꿔 green 을 만드는 것은 4 개 서피스 사이에 새 drift 를
만드는 것이고, Phase 3 이 없애려던 바로 그 문제다. 따라서 canonical 을 byte-identical 로 유지하고
V5 를 미해소 상태로 보고한다.

**⚠ 즉시 위험 — `--fix` 가 SSOT 를 손상시킨다:** `validate-plugin.py:42` 의
`FIX_PLACEHOLDER_RULES` 는 `TBD` → `<내용 추가>` 로 치환한다. 누가 `--fix` 를 돌리면 4 개 서피스의
canonical 조항 1 이 조용히 변조된다. 커밋 전에 `--fix` 를 돌리지 마라.

**권장 수정 (오케스트레이터 · Phase 4 harness 소관, 2 파일):**

1. `scripts/validate-plugin.py` — 인라인 코드(백틱) 안의 토큰은 placeholder 로 세지 않는다.
   인용된 예시와 실제 미완성 표시를 구분하는 일반 규칙이며 `--fix` 도 안전해진다.
2. `harness/docs/guides/qa-evaluation-guide.md` §Canonical 조항 1 — 동의어를 인라인 코드로 표기:
   ``동의어(`미확인`, `N/A`, `TBD`, `unverified`) 를 만들지 않는다.`` 후 4 개 서피스 재복제.

둘 중 1 번만 해도 red 는 사라지지만, 2 번까지 해야 "인용은 백틱" 규약이 명시적으로 고정된다.
