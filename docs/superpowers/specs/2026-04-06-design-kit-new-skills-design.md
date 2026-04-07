# design-kit 신규 스킬 3종 설계

## 개요

design-kit 플러그인에 3개 스킬을 추가한다. 기존 스킬(design-system, design-guide, design-audit)이 "토큰 세팅 → 개발 중 피드백 → 완성 후 감사" 흐름이라면, 신규 스킬은 그 앞단과 사이를 채운다: "컨셉 정의 → 화면 시안 → 컴포넌트 정의".

3개 스킬은 독립 호출 가능하며, 이전 단계 산출물이 프로젝트에 있으면 자동으로 읽어서 반영한다.

## 전체 흐름

```
design-concept ──→ design-system(기존) ──→ design-mockup ──→ design-component
     ↑                                          ↑                    ↑
  단독 호출 가능                          단독 호출 가능        단독 호출 가능
```

각 스킬은 파이프라인 강제 없이 독립 운영된다. 이전 단계 산출물(`.design/concept.md`, 디자인 토큰, 확정 시안)이 프로젝트에 존재하면 자동 로드하여 일관성을 유지한다.

---

## 1. design-concept — 디자인 컨셉 정의

### 목적

프로젝트의 디자인 방향성(무드, 컬러 방향, 타이포 방향, UI 패턴)을 정의하고 비주얼 무드보드로 시각화한다. design-system의 상위 레이어이자 입력값 역할.

### 트리거 키워드

"디자인 컨셉", "무드보드", "컨셉 잡아줘", "design concept", "디자인 방향", "톤앤매너", "무드 정의"

### 입력 (3가지 경로)

- **키워드/분위기 설명**: "미니멀하고 따뜻한 SaaS 대시보드"
- **레퍼런스 URL**: 분석해서 컨셉 추출
- **둘 다 + 자체 리서치**: 웹에서 관련 레퍼런스 사이트/트렌드를 조사하고 조합

### 프로세스

0. 기존 컨셉 감지 — `.design/concept.md`가 존재하면 로드하여 수정/확장 모드로 진입. 없으면 신규 생성 모드.
1. 사용자 입력 분석 (키워드, 레퍼런스, 프로젝트 맥락)
2. 웹 리서치 — 관련 디자인 레퍼런스/트렌드 조사 (WebSearch, Codex 활용)
3. 컨셉 요소 도출: 무드 키워드, 컬러 방향, 타이포 방향, UI 패턴 스타일
4. 컨셉 문서 생성/갱신 (`.design/concept.md`)
5. 비주얼 무드보드 HTML 생성 (브라우저에서 컬러/타이포/레이아웃 방향 확인)
6. 사용자 피드백 → 수정 반복 → 확정
7. 확정 시 `/design-system` 다음 단계로 안내

### 아웃풋

- **컨셉 문서** (`.design/concept.md`): 무드 키워드, 컬러 방향, 타이포 방향, UI 패턴, 레퍼런스 목록
- **비주얼 무드보드 HTML**: 컬러 팔레트 방향, 타이포 샘플, 레이아웃 패턴을 시각화한 페이지

### References

