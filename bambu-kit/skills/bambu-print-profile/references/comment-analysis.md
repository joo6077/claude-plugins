# MakerWorld 댓글 분석 매뉴얼

> Last updated: 2026-05-23
> Added in: bambu-kit v0.4.0
> Trigger: SKILL.md Phase 1.6 (Comment Analysis) 진입 시 로드

스킬이 MakerWorld 모델 페이지의 댓글을 체계적으로 분석하여 **디자이너 명시 권장사항 + 사용자 실측 피드백**을 추출할 때 참조한다. 추출된 데이터는 Phase 2(소재 추천)/Phase 3(JSON 생성)/Phase 4(notes.md)에 강제 반영된다.

## 1. 분석 목적과 우선순위

1. **Designer Constraints 추출** — 디자이너가 댓글에서 명시한 권장/금지/필수 사항. surface-first 자동 모드보다 **상위 우선순위**.
2. **사용자 실측 피드백** — 실패 사례, 변형 사례, 성공 사진 등으로 process 결정 보정.
3. **안전/사용성 이슈** — 사용자가 제기한 위험, 디자이너 답변 여부.

> **자동 적용 원칙**: 디자이너 권장이 "no supports", "do not modify profile" 같은 명시적 제약을 포함하면 그 부분의 자동 카이젠/surface-first 모드는 **자동 적용하지 않는다**. 사용자에게 명시적 confirm 받아야 진행한다.

## 2. 4 카테고리 추출 매뉴얼

### designer_reply

디자이너 본인(@<creator_handle>)이 작성한 댓글 또는 답변. 권장사항/금지사항이 가장 중요.

**추출 패턴:**
- 작성자 handle이 모델 페이지의 author와 일치
- "designer", "author", "creator", "OP", "제작자" 같은 메타 라벨이 댓글에 붙어 있음
- "The designer has replied" 같은 UI 표식

