# 절차 문서 작성 표준 — 스텝 하나를 어떻게 쓰라고 하는가

`last_updated: 2026-09-10`

이 킷의 Step Contract 는 DITA 1.3 을 뼈대로 삼는다. 이 문서는 그 인용이 실제로 표준에 있는지,
그리고 **킷이 표준을 어디서 넘어섰는지**를 기록한다.

넘어선 곳을 감추면 나중에 "표준이 그렇다더라" 로 잘못 인용된다. 강화한 지점은 강화했다고 적는다.

---

## 1. 확정된 인용 7 건

조회일 **2026-09-10**. 출처 열이 빈 행은 없다.

| 규정 | 원문 | 출처 |
| --- | --- | --- |
| 스텝 명령문은 한 문장 | *"should not be more than one sentence"* | DITA 1.3 `<cmd>` — docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/langRef/technicalContent/cmd.html |
| 결과를 매 스텝에 쓰지 마라 | *"should not be used for every step"* | DITA 1.3 `<stepresult>` — docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/langRef/technicalContent/stepresult.html |
| task 모델은 **둘**이다 | *"the DTD and Schema packages distributed by OASIS contain two task models"* | DITA 1.3 `<taskbody>` — docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/langRef/technicalContent/taskbody.html |
| strict 모델이 OASIS 기본 | *"this constraint is used in the default task distributed by OASIS"* | 같은 문서 |
| 스텝 하나에 동작 하나 | *"In general, use one step for each action."* | Google — developers.google.com/style/procedures |
| 동작 먼저, 결과 나중 | *"State the action first and the result second."* | Google — 같은 문서 |
| 번호 매긴 목록 | *"Use a numbered list."* | Microsoft — learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions |
| 명령형 동사 | *"Use imperative verb forms."* | Microsoft — learn.microsoft.com/en-us/style-guide/checklists/procedures-and-instructions-checklist |

---

## 2. 킷의 `<taskbody>` 인용이 불완전했다

킷은 `step-contract.md` 에서 `<taskbody>` 콘텐츠 모델을 이렇게 인용했다.

```text
<prereq>?, <context>?, (<steps>|<steps-unordered>)?, <result>?, <postreq>?
```

**어느 모델인지 밝히지 않았다.** DITA 1.2 부터 OASIS 배포본에는 모델이 둘이다.

> *"Beginning with DITA 1.2, the DTD and Schema packages distributed by OASIS contain **two task
> models**. The **general task model** allows two additional elements inside the task body (…);
> it also allows multiple instances and varying order for the …, …, and … elements. The **strict
> task model** maintains the order and cardinality of the DITA 1.0 and 1.1 content model."*
> — docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/langRef/technicalContent/taskbody.html
> (조회 2026-09-10)

| 모델 | 순서 | 요소 |
| --- | --- | --- |
| **strict task** | DITA 1.0/1.1 의 순서와 개수를 유지 — **고정** | 제한적 |
| **general task** | 순서 자유, 다중 인스턴스 허용 | 두 요소 추가 |

킷이 인용한 고정 순서 모델은 **strict task model** 이다. 그리고 그것이 OASIS 기본이다 —
*"this constraint is used in the default task distributed by OASIS."*

**그러므로 킷의 인용은 틀리지 않았지만 불완전했다.** 어느 모델인지 안 쓰면, general 모델을 쓰는
사람이 "킷이 DITA 를 잘못 인용했다" 고 판단하게 된다. `step-contract.md` 에 모델 이름을 박았다.

---

## 3. 킷이 표준을 넘어선 지점 — `verify` 필수

DITA 는 결과를 매 스텝에 쓰지 말라고 한다.

> *"should not be used for every step"* — DITA 1.3 `<stepresult>` (조회 2026-09-10)

**이 킷은 그 권고를 의도적으로 강화한다.** `verify` 는 모든 스텝에 필수다.

표준을 모르고 어기는 것이 아니다. 이 도메인의 실패 데이터가 다르기 때문이다 — 막으려는 실패가
**무증상 실패**다. 절차를 다 따랐는데 아무 일도 일어나지 않고 에러도 안 난다. 확인 지점이 없으면
사용자는 마지막 스텝까지 가서야 아무것도 안 됐다는 것을 알고, **어느 스텝이 실패했는지 되짚을 수
없다.**

Google 의 규정도 결과를 쓰라고는 하되 **순서만** 정한다.

> *"State the action first and the result second."* — developers.google.com/style/procedures
> (조회 2026-09-10)

**"매 스텝에 확인을 넣어라" 라고 규정한 스타일 가이드 조항은 찾지 못했다** — `[미확인]`.
그러므로 이 킷의 `verify` 필수 규칙은 **표준의 인용이 아니라 도메인 실패 데이터에 근거한 강화**다.
그렇게 표기한다. 다른 표기는 과대 인용이다.

---

