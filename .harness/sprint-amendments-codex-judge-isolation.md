# Sprint Amendments — codex-judge-isolation / 개정 1

봉인 기준은 원 계약 `.harness/sprint-contract-codex-judge-isolation.md` 의 `conditions_digest: sha256:d1e0c6639fea2acf`, `measurement_digest: sha256:7d4bba22350ba3d0`, `locked_at: "2026-10-07 14:50"`, 봉인 커밋 `cd68799d` 다. 조건 줄 · 측정 줄 · 봉인 필드는 고치지 않는다. 아래 네 건은 측정 묶음(`.harness/.meta/codex-judge-isolation/measure/`)과 계약의 서술 줄을 고쳐, 측정이 조건 문구를 글자 그대로 재게 바로잡은 것이다.

## 동의

- 질문: AskUserQuestion 「봉인 뒤 측정을 고친 네 건을 개정으로 인정할까요?」(네 건의 내용과 이전 · 이후 동작을 질문에 그대로 적었다). 답: 「네 건 모두 동의 (추천)」.
- 앵커: `/Users/jackson/.claude/projects/-Users-jackson-Hub-10-Dev-claude-plugins/35b5945f-4957-4359-9b18-2d22b3bafeb0.jsonl` 1643 행 호출(`toolu_019e7TDKqE92aRMxy89FaoGk`, `2026-10-07T06:03:09.550Z`, uuid `d34bffa5-a0ba-4ef5-9c58-03bfbeb619dd`) · 1644 행 응답(**동의 시각** `2026-10-07T06:59:22.296Z`, uuid `39f1ff00-813e-443a-ad35-0dbf85176394`), cwd `/Users/jackson/Hub/10_Dev/claude-plugins/.claude/worktrees/codex-judge-isolation`.
- consent: anchored. 선후: ① · ② · ③ 의 측정 수정 커밋(`33eb890c` · `e091f39b`)은 동의보다 먼저 들어갔다 — 측정 결함을 찾은 직후 고치고 바로 물었다. ④ 와 이 파일은 동의 뒤에 커밋한다.

## AM-01 — relaxing · 판정 사본 경로를 `-C` 에서 읽기 (스크립트-02 · 스크립트-04)

- 변경: 가짜 codex 가 기록하는 차례 작업 폴더를 자기 프로세스 위치(`os.getcwd()`, 언제나 픽스처 저장소) 대신 codex 호출 인자 `-C` 값으로 적는다.
- 이유: 조건은 「가짜 codex 가 기록한 각 판정 · 재심 차례의 작업 폴더(판정 사본) 경로」를 잰다. 옛 측정은 저장소 폴더를 재서 그 폴더가 늘 있으니 스크립트-04 가 어떤 구현에도 FAIL 했고(통과 집합 공집합), 스크립트-02 의 「사본 쓰기」 칸도 저장소에 써 보고 있었다.
- direction 계산(측정 집합, `amend_direction_oracle` 규칙): 원 측정 대상 {픽스처 저장소}, 개정 측정 대상 {판정 사본}. removed={픽스처 저장소} added={판정 사본} → `relaxing measured_removed=1 measured_added=1`. 통과 집합이 공집합에서 늘어나므로 완화다.

## AM-02 — relaxing · 스크립트-02 샌드박스 확인을 판정과 같은 환경으로

- 변경: `codex sandbox -P` 를 띄울 때 `TMPDIR` 과 `PATH` 를 그 판정 차례가 받은 값(가짜 codex 가 기록한 `TMPDIR` · `PATH`)으로 주고, 두 칸을 `python3 -c 1` · `node -e 1` 이름만으로 부른다. 양성 대조(`--positive`)는 측정 폴더와 실제 경로로 푼 PATH 를 쓴다.
- 이유: 조건은 「판정 차례에 감독이 쓴 config.toml 을 그대로 쓴 codex sandbox」 와 「`python3 -c 1` 종료 0 · `node -e 1` 종료 0」 이다. 옛 측정은 측정 프로세스의 시스템 임시 폴더를 `TMPDIR` 로 넘겨 `:workspace` 가 시스템 임시 폴더 전체를 열었고(다른 감독 미끼가 읽힘), node 를 판정이 쓰지 않는 바로가기 경로로 불렀다.
- direction 계산: 원 측정 집합 {측정 프로세스 TMPDIR, 바로가기 경로 node}, 개정 측정 집합 {판정 TMPDIR, 판정 PATH 의 node} → `relaxing measured_removed=2 measured_added=2`.
- 구현 쪽 대응: 판정 차례에 넘기는 `PATH` 를 실제 경로로 풀었다(`f2dd4832` · `resolved_path`). 판정 격리가 바로가기 경유 실행을 막아 fnm 의 node 가 돌지 않았기 때문이다.

## AM-03 — relaxing · 진단-02 의 「더한 줄」 세기

- 변경: BASE 대비 바뀐 줄이 없는 파일은 더한 줄 0 개로 센다. 옛 측정은 파일 전체를 더한 줄로 셌다. 양성 대조(`--positive`)일 때만 파일 전체를 센다.
- 이유: 조건은 「BASE 대비 더한 줄(`git diff -U0` 의 `+` 줄 번호)에 걸린 경고」 다. 바뀌지 않은 파일에는 더한 줄이 없다.
- direction 계산: 원 측정 집합 {바뀌지 않은 파일의 모든 줄 ∪ 더한 줄}, 개정 측정 집합 {더한 줄} → `relaxing measured_removed=1 measured_added=0`.

## AM-04 — relaxing · 계약 서술 줄 두 개 (진단-02)

- 변경: 계약 frontmatter 다음에 제목 줄 `# Codex 감독 판정 격리 · 용량 · 비용 · 속도 최적화` 를 넣고, 봉인한 스크립트-01 조건 줄 바로 위에 `<!-- markdownlint-disable-next-line MD037 -->` 를 넣었다. 두 줄 모두 들여쓰지 않은 서술 줄이라 봉인은 그대로다(`SEAL_OK` · `MEASURE_OK` 확인).
- 이유: 계약 자신의 경고 2 개 — MD041(첫 줄 제목 없음, 이 저장소 다른 계약은 제목 줄이 있어 안 난다)과 MD037(스크립트-01 줄의 `judge-* · review-*` 를 강조 기호로 잘못 읽음). MD037 이 걸린 줄은 봉인한 조건 줄이라 문구를 고칠 수 없다.
- direction 계산: 원 측정 집합 {MD037 이 걸린 스크립트-01 줄을 포함한 계약 더한 줄}, 개정 측정 집합 {그 줄의 MD037 만 뺀 같은 집합} → `relaxing measured_removed=1 measured_added=0`. 다른 규칙 · 다른 줄은 그대로 잰다.
