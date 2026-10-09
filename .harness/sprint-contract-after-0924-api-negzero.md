---
feature: "api-kit — -0 을 I-JSON 게이트에서 떼어 JCS 앞 -0 검사로 · noncharacter 를 목록에 맞춤"
slug: after-0924-api-negzero
created: "2026-09-26 11:56"
complexity: "중간"
conditions: 18
status: done
owner_session: bda55d45-296c-491f-89ba-b52042d58e72
conditions_digest: sha256:42659fdebb3e228a
locked_at: "2026-09-26 12:11"
---

## 배경

- 넘김 출처: `.harness/.meta/kaizen-0924/f1-kit-followups-notes.md` 80 행 · 다음 사이클 메모 Phase 16 「`-0` 을 「I-JSON 게이트」 에서 떼어 이름을 가를지 — RFC 7493 §2.2 원문을 근거 파일에 먼저」, 핸드오프 `/Users/jackson/Hub/10_Dev/claude-plugins/.harness/handoff/2026-09-26-0110.md` §C3 api-kit.
- 근거 파일(이 가지에서 새로 만듦): `.harness/.meta/evidence/rfc7493-ijson-2026-09-26.md` — Codex(0.157.1 · gpt-5.6-sol)가 rfc-editor.org 원문을 받아 인용했다. 요지: 중복 키(§2.3) · surrogate · **noncharacter(§2.1, MUST NOT)** · binary64 밖 숫자(§2.2, SHOULD NOT) 는 RFC 7493 에 있다. **`-0` 은 RFC 7493 에 없다**(전문 검색 0 건, RFC 8259 문법상 유효한 숫자). `-0` 을 막는 근거는 RFC 8785(JCS) 정정 7920 의 SHOULD 다. NaN/Infinity 는 JSON 문법 자체가 금지한다.
- 그래서 `-0` 을 「I-JSON 게이트」 목록에서 빼 그 뒤의 「`-0` 검사」 로 따로 적는다. 분류(계약 실패가 아니라 비교 불가 · 봉인 불가)는 바꾸지 않는다 — 이름과 근거만 바로잡는다. noncharacter 는 api-contract 표에만 있고 다른 두 목록에 빠져 있어 맞춘다.
- 사용자 위임: user `2026-09-26T01:04:21.505Z` 「다음 세션에서 직접할 일을 다 실행하고 이어질것도 실행해」 (세션 기록 `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/de8c7935-a5b6-4df5-9106-fafa73c288a0.jsonl`).
- 복잡도 4 축: 레이어 — 킷 스킬 문서 · 원본 문서 · 문서 페이지 / 공개 계약 변경 — 예 (킷이 적은 검사 순서 · 이름) / 소비면 — 예 (원본 문서 · 문서 페이지가 같은 목록을 싣는다) / 회귀 위험 — 낮음 (실행 코드 없음 — 검사는 문서 규칙뿐, `find api-kit -name '*.py' -o -name '*.sh'` 0 개). 둘이 예라 「중간」.

## 범위 경계

- 대상 파일 다섯: `api-kit/skills/api-contract/SKILL.md` · `api-kit/skills/api-verify/SKILL.md` · `api-kit/skills/api-probe/SKILL.md` · `docs/api/contract/snapshot-sealing-canonicalization.md` · `docs/api-kit/snapshot-sealing-canonicalization.html`. 그 밖에 근거 파일과 `docs/api/research-log.md` 에 이번 결정 한 절.
- `api-kit/skills/api-probe/references/hurl-execution.md:276` 의 흐름 줄(`scrub → I-JSON 검문 → raw 봉인 → normalized(JCS)`)은 `-0` 을 나열하지 않으므로 그대로 둔다.
- 측정 스크립트: scratchpad `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72/scratchpad/api0-measure.py <워크트리>` (봉인 시점 sha256 앞 16 자 `9b4127b764ed5a62`). 고치기 전 결과 `api0-before.txt`. 「-0 검사」 가 새 표시다 — `-0` 을 백틱이나 `<code>` 로 감싼 표기도 같은 표시로 본다(교차 진단 지적: 문서 관례대로 백틱을 쓰면 옛 측정은 고친 판을 못 가렸다). 한 줄 안에서 그 표시 앞이 I-JSON 목록이다. 봉인 전 세 방향 실측: 고치기 전 판 불합격 · 수정 스크립트(`api0-apply.py`)를 사본에 적용한 판 통과 · 그 사본을 백틱 표기로 바꾼 판 통과.
- AR-01 결정: 원본 문서 목록의 「Unicode 로 표현 불가한 문자열」 과 noncharacter 는 **합친다** — 「Unicode 로 표현 불가한 문자열(lone surrogate · noncharacter)」 로 괄호 안 예로 둔다.
- 기준 커밋: 이 가지는 V10 PR #111 이 합쳐진 뒤의 origin/main `cdadb10` 에서 갈라졌다(교차 진단 지적 — 처음 적은 `f81568d` 는 무관한 파일 여섯을 끌어들인다).
- 같은 킷을 다른 묶음 둘이 고친다(`ak-c3c` 설계 기록 · `ak-c4a` api-ui). 파일은 겹치지 않는다. 킷 버전은 합친 뒤 한 번 올린다.
- 커버리지 해소: SK-02 · AR-02 — 줄 · 자리 이름은 측정 스크립트 출력 이름과 같다.

