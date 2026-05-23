# bambu-kit

Bambu Lab H2S 자동 process+filament JSON 생성 플러그인.

## 개요

H2S + AMS HT + AMS 2 Pro + Bambu Studio v2.6.0+ 환경 가정. MakerWorld URL이나 로컬 모델 파일을 받아 모델 분석 → 소재 추천 → seam 전략 결정 → Bambu Studio용 process+filament JSON을 자동 생성하고 import용 zip 번들로 떨궈준다.

다른 플러그인(rust-kit, react-kit 등)과 달리 도구형 1스킬 킷이다. guide/audit/system 3종 패턴 대신 `bambu-print-profile` 단일 스킬이 references 4종을 토대로 풀 워크플로우(Phase 1~5)를 수행한다.

## 스킬

| 스킬 | 용도 |
|------|------|
| `/bambu-print-profile` | MakerWorld URL/모델 분석 → 소재 추천 → seam 전략 → Bambu Studio용 JSON 생성 → zip 번들 출력 |

트리거 키워드: "삼프 설정", "Bambu 프로파일 만들어줘", "출력 셋팅 추천", "프린트 프로파일", "MakerWorld 출력".

## 리서치 문서 (스킬 내부 references)

`skills/bambu-print-profile/references/`에 4종이 있으며, 스킬이 SSOT로 참조한다.

| 문서 | 내용 |
|------|------|
| `bambu-fields-baseline.md` | Bambu Studio JSON schema — process/filament 필수 필드, inherits 체인, silent skip 회피 메타필드 |
| `materials.md` | Bambu 필라멘트 카탈로그 40+ + 용도 매핑 (PLA/PETG/PA/PC/ASA/CF/TPU) + AMS 호환성 |
| `seam-recipes.md` | 형상×소재 scarf 매트릭스 + Real-world findings (회전체 random vs aligned, PETG entire_loop stringing 등) |
| `surface-recipes.md` | Surface-first 정책 (Auto-select 결정 트리 + 외벽/Top·Bottom/Ironing 매트릭스 + 트레이드오프) |
| `comment-analysis.md` | v0.4.0 신규 — 댓글 4 카테고리 추출 매뉴얼 + 한/영/중 키워드 사전 + Designer Constraint Override Rule |
| `kaizen-sources.md` | 주 1회 갱신용 데이터 소스 Top 10 (GitHub releases / Bambu Blog / Discourse forum / Reddit / OrcaSlicer wiki) |

## 카이젠

bambu-kit는 자체 카이젠 스킬을 플러그인 외부 `.claude/skills/`에 분리해 둔다(다른 kit 패턴과 동일).

- `/bambu-research` — `kaizen-sources.md` Top 10을 폴링하여 references 4종 갱신
- `/bambu-kaizen` — references 기준으로 SKILL 격차 분석 + 개선

## 출력 위치

```text
/Users/jackson/Hub/60_3D Print/Settings/<모델명>/
├── <모델명>.zip              # Bambu Studio Import Configs용
│   ├── process/<name>.json
│   └── filament/<name>.json (멀티 소재 시 N개)
└── notes.md                  # 케이스별 디테일/실측 결과
```

## 검증된 실측 사례

| 모델 | 소재 | 결과 |
|------|------|------|
| Box opener knife (MakerWorld 583712) | PLA Basic dual-color | ✅ 정상 출력 |
| H2D Vent Pipe (1441653) | PETG HF + TPU 90A | ⚠️ stringing (필라멘트 건조 부족 의심) |
| Stealth Press 1S (825644) | ASA dual-color | ✅ PDF/영상 통합 분석 dogfood — v0.3.0 |
| 9mm Craft Knife Elite (1517485) | PLA Basic | ⚠️ 디자이너 권장 무시 회귀 → v0.4.0 Phase 1.6 신규 |

## 변경 이력

- **v0.4.0** (2026-05-23) — Phase 1.6 Comment Analysis 신규, Designer Constraint Override Rule 정책, comments-raw.md 아카이브, 전체 크롤링 강화(다국어/페이지네이션/스크롤), references/comment-analysis.md 추가. 9mm Craft Knife Elite 회귀 dogfood.
- **v0.3.0** (2026-05-19) — Phase 1.5 Attached Resources Analysis (PDF/영상/GitHub), notes.md 5섹션 표준화, Phase 5 coupon 자동 생성. Stealth Press 1S dogfood.

## 출처

- Codex research 8회 (모두 평균 25/25점). 전체 로그: `~/.claude/codex-research-log/2026-05.md`
- 실측 dogfood 4건 (2026-05-15 ~ 2026-05-23)
