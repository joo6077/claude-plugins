# 디자인 감사 리포트

> 일시: {{date}}
> 대상: {{target-path}}
> 모드: {{quick|deep}}
> 판정: **{{APPROVE|REJECT|BLOCKED}}**
> 보류 사유: {{BLOCKED 일 때만 `insufficient_verified_coverage` — 재검증 명령을 돌린 뒤 재감사}}

## 요약

| 카테고리 | 판정 | Critical | Major | Minor | 미검증 |
|----------|------|----------|-------|-------|--------|
| Typography | {{PASS/FAIL}} | {{n}} | {{n}} | {{n}} | {{n}} |
| Color | {{PASS/FAIL}} | {{n}} | {{n}} | {{n}} | {{n}} |
| Spacing | {{PASS/FAIL}} | {{n}} | {{n}} | {{n}} | {{n}} |
| Accessibility | {{PASS/FAIL}} | {{n}} | {{n}} | {{n}} | {{n}} |
| Interaction | {{PASS/FAIL}} | {{n}} | {{n}} | {{n}} | {{n}} |
| Motion | {{PASS/FAIL}} | {{n}} | {{n}} | {{n}} | {{n}} |
| Visual Hierarchy | {{PASS/FAIL}} | {{n}} | {{n}} | {{n}} | {{n}} |
| Layout & Grid | {{PASS/FAIL}} | {{n}} | {{n}} | {{n}} | {{n}} |
| Ethical Design | {{PASS/FAIL}} | {{n}} | {{n}} | {{n}} | {{n}} |
| Authenticity | {{PASS/FAIL}} | {{n}} | {{n}} | {{n}} | {{n}} |

## Critical FAIL (즉시 수정)

### [카테고리] 항목 제목

- **심각도:** Critical
- **위치:** `파일경로:라인`
- **위반 원칙:** [원칙명]
- **출처:** [출처 URL/문서명]
- **현재:** [현재 상태]
- **권장:** [개선 방향]

## Major FAIL (다음 스프린트 전)

### [카테고리] 항목 제목

- **심각도:** Major
- **위치:** `파일경로:라인`
- **위반 원칙:** [원칙명]
- **출처:** [출처 URL/문서명]
- **현재:** [현재 상태]
- **권장:** [개선 방향]

## Minor FAIL (개선 권장)

### [카테고리] 항목 제목

- **심각도:** Minor
- **위치:** `파일경로:라인`
- **위반 원칙:** [원칙명]
- **출처:** [출처 URL/문서명]
- **현재:** [현재 상태]
- **권장:** [개선 방향]

## 미검증 항목 (수동 확인 필요)

- `invalid_evidence`: {{n}} 건 — `[미검증:INVALID]` · 접미 없는 `[미검증]`. 2 건 이상이면 REJECT
- `env_gaps`: {{n}} 건 — 남용 방지 4 요건을 다 채운 `[미검증:ENV]`. REJECT 셈에 넣지 않는다
- `verified_coverage`: {{(판정한 체크 항목 수 − env_gaps) / 판정한 체크 항목 수}} — 0.60 미만이면 BLOCKED

### [카테고리] 항목 제목 — {{`[미검증:ENV]` | `[미검증:INVALID]`}}

- **사유:** [정적 분석으로 판정 불가한 이유]
- **확인 방법:** [수동 확인 절차]
- **재검증 명령:** [`[미검증:ENV]` 일 때만 — 환경이 갖춰지면 이 항목을 판정할 실행 가능한 명령]

## NOTE

{{토큰 미사용 등 감사 범위 외 참고 사항}}
