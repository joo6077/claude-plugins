---
feature: "카이젠 자료 수집이 하네스 저장소를 직접 훑는다"
slug: kaizen-harness-store
created: "2026-10-09 17:54"
complexity: "중간"
conditions: 18
status: active
owner_session: c0c0aae7-8201-45fd-b1e1-338ea412ed57
conditions_digest: sha256:22af0e632a16600c
measurement_digest: sha256:2d6bcbb58b8c9574
locked_at: "2026-10-09 18:01"
---

## 배경

- 2026-10-09 사용자 결정: PC 하나에 하네스 저장소(`~/Hub/10_Dev/harness-store`)를 두고 프로젝트마다 폴더를 둔다. 프로젝트의 `.harness` 는 그 폴더로 가는 바로가기다(harness 0.24.0). 사용자 지시 「카이젠할 때 그거 참고해서 진행하고」.
- 카이젠 자료는 `scripts/collect-kaizen-data.py` 가 모은다. 지금은 `~/Hub/10_Dev` 아래 두 단계 깊이의 `.harness` 만 훑는다(`scripts/collect-kaizen-data.py:728`). 바로가기도 따라가지만 세 단계 깊이(`apps/apps/app_kiosk`)와 Hub 밖 프로젝트는 빠진다.
- 이번 계약: 수집기가 하네스 저장소를 깊이 제한 없이 직접 훑어 프로젝트를 더한다. Hub 에서 찾은 것과 실제 위치가 같으면 한 번만 센다.

## GAP 분석

| 대상 | 증거 | 발견 | 조건 |
| --- | --- | --- | --- |
| 수집기 | `scripts/collect-kaizen-data.py:713-762` | `collect_hub_projects` 가 `*/.harness` · `*/*/.harness` 만 훑음. 같은 곳 판정은 프로젝트 폴더 실제 경로(`project_path.resolve()`) | 스크립트-01 · 스크립트-02 |
| 수집기 | `scripts/collect-kaizen-data.py:1736-1741` | 인자는 `--hub-dir` 하나. 하네스 저장소 위치를 줄 길이 없음 | 스크립트-04 |
| 시험 | `scripts/test-collect-kaizen-data.py:298-312` | Hub 프로젝트 찾기 시험이 없음. `--script <사본>` 으로 음성 대조 가능 | 구조-01 |
| 원격 검사 | `.github/workflows/ci.yml:132` | `python3 scripts/test-collect-kaizen-data.py` 를 이미 돌림 | 구조-01 |

- `python3 scripts/validate-doc-contracts.py` 종료 0 · `violation 0` (kaizen-orchestrator SKILL.md 233행 `options:` 목록이 수집기 인자와 맞아야 한다 — 인자를 더하면 이 목록도 고친다).

기준값(2026-10-09 17:54, 가지 시작점 `ae918dab`, 이 PC 실제 자료): `python3 scripts/collect-kaizen-data.py --skip-validate --output <임시>` 종료 0, `## 2. 외부 프로젝트` 절의 `### ` 제목 12 개(`_sandbox/flutter_colorpicker` `apps` `claude-plugins` `codex-audit-ui-trial` `fit-pal` `fit-pal/app` `fit-pal/server` `flutter_playwright` `iyaki-zip-dev` `navi2025flutter` `purchase-bot` `viseo365`), 그중 `app_kiosk` 가 든 제목 0 개. `python3 scripts/test-collect-kaizen-data.py` 끝 줄 `결과: 31 통과 · 0 실패`.

## 범위 경계

- 하네스 저장소 폴더 구조나 플러그인(harness) 쪽은 바꾸지 않는다. 다른 카이젠 단계(evaluator-kaizen 등)의 자료 읽기도 이 계약 밖.
- 이 PC 의 claude-plugins `.harness` 는 실제 폴더라 「이 레포 자신 빼기」는 실제 자료로 못 재고 시험으로만 잰다.
- 이 저장소 자신의 `.harness` 를 옮기는 일(원격 검사 `ci.yml:273-274` 수정 필요)은 이 계약 밖이다.

```text
# sprint-scope
scripts/collect-kaizen-data.py
scripts/test-collect-kaizen-data.py
.claude/skills/kaizen-orchestrator/SKILL.md
```

공통 정의 — 시험: `python3 scripts/test-collect-kaizen-data.py`. 사례마다 `PASS <사례>` · `FAIL <사례>` 한 줄, 끝 줄 `결과: N 통과 · M 실패`. 새 사례는 임시 폴더에 Hub 폴더와 하네스 저장소 폴더를 만들고 수집기의 프로젝트 찾기 `collect_hub_projects(hub_dir, harness_store=<폴더>)` 를 직접 부른다. 사례 이름은 `하네스 저장소 —` 로 시작한다. 호출이 예외를 내면(원본에는 `harness_store` 인자가 없어 TypeError) 그 사례를 FAIL 로 적고 다음 사례로 간다 — 시험 전체가 멈추지 않는다. 음성 대조의 「원본」은 `git show ae918dab:scripts/collect-kaizen-data.py` 를 임시 파일로 꺼내 `--script` 로 준다.

