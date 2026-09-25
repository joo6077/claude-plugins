---
phase: 17
title: "Phase 17 howto-kit — 확보된 외부 근거"
collected: 2026-09-24
method: Claude 에이전트(WebFetch · WebSearch · curl) — Codex 사용 한도 소진, 사용자 지시 「코덱스 대신에 그냥 너가 알아서 진행하라고」(세션 기록 user 2026-09-24T11:54:58.940Z)
inputs: 처리 배정표(.claude/kaizen-input/insights-report.md)의 Phase 17 행 · phase-research-templates.md Phase 17 필수 출처 · 현행화 점검
note: 이 파일이 이 Phase 의 유일한 외부 근거다. 바깥 자료를 새로 찾지 마라. 여기 없는 URL·수치를 지어내지 마라. 없으면 미반영으로 남긴다.
---

조회 수단: Claude(WebFetch·WebSearch·curl) — Codex 한도 소진으로 대체

카이젠 Phase 17 (howto-kit) 외부 근거. 조회일 2026-09-24. 레포 기준은 워크트리 `kaizen-0924` 의 커밋 `76cfb37` 이고 읽기만 했다.
로컬에서 돌린 실측(셸 실행)은 "실측" 으로, 내 판단은 "추론:" 으로 표시했다.

---

## 1. 출처 목록 (실제로 가져온 것만)

셸 동작 표준·도구 문서

1. ShellCheck(셸 스크립트 정적 검사기) 규칙 SC2033 설명 — https://www.shellcheck.net/wiki/SC2033
2. POSIX(유닉스 계열 공통 표준) 2024판, 2장 Shell Command Language — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
3. POSIX 2024판, `find` 명세 — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/find.html
4. bash(1) 매뉴얼 페이지 (man7.org 사본, 업스트림 git 에서 2026-08-03 수집이라고 페이지에 적혀 있음) — https://man7.org/linux/man-pages/man1/bash.1.html
5. zsh 매뉴얼 Functions 장 — https://zsh.sourceforge.io/Doc/Release/Functions.html
6. GNU(자유 소프트웨어 재단 프로젝트) bash 배포 목록 — https://ftp.gnu.org/gnu/bash/
7. ShellCheck 최신 릴리스 (gh 로 조회) — https://github.com/koalaman/shellcheck/releases

Claude Code 플러그인 문서

8. Claude Code 스킬 문서 (Available string substitutions) — https://code.claude.com/docs/en/skills
9. Claude Code 플러그인 참조 (Environment variables · Plugin caching and file resolution · Path traversal limitations) — https://code.claude.com/docs/en/plugins-reference

GitHub Actions 실행 환경

10. actions/runner-images README (라벨 대응표, `-latest` 이동 설명) — https://github.com/actions/runner-images
11. Ubuntu 24.04 이미지 설치 목록 — https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md
12. Ubuntu 24.04 이미지 패키지 목록 파일 — https://github.com/actions/runner-images/blob/main/images/ubuntu/toolsets/toolset-2404.json
13. Ubuntu 26.04 이미지 설치 목록 — https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Readme.md
14. GitHub Docs, Customizing GitHub-hosted runners — https://docs.github.com/en/actions/how-tos/manage-runners/github-hosted-runners/customize-runners
15. actions/checkout 최신 릴리스 — https://github.com/actions/checkout/releases
16. actions/setup-python 최신 릴리스 — https://github.com/actions/setup-python/releases

킷이 인용하는 절차 문서 표준

