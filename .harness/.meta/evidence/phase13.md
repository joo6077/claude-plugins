---
phase: 13
title: "Phase 13 bambu-kit — 확보된 외부 근거"
collected: 2026-09-24
method: codex (foreground, 직접 호출 · gpt-5.6-sol · 조회는 curl/gh)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 13 행 · phase-research-templates.md Phase 13 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

## 1. 출처 목록

실제로 조회한 출처만 적었다.

1. Bambu Studio 공식 소스

   - [`PrintConfig.cpp` master](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)
   - [`PrintConfig.cpp` v02.08.02.61](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintConfig.cpp)
   - [`PrintObjectSlice.cpp` master](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintObjectSlice.cpp)
   - [`PrintObjectSlice.cpp` v02.08.02.61](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/PrintObjectSlice.cpp)

2. 공식 릴리스

   - [Bambu Studio Releases API](https://api.github.com/repos/bambulab/BambuStudio/releases)
   - [Bambu Studio v02.08.02.60](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.02.60)
   - [Bambu Studio v02.08.02.61](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.02.61)
   - [Bambu Studio v02.08.03.66 beta](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.03.66)
   - [Bambu Studio v02.08.04.57 beta](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.04.57)
   - [OrcaSlicer v2.4.2](https://github.com/OrcaSlicer/OrcaSlicer/releases/tag/v2.4.2)

3. OrcaSlicer 정밀도 문서

   - [OrcaSlicer Wiki 저장소의 precision 문서](https://github.com/OrcaSlicer/OrcaSlicer_WIKI/blob/main/print_settings/quality/quality_settings_precision.md)

4. 3MF 공식 규격

   - [3MF Core Specification v1.4.0 릴리스](https://github.com/3MFConsortium/spec_core/releases/tag/1.4.0)
   - [3MF Core Specification v1.4.0 본문](https://github.com/3MFConsortium/spec_core/blob/1.4.0/3MF%20Core%20Specification.md)

5. MakerWorld API 관측 — 공개 공식 문서가 아니라 **[관측 2026-09-24]**

   - [design/1186414](https://makerworld.com/api/v1/design-service/design/1186414)
   - [commentandrating, offset 0](https://api.bambulab.com/v1/comment-service/commentandrating?designId=1186414&offset=0&limit=100)
   - [commentandrating, offset 100](https://api.bambulab.com/v1/comment-service/commentandrating?designId=1186414&offset=100&limit=100)
   - [instances](https://api.bambulab.com/v1/design-service/design/1186414/instances)

---

## 2. 항목별 관찰 사실

### bambu:P1 — MakerWorld 읽는 순서

**[관측 2026-09-24]** 모델 `1186414`로 세 JSON 주소를 셸 `curl`로 호출했으며 모두 HTTP 200이었다.

- `design/<id>` 응답에는 실제로 `title`, HTML인 `summary`, `designCreator`, `instances`, `commentCount`, `license`가 있었다.
- 같은 응답의 `instances`에는 프로파일별 `title`, `summary`, 호환 기기와 plate/project 설정 등이 포함됐다.
- 별도 `/instances` 응답은 `total: 4`와 `hits` 배열을 반환했다.
- 댓글 API는 `total: 159`, `hits` 배열을 반환했다.

따라서 **JSON → 선택적 브라우저 → 사용자 입력** 순서는 이번 관측에 부합한다. 현재의 브라우저 우선 순서에 유리한 외부 근거는 찾지 못했다.

반대 근거/제약:

- 이 API들의 공개 공식 문서나 안정성 계약은 찾지 못했다. 필드와 경로 모두 `[관측 2026-09-24]`로 한정해야 한다.
- `design.commentCount`는 `190`, 댓글 API `total`은 `159`였다. 둘은 같은 의미의 수치라고 간주하면 안 된다. 추론: 전자는 답글 등을 포함한 표시용 총계일 가능성이 있지만, 그 의미를 설명하는 공식 근거는 찾지 못했다.

### bambu:P2 — 브라우저는 조건부, 실패 시 즉시 다음 단계

현재 [SKILL.md:63](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/SKILL.md:63)과 [SKILL.md:2099](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/SKILL.md:2099)은 특정 `mcp__playwright__...` 이름을 박고 브라우저를 1순위로 둔다.

이번 관측에서는 인증 없는 JSON 요청만으로 본문·제작자·프로파일·댓글을 읽었다. 따라서 특정 MCP 서버명을 계약에 넣을 필요가 없고, 브라우저는 JSON에 없는 렌더링 정보나 이미지를 보충하는 단계로 내리는 것이 타당하다.

`Just a moment...` 또는 HTTP 403에서 기다리지 말라는 동작을 직접 뒷받침하는 공식 MakerWorld 문서는 찾지 못했다. 이는 재시도 정책에 관한 운영 규칙으로 표시해야 한다.

“Cloudflare 우회” 표현은 삭제가 적절하다. 실제 우회 능력을 보장하는 1차 출처를 찾지 못했고, 현재 문구는 [comment-analysis.md:318](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/references/comment-analysis.md:318)에도 중복된다.

### bambu:P3 — Codex에는 브라우저 대신 셸 `curl`

**[관측 2026-09-24]** 같은 환경에서 셸 `curl`로 세 API가 모두 200이었다. 따라서 Codex 경로에 정확한 URL과 `curl` 우선 실행을 적는 것은 재현 가능한 계약 조건이다.

반대로 현재 [SKILL.md:2100](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/SKILL.md:2100)은 “캐시/웹검색 또는 우회 정보”에 기대며 API 주소를 주지 않는다. 관측된 직접 경로보다 약하다.

### bambu:P4 — 모두 실패하면 사용자 입력, 3MF는 사용자에게 요청

JSON·선택적 브라우저·셸 `curl`이 모두 실패했을 때 사용자에게 핵심 정보를 묻는 fail-soft는 합리적이다.

다만 “3MF 다운로드는 로그인이 필요하다”는 사실은 이번 조회에서 다운로드 요청까지 검증하지 않았다. 이번 근거로 확정할 수 있는 표현은 다음 정도다.

- 자동 다운로드 성공을 가정하지 않는다.
- 다운로드가 인증을 요구하거나 실패하면 재시도 루프 대신 사용자가 받은 `.3mf`를 요청한다.

### bambu:P5 — 댓글 수 확인과 칸마다 읽기

**[관측 2026-09-24]** 댓글 API 페이지네이션 결과:

| offset | total | hits | 최상위 comment | ratingItem | 중첩 comment replies | rating replies |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 159 | 100 | 44 | 56 | 24 | 3 |
| 100 | 159 | 59 | 0 | 59 | 0 | 0 |
| 159 | 159 | 0 | 0 | 0 | 0 | 0 |

관찰로 확인되는 계약:

- `offset += len(hits)`로 진행한다.
- `hits`가 비거나 누적 hit 수가 `total`에 도달하면 끝낸다.
- 각 `hit`에서 `comment`와 `ratingItem`을 각각 확인해야 한다. 한 종류만 읽으면 일부를 잃는다.
- 각 항목의 답글 배열도 별도로 읽어야 한다.
- `design.commentCount`와 댓글 API `total`이 다르면 오류로 중단하기보다 두 값을 함께 기록하고 불일치를 보고한다.

현재 [SKILL.md:381-386](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/SKILL.md:381)과 [comment-analysis.md:137-148](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/references/comment-analysis.md:137)은 UI 헤딩·스크롤·50개 초과 sampling을 사용한다. API가 200인 경우에는 전수 페이지네이션이 가능하므로 이 규칙은 1차 경로로는 낡았다.

### bambu:P6 — 형상 측정에 정답을 아는 입력 추가

3MF Core 1.4.0은 다음을 규정한다.

- `<model>`은 `<resources>`와 `<build>`를 가져야 한다.
- 실제 출력 대상은 `<build><item objectid=...>`가 참조하는 객체다.
- item/component transform은 출력 전에 적용해야 한다.
- mesh는 vertices와 triangles로 구성된다.
- model의 기본 단위는 millimeter다.  
  [3MF Core 1.4.0](https://github.com/3MFConsortium/spec_core/blob/1.4.0/3MF%20Core%20Specification.md)

따라서 테스트용 3MF를 파이썬 몇 줄로 생성하는 방식은 표준 구조와 맞는다. 별도 이진 fixture를 커밋할 필요는 없다.

현재 알고리즘에 대한 기대값도 산술적으로 맞는다.

- 10 mm 정육면체 단면: 한 루프, 둘레 `4×10 = 40 mm`; 30 mm 미만 루프 비율 0 → `planar`.
- 2 mm 정사각 기둥 단면: 둘레 `4×2 = 8 mm`; 30 mm 미만 비율 1 → `thin`.
- 1 mm 벽 사각 관, `WALL_LOOPS=2`: 현재 식은 `0.42×2 + 0.45×2×(2−1) = 1.74 mm`; 1 mm는 예산보다 좁으므로 부족 비율 `1.0`, 최소 살 `1.0 mm`.

추론: 이 세 입력은 단일 루프 분류와 이중 루프 거리 측정을 함께 고정하므로, 실제 모델만 재는 것보다 회귀 검출력이 높다. 결과가 다르면 실측을 계속하지 않고 probe 자체를 먼저 고치는 stop gate가 적절하다.

---

## 3. 현행화 — 낡은 곳

| 파일:줄 | 현재 값 | 최신 확인값 | 판정·출처 |
|---|---|---|---|
| [bambu-fields-baseline.md:3](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md:3) | Last updated `2026-05-15` | 2026-09-24 조사 필요 상태 | 메타데이터가 실제 9월 검증 내용보다 낡음 |
| [bambu-fields-baseline.md:10](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md:10) | 최신 beta `2.7.0` | 최신 공개 항목은 `2.8.4.57 beta`(2026-09-22) | [릴리스 API](https://api.github.com/repos/bambulab/BambuStudio/releases), [2.8.4.57](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.04.57) |
| [bambu-fields-baseline.md:16-17](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md:16) | 안정판 `2.6.0.51` | 최신 안정판 `2.8.2.61`, 2026-08-21 | [2.8.2.61](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.02.61) |
| [bambu-fields-baseline.md:250](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/references/bambu-fields-baseline.md:250) | “master는 2.6.0 이후 142 commits” | 고정 숫자는 더 이상 현행 근거가 아님 | 안정 태그가 이미 2.8.2.61이며 master에는 이후 변경이 있음. 태그↔master 비교 절차만 남기는 편이 안전 |
| [materials.md:140](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/references/materials.md:140) | PLA Pure는 2.7 beta뿐, 2.6 stable 미포함이므로 보류 | 2.8.2.61 안정 태그에 `Bambu PLA Pure @BBL H2S.json` 및 H2S 노즐별 프로파일 존재 | [v02.08.02.61 프로파일 트리](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/filament) |
| [materials.md:152](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/references/materials.md:152) | 로컬 `02.06.00.51`만 출처로 기재 | 안정판 `02.08.02.61` | [2.8.2.61](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.02.61) |
| [comment-analysis.md:335](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/references/comment-analysis.md:335) | API endpoint 존재 여부 미해결 | 세 API 모두 200, 댓글 페이지네이션도 확인 | 위 MakerWorld 관측 URL |
| [SKILL.md:63](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/SKILL.md:63) | Playwright 1차·고정 서버명·“Cloudflare 우회” | JSON `curl` 1차가 관측상 작동 | MakerWorld 관측 URL |
| [SKILL.md:381-386](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/SKILL.md:381) | UI 헤딩 댓글 수, 50+ sampling | API `total`과 offset 전수 순회 가능 | commentandrating 관측 |
| [SKILL.md:2097-2104](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/SKILL.md:2097) | Playwright → Codex → WebFetch → 사용자 | JSON curl → 선택적 브라우저 → Codex 셸 curl → 사용자 | MakerWorld 관측 URL |

현행 버전 중 낡지 않은 곳:

- `option-keys/bambu-02.08.02.61.tsv`는 최신 안정 Bambu 버전과 일치한다.
- `option-keys/orca-2.4.2.tsv`는 최신 안정 OrcaSlicer `2.4.2`와 일치한다.
- 3MF Core 최신 공개 릴리스는 `1.4.0`이며, 이번 파서의 기본 구조 전제와 충돌하지 않는다.
- README의 `Bambu Studio v2.6.0+`, `OrcaSlicer v2.4+`는 지원 하한 표현이므로 그 자체로 낡았다고 단정할 수 없다.

폐기·깨지는 변경 점검:

- 조회한 최신 안정판 릴리스 노트에서는 명시적인 deprecated 또는 breaking 선언을 찾지 못했다.
- Bambu 2.8.2.60은 프로파일·프리셋 변경이 있고, 2.8.2.61은 H-series 프리셋의 비정상 값을 수정했다. 따라서 소스의 generic default만으로 실제 H2S 기본값을 대체하면 안 된다. [2.8.2.60](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.02.60), [2.8.2.61](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.02.61)
- 최신 beta 2.8.3/2.8.4는 새 line-width·ironing·sub-top 설정을 추가하고, beta가 저장한 3MF는 MakerWorld 업로드를 지원하지 않는다고 명시한다. 안정판 계약에는 아직 섞지 않는 편이 안전하다. [2.8.3.66](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.03.66), [2.8.4.57](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.04.57)
- master에는 색칠된 멀티소재 모델에서 filament shrink compensation을 건너뛰는 로직이 안정 태그보다 추가돼 있다. 추론: 다음 안정판으로 기준을 올릴 때 공차 회귀 항목으로 재검증해야 한다. [`PrintObjectSlice.cpp` master](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintObjectSlice.cpp)

---

## 4. 권장안

Phase 13 계약 조건으로 다음을 권장한다.

1. MakerWorld URL의 숫자 ID를 뽑아 세 JSON 주소를 정해진 순서로 `curl`한다. 각 응답이 200일 때만 읽고, 아니면 즉시 다음 단계로 간다.

2. 댓글은 `total`만 믿고 한 번 읽지 않는다. `hits`의 모든 원소에서 `comment`, `ratingItem`, 각각의 답글 배열을 칸마다 읽고 offset을 끝까지 넘긴다. `design.commentCount`와 댓글 API `total`은 별도 값으로 기록한다.

3. 브라우저 도구는 실제 도구 목록에서 발견될 때만 사용한다. 서버명을 문서에 고정하지 않는다. 제목이 `Just a moment...`이거나 403이면 재대기 없이 다음 fallback으로 간다.

4. Codex 위임문에는 “브라우저로 열어라”가 아니라 세 API URL을 셸 `curl`로 호출하라고 명시한다.

5. 최종 fallback은 사용자 입력이다. 3MF 자동 다운로드가 인증 실패하면 사용자가 내려받은 파일을 요청한다.

6. [SKILL.md:336](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/SKILL.md:336) 코드 블록 직후, 현재 실측 문단 [SKILL.md:339](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/release-0924/bambu-kit/skills/bambu-print-profile/SKILL.md:339) 앞에 self-test를 둔다.

7. self-test는 실행 시 임시 3MF 세 개를 생성하고 종료 시 지우는 파이썬으로 제공한다. 저장소에는 이진 fixture를 추가하지 않는다. 세 기대값 중 하나라도 다르면 non-zero로 멈추고 실제 모델 측정을 실행하지 않는다.

8. 버전 계약은 안정판 기준으로 `Bambu 2.8.2.61`, `Orca 2.4.2`, `3MF Core 1.4.0`을 기록하되, beta/master 내용은 “차기 재검증 후보”로 분리한다.

---

## 5. 못 가져온 것 / 열린 질문

- MakerWorld 세 API의 공개 공식 스키마·안정성·rate-limit 문서는 찾지 못했다. 모두 `[관측 2026-09-24]`로 표시해야 한다.
- `design.commentCount=190`과 댓글 API `total=159`가 각각 무엇을 세는지 설명하는 공식 근거를 찾지 못했다.
- MakerWorld 3MF 다운로드의 인증 요구를 이번 조사에서 직접 검증하지 못했다.
- 403 또는 `Just a moment...` 이후 재시도를 금지한다는 MakerWorld 공식 지침은 찾지 못했다.
- Orca 위키의 사용자 제시 URL은 직접 raw 조회 시 404였고, 실제 문서는 별도 `OrcaSlicer_WIKI` 저장소에서 확인했다. 내용은 존재하지만 원래 URL의 redirect/별칭 안정성은 확인하지 못했다.
- 가짜 3MF self-test는 읽기 전용 제약 때문에 실제 파일을 생성·실행하지 않았다. 기대값은 현재 probe 코드와 3MF 규격을 대조한 산술 검증이다.
