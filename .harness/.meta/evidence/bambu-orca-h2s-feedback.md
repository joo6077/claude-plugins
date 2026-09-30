---
title: "bambu-kit 오르카 · H2S fly-catcher 피드백 — 확보된 근거"
collected: 2026-09-19
method: codex (foreground, 직접 호출 · gpt-5.6-sol · read-only) 4 건 + 오르카 2.4.2 명령줄 슬라이스 실측 + 설치본 대조
contract: .harness/sprint-contract-bambu-kit-orca-h2s-feedback.md
note: 이 스프린트의 킷 반영 근거다. 여기 없는 URL · 수치를 지어내지 마라.
---

## 1. 사용자 피드백 → 원인 → 킷 반영

fly-catcher(바닥이 막힌 원통 컵 + 벽에 붙이는 레일 · PLA Basic · 오르카 2.4.2 · H2S)를 뽑으며 나온 피드백이다.

| 사용자 보고 | 원인 (근거) | 킷 반영 |
| --- | --- | --- |
| 필렛이 끝나는 둘레에 선이 솟았고, 레일과 원통의 직각 모서리에 가까울수록 더 튀어나온다 (사진) | 판에 접하는 필렛이라 2층 벽이 1층보다 0.80 mm 바깥 허공에 놓이고, 그 자리에 깔린 테두리에 붙는다. 테두리를 떼면 붙은 자리가 선으로 남는다. 얹힌 폭 0.38 mm · 모서리 0.44 mm | `failure-recipes.md` §3.5 · SKILL.md Phase 3.0 행 · Gotcha |
| 필렛 이어지는 곳이 이상하고 원이 다 채워지지 않았다 | 같은 오버행. 오르카 `make_overhang_printable` 45° 를 바닥 0~3 mm 에만 켜 0.80 → 0.31 mm. 전체에 켜면 M4 가로 구멍이 폭 4.1 → 0.1 mm 로 막힌다 | `failure-recipes.md` §3.5 · SKILL.md Phase 3.0 |
| 안쪽 바닥에 줄 · 돌기가 올라왔다 | 다림질 재료가 많다. 면적당 양은 층 높이 × 흐름이고 간격은 상쇄된다 — 흐름 12 → 10 % 가 −16.7 % | `surface-recipes.md` §5.3 · Gotcha |
| 심 자국이 보였다 | 부모 설정 `aligned` 이 레일 세 면에 흩어 놓음. `back` + 원 프로젝트의 14° 회전이면 바깥 485 개가 레일 바깥면(벽에 붙는 면), 안쪽 466 개가 홈 속. `aligned_back` 은 안쪽 580 개를 컵 안 정면에 놓는다 | `seam-recipes.md` §6.6 |
| 오르카 파일로만 툴헤드 카메라 초기화 실패 (다른 파일은 정상) | 오르카 H2S 시작 명령(2025/08/06)에 뱀부(2026/04/21)의 카메라 준비 블록이 없다 | `bambu-fields-baseline.md` §11.5 · SKILL.md Phase 3.1 · 게이트 machine 검사 |
| 오르카와 H2S 가 연결되지 않는다 | 뱀부 권한 제어로 외부 슬라이서 직접 전송 불가 | SKILL.md Phase 1.95.3 |
| 3mf 를 여니 뱀부 스튜디오가 값이 바뀌었다고 한다 · Transfer 와 Save 중 무엇? | 더블클릭이 운영체제 연결 앱(뱀부)으로 연다. 설정 전환 창 안내가 절차에 없었다 | SKILL.md 4.4 오르카 분기 |

M4 구멍 보정도 확인했다. `xy_hole_compensation` 0 → 0.12 에서 가로 구멍 층 단면 폭 변화 0, 컵 안쪽 지름만 +0.24 mm.
→ `tolerance.md` §1.3.

## 2. 외부 근거 (Codex 리서치 4 건 · 2026-09-19)

**시작 명령 (r3).**