17. OASIS(표준 단체) DITA(기술 문서 구조 표준) 위원회 페이지 — https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=dita
18. OASIS 문서 디렉터리 `dita/` · `dita/dita/` (그리고 `dita/dita/v2.0/` 은 404) — https://docs.oasis-open.org/dita/dita/
19. DITA 1.3 `<cmd>` · `<stepresult>` · `<taskbody>` 페이지 (셋 다 200) — https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/langRef/technicalContent/cmd.html 외 2 건 (`stepresult.html`, `taskbody.html`)
20. DITA 2.0 Beta 03 릴리스 (2026-07-02) — https://github.com/oasis-tcs/dita/releases/tag/v2.0-beta03
21. DITA 2.0 초안의 task 요소 원문 (`cmd.dita` · `stepresult.dita` · `taskbody.dita`) — https://github.com/oasis-tcs/dita-techcomm/tree/main/specification/langRef/technicalContent
22. Diátaxis, How-to guides — https://diataxis.fr/how-to-guides/
23. Google developer documentation style guide, Procedures — https://developers.google.com/style/procedures
24. Microsoft Writing Style Guide, Writing step-by-step instructions — https://learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions
25. iso.org 의 ISO/IEC/IEEE(국제 표준 기구 세 곳의 공동 표준) 26514:2022 페이지 (시도 — 403, 봇 확인 화면만 옴) — https://www.iso.org/standard/77451.html
26. ISO/IEC/IEEE 26514:2022 무료 견본 PDF (iTeh 배포, 용어 정의 절까지 포함) — https://cdn.standards.iteh.ai/samples/77451/e161501288fd44f88c6fdd0f6e46b017/ISO-IEC-IEEE-26514-2022.pdf

킷 문서가 주기적으로 확인하라고 적은 피드 5 건 (오늘 다시 받음)

27. https://docs.cloud.google.com/feeds/gcp-release-notes.xml
28. https://developer.apple.com/news/rss/news.rss
29. https://developer.apple.com/news/releases/rss/releases.rss
30. https://github.blog/changelog/feed/
31. https://aws.amazon.com/about-aws/whats-new/recent/feed/

WebSearch 결과 목록(26514 판 정보 검색)은 링크만 봤고 본문은 가져오지 않아 인용하지 않는다.

---

## 2. 항목별 관찰 사실

### other-kits:P4 (1) — 부모 셸에서 읽은 함수를 `find -exec sh -c` 자식 셸이 못 부른다

**표준이 말하는 것**

- POSIX 2.13 은 셸 실행 환경에 "Shell functions; see 2.9.5 Function Definition Command" 가 들어 있다고 적는다. 그러나 특수 내장 명령이 아닌 프로그램은 "shall be invoked in a separate environment" 이고, 그 목록에서 넘어가는 것은 열린 파일, 작업 폴더, 파일 생성 마스크, 트랩, 그리고 "Variables with the export attribute, along with those explicitly exported for the duration of the command, shall be passed to the utility environment variables" 뿐이다. 함수는 그 목록에 없다. — 출처 2
- 같은 절은 괄호나 파이프로 생기는 하위 셸은 "A subshell environment shall be created as a duplicate of the shell environment" 라고 한다. 그래서 같은 셸 안의 `find ... | while read` 는 함수를 쓸 수 있고, 새 프로세스로 뜨는 `sh -c` 는 못 쓴다. — 출처 2
- POSIX `find` 의 `-exec ... {} +` 는 `utility_name` 을 새로 실행한다. 또 "The current directory for the invocation of utility_name shall be the same as the current directory when the find utility was started" 라서, `sh -c` 안의 상대 경로는 find 를 시작한 폴더 기준으로 풀린다. "If any invocation returns a non-zero value as exit status, the find utility shall return a non-zero exit status." — 출처 3
- ShellCheck SC2033: "Shell functions can't be passed to external commands. Use separate script or sh -c." / "Shell functions are only known to the shell. External commands like `find`, `xargs`, `su` and `sudo` do not recognize shell functions." 권장 해법 두 가지는 `sh -c` 안에서 실행하기, 또는 별도 스크립트 파일로 두기다. — 출처 1

**반대 근거 (함수를 자식에게 넘기는 방법)**

- bash 매뉴얼: "Functions may be exported so that child shell processes (those created when executing a separate shell invocation) automatically have them defined with the -f option to the export builtin." — 출처 4
- 실측 (bash 에서 `export -f f` 뒤 각 셸로 `f` 호출): macOS `/bin/sh`(bash 3.2) 와 bash 는 `called`, `/bin/dash` 는 `f: not found`, zsh 는 `command not found: f`. Ubuntu 실행 환경의 `sh` 는 dash 다(이미지 목록에 "Dash 0.5.12-6ubuntu5" — 출처 11). 즉 `export -f` 로 고치면 **맥에서는 통과하고 리눅스 CI 와 zsh 에서는 깨진다.**
- zsh 매뉴얼 Functions 장은 함수가 "execute in the same process as the caller" 라고만 하고, 함수를 내보내는 방법은 그 장에서 찾지 못했다. — 출처 5 (그 장에 없다는 뜻이지 zsh 전체에 없다고 확인한 것은 아니다)

