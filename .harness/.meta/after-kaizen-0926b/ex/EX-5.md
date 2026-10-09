# EX-5 — Codex 원문 대조 (2026-09-26, gpt-5.6-sol, 읽기 전용)

## 물은 것

확인할 것:
- --delete-conflicting-outputs (-d) 옵션이 어느 판에서 어떻게 바뀌었는가(기본 동작 변경 · 폐기 여부)
- 2.16 이후 이 플래그가 여전히 필요하거나 무시되는가, 2.3.3 · 2.4.x 에서의 동작

저장소 근거(읽어서 무엇을 주장했는지 먼저 확인):
- /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase5.md 25행

원문: https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md

## 답

## 1. 출처 목록

가져온 날짜: **2026-09-26 (Asia/Seoul)**

- 저장소 근거: [phase5.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase5.md:25)
- 원문: [build_runner CHANGELOG](https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md)
- 현재 구현 확인: [build_runner_command_line.dart](https://raw.githubusercontent.com/dart-lang/build/master/build_runner/lib/src/build_runner_command_line.dart)

참고로 현재 파일 기준 25행은 출처 목록이고, 실제 주장은 41·144·175–183·203행에 있습니다.

## 2. 질문별 대조

### `--delete-conflicting-outputs`는 어느 판에서 어떻게 바뀌었는가?

원문 인용:

> “Ignore `-d` flag: always delete files as if `-d` was passed.”

이 문장은 **2.7.0** 항목에 있습니다. 같은 항목은 대화형 삭제 확인도 제거했다고 밝힙니다. [CHANGELOG 원문](https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md)

현재 CLI 소스에는 다음 설명과 함께 `delete-conflicting-outputs`가 숨은 옵션으로 남아 있습니다.

> “Removed options, kept to not break old command lines.”

[현재 CLI 원문](https://raw.githubusercontent.com/dart-lang/build/master/build_runner/lib/src/build_runner_command_line.dart)

저장소 주장:

- “2.16.0부터 … `--delete-conflicting-outputs`는 제거된 호환 옵션 목록으로 이동했다.”
- “build_runner 2.16과 충돌하는 ‘플래그 필수’”

판정:

- **2.16.0부터 잘못된 생성물을 기본 수정한다:** 맞음.
- **플래그의 무시/폐기 전환이 2.16.0에서 일어났다:** 틀림. CHANGELOG상 전환점은 **2.7.0**입니다.
- **현재 제거된 호환 옵션으로 남아 있다:** 맞음. 완전히 파서에서 삭제된 것이 아니라, 이전 명령줄을 깨뜨리지 않도록 숨겨진 채 받아들이는 옵션입니다.
- **“제거”의 정확한 의미:** 효과가 제거되어 무시되는 것이지, 옵션 문자열 자체를 입력할 수 없게 제거한 것은 아닙니다.

### 2.16 이후에도 필요한가? 2.3.3·2.4.x에서는 어떻게 동작했는가?

2.16.0 원문 인용:

> “New default output behavior: always fix incorrect generated files.”

[CHANGELOG 원문](https://raw.githubusercontent.com/dart-lang/build/master/build_runner/CHANGELOG.md)

판정:

- **2.16 이후:** 플래그는 필요하지 않고 무시됩니다. 다만 이것은 2.16에서 처음 무시된 것이 아니라 **2.7.0부터 이미 무시**된 상태입니다.
- **2.3.3:** 해당 버전 항목에는 플래그 변경 문장이 **원문에 없음**.
- **2.4.x:** 각 2.4.x 항목에도 플래그 변경 문장이 **원문에 없음**.
- **추론:** `-d` 단축형은 2.3.0에서 추가됐고 “무시” 전환은 2.7.0에 기록됐으므로, 2.3.3과 2.4.x에서는 아직 유효한 동작 옵션이었습니다. 충돌 산출물을 확인 없이 자동 삭제하려는 경우 사용했으며, 무조건 필요한 옵션은 아니었습니다.
- **추론:** 2.7.0의 “대화형 확인 제거”와 “항상 `-d`를 준 것처럼 삭제”를 함께 보면, 그 이전에는 플래그가 삭제 승인을 자동화하는 역할을 했습니다.

따라서 저장소의 “`>=2.16`에서는 플래그 없이 실행” 권고는 결과적으로 맞지만, 정확한 경계는 **`>=2.7.0`**입니다.

## 3. 저장소 반영 문장 제안

- `build_runner 2.7.0부터 -d/--delete-conflicting-outputs는 무시되며, 충돌 파일은 플래그를 지정한 것처럼 항상 삭제된다.`
- `현재 이 옵션은 기존 명령줄과의 호환성을 위해 숨은 removed option으로 받아들이지만 동작에는 영향을 주지 않는다.`
- `build_runner 2.16.0부터는 별도로 잘못되거나 수정된 생성물을 기본적으로 다시 고친다.`
- `2.3.3 및 2.4.x에서는 -d가 아직 유효했으며, 자동 충돌 삭제가 필요할 때 사용할 수 있었다(버전별 직접 문구가 아니라 CHANGELOG 변경 시점에 따른 추론).`
- ``플래그 없이 실행``의 버전 기준은 `>=2.16`이 아니라 `>=2.7.0`으로 적는 것이 정확하다.`

## 4. 못 가져온 것 / 열린 질문

- 지정된 CHANGELOG와 현재 CLI 소스는 모두 정상적으로 가져왔습니다.
- 2.3.3 및 2.4.x 항목에는 해당 플래그의 동작을 직접 설명하는 문장이 없습니다. 위 동작 판정은 2.3.0 추가와 2.7.0 무시 전환 사이의 변경 기록에 근거한 **추론**입니다.
- 2.3.3·각 2.4.x 태그의 실제 소스나 실행 결과까지는 확인하지 않았습니다.