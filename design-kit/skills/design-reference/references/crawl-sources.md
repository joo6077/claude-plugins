# 크롤링 소스 가이드

design-reference 스킬이 참조하는 소스 채널별 크롤링 대상과 수집 기준.

## 소스 채널 배분

| 소스 채널 | 기본 배분 | 역할 |
|-----------|-----------|------|
| 디자인 갤러리 | ~10개 | 시각적 트렌드, 영감, 컬러/타이포 조합 |
| 실제 프로덕트 사이트 | ~12개 | 실전 검증된 UI/UX, 인터랙션 패턴 |
| 오픈소스 DS 컴포넌트 비주얼 | ~8개 | 컴포넌트 형태, variant, 상태 시각 표현 |

사용자가 `--count N`으로 총 수량을 변경하면 비율을 유지하여 재배분한다.

## 디자인 갤러리 소스

| 사이트 | URL 패턴 | 검색 방법 |
|--------|----------|-----------|
| Dribbble | dribbble.com/search/{keyword} | WebSearch "site:dribbble.com {keyword}" |
| Awwwards | awwwards.com/websites/{keyword} | WebSearch "site:awwwards.com {keyword}" |
| siteinspire | siteinspire.com | WebSearch "site:siteinspire.com {keyword}" |
| Mobbin | mobbin.com | WebSearch "site:mobbin.com {keyword}" (모바일 앱 UI) |

**수집 항목:**
- 전체 레이아웃 구조 (그리드, 섹션 배치)
- 컬러 조합 (주요 컬러 3-5개, 배경/텍스트/강조)
- 타이포그래피 사용 (서체 분류, 크기 위계, 웨이트 활용)
- 전체 분위기/무드

**비수집 항목 (design-research 영역):**
- 디자인 원칙 추출
- UX 가이드라인 정리
- 접근성 기준 분석

## 실제 프로덕트 소스

키워드 기반으로 해당 도메인의 실제 서비스를 검색한다:

| 도메인 예시 | 검색 전략 |
|-------------|-----------|
| SaaS 대시보드 | "best SaaS dashboard design 2026" |
| 이커머스 | "ecommerce website design examples" |
| 핀테크 | "fintech app design UI" |
| 헬스케어 | "healthcare platform UI design" |

**수집 항목:**
- 네비게이션 패턴 (사이드바/탑바/탭바/햄버거)
- 정보 구조 (카드/리스트/테이블/대시보드)
- 인터랙션 패턴 (호버 효과, 트랜지션, 피드백)
- 반응형 전략 (데스크톱/태블릿/모바일 대응)

**WebFetch 분석 포인트:**
- HTML 구조에서 레이아웃 패턴 파악
- CSS에서 컬러 변수, 간격 체계, 타이포 스케일 추출
- 주요 컴포넌트의 시각적 구성 기록

## 오픈소스 DS 컴포넌트 비주얼 소스

| 시스템 | 쇼케이스 URL | 수집 대상 |
|--------|-------------|-----------|
| Ant Design | ant.design/components | 컴포넌트 렌더링 결과 |
| Chakra UI | chakra-ui.com/docs/components | 컴포넌트 시각 형태 |
| shadcn/ui | ui.shadcn.com | 컴포넌트 스타일링 |
| Mantine | mantine.dev | 컴포넌트 variant |
| Radix Themes | radix-ui.com/themes | 테마 적용 결과 |

**수집 항목:**
- 버튼, 카드, 입력 필드 등의 시각 스타일
- Variant별 시각 차이 (primary/secondary/outline 등)
- 상태별 시각 표현 (default/hover/active/disabled)
- 간격과 라디우스 체계

**비수집 항목 (design-research 영역, docs/design/systems/에 이미 존재):**
- 컴포넌트 API 분석
- 아키텍처/철학 분석
- 접근성 구현 방식 분석
- 코드 패턴 분석

## 다양성 확보 규칙

- 같은 사이트에서 3개 이상 수집 금지
- 같은 레이아웃 패턴이 5개 이상 중복되면 다른 패턴을 우선 수집
- 소스 채널 간 비율은 유지하되, 특정 채널에서 수집 불가 시 다른 채널로 재배분