- 뱀부 커밋 `50bb6ab`(2025-11-06, "툴헤드 카메라 초기화 실패 방지")가 `M104 S0 T0` · `M562 P1 E0 B1` · `M18 E` · `M1028 S1`
  … `M1028 S0` · `M562 P1 E1 B1` · `M17 D` 를 넣었다
  <https://github.com/bambulab/BambuStudio/commit/50bb6ab9ae8b72ba9f3225ebac84db31d8633ccb>
- 오르카 v2.4.2 · main 의 H2S 0.4 프리셋은 2025/08/06 판이고 `M1028` 이 없다
  <https://github.com/OrcaSlicer/OrcaSlicer/blob/v2.4.2/resources/profiles/BBL/machine/Bambu%20Lab%20H2S%200.4%20nozzle.json>
- 같은 증상 이슈 #14947 은 열려 있고 연결된 수정이 없다 <https://github.com/OrcaSlicer/OrcaSlicer/issues/14947>
- `cooling_filter_enabled` 블록을 지워 해결했다는 사용자 사례
  <https://www.reddit.com/r/3Dprinting/comments/1r88prr/toolhead_camera_doesnt_work_with_orca_slicer/>
- 못 찾은 것: `M1028` · `M562 P… E… B…` 의 공식 뜻, HMS 0500-8092 공식 설명

**가로 구멍 (r2).**

- 두 슬라이서 모두 `_shrink_contour_holes()` 가 층 단면의 `ex_poly.holes` 전체를 오프셋한다. 원 판정 없음
  <https://github.com/OrcaSlicer/OrcaSlicer/blob/v2.4.2/src/libslic3r/PrintObjectSlice.cpp#L1511-L1542> ·
  <https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintObjectSlice.cpp#L1370-L1402>
- 통 안쪽 보정이 가로 구멍 높이에서 꺼졌다 켜진다는 재현 #7744
  <https://github.com/OrcaSlicer/OrcaSlicer/discussions/7744> · 가로 구멍 보정 요청 #7080 "계획 없음"
- ISO 273 M4 통과 구멍 4.3 · 4.5 · 4.8 mm
  <https://www.albanycountyfasteners.com/media/6b/b8/g0/1764944339/clearance-hole-chart.pdf>
- 눈물방울(45°) 형상 · 구멍 축 세우기 <https://cdn.jackcrane.rocks/designing-for-print.pdf>

**바닥 필렛 · 테두리 (r1).**

- 오르카 2.4.2 `Brim.cpp` — 테두리 기준은 보정 전 윤곽(`brim_use_efc_outline` 기본 false), 그 바깥 `brim_object_gap`,
  첫 줄은 다시 선 간격 절반 바깥. 선 간격 0.42 mm 면 첫 줄 중심 ≈ 윤곽 + 0.10 + 0.21 mm
  <https://github.com/OrcaSlicer/OrcaSlicer/blob/v2.4.2/src/libslic3r/Brim.cpp#L812-L833>
- `make_overhang_printable` 은 윗층 윤곽을 `tan(각도) × 층 높이` 만큼 줄여 아래층에 합친다. 구멍 보호는 바닥의 오목한 구멍만 대상
  <https://github.com/OrcaSlicer/OrcaSlicer/blob/v2.4.2/src/libslic3r/PrintObjectSlice.cpp#L1394-L1497>
- 판 방향 필렛은 모따기가 낫다 (Prusa 설계 지침)
  <https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135>

**다림질 (r4).**

- 두 슬라이서 `Fill.cpp` 의 다림질 양 식에서 면적당 재료 = 층 높이 × 흐름, 간격은 상쇄
  <https://github.com/OrcaSlicer/OrcaSlicer/blob/v2.4.2/src/libslic3r/Fill/Fill.cpp#L1593-L1612>
- `top_surface_acceleration` 은 윗면 채움에만 걸리고 다림질 경로에는 안 걸린다
  <https://github.com/OrcaSlicer/OrcaSlicer/blob/v2.4.2/src/libslic3r/GCode.cpp#L6423-L6437>
- 솟은 능선 = 과다, 줄 사이 홈 = 부족 <https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing>

