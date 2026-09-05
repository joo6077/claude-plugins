---
slug: api-kit-docs-site
kind: amendments
---

# Sprint Amendments — api-kit docs-site

계약 봉인 이후 측정 과정에서 드러난 사실과 그에 따른 조정을 기록한다.

## A-01 — 대비 측정 범위를 선택자 3 종에서 전체 텍스트 노드로 넓혔다

**계기.** AR-03 을 `.desc` · `.card-source` · `.section-label` 3 종만 재는 스크립트로 측정했더니
`minContrast 4.64` 로 PASS 가 나왔다. 같은 페이지를 전체 텍스트 노드 훑기로 다시 재니
**9 건이 AA 미달**이었다 — 다크 `.caption`/`.dist-val`/`.pane-what`/`.pair-caption`(`--text3`) 3.95,
라이트 `.rank`/`.strength`/`.rule-box strong`(`--accent` on `--surface2`) 4.46.

**조정.** 측정 스크립트가 `body *` 중 **직접 자식 텍스트를 가진 모든 요소**를 훑고,
유효 배경을 조상으로 거슬러 올라가 계산하며, WCAG 큰 텍스트 예외(24px 이상 또는 18.66px 이상 bold → 3:1)를
적용하도록 바꿨다. AR-03 의 판정 근거는 이 넓은 측정이다.

## A-02 — 팔레트 4 개 토큰을 내렸다 (tone-kit 에서 물려받은 값)

A-01 로 드러난 미달을 실측 기준으로 고쳤다. 괄호 안은 고치기 전 실측값이다.

| 토큰 | 테마 | 전 | 후 | 근거 |
| --- | --- | --- | --- | --- |
| `--text3` | dark | `#7A6F64` (3.95 on `--bg`, 4.25 on `--surface2`) | `#948779` | 4.67 / 5.55 |
| `--text3` | light | `#6b7264` (4.45 on `--surface2`) | `#666D5F` | 4.79 |
| `--accent` | light | `#4D7C0F` (4.46 on `--surface2`) | `#3F6212` | 6.33 · `--accent2` → `#365314` |
| `--green` / `--yellow` | light | `#15803d` (4.48) / `#a16207` (4.40) | `#146B32` / `#7A4A05` | 5.90 / 6.68 |

`--red`(5.78) · `--blue`(7.06) · `--cyan`(4.79) 는 통과라 그대로 두었다.
다크 `:root` 의 `--accent:#A3E635` · `--accent2:#D9F99D` 는 `css-tokens.md` 등록값이므로 건드리지 않았다.

## A-03 — 테마 토글 44×44 를 되살렸다

베이스 CSS 를 `tone-kit` 페이지에서 가져오면서 docs-site 정본 템플릿의 규칙 (4)
(`button,.btn,[role="button"]{min-height:44px;min-width:44px}`)이 빠졌다. 실측 96×34 였다.
`.theme-toggle` 에 `min-height:44px;min-width:44px` 를 넣어 96×44 로 맞췄다.

기존 `docs/tone-kit/*.html` 10 페이지도 같은 이유로 96×34 다. **이번 범위 밖이라 고치지 않았다** —
별도 스프린트로 다뤄야 한다.

## A-04 — SC-03 음성 대조가 1 차 시도에서 잘못 통과했다

계약이 요구한 음성 대조(출처 링크를 지우면 오라클이 잡는가)를 처음엔 `card-source` 링크
**한 개만** 지워서 했는데 오라클이 `OK` 를 냈다. 원인은 그 URL 이 같은 페이지 안 4 곳에 있었고
오라클이 **집합 포함**을 보기 때문이다.

오라클은 "소스의 출처 URL 이 페이지에 **한 번이라도** 나타나는가" 를 재고, SC-03 의 주장도 그것이다 —
지표는 주장과 일치한다. 틀린 것은 대조 방법이었다. 4 곳 전부를 바꿔 다시 대조하니
`exit 1` + 누락 URL 명시가 나왔고, 원복 후 `OK` 로 돌아왔다.

