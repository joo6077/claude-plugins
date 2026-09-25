# 카이젠 2026-09-24 Phase 16 (api-kit) — 계약 초안 독립 검토

- 대상: `.harness/sprint-contract-kaizen-0924-p16-api-kit.md` (봉인 전, 추적 안 된 파일, 761 줄, 조건 29 · 기능 조건 19, sha256 앞 16 자리 `a2548add84181b1e`)
- 개정 파일 `.harness/sprint-amendments-kaizen-0924-p16-api-kit.md` 은 아직 없다 — 봉인 전이라 맞다
- 검토자: REVIEW 에이전트 (사용자 승인 대신, 러닝북 「사용자 승인(5 단계) 대체」)
- 검토일: 2026-09-25

## 결론

네 군데를 고치면 봉인할 수 있다. 측정 정의 블록 다섯은 계약에서 새로 뽑아 DRAFT(초안 담당 에이전트)의 `p16d/k/` 와 바이트 단위로 같았고,
예행 저장소 두 벌에서 내가 다시 잰 값도 계약의 `봉인 전 실측` 표와 같았다. 처리 배정표 두 행 · 범위 · 공유 파일 · 조건끼리의 충돌에서는
막을 문제를 못 찾았다. 고칠 것은 둘이 보안 · 측정 구멍이고 둘이 글의 정확도 · 절차 누락이다.

1. **SK-05 가 `.api/` 폴더를 통째로 웹 서버에 올리라고 시킨다.** 새 §7 1 번 항목의 명령이 `python3 -m http.server 8765 --bind 127.0.0.1 --directory .api` 다.
   `.api/` 에는 `credentials.local.json`(아이디 · 비밀번호, 권한 0600 — `api-kit/references/api-layout.md:14`) · `reports/`(가리지 않은 원본 응답 —
   `docs/api/research-log.md` 2026-09-05 표) · `snapshots/prod/`(실제 고객 자료)가 있다. 이 명령은 폴더 목록 화면까지 열어 그 파일들을 같은 기계의
   누구에게나 HTTP 로 내준다 — 0600 권한이 소용없어진다. `ui.html` 은 자료를 전부 안에 담은 한 장짜리라 그 한 장만 빈 폴더에 복사해 올리면 된다.
   덤으로 한 장만 든 폴더에서는 옆 파일 `fetch` 가 404 콘솔 오류로 드러나, 초안이 「웹 서버로 열면 성공해 버린다」 고 적은 결함을 브라우저 확인이 잡게 된다(아래 재현 5).
2. **ER-01 이 이 Phase 가 고칠 수 있는 근거 파일을 끝 판에서 읽는다.** 근거 파일 `.harness/.meta/evidence/phase16.md` 는 `.harness/` 안이라 AR-01 이 편집을 막지 않는다.
   strictness-modes 사본에 가짜 URL 을 넣고 같은 URL 을 끝 판 근거 파일 사본에도 한 줄 덧붙이자 첫 줄이 `1` 에서 `0` 으로 돌아갔다(재현 2).
   Phase 15 검토(`phase15-review.md` 1 번)가 같은 구멍을 잡았는데 이 초안에 다시 나왔다. 근거 파일은 시작 커밋보다 앞선 `43fc9ee` 에 들어왔고
   시작 커밋 뒤로 바뀌지 않았다 — 시작 커밋 판에서 읽고, 끝 판이 같은지를 따로 잰다.
3. **SK-09 새 문장이 「`--secret` 이 가리는 곳은 stderr 로그와 `report.json` 뿐」 이라고 못박는데 틀렸다.** 근거 파일 L5 는 `--curl <파일>` 도 가린다고 적었고,
   이 계약이 넣는 research-log 새 절(`rl-append.md`)도 「`--curl <파일>` … 도 등록한 시크릿을 `***` 로 가렸다」 고 쓴다. 같은 커밋 안에서 킷 문서끼리 어긋난다.
   hurl 8.0.1 로 다시 쟀다 — 시크릿으로 건 판은 `--curl` 파일에 `Bearer ***`(평문 0 줄), 같은 값을 변수로 건 대조 판은 평문 1 줄(재현 3).
   네 자리(api-verify · api-ui · api-probe · README)의 「뿐 / 만」 을 「가린다고 확인된 곳」 으로 바꾼다. 가리는 곳을 적게 말하는 쪽이라 새는 위험은 없지만,
   오케스트레이터 Phase 16 줄의 「문서 기재와 실측이 어긋나면 실측을 채택한다」 를 이 Phase 가 스스로 어기는 모양이 된다.
4. **api-kaizen 스킬 Step 1 · Step 5(사전 · 사후 측정)가 빠졌다.** 러닝북 「입력」 4 번은 카이젠 스킬 파일의 절차를 따르라고 하고, 그 스킬 Step 1 은
   「서술로 대체하지 마라」 고 적는다. 계약 `GAP 분석` 의 「Step 1」 은 sprint-contract 의 복잡도 판정이지 api-kaizen Step 1 이 아니다.
   notes 에 표 하나를 넣고 ER-03 이 그 절 머리를 재면 된다. 값은 내가 미리 쟀다(아래 C4).

넷 다 고칠 문구를 아래에 적었다. 조건 줄 수(29)는 그대로다. 고치면 `APPROVE` 다.

## 다시 돌려 본 것

모두 스크래치 `p16review/` 아래에서만 돌렸다. 작업 폴더에는 이 파일 하나만 썼다. 띄운 `srv.py` 는 갈래마다 내렸다(끝난 뒤 `pgrep` 0).

1. 계약의 코드 블록 다섯(`common.sh` · `m.sh` · `rule-delta.sh` · `srv.py` · `probe.js`)을 새로 뽑아 `p16d/k/` 와 `cmp` — 다섯 다 같다.
   `mock.py` sha256 앞 16 자리 `638c2c8c0c9f1904`, 확정 시안 `c4bd563ec8b71a95` 둘 다 계약 값과 같다.