**레포 실측 (오늘, 워크트리 루트에서)**

- `howto-kit/skills/howto-audit/SKILL.md:75-80` 의 형태(부모 셸에서 `. howto-kit/scripts/howto-gate.sh` 후 `find -exec sh -c '... howto_gate ...'`)를 zsh 와 bash 로 각각 돌리면 파일마다 `sh: howto_gate: command not found` 만 나온다. 시험 입력 15 개 전체에 돌렸을 때 find 의 종료 코드는 1 이었다.
- `howto-kit/skills/howto-doc/SKILL.md:64-69` 의 Gotcha 3 형태(`.` 를 `sh -c` 안에 둠)는 `GATE_PASS` 까지 정상 출력된다.
- 검사 스크립트 결과가 셸마다 같은지: 시험 입력 15 개 모두에서 bash · `/bin/dash` · macOS `/bin/sh` 출력이 같았다(차이 0 건). 그러니 `.` 를 `sh -c` 안으로 옮겨도 리눅스의 dash 에서 결과가 달라지지 않을 것으로 본다. 추론: 실제 우분투에서는 돌려 보지 않았고, 맥의 dash 버전은 확인하지 않았다.
- ShellCheck 0.11.0 에 audit 형태를 넣으면 SC1091(읽을 파일을 따라가지 않음, info) 하나만 나오고 함수 문제는 잡지 못한다. 따옴표 안 문자열은 검사하지 않기 때문이다. 같은 함수를 `find -exec howto_gate {} +` 로 직접 부르면 SC2032 가 잡는다. → 이 결함은 정적 검사로 막을 수 없고 **실제로 돌려 보는 검사**가 필요하다.
- 추론: audit 형태의 `for` 반복은 마지막 파일의 종료 코드만 남긴다. 앞쪽 파일이 실패해도 마지막 파일이 성공하면 find 가 0 으로 끝날 수 있다. 판정은 종료 코드가 아니라 파일마다 나오는 `GATE_` 줄 수로 세는 편이 안전하다.

### other-kits:P4 (2) — 상대 경로라서 플러그인으로 설치한 프로젝트에서는 스크립트를 못 찾는다

**공식 문서가 말하는 것**

- 스킬 문서의 치환 표: `${CLAUDE_SKILL_DIR}` 는 "The directory containing the skill's `SKILL.md` file. For plugin skills, this is the skill's subdirectory within the plugin, not the plugin root. Use this in bash injection commands to reference scripts or files bundled with the skill, regardless of the current working directory." `${CLAUDE_PLUGIN_ROOT}` 는 "The plugin's installation directory. Substituted only in plugin skills. Use this to reference scripts or files bundled anywhere in the plugin, including resources shared between the plugin's skills." 둘 다 스킬 본문과 `allowed-tools` 의 Bash 규칙에서 치환된다. — 출처 8
- 플러그인 참조: "In plugin content, write the placeholder instead, and Claude Code substitutes the path inline when it loads the content." 스킬·에이전트 본문은 "Anywhere the placeholder appears". 환경 변수로 내보내는 곳은 "hook processes and to MCP and LSP server subprocesses" 로 적혀 있다(MCP·LSP 는 플러그인이 띄우는 보조 서버 종류). — 출처 9
  - 추론: Bash 도구 프로세스는 그 목록에 없으므로, 스킬 본문에서는 `$CLAUDE_PLUGIN_ROOT` 환경 변수에 기대지 말고 **불러올 때 글자로 바뀌는 치환**에 기대야 한다. 또 플러그인이 아닌 경로로 스킬을 읽으면 치환이 안 되고, 셸에서는 빈 값이 되어 `/scripts/howto-gate.sh` 를 찾게 된다. 그래서 `test -f` 로 확인하는 단계가 필요하다.
