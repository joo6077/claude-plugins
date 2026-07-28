# WIP — ci-gate-hardening 스프린트 진행 상태

계약: `.harness/sprint-contract-ci-gate-hardening.md` (25 조건, `status: active`)
브랜치: `fix/ci-gate-hardening` (base `cd973aa` = PR #16 머지 커밋)

## 사용자가 승인한 3 가지 결정 (2026-07-28)

1. **`enforce_admins: true`** + `release.sh` PR 경유 전환 (같은 스프린트 필수)
2. **docs 수정 범위 = 전체 146 페이지** (오버플로 66 건 전부)
3. **Playwright Visual Tests 를 required check 에 지금 포함**

## 실행 순서 (역순 금지 — 자물쇠 사고)

```text
A 재발방지 → B 66건 해소 → C 액션 v7 → D release PR 전환 → PR 머지 → E protection
```

**E 를 D 머지보다 먼저 하면 `release.sh:110` 이 거부되어 자기 수정을 push 못 한다.**

## 진행 상황

### Phase A — 재발 방지 (진행 중)

- [x] `.claude/skills/docs-site/references/page-template.html` — 4 규칙 인코딩 완료.
      실측 검증: 스트레스 콘텐츠(긴 코드 + 6 컬럼 표 + grid 내 compare)에서
      375px/768px 오버플로 **0**, 표·코드 끝까지 스크롤 도달, 버튼 44px,
      테마 토글 + `dk-theme` + `prefers-color-scheme` 폴백, 콘솔 에러 0.
- [ ] `.claude/skills/docs-site/SKILL.md` — Gotchas 4 규칙 + 자가검증 명령 (SK-01)
- [ ] `design-kit/templates/*.html` 8 개 — grid/flex 자식 `min-width:0` (AR-05).
      현재 `component.html` 만 보유 (L251, L648)
- [ ] `design-kit/skills/design-audit/references/audit-criteria.md` — 오버플로/그리드 기준 (SK-02).
      기존 터치타겟 수치(WCAG 2.2 SC 2.5.8 AA 24px / SC 2.5.5 AAA 44px) **낮추지 마라**
- [ ] `scripts/detect-docs-drift.py` — SC-01/SC-02

### Phase B — 오버플로 66 건 (워크플로 백그라운드 실행 중)

Run ID `wf_15bb7aca-d32`, 스크립트
`~/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/8a9c2ebc-8d41-48fb-9586-496555a22b30/workflows/scripts/fix-docs-overflow-66-wf_ccc44852-d73.js`
(KITS 리터럴이 스크립트에 인라인됨 — `args` 로 배열을 넘기면 문자열이 되어 실패한다).

킷별 건수: rust-kit 14 · harness 11 · react-kit 10 · design-kit 9 · flutter-toolkit 7 ·
backend-kit 5 · bambu-kit 4 · infra-kit 4 · onboarding-kit 1 · process 1.

킷마다 수정 에이전트 + **독립 검증 에이전트**가 붙어 자르기·매직넘버·범위 밖 수정을 검사한다.

### Phase C — 액션 v7 (미착수)

`.github/workflows/ci.yml` 6 건: L20/L44/L73 `checkout@v4`→`@v7`, L23 `setup-python@v5`→`@v7`,
L47 `setup-node@v4`→`@v7`, L63 `upload-artifact@v4`→`@v7`. **`with:` 블록은 손대지 마라** —
전 input 이 v7 에서 유효함을 `action.yml` diff 로 확인했다.

배포 템플릿 5 건: `docs/rust/ops/ci-cd.md` 4 건 + `infra-kit/skills/infra-init/SKILL.md` 1 건.
`.harness/history/20260727-kaizen-phase8-infra-sprint-contract.md` 1 건은 **이력이므로 수정 금지**.

### Phase D — release PR 전환 (미착수)

`scripts/release.sh:106-110` 이 `git commit` → `git tag -a` → `git push origin HEAD --follow-tags`.
브랜치 생성 → push → PR 생성으로 바꾼다. 태그는 protection 대상이 아니므로
(`gh api .../tags/protection` → Not Found) 태그 푸시는 유지. `.claude/commands/release.md:40` 동기화 (SK-03).

**SC-06: `bash -n` 만으로 부족 — 임시 브랜치에서 실제 실행해 main 에 커밋·푸시가 안 생기는 걸 확인하라.**

### Phase E — protection (반드시 마지막, D 머지 후)

```bash
cat > /tmp/protection.json <<'JSON'
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
JSON
gh api -X PUT repos/joo6077/claude-plugins/branches/main/protection \
  -H "Accept: application/vnd.github+json" --input /tmp/protection.json
```

**최대 리스크**: main 은 check-run 6 개, PR head 는 3 개다. 차이 3 개
(`build`, `deploy`, `report-build-status`)는 `pages-build-deployment` 소속이라 PR 에 안 뜬다.
하나라도 넣으면 **영구 pending → 머지 완전 차단**. legacy commit status 0 건이라
오타 시 `/status` 가 `total_count: 0` 을 조용히 반환한다.

되돌리기 (ER-02):

```bash
gh api -X DELETE repos/joo6077/claude-plugins/branches/main/protection                        # 전체 해제
gh api -X DELETE repos/joo6077/claude-plugins/branches/main/protection/required_status_checks # 체크만
gh api -X DELETE repos/joo6077/claude-plugins/branches/main/protection/enforce_admins         # admin 강제만
```

적용 후 **DG-04**: `gh pr view <PR> --json mergeStateStatus` 가 `BLOCKED` 로 고착되지 않는지 확인.
고착되면 즉시 위 명령으로 되돌린다.

## detect-docs-drift.py 버그 (SC-01) — 원인 파악 완료

`map_source_to_html()` (L136~) 이 `design-kit/docs/design/` prefix 에서만 subdir 을 보존한다:

```python
if prefix == "design-kit/docs/design/":
    subdir = str(Path(rel).parent) + "/" if Path(rel).parent != Path(".") else ""
    return f"{html_dir}{subdir}{name}.html"
```

실제 출력은 **flat** 이라 `design-kit/docs/design/foundations/color.md` →
`docs/design-kit/foundations/color.html` (부재) 로 매핑된다. 실제 파일은
`docs/design-kit/color-palette.html`. 26/26 전부 MISS → 전부 `[NEW — 신규 생성 필요]` 로
오보되고 재생성 에이전트가 템플릿에서 새로 만들며 기존 수정을 날린다.

`resolve_target()` 의 `STEM_VARIANTS` 는 `-guide` 접미만 처리하므로 `color` → `color-palette`
같은 이름 변화를 흡수하지 못한다. **수정 방향**: subdir 보존 제거 + `docs/index.html`
레지스트리(SSOT)를 stem 기준으로 조회하는 경로 추가.

SC-02 누락 prefix 4 종: `rust-kit/references/`, `react-kit/references/`,
`planning-kit/references/`, `docs/planning/` (미커버 `.md` 20 개).

## 이 스프린트에서 지켜야 할 것

- `design-kit/evals/visuals.spec.js` **수정 금지** (기준 완화 금지 — PR #16 의 전제)
- `.harness/history/**` 수정 금지 (이력 기록물)
- force push 금지 (AP-02)
- 오버플로를 `overflow:hidden` 으로 **자르지 마라** (AR-02). 표·코드는 끝까지 스크롤 도달해야 한다
- 페이지별 매직넘버 폭 도입 금지 (RE-01)
- 완료 후 `harness:qa-evaluator` 로 25 조건 판정 → APPROVE 시 계약 `status: done`

## 범위 밖 (audit-log 에 남길 후속 부채)

터치타겟 249/332 건 44px 미만 (진짜 WCAG AA 위반 24 건: checkbox 20×20 이 19, button 4, li 1) ·
테마 키 파편화 4 종(`dk-theme` 12 / `theme` 3 / `vs-theme` 2 / `cp-theme` 2) ·
dependabot 부재 · 액션 SHA 핀닝 · `allow_auto_merge` ·
`visuals.spec.js` 위생(테스트명 `>=44px` 인데 단정 28/34/38, 44 단정 0 건 · 146 중 13 페이지만 커버 ·
`ER-01` 오라클이 `pageerror` 만 보고 `console.error` 미포착 · `KNOWN_OVERFLOW_PAGES` 80px 관용) ·
`validate-plugin.py` 가 `docs/*.html` 을 전혀 검사하지 않음 ·
`qa-evaluator.md` Step 5 가 파일 저장을 지시하나 frontmatter 에 Write 권한 없음(구조적 모순) ·
계약 SK-01 이 지목한 `design-kit/references/audit-criteria.md` 는 실제로
`design-kit/skills/design-audit/references/` 에 있음
