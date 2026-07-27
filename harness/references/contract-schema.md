# Sprint Contract 스키마

> sprint-contract 와 qa-evaluator 가 공유하는 계약 포맷 정의.
> contract-kaizen 이 변경 제안 가능, evaluator-kaizen 이 읽어서 평가 루브릭에 반영.
>
> **최근 갱신: 2026-07-27 (Phase 2 kaizen · v4)** — 허용 섹션 헤더 2 계층 분류 (조건 섹션 / 서술 섹션), Counterpart 조건 패턴 (producer/consumer 분리 필수), Diff-Scope Oracle 표준형 4 요소, 증거 아티팩트 경로 명시 의무 추가. 상세 작성법은 `harness/docs/guides/contract-design-guide.md` 참조.
>
> 이전: 2026-04-24 (v3) — 검증 수단 명시 의무, 스코프 범위 인라인 명시, sibling consistency enumerated 필수, `[미검증]` 마커 표기 규칙 추가.
>
> 이전: 2026-04-11 (v2) — 조건 태그 (Specificity Tag) 서브섹션 신설, aggregation mode 개념 추가.

## 계약 파일

**경로**: `{CONTRACT_ROOT}/.harness/sprint-contract.md`

`CONTRACT_ROOT` 는 `.harness/project.yaml` 을 발견한 디렉토리의 **절대경로**다. 세션 도중 cwd 가
바뀌어도 이 값을 기준으로 경로를 해석한다 (v4 추가 — `cwd-contract-path-drift` 재발 방지).

## 허용 섹션 헤더 (v4 추가)

계약 파일의 2 단계(`##`) 헤더는 아래 두 계층 중 하나여야 한다. 밖의 헤더는 금지다.

| 계층 | 허용 헤더 | 헤더 매칭 | 조건 체크박스 |
| ------ | ------ | ------ | ------ |
| **조건 섹션 (parsed)** | `project.yaml.contract_categories` 의 각 `id` + `Anti-patterns` + `Reusability` + `Diagnostics` | 정확히 일치 (괄호 부연 금지) | `- [ ] {PREFIX}-{NN}:` 형태로 **여기에만** 존재 |
| **서술 섹션 (non-parsed)** | `배경` · `리서치 소스` · `GAP 분석` · `범위 경계` · `회귀 게이트` | 접두 일치 (뒤에 부연 허용) | 조건 체크박스 **금지** — 일반 불릿만 |

**결정론적 검사 (E3)** — 계약 저장 직후 실행하고 위반 0 건을 확인한 뒤 다음 단계로 넘어간다:

```bash
# (1) 헤더 목록 — 허용 목록 밖 헤더가 있으면 위반
grep -n '^## ' "$CONTRACT_ROOT/.harness/sprint-contract.md"

# (2) 서술 섹션에 조건 체크박스가 섞였는지 — 조건 섹션 밖의 '- [ ]' 는 위반
awk '/^## /{s=$0} /^- \[ \]/{print FILENAME":"FNR": "s" -> "$0}' \
  "$CONTRACT_ROOT/.harness/sprint-contract.md"
```

## 메타데이터 (YAML frontmatter)

```yaml
feature: "{기능명}"
created: "{YYYY-MM-DD HH:mm}"
complexity: "{simple|medium|complex}"
conditions: {총 조건 수}
```

## 필수 섹션

### 1. 카테고리별 조건

```markdown
## {CategoryID}
- [ ] {PREFIX}-{NN}: {PASS/FAIL 이진 판정 가능한 조건문} [specificity-tag]
```

- `CategoryID` 와 `PREFIX` 는 `project.yaml.contract_categories` 에서 가져온다
- 조건문은 능동태, 단일 조건, 측정 가능해야 한다
- "잘 동작한다", "적절히 처리한다" 같은 모호 표현 금지
- 조건 끝에 **구체성 태그** 를 붙여라 — 상세는 아래 §조건 태그 섹션 참조

#### 조건 태그 (Specificity Tag)

모든 계약 조건은 끝에 구체성 태그를 붙여야 한다. 미명시 시 `[structural]` 로 간주.

| 태그 | 의미 |
|------|------|
| `[exact]` | 이름/값/구조 문자 그대로 매칭 |
| `[structural]` | 섹션/필드/파일 존재 확인 (기본값) |
| `[goal]` | 목표 달성 여부만 판정, 수단 무관 |

**예시:**