2. 예행 판 `rh-base` 에서 `m` 스물넷(SK-01 ~ SK-11 · ER-01 ~ ER-03 · AR-01 ~ AR-03 · AP-01 · AP-03 · AP-04 · DG-02 · DG-05 · DG-06 · NA)을 다시 돌렸다 — 표와 전부 같다.
   시작 커밋 판 `rh-start` 에서 SK-01 · SK-06 · SK-08 도 표와 같다(`EXPR_MISSING` 포함). DRAFT 의 `out-del.txt`(토큰 98 개 모두 값이 떨어짐, SAME 0 · MISSING 0)와
   `out-ctl.txt`(양성 · 음성 대조)도 표의 「대조」 칸과 같다.
   - ER-01 구멍: 원래 `0` · `0` → strictness-modes 에 `https://example.invalid/p16-fake` → `1` · `0` → 같은 URL 을 끝 판 근거 파일에도 → `0` · `0`.
     고친 측정(C2)으로는 마지막 경우가 `1` · `0` · `evid_same=0`, 예행 판 그대로는 `0` · `0` · `evid_same=1`, 시작 커밋 판은 `0` · `NOTES_MISSING` · `evid_same=1`.
3. `--curl` 파일 마스킹: `srv.py` 의 `/fx/sec` 에 `Authorization: Bearer {{tok}}` 를 보내는 케이스로 `--secret tok=sekret-p16 --curl c.curl` → `rc=0`, 파일 안 평문 0 · `Bearer ***` 1.
   대조로 `--variable tok=sekret-p16` 로 건 판 → 평문 1. SK-09 의 옛 글 검사에 넣을 두 글(`` `report.json` 뿐 `` · `` `report.json` 만 가리 ``)을 세어 보니
   예행 판 `3 1`, 시작 커밋 판 `0 0`.
4. 뷰어 스펙 CSP(페이지가 불러올 수 있는 자원을 제한하는 규칙): 확정 시안의 `Content-Security-Policy` 는 0 줄이다. 뷰어 스펙 §1 의 CSP `<meta>` 를 `<head>` 바로 뒤에 넣은
   사본을 `m SK-06` 과 같은 길로 돌린 줄 — `csp chromium ep=14 shown=14 targets=56 under24=0 under44=39 err_other=0 err_favicon=0`.
   식 값은 같고, 아이콘을 부르는 크로미엄에서도 `favicon.ico` 404 가 아예 안 나왔다. 식은 `'unsafe-eval'` 없는 CSP 아래서도 돌았다.
5. 한 장 폴더: 확정 시안 사본 끝에 `fetch("./data.json")` 를 넣고 `ui.html` 한 장만 든 폴더를 띄웠다 — 헤드리스 셸에서 콘솔 error
   `Failed to load resource: … 404` 1 건(`/data.json`). CSP 를 넣은 사본은 `connect-src 'none'` 위반 error 3 건. 둘 다 콘솔 확인이 잡는다.
6. api-kaizen Step 1 명령(스킬 본문 그대로)을 두 판에서 돌렸다 — C4 표.
7. 덤으로 확인한 것: 첫 CSP 실행을 zsh 에서 `set -- $q` 로 돌렸더니 낱말이 안 쪼개져 주소가 `csp chromium.html` 이 되고 `EP is not defined` 가 났다.
   `common.sh` 머리의 `NOT_BASH` 멈춤이 이 함정을 막는다는 확인이다. `ps` 에 보이는 `python3 srv.py`(PID 75318)는 2026-09-05 부터 떠 있는 다른 세션 것이다 —
   DRAFT 의 `srv.pid`(40907)는 살아 있지 않다.

## 꼭 고칠 것 — 봉인 전에

`mock.py` 가 쓰는 글, `m.sh` 의 같은 ID 갈래 토큰, 계약 조건 줄, `봉인 전 실측` 표의 그 행을 함께 고친다. 새 글에는 번역투 6 종 · 새 이름이 없다(ER-02 · K-11 기준으로 봤다).

### C1 — SK-05 (b) · SK-07 (d): 한 장만 든 빈 폴더를 올린다

api-ui `SKILL.md` §7 의 1 번 항목을 이 글로 바꾼다.

```text
1. **여는 방법** — 브라우저 조종 도구 가운데 기본 설정에서 `file://` 주소를 막는 것이 있다(오류 예: `Access to "file:" protocol is blocked`). `D=$(mktemp -d) && cp .api/ui.html "$D/" && python3 -m http.server 8765 --bind 127.0.0.1 --directory "$D"` 로 `ui.html` 한 장만 든 빈 폴더를 띄우고 `http://127.0.0.1:8765/ui.html` 을 열거나, 도구의 로컬 파일 허용 설정을 켜고 `file://` 로 연다. 어느 쪽으로 열었는지 보고에 적는다. `.api/` 를 통째로 띄우지 마라 — `credentials.local.json`(아이디 · 비밀번호) · `reports/`(가리지 않은 원본 응답) · `snapshots/prod/` 가 HTTP 로 열리고, 출처가 `http://127.0.0.1` 로 바뀌어 옆 파일 `fetch` 가 성공해 버린다. 한 장만 든 폴더에서는 옆 파일 `fetch` 가 404 콘솔 오류로 드러난다(실측 2026-09-25). 그래도 외부 참조 0 건은 위 `grep` 검사로 잰다 — 브라우저 확인으로 대신하지 마라.
```

`m.sh` `SK-05)` 갈래 — 첫 `toks` 의 둘째 · 셋째 · 넷째 토큰을 아래 셋으로 바꾸고 넷째 줄을 하나 더해 토큰을 열하나로 만든다.

```text
'1. **여는 방법** — 브라우저 조종 도구 가운데 기본 설정에서 `file://` 주소를 막는 것이 있다(오류 예: `Access to "file:" protocol is blocked`).'
'`D=$(mktemp -d) && cp .api/ui.html "$D/" && python3 -m http.server 8765 --bind 127.0.0.1 --directory "$D"` 로 `ui.html` 한 장만 든 빈 폴더를 띄우고 `http://127.0.0.1:8765/ui.html` 을 열거나, 도구의 로컬 파일 허용 설정을 켜고 `file://` 로 연다. 어느 쪽으로 열었는지 보고에 적는다.'
'`.api/` 를 통째로 띄우지 마라 — `credentials.local.json`(아이디 · 비밀번호) · `reports/`(가리지 않은 원본 응답) · `snapshots/prod/` 가 HTTP 로 열리고, 출처가 `http://127.0.0.1` 로 바뀌어 옆 파일 `fetch` 가 성공해 버린다.'
'한 장만 든 폴더에서는 옆 파일 `fetch` 가 404 콘솔 오류로 드러난다(실측 2026-09-25). 그래도 외부 참조 0 건은 위 `grep` 검사로 잰다 — 브라우저 확인으로 대신하지 마라.'
```

같은 갈래 `echo "rows=…"` 줄 끝에 한 칸 띄우고 `dir_api=$(grep -cF -- '--directory .api' "$E/$U")` 를 붙인다.

SK-05 조건 줄 (b) 를 이렇게 바꾼다 — 「(b) 여는 방법 — `file://` 를 막는 조종 도구가 있다는 오류 예, `ui.html` 한 장만 든 빈 폴더를 `127.0.0.1` 웹 서버로 띄우거나
로컬 파일 허용 설정 · 어느 쪽으로 열었는지 보고, `.api/` 를 통째로 띄우지 말라는 문장(`credentials.local.json` · `reports/` · `snapshots/prod/` 가 열리고 옆 파일
`fetch` 가 성공한다), 한 장 폴더에서는 옆 파일 `fetch` 가 404 콘솔 오류로 드러나도 외부 참조는 `grep` 으로 잰다는 문장이 각각 1 줄 이상이고 `--directory .api` 는 0 줄」.
측정 문구는 「세 줄이 `1` 열하나 · `rows=1 js=1 old=0 dir_api=0` · `1`. 알려진 답: 시작 커밋 판 `0` 열하나 · `rows=0 js=0 old=1 dir_api=0` · `0`.
문장 삭제 대조: 토큰 열둘. 양성 대조: 초안 첫 판 글(`--directory .api`)을 되살린 사본에서 `dir_api=1`」 로.

