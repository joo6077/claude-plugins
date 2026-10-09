## 1. 확인된 결함

### 막아야 함 — CRLF 가이드에서 G5가 빈 필수 칸을 정상으로 통과시킴

위치: [onboarding-kit/skills/setup-guide/SKILL.md:124](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/onboarding-kit/skills/setup-guide/SKILL.md:124)

`trim()`과 행 끝 정규식이 `\r`을 제거하지 않습니다. 같은 표라도 CRLF이면 헤더 마지막 칸이 `우회\r`가 되어 표를 시작하지 못하고, 잘못된 행을 `rows=0`으로 통과시킵니다.

재현:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import pathlib, subprocess, tempfile

awk = r'''function trim(text){ gsub(/^[ \t]+|[ \t]+$/, "", text); return text }
/^\|/ {
 row=$(0); sub(/^\|/, "", row); sub(/\|[ \t]*$/, "", row)
 ncell=split(row, cell, "|")
 for (i=1; i<=ncell; i++) cell[i]=trim(cell[i])
 if (ncell==4 && cell[1]=="요구" && cell[2]=="출처" &&
     cell[3]=="막히는 것" && cell[4]=="우회") { in_table=1; next }
 if (!in_table || row ~ /^[ \t:|-]+$/) next
 rows++
 if (ncell!=4 || cell[1]=="" || cell[2]=="" || cell[3]=="" || cell[4]=="") empty++
 if (cell[2] !~ /http/) nourl++
}
END { print rows+0, empty+0, nourl+0 }'''

body = '| 요구 | 출처 | 막히는 것 | 우회 |\n| --- | --- | --- | --- |\n| 필수 도구 | https://example.test |  | 대체 도구 |\n'
with tempfile.TemporaryDirectory(dir='/tmp') as d:
    for kind, nl in [('LF', '\n'), ('CRLF', '\r\n')]:
        p = pathlib.Path(d) / f'{kind}.md'
        p.write_bytes(body.replace('\n', nl).encode())
        out = subprocess.run(['awk', awk, str(p)], text=True,
                             capture_output=True, check=True).stdout.strip()
        rows, empty, nourl = map(int, out.split())
        verdict = 'FAIL' if empty or nourl else 'PASS'
        print(f'{kind}: G5_BLOCKING {verdict} rows={rows} empty={empty} nourl={nourl}')
PY
```

실제 출력:

```text
LF: G5_BLOCKING FAIL rows=1 empty=1 nourl=0
CRLF: G5_BLOCKING PASS rows=0 empty=0 nourl=0
```

영향: Windows checkout나 CRLF로 생성된 온보딩 가이드에서 출처·막히는 것·우회가 비어 있어도 완료 게이트가 성공합니다. 기존 평가 11건은 모두 LF라서 `EVALS_PASS`였지만 이 실패 형태를 다루지 않습니다. 각 입력 줄에서 `\r`을 제거해야 합니다.

### 고치면 좋음 — 시각 변경 정본이 승인 기록 규칙을 잘못된 Step으로 연결함

위치: [design-kit/references/visual-change-protocol.md:223](/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/after-0926b/design-kit/references/visual-change-protocol.md:223)

이 줄은 승인 기록의 폐기 칸 규칙을 `design-mockup Step 6`이라고 가리키지만, 현재 Step 6은 Figma 전송이고 승인 기록은 Step 5입니다.

재현:

```bash
rg -n '^## Step 5:|^## Step 6:|design-mockup.*Step 6' \
  design-kit/skills/design-mockup/SKILL.md \
  design-kit/references/visual-change-protocol.md
```

실제 출력:

```text
design-kit/references/visual-change-protocol.md:223:... (`design-mockup` Step 6).
design-kit/skills/design-mockup/SKILL.md:152:## Step 5: 승인 기록 생성 (확정 시 필수)
design-kit/skills/design-mockup/SKILL.md:183:## Step 6: Figma 전송 (선택)
```

영향: 규약을 따라 세부 절차를 찾는 에이전트가 무관한 Figma 전송 절로 이동합니다. 이번 가지가 Step 번호를 재배치하면서 생긴 원문·사본 불일치입니다.

1차 점검의 두 결함은 실제로 고쳐졌습니다.

- 외부 CSS의 `HTTPS://`, URL 앞 공백, 대문자 태그가 모두 탐지됨.
- sprint 정본과 Flutter·React 원인 판정표가 일치하며 `check-cause-table-copies.py`도 통과함.

## 2. 가설

- 가설: `detect-docs-drift.py --since origin/main`은 190개 재생성 대상을 내고 그중 19개를 `[NEW — 대응 HTML 없음]`으로 보고합니다. docs-site 규칙의 “리서치 문서 1개 = HTML 페이지 1개”를 엄격히 적용하면 미완료지만, HTML은 이번 검토 범위에서 제외됐고 일부 원본 변경은 마크다운 모양 정리뿐이어서 병합 차단 결함으로 확정하지 않았습니다.
- 가설: `check-cause-table-copies.py`의 정본 범위가 첫 `- **미확정**` 줄에서 끝나므로 그 뒤에 추가되는 새 규칙은 사본에서 빠져도 통과할 수 있습니다. 현재 사본에는 실제 불일치가 없어 미래 회귀 가능성으로만 남깁니다.

## 3. 돌려 본 것과 결과, 못 본 범위

필수 실행 결과:

- `commit-guard-test.sh`: 실패 0건. 정상 커밋 허용, 51/60개 삭제 차단, 하위 폴더 `commit -a`, 결합 `git add`, 경로 지정 커밋, 범위 밖 경로 차단 모두 통과.
- 별도 `/tmp` 저장소:
  - 정상 수정: `RC=0`, 출력 없음
  - 55개 삭제: `RC=2`, `삭제 55 개가 실린 커밋을 막았다`
  - 범위 밖 `out/outside.txt`: `RC=2`, `계약 범위 목록 밖 경로 1 개`
  - `TemporaryDirectory` 종료 후 폴더 제거 확인.
- `save-test.sh`: `=== ALL TESTS PASSED ===`
- `validate-plugin.py`: 14 plugins, 14 OK, rc 0
- `run-kaizen-assertions.py`: 14 passed, 0 failed
- `check-api-kit-docs.py`: 12/12 PASS
- `check-reviewer-protocol-copies.py`: 9 checked, violations 0
- `check-cause-table-copies.py`: 2 checked, violations 0
- `detect-docs-drift.py --check-table`: 스크립트 45짝·표 34짝·어긋남 0

추가 실행:

- `run-evals.py`: 122 passed, 0 failed
- sync-docs/evals/orchestrator check-only: 모두 rc 0
- 내부 링크 614개 및 등록 페이지 188개: 이상 없음
- stale-value, contrast claim, collector, reflect 훅, measure helper, design gate, Bambu gate, onboarding/howto 평가: 모두 통과
- Python AST, 변경된 셸 `bash -n`, `git diff --check`: 통과
- 최종 `git status --short`: 빈 출력. 저장소 수정 없음.

못 본 범위:

- Playwright 브라우저·픽셀 테스트는 실행하지 않았습니다.
- 로컬 markdownlint 실행 파일이 없어 전체 경고 수를 독립 재측정하지 못했습니다.
- 요청에서 제외한 생성 HTML 내용 자체는 검토하지 않았습니다.
- 외부 문서의 최신성·링크 내용은 네트워크로 재검증하지 않았습니다.