- `references/concept-criteria.md` — 컨셉 도출 기준 (무드 키워드 분류, 컬러 방향 체계, 타이포 선택 기준, UI 패턴 카테고리). `docs/design/` 리서치 문서 중 참조 대상: foundations/color.md, foundations/typography.md, foundations/authentic-design.md, systems/*.md

### 원칙

- 스택 무관 — 구현 코드 없음, 방향과 원칙만 정의
- design-kit의 `docs/design/` 리서치 문서를 근거로 제안
- 자체 리서치 결과는 출처와 함께 제시

---

## 2. design-mockup — 화면 시안 생성

### 목적

특정 화면 요청 시 하이파이 HTML 시안 5개를 생성하여 제시한다.

### 트리거 키워드

"시안 만들어줘", "목업", "mockup", "화면 시안", "디자인 시안", "레이아웃 제안", "시안 보여줘"

### 자동 감지

- `.design/concept.md` 존재 시 → 컨셉 로드하여 반영
- 디자인 토큰 존재 시 → 토큰 적용
- 둘 다 없으면 → 요구사항만으로 생성

### 프로세스

1. 화면 요구사항 파악 (어떤 페이지, 주요 기능, 대상 사용자)
2. 컨셉/토큰 자동 감지 및 로드
3. 하이파이 HTML 시안 5개 생성 (실제 컬러, 타이포, 간격 반영)
4. 각 시안의 디자인 의도 설명 (레이아웃/구성 선택 이유)
5. 사용자 선택 → 피드백 → 수정 → 확정

### 아웃풋

- **HTML 시안 5개**: 브라우저에서 확인 가능한 하이파이 목업
- **디자인 의도 설명**: 각 시안별 레이아웃, 정보 구조, 시각적 강조 선택의 근거

### 인터랙티브 컴포넌트 ID 시스템

시안 HTML의 모든 UI 요소에 의미 있는 ID를 부여한다. 사용자가 특정 컴포넌트를 지칭하거나 추출할 때 사용.

**ID 포맷**: `{컴포넌트명}-{짧은해시}` — 예: `card-product-a3f2`, `header-nav-9b1c`, `btn-primary-7e4d`

- 전역 유니크 — 시안 5개에 걸쳐 ID 중복 없음, 어떤 파일에 있는지 몰라도 지칭 가능
- 호버 시 해당 요소의 ID를 툴팁/오버레이로 표시
- 사용자가 ID로 소통: "v3-card-product-1 추출해줘", "v1-header-nav 피그마로 보내줘"

**Figma 연동**: 사용자가 선택한 시안 또는 개별 컴포넌트를 Figma MCP로 전송 가능. HTML이 기본 출력, Figma는 선별 전송. Figma MCP가 미설정이면 HTML만 제공하고 "Figma 전송을 원하면 Figma MCP 설정이 필요합니다" 안내. 전송 실패 시 에러 메시지와 함께 HTML 파일 경로를 재안내한다.

### References

- `references/mockup-guidelines.md` — 시안 생성 기준 (레이아웃 다양성 규칙, 하이파이 수준 정의, ID 부여 규칙, 디자인 원칙 체크리스트). `docs/design/` 리서치 문서 중 참조 대상: foundations/visual-hierarchy.md, foundations/spacing-layout.md, foundations/grid-alignment.md, interaction/*.md

### 원칙

- 하이파이 수준 — 와이어프레임이 아닌 실제 컬러/타이포/간격이 반영된 완성형
- 5개 시안은 서로 다른 레이아웃/구성 접근 (단순 컬러 변형이 아님)
- design-kit의 디자인 원칙(접근성, 시각 위계, 인증성 등)을 자동 준수
- 기존 UI 코드 리뷰/가이드에는 트리거하지 않는다 — design-guide 사용

---

## 3. design-component — 컴포넌트 정의

### 목적

반복되는 UI 요소를 컴포넌트로 정의하고 카탈로그화한다.

### 트리거 키워드

"컴포넌트 정의", "컴포넌트 리스트", "design component", "UI 컴포넌트 정리", "컴포넌트 만들어줘", "컴포넌트 카탈로그"

### 자동 감지

- 컨셉 문서, 디자인 토큰, 확정 시안이 있으면 로드
- 없으면 사용자가 직접 정의

### 프로세스

0. 자동 감지 및 로드 — 컨셉 문서(`.design/concept.md`), 디자인 토큰, 확정 시안(`.design/mockups/`)이 존재하면 자동 로드하여 반영. 없으면 사용자 직접 정의 모드로 진행.
1. 대상 파악 (확정 시안에서 추출 / 사용자 직접 지정)
2. 컴포넌트 분류 — 버튼, 카드, 입력 필드, 네비게이션, 모달 등
3. 컴포넌트별 정의: 사이즈 variant, 상태(default/hover/active/disabled/loading), 간격, 토큰 매핑
4. 사용자 피드백 → 수정 → 확정

### 아웃풋

- **컴포넌트 카탈로그**: 이름, variant, 상태, 스펙
- **토큰 매핑**: 각 컴포넌트가 사용하는 디자인 토큰

### 아웃풋 형식

기본: Markdown 스펙 문서 (`.design/components/catalog.md`). 추후 Figma 또는 HTML 카탈로그 출력 옵션을 추가할 수 있으나, 1차 구현은 Markdown 스펙만 생성한다.

### References

- `references/component-spec-template.md` — 컴포넌트 정의 템플릿 (이름, variant, 상태, 토큰 매핑, 사용 가이드라인). `docs/design/` 리서치 문서 중 참조 대상: foundations/spacing-layout.md, foundations/color.md, foundations/typography.md, interaction/forms.md

### 원칙

- 컴포넌트 정의는 구현이 아닌 디자인 스펙
- 상태(state)와 variant를 빠짐없이 정의
- 토큰 매핑으로 디자인 시스템과의 일관성 보장

---

## 공통 설계 원칙

### 독립 운영 + 자동 감지

각 스킬은 단독 호출 가능. 이전 단계 산출물이 프로젝트에 존재하면 자동으로 로드하여 반영하되, 없어도 동작한다.

감지 대상:
- `.design/concept.md` — 컨셉 문서
- 디자인 토큰 파일 (design-system 아웃풋)
- `.design/mockups/` — 확정된 시안

### 스택 무관

design-kit의 기존 철학을 유지한다. 원칙과 스펙만 정의하고, 구체적 코드 생성은 해당 toolkit 플러그인(flutter-toolkit 등)에 위임한다. 단, HTML 시안/무드보드는 시각화 목적이므로 예외.

### 리서치 기반

`docs/design/` 22개 리서치 문서를 근거로 디자인 판단. 자체 웹 리서치는 출처와 함께 제시.

### 산출물 저장 위치

```
.design/
├── concept.md          # design-concept 아웃풋
├── moodboard.html      # design-concept 비주얼 무드보드
├── mockups/            # design-mockup 아웃풋
│   ├── <page>-v1.html
│   ├── <page>-v2.html
│   └── ...
└── components/         # design-component 아웃풋
    └── catalog.md      # 컴포넌트 카탈로그
```
