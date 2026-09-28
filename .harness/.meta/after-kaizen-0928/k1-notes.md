# k1 — 킷 약점 (api · bambu · onboarding · 설치본 안내)

- 계약: `.harness/sprint-contract-after-0928-kit-weaknesses.md` (28 조건, 봉인 `sha256:f05433dec1131ccc` · 측정 `sha256:5c70a649404879e3`, 봉인 커밋 `c8e2d0e`)
- 가지 `chore/ak3-k1`, 기준 `95508d9`. QA 판정 APPROVE (3 회째, 유효 조건 26 개 전부 PASS). 리포트 `.harness/sprint-feedback-after-0928-kit-weaknesses.md`.

## 항목별 결과

| 항목 | 결과 | 커밋 | 잰 값 |
| --- | --- | --- | --- |
| A15 | 예시 `ui.html` 에서 `users.me` 를 보류, `products.inventory` 를 flaky 로 두고 트리 줄과 `실패 원인` 탭 옆에 글자 표지와 `aria-label` 을 그린다. 리포트 요약 보류 · flaky 칸을 1 로 맞췄다 | `28b27b9` | `hold=1 flaky=1 misplaced=0` · `MATCH … ok=1`, 시험 8 → 12 통과. 자료를 지운 사본 · 그리는 줄을 지운 사본은 둘 다 rc=1 |
| B5 | 시험 러너가 표의 `[미검증]` 줄 수까지 잰다. 설치본이 없으면 그 기대를 일치로 세지 않고 건너뜀으로 적는다 | `680ba88` · `c56d720` · `f1d45d1` | 이 맥 `24 경우 중 불일치 0`. 설치본 없는 사본 `불일치 0 · 건너뜀 19`. m1~m4 사본 넷 모두 rc=1 에 이름이 나온다 |
| B6 | G5 가 줄 앞 공백 · 인용 속 표 · 굵은 머리 · U+00A0 / U+3000 · U+00A0 하나뿐인 칸을 읽고, 네 낱말이 든 네 칸 아닌 표는 `unrecognized` 로 FAIL 한다 | `03a3e0a` · `c56d720` · `85f8ffd` · `2219738` · `56f3356` | 변형 30 개 zsh · bash · 도커 mawk 모두 `diff=0`. 시험 12 → 20, `SHAPES covered=7/7 crlf_cases=2` |
| B11 | 파일 60 개에 raw 주소 안내 줄을 넣고 레포 검사 `scripts/check-install-docs-guidance.py` 를 CI 에 등록했다 | `97a9505` · `8166e9d` · `9b34255` · `b1f84c0` · `a020ed0` · `bdd8064` · `e5a284c` · `0a21704` | `TOTAL files=94 ok=73 need=0 exempt=21`, 안내 줄 61 줄 전부 두 문구 포함, `PATHS … missing=0` |
| B21 | 예시 주소를 코드 글자로, N-12 를 제목에서 글 줄로 | `9b34255` · `893bbf1` | `<https://` 0 · 코드 글자 1, §6 `###` 제목 4 개, 경고 0 |
| D7 | SKILL.md 와 문서 쪽 버전 대조 표를 `02.08.02.61` 과 옵션 목록 `bambu-02.08.02.61.tsv` 기준으로 | `680ba88` · `c56d720` | 두 쪽 모두 옛 기준 문구 0, 넘침 0 |

B5 에서 계약 밖 사실 하나를 찾았다. 표는 `process-thin-unreadable-slot.json` 을 `[미검증]` 1 줄로 적었지만 실제 출력은 2 줄이다(슬롯 1 못 읽음 + 벽 예산 미기록). 러너가 줄 수를 재기 시작하자 드러났다. 시험 파일은 범위 밖이라 표를 실제 출력에 맞췄다(SKILL.md · 문서 쪽 둘 다, AR-03 `diff=0`).

## 킷 버전 판단

모두 고침(patch)이다 — api-kit · howto-kit · planning-kit · react-kit · rust-kit · bambu-kit · onboarding-kit · tone-kit. 이 작업에서는 판 번호를 올리지 않는다. 릴리스는 합친 뒤 main 에서 한다.

## 로컬 CI

- `ci-local.sh` 25 단계 rc=0 (feedback-agg-test 는 yq 가 없어 건너뜀)
- CI 파일에만 있는 여섯(check-api-kit-docs · detect-docs-drift --check-table · check-cause-table-copies · measure-helpers-test · makerworld-fetch-test · check-install-docs-guidance) rc=0
- `npx playwright test` 168 통과, `validate-plugin.py` 「14 plugins, 14 OK」

## 독립 검토가 짚은 두 가지

- 막는 결함: 슬라이서 없는 기계에서 `[미검증]` 줄 수를 건너뛰는 분기가 판정 결과를 보지 않아, 판정 불일치까지 「건너뜀」 으로 숨었다. `f1d45d1` 에서 판정이 맞았을 때만 건너뛰게 고쳤다. 검토가 만든 망가뜨린 사본(`filament-lattice-fanfix.json` 기대를 FAIL 로 바꾸고 슬라이서 경로를 없앤 것)으로 다시 재니 `불일치 1 · 건너뜀 18` 로 잡는다. 망가뜨리지 않은 사본은 `불일치 0 · 건너뜀 19`.
- 막지 않는 결함(B6 일부만 고침): 밑줄 굵은 머리 · 기울인 머리 · 양 끝 `|` 없는 표를 G5 가 못 읽고 PASS 로 흘렸다. `85f8ffd` 에서 셋 다 읽게 고치고 음성 입력 셋을 시험에 더했다(`2219738` 문서 쪽 사본 맞춤, `56f3356` 새 입력의 마크다운 경고). `run-gate-evals.sh` 에서 셋 다 기대대로 FAIL 로 판정해 PASS.

## 남은 것

- remaining.md 의 A1 · A2 · A3 · B12~B20 · D1 · D3 은 어느 작업 폴더 계약에도 없다. k1 은 여섯 항목만 맡았다. 배정은 부모 세션이 정한다.
- `api-kit` 예시 계약 파일(`contracts/users.me.yaml`)에는 baseline 블록이 없어 「pending」 이 리포트 글로만 적혀 있다. 계약 파일에 baseline 을 새로 적는 것은 예시 계약 모양을 바꾸는 일이라 하지 않았다.
- `process-thin-unreadable-slot.json` 이 벽 예산 미기록 알림까지 내는 것은 시험 파일에 `_wall_budget_short_share` 가 없어서다. 한 가지만 재는 입력으로 좁히려면 시험 파일을 고쳐야 하는데 이번 범위 밖이다.
- 계약 SC-01 은 슬라이서가 설치된 이 맥에서만 잰다. 슬라이서 없는 쪽은 조건으로 잠겨 있지 않아, 위 막는 결함 같은 것은 독립 검토에서만 드러났다. 다음 계약에서 슬라이서 없는 사본 대조를 조건으로 넣을 만하다.