**조건부 경사 기본값 (소스 직접 확인).** 뱀부 v02.08.02.61 `PrintConfig.cpp` `seam_slope_conditional` 기본 `true`
(화면 "Smart scarf seam application"), 오르카 v2.4.2 기본 `false` ("Conditional scarf joint").

## 3. 로컬 실측 (2026-09-19)

- 설치본 템플릿 전수: 뱀부 02.08.02.61 에서 `M1028` 은 H2S · X2D 템플릿에만 있다. H2D · H2C 에는 없다
- 뱀부 원문 시작 명령을 그대로 넣은 오르카 프린터 설정은 명령줄 슬라이스가 exit 156 으로 거부된다.
  `cooling_filter_enabled` 블록을 `M145.2 P0 F1` 로 고정하면 통과하고 실행 줄 `M1028 S1` 1 개
- 옵션 목록: `make_overhang_printable` 은 `bambu-02.08.02.61.tsv` 에 없고 `orca-2.4.2.tsv` 에 있다.
  `brim_type: brim_ears` 는 두 목록 모두 받는다
- 오르카 화면에서 다시 저장한 3mf 는 프린터가 원 이름으로 돌아와 있었다 — 전달 전 재확인 필요

## 4. 게이트 음성 대조

`scratchpad/check-gate.sh` · SKILL.md 음성 대조 블록을 zsh 로 그대로 실행. 새 시험 파일 4 개는 목표 위반 1 개씩만 담는다.

| 대상 | 원본 검사 | 목표 판정만 지운 사본 |
| --- | --- | --- |
| `machine-orca-h2s-no-camera-prep.json` | FAIL 1 (`M1028`) · exit 1 | PASS · exit 0 (바뀐 줄 1) |
| `machine-orca-h2s-cooling-filter-var.json` | FAIL 1 (`cooling_filter_enabled`) · exit 1 | PASS · exit 0 (바뀐 줄 1) |
| `machine-orca-h2s-bs-start.json` | PASS · exit 0 · `[미검증]` 0 | 받는 종류에서 machine 을 빼면 FAIL · exit 1 |
| `machine-orca-x1c.json` | PASS · `M1028` FAIL 0 | — |
| 기존 시험 파일 11 개 × 슬라이서 2 | 옛 검사(`baa1a38`)와 출력 · 종료 코드 22 / 22 동일 | — |

## 편집기 진단

측정: 편집기 확장(vscode-markdownlint 0.62.1)이 쓰는 markdownlint-cli2 0.23.2 를 같은 기본 규칙(줄 길이 MD013 끔)으로 실행해,
`git diff -U0 baa1a38` 이 더하거나 바꾼 줄에 걸린 경고만 셌다. 이 세션 편집 직후 편집기가 돌려준 진단 개수와 전체 수가
일치했다 (`failure-recipes.md` 60 · `seam-recipes.md` 90). 맞춤법 검사는 제외.
측정이 살아 있는지: 줄 길이 규칙을 켜면 같은 방법이 새 줄 경고 SKILL.md 37 건을 잡는다.

| 파일 | 기준 커밋 전체 | 지금 전체 | 새로 생긴 경고 |
| --- | --- | --- | --- |
| `bambu-kit/skills/bambu-print-profile/SKILL.md` | 119 | 118 | 0 |
| `references/bambu-fields-baseline.md` | 133 | 133 | 0 |
| `references/tolerance.md` | 60 | 60 | 0 |
| `references/failure-recipes.md` | 60 | 60 | 0 |
| `references/surface-recipes.md` | 79 | 79 | 0 |
| `references/seam-recipes.md` | 90 | 90 | 0 |
| `bambu-kit/evals/gate-fixtures/machine-*.json` 4 개 | — | JSON 파싱 오류 0 | 0 |
| `docs/bambu-kit/bambu-print-profile.html` | — | 접근성 검사로 대신 확인 (DG-04) | 0 |

기존 경고(표 구분선 간격 MD060 등)는 이번 범위 밖이라 손대지 않았다.
