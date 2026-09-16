# Amendments — bambu-kit-option-key-registry-probe

계약 본문은 봉인(`sha256:2cae367545296fef`)되어 수정하지 않는다. 아래는 구현·교차 진단 중 발견한 조건
결함과 그 처리다. 방향은 `harness/references/contract-schema.md` §Amendment 사이드카의 계산 함수로 구했다
(재현: 세션 작업 폴더 `amend-dir.sh`).

## AM-01 — relaxing · SC-09 허용 집합에 "등록됐지만 JSON 에서 버리는 옵션" 추가

- 대상 조건: SC-09
- 결함: SC-09 은 명령줄 자르기 결과 3mf 의 `Metadata/project_settings.config` 키가 목록의 `canonical` 또는
  `header` 에 모두 있기를 요구한다. 그런데 3mf 는 **메모리의 설정 전체**를 적으므로, 등록부에는 있지만 옛 이름
  처리 함수가 버리는 옵션도 기본값으로 기록한다. SK-03 이 봉인한 `canonical` 749 는 "JSON 에서 받는 키" 라
  그런 옵션을 뺀다 — 두 조건이 같은 낱말을 다른 뜻으로 쓴다.
- 실측 (2026-09-15): 오르카 3mf 키 641 개 중 목록 밖 1 개 `silent_mode` · 뱀부 578 개 중 0 개.
  오르카 `PrintConfig.cpp:4440` 이 `silent_mode` 를 등록하고 `:8272` 무시 목록이 버린다.
  **목록이 맞다는 실행 확인**: 머신 JSON 에 `silent_mode: "1"` 을 넣어 오르카 명령줄로 잘랐더니 3mf 값이
  기본값 `"0"` 그대로였다 (주입 전 `"0"`). JSON 에서 받는 키로 목록에 넣으면 게이트가 버려지는 키를 통과시킨다.
- 변경: SC-09 허용 집합을 `canonical ∪ header ∪ {등록부에 있으나 옛 이름 처리 함수가 버리는 키}` 로 읽는다.
  이번 측정에서 추가되는 원소는 `silent_mode` 1 개다. 보완 확인으로 "그 키에 기본값과 다른 값을 넣어 잘랐을 때
  3mf 값이 바뀌지 않는다" 를 함께 요구한다 (위 실측이 그 증거).
- direction: `relaxing added=1 removed=0` (`amend_direction`, 허용 집합 입력)
- consent: `anchored` — 사용자가 질문 답으로 승인했다.
- 근거 (redaction 거친 원문): 질문 "① SC-09: 오르카가 결과 파일에 `silent_mode` 를 기본값으로 적는데, 이 키는 JSON 으로
  넣어도 버립니다 … 이 한 키를 허용 목록에 더해 읽습니다. ② AR-05·AR-06·SC-06 … 백업 폴더만 빼고 셉니다." 에 대한 답 "둘 다 승인 (권장)"
- 앵커: 2026-09-15T07:54:33.999Z · session=5d88caf0-e6ef-425e-a688-7cd21beae1d9 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins (세션 대화 기록의 질문 답 · reflect-kit 프롬프트 로그가 아니라 대화 기록 기준)

## AM-02 — relaxing · AR-05 · AR-06 · SC-06 측정에서 백업 폴더를 뺀다

- 대상 조건: AR-05, AR-06, SC-06
- 결함: AR-05 는 "설정 폴더 아래 JSON 중 `"topmost_only"` 를 담은 파일 0 개" 와 "설정 폴더 **안의** 백업 폴더
  `_backup-2026-09-15-ironing-topmost_only/` 에 원본 19 개가 각각 `"topmost_only"` 1 건" 을 동시에 요구한다.
  문자 그대로 재면 두 요구를 함께 만족하는 상태가 없다 (실측: 백업 포함 19 개 · 그 19 개 전부 백업 폴더).
  AR-06 의 zip 도 같다. SC-06 의 "설정 폴더 JSON 154 개" 도 백업 폴더가 생기면 173 개가 된다.
- 변경: 세 조건의 설정 폴더 측정은 `_backup-2026-09-15-ironing-topmost_only/` 아래를 뺀다. 백업 폴더 요구는
  그 폴더만 따로 잰다.
- direction: JSON `relaxing measured_removed=19 measured_added=0` · zip `relaxing measured_removed=15 measured_added=0`
  (`amend_direction_oracle`, 측정 집합 입력)
- consent: `anchored` — 백업 위치를 설정 폴더 안에 두는 문구는 계약 작성자가 적었고(범위 선택은 2026-09-15T07:11:09Z
  질문 답 "topmost_only 19개도 고침"), 이 해석은 AM-01 과 같은 질문에서 사용자가 승인했다.
