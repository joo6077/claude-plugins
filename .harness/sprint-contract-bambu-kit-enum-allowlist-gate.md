---
feature: "bambu-kit enum 오염 수정 + Phase 4.3 allowlist 게이트"
slug: bambu-kit-enum-allowlist-gate
created: "2026-09-06 11:35"
complexity: "복잡"
conditions: 22
status: done
owner_session: 44c7700e-f565-4643-8410-e162aa7d93d5
conditions_digest: sha256:504aad0be7af3d5b
locked_at: "2026-09-06 11:34"
---

## 배경

bambu-kit 이 처방하는 `ironing_type` 값 3 종(`topmost_only` · `top_surfaces` · `all_solid`)과
`top_surface_pattern` 값 2 종(`archimedean` · `hilbert`)은 **OrcaSlicer 이름이고 Bambu Studio 에는
없다.** 설치본 `02.08.02.61` 바이너리 + 시스템/user 프로파일 실측으로 확인한 Bambu 실제 값은
`ironing_type` = `no ironing` · `top` · `topmost` · `solid`,
`top_surface_pattern` = `monotonic` · `monotonicline` · `concentric` · `archimedeanchords` ·
`hilbertcurve` 등이다.

근본 원인은 `references/bambu-fields-baseline.md:182` 가 **Orca wiki 를 출처로 인용**한 것이다.

영향: Bambu 는 알 수 없는 enum 값을 조용히 무시한다. 따라서 표면 마감이 통째로 빠진 채
"적용했다" 고 보고된다. Phase 4.3 게이트는 `FORBIDDEN` **blocklist** 만 갖고 있어
(`SKILL.md:1173-1180`) 값 오염을 검출하지 못한다 — blocklist 는 미지의 값을 못 잡는다.

발견 경위: 2026-09-06 DG-04 완주 실행 중, 직전 세션 생성물이 `topmost` 를 쓴 것을 보고
references 와 다르다고 의심했다가 실측 결과 **생성물이 맞고 references 가 틀렸다.**

## 범위 경계

- 소스 4 파일 + 파생 HTML 2 파일 = 6 파일. 그 밖 경로 0 건.
- 이번 스프린트는 **enum 값 정합성 + 게이트 확장**만 다룬다. ironing 정책 자체(어느 소재에
  ironing 을 권장하는가)는 바꾸지 않는다 — 값 이름만 교정한다.
- 기존 생성 preset 소비면 조사 결과: user preset 10 건이 전부 `topmost`/`top` 정상값이므로
  **소비면 파손 없음**. 재생성 대상 0 건.
- 동시 실행 중인 다른 세션이 이 레포의 죽은 URL 을 일괄 교정 중이다. 그 세션의 대상 8 URL 은
  본 계약 대상 6 파일에 0 건으로 확인했다.
- 커버리지 해소: SK-03 — 6 키를 조건 산문과 측정 절에 동일 백틱 표기로 열거했다.
- 커버리지 해소: AR-01 — `docs/bambu-kit/` 2 파일을 측정 절에 개별 경로로 열거했다.

## Skill

- [ ] SK-01: `bambu-kit/` 소스에서 Orca ironing 이름 3 종 `topmost_only` · `top_surfaces` · `all_solid` 이 각각 0 건이다 [exact, enumerated] (측정: 3 값 각각 `grep -rc '<값>' bambu-kit/` 합계 == 0)
- [ ] SK-02: `bambu-kit/` 소스에서 Orca infill 이름 2 종이 단어 경계 기준 0 건이고, Bambu 값 `archimedeanchords` · `hilbertcurve` 로 대체돼 있다 [exact, enumerated] (측정: `grep -rEc '\barchimedean\b|\bhilbert\b' bambu-kit/` == 0 이고 `grep -rc 'archimedeanchords' bambu-kit/` >= 1, `grep -rc 'hilbertcurve' bambu-kit/` >= 1)
- [ ] SK-03: Phase 4.3 게이트가 enum allowlist 검사를 수행하며 `ironing_type` · `top_surface_pattern` · `seam_position` · `seam_slope_type` · `wall_sequence` · `brim_type` 6 키를 검사 대상으로 갖는다 [exact, enumerated] (측정: `SKILL.md` 의 Phase 4.3 코드 블록 안에서 6 키 각각 `grep -c` >= 1, 그리고 allowlist 자료구조 식별자가 1 건 이상 존재)
- [ ] SK-04: Gotcha 체크리스트에 enum allowlist 위반을 막는 항목이 1 건 이상 추가돼 있다 [structural] (측정: `## Gotcha 체크리스트` 섹션 내 `enum` 언급 줄 >= 1)

