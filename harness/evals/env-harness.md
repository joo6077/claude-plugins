## EVAL DEFINITION: env-harness

환경 하네스가 반복 실수를 실제로 차단하는지 검증한다.

### Capability Evals

#### ENV-CAP-01: SessionStart 진단
- Task: 새 세션 시작 시 환경 진단이 자동 실행됨
- Success Criteria:
  - [ ] OS 감지 정확 (windows/macos/linux)
  - [ ] fvm 명령어 경로 올바름 (windows → fvm.bat)
  - [ ] .dart_defines.json 존재 여부 보고
  - [ ] .env 존재 여부 보고
  - [ ] adb 디바이스 연결 상태 보고

#### ENV-CAP-02: fvm 차단
- Task: Windows에서 `fvm flutter analyze` 실행 시도
- Expected: exit code 2로 차단, "fvm.bat을 사용하세요" 메시지
- Success Criteria:
  - [ ] `fvm` 명령이 차단됨
  - [ ] `fvm.bat` 명령은 통과
  - [ ] 차단 메시지가 Claude에게 전달됨

#### ENV-CAP-03: dart_defines 차단
- Task: .dart_defines.json 없이 `flutter run --dart-define-from-file=.dart_defines.json` 시도
- Expected: exit code 2로 차단, 해결 방법 안내
- Success Criteria:
  - [ ] 파일 없으면 차단
  - [ ] 파일 있으면 통과
  - [ ] 해결 방법(resolve-host.sh) 안내됨

### Regression Evals

#### ENV-REG-01: 정상 명령 통과
- Tests:
  - fvm.bat-flutter-analyze-passes: PASS/FAIL
  - flutter-run-without-defines-flag-passes: PASS/FAIL
  - non-flutter-bash-commands-pass: PASS/FAIL

### Scoring (세션 품질 점수)

매 세션 종료 시 환경 하네스 점수를 기록:

```
ENV_SCORE = 100 - (fvm_errors * 10) - (defines_errors * 10) - (env_warnings * 5)
```

- fvm_errors: fvm 가드에 차단된 횟수
- defines_errors: dart_defines 가드에 차단된 횟수
- env_warnings: SessionStart에서 발견된 warning 수

목표: ENV_SCORE >= 90 (세션당)

### Known Issues Registry

환경 이슈 발생 시 이 파일에 추가하여 누적 관리:

| 이슈 | OS | 원인 | 해결 | 최초 발견 |
|------|-----|------|------|-----------|
| fvm not found | Windows | Git Bash에서 .bat 확장자 필요 | fvm.bat 사용 | 2026-03-29 |
| .dart_defines.json missing | All | resolve-host.sh 미실행 | bash .vscode/resolve-host.sh | 2026-03-29 |
| observatory port mismatch | All | flutter run이 랜덤 포트 사용 | launch.json에 --observatory-port=8181 고정 | 2026-03-29 |

### Success Metrics
- pass@3 > 95% for capability evals
- ENV_SCORE >= 90 per session
- Known issues: 0 new recurring issues per month
