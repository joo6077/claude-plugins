---
feature: "bambu-kit seam 정책 전환 + 실물 기준 버전·값 검증"
slug: bambu-seam-policy
created: "2026-09-05 23:03"
complexity: "복잡"
conditions: 27
status: active
owner_session: 80e6651a-4542-4964-92cf-b2b72d8c3a42
conditions_digest: sha256:134c147c06cb3da5
locked_at: "2026-09-05 23:04"
---

## 배경

사용자가 회전체 default 인 `seam_position: random` 을 거부했다 ("솔직히 랜덤 별로임").
리서치로 확인된 바 random 은 해결이 아니라 **한 줄을 specks 로 바꾸는 것**이다 (Prusa KB).
실제 "해결" 은 spiral vase + Smooth Spiral 하나뿐이다.

동시에 킷이 참조 헤더에 `2.6.0 (v02.06.00.51)` 을 하드코딩하고 있는데, 실제로 슬라이서가 읽는
프로파일 번들은 **앱과 별개로 네트워크 갱신**된다 (로컬 앱 `02.06.00.51` vs 프로파일 번들
`02.06.00.05`, 2026-05-20 수신). 킷은 하드코딩 대신 실물을 읽어야 한다.

사용자 선택 (2026-09-05): 업그레이드는 **감지 + 알림만**(자동 설치 안 함), 킷 검사는
**버전 + 값 검증**까지.

## 리서치 소스

- Codex research D (seam 해결 기법) · E (소재별 seam) · F (버전) — 전부 foreground read-only
- 서브에이전트: H2S 프로파일 diff `v02.06.00.51` ↔ `v02.08.02.61` (163 파일 전수),
  spiral vase 키 소스 추적 (`PrintConfig.cpp` · `GCode.cpp` · `ConfigManipulation.cpp`)
- 설치된 `02.06.00.51` 바이너리 문자열 + 슬라이스된 3mf 최종 config

핵심 근거:

- H2S 0.4 인쇄 파라미터는 2.6.0 → 2.8.2.61 사이 **실질 변경 0 건** (205 diff 중 199 건이
  3 번째 익스트루더 변종 추가에 따른 배열 확장, idx0·1 동일). 도구가 쓰는 키 68 셀 CHANGED 0.
- 릴리스 노트의 "abnormal parameter values" 는 **2.8.1.55 에서 생겨 2.8.2.61 에서 복구된 회귀**다
  (`nozzle_volume ["32","32","32"]`, MVS idx2 오류). 2.6 은 겪은 적 없다. 자동 업그레이드였으면
  그 창(약 1 개월)에 올라탔다.
- issue #9166 근본 원인: `GCode.cpp` 의 timelapse 주입 조건에서 `!m_spiral_vase` 예외가
  **I3 구조에만** 걸려 있다. H2S 는 corexy + 단일 익스트루더라 else 분기로 빠져 매 레이어
  timelapse G-code 가 주입된다. `timelapse_type` 에 off 값이 없고 spiral 은 `0` 을 요구하므로
  **프로파일로 해결 불가** — 기기측 조치가 필요하다. 이슈는 열려 있다.
- spiral 은 조건 위반 레이어에서 **에러 없이** 일반(seam 있는) 출력으로 폴백한다
  (`GCode.cpp` per-layer 게이트).

## GAP 분석

- `spiral_mode_smooth` · `spiral_mode_max_xy_smoothing` 이 킷에 **전혀 없다**
- `seam_slope_min_length` 를 2026-08 superlube 는 "scarf 길이", 2026-09 opus-xero 는
  "최소 길이 필터" 로 썼다 — 상반된 해석 2 개 공존
- scarf 길이와 루프 둘레의 관계 규칙이 없다 (⌀10.19 둘레 32mm 에 8mm = 25% 적용 사례)
- `wall_sequence: inner-outer-inner` 를 `wall_loops: 2` 와 함께 내보낸 사례가 있다
- `bambu-fields-baseline.md` 의 `spiral_mode` 근거 라인 인용이 틀렸다 (277-282 는 WallSequence enum)
- 버전 앵커가 references 헤더에 하드코딩돼 있다

## 범위 경계

수정 대상은 `bambu-kit/skills/bambu-print-profile/` 하위로 한정한다.
**온도·팬 키는 이번에도 건드리지 않는다.**
기존 42 개 생성 번들은 재생성하지 않는다.
앱 자동 설치는 **구현하지 않는다** (사용자 선택: 감지 + 알림만).

커버리지 해소: SC-04 — `validate-plugin.py` 는 킷 전체를 검사하는 상위 명령이므로 킷 이름
하나로 측정한다.

## 회귀 게이트

`SC-01` ~ `SC-03` 이 결정론적 검증의 정본이다. 각 조건은 양성 대조(알려진 불량 입력에 FAIL)와
음성 대조(정상 입력에 PASS)를 **둘 다** 실행해 가드 생존을 증명한다.

## Skill