## Script

- [ ] SC-01: 게이트가 `ironing_type` 이 `"topmost_only"` 인 process JSON 에 대해 `RESULT: FAIL` 을 출력하고 exit 1 한다 [goal] (측정: 픽스처 생성 후 게이트 실행, 출력과 `echo $?` 인용) 음성 대조: allowlist 검사 블록을 삭제하면 같은 픽스처가 `RESULT: PASS` 로 통과한다
- [ ] SC-02: 게이트가 `ironing_type` 이 `"topmost"` 인 정상 process JSON 에 대해 `RESULT: PASS` 를 출력하고 exit 0 한다 [goal] (측정: 이번 세션이 생성한 `H2S Superlube Box+Lid - PETG HF 0.12mm v2.json` 으로 실행, 출력과 `echo $?` 인용) 음성 대조: allowlist 값 목록에서 `topmost` 를 빼면 같은 파일이 FAIL 한다
- [ ] SC-03: enum 키가 아예 없는 process JSON 은 FAIL 하지 않는다 (미설정 = 부모 상속이며 정상) [goal] (측정: `H2S Superlube Tips - PETG HF 0.12mm v2.json` 은 `top_surface_pattern` 미설정 — 게이트 실행 시 PASS) 음성 대조: 미설정을 FAIL 로 처리하면 이 파일이 FAIL 한다
- [ ] SC-04: `python3 scripts/validate-plugin.py bambu-kit` 가 exit 0 으로 통과한다 [goal] (측정: 명령 실행 후 `echo $?` == 0)

## Error

- [ ] ER-01: 잘못된 enum 값에 대한 FAIL 메시지가 (a) 키 이름 (b) 발견된 잘못된 값 (c) 허용값 전체 목록 3 요소를 모두 포함한다 [exact, enumerated] (측정: SC-01 실행 출력 1 줄에서 3 요소 각각 존재 확인)
- [ ] ER-02: allowlist 의 출처가 추측이 아니라 설치본 실측임이 명시되고, 그 Bambu Studio 버전이 함께 적혀 있다 [structural] (측정: allowlist 정의 근처 주석 또는 references 에 버전 문자열 `02.08.02.61` 1 건 이상)

## Architecture

- [ ] AR-01: 파생 발행물이 소스와 동기화된다 — `docs/bambu-kit/surface-recipes.html` 과 `docs/bambu-kit/bambu-fields-baseline.html` 두 파일에서 Orca 이름 3 종이 0 건이다 [exact, enumerated] (측정: 두 경로 각각 `grep -c 'topmost_only\|top_surfaces\|all_solid'` == 0)
- [ ] AR-02: `references/bambu-fields-baseline.md` 의 `ironing_type` 행 출처가 Orca wiki 단독이 아니며 Bambu 1 차 근거(시스템 프로파일 경로 또는 설치본)를 포함한다 [exact] (측정: 해당 행에 `fdm_process_common.json` 또는 `02.08.02.61` 문자열 존재 + 그 행이 Bambu 실제 enum 4 값을 적고 있다)
- [ ] AR-03: 변경 범위가 한정된다. Given: 계약 봉인 후 구현 완료 시점, 아직 커밋하지 않은 상태. `git diff --name-only -- bambu-kit/ docs/bambu-kit/` 결과가 6 개 이내이고 그 밖 경로 0 건이다 [exact, enumerated] (측정: 해당 명령 출력 전체를 인용. baseline: 계약 작성 시점 이 명령 출력 0 파일)

## Anti-patterns

- [ ] AP-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다
- [ ] AP-03: bare code fence 금지 — validate-plugin V6 FAIL (언어 힌트 필수: ```text, ```bash, ```yaml 등)
- [ ] AP-04: SKILL.md / agents/*.md frontmatter 에서 name 필드 누락 — validate-plugin V1 FAIL

## Reusability

- [ ] RE-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] RE-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] DG-01: `bash -n scripts/release.sh` 워닝 0개 (변경/생성 파일 대상)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (제외 없음)
- [ ] DG-03: `bash scripts/release.sh 2>&1 || true` 콘솔 로그에 에러/예외 0개
- [ ] DG-04: 수정된 게이트를 실제 1 회 실행해 정상 프로파일에 PASS, 오염 프로파일에 FAIL 판정이 나온다