「프로젝트」 기준: 하네스 저장소 안에서 `sprint-feedback.md` 또는 `sprint-feedback-*.md` 를 **직접** 가진 폴더만 항목이 된다. 항목 이름은 하네스 저장소 기준 상대 경로다. 「같은 곳」 기준: Hub 항목의 `.harness` 실제 경로(`resolve()`)와 하네스 저장소 폴더의 실제 경로가 같으면 같은 곳이고, Hub 쪽 항목 하나만 남는다(이름도 Hub 기준). 기존 프로젝트 폴더 실제 경로 비교는 그대로 둔다.

## Skill

- [ ] 스킬-00: N/A (스킬 동작을 바꾸지 않는다 — kaizen-orchestrator SKILL.md 는 인자 목록 한 줄과 데이터 풀 설명만 고치며 구조-02 · 구조-03 이 잰다)

## Script

- [ ] 스크립트-01: Given Hub 는 비고 하네스 저장소에 `p1` · `p1/app` · `x/y/z` 세 폴더가 `sprint-feedback-a.md` 를 하나씩 갖고, `p1/history` 는 피드백 없이 계약 파일만 가질 때, When 프로젝트를 찾으면, Then 항목 이름이 정확히 `p1` · `p1/app` · `x/y/z` 셋이고 각 피드백 수가 1 이며 `p1/history` 는 없다 [exact, enumerated]
  측정: 시험 출력에 `PASS 하네스 저장소 — 깊이 제한 없이 세 곳` · `PASS 하네스 저장소 — 피드백 없는 폴더 빼기` 두 줄
  음성 대조: 원본을 `--script` 로 주면 두 사례가 FAIL 한다
- [ ] 스크립트-02: Given Hub 의 `_x/proj/.harness` 가 하네스 저장소 `proj` 폴더로 가는 바로가기이고 그 폴더에 피드백 2 개가 있을 때, When 프로젝트를 찾으면, Then 이름이 `_x/proj` 인 항목 하나만 있고 이름이 `proj` 인 항목은 없으며 그 항목 피드백 수가 2 다 [exact]
  측정: 시험 출력에 `PASS 하네스 저장소 — 바로가기와 같은 곳은 한 번` 한 줄
  음성 대조: 원본을 `--script` 로 주면 FAIL 한다. 또 수집기에서 「같은 곳」 판정 한 곳을 지운 사본으로도 FAIL 한다 — 그 줄 위치를 시험 파일 머리 주석에 적는다
- [ ] 스크립트-03: Given 하네스 저장소에 `p1/_from-worktrees/w1` 과 `p1/_from-worktrees/w1/app` (둘 다 피드백 있음), 그리고 실제 위치가 이 레포의 `.harness` 실제 경로(`(REPO_ROOT/.harness).resolve()`)와 같은 폴더가 있을 때, When 프로젝트를 찾으면, Then 경로 어느 단계에든 `_from-worktrees` 가 든 폴더와 이 레포 자신의 폴더는 항목으로 나오지 않는다 [exact, enumerated]
  측정: 시험 출력에 `PASS 하네스 저장소 — 보관 폴더 빼기` · `PASS 하네스 저장소 — 이 레포 자신 빼기` 두 줄
  음성 대조: 원본을 `--script` 로 주면 두 사례가 FAIL 한다
- [ ] 스크립트-04: Given 하네스 저장소 위치로 없는 폴더를 주고 Hub 에 `a/.harness` · `b/c/.harness` 가 피드백을 하나씩 가질 때, When 프로젝트를 찾으면, Then 항목 이름이 정확히 `a` · `b/c` 이고 예외가 없다. 수집기 인자 해석기의 하네스 저장소 인자 기본값이 `Path.home() / "Hub" / "10_Dev" / "harness-store"` 와 같다 [exact]
  측정: 시험 출력에 `PASS 하네스 저장소 — 없으면 Hub 만` · `PASS 하네스 저장소 — 기본 위치` 두 줄(기본값은 시험이 수집기의 인자 해석기에서 읽어 맞댄다)