- 설치 위치: "Claude Code copies *marketplace* plugins to the user's local **plugin cache** (`~/.claude/plugins/cache`), unless the plugin loads in place." 그리고 "Claude Code also doesn't copy files outside the plugin directory into the cache when it installs the plugin". — 출처 9
- 공유 스크립트 위치: 이 검사 스크립트는 `howto-kit/scripts/` 에 있어 세 스킬이 같이 쓴다. 문서가 "resources shared between the plugin's skills" 에는 `${CLAUDE_PLUGIN_ROOT}` 를 쓰라고 하므로, `${CLAUDE_SKILL_DIR}/../../scripts/...` 보다 `${CLAUDE_PLUGIN_ROOT}/scripts/howto-gate.sh` 가 문서 권장과 맞는다. — 출처 8

**점 명령(`.`)이 파일을 못 찾을 때 — 셸마다 다르다**

- POSIX: "If no readable file is found, a non-interactive shell shall abort". 오류 결과 표에서도 특수 내장 명령 오류는 비대화형 셸이면 "shall exit". — 출처 2
- 실측 (레포 밖 폴더에서 `. howto-kit/scripts/howto-gate.sh; echo rc=$?`): `sh`(macOS, bash 의 POSIX 모드)는 그 자리에서 종료(종료 코드 1). bash 는 `rc=1` 을 찍고 **계속 진행**. zsh 는 `rc=127` 을 찍고 **계속 진행**. 그래서 bash·zsh 에서는 다음 줄 `howto_gate` 가 "command not found" 로 넘어가 버린다. 스킬 시작 때 `test -f` 로 먼저 확인하고 멈추게 하자는 인사이트 제안과 맞는다.

**레포 관찰**

- 상대 경로 `. howto-kit/scripts/howto-gate.sh` 를 쓰는 곳은 인사이트가 적은 3 곳(`howto-doc/SKILL.md:66`, `:101`, `howto-audit/SKILL.md:76`) 외에 **`howto-kit/README.md:56`** (사용 예시)와 `howto-kit/scripts/howto-gate.sh:4` (주석의 사용법)도 있다. 총 5 곳. `.claude/skills/howto-kaizen/SKILL.md:90` 은 레포 개발용 목록이라 해당 없음.
- howto-kit 어디에도 `CLAUDE_PLUGIN_ROOT` 나 `CLAUDE_SKILL_DIR` 를 쓰지 않는다.
- 이 맥의 설치 상태: `~/.claude/plugins/cache/joo6077-plugins/howto-kit/0.2.1/scripts/howto-gate.sh` 와 `~/.claude/plugins/marketplaces/joo6077-plugins/howto-kit/scripts/howto-gate.sh` 가 있고, 레포 파일과 셋 다 같은 SHA-1(파일 내용 지문) `88104f96…` 이다(오늘 기준). 설치본 폴더 이름에 버전(`0.2.1`)이 들어간다.
- harness `refactor-checklist/SKILL.md:52-61` 의 경로 찾기 순서는 (1) `${CLAUDE_PLUGIN_ROOT}/{rel}` → (2) `{repo_root}/{kit}/{rel}` → (3) `ls -1d "$HOME"/.claude/plugins/marketplaces/*/{kit}/{rel} | head -1`. (3) 은 `marketplaces` 폴더를 본다. 공식 문서가 복사본 위치로 적은 곳은 `~/.claude/plugins/cache` 이고, `marketplaces` 폴더에 대한 설명은 가져온 문서에서 찾지 못했다. — 출처 9
  - 추론: 이 맥에서는 두 폴더가 다 있어서 지금은 어느 쪽이든 찾는다. 다만 howto-kit 용으로 옮길 때 (3) 에 `cache/*/howto-kit/*/scripts/howto-gate.sh` 를 쓰면, 버전 폴더가 여러 개일 때 `head -1` 이 가장 오래된 버전을 집을 수 있다(`ls` 는 이름순이라 `0.10.0` 이 `0.2.1` 보다 앞선다).

### other-kits:P3 (1) — CI(깃허브에 올릴 때 자동으로 도는 검사)에 howto evals 단계 추가

**레포 관찰**

