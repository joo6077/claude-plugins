# EX-8 — Codex 원문 대조 (2026-09-26, gpt-5.6-sol, 읽기 전용)

## 물은 것

확인할 것:
- Flux 최신 안정 판과 날짜
- Argo CD 최신 안정 판과 날짜
- Kubernetes 최신 안정 판(1.37 여부)과 날짜, 지원 중인 판 목록

저장소 근거(읽어서 무엇을 주장했는지 먼저 확인):
- /Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase8.md 39행

원문: https://github.com/fluxcd/flux2/releases , https://github.com/argoproj/argo-cd/releases , https://kubernetes.io/releases/

## 답

조회 기준일: 2026-09-26(KST). 저장소는 수정하지 않았습니다.

## 1. 출처 목록

실제로 가져온 자료만 나열합니다.

- 저장소 근거: [phase8.md](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/.harness/.meta/evidence/phase8.md:33) — 2026-09-26 읽음
- [Flux GitHub Releases](https://github.com/fluxcd/flux2/releases) — 2026-09-26 가져옴
- [Argo CD GitHub Releases](https://github.com/argoproj/argo-cd/releases) — 2026-09-26 가져옴
- [Kubernetes Releases](https://kubernetes.io/releases/) — 2026-09-26 가져옴

## 2. 질문별 확인

### Flux 최신 안정판과 날짜

- 원문 인용: “Flux v2.9.5 is a patch release…” 원문에서 `v2.9.5`에는 “Latest”가 붙어 있고, 게시 시각은 “released this 31 Aug 17:05”입니다. HTML 시간값은 `2026-08-31T17:05:02Z`입니다. [원문](https://github.com/fluxcd/flux2/releases)
- 저장소 주장: 39행 `Flux v2.9.5`
- 판정: **맞음**
- 확인 결과: 최신 안정판은 **v2.9.5**, 게시일은 **2026-08-31 UTC**입니다.

### Argo CD 최신 안정판과 날짜

- 원문 인용: `v3.5.3`에는 “Latest”가 붙어 있고 “released this 14 Sep 07:58”로 표시됩니다. HTML 시간값은 `2026-09-14T07:58:59Z`입니다. 한편 더 위의 `v3.6.0-rc1`은 “Pre-release”입니다. [원문](https://github.com/argoproj/argo-cd/releases)
- 저장소 주장: 38행 `Argo CD v3.5.3`
- 판정: **맞음**
- 확인 결과: 최신 안정판은 **v3.5.3**, 게시일은 **2026-09-14 UTC**입니다.

### Kubernetes 최신 안정판과 날짜

- 원문 인용: “Latest Release:1.37.0 (released: 2026-08-26)” [원문](https://kubernetes.io/releases/)
- 저장소 주장: 33행 `Kubernetes v1.37.1`
- 판정: **틀림**
- 확인 결과: **1.37 계열인 것은 맞지만**, 지정 원문이 밝히는 최신 안정 패치는 **v1.37.0**, 날짜는 **2026-08-26**입니다. 원문에는 `v1.37.1`이 없습니다.

### Kubernetes 지원 중인 판

- 원문 인용: “The Kubernetes project maintains release branches for the most recent three minor releases (1.37, 1.36, 1.35).” [원문](https://kubernetes.io/releases/)
- 저장소 주장: 지원 중인 판 목록은 해당 근거 목록에 적혀 있지 않음.
- 판정: **저장소 주장 없음**. 원문이 명시한 유지 대상은 **1.37, 1.36, 1.35**입니다.
- 참고: 같은 페이지에는 1.34의 EOL이 “2026-10-27”로 표시되어 있어, 상단의 “most recent three” 문장과 시점상 긴장이 있습니다. 지원 목록을 기록할 때는 원문의 명시적 유지 목록을 그대로 쓰는 편이 안전합니다.

## 3. 저장소에 반영할 문장 제안

- `Flux 최신 안정판은 v2.9.5이며 2026-08-31에 게시되었다.`
- `Argo CD 최신 안정판은 v3.5.3이며 2026-09-14에 게시되었다(v3.6.0-rc1은 사전 릴리스).`
- `Kubernetes 릴리스 페이지 기준 최신 안정판은 v1.37.0이며 2026-08-26에 게시되었다.`
- `Kubernetes가 명시적으로 유지하는 최근 세 마이너 릴리스는 1.37, 1.36, 1.35이다.`

## 4. 못 가져온 것 / 열린 질문

- 못 가져온 지정 원문: **없음**
- 열린 질문: Kubernetes 페이지는 유지 대상이 `1.37·1.36·1.35`라고 명시하면서도 `1.34`의 EOL을 2026-10-27로 표시합니다. 이 페이지만으로 1.34의 현재 지원 상태를 더 단정하지 않았습니다.
