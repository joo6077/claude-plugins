# Perf Kit

> **v0.1.0** — 스택 무관 성능 · 효율 · 비용 비교 킷.

두 버전(옛 · 새 코드, 옛 · 새 서버, 설정 두 가지)을 같은 조건에서 반복 측정하고, 지표마다 통계 판정 · 월 비용 환산 ·
기기 부담 예산 대조를 HTML 보고서 한 장으로 만든다. 스택별 측정 방법은 스킬 안 `references/stacks/` 에 모아 두고,
프로젝트 스택을 감지해 맞는 문서만 읽는다.

## 이 킷이 고치는 것

변화율 하나로 "빨라졌다" 고 말하는 일. 2026-11-08 viseo365 TC-056 은 랜딩 프리로드를 3:3 표본으로 재서 -23.9% 를 냈다.
양측 Mann-Whitney 에서 3:3 은 아무리 갈려도 p 가 0.1 아래로 내려가지 않는다 — 이 킷은 그 지표를 `표본 부족` 으로 판정한다.

## 스킬

<!-- AUTO:skills -->
| 스킬 | 설명 |
| --- | --- |
| `perf-compare` | 두 버전(옛 · 새 코드, 옛 · 새 서버, 설정 두 가지)의 성능 · 효율 · 비용을 같은 조건에서 반복 측정해 비교하고, 통계 판정 · 월 비용 환산 · 기기 부담 예산 대조를 HTML 보고서 한 장으로 만든다. |
<!-- /AUTO:skills -->

## 스택별 측정 문서

| 문서 | 감지 | 측정 |
| --- | --- | --- |
| `stacks/server.md` | HTTP API 비교 | 응답 시간 · 동시 호출 · CPU 시간 · DB 쿼리 · 외부 API |
| `stacks/flutter.md` | `pubspec.yaml` | 콜드 스타트 · 프레임 · 메모리 · 발열 · 배터리 |
| `stacks/rust.md` | `Cargo.toml` | criterion · hyperfine · 최대 메모리 · 바이너리 크기 |
| `stacks/web.md` | `vite` · 화면 라이브러리 · `src-tauri/` | Lighthouse(LCP · TBT · CLS) · 번들 · Tauri |
| `stacks/load.md` | p95 · 처리량 비교 | k6 고정 도착률 · wrk |

새 스택은 같은 절 순서(감지 → 함정 → 지표별 경로 → 명령 → 출처)로 문서 하나를 더하고 `SKILL.md` 1 단계 감지 표에 한 줄을 더한다.

## 다른 킷과의 관계

`flutter-toolkit` · `rust-kit` · `react-kit` · `backend-kit` 은 `plugin.json` 의 `dependencies` 에 `perf-kit` 을 선언한다.
그 킷 중 하나를 설치하면 이 킷도 함께 설치된다. 스택 킷은 측정 지식을 따로 들지 않는다 — 원칙이 키트마다 복사되면
한쪽만 고쳐져 어긋나기 때문이다.

## 시험

```bash
python3 -m unittest discover -s perf-kit/evals/perf-compare -v
```

알려진 답 대조(SciPy 문서 예제 · 손으로 센 순열 수 · 비용 계산)와, 계산을 일부러 틀린 사본으로 테스트가 떨어지는지 본다.