- `.github/workflows/ci.yml` 에 `howto-kit/evals/run-evals.sh` 를 부르는 단계가 없다. 일반 eval 단계는 `ci.yml:46-47` 의 `python3 scripts/run-evals.py --verbose` 하나이고, `scripts/run-evals.py:32-35` 의 `ALL_KITS` 에 howto-kit 과 onboarding-kit 이 없다.
- `run-evals.sh:16` 은 zsh 가 없으면 `SHELL_MISSING zsh` 를 찍고 exit 2 로 끝난다. `evals.json` 의 `runner` 값은 `bash howto-kit/evals/run-evals.sh`, 스크립트 머리 주석(`run-evals.sh:3`)은 `sh ...` 로 적혀 있다.
- 실측: `/bin/dash howto-kit/evals/run-evals.sh` → `EVALS total=16 pass=16 fail=0`, `EVALS_PASS`, 종료 코드 0. 우분투의 `sh`(dash)로 불러도 돌아갈 것으로 본다. 추론: 우분투에서 직접 돌린 것은 아니다.

**실행 환경이 말하는 것**

- `ubuntu-latest` 는 지금 Ubuntu 24.04 를 가리킨다("`ubuntu-latest` or `ubuntu-24.04`"). "The `-latest` migration process is gradual and happens over 1-2 months" 이고, 고정 라벨로 이동을 피할 수 있다고 적혀 있다. Ubuntu 26.04 는 public preview 로 올라와 있다. — 출처 10, 11
- Ubuntu 24.04 이미지(Image Version 20260907.300.1) 설치 목록: "Bash 5.2.21(1)-release", "Dash 0.5.12-6ubuntu5", "Python 3.12.3". **zsh 항목 없음.** 패키지 목록 파일의 `vital_packages` · `common_packages` · `cmd_packages` 에도 zsh 없음(`shellcheck` 는 있음). — 출처 11, 12
- Ubuntu 26.04 이미지(Image Version 20260907.131.1): "Bash 5.3.9(1)-release", "Dash 0.5.12-12ubuntu3", "Python 3.14.4". 여기에도 **zsh 항목 없음.** — 출처 13
  - 추론: `-latest` 가 26.04 로 넘어가도 zsh 설치 단계는 여전히 필요하다. 이미지 목록에 없다는 것이 "간접 설치로도 절대 없다" 는 증명은 아니므로, `command -v zsh` 로 확인하고 없으면 설치하는 방식이 맞다.
- GitHub 공식 예시는 `sudo apt-get update` 뒤 `sudo apt-get install jq`. 문서: "Always run `sudo apt-get update` before installing a package. In case the `apt` index is stale, this command fetches and re-indexes any available packages, which helps prevent package installation failures." — 출처 14
- 추론: `ci.yml:115-120` 의 yq 단계처럼 "도구가 없으면 SKIP 을 찍고 통과" 하는 모양을 그대로 베끼면, zsh 가 없을 때 howto evals 가 **조용히 건너뛰고 초록불**이 된다. zsh 는 설치하고, 설치가 안 되면 단계가 실패해야 한다.

### other-kits:P3 (2) — onboarding-kit 시험 입력 3 개가 등록도 실행도 안 돼 있다

**레포 관찰**

- `onboarding-kit/skills/setup-guide/evals/fixtures/` 에 `gate-ok-flutter.md` · `gate-g4-ko-sourced.md` · `gate-g4-ko-unsourced.md` 가 있다. `evals.json` 에서 이 이름을 찾으면 0 건이고, `.harness/` 와 fixtures 폴더 밖에서 이 이름을 쓰는 파일도 없다.
- `guide_gate` 함수는 `setup-guide/SKILL.md:54-113` (코드 블록은 `:50-114`)에 있다. 같은 스킬 `:222-224` 는 `find ... | while IFS= read -r f; do ... guide_gate ...; done` 으로 **같은 셸의 하위 셸**에서 부르므로 함수가 보인다(POSIX 의 하위 셸 = 환경 복제 — 출처 2). howto-audit 과 달리 이쪽은 구조상 문제없다.

**실측 (SKILL.md 의 함수 블록을 그대로 뽑아 bash · zsh 에서 실행)**

| 시험 입력 | 스택 | bash · zsh 공통 결과 |
|---|---|---|
| gate-ok-flutter.md | flutter | `G3_STACKMIX PASS stack=flutter swift_fence=0` · `G4_DEPRECATION PASS unsourced_boxes=0` · `GATE_PASS` |
| gate-ok-flutter.md | (빈 값) | `G3_STACKMIX FAIL stack=unset swift_fence=0` · `GATE_FAIL` |
| gate-g4-ko-sourced.md | flutter | `G4_DEPRECATION PASS unsourced_boxes=0` · `GATE_PASS` |
| gate-g4-ko-unsourced.md | flutter | `G4_DEPRECATION FAIL unsourced_boxes=1` · `GATE_FAIL` |

