# Evals Audit — 2026-09-24 (kaizen-2026-09-24)

오케스트레이터 Step F4 4 번 점검 기록. 가지 `kaizen/2026-09-24` 끝 판에서 2026-09-25 에 돌렸다.

## sync-evals 결과

`python3 scripts/sync-evals.py --check-only` (종료 코드 0) 요약 줄:

```text
Total: 0 added, 0 orphans, 0 missing (preview)
```

`python3 scripts/run-evals.py` 는 `Total: 115 passed, 0 failed` 다.

## 점검한 evals.json (10)

각 파일의 스킬 목록이 그 킷 `skills/` 폴더와 맞는지 `sync-evals.py` 가 본다. onboarding-kit 은 평가 파일이 스킬 폴더 안에 있고 게이트 평가 형식이라 `run-gate-evals.sh` 러너가 돈다.

- `backend-kit/evals/evals.json`
- `design-kit/evals/evals.json`
- `flutter-toolkit/evals/evals.json`
- `harness/evals/evals.json`
- `howto-kit/evals/evals.json`
- `infra-kit/evals/evals.json`
- `onboarding-kit/skills/setup-guide/evals/evals.json`
- `react-kit/evals/evals.json`
- `rust-kit/evals/evals.json`
- `tone-kit/evals/evals.json`

## 이번 사이클 스킬 · 에이전트 더함 · 지움 · 이름 바꿈

사이클 기준 커밋(가지가 `main` 에서 갈라진 `83cfb4f`)부터 끝 판까지 스킬 · 에이전트 파일의 변경 종류를 셌다:

```bash
git diff --name-status -M 83cfb4f311d6497186da13c75bdb8f8a108481b3 HEAD -- '*/skills/*/SKILL.md' '*/agents/*.md' | grep -vc '^M'
```

결과 `0` — 바뀐 86 파일 모두 `M`(본문 수정)이다. 더하거나 지우거나 이름을 바꾼 스킬 · 에이전트가 없어 evals.json 의 스킬 목록은 고칠 것이 없다.
이번 사이클에 평가 사례가 바뀐 evals.json 아홉(backend · design · flutter · howto · infra · onboarding · react · rust · tone)은 각 Phase 계약과 QA 가 이미 쟀다.

## evals.json 이 없는 킷

`api-kit` · `bambu-kit` · `planning-kit` · `reflect-kit` 은 `evals/evals.json` 이 없다. bambu-kit 은 게이트 시험 파일(`evals/gate-fixtures/`), reflect-kit 은 훅 시험(`evals/hooks/`)을
두고 CI 가 돌린다. evals.json 신설은 이 사이클 범위 밖이라 다음 사이클 검토 대상으로 남긴다.

## 판정

evals 정합성 OK. 조치 불필요.