**추출 항목:**
- 제약 사항 (do/don't, must/must not)
- 권장 소재 명시
- 권장 print profile (layer, wall, infill, support 등) 명시
- 출력 후 사용/조립 주의사항
- 사용자 안전 우려에 대한 답변

### user_success

사용자가 출력 성공을 보고한 댓글. 사진/이미지가 첨부된 경우가 많음.

**추출 패턴:**
- "Print Profile" 또는 "프로파일" 키워드 + 평점/이미지
- 출력 사진 첨부 + 별점 4-5점
- "이것으로 출력했더니" 같은 후기 표현

**추출 항목:**
- 사용한 소재 (PLA/PETG/ABS 등)
- 사용한 print profile (layer/walls/infill)
- 사용자 변형 (다른 색상, 다른 노즐, 다른 슬라이서)
- 출력 시간 보고

### user_failure

출력 실패/문제 보고 댓글. 자주 1-3점 평점.

**추출 패턴:**
- "doesn't work", "failed", "fail", "안 됨", "실패", "warping", "stringing", "broke", "crack"
- 별점 1-3점 + 본문이 문제 보고
- "Removing the support is hard", "Mechanism doesn't lock" 같은 사용성 보고

**추출 항목:**
- 실패 증상 (stringing, warping, dimensional fit, mechanism failure)
- 사용 환경 (프린터, 소재, 슬라이서)
- 디자이너 답변 유무
- 사용자 제안 보정 (다른 orientation, 다른 소재)

### user_variant

사용자가 디자인을 변형/응용한 보고.

**추출 패턴:**
- "I modified", "I changed", "remix", "변형", "수정해서", "scaled to"
- 다른 사이즈, 다른 소재로 재해석한 사례
- 다른 부품과의 조합 보고

**추출 항목:**
- 변형 내용 (사이즈/소재/구조)
- 변형 결과 (잘 됨/안 됨)
- 원본 대비 개선/악화

## 3. Designer Constraint 키워드 사전 (한/영/중)

MakerWorld는 다국어(영/중/한 등) 환경이므로 댓글 원문 언어에 따라 추출 키워드가 다르다. **Show original 버튼을 클릭하여 원문도 함께 확인**한다.

### 영어 (English)

| 카테고리 | 키워드 / 패턴 |
|---------|--------------|
| 금지 (강) | "no supports", "no support needed", "do not modify", "do not use", "must not", "never" |
| 권장 (강) | "must", "required", "always use", "highly recommend" |
| 권장 (약) | "recommend", "suggested", "preferred", "should" |
| 주의 | "be careful", "watch out", "warning", "caution" |

### 한국어

| 카테고리 | 키워드 / 패턴 |
|---------|--------------|
| 금지 (강) | "금지", "사용하지 마", "절대 안 됨", "쓰면 안 돼" |
| 권장 (강) | "필수", "반드시", "꼭" |
| 권장 (약) | "권장", "추천", "좋아" |
| 주의 | "주의", "조심", "유의" |

### 중국어 (简体/繁體)

MakerWorld 중국발 모델 비율이 높음 — 디자이너 원문이 중국어인 경우 많음.

| 카테고리 | 키워드 / 패턴 |
|---------|--------------|
| 금지 (강) | "请不要" (please don't), "禁止" (forbidden), "不要修改" (do not modify), "不可" (must not) |
| 권장 (강) | "必须" (must), "需要" (need/required), "一定要" (must) |
| 권장 (약) | "建议" (recommend), "推荐" (recommend), "可以" (can) |
| 주의 | "注意" (caution), "小心" (careful) |

### Grep 가능 형태 (전체 키워드 평면 리스트)

스킬에서 grep으로 추출할 때 다음 키워드를 패턴으로 사용:

```text
no supports
do not modify
must
권장
금지
필수
请不要
需要
```

**최소 보장 키워드 8개** — DC-02 조건 기준. 신규 케이스에서 추가 발견 시 이 섹션에 append.

## 4. 운영 가이드

### 4.1 댓글 50+ 페이지 처리 (페이지네이션/스크롤)

MakerWorld 댓글은 lazy loading + "Newest First / Most Likes / Most Replies" 정렬 옵션이 있다.

**전략:**

1. **첫 스냅샷**: `mcp__playwright__browser_snapshot` 호출 후 댓글 카운트 헤딩 확인
   ```yaml
   - heading "Comment & Rating (N)"
   ```
2. **N ≤ 20**: 단일 스냅샷으로 충분.
3. **20 < N ≤ 50**: `browser_evaluate`로 `window.scrollBy(0, 2000)` 3-5회 호출 후 재스냅샷.
4. **N > 50**:
   - `Top` 정렬로 핵심 댓글 추출 (designer_reply, 평점 분포 sample)
   - `Most Likes`로 검증된 user_success/user_failure 추출
   - `Newest First`로 최근 issue 추출
   - 전체 enumerate는 token 비용 ↑ — sampling 전략 사용 (designer_reply 100% + 평점 분포 + 텍스트 댓글 30+).
5. **사용자에게 보고**: "댓글 N개 발견 → 분석 대상 M개 (sampling 적용 여부 명시)"

### 4.2 댓글 안 외부 링크 follow

댓글 본문에 외부 URL이 포함된 경우 (예: GitHub fork, Thingiverse 변형, 사용자 블로그 후기) → "Further Research" 분기.

**자동 follow 조건:**
- 같은 모델의 다른 호스팅 (printables/thingiverse): 매뉴얼/추가 STL 가능성 → fetch
- GitHub repo: README/CHANGELOG fetch (raw.githubusercontent.com)
- YouTube/Bilibili: Codex 위임 (transcript), fail-soft

**skip 조건:**
- SNS 링크 (Twitter/Instagram): cosmetic, skip
- 짧은 URL shortener (bit.ly/tinyurl): 위험, skip
- Affiliate (amazon/aliexpress affiliate ID): 부품 BOM 아닌 한 skip

### 4.3 댓글 안 이미지/사진 visual 검토

사용자가 출력 결과 사진을 댓글에 첨부한 경우.

**전략:**
1. `mcp__playwright__browser_take_screenshot`으로 댓글 영역 캡처 (full comment block)
2. 이미지에서 다음 단서 추출:
   - **표면 품질**: 광택/매트/stringing 흔적
   - **색상 변형**: 멀티컬러 패턴
   - **조립 상태**: 일부 부품 누락 또는 추가
   - **사용 환경**: 책상/벽/실외 (소재 적합성 판단)
3. **OCR 불필요** — 시각 패턴만 보면 됨. 텍스트 댓글이 별도로 추출되므로.
4. **fail-soft**: 이미지 로딩 실패 시 skip, notes.md §5에 "댓글 사진 일부 미확인" 명시.

## 5. notes.md 통합 매뉴얼

추출 결과를 notes.md 5섹션 표준 템플릿에 어떻게 통합하는지:

### 5.1 §1 "필라멘트 요구사항"

- **§1.1 추천 소재**에 디자이너 명시 권장 소재 우선 표기 (creator가 댓글에서 "PETG만 쓰세요" 했으면 1등급)
- **§1.2 출력 설정**에 디자이너 명시 layer/wall/infill 값 우선 표기 + "Creator 명시 — 수정 X" 주석

### 5.2 §3 "조립 워크플로우"

- **§3.0 디자이너 명시 권장사항** (신규 서브섹션) — 추출된 designer_reply 전체를 enumerate
  - support 사용 여부
  - profile 수정 가능 여부
  - 안전 주의사항 (사용성 limitation 포함)

### 5.3 §5 "License + Credits"

- **댓글 분석 출처** — comments-raw.md 파일 경로 명시
- 핵심 designer_reply quote (1-3줄)
- 평점 분포 요약 (5점 N개 / 4점 N개 / ... / 1점 N개)

## 6. comments-raw.md 아카이브 포맷

원본 보존용. MakerWorld 페이지가 미래에 수정/삭제될 수 있어 reproducibility 확보.

```markdown
# <모델명> — Comments Archive (raw)

**Source URL:** <MakerWorld URL>
**Fetched:** <YYYY-MM-DD HH:MM>
**Total comments:** N
**Sampled:** M (sampling strategy: ...)

---

## designer_reply (X개)

### [2025-07-22 11:11] @<creator_handle>
> No supports needed, please do not modify the print profile. Push-lock means it must be held down.

(이런 형태로 quote-block로 보존)

---

## user_success (Y개)
...

## user_failure (Z개)
...

## user_variant (W개)
...
```

## 7. Fail-soft 정책

다음 케이스는 fail-soft (skip + 보고 + 진행):

- Cloudflare bot challenge로 페이지 로드 실패 → MakerWorld URL fallback 체인 작동 (Playwright → Codex → WebFetch → 사용자 직접 입력)
- 댓글 0개 모델 → "댓글 없음" 명시 후 Phase 2 진행 (designer_constraints는 description 본문에서만 추출)
- 다국어 번역 결과 부정확 → 원문 quote 함께 보존
- 외부 링크 follow 실패 → notes.md §5에 URL만 적고 진행

## 8. v0.4.0 도입 동기 (dogfood)

2026-05-23 9mm Craft Knife Elite 케이스에서 발견된 회귀:
- 디자이너 댓글에 "No supports needed, please do not modify the print profile" 명시
- v0.3.0은 댓글에서 이 권장을 추출하지 못함
- surface-first 모드가 자동 적용되어 layer 0.1→0.12 / walls 2→3 / ironing 추가 / infill 15→18 등 profile을 대폭 수정
- 사용자 피드백: "넌 서포트 넣엇더라" + "댓글이나 피드백 참고 안 하더라"

→ Phase 1.6 + Designer Constraint Override Rule + comments-raw.md 아카이브 신규 도입.

## 9. 미해결 / 검증 필요

- MakerWorld API endpoint (있다면) 직접 호출로 댓글 전체를 단일 호출에 받을 수 있는지 검증 (v2 BACKLOG)
- 다국어 자동 번역 품질 — Show original 클릭 자동화 검증 필요
- 50+ 댓글 페이지 sampling 전략의 reproducibility (random seed 영향)
- 이미지 OCR 도입 가치 평가 — 현재는 visual 검토만 (text는 댓글 본문에서 추출)
