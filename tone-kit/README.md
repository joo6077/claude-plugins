# Tone Kit

> **v0.1.0** — 스택 무관 코딩 톤·유지보수성 게이트.

기계적으로 생성된 듯한 주석·네이밍·구조를 걸러 내고, 재사용 골격을 명시 템플릿으로 제공하며, 대량 정리를 파일 단위 승인 루프로 운영한다.

## 포지셔닝

이 킷은 **AI 탐지 회피 도구가 아니다.** AI 생성 코드 탐지 문헌은 표면적 humanizing 을 별도 위험군(`Adversarial`)으로 분류한다. 목표는 읽고 고치기 쉬운 코드이며, 톤 개선은 그 부산물이다. 근거는 `docs/tone/ai-code-stylometry.md` 에 있다.

규칙은 세 등급으로 표기한다.

| 등급 | 조건 |
|---|---|
| `MUST` | 공식 문서·표준이 금지 또는 강제 |
| `SHOULD` | 공식 문서가 권고 수준 |
| `관측 컨벤션` | 공개 근거 없음, 코퍼스 실측만 존재 |

## 3축 레이어

코어/어댑터 2축으로는 표현되지 않는다. 세 축이 직교한다.

| 축 | 값 | 예 |
|---|---|---|
| 스택 | core / adapter | 구분선 주석 금지 = core · 헬퍼 접두사 금지 = adapter |
| 언어 | neutral / locale | 이름 대신 변수명 = neutral · 문서 반환값 라벨 = locale |
| 프로젝트 | universal / param | 역할 접미사 taxonomy = universal · 컴포넌트 prefix = param |

어댑터는 위반이 실제로 관측된 스택에만 만든다. 현재는 `dart-flutter` 하나다. 코어는 어댑터 없이 단독 동작한다.

## 스킬 목록

<!-- AUTO:skills -->
| 스킬 | 설명 |
|------|------|
| `tone-campaign` | 이미 작성된 코드 다수를 한 파일씩 순차 정리하는 운영 루프를 관리한다. |
| `tone-guide` | 코드의 톤·유지보수성 규칙을 구현 전에 강제 로드하고, 완료 선언 전에 규칙 전수 대조까지 수행한다. |
| `tone-scaffold` | 파일 헤더, 문서 주석, 시맨틱 typedef 를 프로젝트 파라미터로 채워 생성하고, |
<!-- /AUTO:skills -->

## 참조 문서

<!-- AUTO:references -->
| 파일 | 설명 |
|------|------|
| `adapter-contract.md` | 어댑터 계약 |
| `adapter-dart-flutter.md` | dart-flutter 어댑터 |
| `core-antipatterns.md` | 안티패턴 판정 카탈로그 A~J |
| `core-comment.md` | 주석 경제성 — 코어 판정 규칙 |
| `core-naming.md` | 역할 기반 네이밍 — 운영 규칙 |
| `core-structure.md` | 코드 구조 — 관심사 분리 · 추출 임계 · 파일 조직 |
| `locale-korean.md` | 한국어 축 운영 규칙 (locale-korean) |
| `project-detection.md` | 프로젝트 파라미터 감지 |
| `sources.md` | 출처 목록 |
<!-- /AUTO:references -->

## Evals

<!-- AUTO:evals -->
| 파일 | 설명 |
|------|------|
| `evals.json` | 파일 |
<!-- /AUTO:evals -->

## 사용 흐름

```text
새 코드 작성          tone-scaffold → tone-guide
기존 코드 리뷰        tone-guide
대량 정리             tone-campaign (내부에서 규칙 로드 + 파일당 승인)
```

## 다른 킷과의 경계

| 상황 | 담당 |
|---|---|
| 스택별 일반 코드 품질 감사 | 각 스택 킷의 audit 스킬 |
| 리팩터 착수 전 위반 열거 후 일괄 편집 | harness 의 refactor-checklist |
| 화면·라우트·API 레이어 생성 | 각 스택 킷의 생성 스킬 |
| 주석·네이밍·구조의 톤 판정 | 이 킷 |

## 프로젝트 오버레이

컴포넌트 prefix, 토큰 클래스, 경로 같은 값은 킷이 정하지 않는다. `tone-guide` 가 감지하고 확인이 필요한 값만 사용자에게 묻는다. 확정값은 프로젝트의 `.claude/tone-project.md` 에 남는다.

## 참고

- 리서치 문서 8종: `docs/tone/`
- 카이젠: `/tone-research` · `/tone-kaizen` (레포 개발용)