```markdown
- [ ] UI-01: 라우터에 /settings 경로가 등록된다 [exact]
- [ ] UI-02: 설정 화면에 접근성 라벨이 모든 버튼에 존재한다 [structural]
- [ ] LO-01: 로그인 실패 시 사용자에게 실패 원인이 전달된다 [goal]
```

**Aggregation Mode** — 다수 대상 (파일/모듈/키워드) 조건은 태그에 모드를 함께 명시한다:

| 모드 | 의미 |
|------|------|
| `enumerated` | 각 대상을 개별 이름으로 명시해야 PASS |
| `collective` | 포괄 경로/패턴 하나로도 PASS (기본값) |

**예시:**

```markdown
- [ ] RE-01: References 에 g1, g2, g3, g4, g5, g5b, g6 7 개 파일이 각각 파일명으로 명시된다 [exact, enumerated]
- [ ] RE-02: References 에 docs/react/kit-design/ 경로가 명시된다 [structural, collective]
```

**규칙:**

- 숫자 레벨 태그 (L-one/L-two/L-three) 는 **QA 평가 깊이 전용** — 계약 태그로 재사용 금지
- 상세한 작성법은 `harness/docs/guides/contract-design-guide.md` §조건 구체성 태그 참조

#### 검증 수단 인라인 명시 (v3 추가)

모든 조건은 "어떤 도구 · 명령 · 관찰로 판정할지" 를 인라인 기술한다.

**형식:**

```markdown
- [ ] {PREFIX}-{NN}: {조건} (측정: {명령/도구/관찰}) [specificity-tag]
```

**예시:**