뷰어 계약 문서 `## Gotchas` 의 브라우저 확인 Gotcha 앞 두 조각을 바꾼다(`favicon.ico` 두 조각은 그대로). 문장 전체는 이렇게 이어진다.

```text
- **브라우저로 여는 확인은 글자 검사를 대신하지 못한다** — 브라우저를 조종하는 도구 가운데 기본 설정에서 `file://` 주소를 막는 것이 있어(실측 오류 `Access to "file:" protocol is blocked`) `127.0.0.1` 웹 서버로 열게 된다. `.api/` 폴더를 통째로 띄우면 출처가 `http://127.0.0.1` 로 바뀌어 `file://` 에서 막히는 옆 파일 `fetch` 가 성공해 버리고 `credentials.local.json` · `reports/` 까지 HTTP 로 열린다 — `ui.html` 한 장만 든 빈 폴더를 띄운다. 외부 참조 0 건은 계속 글자 검사로 잰다. (이하 favicon.ico 문장 둘 그대로)
```

`m.sh` `SK-07)` 갈래 넷째 `toks` 의 앞 두 토큰:

```text
'- **브라우저로 여는 확인은 글자 검사를 대신하지 못한다** — 브라우저를 조종하는 도구 가운데 기본 설정에서 `file://` 주소를 막는 것이 있어'
'`.api/` 폴더를 통째로 띄우면 출처가 `http://127.0.0.1` 로 바뀌어 `file://` 에서 막히는 옆 파일 `fetch` 가 성공해 버리고 `credentials.local.json` · `reports/` 까지 HTTP 로 열린다 — `ui.html` 한 장만 든 빈 폴더를 띄운다.'
```

SK-07 조건 줄 (d) 괄호는 「(`file://` 차단 → 웹 서버 · `.api/` 를 통째로 띄우면 `fetch` 가 성공하고 아이디 · 비밀번호 파일이 열리니 한 장 폴더 · `favicon.ico` 404 · 헤드리스 셸은 아이콘을 안 부른다)」 로.
값(`1 1 1 1`)은 그대로다.

### C2 — ER-01: 근거 파일은 시작 커밋 판에서 읽는다

`m.sh` `ER-01)` 갈래를 이것으로 바꾼다(재현 2 에서 돌린 판).

```bash
  ER-01)  # 새로 생긴 URL 이 근거 파일에 있다 — 파일마다 편집 전 판과 비교, notes 는 URL 전부
    # 근거 파일은 .harness 안이라 이 Phase 가 고칠 수 있다 — 시작 커밋 판에서 읽고, 끝 판이 같은지 따로 잰다
    for f in "${FILES[@]}"; do comm -13 <(url < "$T/B/$f") <(url < "$E/$f"); done | sort -u | comm -23 - <(url < "$T/B/$EVID") | grep -c .
    if [ -f "$E/$NOTES" ]; then url < "$E/$NOTES" | comm -23 - <(url < "$T/B/$EVID") | grep -c .; else echo NOTES_MISSING; fi
    cmp -s "$T/B/$EVID" "$E/$EVID" && echo evid_same=1 || echo evid_same=0 ;;
```

ER-01 조건 줄 — 「… URL 이 전부 **시작 커밋 판**의 외부 근거 파일 `.harness/.meta/evidence/phase16.md` 에 있고, 끝 판 근거 파일이 시작 커밋 판과 같다 —
근거 파일은 `.harness/` 안이라 이 Phase 가 고칠 수 있으므로 끝 판에서 읽지 않는다. 파일마다 편집 전 판과 비교한다 …」.
측정 「세 줄이 `0` · `0` · `evid_same=1`」. 양성 대조에 한 줄 더 — 「strictness-modes 사본과 끝 판 근거 파일 사본에 같은 가짜 URL 을 넣은 사본에서
`1` · `0` · `evid_same=0`」. `봉인 전 실측` 표 ER-01 행도 이 값으로. AR-02 (d) 의 `| L7 |` 도 `$T/B/$EVID` 에서 읽으면 같은 틈이 닫힌다(값은 `1` 그대로).

### C3 — SK-09: 「뿐 / 만」 을 「가린다고 확인된 곳」 으로

네 자리를 이렇게 바꾼다. 뒤따르는 「가리지 않는다」 목록은 그대로다.