## 4. ISO/IEC/IEEE 26514 · 26515 — `[미확인]`

설계 브리프 §11-2 가 남긴 항목이다. 이번에도 **해소하지 못했다.**

| 표준 | 공개 범위에서 확인한 것 | 확인 못 한 것 |
| --- | --- | --- |
| ISO/IEC/IEEE 26514 | 제목 · 판 | **절차 작성 세부 조항** |
| ISO/IEC/IEEE 26515 | 제목 · 판 | 같음 |

두 표준 모두 **유료**다. 그리고 이 환경에서는 `iso.org` 자체가 **5.5KB 스텁**만 응답해 공개
Scope 조차 직접 대조하지 못했다 — 접근 차단이지 부재가 아니다.

**킷의 처리**: ISO 를 근거로 인용하지 않는다. 유료 전문의 내용을 2 차 요약으로 추정해 쓰지
않는다. 시도한 URL 은 `howto-kit/references/provenance-notes.md` §9 에 있다.

---

## 5. 킷 규약과 표준의 대조

| 킷 규약 | 표준 근거 | 관계 |
| --- | --- | --- |
| 스텝 명령문 1 문장 | DITA `<cmd>` | **인용** |
| 스텝 하나에 동작 하나 | Google | **인용** |
| 번호 매긴 스텝 | Microsoft | **인용** |
| 명령형 | Microsoft | **인용** |
| 골격 `prereq/context/steps/result/postreq` | DITA strict task model | **인용** (모델명 명시 필요 — §2) |
| **`verify` 매 스텝 필수** | DITA 는 반대 권고 | **강화** — 도메인 실패 데이터 근거 |
| **`안 보이면` 선제 분기 필수** | 규정 조항 확인 실패 | **관행의 귀납** (`branch-catalog.md` §5) |
| **출처 등급 표기** | 대응 표준 없음 | **킷 고유** |

**"인용" 과 "강화" 와 "킷 고유" 를 섞어 쓰지 마라.** 강화한 것을 표준이라 부르면 그것이 이 킷이
막으려는 F3 다.

---

## 6. 검증 함정 4 종이 이번에도 값을 했다

이번 사이클은 앞선 사이클들이 축적한 함정 목록을 전부 적용한 정규화 대조기를 썼다.

| 함정 | 발견 사이클 |
| --- | --- |
| HTML 엔티티 | `branch-catalog` |
| 공백 정규화 (줄바꿈 + 들여쓰기) | `deprecation-policy` |
| SPA | `deep-links` |
| PDF 폰트 서브셋 | `ui-anchoring` |

그 덕에 이번에 하나를 건졌다.

```text
Google "State the action first and the result second"
  raw=miss   norm=HIT
```

원문이 두 줄에 걸쳐 있어 raw 대조로는 안 잡혔다. **함정 목록이 없었으면 이 인용은 "확인 실패" 로
잘못 기록됐을 것이다.** 목록이 사이클을 거치며 실제로 값을 하고 있다.

전체 결과: 9 건 중 **7 raw HIT · 1 norm 으로 구제 · 1 확인 실패**(ISO — 접근 차단).

---

## 7. 표준 인용 체크리스트

절차 규약에 표준을 근거로 달 때 순서대로 확인한다.

1. 인용한 문장이 **그 URL 에 실재**하는가. 정규화 대조기로 확인했는가 (엔티티 · 공백 · SPA · PDF)
2. 표준에 **변종**이 있는가. DITA task 처럼 모델이 둘이면 **어느 것인지 명시**했는가
3. 규약이 표준보다 **강한가**. 강하다면 "강화" 라고 적고 **왜 강화했는지** 근거를 댔는가
4. 표준에 대응 조항이 **아예 없는** 규약인가. 그렇다면 "킷 고유" 로 표기했는가
5. **유료 표준의 내용을 2 차 요약으로 추정해** 쓰고 있지 않은가. 공개 범위에서 본 것만 인용하라
6. 접근 실패를 **부재로 승격**하고 있지 않은가. `iso.org` 가 스텁을 주는 것은 차단이지 없는 것이 아니다

---

## 8. 조회 기록

Codex 위임 1 회 (MODE=research · read-only · foreground · 검색 하드캡 20). rollout 로그의
`turn_aborted` 는 0 건으로 정상 완주했다.

**Codex 가 킷의 오류를 지적했다** — `<taskbody>` 모델이 킷 인용과 다르다는 것이다. 직접 확인한
결과 지적은 절반만 맞았다: 킷 인용이 틀린 게 아니라 **두 모델 중 어느 것인지 안 밝힌 것**이
문제였다. 위임 결과를 그대로 받았으면 멀쩡한 인용을 틀린 것으로 고칠 뻔했다.

미확정 근거의 원장은 `howto-kit/references/provenance-notes.md` 가 정본이다. 확정된 항목은
이 문서가 정본이다.
