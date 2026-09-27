# 부모 교차 진단 결과 (2026-09-27)

이 세션 피드백 103 개 가운데 `cross_diagnosis_by: pending-parent` 47 개를 에이전트 셋이 나눠 채웠다(verify-feedback 47/47 PASS). 뒤집은 판정은 없다.

## 합친 뒤 생긴 어긋남 — cx3 묶음이 고친다

1. `design-kit/skills/design-mockup/SKILL.md:171` · `docs/design-kit/design-mockup.html:665` 에 「다음 시안 전에는 Step 2 가 폐기 칸의 경로를 따라 원문을 읽는다」 가 남았다. k2 가 단계를 다시 매겨(0cfcb03) 폐기 칸을 읽는 자리는 Step 0(같은 파일 57 줄)이다.
2. `harness/evals/gate-exit-codes.md:72` 에 이 표를 인용하지 않는 `scripts/check-api-kit-docs.py` 행이 있다(dr1a 92377e0). hs 도우미 `hs5.sh` 가 통합 폴더에서 `cite=11 rows=12 extra=1`.
3. `~/.claude/hooks/parallel-session-guard.sh` 가 `echo "$(echo "it's")"; git commit -m x` 를 놓친다(고치기 전 `us-backup` 사본은 잡는다). 큰따옴표 안 `$( )` 가 따옴표를 새로 여는 것을 따옴표 처리가 모른다.
4. 2 회차 계약에 쓴 `status: superseded` 가 계약 형식 문서의 허용 값(`active | done`) 밖이고, 새 판 계약을 가리키는 칸이 없다.

## 알아둘 것 (고치지 않음)

- user-hooks 훅이 고치기 전에도 못 잡던 모양: `git -c k=v commit` · 서브셸 · `{ …; }` · `then` · `time` · `command` · `bash -c`.
- onboarding G5 가 고치기 전에도 못 잡던 빈 칸 모양 넷(표 줄 앞 공백 · U+00A0 · U+3000).
- dr2 가 `prefers-reduced-motion` 낱말을 `&#45;` 로 적어 측정을 피해 간 것으로 보이는 자리 6 곳(판정은 맞음 — 스타일 블록에 규칙을 다시 적은 곳 0).