| 파일 | 바꾸기 전(초안) | 바꾼 뒤 |
| --- | --- | --- |
| api-verify `## Gotchas` | Hurl `--secret` 이 exact match 로 가리는 곳은 **stderr 로그와 JSON 리포트의 `report.json` 뿐**이다 | Hurl `--secret` 이 exact match 로 가린다고 확인된 곳은 **stderr 로그 · JSON 리포트의 `report.json` · `--curl` 파일**이다(실측 2026-09-05 · 2026-09-24) |
| api-ui `## Gotchas` | Hurl 의 `--secret` 이 exact match 로 가리는 곳은 stderr 로그와 JSON 리포트의 `report.json` 뿐이다(실측 2026-09-05). | Hurl 의 `--secret` 이 exact match 로 가린다고 확인된 곳은 stderr 로그 · JSON 리포트의 `report.json` · `--curl` 파일이다(실측 2026-09-05 · 2026-09-24). |
| api-probe `## Gotchas` | `--secret` 이 마스킹하는 건 stderr 로그와 JSON 리포트의 `report.json` 뿐이다(실측 2026-09-05). | `--secret` 이 가린다고 확인된 곳은 stderr 로그 · JSON 리포트의 `report.json` · `--curl` 파일이다(실측 2026-09-05 · 2026-09-24). |
| `api-kit/README.md` | Hurl `--secret` 은 stderr 와 JSON 리포트의 `report.json` 만 가리고 stdout · … | Hurl `--secret` 은 stderr · JSON 리포트의 `report.json` · `--curl` 파일을 가리지만 stdout · `--output` 파일 · 리포트의 원본 응답 파일(`store/`)은 가리지 않는다 |

`m.sh` `SK-09)` 갈래의 네 토큰(api-verify 첫 토큰 · api-ui 첫 토큰 · api-probe 첫 토큰 · README 토큰)을 오른쪽 칸 글로 바꾼다 — api-verify 토큰은
「… `--curl` 파일**이다」 까지. 마지막 `oldn` 에 두 글 `` '`report.json` 뿐' `` · `` '`report.json` 만 가리' `` 를 더한다.
SK-09 조건 줄 — (a) 첫 조각을 「가린다고 확인된 곳은 stderr 로그 · `report.json` · `--curl` 파일」 로, (d) 를 「README 한 줄(`--curl` 파일 포함)」 로,
(e) 에 「가리는 곳을 다 적은 것처럼 말하는 두 글(`` `report.json` 뿐 `` · `` `report.json` 만 가리 ``)」 을 더해 옛 글 일곱.
측정 다섯째 줄 `old=0 0 0 0 0 0 0`. 알려진 답: 시작 커밋 판 `old=2 1 1 1 1 0 0`. 양성 대조: 초안 첫 판 글에서 `old=0 0 0 0 0 3 1`(재현 3).
근거는 근거 파일 L5 와 research-log 새 절 — URL 은 늘지 않는다.

### C4 — ER-03 (a): notes 에 api-kaizen Step 1 · Step 5 표

notes 에 `## 사전 · 사후 측정 (api-kaizen Step 1 · 5)` 절을 두고, 스킬 Step 1 명령을 시작 커밋 판과 `$END` 판에서 돌린 출력을 표로 넣는다. 예행 판 값은 이렇다.

| 스킬 | 시작 커밋 gotchas · steps | 예행 판 gotchas · steps |
| --- | --- | --- |
| api-init | 10 · 9 | 10 · 9 |
| api-probe | 12 · 9 | 12 · 9 |
| api-contract | 10 · 12 | 10 · 12 |
| api-verify | 10 · 12 | 12 · 12 |
| api-ui | 20 · 9 | 20 · 9 |

api-verify 의 +2 는 새 Gotcha 가 아니라 §6 에 더한 굵은 불릿 둘이다 — Step 1 명령(`grep -c '^- \*\*'`)이 파일 전체의 굵은 불릿을 세기 때문이다. 이 한 줄을 표 아래에 적는다.
Step 5 의 음성 대조는 계약의 문장 삭제 대조(`del.sh`)와 양성 · 음성 대조(`ctl.sh`)를 가리키면 된다.
ER-03 조건 줄 (a) 의 절 머리 목록에 `## 사전 · 사후 측정` 을 더해 여덟로, `m.sh` `ER-03)` 갈래 첫 `toks` 에 `'## 사전 · 사후 측정'` 을 더해 둘째 줄이 `1` 열이 된다.
음성 대조: 그 절 머리를 지운 notes 사본에서 둘째 줄 열째 값 `0`.

### 반영 뒤 BUILD(봉인 · 구현 담당 에이전트)가 봉인 전에 다시 돌릴 것

1. `mock.py` 를 고치고 `rehearse.sh base` 로 예행 저장소를 새로 만든 뒤 `runall.sh` 전체, `rh-start` 전체 — 바뀐 행(SK-05 · SK-07 · SK-09 · ER-01 · ER-03)을 표에 다시 적는다
2. `del.sh` SK-05 · SK-07 · SK-09 · ER-03 — SAME 0 · MISSING 0
3. `ctl.sh` 에 새 대조 셋(ER-01 근거 파일 동시 편집 · SK-05 `--directory .api` 되살림 · SK-09 초안 첫 판 글)
4. DG-02 열일곱 줄 `rules_up=0`, ER-02 `k02=0 names=0` — 새 글이 목록 · 표 옆에 들어간다
5. `mock.py` sha256 앞 16 자리가 바뀌니 계약 91 줄 값도 고친다

## 고치면 좋은 것 — 판정에 넣지 않는다

1. **CSP 사본 한 줄을 SK-06 에 더한다.** 실제로 만들어질 뷰어는 스펙대로 CSP 가 든 쪽인데 확정 시안에는 없다(재현 4). `m.sh` `SK-06)` 의 파이썬 사전에
   `"csp": ("<head>", "<head><meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'\">")`
   를 넣고 반복 목록 끝에 `"csp chromium"` 을 더하면 여섯째 줄이 `csp chromium ep=14 shown=14 targets=56 under24=0 under44=39 err_other=0 err_favicon=0` 이다(내가 돌린 값).
   같이 뷰어 계약 문서 Gotcha 끝에 「뷰어 스펙의 CSP `<meta>`(`img-src data:`)를 넣은 사본에서는 이 한 건도 나오지 않았다(실측 2026-09-25).」, research-log 브라우저 표에
   「콘솔 error — 뷰어 스펙 CSP `<meta>` 를 넣은 사본 | 0」 행을 두면 좋다. notes `## 다음 사이클 메모` 에는 「확정 시안에 뷰어 스펙 §1 의 CSP `<meta>` 가 없다 ·
   §7 글자 검사가 CSP `<meta>` 가 있는지를 재지 않는다」 두 줄.
2. **hurl 판이 바뀌면 멈추게 한다.** SK-02 (d) · SK-08 (e) 는 이 기계의 hurl 8.0.1 동작에 묶여 있다. 갈래 머리에
   `hurl --version | head -1 | grep -q '^hurl 8\.0\.1 ' || { echo "HURL_VERSION_CHANGED"; return 2; }` 를 두면 QA 전에 판이 올라갔을 때 구현 탓 FAIL(실패)이 아니라
   측정 멈춤으로 드러난다(Phase 12 검토 1 번과 같은 모양).