## A-05 — 범위 밖으로 미룬 것

- `docs/tone-kit/*.html` 의 44px 미달 (A-03).
- `.playwright-mcp/page-2026-04-09T10-31-43-978Z.yml` 1 개가 추적 중이다. `.gitignore` 에
  `.playwright-mcp/` 를 넣어 이후 137 개가 추가로 들어오는 것은 막았지만, 이미 추적 중인
  1 개를 지우는 것은 이번 변경과 무관하므로 두었다.

## A-06 — SK-05 오라클이 내가 지어낸 URL 을 잡았다

Phase 16 리서치 템플릿의 fallback 칸에 `https://datatracker.ietf.org/doc/html/rfc8785` 를
적었는데, SK-05 의 "인용한 URL 이 `docs/api/` 에 실재하는가" 검사에서 유일하게 걸렸다.
RFC 8785 자체는 실재하지만 그 URL 형태는 이 레포 어디에도 없었고 나는 확인하지 않고 적었다.
`docs/api/contract/snapshot-sealing-canonicalization.md` 가 실제로 인용하는
[I-JSON (RFC 7493)](https://www.rfc-editor.org/rfc/rfc7493.html) 로 바꿨다.
재검사 결과 그 절의 URL 11 개가 전부 `docs/api/` 에 실재한다.

## A-07 — SC-03 오라클을 양방향으로 넓혔다 (QA 지적)

QA 가 지적한 구조적 공백: `check-api-kit-docs.py` 는 "소스 URL 이 HTML 에 있는가" 단방향만 봤다.
그래서 **소스에 근거가 없는 URL 이 페이지에 새로 들어와도 영원히 안 걸린다.**
A-06 이 잡힌 것은 SK-05 가 별도로 양방향이었기 때문이지 이 오라클 덕이 아니었다.

역방향 보고를 추가했다. 초과분은 **실패가 아니라 보고**다 — 저자가 본문에서 든 비교 대상 문서일 수
있기 때문이고, 사람이 한 번 보라는 신호로 남긴다.

실행 결과 초과 URL 13 개가 드러났다. 9 개는 `docs/api/` 다른 문서에 이미 인용된 것이고
(짝지어진 문서의 `> **출처:**` 줄에만 없었다), 나머지 4 개는 이 레포에 처음 등장한다.
4 개 전부 `curl` 로 **HTTP 200** 을 확인했다.

| URL | 확인 |
| --- | --- |
| `https://docs.karatelabs.io/api-reference/syntax-reference/` | 200 |
| `https://docs.pact.io/getting_started/matching` | 200 |
| `https://dredd.org/en/latest/how-it-works.html` | 200 |
| `https://json-schema.org/understanding-json-schema/reference/annotations` | 200 |

## A-08 — AP-03 의 측정 도구가 대상을 못 본다 (QA 지적)

`validate-plugin.py` V6 은 등록된 킷 디렉토리(`<kit>/skills`, `agents`, `references`, `README.md`)만
스캔한다. 이번에 고친 `.claude/skills/**` 와 루트 `README.md` · `CLAUDE.md` 는 스캔 범위 밖이라
**13/13 OK 가 나와도 이 파일들의 bare fence 는 절대 안 걸린다.** 지표가 주장을 재지 못하는 전형이다.

V6 과 같은 상태 머신(여는 fence 만 판정, 닫는 fence 는 원래 언어 힌트가 없다)으로 이번에 만진
`.md` 8 개를 직접 검사해 `phase-dependencies.md:5` 의 여는 bare fence 1 건을 찾아 ```` ```text ````
로 고쳤다. 나머지 7 개는 0 건이다.

루트 `README.md`(5 곳) · `CLAUDE.md`(1 곳)에도 사전부터 bare fence 가 있다. `README.md` 는
`sync-docs.py` 가 일부를 생성하므로 손대면 drift 가 나고, 둘 다 이번 변경과 무관해 **두었다.**
V6 의 스캔 범위를 리포 레벨 문서까지 넓히는 것은 별도 스프린트 대상이다.
