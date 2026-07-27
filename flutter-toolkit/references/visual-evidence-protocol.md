---
title: Visual Evidence Protocol (시각 산출물 완료 증거 규약)
version: 1.0.0
last_updated: 2026-07-27
source: /insights 2026-07-27 Friction #2 (신규 최상위 신호) · skill-design-guide §3.7 · qa-evaluation-guide §Evidence Validity Gate
enforcement: E2 (체크리스트 아티팩트)
---

# Visual Evidence Protocol

UI 를 만들거나 고치는 flutter-toolkit 스킬(`flutter-widget` · `flutter-screen` ·
`flutter-skeleton` · `flutter-transition` · `flutter-responsive`)이 **완료를 선언하기 직전**에
실행하는 증거 규약이다. 상위 정의는 아래를 따르며 여기서 임계값이나 마커 의미를 재정의하지 않는다.

- 마커·임계값 SSOT: `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol
- 증거 유효성 SSOT: 같은 문서 §Evidence Validity Gate
- 등급(E1/E2/E3) SSOT: `harness/docs/guides/skill-design-guide.md` §3.7

## 왜 필요한가

`/insights` 2026-07-27 (53 일 · 51 세션) 에서 **Friction #2 "시각·런타임 검증을 신뢰할 수 없음"**
이 신규 최상위 마찰로 올라왔고, 관측된 사례가 전부 Flutter 였다.

- 빈 카탈로그 화면의 스냅샷을 근거로 "정상 렌더링" 을 **반복 주장**. 실제 원인은 unbounded-height
  `ListView` collapse 였다. 사용자 신뢰가 손상되어 욕설로 끝난 세션이 2 건 발생했다
- AOT 빌드 + multi-VM vmservice race 로 런타임 검증 자체가 실패 → 검증 부담이 전부 사용자에게 전가
- 사용자가 "MCP 를 UI/e2e 검증에 쓰지 않는 재발 습관을 영구히 고쳐달라" 는 전용 세션을 개설

즉 문제는 "증거가 없다" 가 아니라 **"증거가 있는데 아무것도 입증하지 않는다"** 였다.
빈 캡처를 "문제 없음" 으로 읽는 것이 사고의 실제 형태다.

## Step 0 — 무엇을 바꾸는지 먼저 확정한다

편집을 시작하기 전에 다음 3 줄을 응답에 남긴다. 시각 작업은 말이 의도를 충분히 규정하지 못한다.

1. **대상**: 바꿀 위젯을 `파일:라인` 으로 지목 (신규 생성이면 "신규" 라고 명시)
2. **바꿀 것 / 바꾸지 않을 것**: 색상·크기·모션·레이아웃 중 **유지할 속성을 열거**한다
3. **교체 여부**: 기존 위젯을 Flutter 기본 위젯이나 다른 컴포넌트로 **교체**하려면 편집 전에 승인을 받는다

> 기본값은 **기존 위젯 수정**이다. "아이콘이 회전했으면 좋겠다" 는 그 아이콘을 회전시키라는 뜻이지
> `CircularProgressIndicator` 를 새로 만들라는 뜻이 아니다.

## Step 1 — 시각 검증 채널 결정 (프로젝트 감지 기반)

특정 MCP 서버 이름이나 도구 이름을 가정하지 마라. 프로젝트마다 다르다.
`references/project-detection.md` 실행 후 아래 순서로 **실제로 존재하는 채널**을 고른다.

| 우선 | 채널 | 감지 방법 | 산출 증거 |
| ---- | ---- | --------- | --------- |
| 1 | golden test | `test/` 에 `matchesGoldenFile` 사용처가 있거나 `test/**/*golden*` 존재 | `$FLUTTER test` 출력 + 실패 시 생성되는 diff 이미지 |
| 2 | integration_test 스크린샷 | `integration_test/` 디렉토리 존재 | `takeScreenshot` 산출 PNG |
| 3 | 프로젝트 등록 MCP | `.mcp.json` · `.claude/settings.json` · `.claude/settings.local.json` 의 `mcpServers` 키를 **읽어서** 사용 가능한 서버명을 확인 | 스냅샷/스크린샷 |
| 4 | 없음 | 위 3 개 모두 부재 | **degraded 모드** — Step 4 로 |

`HAS_VISUAL_CHANNEL` = 1~3 중 하나라도 사용 가능하면 true.

## Step 2 — baseline → 변경 → 재캡처 → 대조

`HAS_VISUAL_CHANNEL = true` 일 때만 수행한다.

1. **baseline 캡처**. 캡처한 것을 한 문장으로 **서술**한다 (본 것을 적는다 — "정상" 같은 판정이 아니라
   "카드 3 행 · 헤더 텍스트 '내 그룹' · 하단 여백 있음" 처럼 요소를 지목)
2. **한 번에 하나의 의도**만 편집한다. 여러 변경을 묶으면 재캡처 차이가 무엇 때문인지 귀속되지 않는다
3. **재캡처**
4. **대조**. Step 0 에서 "바꾸지 않을 것" 으로 열거한 속성이 그대로인지 확인한다.
   **의도 외 영역이 변했으면 self-reject 하고 되돌린 뒤 다시 시도**한다 (최대 3 회, 이후 사용자 에스컬레이션)

Figma 시안 대조처럼 수치 수렴이 필요한 작업은 이 규약을 만족한 뒤
`references/figma-parity-self-verify.md` 의 SSIM 루프로 이어간다.

## Step 3 — 증거 유효성 (PASS 확정 전 필수)

캡처를 얻었다는 것만으로 PASS 가 아니다. `qa-evaluation-guide.md §Evidence Validity Gate` 4 검사를
그대로 적용한다. 시각 산출물에서 특히 자주 깨지는 것은 검사 1·2 다.

- **빈 화면·빈 목록·플레이스홀더만 있는 캡처는 PASS 증거가 아니라 검증 실패 신호다.**
  "요소가 안 보이니 문제도 없다" 는 invalid absence 이며, Friction #2 의 실제 사고 형태였다
- 캡처에서 조건이 요구하는 **구체 요소를 지목**해 근거에 쓴다. 지목할 수 없으면 그 캡처는 무효 증거다
- 캡처 자체가 실패했거나 도구가 응답하지 않으면 그것은 PASS 가 아니라 `[미검증]` 이다

## Step 4 — degraded 모드 (`HAS_VISUAL_CHANNEL = false` 또는 캡처 실패)

**멈추고 말하라. 추측하지 마라.**

1. 해당 항목에 `[미검증]` 마커 + 사유 한 줄 (예: `[미검증] 시각 검증 채널 없음 — golden/integration_test/MCP 모두 부재`)
2. 시도한 fallback 단계를 남긴다 (어떤 채널을 어떤 순서로 확인했는지)
3. "정상 동작합니다" / "정상 렌더링됩니다" 같은 **서술로 완료를 대체하지 않는다**
4. 사용자에게 확인이 필요한 지점을 1~3 개로 좁혀서 제시한다

임계값은 canonical 을 따른다 — `[미검증]` 1 건은 경고 명시 후 진행 가능, **2 건 이상이면 완료가
아니라 부분 완료**로 보고한다.

## Visual Evidence Block (완료 보고에 복사해 채운다)

```text
## Visual Evidence
- 대상: <파일:라인 또는 "신규">
- 유지할 속성: <색상/크기/모션/레이아웃 중 열거>
- 채널: <golden | integration_test | mcp:<서버명> | none>
- baseline: <본 것을 요소 단위로 서술 | [미검증] 사유>
- 재캡처: <본 것을 요소 단위로 서술 | [미검증] 사유>
- 대조 결과: <의도한 변경만 발생 | 의도 외 변경 발견 → self-reject N회>
- 미검증: N 건 [항목 — 사유 — 시도한 fallback]
```

```text
Bad:  위젯 수정 → "다크 모드에서도 정상적으로 보입니다" (캡처 없음)
Bad:  스냅샷이 빈 화면 반환 → "렌더링 정상" 으로 해석 → 반복 주장 → 신뢰 손상
Good: baseline 캡처("카드 3행·헤더 '내 그룹'") → 보더만 변경 → 재캡처 → 배경색 동일 확인 → 완료
Good: 채널 없음 → "[미검증] 시각 검증 채널 부재" 명시 → 부분 완료로 보고 + 확인 요청 2건 제시
```

## 참조

- `harness/docs/guides/skill-design-guide.md` §3.7 Completion Evidence Gate (등급·5 조항 SSOT)
- `harness/docs/guides/qa-evaluation-guide.md` §Evidence Validity Gate · §Canonical Unverified-Evidence Protocol
- `flutter-toolkit/references/figma-parity-self-verify.md` — 본 규약 통과 후 수행하는 Figma SSIM 수렴 루프
- `flutter-toolkit/references/project-detection.md` — 채널 감지의 전제 절차
- golden 매처 공식 문서: <https://api.flutter.dev/flutter/flutter_test/matchesGoldenFile.html>
  (폰트·플랫폼·Flutter 버전이 다르면 같은 코드도 diff 가 난다 — CI 와 로컬의 OS/버전을 맞춰야 한다)
