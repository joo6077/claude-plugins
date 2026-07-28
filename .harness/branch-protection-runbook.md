# main branch protection 런북

2026-07-28 적용. 근거 계약: `.harness/sprint-contract-ci-gate-hardening.md`.

## 왜 켰나

이 레포는 main 계보 317 커밋 중 303 개(95.6%)가 직접 푸시였고, Playwright 잡이
**37 런 중 32 회 failure · success 0 회**인 채로 릴리스가 계속 나갔다. 기록 시작
(2026-04-12)부터 한 번도 green 이 아니었다. 강제 장치가 없던 것이 구조적 원인이다.

## 현재 설정

```json
{
  "required_status_checks": {
    "strict": true,
    "checks": [
      { "context": "Plugin Validation",         "app_id": 15368 },
      { "context": "Playwright Visual Tests",   "app_id": 15368 },
      { "context": "Harness Integration Tests", "app_id": 15368 }
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": false,
  "lock_branch": false,
  "allow_fork_syncing": false
}
```

적용:

```bash
gh api -X PUT repos/joo6077/claude-plugins/branches/main/protection \
  -H "Accept: application/vnd.github+json" --input protection.json
```

## 설계 판단 3 가지 — 바꾸기 전에 읽어라

**required contexts 는 반드시 이 3 개만.** main 의 check-run 은 6 개인데 PR head 는 3 개다.
차이 3 개(`build`, `deploy`, `report-build-status`)는 GitHub 관리형
`pages-build-deployment` 소속이라 **PR 에 절대 안 뜬다.** 하나라도 넣으면 영구 pending 이
되어 머지가 완전히 막힌다. 게다가 이 레포는 legacy commit status 가 0 건이라 오타를 내면
`/commits/<sha>/status` 가 `total_count: 0` 을 조용히 반환해 원인을 알기 어렵다.

정확한 문자열은 PR head 에서 뽑아라 (main 에서 뽑으면 pages 3 종이 섞인다):

```bash
gh api repos/joo6077/claude-plugins/pulls/<N> --jq .head.sha | \
  xargs -I{} gh api repos/joo6077/claude-plugins/commits/{}/check-runs \
  --jq '.check_runs[] | "\(.app.id)\t\(.name)"'
```

**`required_pull_request_reviews` 는 null 이어야 한다.** 머지된 PR 이 전부 셀프 머지
(author == mergedBy)라, 켜는 순간 자기 PR 을 머지할 수 없게 된다.

**`required_linear_history` 는 false.** 기존 PR 이 전부 merge commit 으로 들어왔다.
켜면 앞으로 squash/rebase 만 가능해진다.

## enforce_admins: true 의 파급

소유자의 직접 push 도 거부된다. 실측:

```text
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote: - 3 of 3 required status checks are expected.
 ! [remote rejected] main -> main (protected branch hook declined)
```

**그래서 `scripts/release.sh` 가 PR 경유로 바뀌었다** — 이전에는 L110 에서
`git push origin HEAD --follow-tags` 로 main 에 직접 push 했고, protection 을 켜면
`/release` 가 즉시 깨진다. 지금은 `release/<plugin>-v<version>` 브랜치 + PR 을 만든다.
태그는 protection 대상이 아니므로(`gh api .../tags/protection` → Not Found) 그대로 push 된다.

**순서를 지켜라**: release.sh 변경이 머지된 **후에** protection 을 켜야 한다.
역순이면 자기 수정을 push 할 수 없는 자물쇠 사고가 난다.

## 되돌리기

```bash
# 전체 해제
gh api -X DELETE repos/joo6077/claude-plugins/branches/main/protection

# 체크만 해제 (admin 강제는 유지)
gh api -X DELETE repos/joo6077/claude-plugins/branches/main/protection/required_status_checks

# admin 강제만 끄기 (탈출구 확보 — 체크는 유지)
gh api -X DELETE repos/joo6077/claude-plugins/branches/main/protection/enforce_admins

# admin 강제 다시 켜기
gh api -X POST   repos/joo6077/claude-plugins/branches/main/protection/enforce_admins
```

## 정상 동작 확인

```bash
gh api repos/joo6077/claude-plugins/branches/main/protection --jq '{
  contexts: [.required_status_checks.checks[].context],
  strict: .required_status_checks.strict,
  admins: .enforce_admins.enabled,
  reviews: .required_pull_request_reviews
}'
```

`contexts` 가 정확히 3 개여야 한다.

PR 이 `BLOCKED` 로 **영구 고착되지 않는지**도 확인하라 — 체크가 pending 인 동안은
`BLOCKED` 가 정상이고, 통과하면 `CLEAN` 으로 바뀌어야 한다:

```bash
gh pr view <N> --json mergeStateStatus,mergeable
```

실측(PR #18): `BLOCKED` → `BLOCKED` → `BLOCKED` → `CLEAN MERGEABLE`.
`CLEAN` 으로 안 바뀌고 계속 `BLOCKED` 면 context 오타를 의심하고 위 되돌리기를 실행하라.

## 알려진 한계

- `strict: true` 는 base 최신화를 요구한다. 동시 PR 이 많아지면 머지 1 건마다 나머지 PR 이
  CI 재실행된다. 현재는 CI 전체 wall-clock 이 약 60~70 초라 비용이 작다.
- 태그는 보호되지 않는다. 태그 보호가 필요하면 별도 ruleset 을 만들어야 한다.
- 이 설정은 GitHub 콘솔에만 존재하고 레포에 config-as-code 로 커밋되어 있지 않다.
  이 문서가 SSOT 역할을 하지만 실제 상태와 drift 할 수 있으므로, 의심되면 위 조회 명령으로 확인하라.
