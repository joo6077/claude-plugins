---
feature: "docs 품질 게이트 정비 — 접근성·사실·링크·내비 4종 신설 + 그 게이트가 잡은 결함 일괄 수정"
slug: docs-quality-gates
created: "2026-09-06"
complexity: "큼"
conditions: 25
status: review
retroactive: true
---

## 배경 · 이 계약이 사후인 이유

세션은 `/create-kit` 파이프라인 §14 잔여 4항목으로 시작했고 그건 `sprint-contract-api-kit-docs-site.md`
(38조건, APPROVE)로 덮여 있다. 그 뒤 작업은 **계약 없이** 이어졌다 — 앞 단계 검증이 다음 결함을
드러내는 연쇄였기 때문이다(접근성 실측 → 사실 오류 → 링크 → 내비 등록).

사후 계약이라 "구현 전 합의" 기능은 못 한다. **최종 상태를 독립 검증하는 것**이 목적이다.
사후임을 frontmatter 에 명시한다.

## 공통 전제

- 모든 측정은 레포 루트에서 실행한다.
- 게이트는 **실패를 실제로 잡는 것이 증명된 것만** 인정한다. 변이(mutation) 없이 "통과했다" 는
  근거가 아니다 — 이 세션에서 빈 범위·삼켜진 종료 코드·좁은 표본으로 3 회 헛통과했다.
- 레포 밖 값은 1차 출처 확인 없이 고치지 않는다.

## 범위 경계

- `.harness/history/*` · `docs/superpowers/plans|specs/*` · research-log 의 `[dated:]` 항목은
  **역사 기록**이라 고치지 않는다.
- 의도적 표본(`data-contrast-exempt="specimen"`, "일부러 AA 를 어긴" 예시, 코드 예제의
  플레이스홀더·생략기호)은 결함이 아니다.
- 코드 블록 문법 게이트는 만들지 않는다 (아래 SC-06 참조).

## Skill — 게이트 신설

- [ ] SK-01: `scripts/check-docs-a11y.js` 가 존재하고 `docs/` 전체를 재귀로 훑는다 [exact] (측정: 인자 없이 실행 시 검사 페이지 수 == `find docs -name '*.html' | wc -l`)
- [ ] SK-02: 그 게이트가 오버플로·콘솔에러·대비·터치타깃 **4 종**을 재고, 결함 변이 4 종이 각각 FAIL 하며 정상 페이지와 명시 면제(`data-contrast-exempt`) 페이지는 PASS 한다 [exact, enumerated] (측정: 결함 4 + 정상 1 + 면제 1 = 6 케이스)
- [ ] SK-03: `scripts/check-contrast-claims.py` 가 **문서에 적힌 대비 수치**를 실제 계산과 대조한다 — 렌더된 픽셀을 재는 SK-01 과 대상이 다르다 [structural]
- [ ] SK-04: `scripts/check-docs-links.py` 가 내부 상대링크 + 고아 + 유령 + 아이콘 누락 4 종을 본다 [exact, enumerated]
- [ ] SK-05: `scripts/check-external-links.py` 가 외부 URL 생존을 재고, **CI 게이트가 아니라는 것이 문서에 명시**돼 있다 (네트워크 의존) [structural]
- [ ] SK-06: 4 게이트 전부 이스케이프된 코드 예제를 링크·주장으로 오인하지 않는다 [exact] (측정: `&lt;img src="x"&gt;` 형태를 넣은 합성 페이지에서 검출 0)

## Script — CI 배선

