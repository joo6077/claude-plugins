# Codex supervisor 계약 측정 묶음

구현이 아니라 계약의 판정 도구다. 스크립트-11의 일반 실행만 실제 모델을 호출하며 비용이 발생한다. `--prepare-only`는 실제 Codex CLI의 로그인 상태만 확인하며 모델 호출은 0회다. 정상 경로는 좋은 예 1차례와 나쁜 예 최초·재심 2차례로 총 3차례다. 레포 W는 git 조회·archive로 읽고, 임시 사본과 Git 저장소는 이 폴더의 `.runs/` 아래에 만든다. 진짜 codex 실행 파일이나 바로가기를 변경하지 않는다.

## 실행

이 폴더를 W의 `.harness/.meta/codex-supervisor/measure/`로 옮긴 뒤 W에서 실행한다.

```bash
bash .harness/.meta/codex-supervisor/measure/measure.sh 스크립트-03
bash .harness/.meta/codex-supervisor/measure/measure.sh 스크립트-03 --controls-only
bash .harness/.meta/codex-supervisor/measure/measure.sh 스크립트-03 --negative
```

일반 실행의 PASS/FAIL과 종료 0/1이 구현 판정이다. 스크립트-11의 로그인 전제 불성립은 `PRECONDITION_UNMET`·종료 2·`implementation_evaluated=false`로 구분한다. `--prepare-only`의 PASS는 준비 성공이며 구현 판정이 아니다. `--controls-only`의 PASS는 양성 대조·알려진 답의 성공이며 구현 성공이 아니다. `--negative`는 사본의 실행 명령을 무력화하며 정상 기대값은 FAIL/1이다. 구문·문서·V1/V6 조건은 해당 입력을 파괴한다. 잘못된 조건 번호는 FAIL/64다.

상한은 `feat/codex-supervisor`, 기준은 `88b2a84e`다. 미커밋 구현은 평가하지 않는다. W에서 실행하지 않는 경우 `MEASURE_W`로 W를 지정할 수 있다. 기본 W 경로는 최초 요구사항의 경로다.

필요 도구: Python 3.11 이상, PyYAML(레포 검증기의 의존성), git, tar, bash, zsh, shellcheck. 새 패키지를 설치하지 않는다. 스크립트-11 외에는 네트워크를 쓰지 않는다. 도구 부재는 FAIL이다.

## 파일

- `measure.sh`: bash·zsh 공용 진입점.
- `measure.py`: 27개 조건 디스패치, 임시 저장소, 관측과 대조.
- `fake-codex`, `fake_codex.py`: CODEX_BIN 전용 가짜 실행 파일과 구현. thread 사건과 세션 기록도 만든다.
- `prompt_checks.py`: 구조-02의 역할 부여·8192바이트·풀이 예시 제한과 변이 대조.
- `auth_support.py`: 권한 600 인증 사본 생성·정리와 키 잔여 검사.
- `live_calibration.py`: 스크립트-11의 실제 좋은/나쁜 예·세션 기록 대조.
- `fixtures.py`: 손으로 답을 셀 수 있는 계약·판정·스키마 표본.
- `check-contract.sh`: 규약의 헤더·조건 배치·조건 수 명령.
- `verify.py`: 언어별 소스 문법, 계약 형식, 명시된 23개 대조와 구현 전 12개 FAIL 재현 및 비용 없는 로그인 준비 확인.
- `frontmatter-check.txt`: frontmatter 수정 전후 조건 줄 지문.
- `control-results.md`: 계약 기대값과 실측값 표.
- `verification/`: 원문 검증 출력·요약·가짜 Codex smoke 결과.
- `.runs/`: 재실행할 수 있는 임시 시험 데이터와 관측 로그. 의도적으로 깨진 셸·계약·JSON 입력을 포함한다. 측정기 소스 문법 검사의 대상이 아니다.

검증 명령은 다음과 같다.

```bash
python3 -B out/measure/verify.py
bash out/measure/check-contract.sh out/sprint-contract-codex-supervisor.md
```

첫 명령은 구현 전 초안 QA용이다. 구현 후에는 12개 조건의 FAIL을 더 이상 기대하면 안 되므로 각 조건의 일반 실행을 사용한다. `.runs/`의 원본 커밋 `source/` 사본은 다시 생성할 수 있어 배포에 포함할 필요가 없다. `evidence.json`, `verification/`의 원문 출력과 source_ref는 보존한다. `__pycache__/`도 배포에 필요 없다.

스크립트-11은 기본 감독 설정 폴더의 file 로그인·auth.json 권한 600을 확인하고 auth.json·config.toml을 측정 폴더 아래 권한 700의 쓰기 가능한 임시 폴더로 복사한다. 인증 사본은 생성부터 600이다. 원본과 사본에서 login status가 성공해야 진행하며 임시 프로젝트의 codex_audit.codex_home과 CODEX_HOME을 사본으로 지정한다. 설정의 model·effort는 유지한다. 세션은 실행 폴더에 보존하고 인증 사본만 정상·실패·시간 초과·SIGINT/SIGTERM 뒤 삭제한다. 원래 설정·인증·세션 폴더는 읽기만 한다. 로그에는 키를 쓰지 않는다. 실제 호출 측정에서 기본 설치의 실제 경로와 다른 CODEX_BIN·custom provider/endpoint는 거부한다. 중첩 실행에서 기본 Codex 경로가 상속된 경우는 허용한다. SIGKILL·전원 단절의 즉시 정리는 보장할 수 없으며 계약 범위 경계에 명시했다.

구조-02의 `--negative`는 역할 부여·길이·예시 수를 각각 변조한 템플릿 사본을 같은 검사에 넣는다. 구현 전에도 MISSING과 무관하게 세 위반을 검출해야 한다. 스크립트-11의 `--negative`는 가짜 CODEX_BIN을 거부하며 비용이 없다. verify.py는 MEASURE_NO_LIVE=1로 모델 호출을 차단한다. 원본·사본에서 비용 없는 login status만 실행하며, 이번 파일 인증 전제 검증은 READY를 요구한다. UNMET은 구현 FAIL과 별도로 남긴다. 구현 뒤 스크립트-11을 직접 일반 실행해야 실제 판정을 받을 수 있다.

반복 2회차 보완: 스크립트-10은 draft·revise·impl·조사 네 종류의 실제 가짜 호출 6개에서 스키마를 검사한다. 오류-01은 impl 17개와 다른 세 호출의 형식 오류 9개를 검사한다. 9개 추가 오류 표본은 `--controls-only`에서도 가짜 실행 파일로 생성해 검출한다.

```bash
bash out/measure/measure.sh 스크립트-11 --prepare-only
```

준비 결과 원문은 `verification/스크립트-11-preparation.txt`에 있다. 2026-10-06 이 격리 환경에서 원본·사본 모두 Logged in using an API key를 확인했다. 실제 모델 판정은 사용자 지시대로 실행하지 않았다.

반복 3회차: 판정 인터넷을 허용하되 조사 질문·별도 차례는 유지한다. 구조-04는 인증 파일 읽기·복사 권한·다섯 종료 경로의 잔여 키 부재를 잰다. 스크립트-08도 스크립트·감독 산출물·피드백·얼린 입력·임시 잔여물의 키 검사를 수행한다. 삭제에는 Python unlink/shutil을 쓰며 verify.py는 측정 소스에 자동 승인 검사가 거부하는 강제 삭제 셸 명령이 없는지와 검사기 양성 대조를 확인한다.