3. **research-log 새 절에 셈 기준 한 줄.** 근거 파일 L7 은 같은 시안에서 누르는 요소를 59 개로 셌고 이 절 표는 56 이다. 셀 대상을 고르는 기준이 달라서다
   (§7 식으로 세면 버튼 53 · 입력 3, 역할 요소는 버튼과 겹친다). 또 표의 「실측 2026-09-24」 가운데 `targets 56` 과 hurl 재측정은 2026-09-25 에 돌렸다 —
   절 머리에 「실측은 2026-09-24(근거 수집)와 2026-09-25(계약 초안 · 검토)에 돌렸다」 한 줄이면 된다.
4. **뷰어 스펙 §1 누르는 자리 행의 「위반 시」 칸.** 「WCAG 2.2 2.5.8 (AA) 미달」 이라 적었지만 요소 상자만 재는 이 기준은 2.5.8 의 간격 예외를 안 보므로 그보다 엄하다.
   「요소 상자만 재므로 WCAG(웹 접근성 지침) 2.5.8 보다 엄하다 — 24 미만이면 간격 예외를 따지기 전에 고친다」 쪽이 정확하다. SK-07 (a) 토큰이 걸려 있어 바꾸면 토큰도 같이.
5. **hurl-execution §6 표에 `--curl <file>` 행.** C3 과 맞추려면 가려지는 곳 칸에 「`--curl <file>` (실측 2026-09-24)」 한 행. SK-08 로 어차피 고치는 파일이다.
6. **다음 사이클 메모 후보 — 화면에 안 보이게 숨긴 1 px 요소.** §7 식은 크기가 0 보다 크면 보이는 것으로 친다. 화면 읽기 프로그램용으로 1×1 px 로 숨긴 입력칸이
   생기면 `under24` 가 1 이 되어 멀쩡한 뷰어가 떨어진다. 확정 시안에는 없다(재현 4 의 `under24=0`).
7. **ER-03 (d) 는 서명 없는 남의 커밋도 이 Phase 탓으로 센다.** 지금 구간(`3a348d6..HEAD`)의 커밋 열하나는 전부 `Kaizen-Phase:` 서명이 있고 넘김 경로를 건드린 커밋은 0 이다.
   QA 때 오케스트레이터가 서명 없이 `scripts/` 등을 고친 커밋이 끼어 있으면 개정 파일로 그 커밋을 적어 가른다.

## 확인만 하고 넘어간 것

1. **조건마다 실패를 한 문장으로 쓸 수 있는가.** 된다. 예: SK-01 「§6 에 아홉 문장 가운데 하나가 없거나 옛 문장 「`.hurl` 로 표현되지 않은」 이 남았다」,
   SK-06 「끝 판 §7 식을 시안 사본에 돌린 다섯 줄 가운데 하나라도 적힌 값과 다르다」, AR-03 「확정 결정 여덟 줄 가운데 하나가 시작 커밋 판과 글자가 다르거나
   열일곱 밖 킷 · 문서 파일이 하나라도 바뀌었다」, DG-06 은 다른 Phase 몫을 가르는 단서까지 조건 줄에 있다.
2. **처리 배정표 Phase 16 행.** `other-kits:P7` → SK-01 ~ SK-04, `other-kits:P8` → SK-05 ~ SK-07, 적용 힌트 「화면 확인 숫자를 보고에 인용」 → SK-05 (h) · §8.
   러닝북 `Phase 별 추가 과제` 에 Phase 16 줄은 없다. 오케스트레이터 Phase 16 줄의 확정 결정 여섯은 AR-03 이 글자 그대로 잡고, 「Hurl assert 로 표현할 수 없다」 는
   실측(근거 파일 L1)과 달라 결론(후처리)은 두고 이유만 고쳤다 — 오케스트레이터 파일 · 설계문서 `:249` 는 ER-03 넘김. 근거 파일 §4 권장 열셋 가운데 12 · 13 번(선택)은
   research-log 이월 절과 ER-03 (c) 로 미반영 사유가 남는다.
3. **범위.** 고치는 열일곱이 전부 `api-kit/` · `docs/api/` 안이고 나머지는 `.harness/` 다 — Phase 표의 고쳐도 되는 범위 안이다. 범위 선언 블록 모양과 `FILES` 가 같은지
   AR-01 ⑤가 잰다. 공통 폴더 `api-kit/references/` 는 안 건드린다.
4. **공유 파일.** 마켓플레이스 · `plugin.json` 버전 · 루트 문서 · `docs/` HTML · `ci.yml` · 처리 배정표 · 등록부를 건드리지 않고 notes 로 넘긴다. 서명 커밋은 AR-01 ②,
   서명 없는 커밋은 ER-03 (d) 가 경로로 직접 센다. 예행 변형 넷에서 잡히는 것을 다시 확인했다. `scripts/detect-docs-drift.py` 에 `docs/api` 매핑이 없어 Final 문서 재생성이
   이 여섯 페이지를 놓칠 수 있다는 점도 ER-03 (b) 넘김에 들어 있다.
5. **조건끼리 충돌.** SK-01 (d) · SK-03 (c) 가 0 을 요구하는 옛 글과 새 글은 글자가 다르다. SK-07 (e) 가 막는 `44px` 는 SK-05 · SK-07 새 글(「44 는 권장」)에 없다.
   SK-03 · SK-10 이 고치는 api-contract Gotcha 줄과 AR-03 이 고정하는 확정 결정 줄은 다른 줄이다(예행 판 `1 1 1 1 | 1 1 1 1`). 옛 글 검사 넷(SK-03 · SK-07 · SK-08 · SK-09)의
   시작 커밋 값이 끝 판에서 0 이 되면서 AR-03 `outside_changed=0` 이므로, 옛 글이 전부 열일곱 안에 있었다 — ER-03 · AR-03 과 부딪히지 않는다. C1 ~ C4 도 새 충돌을 만들지 않는다
   (새 글에 `44px` · 「클릭 타깃」 · 번역투 없음, 새 URL 없음).