- [ ] SC-01: `ci.yml` 의 Plugin Validation 잡이 `check-contrast-claims` · `check-docs-links` · `sync-docs --check-only` · `sync-orchestrator --check-only` 를 실행한다 [exact, enumerated]
- [ ] SC-02: `ci.yml` 의 Playwright 잡이 `check-docs-a11y.js` 를 실행한다 [exact]
- [ ] SC-03: `check-external-links.py` 는 CI 에 **없다** — 네트워크 의존이라 의도적으로 뺐다 [exact]
- [ ] SC-04: `release.sh` 가 `marketplace.json` 갱신 직후 `sync-docs.py` 와 `sync-orchestrator.py` 를 돌리고 산출물을 커밋에 포함한다 [exact] (측정: `--dry-run` 으로 README·orchestrator 가 실제로 바뀌는지 확인)
- [ ] SC-05: 게이트 스크립트가 `python3 -m py_compile` / `node --check` 를 통과한다 [exact]
- [ ] SC-06: 코드 블록 문법 게이트는 **만들지 않았다**. 근거: JSON/YAML/TOML/Python 블록을 파싱해 14 건이 실패했고, 그중 **11 건이 의도적**(생략기호 · 템플릿 플레이스홀더 · 한 블록 두 파일 · 대안 표기 · "후행 쉼표 parse 실패" 안티패턴 표본)이며 **3 건이 진짜 오류**였다 — 그 3 건은 게이트 없이 직접 고쳤다 [goal]
      (정정 이력: 이 조건은 처음에 "진짜 오류 0 건" 이라고 적었고 그것은 **거짓이었다**. 14 건 중 4 건만 열어 보고 일반화한 결과이며 QA 가 전수 확인으로 잡았다. 좁은 표본에서 일반화한 판단은 근거가 아니다.)
- [ ] SC-07: SC-06 이 지목한 진짜 오류 3 건이 고쳐졌고 해당 블록이 파싱된다 [exact, enumerated] (측정: `docs/react/kit-design/g5b-animation.md` · `docs/react/kit-design/g2-state-data.md` — `@` 로 시작하는 미인용 스칼라, `api-kit/skills/api-contract/SKILL.md` — 콜론 뒤 공백 누락. 셋 다 `yaml.safe_load_all` 통과)

## Error — 게이트가 잡은 결함

- [ ] ER-01: `docs/` 전 페이지가 WCAG AA 를 통과한다. 미달은 `data-contrast-exempt="specimen"` 으로 명시 면제된 것뿐이고, 면제마다 사람이 읽을 사유가 붙어 있다 [exact]
- [ ] ER-02: 문서에 적힌 대비 수치가 실제 계산과 일치한다 [exact] (`check-contrast-claims.py` exit 0)
- [ ] ER-03: 내부 상대링크가 전부 실재하는 파일을 가리킨다 [exact]
- [ ] ER-04: 고아 페이지 · 유령 등록 · 아이콘 누락이 0 이다 [exact]
- [ ] ER-05: 외부 URL 중 404/410 이 **0 건**이다 [exact]. 추출 아티팩트로 남기지 않는다 — `](url)` 정규식이 URL 중간의 균형 괄호(`Nudge_(book)` · `EPRS_ATA(2025)…`)에서 끊기던 버그를 `check-external-links.py` 에서 고쳤다
- [ ] ER-06: 레포 밖 사실 주장 중 1 차 출처와 어긋난 것을 고쳤고, **확인 못 한 값은 고치지 않았다** [goal] (음성 대조: 확인 없이 고쳤다면 틀린 값을 다른 틀린 값으로 바꿨을 것이다 — 실제로 Codex 제안 3 건이 curl 검증에서 404 였다)

## Architecture

- [ ] AR-01: 생성 HTML 을 고칠 때 **소스 `.md` 도 함께** 고쳤다 [exact] (측정: 고친 값의 옛 형태가 `docs-site` 매핑표의 **모든** 소스 디렉토리에 남아 있지 않다 — design-kit · harness · api 뿐 아니라 `docs/backend/` · `docs/infra/` · `docs/tone/` 포함)
      (정정 이력: 1 차에서 design-kit·harness·api 소스만 맞추고 backend·infra 소스 5 곳을 빠뜨려 QA 가 FAIL 했다. 매핑표를 열어 대상 전체를 세지 않고 "고친 것 위주"로 훑은 결과다.)
- [ ] AR-02: 날짜가 박힌 역사 기록(변경이력 행 · `[dated:]` · `.harness/history/`)은 고치지 않았다 [exact]
- [ ] AR-03: 색을 바꿔 대비 수치를 맞추지 않았다 — 틀린 것은 적힌 수치지 색이 아니다 [exact]
- [ ] AR-04: 삭제한 페이지 4 개는 소스 `.md` 가 없고 내비 미등록이며 `-guide` 판으로 대체된 것이다 [exact]

## Diagnostics

- [ ] DG-01: 게이트 11 종 전부 exit 0 (contrast-claims · docs-links · validate-plugin · api-kit-docs · run-evals · sync-docs · sync-orchestrator · sync-evals · a11y · playwright · harness save-test)
- [ ] DG-02: 워킹트리 클린, `main` 대비 커밋만 존재