인사이트가 적은 기대 줄 두 개(`G4_DEPRECATION FAIL unsourced_boxes=1`, `G3_STACKMIX FAIL stack=unset`)가 그대로 나온다.

- 실측 중 겪은 일: 처음에 zsh 에서 `set -- $c` 로 인자를 나누려다 zsh 가 단어를 쪼개지 않아 모든 경우가 `GATE_BLOCKED no_such_file=...` 로 나왔다. `run-evals.sh:7-8` 이 적어 둔 것과 같은 함정이다. 새로 만드는 실행 스크립트에서 `set -- $var` 를 쓰지 않아야 한다.
- 추론: 함수 블록을 **줄 번호**(51-113)로 뽑으면 SKILL.md 가 한 줄만 바뀌어도 어긋난다. `guide_gate() {` 부터 맨 앞 칸의 첫 `}` 까지 **표시 문자열**로 잘라야 한다.

---

## 3. 현행화 — 낡은 곳

직전 카이젠(2026-08-13) 뒤로 이 킷이 다루는 도구·표준을 다시 대조했다. **버전이 낡아서 고쳐야 할 곳은 찾지 못했다.** 대신 "지켜볼 것" 과 "주장과 검사 범위가 어긋난 것" 이 있다.

| 파일:줄 | 현재 값 | 최신 확인 값 | 판정 | 출처 |
|---|---|---|---|---|
| `docs/howto/procedure-standards.md:18-20`, `:63` · `howto-kit/references/step-contract.md:54`, `:74-81` · `docs/howto/design-brief.md:79`, `:225`, `:237-239` | DITA 1.3 인용 (`<cmd>` "should not be more than one sentence", `<stepresult>` "should not be used for every step", task 모델 둘) | OASIS 표준은 여전히 1.3 ("OASIS Standard, approved 17 December 2015", Errata 02 "approved on 29 June 2018"). 2.0 은 Beta 03 (2026-07-02) 이고 `docs.oasis-open.org/dita/dita/` 에는 `v1.3/` 만 있다. 1.3 페이지 셋 다 오늘 200 | **낡지 않음.** 다만 지켜볼 것 — 2.0 초안의 `cmd.dita` · `stepresult.dita` 원문에는 "one sentence" · "every step" 문장이 **없다**. `taskbody.dita` 는 "strict task or general task document-type shell" 구분을 그대로 둔다 | 17, 18, 19, 20, 21 |
| `docs/howto/procedure-standards.md:83-96` · `howto-kit/references/provenance-notes.md:229-243` | ISO/IEC/IEEE 26514 · 26515 `[미확인]`, "iso.org 는 5.5KB 스텁만 응답" | iso.org 는 오늘도 403 과 "Just a moment..." 제목의 5,629 바이트 봇 확인 화면. 기록과 같다. 새로 찾은 것: iTeh 무료 견본 PDF 에서 26514 가 "First edition 2022-01" 이고, 용어 정의 원문(3.1.39 procedure "ordered series of steps that specify how to perform a task", 3.1.48 step "element (numbered list item) in a procedure that tells a user to perform an action (or actions)", 주석 "Responses by the software are not considered to be steps.", 3.1.3 action "element of a step that a user performs during a procedure")을 확인 | 낡지 않음. **정의 수준은 이제 인용 가능**, 절차 작성 세부 조항은 여전히 미확인. 26515 는 이번에 조회하지 않음 | 25, 26 |
| `docs/howto/design-brief.md:78`, `:83`, `:298` | Google "In general, use one step for each action." · Microsoft "Make sure that customers know where the action should take place before you describe the action." · Diátaxis "guide the reader through a problem or towards a result" | 세 문장 모두 오늘 원문에 그대로 있음 (셋 다 200) | 낡지 않음 | 22, 23, 24 |
| `docs/howto/changelog-feeds.md:19-25` | 확정 피드 5 건 (조회 2026-09-09) | 5 건 모두 200, 형식 동일(Google 은 Atom `<feed>`, 나머지 RSS(구독용 피드 형식) `<rss>`), 최신 항목 날짜 2026-09-18 ~ 09-24 | 낡지 않음 | 27~31 |
| `.github/workflows/ci.yml:18` (그리고 `:72`, `:107`) | `runs-on: ubuntu-latest` | 지금은 24.04. 26.04 가 public preview 이고 `-latest` 는 1~2 개월에 걸쳐 옮겨 간다. 두 이미지 모두 zsh 없음 | 새 howto 단계에 영향: zsh 설치 단계가 두 이미지 모두에서 필요 | 10, 11, 13 |
| `.github/workflows/ci.yml:20`, `:23` | `actions/checkout@v7`, `actions/setup-python@v7` | checkout v7.0.1 (2026-07-20), setup-python v7.0.0 (2026-07-20) | 최신 | 15, 16 |
| `howto-kit/scripts/howto-gate.sh:7` 와 `howto-kit/evals/run-evals.sh:39-40` | 스크립트 주석은 "zsh · bash · sh 에서 동일 출력" 이라 하는데, 실행기는 zsh 와 bash 만 대조 | 실측: 15 개 시험 입력에서 bash · dash · macOS sh 출력 동일 | 주장은 오늘 맞지만 **실행기가 sh(dash)를 재지 않는다.** 스킬이 실제로 쓰는 셸은 `sh -c` 다 | 실측 |
| `harness/skills/refactor-checklist/SKILL.md:60` (옮겨 올 대상) | 3 단계가 `~/.claude/plugins/marketplaces/*/{kit}/{rel}` | 공식 문서가 적은 설치 복사본 위치는 `~/.claude/plugins/cache` | 낡았다고 단정 못 함(`marketplaces` 설명을 문서에서 못 찾음). howto-kit 에 옮길 때 두 곳을 다 볼지 정해야 함 | 9 |
| (킷 전체) | 셸·파이썬 버전을 박아 둔 곳 없음 | bash 최신 배포 5.3 (배포 목록의 `bash-5.3.tar.gz` 2025-07-30), 러너 bash 5.2.21 / 5.3.9, ShellCheck 최신 v0.11.0 (2025-08-04) | 해당 없음 | 6, 7, 11, 13 |