6. **러닝북 측정 규칙.** 상한을 변수로 받고 못 구하면 멈춘다(`END_UNRESOLVED`). 도우미 함수가 없으면 멈춘다(`HELPER_MISSING`). 파일마다 옛판과 비교한다(ER-01 · AR-03 · DG-02).
   편집기 경고는 규칙별로 편집 전 판과 비교한다. `validate-plugin.py` 는 종료 코드로, 옛 값은 열일곱 파일에 직접 센다. 문장 삭제 대조가 토큰 98 개 전부에 돌았다.
   두 판을 `git archive` 로 풀어 작업 폴더의 남의 미커밋 변경(지금 다른 Phase 계약 파일 여럿이 `M`)이 끼지 않는다.
7. **사용자 결정 대신 판단(근거 파일 §5 열린 질문 1 · 2).** 두 결정에 동의한다.
   - `판정 불가` 를 통과선 검사에 넣지 않는다 — 사라진 경로가 계약상 필수면 필드 삭제로 이미 계약 실패가 나고, 선택이면 계약상 없어도 되는 값이라 판정할 수 없는 게 맞다.
     §11 「게이트를 깨지 않은 항목」 에 없는 경로 이름과 함께 따로 보이므로 조용히 묻히지 않는다. api-reviewer 3 행이 경로가 없는 불변식을 처음부터 막는다.
     notes 에 「사용자 확인 권장」 으로 남기는 것도 맞다.
   - 누르는 자리 통과선을 24 로 둔다 — 44 는 확정 시안부터 56 개 가운데 39 개가 못 넘는 값이라 통과선으로 쓸 수 없고, 24 는 WCAG 2.2 AA(기본 준수 등급) 기준이다.
     44 를 권장값으로 보고에 남기는 것도 맞다.

VERDICT: CHANGES

## 2 회차

- 대상: `.harness/sprint-contract-kaizen-0924-p16-api-kit.md` (봉인 전, 추적 안 된 파일, 807 줄, 조건 29, sha256 앞 16 자리 `d9bcff6486022417`) — 스크래치 `p16d/contract.md` 와 바이트 단위로 같다
- 개정 파일은 아직 없다 — 봉인 전이라 맞다
- 검토자: REVIEW 에이전트 (사용자 승인 대신, 러닝북 「사용자 승인(5 단계) 대체」) · 검토일 2026-09-25

### 2 회차 결론

1 회차의 꼭 고칠 것 넷(C1 ~ C4)은 조건 줄 · `m.sh` 토큰 · 표 값까지 그대로 들어갔고, 내가 새로 만든 예행 저장소에서 다시 재도 값이 같았다.
고치면 좋은 것 1 ~ 6 도 들어갔다(1 은 일부). 그런데 C3 과 같은 결함이 한 파일에 더 남아 있다 — 아래 D1. 1 회차가 네 자리만 짚어서 놓친 곳이고,
이 Phase 가 이미 고치는 열일곱 파일 가운데 하나다. D1 하나를 고치면 봉인할 수 있다.

### 1 회차 CHANGES 반영 확인

| 항목 | 계약에서 본 자리 | 확인 |
| --- | --- | --- |
| C1 | SK-05 (b) 조건 줄 · `m.sh` SK-05 토큰 넷 · `dir_api` · SK-07 (d) 조건 줄과 토큰 둘 · `mock.py` §7 1 번 글 | 반영. 토큰 열둘, 시작 커밋 판 `dir_api=0`, 초안 첫 판 되살림 `dir_api=1` |
| C2 | ER-01 갈래 `$T/B/$EVID` · `evid_same` · 조건 줄 · AR-02 (d) 의 `L7` 행 검사 | 반영. 근거 파일 동시 편집 대조 `1` · `0` · `evid_same=0` |
| C3 | SK-09 네 자리 글 · 옛 글 일곱 · (d) README · (g) `--curl` hurl 줄 | 네 자리는 반영. 다섯째 문서 자리가 남았다 — D1 |
| C4 | `GAP 분석` 절 Step 1 표 · ER-03 (a) `## 사전 · 사후 측정` · 토큰 열 | 반영. 절 머리를 지운 사본에서 둘째 줄 열째 값 `0` |
| 좋은 것 1 | SK-06 `csp` 사본 줄 · notes 다음 사이클 메모 둘 | 반영. 뷰어 계약 문서 Gotcha 끝 문장과 연구 기록 표 행은 안 들어갔다(`mock.py` 에 `CSP` 0 건) — `## 범위 경계` 의 「1 ~ 6 을 반영했다」 는 「1 은 SK-06 줄과 notes 메모만」 으로 적는 편이 정확하다 |
| 좋은 것 2 | SK-02 · SK-08 · SK-09 의 `HURL_VERSION_CHANGED` 멈춤과 가짜 `hurl` 8.1.0 대조 | 반영 |
| 좋은 것 3 | 연구 기록 새 절 셈 기준(버튼 53 · 입력칸 2 · 선택 상자 1, 근거 파일 59) · 실측 날짜 줄 | 반영. 근거 파일 `:117` 의 「59 개 중 39 · 24 미만 0」 과 맞다 |
| 좋은 것 4 | 뷰어 스펙 §1 「위반 시」 칸과 SK-07 (a) 토큰 | 반영 |
| 좋은 것 5 | hurl-execution §6 표 `--curl <file>` 행 · SK-09 (e) | 반영 |
| 좋은 것 6 | notes 1×1 px 메모 | 반영 |
| 좋은 것 7 | 반영하지 않고 사유를 적음 | 동의 |

### 다시 돌려 본 것 (2 회차)

모두 스크래치 `p16review2/` 아래에서 돌렸다. 작업 폴더에는 이 절 하나만 썼다.

1. 계약의 코드 블록 다섯을 새로 뽑아 DRAFT(초안 담당 에이전트)의 `p16d/k/` 와 `cmp` — 다섯 다 같다. `mock.py` 앞 16 자리 `38685beaa5f32d56` · 확정 시안 `c4bd563ec8b71a95` — 계약 값과 같다
2. DRAFT 의 `rehearse.sh` 로 **지금 계약 파일**과 `mock.py` 에서 예행 저장소를 새로 만들어 `m` 스물넷을 돌렸다 — `out-base.txt` 가 DRAFT 의 것과 차이 0.
   시작 커밋 판 열여덟 ID — `out-start.txt` 차이 0