## 회귀 게이트

- 고치기 전(`api0-before.txt`): `SK-01 gate_block_neg0=1 prose_neg0_7920=0 prose_neg0_7493=0 nonchar_in_block=1` · SK-02 세 줄 모두 `mark=0 neg0_in_ijson=1 nonchar=0` · `SK-03 order_ok=0 neg0_class_noncomparable=0` · `AR-01 neg0_in_list=1 nonchar_in_list=0 neg0_sep_7493=0 neg0_sep_7920=1` · `AR-02 diagram=1 flow=1 card=1 faq=1 check=1 gate_row=1 new_mark=0` · `AR-02 ijson_neg0_lines=3 at=311,346,1033` · `AR-03 evidence_cited=0 old_row=1 linked=0`.
- `python3 scripts/validate-plugin.py api-kit` 종료 코드 0 (작성 시점).
- 마크다운 경고 기준값(markdownlint-cli2 0.23.2 · MD013 끔, scratchpad `mdlint/`): api-contract 21 · api-verify 33 · api-probe 15 · 원본 문서 11 · research-log 0. 대부분 레포 전체의 표 모양 규칙(MD060)이다. 페이지 너비 기준값(`page-overflow.cjs`): 375 · 1280 모두 `overflow=0`. 문서 검사 두 개(`check-docs-a11y.js` · `check-docs-links.py`) 종료 코드 0.

