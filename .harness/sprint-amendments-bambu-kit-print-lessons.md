# sprint-amendments — bambu-kit-print-lessons

계약 본문은 봉인됐다(`sha256:47696418d0328fc4`). 조건 줄을 고치지 않고 여기에 덧붙인다.

## AM-01 — unknown (입력 파일 경로 교체)

- 대상 조건: 공통 전제의 "제작자 원본" — 이를 쓰는 SK-01 · SK-02 · SK-03 · SK-06
- 변경: `~/Downloads/H2_simple_AMS_Flipper--ABS(3).3mf` → 고정 사본
  `/private/tmp/claude-501/-Users-jackson-Hub-10-Dev-claude-plugins/be3037df-1ee8-45db-aa79-f54d3cadb2fc/scratchpad/lessons/creator-original-abs.3mf`
  (원본 위치 `~/Downloads/꽃톡/H2_simple_AMS_Flipper--ABS.3mf`, sha256 앞 16 자리 `8eeeecc00af3fdc0`)
- 왜: 봉인 직후 사용자가 다운로드 폴더를 정리해 `(2)` · `(3)` 사본이 사라졌다. 같은 날 08:05 에 받은 제작자 원본이 하위 폴더에
  남아 있다. 동일성 근거 — 계약이 원본을 식별한 바이트 수 8,008,196 이 같고, 받은 시각 08:05:14, build item 10 개의 변환 행렬과
  두 번째 `axis_insert`(objectid 18) 의 `printable="0"` 이 이 세션 첫 분석 출력과 전부 같다.
- 방향 계산 (`amend_direction_oracle`, 측정 대상 식별자 = 바이트 수): `unknown measured_removed=0 measured_added=0`
- 규칙상 `unknown` 은 PASS 근거가 아니다 — 아래 AM-03 사용자 확인으로 넘긴다.

## AM-02 — relaxing (SK-02 뒤쪽 브래킷 기대 범위)

- 대상 조건: SK-02 의 `rear_bracket` 기대 범위
- 변경: `53.8~63.8 %` → `67.0~77.0 %` (다른 두 부품 범위는 그대로)
- 왜: 봉인 전 독립 측정(`webwidth.py`)이 **점 수** 로 비율을 셌다. 메시 선분마다 점을 최소 1 개 찍어서, 선분이 잘게 쪼개진
  곡선 구간이 부풀었다. 같은 독립 스크립트를 둘레 **길이** 가중으로만 바꿔 다시 재면(`lenw/webwidth.py`, 구현과 별개)
  `rear_bracket` 72.0 % · 71.9 %, `80angle_bracket` 71.9 % · 72.1 %, `AMS2_bracket` 0 % 다. 새 범위는 72.0 ± 5 %p 다.
  계약 문구 "부족 비율" 의 뜻은 둘레 비율이라 길이 가중이 맞는 측정이다. `80angle_bracket` 범위(69.5~79.5)는 두 방식 값이 모두
  들어가 바꾸지 않는다.
- 방향 계산 (`amend_direction`, 허용 집합을 0.1 %p 단위로 나열): `relaxing added=101 removed=101`
- 규칙상 `relaxing` 은 사용자 동의(`anchored`)가 있어야 PASS 근거가 된다 — 아래 AM-03.

## AM-03 — 승인 기록

- 대상: AM-01 · AM-02 의 consent 축
- 질문: 「봉인된 bambu-kit 계약의 두 가지 수정을 승인할까요? ① 사라진 제작자 원본 (3) 대신 「꽃톡」 폴더의 같은 원본 사본으로 검사.
  ② 뒤쪽 브래킷 벽 폭 부족 비율의 기대 범위를 53.8~63.8% → 67~77% 로 (점 수 기준값이 곡선에서 부풀었고 길이로 재면 72%).」
- 사용자 응답 (원문): **「둘 다 승인」**
- consent: `anchored` — session=be3037df-1ee8-45db-aa79-f54d3cadb2fc · cwd=/Users/jackson/Hub/10_Dev/claude-plugins ·
  2026-09-19 세션 내 선택지 응답