```markdown
- [ ] AR-03: docs/flutter/ 총 줄 수 >= 1500 (측정: `wc -l docs/flutter/*.md | tail -1`) [exact]
- [ ] UI-05: 모달 overlay 가 표시된다 (측정: MCP Figma read-back 또는 Playwright snapshot) [goal]
```

**MCP / 외부 도구 fallback 3 단계 (v3 추가):**

외부 도구 의존 조건은 다음 3 단계를 인라인 기술한다:

```markdown
- [ ] LG-02: 모달 close 버튼 클릭 시 overlay 가 dismiss 된다
      (측정: 1차 MCP Figma read-back · 2차 fallback: MutationObserver 로 CSS display
      상태 확인 스크린샷 · 3차 불가능 시 `[미검증]` 마커 허용) [goal]
```

#### `[미검증]` 마커 (v3 추가)

평가 시점에 검증 도구가 모두 불가능하면 평가자는 해당 조건에 `[미검증]` 마커를
붙이고 근거 블록에 사유를 기록한다.

**수용 임계:**

- 계약 전체에서 `[미검증]` 마커 **1 건까지만** PASS 처리 가능
- **2 건 이상 누적 시 자동 REJECT** (qa-evaluation-guide 의 동일 정책과 맞물림)
- 계약 작성 단계에서 `[미검증]` 허용 건수 예상치가 2 건 이상이면 조건 재설계

#### Sibling Consistency enumerated (v3 추가)

플러그인 내 여러 스킬에 공통 원칙을 요구하는 조건은 반드시 `[exact, enumerated]`
또는 `[structural, enumerated]` 를 사용한다. 대상 스킬 개수를 숫자로 명시하고
이름 전부 열거.

```markdown
- [ ] SK-03: domain event + outbox 원칙이 rust-init, rust-feature, rust-service,
      rust-api 4 개 스킬 Gotchas 에 모두 존재한다 [exact, enumerated]
```

#### Counterpart 조건 (v4 추가)

계약 · 직렬화 포맷 · 공유 모델 · 공개 시그니처 · DB 스키마를 변경하는 스프린트는
**producer 면과 consumer 면을 각각 별도 조건**으로 담아야 한다. 한 조건에 양면을 묶는 것은
복합 조건이므로 금지다. 각 조건은 해당 면의 파일 경로를 `[exact, enumerated]` 로 열거한다
(`collective` 금지). consumer 가 없으면 "소비자 없음" 을 근거와 함께 조건에 명시한다.

```markdown
- [ ] AR-04: 응답 필드 rename 이 producer 면 파일 `server/src/handler/schedule.rs` 에
      반영된다 [exact, enumerated] (측정: 신규 필드명 존재 · 구 필드명 0 건)
- [ ] AR-05: 같은 rename 이 consumer 면 파일 `app/lib/data/model/schedule_model.dart`,
      `app/lib/data/model/schedule_model.g.dart` 2 개에 반영된다 [exact, enumerated]
      (측정: 신규 필드명 존재 · 구 필드명 0 건)
```

소비면의 **내부 구현**은 조건화하지 않는다 (과잉 계약). 한 스프린트에서 양면을 다 못 바꾸면
남는 쪽은 `[미검증]` 이 아니라 **명시적 미완 조건**으로 남긴다 — `[미검증]` 은 검증 도구 부재
전용 마커다.

#### Diff-Scope Oracle 표준형 (v4 추가)

"변경 범위" 를 조건으로 쓸 때 `git diff` 자유 서술을 금지한다. 아래 4 요소를 모두 채운다:
**(1) 상태 전제** (`Given: 커밋 직전 working tree` 또는 `Given: 스테이징 완료 후`) ·
**(2) 경로 한정 pathspec** · **(3) 생성물 제외 pathspec** · **(4) 기대 집합**("정확히 일치" 인지
"포함" 인지).

```markdown
- [ ] AR-01: 변경이 변환 헬퍼 2 개 파일로 한정된다 [exact, enumerated]
      (Given: 커밋 직전 working tree ·
       측정: `git diff --name-only HEAD -- app/lib ':(exclude)*.g.dart'` 결과가
       `app/lib/data/mapper/schedule_mapper.dart`,
       `app/lib/data/mapper/group_mapper.dart` 2 행과 정확히 일치)
```

계약 작성 시점에 그 명령을 1 회 실행하고 현재 출력(baseline)을 서술 섹션에 남긴다.

#### 증거 아티팩트 경로 (v4 추가)

조건이 참조하는 증거가 코드 · 파일 · 명령 출력이 아니라 **기록물**(승인 로그, 합의 기록, 실측
수치)이면, 그 기록물이 평가 시점에 존재할 **경로**를 조건에 적는다. 경로를 적을 수 없으면 그
조건을 만들지 않는다.

```markdown
- [ ] UI-06: 채택 시안 ID 와 승인 일시가 `.harness/design-approval.md` 에 기록되어 있다
      [structural] (측정: 파일 존재 + 시안 ID 1 건 이상)
```

### 2. Anti-patterns

```markdown
## Anti-patterns
- [ ] {id}: {message}
```

- `project.yaml.anti_patterns`에서 최소 2개 선별
- 해당 구현에서 발생 가능성이 높은 것을 우선 선택

### 3. Reusability (자동 포함)

```markdown
## Reusability
- [ ] RE-01: private 일회용 컴포넌트가 없다
- [ ] RE-02: 기존 공용 컴포넌트를 재사용한다
```

### 4. Diagnostics (자동 포함)

```markdown
## Diagnostics
- [ ] DG-01: analyze 경고 0건
- [ ] DG-02: analyze 에러 0건
- [ ] DG-03: 테스트 전체 통과
- [ ] DG-04: 콘솔 에러 0건
```

## 복잡도별 조건 수 가이드

| 복잡도 | 파일 영향 | 조건 수 |
|--------|----------|--------|
| 단순 | 1-3 | 4-6 |
| 중간 | 4-8 | 8-12 |
| 복잡 | 9+ | 12-20 |

## 스키마 버전

현재: **v4** (2026-07-27)

변경 이력:

- **v4 (2026-07-27)** — 허용 섹션 헤더 2 계층 분류 (조건 섹션 parsed / 서술 섹션 non-parsed) 와 저장 직후 결정론적 검사, `CONTRACT_ROOT` 기준 경로 해석, Counterpart 조건 (producer/consumer 분리 · `[exact, enumerated]` 필수), Diff-Scope Oracle 표준형 4 요소, 증거 아티팩트 경로 명시 의무. Phase 1 §3.7 enforcement 등급 사다리를 계약 레이어에 적용하여 재발 규칙 4 건을 승급.
- **v3 (2026-04-24)** — 검증 수단 인라인 명시 필수, MCP/외부 도구 의존 조건의 3 단계 fallback 규칙, `[미검증]` 마커 및 수용 임계 (1 건 허용 / 2 건 이상 REJECT) 명문화, Sibling Consistency 조건 enumerated 필수. Phase 1 (skill/agent-design-guide) Cross-Surface Parity 원칙을 계약 레이어에 전수.
- **v2 (2026-04-11)** — 조건 구체성 태그 (`[exact]` / `[structural]` / `[goal]`) 와 aggregation mode (`enumerated` / `collective`) 필수화. 숫자 레벨 태그 금지 명시.
- **v1** — 초기 스키마.