3. `ctl.sh` 전체 — DRAFT 의 `out-ctl.txt` 와 차이 0. `del.sh` SK-05 · SK-07 · SK-09 · ER-03 — 토큰 12 · 8 · 10 · 26 개 모두 값이 떨어짐, SAME 0 · MISSING 0
4. api-kaizen Step 1 명령(스킬 본문 그대로)을 시작 커밋 판 · 예행 판에서 — 계약 `GAP 분석` 절 표와 같다(api-verify 만 `gotchas` 10 → 12)
5. 뷰어 스펙 §1 의 CSP(페이지가 불러올 수 있는 자원을 제한하는 규칙) `<meta>` 문자열과 SK-06 `csp` 사본에 넣는 문자열이 글자 그대로 같다
6. 측정 뒤 스크래치 `tmp/` 는 비었고, 떠 있는 `srv.py` 는 1 회차가 적은 다른 세션 것(프로세스 번호 75318) 하나뿐이다
7. D1 을 고친 판 — 아래 표. 도중에 디스크가 차서 1 ~ 3 의 예행 저장소 사본은 지웠다. 출력은 `p16review2/out-*.txt` 에 남아 있다

### 새로 찾은 것 — 봉인 전에 고칠 것

#### D1 — SK-09: `auth-secret-lifecycle.md` 세 자리가 아직 「둘뿐」 이다

예행 판(이 계약대로 고친 끝 판)의 `docs/api/execution/auth-secret-lifecycle.md` 에 이 셋이 그대로 남는다.

- `:60` 「가려지는 곳은 stderr 로그(`--verbose` / `--very-verbose`)와 JSON 리포트의 `report.json`(`curl_cmd`·요청 헤더)뿐이다.」
- `:99` 수치 표 「| `--secret` 마스킹되는 채널 | stderr 로그, JSON 리포트 `report.json` | 실측 2026-09-05 (hurl 8.0.1) |」
- `:125` Gotcha 머리 「**`--secret`이 가리는 채널은 stderr 로그와 `report.json` 둘뿐이다**」

이 파일은 열일곱 안이고, 이 Phase 가 같은 `## Gotchas` 절에 새 Gotcha 를 넣고 머리 설정을 0.2.1 로 올린다. 그런데 새 api-verify Gotcha 는
「가린다고 확인된 곳은 … `--curl` 파일」 이라 쓰고 출처로 `auth-secret-lifecycle.md` §5·§6 을 댄다 — 댄 출처가 같은 커밋 안에서 다르게 말한다.
api-probe `SKILL.md` References 도 이 문서의 「`--secret` 의 stdout 한계」 를 가리킨다. C3 이 막으려던 「같은 커밋 안에서 킷 문서끼리 어긋남」 이 이 파일에 남는다.

측정이 못 잡는 까닭: SK-09 (f) 옛 글 일곱은 글자가 정해져 있다. 「`report.json`(…)뿐이다」 · 「`report.json` 둘뿐」 은 사이에 낀 글자 때문에
「`report.json` 뿐」 에 안 걸린다(시작 커밋 판에서 여섯째 · 일곱째 값이 `0 0` 인 까닭). 조건 (f) 의 뜻(가리는 곳을 다 적은 것처럼 말하는 글 0)을 어기는데 측정은 통과한다.

고칠 글 — `mock.py` 에 `rep(AS, …)` 셋(끝 판 글 기준):

```text
(1) :60
가려지는 곳은 stderr 로그(`--verbose` / `--very-verbose`)와 JSON 리포트의 `report.json`(`curl_cmd`·요청 헤더)뿐이다.
→ 가린다고 확인된 곳은 stderr 로그(`--verbose` / `--very-verbose`), JSON 리포트의 `report.json`(`curl_cmd`·요청 헤더), `--curl <file>`의 헤더 값이다(`--curl`은 실측 2026-09-24).

(2) :99
| `--secret` 마스킹되는 채널 | stderr 로그, JSON 리포트 `report.json` | 실측 2026-09-05 (hurl 8.0.1) |
→ | `--secret` 마스킹되는 채널 | stderr 로그, JSON 리포트 `report.json`, `--curl <file>` | 실측 2026-09-05 · 2026-09-24 (hurl 8.0.1) |

(3) :125 머리
- **`--secret`이 가리는 채널은 stderr 로그와 `report.json` 둘뿐이다** —
→ - **`--secret`이 가린다고 확인된 채널은 stderr 로그 · `report.json` · `--curl <file>`이다** —
```

§6 제목 「마스킹되는 채널은 절반뿐이다」 는 둔다 — 가리는 곳 셋 · 안 가리는 곳 다섯이라 틀리지 않고, 측정이 기대는 제목도 아니다.

`m.sh` `SK-09)` 갈래 — 두 문장을 이것으로 바꾼다. 출력 줄 수는 일곱 그대로라 `ctl.sh` 의 `5p` · `6p` · `7p` 자리가 안 바뀐다.

```bash
    toks "$(cat "$E/$HE" "$E/$AS")" '| `--curl <file>` 의 헤더 값 (실측 2026-09-24) | `--output <file>` |' \
      '가린다고 확인된 곳은 stderr 로그(`--verbose` / `--very-verbose`), JSON 리포트의 `report.json`(`curl_cmd`·요청 헤더), `--curl <file>`의 헤더 값이다(`--curl`은 실측 2026-09-24).' \
      '| `--secret` 마스킹되는 채널 | stderr 로그, JSON 리포트 `report.json`, `--curl <file>` | 실측 2026-09-05 · 2026-09-24 (hurl 8.0.1) |' \
      '- **`--secret`이 가린다고 확인된 채널은 stderr 로그 · `report.json` · `--curl <file>`이다**'
    # 뒤 두 글은 가리는 곳을 다 적은 것처럼 말하는 초안 첫 판 글이다
    # 목록에 없는 말투는 curl_missing 이 잡는다 — report.json 과 가림 낱말이 같이 든 줄에 --curl 이 없으면 센다
    echo "old=$(oldn "$E" 'stderr 로그와 리포트만' 'stderr 로그와 리포트뿐' 'stderr 와 리포트만' 'body 를 stderr 에 그대로 뿌린다' '뱉으므로 CI 로그에 그대로 남는다' '`report.json` 뿐' '`report.json` 만 가리' \
      '`report.json`(`curl_cmd`·요청 헤더)뿐이다' '`report.json` 둘뿐' '| `--secret` 마스킹되는 채널 | stderr 로그, JSON 리포트 `report.json` |')curl_missing=$(find "$E/api-kit" "$E/docs/api" -type f ! -name research-log.md -exec grep -hF -- 'report.json' {} + | grep -E -- '--secret|가려지는|가리는|가린다|마스킹되는' | grep -cvF -- '--curl')"
```

