---
name: flutter-perf-probe
description: >
  Flutter 앱의 콜드 스타트 · 프레임 드랍 · 메모리 · CPU · 발열 · 배터리 · 화면당 전송량을 두 버전에서 반복 측정해 원시 표본을 모으고,
  harness 의 perf-compare 기록 형식(perf.json)으로 넘겨 통계 판정 · 비용 환산 · 예산 대조를 받는다.
  "Flutter 성능 측정", "앱 시작 시간 비교", "프레임 드랍 측정", "앱 발열 측정", "앱 배터리 소모 측정", "스크롤 버벅임 수치" 같은 요청 시 트리거.
  서버 · API 만 비교하는 요청에는 트리거하지 않는다 — harness 의 perf-compare 가 맡는다.
  코드를 읽고 성능 문제를 지적하는 감사에는 트리거하지 않는다 — flutter-audit 이 맡는다.
argument-hint: "[비교할 두 버전 또는 잴 화면]"
user-invocable: true
---

# Flutter Perf Probe

## Gotchas

- **profile mode · 실기기가 아니면 앱 쪽 수치는 근거가 아니다** — 공식 문서는 성능 측정을 물리 기기 + `--profile` 에서 하라고 하고, profile mode 는 simulator/emulator 에서 꺼져 있다 (<https://docs.flutter.dev/perf/ui-performance>). 프레임 · CPU · 메모리 · 발열 · 배터리는 실기기 profile 빌드에서만 잰다. 디버그 빌드 · 시뮬레이터로는 같은 빌드로 서버만 바꾼 비교의 서버 쪽 구간만 잰다 (flutter-audit 의 Performance — Environment Exclusion Checklist 와 같은 기준)
- **프레임 0 개는 "버벅임 없음" 이 아니라 측정 실패다** — 프레임 지표 도구가 0 프레임을 돌려주면 그 측정은 죽은 것이다. 2026-11-08 TC-056 에서 MCP 프레임 지표가 세 번 모두 `No Frame events captured` 를 돌려줬다. `frame_count` 가 0 보다 큰지 먼저 보고, 0 이면 `references/flutter-metrics.md` 의 integration_test 경로로 바꾼다 (E2 — 4 완료 전 대조 항목)
- **프레임 예산은 기기 주사율로 정한다** — 60Hz 는 16.7ms, 120Hz 는 8.3ms 다. `TimelineSummary` 의 `missed_*_budget_count` 는 주사율과 관계없이 16ms 고정값(`kBuildBudget`)으로 센다. 120Hz 기기는 프레임 시간 목록에서 다시 센다 (flutter-audit 의 target refresh rate 항목과 같다)
- **시간 마커 임시 코드는 측정 뒤 지운다** — 콜드 스타트 구간을 재려고 넣은 로그 · 채널 코드는 측정이 끝나면 되돌리고 `git diff` 로 남은 것이 없는지 본다. 남기면 다음 커밋에 섞인다 (E2 — 4 대조 항목)
- **시뮬레이터 · 에뮬레이터의 발열 · 배터리 값은 쓰지 않는다** — 기기의 열 · 전력 상태가 아니라 맥의 상태를 따른다. 실기기에서 온 값이 아니면 지표에서 빼고 이유를 적는다
- **MCP 서버와 도구 이름은 이 파일에 적지 않는다** — 프로젝트 설정에서 읽은 이름만 쓴다. 프레임 · 네트워크 · 성능 지표 도구가 있는지는 서버 도구 목록으로 확인한다

## 하는 일

Flutter 앱 쪽 수치를 재는 방법을 고르고, 두 버전에서 반복 측정한 원시 표본을 `perf.json` 의 `metrics` 로 모은다.
판정 · 비용 · 보고서는 `harness:perf-compare` 가 맡는다. 이 스킬은 무엇을 어떻게 잴지와 표본의 질을 책임진다.

## Input

`$ARGUMENTS`: 비교할 두 버전이나 잴 화면 (선택). 없으면 이번 대화에서 바꾼 것을 대상으로 삼고, 무엇을 비교할지 한 문장으로 되묻는다.

## Process

### 1. 환경 확인

- 플러그인 공용 `references/project-detection.md` 로 SDK 명령 접두(`fvm flutter` 등)와 MCP 서버 이름을 정한다
- 아래 다섯 줄을 응답에 남긴다. 모르면 `미확인` 이라 적는다 — 빈칸 금지

```text
빌드 모드: {profile | release | debug}
기기: {실기기 모델명 | 시뮬레이터 · 에뮬레이터 이름}
주사율: {60 | 90 | 120}Hz → 프레임 예산 {16.7 | 11.1 | 8.3}ms
렌더러: {Impeller | Skia}
호스트 상태: {swap 사용량 · memory pressure} (시뮬레이터일 때)
```

- 디버그 빌드나 시뮬레이터면 잴 수 있는 지표를 서버 쪽 구간(랜딩 프리로드처럼 API 를 기다리는 시간)과 전송량으로 좁히고, 그 사실을 사용자에게 알린다

완료 기준: 위 다섯 줄이 응답에 있다.

### 2. 지표와 측정 경로 고르기

- `references/flutter-metrics.md` 에서 지표마다 측정 경로를 고른다
- `harness:perf-compare` 의 1 (비교 설계와 사용자 확인) 표를 이 지표들로 채워 확인받는다. 대조 지표는 바꾼 변수가 닿지 않는 구간으로 고른다 — 서버만 바꿨으면 `main()` 까지 시간, 앱만 바꿨으면 같은 API 단독 호출 시간
- harness 가 설치돼 있지 않으면 같은 표를 직접 보여 주고, 판정은 하지 않는다고 미리 알린다

완료 기준: 사용자가 설계 표를 확인했다는 응답이 대화에 있다.

### 3. 측정

- 새로 짠 파싱 명령(로그에서 마커 시각 빼기, timeline summary 에서 값 꺼내기)은 본 측정 전에 알려진 답 대조를 한다 — 손으로 셀 수 있는 로그 두세 줄로 기대값 · 실제값 · 명령을 남긴다
- 쪽마다 예열 1 회 + 5 회 이상 잰다. 콜드 스타트는 매 회 앱 프로세스를 완전히 끈다
- 프레임 지표는 `frame_count` 가 0 보다 큰지 회마다 확인한다
- 측정이 끝나면 임시 마커 코드를 되돌리고 `git diff --stat` 를 응답에 남긴다

완료 기준: 지표마다 쪽별 원시 표본이 예열 + 5 개 이상이고, 프레임 지표는 회마다 `frame_count > 0` 이다.

### 4. 넘기기와 완료 전 대조

- 표본을 `perf.json` 의 `metrics` 로 옮긴다. 형식은 `harness:perf-compare` 의 `references/samples-format.md` 다. 결과 폴더는 `{앱 루트}/.mcp_screenshots/test-evidence/{케이스 폴더}/` 다
- `harness:perf-compare` 를 불러 4 (기록과 판정) 부터 이어 간다
- harness 가 설치돼 있지 않으면 지표마다 쪽별 중앙값과 원시 표본만 보고하고, `[미검증]` 에 네 칸(막는 것 · 시도한 우회 · 통제 불가 사유 · 재검증 명령)을 채워 통계 판정이 빠졌다고 적는다. 변화율만으로 `개선` 이라 쓰지 않는다

완료를 말하기 전에 아래를 확인하고 결과를 응답에 남긴다.

- [ ] 1 의 환경 다섯 줄이 있다
- [ ] 프레임 지표는 회마다 `frame_count > 0` 이었다 — 0 이 나온 회는 버리고 그 수를 적었다
- [ ] 실기기가 아닌 곳에서 잰 발열 · 배터리 · 프레임 값을 지표에 넣지 않았다
- [ ] 임시 마커 코드를 되돌렸다 — `git diff --stat` 출력이 응답에 있다
- [ ] `harness:perf-compare` 의 `report` 출력(`판정:` · `지표:` 줄)을 보고에 옮겼다, 또는 `[미검증]` 네 칸을 채웠다
- [ ] 위 Gotchas 를 한 줄씩 다시 읽고 어긴 것이 없다

## References

- `references/flutter-metrics.md` (이 스킬 폴더) — 지표별 측정 명령 · 출력 위치 · 함정
- `references/project-detection.md` (플러그인 공용) — SDK 명령 접두와 MCP 서버 이름 감지
- `skills/flutter-audit/SKILL.md` (플러그인 공용) — Performance — Environment Exclusion Checklist. 환경 다섯 줄의 기준 원본
- `harness:perf-compare` (다른 플러그인) — 비교 설계 · `perf.json` 형식 · 통계 판정 · 비용 환산 · 보고서
