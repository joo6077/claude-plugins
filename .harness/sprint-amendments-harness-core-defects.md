# Sprint Amendments — harness-core-defects

> **이 파일은 봉인된 계약의 보완이지 대체가 아니다.**
> `.harness/sprint-contract-harness-core-defects.md` 는 write-once 이며 조건 줄을 수정하지 않았다
> (`conditions_digest: sha256:459a7c625948ffcb`, 평가 후 `SEAL_OK` 재확인).
> 아래에서 원 조건을 인용할 때는 전부 **원문 그대로**이고 수정본이 아니다.

## AM-01 — narrowing

- **대상 조건**: `AR-03`
- **변경**: 변경 대상 파일 집합을 8 개에서 6 개로 한정. 원 집합은 핸드오프
  `2026-09-06-0130.md` 가 "필수 수정 8 파일" 로 지목한 목록이고, 제외한 2 개는
  `harness/templates/project.yaml` · `.harness/project.yaml` 이다.
- **근거**: 사용자 발언이 아니라 **작성자 자체 판단**이다. `commands.lint` 는 이미 선택 필드로
  존재하므로 스키마를 바꾸지 않고 `harness/README.md` 의 문서 연결만으로 결함 C 의 해당 부분이
  해소된다. 두 `project.yaml` 은 손댈 필요가 없었다.
- **앵커**: 없음 — 사용자 합의가 아닌 에이전트 자체 판단이므로 `consent: unanchored` 다.
  앵커를 지어내지 않는다.
- **direction 산출** (자기신고 아님 · 집합 비교):

```text
원 집합   8 (핸드오프가 지목)
개정 집합 6 (계약이 확정)
added=0 · removed=2 → narrowing
removed: harness/templates/project.yaml · .harness/project.yaml
```

`narrowing · unanchored` 는 §direction × consent 표에서 **PASS 근거로 사용 가능**하다
(제약을 강화하는 방향이라 남용이 불가능하기 때문).

## AM-02 — 기록 전용 (direction 없음)

- **대상 조건**: `AR-03` · `DG-04` · `AR-02`
- **변경**: **없다.** 조건 문구를 고치지 않았으므로 PASS 집합이 움직이지 않는다 —
  direction 판정 대상이 아니다. 이 엔트리는 평가자 improvement 를 **기록만** 한다.
- **근거**: `qa-evaluator` iteration 1 판정 REJECT (20/22) 와 함께 남긴 improvement.
- **앵커**: 피드백 산출물 `.harness/sprint-feedback-harness-core-defects.md` (iteration 1)
  및 `~/.harness/feedback/evaluator/1a3bcba6-2026-09-06T121550-44c7700e-95266.yaml`

| 원 조건 | 결함 태그 | 내용 |
| ------- | --------- | ---- |
| `AR-03` | `측정-상태-모호` | `Given:` 이 "아직 커밋하지 않은 상태" 라는 **상태 서술**로 전제를 잡았는데, 동시 편집 세션의 broad commit 으로 그 전제가 깨졌다. 측정값이 6 이 아니라 10 이 나왔고 초과분 4 는 남의 변경이었다 |
| `DG-04` | `측정-산출물-부재` | "계약을 1 건 작성" 이라는 **실행**을 요구하면서 그 산출물을 어디에 남겨야 하는지(파일 경로 · 최소 조건 수 · 어떤 신규 컨벤션을 반드시 행사해야 하는지)를 조건이 지정하지 않았다 |
| `AR-02` | `범위-미명시` | "같은 표를 2 곳 이상에 복제하지 않는다" 의 **"표"** 가 정의되지 않았다. 태그 이름이 여러 파일에 등장하는 것과 2 열 정의표가 복제된 것은 다른데, 조건이 그 경계를 긋지 않았다 |

### 적용 권고 (다음 계약부터)

- diff-scope 조건은 상태 서술 대신 **baseline 커밋 해시를 조건 본문에 고정**한다.
  후속 계약 `harness-attribution-followup` 의 `AR-01` 이 이 형태를 처음 적용했다.
- 실행을 요구하는 조건은 **산출물 경로를 조건에 적는다.**
- 구조 비교 조건은 비교 단위(표 / 목록 / 문자열)를 조건에 명시한다.

## 귀속 기록 — 동시 세션 커밋에 섞인 이 세션의 산출물

동시 편집 세션이 이 세션의 산출물을 자기 커밋에 함께 담았다. 커밋 메시지가 내용과 어긋나므로
나중에 추적할 수 있도록 여기에 남긴다. 사용자 결정에 따라 **이력은 재구성하지 않았다**.

| 커밋 | 커밋 메시지 | 이 세션 귀속 파일 | 소속 스프린트 |
| ---- | ----------- | ----------------- | ------------- |
| `e73429f` | fix(docs): 죽은 외부 링크 40건 교정 + 외부 링크 검사기 | `bambu-kit/skills/bambu-print-profile/{SKILL.md,BACKLOG.md}` · `.../references/{surface-recipes.md,bambu-fields-baseline.md}` · `docs/bambu-kit/{surface-recipes,bambu-fields-baseline}.html` | `bambu-kit-enum-allowlist-gate` |
| `e73429f` | 〃 | `harness/{README.md,agents/qa-evaluator.md,references/contract-schema.md,skills/sprint-contract/SKILL.md}` · `harness/docs/guides/{contract-design-guide,qa-evaluation-guide}.md` · 계약 2 건 | `harness-core-defects` |
| `3cd7dfe` | fix(docs): QA REJECT 2건 수정 — 소스 역전파 5곳 + 진짜 YAML 오류 3건 | `.harness/sprint-feedback-{bambu-kit-enum-allowlist-gate,harness-core-defects}.md` · 계약 status 전환 | 양쪽 QA 산출물 |

귀속 판정 근거는 diff 내용의 주제다 — 이 세션 것은 enum 값 교정 · 태그 어휘 · `N/A` 규약이고,
동시 세션 것은 URL 문자열 치환이다. 두 주제는 한 파일 안에서도 겹치지 않았다.
