---
name: tone-scaffold
description: >
  파일 헤더, 문서 주석, 시맨틱 typedef 를 프로젝트 파라미터로 채워 생성하고,
  생성물을 자기 감사한다.
  매번 기존 파일을 복사해 쓰던 암묵 템플릿을 명시 템플릿으로 대체한다.
  사용자가 "톤 골격", "헤더 골격", "주석 골격" 을 요청할 때 트리거한다.
  컴포넌트·상태 컨테이너 골격 생성에는 트리거하지 않는다 — 각 스택 킷이 소유한다.
  스택별 화면·라우트·API 레이어 생성에도 트리거하지 않는다 — 각 스택 킷의 생성 스킬이 우선한다.
  이미 작성된 코드의 규칙 위반 판정에는 트리거하지 않는다 — tone-guide 가 우선한다.
argument-hint: "[대상 파일 또는 컴포넌트명]"
user-invocable: true
---

# Tone Scaffold

암묵 템플릿을 명시 골격으로 생성하는 스캐폴더. 생성 후 자기 감사까지 한다.

## Gotchas

1. **작성자 필드를 기존 파일에서 복사하지 마라** — 실제로 발생한 사고다. 파일 헤더의 작성자는 `git config user.name` 을 읽어 채운다. 옛 파일을 참조 삼아 헤더를 만들면 작성자가 따라온다.
2. **템플릿을 붙여 넣고 파라미터를 그대로 두지 마라** — `{widget_prefix}` 같은 자리표시자가 남은 채 생성되면 컴파일은 되면서 규약만 깨진다. 치환 후 자리표시자 잔존 검사를 한다.
3. **쓰지 않을 필드·파라미터를 미리 만들지 마라** — 골격에 있는 항목이라고 전부 채우는 것이 아니다. 실제 호출부에서 전달되는 것만 남긴다. 나머지는 지운다.
4. **기본값 해소 변수에 fallback 접두사를 붙이지 마라** — 기본값 연산자가 이미 fallback 을 표현한다. 도메인·역할 이름을 쓴다. 이 위반은 스캐폴딩 단계에서 가장 자주 새로 만들어진다.
5. **문서 주석을 모든 것에 붙이지 마라** — 커버리지 판정표가 있다. 조립만 하는 진입 함수, 한 줄 위임 래퍼, 본문 내부 람다에는 붙이지 않는다. 특히 람다에 붙이는 것은 금지다.
6. **필드 문서 주석은 비자명한 계약이 있을 때만** — 이름을 그 언어로 옮기기만 한 필드 문서는 노이즈다. 계약·제약·단위가 있을 때만 단다.
7. **라벨 상수를 "더 자연스럽게" 다듬지 마라** — 문서 주석의 반환값 라벨 같은 값은 상수다. 표기를 바꾸면 대조 게이트가 깨진다. 바꾸려면 전수 치환한다.
8. **생성 후 코드 생성기를 돌리기 전에 완료를 선언하지 마라** — 부분 파일에 의존하는 골격은 생성기를 돌려야 컴파일된다. 명령은 감지값을 쓴다.
9. **타입 별칭을 공유 파일에 모으지 마라** — 의미가 생겨난 컴포넌트의 파일에 둔다. 모아 두면 어느 컴포넌트의 계약인지 추적이 끊긴다.
10. **기존 파일 하나를 보고 규약을 단정하지 마라** — 실측 코퍼스에서 헤더 구분선만 세 변종이 공존했다. 다수 패턴이 정리 대상일 수도 있다. 확인이 필요한 값은 사용자에게 묻는다.

## Process

### Step 1. 파라미터 확보

[project-detection.md](../../references/project-detection.md) 절차를 따른다. 오버레이 파일이 있으면 읽고, 없으면 감지 후 확인 대상을 한 번에 확인받는다.

스캐폴딩에 필요한 값: 어댑터 · 주석 언어 · `{widget_prefix}` · `{widget_suffix}` · `props_suffix` · 토큰 클래스 · 헤더 필드 집합 · 구분선 스타일 · 코드 생성 명령.

**확인 대상 값이 비어 있으면 생성하지 마라.** 자리표시자가 남은 파일이 만들어진다.

### Step 2. 규약 로드

생성물이 지켜야 할 규칙을 읽는다.

