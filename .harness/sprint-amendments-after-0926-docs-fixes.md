---
slug: after-0926-docs-fixes
created: "2026-09-26 21:02"
---

# after-0926-docs-fixes 개정

## A-01 — AR-02 와 ER-01 · ER-02 가 한 쪽에서 부딪힌다 (동의함 · 옵션 1)

봉인 뒤 구현하다 찾았다. 계약 본문은 고치지 않았다.

- 부딪히는 곳: `docs/tone-kit/dart-flutter-idioms.html`. AR-02 는 이 쪽에서 바뀐 줄이 DC-7 괄호 한 줄뿐이어야 한다(`changed=1/1`).
  그런데 이 쪽은 320 폭에서 `.detail li` 목록 줄이 상자 밖으로 나간다 — `display:flex` 인 `li` 안에 글 · `<code>` 가 섞여 있어
  글 토막마다 따로 가로로 늘어서기 때문이다. 글자 간격 그대로 `esc=1`, 넓힌 간격 `doc=5 esc=1`(도우미 `pw.js w`, 이 가지 끝 `7d02ffe` 기준 실측).
- 이 쪽을 고치지 않으면 ER-01 · ER-02 가 떨어지고, 고치면 AR-02 가 떨어진다. 공통 파일(`docs/assets/site.css`)로 풀어 보았다 —
  `li>*{min-width:0}` 를 더하면 문서 넘침은 0 이 되지만 글 토막 하나가 상자 밖으로 나가는 것(`esc=1`)은 남았다. 다른 쪽 목록까지
  건드리는 규칙이라 되돌렸다.
- 쪽 고침은 두 줄이다(준비해 둔 판 — 적용하지 않았다):

```diff
-  .detail li{display:flex;align-items:flex-start;gap:8px;font-size:13px;color:var(--text2);line-height:1.7;overflow-wrap:anywhere}
-  .detail li::before{content:'\2013';color:var(--accent);flex-shrink:0;font-weight:800}
+  .detail li{display:block;position:relative;padding-left:1.2em;font-size:13px;color:var(--text2);line-height:1.7;overflow-wrap:anywhere}
+  .detail li::before{content:'\2013';color:var(--accent);position:absolute;left:0;font-weight:800}
```

  이 판을 넣으면 그 쪽이 320 폭(글자 간격 그대로 · 넓힘 모두)에서 `OK` 였다(구현 중 실측).

고를 수 있는 것 둘 — 둘 다 조건을 느슨하게 하는 쪽이라 위임으로 동의 처리하지 않았다.

| 옵션 | 개정 내용 | 방향 계산 |
| --- | --- | --- |
| 1 (권함) | AR-02 에서 `dart-flutter-idioms.html` 의 바뀐 줄로 DC-7 줄에 더해 위 `.detail li` 두 줄을 허용한다. 측정은 `changed=3/3` · `old_left=0` 이고, DC-7 줄은 지금처럼 괄호만 지운 것과 글자까지 같아야 한다 | `amend_direction` 허용 줄 집합 1 → 3: `relaxing added=2 removed=0` |
| 2 | ER-01 · ER-02 의 재는 쪽에서 `dart-flutter-idioms.html` 을 뺀다(177 → 176) | `amend_direction_oracle` 측정 집합: `relaxing measured_removed=1 measured_added=0` |

옵션 1 을 권하는 까닭: 쪽이 실제로 고쳐지고, 늘어나는 두 줄은 목록 모양 규칙뿐이다. 옵션 2 는 320 폭에서 글이 상자 밖으로 나가는 쪽을 남긴다.

- amend_direction: relaxing (옵션 1 · 옵션 2 모두 — 위 표의 계산 출력)
- consent: 사용자 동의 — 이 개정만 콕 집어 물은 질문에 옵션 1 을 골랐다(일반 위임이 아니다)
- 동의한 사용자 말 · 시각 · 세션: 질문 「문서 사이트 dart-flutter-idioms 페이지가 320px 에서 목록 글이 상자 밖으로 나갑니다. 이 페이지는 '괄호 한 줄만 고친다'는 조건에 묶여 있어, 고치려면 조건을 넓혀야 합니다. 어떻게 할까요?」 · 답 「CSS 두 줄 더 허용 (추천)」 · 2026-09-26T16:20:41.030Z · 세션 bda55d45-296c-491f-89ba-b52042d58e72 (`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/bda55d45-296c-491f-89ba-b52042d58e72.jsonl` 3632 번째 줄, uuid 345eee23-7b93-46ed-bc3f-37a1a251e5e4)
- 고른 옵션: 1 — AR-02 의 허용 줄을 DC-7 괄호 줄에 `.detail li` 두 줄을 더한 셋으로 넓힌다. 판정은 `changed=3/3` · `old_left=0` 이고 DC-7 줄은 괄호만 지운 것과 글자까지 같아야 한다. 옵션 2(측정에서 빼기)는 쓰지 않는다 — ER-01 · ER-02 는 177 쪽 그대로 잰다