- [ ] SK-01: 회전체·원통 결정 트리가 `vase+smooth spiral` → `aligned/back + painted seam + 짧은 scarf` → `random(fallback)` 순서로 재작성되고, `random` 이 default top 이 아니다 [exact] (측정: `references/surface-recipes.md` §2.1 과 `references/seam-recipes.md` §0 에서 random 이 DEFAULT 로 표기된 행 0 건)
- [ ] SK-02: `spiral_mode`, `spiral_mode_smooth`, `spiral_mode_max_xy_smoothing` 3 키의 이름·타입·기본값·단위가 `references/bambu-fields-baseline.md` 에 표로 존재한다 [exact, enumerated] (측정: 3 키 각각 `grep -c` >= 1 이고 같은 표 행에 기본값이 있음)
- [ ] SK-03: H2S + Smooth Spiral 의 timelapse 경고가 명시되고, **프로파일로 해결 불가**이며 기기측 조치가 필요하다는 사실과 issue 번호가 적혀 있다 [exact] (측정: `9166` 문자열 1 건 이상 + "프로파일" 로 해결 불가 취지 문장 1 건 이상)
- [ ] SK-04: vase 가능 판정 체크리스트가 존재하고, **조건 위반 레이어에서 에러 없이 폴백**한다는 경고를 포함한다 [structural] (측정: 체크리스트 항목 5 개 이상 + 폴백 경고 1 건)
- [ ] SK-05: scarf 길이 상한 가드가 루프 둘레 대비 비율로 명시된다 [exact] (측정: 둘레 대비 % 상한과 mm 하한이 같은 문단에 존재)
- [ ] SK-06: `seam_slope_min_length` 의 의미가 킷 전체에서 "scarf 램프 길이" 하나로 통일되고, "최소 길이 필터" 취지 서술이 0 건이다 [exact, enumerated] (측정: `references/` 전체와 `SKILL.md` 에서 해당 키를 필터로 설명하는 문장 0 건)
- [ ] SK-07: 소재별 seam 전략 표가 재작성되어 PLA Basic · PLA Matte · PLA Silk · PLA-CF · PETG HF · PETG Basic · ABS · ASA · PC · PAHT-CF · PA6-CF · TPU 12 소재 각각에 1 순위 전략과 scarf 길이 권장이 있다 [exact, enumerated] (측정: 12 소재명 각각 표 행에 존재)
- [ ] SK-08: `wall_sequence` 가 `inner-outer-inner wall` 일 때 `wall_loops >= 3` 이 전제라는 사실이 명시되고, 미만이면 쓰지 말라고 적혀 있다 [exact] (측정: 해당 문장 1 건 이상)

## Script

- [ ] SC-01: 킷이 실행 시 설치된 앱 버전과 프로파일 번들 버전을 **실제로 읽어** 보고하는 결정론적 명령을 갖는다 [goal] (측정: 명령 실행 시 `02.06.00.51` 과 `02.06.00.05` 두 값이 출력) 음성 대조: 조회 경로를 잘못된 경로로 바꾸면 값 대신 실패가 보고된다
- [ ] SC-02: 소재 부모값이 상식 범위를 벗어난 **손상 프리셋을 탐지**하는 검사가 있다 [goal] (측정: `nozzle_volume` 을 `["32","32","32"]` 로 조작한 사본에 실행해 이상 보고, 정상값 `["145","148"]` 에 실행해 통과) 음성 대조: 검사 블록을 삭제하면 조작 사본이 통과한다
- [ ] SC-03: Phase 4.3 게이트가 scarf 길이와 루프 둘레의 비율을 검사하고 상한 초과 시 FAIL 한다 [goal] (측정: 둘레 32mm · scarf 8mm 입력에 FAIL, 둘레 32mm · scarf 3mm 입력에 PASS) 음성 대조: 검사 블록을 삭제하면 8mm 입력이 통과한다
- [ ] SC-04: `python3 scripts/validate-plugin.py bambu-kit` 가 exit 0 으로 통과한다 [goal] (측정: `echo $?` == 0)

## Error

- [ ] ER-01: 버전 조회에 실패했을 때의 동작이 정의되고, 추측값 사용을 금지한다 [structural] (측정: 실패 분기 문단 1 건 이상)
- [ ] ER-02: vase 가능 판정이 불확실할 때 조용히 spiral 을 켜지 않고 사용자에게 제시하는 경로가 명시된다 [structural] (측정: 해당 분기 1 건 이상)
- [ ] ER-03: 손상 프리셋이 탐지되면 프로파일 생성을 진행하지 않고 사용자에게 보고하는 경로가 명시된다 [structural] (측정: 해당 분기 1 건 이상)

## Architecture

- [ ] AR-01: `references/` 의 버전 앵커가 하드코딩 대신 런타임 조회를 가리킨다 [exact, enumerated] (측정: `bambu-fields-baseline.md` · `surface-recipes.md` · `seam-recipes.md` · `materials.md` · `failure-recipes.md` 5 파일 헤더에서 `Bambu Studio reference version` 행이 고정 버전 단독 표기가 아니라 런타임 조회 안내를 포함)
- [ ] AR-02: `references/bambu-fields-baseline.md` 의 `spiral_mode` 근거 라인 인용이 정정된다 [exact] (측정: `277-282` 인용 0 건)
- [ ] AR-03: `seam_gap` 이 실재하는 BambuStudio 키임과, **프로파일 JSON 에 없는 것이 키 부재를 뜻하지 않는다**는 사실이 명시된다 [exact] (측정: 해당 취지 문장 1 건 이상)
- [ ] AR-04: 변경 범위가 한정된다. Given: 계약 봉인 후 구현 완료 시점. `git status --porcelain -- bambu-kit/` 결과가 `bambu-kit/skills/bambu-print-profile/` 하위 8 개 이내이고 그 밖 경로 0 건이다 [exact, enumerated]

## Anti-patterns

- [ ] AP-03: bare code fence 금지 — 모든 코드 펜스에 언어 힌트가 있다
- [ ] AP-04: SKILL.md frontmatter 에 `name` 필드가 유지된다

## Reusability

- [ ] RE-01: 수치 정본을 `references/` 에 두고 `SKILL.md` 에 같은 수치를 중복 기재하지 않는다
- [ ] RE-02: 이미 존재하는 references 파일을 새로 만들지 않고 해당 섹션을 확장한다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0 개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0 개 (제외 없음)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0 개
- [ ] DG-04: `python3 scripts/sync-docs.py bambu-kit --check-only` 가 동기화됨으로 통과한다