- 근거 (redaction 거친 원문): AM-01 과 같은 질문 ② 항목에 대한 답 "둘 다 승인 (권장)"
- 앵커: 2026-09-15T07:54:33.999Z · session=5d88caf0-e6ef-425e-a688-7cd21beae1d9 · cwd=/Users/jackson/Hub/10_Dev/claude-plugins
- 측정 결과 (백업 제외 기준): JSON 0 개 · zip 0 개 / 백업 폴더 JSON 19 개(각 1 건) · zip 15 개(항목 17) ·
  고친 19 개 파일 `ironing_type` 외 키·값·순서 동일 · zip 15 개 이름 목록 동일 · 고친 항목 외 CRC 동일 ·
  SC-06 은 백업 제외 163 개에서 두 검사 FAIL 집합 동일(64 = 64).

## AM-03 — narrowing · DG-01 · DG-03 에 새 스크립트 검사를 더한다

- 대상 조건: DG-01, DG-03
- 결함 (교차 진단 지적 1): 두 조건은 `project.yaml` 기본값을 옮겨 이번 스프린트가 건드리지 않는
  `scripts/release.sh` 만 잰다. 새로 만든 빌드 스크립트는 문법 오류가 있어도 통과한다.
- 변경: 원 측정에 더해 `bash -n bambu-kit/scripts/option-key-probe/build-option-list.sh` 경고 0 개와
  `python3 -m py_compile` 로 새 파이썬 2 개(`extract-bundle-ctor.py` · `generate-option-list.py`) 오류 0 개를 요구한다.
  컴파일로 생긴 `__pycache__` 는 레포에 남기지 않는다.
- direction: `narrowing measured_removed=0 measured_added=3` (`amend_direction_oracle`)
- consent: `unanchored` — 제약 강화라 PASS 근거로 쓸 수 있다.
- 측정 결과: `bash -n` 출력 없음 · `py_compile` 오류 0 · `__pycache__` 삭제 확인.

## AM-04 — 측정 절차 명시 (PASS 집합 변화 없음 · PASS 근거로 쓰지 않는다)

교차 진단이 "계약 본문만으로는 절차가 갈릴 수 있다" 고 지적한 항목이다. 조건 문구 그대로 재도 통과하므로
방향 판정 대상이 아니며, 평가자가 같은 절차를 쓰도록 적어 둔다.

| 조건 | 명시 |
| --- | --- |
| SC-09 · SK-03 | `header` 줄 종류의 뜻은 `bambu-kit/scripts/option-key-probe/generate-option-list.py` 머리말: 옵션이 아니라 불러오기가 따로 읽는 파일 머리 키 (`#define *_JSON_KEY_*`). `bambu-fields-baseline.md` §11.1 표에도 있다 |
| SK-05 | 목록은 탭 구분이고 값 안의 공백은 구분자가 아니다. `renamed-value` 줄은 4 칸(`종류 · 키 · 옛 값 · 새 값`) |
| SC-08 | 짝 맞추기는 문자열 · 문자 리터럴 · 주석 안의 괄호를 세지 않는다 (`extract-bundle-ctor.py` 의 `block_from` 과 같은 규칙) |
| SC-07 | 옛 이름 후보를 설치본 번들 프로파일에서 모으므로, 설치본이 오르카 2.4.2 · 뱀부 02.08.02.61 일 때 잰다 (2026-09-15 확인: 두 앱 `CFBundleShortVersionString` 이 그 값) |
| AR-05 · AR-06 | 파일명에 공백이 많아 `xargs` 로 넘기면 0 건으로 깨진다. `find -print0` 또는 파이썬 순회로 잰다 |
| SC-01~SC-06 · ER-01 | 검사 코드는 `SKILL.md` 음성 대조 절의 추출 절차(`grep -n '^TARGET_SLICER=.* python3 - '` ~ `PY`)로 뽑는다. 실행 시 `SKILL_DIR=bambu-kit/skills/bambu-print-profile` 을 넘긴다 |

## 구현 중 발견 — 목록이 못 담는 불러오기 특수 처리 (조건 영향 없음)

기준 문서 `bambu-fields-baseline.md` §11.2a 가 "뱀부 JSON 에 써도 된다" 고 적었던 `reduce_infill_retraction` 은
뱀부 목록에 없다. 뱀부 `Config.cpp` `load_from_json` 이 값 `"0"` 일 때만 `reduce_infill_retraction_mode` 를
`Disabled` 로 옮기고 키 자체는 버린다 (옛 이름 처리 함수 밖의 특수 처리라 목록 생성기가 따라가지 않는다).
같은 함수의 `support_type: hybrid(auto)` → `support_style` · `wall_infill_order` 채움 우선 → `is_infill_first` 도
목록에 없다. 게이트는 첫째를 `모르는 키` 로 막고 나머지 둘은 `옛 값` 으로 알린다. §11.1 · §11.2a · §11.3 에 반영했다.