## Skill
- [ ] SK-01: api-contract 「## 2. I-JSON 게이트」 절의 코드 블록 목록에 `-0` 줄이 없고 noncharacter 줄은 그대로 있으며, 같은 절의 코드 블록 밖에 `-0` 을 따로 다루는 문장이 있어 `7920`(근거)과 `7493`(여기엔 없다는 설명)을 담는다 [exact] (측정: `SK-01 gate_block_neg0=0 nonchar_in_block=1 prose_neg0_7920>=1 prose_neg0_7493>=1` — prose 칸은 코드 블록 밖 줄만 센다. 음성 대조: 고치기 전 `gate_block_neg0=1 prose_neg0_7920=0`)
- [ ] SK-02: 세 목록 줄 — `api-contract`(「비교 기준선은 JCS」 줄) · `api-verify`(「I-JSON 게이트 실패(」 줄) · `api-probe`(「I-JSON 검문」 줄) — 모두 「-0 검사」 표시(백틱 · `<code>` 감싼 표기 포함)가 있고, 그 표시 앞(I-JSON 목록)에 낱개 `-0` 이 없으며 noncharacter 가 있다 [exact, enumerated] (측정: 줄마다 `found=1 mark=1 neg0_in_ijson=0 nonchar=1`. 음성 대조: 고치기 전 세 줄 모두 `mark=0 neg0_in_ijson=1 nonchar=0`)
- [ ] SK-03: api-verify 의 비교 파이프라인 줄이 `I-JSON 게이트` → 「`-0` 검사」 → `JCS 직렬화` 순서이고, 「`-0` 검사」 실패도 「비교 불가」 로 분류한다고 적은 줄이 있다 [exact] (측정: `SK-03 pipe_found=1 order_ok=1 neg0_class_noncomparable>=1`)
- [ ] SK-04: 킷 검사가 통과한다 — `python3 scripts/validate-plugin.py api-kit` 종료 코드 0, `python3 scripts/sync-docs.py --check-only` 종료 코드 0 [exact]

## Script
- [ ] SC-00: N/A (실행 스크립트 없음 — api-kit 의 I-JSON 게이트는 문서 규칙뿐이다. `find api-kit -type f \( -name '*.py' -o -name '*.sh' -o -name '*.js' \)` 0 개)

## Error
- [ ] ER-01: 분류는 바뀌지 않는다 — `-0` 은 여전히 봉인 불가 · 비교 불가이고 「경고」 나 「통과」 로 내려가지 않는다. api-contract §2 의 「게이트 실패는 계약 실패가 아니라 **봉인 불가**다」 문장이 `-0` 검사에도 걸린다고 읽히거나 같은 뜻의 문장이 `-0` 쪽에 있다 [goal] (측정: api-contract §2 원문 대조 — `sed -n '/^## 2\. I-JSON 게이트/,/^---/p' api-kit/skills/api-contract/SKILL.md` 를 읽어 `-0` 줄의 처리가 「실패」 이고 봉인 불가 문장의 적용 범위에 든다)

## Architecture
- [ ] AR-01: 원본 문서 `docs/api/contract/snapshot-sealing-canonicalization.md` §3 의 목록 문장에서 `-0` 이 빠지고 noncharacter 가 들어가며, 같은 절에 `-0` 을 따로 다루는 문장이 `7493`(여기엔 없음)과 `7920`(근거)을 담는다 [exact] (측정: `AR-01 list_found=1 neg0_in_list=0 nonchar_in_list=1 neg0_sep_7493>=1 neg0_sep_7920>=1`. 「Unicode 로 표현 불가한 문자열」 과 noncharacter 는 범위 경계의 결정대로 한 항목으로 합친다)
- [ ] AR-02: 문서 페이지 `docs/api-kit/snapshot-sealing-canonicalization.html` 에서 `-0` 을 I-JSON 항목으로 나열한 여섯 자리(`diagram` · `flow` · `card` · `faq` · `check` · `gate_row`)가 모두 0 이고, 「JCS 앞 `-0` 검사」 표시가 1 곳 이상이며, 페이지 전체에서 `I-JSON` 과 `-0` 이 한 줄에 같이 나오는데 그 줄이 「-0 검사」 표시로 갈라져 있지도 「I-JSON 규칙이 아니다」 류 설명도 없는 줄이 0 이다. 페이지 검사도 통과한다 [exact, enumerated] (측정: `AR-02` 첫 줄 여섯 칸 0 · `new_mark>=1`, 둘째 줄 `ijson_neg0_lines=0`; `node scripts/check-docs-a11y.js` · `python3 scripts/check-docs-links.py` 종료 코드 0; npx playwright 로 375 · 1280 너비에서 `document.documentElement.scrollWidth <= innerWidth`)
- [ ] AR-03: 근거가 남는다 — 근거 파일 `.harness/.meta/evidence/rfc7493-ijson-2026-09-26.md` 가 이 가지에 커밋돼 있고, `docs/api/research-log.md` 에 날짜 붙은 소제목의 새 절이 있어 이 결정 · 근거 파일 경로 · RFC 7493 §2.1 · 정정 7920 을 적고, 2026-09-24 표의 옛 줄(「I-JSON 게이트 목록 · `-0` 없음」) 뒤 10 줄 안에 2026-09-26 연결 표시가 있다 [exact] (측정: `git ls-files --error-unmatch` 종료 코드 0; `AR-03 evidence_cited>=1 old_row=1 linked>=1`)
- [ ] AR-04: 범위 — Given 이 계약의 봉인 커밋과 구현 커밋이 끝난 뒤, 구간 `cdadb10..chore/ak-api0` 의 바뀐 파일(`git diff --name-only cdadb10..chore/ak-api0`, 경로 한정 없음, 생성물 없음)이 정확히 위 대상 다섯 · 근거 파일 · `docs/api/research-log.md` · 이 계약 · 이 계약의 결과 파일 · 개정 파일(있으면) 집합 안에 있다 [exact, collective]

## Anti-patterns
- [ ] AP-03: bare code fence 금지 — 여는 fence 에 언어 힌트 필수 (측정: `python3 scripts/validate-plugin.py api-kit --check=code-fence` 종료 코드 0)
- [ ] AP-01: N/A (버전을 새로 적는 자리가 없다 — 킷 버전은 합친 뒤 release.sh 가 올린다. 측정: `git diff cdadb10..chore/ak-api0 -- api-kit | grep -cE '^\+.*v?0\.[0-9]+\.[0-9]+'` 0)

## Reusability
- [ ] RE-01: N/A (재사용 단위 코드 없음 — 바뀐 파일이 문서 · 페이지뿐이다)
- [ ] RE-02: N/A (재사용 단위 코드 없음 — 바뀐 파일이 문서 · 페이지뿐이다)

## Diagnostics
- [ ] DG-01: N/A (commands.analyze 는 scripts/release.sh 만 잰다 — 이번 변경 파일과 교집합 0. 실제 검사는 SK-04 · AR-02)
- [ ] DG-02: IDE diagnostics 워닝/인포 0개 (제외 없음. 측정: 바뀐 마크다운 넷을 markdownlint-cli2 0.23.2 · MD013 끔 설정으로 재서 고치기 전 수보다 늘지 않는다 — scratchpad `mdlint/`)
- [ ] DG-03: N/A (commands.test 는 release.sh 실행 — 이번 변경 파일과 교집합 0)
- [ ] DG-04: N/A (구동할 앱 · 서버 없음 — 문서 페이지 렌더 확인은 AR-02 가 한다)