- [core-naming.md](../../references/core-naming.md) — 이름 조립 규칙, 금지 접두사
- [core-comment.md](../../references/core-comment.md) — 주석 경제성, 보존 판정
- 주석 언어가 한국어면 [locale-korean.md](../../references/locale-korean.md) — 라벨 상수와 문체
- 어댑터가 있으면 [adapter-dart-flutter.md](../../references/adapter-dart-flutter.md) — 슬롯 값과 대조 목록

### Step 3. 템플릿 선택

| 생성 대상 | 템플릿 | 축 |
|---|---|---|
| 파일 헤더 | [file-header.md](../../templates/file-header.md) | 코어 + 로케일 |
| 문서 주석 3변종 | [dart-doc.md](../../templates/dart-doc.md) | 어댑터 + 로케일 |
| 시맨틱 typedef | [dart-typedef.md](../../templates/dart-typedef.md) | 어댑터 |
| 프로젝트 오버레이 | [tone-project.md](../../templates/tone-project.md) | 코어 |

컴포넌트 골격과 상태 컨테이너 골격은 이 킷이 소유하지 않는다 — 스택 킷이 소유한다 (Dart/Flutter 는 flutter-toolkit 의 `templates/widget-freezed-props.md` · `templates/provider-riverpod.md`). 이 스킬은 그 골격 위에 파일 헤더·doc 주석·typedef 를 얹는다.

어댑터가 없으면 어댑터 템플릿은 쓰지 않는다. 파일 헤더와 오버레이만 생성하고 그 사실을 보고한다.

### Step 4. 치환과 생성

1. 템플릿의 자리표시자를 Step 1 값으로 치환한다.
2. 이름은 [core-naming.md](../../references/core-naming.md) 의 결정 절차로 짓는다. 역할을 한 단어로 판정한 뒤 접미사를 고른다.
3. 실제로 필요한 필드·파라미터만 남긴다.
4. 파일을 쓴다.

### Step 5. 생성물 자기 감사 (건너뛰기 금지)

생성 직후 아래를 전부 확인한다. 하나라도 걸리면 고치고 다시 확인한다.

```text
1. 자리표시자 잔존 — 중괄호 자리표시자가 남아 있는가
2. 작성자 필드 — git user.name 과 일치하는가
3. 금지 접두사 — 기본값 해소 변수에 fallback 접두사가 붙었는가
4. 문서 주석 커버리지 — 필요한 곳에 없거나, 불필요한 곳에 있는가
5. 문서 주석 형식 — 파라미터 줄만 있고 반환값 줄이 없는가
6. 문서 주석 본문 — 섹션 헤딩이 들어갔는가
7. 라벨 상수 — 로케일 값과 정확히 일치하는가
8. 이름 정렬 — 컴포넌트 이름과 그 데이터 타입 이름의 접미사가 맞는가
9. 타입 별칭 위치 — 의미 원천 파일에 top-level 로 있는가
10. 미사용 필드 — 실제로 쓰지 않는 파라미터가 남았는가
```

어댑터가 있으면 그 대조 목록도 함께 실행한다. 각 패턴의 "히트가 위반인지" 판정을 확인한 뒤 보고한다.

### Step 6. 빌드 검증

코드 생성기가 필요한 골격이면 감지된 명령으로 생성기를 돌리고 정적 분석까지 통과시킨다. **통과 증거 없이 완료를 선언하지 마라.**

결과를 [briefing-table.md](../../templates/briefing-table.md) 의 완료 보고 형식으로 낸다.

## References

- [project-detection.md](../../references/project-detection.md) — 파라미터 감지와 확인 절차
- [core-naming.md](../../references/core-naming.md) — 이름 조립과 접미사 결정
- [core-comment.md](../../references/core-comment.md) — 주석 경제성과 보존 판정
- [locale-korean.md](../../references/locale-korean.md) — 라벨 상수와 한국어 문체
- [adapter-dart-flutter.md](../../references/adapter-dart-flutter.md) — Dart/Flutter 슬롯 값
- [adapter-contract.md](../../references/adapter-contract.md) — 어댑터 슬롯 계약
- [file-header.md](../../templates/file-header.md) — 파일 헤더 골격
- [dart-doc.md](../../templates/dart-doc.md) — 문서 주석 3변종
- [dart-typedef.md](../../templates/dart-typedef.md) — 시맨틱 typedef
- [tone-project.md](../../templates/tone-project.md) — 프로젝트 오버레이 골격
- [briefing-table.md](../../templates/briefing-table.md) — 완료 보고 표 형식
