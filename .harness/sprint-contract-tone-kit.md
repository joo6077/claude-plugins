# Sprint Contract — tone-kit v0.1.0 신규 킷 생성

```yaml
sprint: tone-kit-creation
created: 2026-08-31
branch: feat/tone-kit
iteration: 1
scope: app_kiosk anti-AI-tone 자산(코딩 표준 625줄 · 근거 문서 921줄 · 로컬 스킬 4종 · 암묵 템플릿)을 claude-plugins 마켓플레이스 플러그인으로 격상
```

## 공통 전제 (전 조건에 적용 — 조건마다 반복하지 않는다)

1. **원본 무수정.** `apps` 레포와 글로벌 메모리는 이번 범위 밖이다. 모순은 킷 콘텐츠 확정으로만 해소하고 원본 정리는 후속 안건 문서에 남긴다.
2. **근거 등급 3분류.** 모든 규칙은 `MUST`(공식 문서가 금지/강제) · `SHOULD`(공식 문서가 권고) · `관측 컨벤션`(공개 근거 없음, 실측만) 중 하나를 명시한다. 공식 문서의 권고를 강제로 승격하지 않는다.
3. **인용 검증.** URL 을 창작하지 않는다. 접근 실패는 "확인 실패"로 명시한다. 자연어 텍스트 탐지 문헌과 비공개 사내 문서는 인용하지 않는다.
4. **배포 단위는 `tone-kit/` 뿐이다.** 킷 내부 파일은 킷 밖(`../../docs/` 등)을 상대경로로 참조하지 않는다.
5. **오라클은 실행 결과로 증명한다.** 검색 패턴을 실었으면 bash·zsh 양쪽에서 실행하고, 준수 상태에서 0건이 정상인 패턴은 합성 양성 케이스로 생존을 증명한다.

## 완료 조건

### AR — 구조 (Architecture)

| ID | 조건 | 판정 |
|---|---|---|
| AR-01 | `tone-kit/.claude-plugin/plugin.json` 존재, `name` 이 디렉토리명과 일치, `version` `0.1.0` | V7 OK |
| AR-02 | 스킬 정확히 3개 (`tone-guide` · `tone-scaffold` · `tone-campaign`). audit 을 별도 스킬로 분리하지 않음 | 디렉토리 수 = 3 |
| AR-03 | `references/` · `templates/` 가 flat (하위 디렉토리 0개) | `find -type d` 결과 |
| AR-04 | 각 SKILL.md 본문 500줄 미만 | `wc -l` |
| AR-05 | 3축 레이어(스택 / 언어 / 프로젝트)가 파일명 prefix 로 인코딩됨 (`core-*` · `locale-*` · `adapter-*`) | 파일 목록 |
| AR-06 | 어댑터는 `dart-flutter` 하나만 채워지고, 어댑터 계약 파일이 슬롯을 정의 | `adapter-contract.md` 존재 + 슬롯 10개 |

### SK — 스킬 품질 (Skill)

| ID | 조건 | 판정 |
|---|---|---|
| SK-01 | 3개 스킬 frontmatter 에 `name` · `description` · `user-invocable` 존재 | V1 OK |
| SK-02 | 각 스킬이 자기 audit 을 내장 (완료 전 규칙 전수 대조 단계 존재) | Process 에 대조 단계 |
| SK-03 | 트리거 어휘가 킷 내부에서 set intersection ∅ **그리고** substring containment ∅ | 수동 계산 |
| SK-04 | 트리거 어휘가 타 킷과도 두 규칙 모두 공집합 | 수동 계산 |
| SK-05 | 선점 어휘(`anti-AI-tone 체크` · `감사`/`audit` · `리뷰해줘` · `품질 검사` · `체크리스트` · `리팩터링`) 미사용 | grep |
| SK-06 | 각 스킬 description 에 다른 스킬/킷과의 구분 조건 명시 | description 본문 |
| SK-07 | SKILL.md 의 모든 상대링크가 실제 파일로 해석됨 | V3 OK |

### DO — 근거 문서 (Document)

| ID | 조건 | 판정 |
|---|---|---|
| DO-01 | `docs/tone/` 리서치 문서 8종 + research-log | 파일 수 |
| DO-02 | 전 문서에 frontmatter(`title` · `version` · `last_updated`) | grep |
| DO-03 | 모든 원칙에 인라인 출처. 실측 근거는 실측으로 표기하고 논문 각주를 붙이지 않음 | 문서 검토 |
| DO-04 | DetectGPT · Binoculars · 비공개 사내 PDF 인용 0건 (제외 사유 서술 제외) | grep |
| DO-05 | 접미사 taxonomy 가 "업계 표준"이 아니라 **합성 규칙**으로 라벨 | `naming-taxonomy.md` |
| DO-06 | "모든 하위 위젯 별도 파일" 이 `관측 컨벤션` 으로 표기 | `extraction-thresholds.md` · `adapter-dart-flutter.md` |
| DO-07 | 안티패턴 H 가 위반이 아니라 **보존 카테고리**로 분류 | `antipattern-catalog.md` |

