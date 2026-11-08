# 스택: 웹 프런트엔드 · Tauri

감지: `package.json` 에 `react` · `vue` · `svelte` 같은 화면 라이브러리나 `vite` 가 있다. Tauri 데스크톱 앱이면 `src-tauri/` 가 있다.

## 함정

- **Lighthouse 한 번은 표본 하나다** — 같은 페이지도 회마다 값이 흔들린다. 공식 문서는 여러 번 돌려 중앙값을 보라고 하고, 5 회 중앙값 점수가 1 회보다 두 배 안정적이라고 적는다. 쪽마다 5 회 이상 돌리고 회마다 값을 표본으로 쓴다. 성능 점수 하나로 비교하지 않고 LCP · TBT · CLS 를 지표로 나눈다
- **실험실 측정으로는 INP 를 제대로 못 잰다** — INP 는 실제 사용자 입력에서 재는 현장 지표이고, 실험실 값은 측정 중 어떤 조작을 했는지에 따라 달라진다. 실험실에서는 TBT 를 대신 보되, 공식 문서도 TBT 는 INP 를 대체하지 못하는 대리 지표라고 적는다
- **스로틀링 설정을 두 쪽에 똑같이 둔다** — 기기 흉내 · 네트워크 · CPU 감속 설정이 다르면 비교가 아니다. 쓴 설정을 `fixed` 에 적는다
- **개발 서버가 아니라 빌드 결과를 잰다** — `vite build` 뒤 `vite preview`(빌드 결과를 로컬에서 미리 보는 명령)나 실제 정적 서버로 잰다. 공식 문서는 `vite preview` 를 운영 서버로 쓰지 말라고 적는다 — 서버 응답 속도까지 비교 대상이면 실제 정적 서버로 잰다

## 지표별 경로

| 지표 | 경로 | 표본 |
| --- | --- | --- |
| LCP · TBT · CLS | Lighthouse CLI | 회마다 JSON 의 `audits.*.numericValue` |
| 번들 전송량 | `dist/` 의 gzip 크기 합 | 결정값 — 쪽마다 2 회 |
| Tauri 앱 시작 시간 | 앱 안 임시 마커 로그 | 회마다 실행 → 첫 화면 마커 |
| Tauri 앱 메모리 | `ps` RSS | 시나리오 끝 값 |

## Lighthouse

```bash
npx lighthouse "http://localhost:4173/" --only-categories=performance \
  --output=json --output-path=run-03-a.json --chrome-flags="--headless" --quiet
python3 - run-03-a.json <<'EOF'
import json, sys
a = json.load(open(sys.argv[1]))["audits"]
print(a["largest-contentful-paint"]["numericValue"], a["total-blocking-time"]["numericValue"],
      a["cumulative-layout-shift"]["numericValue"])
EOF
```

- LCP · TBT 는 ms, CLS 는 단위 없는 값이다. `unit` 을 지표마다 맞춘다

## 번들 전송량

```bash
vite build >/dev/null && find dist -type f \( -name '*.js' -o -name '*.css' \) -exec gzip -9 -c {} \; | wc -c
```

- 서버가 brotli 로 보내면 `gzip` 대신 `brotli -c` 로 잰다. 실제 전송 압축과 같은 방식으로 잰다
- 첫 화면에 실제로 받는 파일만 보려면 Lighthouse JSON 의 `audits["network-requests"]` 에서 전송 크기를 합한다

## Tauri 앱

- 시작 시간은 Rust 쪽 `main` 첫 줄과 프런트엔드 첫 렌더에 임시 마커를 찍고, 앱을 완전히 끈 뒤 다시 켜는 것을 한 회로 한다. 마커는 측정 뒤 되돌린다
- 메모리는 Tauri 프로세스와 웹뷰 프로세스가 나뉜다. 두 프로세스의 RSS 를 함께 합해 적고, 무엇을 합했는지 `source` 에 쓴다

## 출처

- Lighthouse 변동성(여러 번 · 중앙값 · 5 회): <https://github.com/GoogleChrome/lighthouse/blob/main/docs/variability.md>
- Lighthouse CLI 옵션: <https://github.com/GoogleChrome/lighthouse/blob/main/readme.md>
- INP: <https://web.dev/articles/inp> · TBT: <https://web.dev/articles/tbt>
- Vite CLI(`vite preview`): <https://vite.dev/guide/cli>
