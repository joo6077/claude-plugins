---
title: Infrastructure as Code
version: 0.1.0
last_updated: 2026-04-04
---

# Infrastructure as Code

Terraform 모듈 구조, 상태 관리, drift 감지, plan/apply 워크플로우, 모듈 버저닝, Pulumi/CDK 비교, Policy as Code(OPA, Sentinel), import를 다룬다.

---

## 원칙

### 1. 모듈은 표준 구조를 따른다

`main.tf`(리소스), `variables.tf`(입력), `outputs.tf`(출력), `README.md`(문서), `examples/`(사용 예시)로 구성한다. 이 구조는 Terraform Registry 게시 요건이기도 하며, 모듈 소비자가 별도 설명 없이 구조를 파악할 수 있게 한다. 단일 거대 모듈 대신 기능 단위로 분리하여 재사용성과 테스트 용이성을 확보한다.

> **출처:** [Terraform — Standard Module Structure](https://developer.hashicorp.com/terraform/language/modules/develop/structure)

### 2. 팀 작업은 remote backend + locking이 기본이다

local state는 팀원 간 공유가 불가능하고, 동시 수정 시 상태 파일이 손상된다. S3+DynamoDB, GCS, Terraform Cloud 등 remote backend를 사용하고, state locking으로 동시 apply를 방지한다. state 파일에는 리소스 속성, 시크릿이 포함되므로 암호화 저장과 접근 제어를 적용한다.

> **출처:** [Terraform — Remote State](https://developer.hashicorp.com/terraform/language/state/remote)

### 3. plan 검토 후 승인된 plan만 apply한다

`terraform plan`으로 변경 사항을 미리 확인하고, 검토/승인된 plan 파일(`-out=tfplan`)을 `terraform apply tfplan`으로 적용한다. plan과 apply 사이에 인프라가 변경되면 plan이 무효화되므로, CI에서는 plan → 승인 → apply를 하나의 파이프라인으로 묶는다.

> **출처:** [Terraform — Plan](https://developer.hashicorp.com/terraform/cli/commands/plan)

### 4. Drift는 정기적으로 감지한다

코드 외부에서 수동으로 변경된 인프라(drift)는 다음 apply 시 예기치 않은 결과를 만든다. `terraform plan`의 implicit refresh 또는 `terraform plan -refresh-only`로 현재 인프라 상태와 state 파일의 차이를 정기적으로 확인한다. CI에 야간/주간 drift 감지 파이프라인을 구성한다.

> **출처:** [Terraform — Refresh](https://developer.hashicorp.com/terraform/tutorials/state/refresh)

### 5. import는 상태만 가져온다

`terraform import`는 기존 인프라 리소스를 state에 등록할 뿐, 해당 리소스의 HCL 코드를 자동 생성하지 않는다. import 후 반드시 `terraform plan`으로 state와 코드의 차이를 확인하고, HCL 코드를 실제 인프라와 일치하도록 작성한다. 코드 없이 import만 하면 다음 apply에서 리소스가 변경되거나 삭제될 수 있다.

> **출처:** [Terraform — Import Usage](https://developer.hashicorp.com/terraform/cli/import/usage)

### 6. 모듈 버전을 고정한다

Registry 모듈은 semver 태그로 버전을 고정한다. 버전 없이 최신을 추종하면 upstream의 breaking change가 예고 없이 인프라에 적용된다. `version = "~> 1.2.0"` 같은 제약으로 패치만 자동 반영하고, 마이너/메이저 업그레이드는 명시적으로 수행한다.

> **출처:** [Terraform Registry — Publishing Modules](https://developer.hashicorp.com/terraform/registry/modules/publish)

### 7. Policy as Code로 예방 통제를 구현한다

plan 시점에 정책을 검사하여 위반 리소스가 생성되기 전에 차단한다. Sentinel(Terraform Cloud/Enterprise)은 plan 데이터에 직접 접근하고, OPA(Open Policy Agent)는 plan JSON을 입력으로 받아 Rego로 평가한다. "사후 감사" 대신 "사전 차단"으로 컴플라이언스를 보장한다.

> **출처:** [Sentinel — Policy as Code](https://developer.hashicorp.com/sentinel/docs/concepts/policy-as-code)
> **출처:** [OPA — Terraform](https://www.openpolicyagent.org/docs/latest/terraform/)

---

## 수치/기준값

| 항목 | 값 | 비고 |
|------|-----|------|
| plan -detailed-exitcode: 변경 없음 | 0 | |
| plan -detailed-exitcode: 에러 | 1 | |
| plan -detailed-exitcode: 변경 있음 | 2 | CI에서 분기 조건으로 활용 |
| import CLI | 1 resource씩 | 대량 import는 스크립트로 반복 |
| Registry 태그 형식 | semver (v1.0.1 허용) | v 접두사 선택적 |

---

## 안티패턴

- **환경별 분기가 과도한 거대 모듈**: 하나의 모듈에 dev/staging/prod 분기를 `count`/`for_each` + 조건문으로 구현하면 복잡도가 폭발. 환경별 tfvars 또는 workspace로 분리
- **local state를 팀에서 공유**: 파일 동기화(Dropbox, Git)로 state를 공유하면 동시 수정 시 손상. remote backend + locking 필수
- **CI에서 무조건 auto apply**: plan 검토 없이 자동 적용하면 의도하지 않은 인프라 변경이 프로덕션에 반영. plan → 승인 → apply 워크플로우 준수
- **import 후 HCL 검증 생략**: state에는 등록되었지만 코드가 없으면 다음 plan에서 삭제로 표시됨
- **버전 pin 없이 최신 추종**: `source` 지정 시 version 제약 없으면 upstream 변경이 즉시 반영되어 인프라 장애 가능

---

## Gotchas

- **state lock 실패 시 `-lock=false`로 강행하면 상태 파일이 충돌한다.** 다른 사용자가 동시에 apply 중인 상황에서 lock을 우회하면 state 파일이 서로 다른 버전으로 덮어쓰여 복구가 어렵다. lock 실패 원인(잔존 lock, 권한 문제)을 먼저 해결한다.
- **같은 인프라 객체를 여러 address로 import하면 상태가 손상된다.** 하나의 실제 리소스를 두 개의 Terraform address에 매핑하면, 한쪽을 삭제할 때 실제 리소스가 삭제되고 다른 쪽이 orphan이 된다.
- **remote state에도 민감 정보가 포함될 수 있다.** 데이터베이스 비밀번호, API 키 등이 리소스 속성으로 state에 평문 저장된다. backend의 암호화(SSE-S3, CMEK)와 접근 제어(IAM, bucket policy)를 반드시 설정한다.
- **Pulumi/CDK 비교 문서는 벤더 관점 편향이 있다.** 각 도구의 공식 비교 페이지는 자사 장점을 강조한다. 팀의 기술 스택(TypeScript vs Python vs HCL), 기존 인프라 규모, 상태 관리 방식, 커뮤니티 모듈 생태계를 기준으로 중립적으로 평가한다.