- [ ] 스크립트-05: Given 이 PC 의 실제 자료, When `python3 scripts/collect-kaizen-data.py --skip-validate --output <임시> 2> <임시 오류>` 를 돌리면, Then 종료 0 이고 표준 오류의 `Traceback` 이 0 건이며, `## 2. 외부 프로젝트` 절의 `### ` 제목 집합이 기준값 12 개를 모두 포함하고 거기서 기준값을 뺀 나머지가 `apps/apps/app_kiosk` 하나다. 같은 제목은 두 번 나오지 않는다 [exact, enumerated]
  측정: 제목에서 백틱 안 이름만 뽑아 `LC_ALL=C sort` 후 기준값 목록과 `comm -13` 이 `apps/apps/app_kiosk` 한 줄, `comm -23` 이 빈 출력; `uniq -d` 빈 출력. 나머지에 다른 이름이 더 있으면 그 이름의 폴더가 Hub 나 하네스 저장소에 실제로 있고 이 계약 뒤에 생겼는지 확인해 `[미검증:ENV]` 와 근거를 적는다(시험 스크립트-01~04 가 같은 판정을 임시 자료로 잰다)

## Error

- [ ] 오류-01: Given 하네스 저장소 안에 읽을 수 없는 폴더(권한 000) 하나와 자기 조상을 가리키는 바로가기 하나가 있을 때, When 프로젝트를 찾으면, Then 예외로 멈추지 않고 끝나며 나머지 폴더 항목을 낸다. 하네스 저장소 안 바로가기는 따라가지 않고 `.git` 폴더는 건너뛴다 [exact]
  측정: 시험 출력에 `PASS 하네스 저장소 — 못 읽는 폴더는 건너뜀` · `PASS 하네스 저장소 — 링크 순환에 안 빠짐` 두 줄(이 PC 사용자 번호 501, 관리자 실행이면 첫 사례를 `SKIP` 으로 적는다)
  음성 대조: 수집기의 폴더 훑기에서 읽기 오류 처리를 지운 사본이면 첫 사례가 FAIL 한다 — 시험 파일 머리 주석에 그 위치를 적는다

## Architecture

- [ ] 구조-01: 시험 전체가 통과한다 — `python3 scripts/test-collect-kaizen-data.py` 종료 0, 끝 줄 `결과: N 통과 · 0 실패`, N ≥ 40 (기준 31 + 새 사례 9) [exact]
  측정: 명령 실행, 끝 줄과 종료 코드
  음성 대조: 원본을 `--script` 로 주면 시험이 끝까지 돌고(중단 없음) `하네스 저장소 —` 사례 가운데 스크립트-01 · 02 · 03 의 다섯 줄이 FAIL 이다
- [ ] 구조-02: 수집기 모듈 설명(`__doc__`)의 자료 원천 목록이 하네스 저장소를 적고, kaizen-orchestrator SKILL.md 의 데이터 풀 설명 절에 하네스 저장소가 원천으로 적혀 있다 [structural, enumerated]
  측정: `python3 -c` 로 수집기를 불러 `'harness-store' in module.__doc__` 이 참; `grep -n 'harness-store' .claude/skills/kaizen-orchestrator/SKILL.md` 가 1 줄 이상이고 그 줄이 `## ` 데이터 풀 절(Step 0 설명) 안이다
- [ ] 구조-03: 문서 대조 검사가 통과한다 — `python3 scripts/validate-doc-contracts.py` 종료 0, 끝 줄에 `violation 0`, SKILL.md 의 `options:` 목록에 새 하네스 저장소 인자가 있다 [exact]
  측정: 명령 실행 · `grep -n 'options:' .claude/skills/kaizen-orchestrator/SKILL.md`
  음성 대조: SKILL.md 의 `options:` 목록에서 새 인자를 빼면 이 검사가 0 이 아닌 종료 코드를 낸다(봉인 전 구현이 없어 못 잰다 — QA 가 사본으로 잰다)

## Anti-patterns

- [ ] 금지-01: 버전을 하드코딩하지 않는다 — plugin.json에서 읽어야 한다
- [ ] 금지-03: bare code fence 금지 — `python3 scripts/validate-plugin.py --check=code-fence` 종료 0

## Reusability

- [ ] 재사용-01: 다른 곳에서도 사용 가능한 컴포넌트를 private으로 만들지 않았다
- [ ] 재사용-02: 프로젝트에 이미 동일/유사 컴포넌트가 있으면 새로 만들지 않고 재사용했다

## Diagnostics

- [ ] 진단-01: N/A (commands.analyze 는 `bash -n scripts/release.sh` 만 잰다 — 이번 범위에 없다. 대신 `python3 -m py_compile scripts/collect-kaizen-data.py scripts/test-collect-kaizen-data.py` 종료 0 을 구조-01 과 함께 잰다)
- [ ] 진단-02: N/A (편집기 진단을 이 세션에서 읽을 수단이 없다 — 대신 진단-01 의 py_compile)
- [ ] 진단-03: N/A (commands.test 도 scripts/release.sh 만 돈다 — 대신 구조-01)
- [ ] 진단-04: N/A (구동할 앱 · 서버 없음 — 실제 자료 실행은 스크립트-05 가 표준 오류 `Traceback` 0 건까지 잰다)