---

## 4. 권장안 (이 Phase 가 계약 조건으로 삼을 만한 것)

1. **howto-audit 의 호출 형태를 howto-doc Gotcha 3 과 같게 고친다** (`howto-audit/SKILL.md:75-80`). 근거: 출처 1·2, 실측.
   조건 예: SKILL.md 의 해당 코드 블록을 **파일에서 뽑아서**(손으로 다시 치지 말고) 레포 루트에서 zsh 와 bash 로 `howto-kit/evals/fixtures` 에 돌렸을 때 `command not found` 0 건, `GATE_` 로 시작하는 마지막 줄이 파일 수(15)만큼 나온다. 고치기 전 형태로는 `command not found` 가 15 건 나오는 것도 함께 확인한다(검사가 살아 있다는 증거).

2. **스크립트 경로를 한 번에 찾고, 못 찾으면 시작 단계에서 멈춘다.** 근거: 출처 8·9, POSIX 점 명령(출처 2), 셸별 실측.
   - 찾는 순서: `${CLAUDE_PLUGIN_ROOT}/scripts/howto-gate.sh` → 레포의 `howto-kit/scripts/howto-gate.sh` → 설치 복사본. 각각 `test -f` 로 판정한다.
   - 못 찾으면 첫 줄에 "검사 스크립트를 못 찾음" 과 찾아본 경로 3 개를 찍고 멈춘다.
   - 추론: 찾은 경로는 `sh -c '...'` 의 따옴표 안에 글자로 붙이지 말고 인자나 환경 변수로 넘긴다(`sh -c '. "$G"; ...'` 형태). 홈 폴더 경로에 공백이 있으면 따옴표 안에 붙인 경로가 깨질 수 있다.
   - 적용 자리: `howto-doc/SKILL.md:66`, `:101`, `howto-audit/SKILL.md:76`, 그리고 인사이트에 빠진 **`howto-kit/README.md:56`**. `howto-gate.sh:4` 의 주석 사용법도 맞춘다.
   - 조건 예: 레포 밖 빈 폴더에서 실행하면 (a) 설치본을 찾아 `RESOLVED:` 를 찍거나 (b) 3 개 경로를 찍고 0 이 아닌 코드로 끝난다. 어느 쪽이든 `command not found` 는 0 건이다.