잰 값 — 위 편집을 `mock.py` 끝에 더해 예행 저장소를 새로 만들었다(스크래치 `p16review2/fix/`):

| 판 | 다섯째 줄 | 여섯째 줄 |
| --- | --- | --- |
| 고친 예행 판 | `1 1 1 1` | `old=0 0 0 0 0 0 0 0 0 0 curl_missing=0` |
| 지금 초안대로 만든 예행 판 | `1 0 0 0` | `old=0 0 0 0 0 0 0 1 1 1 curl_missing=3` |
| 시작 커밋 판 | `0 0 0 0` | `old=2 1 1 1 1 0 0 1 1 1 curl_missing=3` |

대조(고친 예행 판 끝 판 사본 한 군데를 바꾸고 되돌림):

- `:125` 머리를 옛 글로 되돌린 사본 — 다섯째 `1 1 1 0` · 여섯째 `old=0 0 0 0 0 0 0 0 1 0 curl_missing=1`
- `:60` 을 목록에 없는 말투(「…와 JSON 리포트의 `report.json`(`curl_cmd`·요청 헤더)에 한정된다.」)로 바꾼 사본 — 옛 글 열은 모두 `0` 인데 `curl_missing=1`. 목록 밖 말투는 이 값이 잡는다
- `del.sh` SK-09 — 토큰 열셋 모두 값이 떨어짐, SAME 0 · MISSING 0
- 곁 조건: DG-02 `auth-secret-lifecycle.md rules_up=0` · ER-02 `added=160 k02=0 names=0 kit_names=0` · ER-01 `0` · `0` · `evid_same=1` · SK-08 · SK-11 · AR-03 값 그대로 ·
  DG-05 `hits=0` · `/bin/bash` 3.2.57 에서도 다섯째 · 여섯째 줄이 같다
- 기존 대조 둘은 값이 바뀐다 — BUILD(봉인 · 구현 담당 에이전트)가 계약 글을 이 값으로 고친다(고친 예행 판에서 잰 값).
  「hurl-execution 새 행을 옛 빈 칸 행으로」 → 다섯째 줄 `0 1 1 1`. 「초안 첫 판 글 넷 되살림」 → 여섯째 줄 `old=0 0 0 0 0 3 1 0 0 0 curl_missing=4`

계약 글을 고칠 자리:

- SK-09 조건 줄 (e) 끝에 「그리고 `docs/api/execution/auth-secret-lifecycle.md` 의 §6 문장 · 수치 표 「`--secret` 마스킹되는 채널」 행 · Gotcha 머리 세 자리에 `--curl <file>`」
- (f) 를 옛 글 열(위 셋 더함)이 각각 0 줄, 그리고 `report.json` 과 가림 낱말(`--secret` · 가려지는 · 가리는 · 가린다 · 마스킹되는)이 같이 든 줄 가운데 `--curl` 이 없는 줄이 0 으로(연구 기록 제외는 그대로)
- 측정 문구: 다섯째 `1 1 1 1`, 여섯째 `old=0 0 0 0 0 0 0 0 0 0 curl_missing=0`. 알려진 답: 시작 커밋 판 `0 0 0 0` · `old=2 1 1 1 1 0 0 1 1 1 curl_missing=3`. 문장 삭제 대조 토큰 열셋. 위 대조 둘을 더한다
- `봉인 전 실측` 표 SK-09 행, `편집 전 감사` 표의 auth-secret-lifecycle 행(`:60` · `:99` · `:125` → SK-09), 개선안 초안 4 의 「`--secret` 넷」, 「검토가 찾은 구멍」 줄에 D1
- notes 모의본의 「`--secret` 이 가리는 곳 네 곳(`--curl` 파일 포함)」 에 문서 세 자리를 더한다(조건은 재지 않는다)
- `## 범위 경계` 의 검토 결과 문장에 2 회차 판정과 D1 반영을 더한다

### 고치면 좋은 것 (2 회차) — 판정에 넣지 않는다

1. **§7 여는 방법의 명령은 서버를 띄운 채 끝난다.** 「확인이 끝나면 서버를 내리고 그 폴더를 지운다」 한 마디가 있으면 사본 폴더와 서버가 남지 않는다. SK-05 토큰이 걸린 문장이라 넣으면 토큰도 같이
2. **연구 기록 새 절에 D1 도 남긴다.** 「문서와 실측이 어긋난 것」 표 아래 `--curl` 문장 끝에 「hurl-execution §6 표와 auth-secret-lifecycle 세 자리에 더했다」 를 붙이면 된다
3. **ER-01 `evid_same` 은 누가 근거 파일을 고쳐도 떨어진다.** 시작 커밋 뒤로 그 파일을 고친 커밋은 0 이고 다른 Phase 가 고칠 까닭도 없다. QA 때 떨어지면
   `git log 3a348d6..<end_sha> -- .harness/.meta/evidence/phase16.md` 로 누가 고쳤는지부터 본다
4. **디스크.** 이 검토 도중 `/System/Volumes/Data` 남은 자리가 130 ~ 200 MB 로 떨어져 측정 한 번이 두 판 풀기에서 `No space left on device` 를 냈다.
   측정은 `SNAPSHOT_FAIL` 자리에서 종료 코드 2 로 멈췄다 — 조용한 0 은 아니었다. 몇 분 뒤 3.9 GB 로 돌아왔다(다른 프로세스 몫이다).
   측정은 저장소를 두 벌 풀고 예행 저장소 하나가 40 MB 쯤이라 BUILD · QA 전에 남은 자리를 먼저 본다

### 확인만 하고 넘어간 것 (2 회차)

1. 조건 줄 29 와 frontmatter `conditions: 29` 가 같다. D1 은 조건을 늘리지 않는다
2. 조건끼리 충돌: D1 의 새 글은 SK-08 (b) 가 재는 `HURL_VARIABLE_` Gotcha 와 다른 줄이고, 새 URL 이 없어 ER-01 과 무관하며, `44px` · 「클릭 타깃」 · 번역투가 없다. AR-03 은 열일곱 밖만 본다
3. 회귀 정책 문서 Gotcha 「4행」 을 api-verify 가 출처로 댄다 — 새 Gotcha 가 절 끝(다섯째)에 붙어 번호가 안 밀린다
4. 1 회차 「사용자 결정 대신 판단」 둘(판정 불가를 통과선 검사에 안 넣음 · 누르는 자리 통과선 24)에 계속 동의한다

VERDICT: CHANGES
