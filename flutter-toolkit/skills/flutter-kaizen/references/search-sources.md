# 검색 소스 및 신뢰도 기준

## 소스 분류

### 학술 논문
- **검색 대상:** arXiv, ACL Anthology, IEEE Xplore, Semantic Scholar
- **키워드:** Flutter architecture, Dart code generation, mobile app testing, widget composition, state management patterns, reactive UI framework, declarative UI, cross-platform development
- **범위:** 최근 6개월 우선, 핵심 논문은 기간 무관
- **후속:** 발견한 논문의 references 섹션에서 관련 논문 추적

### 공식 소스
- **Flutter:** flutter.dev/docs, api.flutter.dev, medium.com/flutter (공식 블로그)
- **Dart:** dart.dev/guides, dart.dev/tools, dart.dev/language
- **Flutter changelog:** github.com/flutter/flutter/releases, flutter.dev/release/breaking-changes
- **Pub.dev:** pub.dev trending, pub.dev 주요 패키지 changelog (riverpod, freezed, go_router, auto_route 등)
- **Google:** medium.com/google-developers (Flutter 관련 포스트)

### 커뮤니티/실무
- **GitHub:** trending repos — 키워드: flutter, dart, riverpod, widget, architecture
- **블로그:** Andrea Bizzotto (codewithandrea.com), Remi Rousselet (riverpod 관련), Very Good Ventures (verygood.ventures/blog)
- **컨퍼런스:** Flutter Forward, FlutterCon, Google I/O Flutter 세션
- **Reddit/Discord:** r/FlutterDev, Flutter Community Discord — 패턴 논의 트래킹

### skills.sh 마켓플레이스
- **URL:** https://skills.sh
- **검색 키워드:** flutter, dart, widget, riverpod, state management, mobile, cross-platform
- **목적:** 다른 Flutter 관련 Claude Code 스킬의 패턴, 접근법, Gotchas를 참고
- **주의:** 스킬의 SKILL.md 원문을 반드시 확인. 목록 description만으로 판단하지 않는다
- **활용 방법:**
  - 우리 스킬에 없는 새로운 패턴이나 워크플로우 발견
  - Gotchas 섹션에서 공통된 실수 패턴 수집
  - Process 구조나 reference 구성의 개선 아이디어 참고

## 신뢰도 기준

| 유형 | 신뢰도 | 태그 | 비고 |
|------|--------|------|------|
| Flutter/Dart 공식 docs | 높음 | — | 최신성 + 권위 |
| Peer-reviewed 논문 | 높음 | — | 가장 신뢰 |
| pub.dev 주요 패키지 docs | 높음 | — | 생태계 표준 |
| arXiv preprint | 중간 | `[preprint]` | 미검증 논문 명시 필수 |
| 유명 Flutter 엔지니어 블로그 | 중간 | `[blog]` | 실전 검증된 패턴 |
| skills.sh 스킬 | 중간 | `[skills.sh]` | 커뮤니티 검증 필요, 원문 확인 필수 |
| GitHub trending | 중간 | `[community]` | 커뮤니티 검증 필요 |
| 일반 블로그/포럼 | 낮음 | `[unverified]` | 다른 소스로 교차 검증 필수 |

## 최신성 기준

- 6개월 이내: 최신으로 간주
- 6개월~1년: `[dated: YYYY-MM]` 태그 부착, 후속 변경 확인
- 1년 이상: Flutter 버전 변화가 빠르므로 폐기 우선 검토

## 중복 방지

- 매 실행 시 `docs/kaizen/flutter-research-log.md`를 먼저 읽는다
- 이미 조사한 URL은 건너뛴다
- 단, 이전 소스의 업데이트(새 Flutter 버전, 패키지 메이저 업데이트, docs 변경)는 재조사한다