3. **`export -f` 로 고치지 않는다.** 근거: 실측에서 dash(우분투의 sh)와 zsh 자식에게는 함수가 넘어가지 않았다. 맥에서만 통과하는 고침이 된다.

4. **CI 에 howto evals 단계를 넣는다.** 근거: 출처 10~14, dash 실측.
   - 모양: `command -v zsh >/dev/null || { sudo apt-get update && sudo apt-get install -y zsh; }` 다음에 `sh howto-kit/evals/run-evals.sh`.
   - yq 단계처럼 "없으면 SKIP" 으로 두지 않는다. zsh 가 없으면 `run-evals.sh` 가 exit 2 로 실패하는 지금 동작을 그대로 살린다.
   - 조건 예: CI 기록에 `EVALS total=16 pass=16 fail=0` 과 `EVALS_PASS` 가 보인다. 로컬에서는 시험 입력의 기대값 하나를 일부러 틀리게 바꿔 이 단계가 실패하는지 확인한다.

5. **onboarding 시험 입력 3 개를 등록하고 같은 CI 단계에서 돌린다.** 근거: 2 절의 실측 표.
   - 기대 줄은 위 표의 4 가지 경우를 그대로 쓴다.
   - 실행 스크립트는 `guide_gate() {` 부터 첫 `^}` 까지 표시 문자열로 잘라 zsh·bash 에서 돌리고, 두 셸 출력이 다르면 실패로 친다(howto `run-evals.sh` 와 같은 모양). `set -- $var` 는 쓰지 않는다.

6. **정적 검사로 대신하지 않는다.** ShellCheck 는 따옴표 안 `sh -c` 문자열의 함수 호출을 못 잡는다(실측). 1·2 번 조건은 반드시 실제 실행 결과로 잰다.

7. (선택, 이번 범위 밖) `provenance-notes.md` 에 두 가지를 기록해 둘 만하다: DITA 2.0 초안에서 인용 문장 두 개가 빠졌다는 것(2.0 이 표준이 되면 다시 볼 것), 그리고 26514:2022 용어 정의는 무료 견본으로 확인할 수 있다는 것.

---

## 5. 못 가져온 것 / 열린 질문

- gnu.org 의 bash 매뉴얼 페이지는 WebFetch 429, curl 403 으로 못 받았다. 같은 문장을 man7.org 의 bash(1) 사본(출처 4)에서 가져왔다.
- iso.org(403 봇 확인 화면)와 IEEE 표준 페이지(Cloudflare "Attention Required")는 본문을 못 받았다. ISO/IEC/IEEE 26515 는 이번에 조회하지 않았다.
- 공식 문서에서 `~/.claude/plugins/marketplaces` 폴더의 역할 설명은 찾지 못했다(없다는 뜻은 아니다).
- `${CLAUDE_SKILL_DIR}` · `${CLAUDE_PLUGIN_ROOT}` 치환이 스킬 본문에 언제부터 들어왔는지 날짜는 찾지 않았다.
- Bash 도구가 뜰 때 `CLAUDE_PLUGIN_ROOT` 환경 변수가 설정되는지는 문서에 없고(훅·MCP·LSP 만 적혀 있음) 직접 확인하지도 않았다.
- 우분투 실행 환경에서 직접 돌려 보지 않았다. dash 동작은 맥의 `/bin/dash` 로만 쟀다.
- 열린 질문: 이 레포에서 킷을 고치면서 시험할 때는 `${CLAUDE_PLUGIN_ROOT}` 가 **설치 복사본**을 가리킨다. 레포에서 막 고친 스크립트보다 옛 버전이 먼저 잡힐 수 있다(오늘은 셋이 같은 내용이라 드러나지 않음). 레포 경로를 먼저 볼지, 찾은 경로를 항상 찍어서 사람이 보게 할지 정해야 한다.
- 열린 질문: 설치 복사본을 찾을 때 `cache/*/howto-kit/*/` 처럼 버전 폴더가 여럿이면 어느 것을 고를지. `ls | head -1` 은 이름순이라 최신을 보장하지 않는다.