### RF — 운영 참조 (Reference)

| ID | 조건 | 판정 |
|---|---|---|
| RF-01 | `references/` 9종 존재 (core 4 · locale 1 · adapter 2 · project-detection · sources) | 파일 목록 |
| RF-02 | `templates/` 8종 존재 (암묵 템플릿 5종 명시화 포함) | 파일 목록 |
| RF-03 | 어댑터 완료 게이트 검색 패턴 10종이 실행 검증됨 (bash · zsh 동일 결과) | 실행 로그 |
| RF-04 | 각 검색 패턴에 "히트가 곧 위반인가" 판정 병기 | `adapter-dart-flutter.md` |
| RF-05 | 프로젝트 파라미터가 3분류(결정론 / 감지+확인 / 정책 상수)로 나뉨 | `project-detection.md` |
| RF-06 | `sources.md` 에 제외된 출처와 그 사유가 기록됨 | 파일 내용 |

### ER — 게이트 (Error / 검증)

| ID | 조건 | 판정 |
|---|---|---|
| ER-01 | `validate-plugin.py tone-kit` V1~V8 전부 OK, exit 0 | 실행 |
| ER-02 | `validate-plugin.py` 전체 12킷 OK — 기존 11킷 회귀 0 | 실행 |
| ER-03 | `sync-evals.py --check-only` 통과 (evals 가 스킬 3개와 1:1) | 실행 |
| ER-04 | `run-evals.py tone-kit` 3/3 PASS | 실행 |
| ER-05 | `sync-docs.py --check-only` drift 0 | 실행 |
| ER-06 | `sync-orchestrator.py --check-only` drift 0 | 실행 |
| ER-07 | 킷 전체에 `TODO`/`TBD`/`FIXME` 0건, 언어 없는 코드펜스 0건 | V5 · V6 |
| ER-08 | 킷 전체에 프로젝트 고유 식별자 0건 | grep |

### RG — 레지스트리 (Registry)

| ID | 조건 | 판정 |
|---|---|---|
| RG-01 | `marketplace.json` 에 등록, description 이 `[vX.Y.Z · YYYY-MM-DD]` 형식 | V7 OK |
| RG-02 | `marketplace.json` **끝에 append** — 기존 Phase 번호 밀림 0 | 배열 위치 |
| RG-03 | `validate-plugin.py` `KIT_CONTEXT_TOKENS` 에 tone-kit 추가 | 파일 |
| RG-04 | `run-evals.py` `ALL_KITS` · `sync-evals.py` `TARGET_KITS` 에 추가 | 파일 |
| RG-05 | `detect-docs-drift.py` `SOURCE_TO_HTML` 에 매핑 추가 | 파일 |
| RG-06 | `.claude/skills/tone-research` · `tone-kaizen` 생성 (플러그인 밖) | 디렉토리 |
| RG-07 | 카이젠 오케스트레이터 Phase 15 생성 + 수기 4곳(다이어그램 · 호출 목록 · 킷별 지시 · Final 범위) 갱신 | 파일 |
| RG-08 | `phase-dependencies.md` · `phase-research-templates.md` 에 Phase 15 추가 (필수 소스 3건 이상) | 파일 |
| RG-09 | `CLAUDE.md` Skills Reference 에 tone-kit 섹션 + 카이젠 2종 | 파일 |

### DS — 문서 사이트 (Docs Site)

| ID | 조건 | 판정 |
|---|---|---|
| DS-01 | `docs/tone-kit/` HTML **8페이지** (리서치 문서 수와 동일) | 파일 수 |
| DS-02 | 각 페이지 400줄 이상 | `wc -l` |
| DS-03 | accent 가 `#D946EF` 계열이고 css-tokens 매핑에 등록됨. 기존 킷과 충돌 0 | grep |
| DS-04 | 테마 저장 키가 `dk-theme` | grep |
| DS-05 | 외부 CDN·스크립트·스타일시트 참조 0건 (standalone) | grep |
| DS-06 | 원칙 카드에 출처 링크 또는 실측 배지 존재 | 페이지 검토 |
| DS-07 | `docs/index.html` categories 에 8페이지 전부 + `getIcon()` 에 8개 id 등록 | grep |

## 범위 밖 (판정 대상 아님)

- `apps` 레포 원본 정리 (섹션 번호·폐기 조항·로그 번호·비공개 PDF 인용)
- 글로벌 메모리 정리 (폐기 마킹·빈 name·인덱스 누락)
- flutter-toolkit 충돌 8건 패치
- 피드백 기록 스킬 ↔ 승격 파이프라인 절차 충돌
- 프로젝트 지침 문서 다이어트

## 판정

- 전 조건 PASS → APPROVE
- FAIL 1건 이상 → REJECT. FAIL 항목 수정 후 재평가 (최대 3회)
