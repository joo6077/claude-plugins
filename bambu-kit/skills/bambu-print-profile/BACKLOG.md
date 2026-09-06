# TODO — bambu-print-profile 스킬

## ✅ 구현 완료 (v0.3.0, 2026-05-19) — 첨부 자료 통합 분석 워크플로우

> 출처: dogfood 피드백 2026-05-19 (Stealth Press 1S 케이스). 사용자 피드백:
> "키트에 이런거 처럼 구매 필요한 리스트나 링크 주는것도 있었으면 좋겠는데 그리고 너 지금 웹만보는데 웹안에 있는 파일 pdf? 기타 등등도 분석했으면 하는데 주의사항이나 필요한 리스트 조립, 필라멘트 기타등등 요구사항을 숙지해야지"

### 해결한 문제

v0.2.x SKILL Phase 1은 MakerWorld 웹페이지 텍스트/스크린샷만 읽음 → 다음 정보 누락:

- 공식 PDF assembly manual의 정확한 BOM, 숨은 부품, 안전 주의사항
- YouTube 빌드 영상의 손기술 팁
- GitHub 레포의 변경 이력 (R1 vs R1S 같은 리비전 차이)

Stealth Press 1S 케이스에서 v0.2.x로는 놓쳤을 항목:
1. Heat-set 인서트 VORON 표준 M3x5x4 명시
2. 숨은 인서트 5군데 ("Insert on other side!" 표시)
3. 희생 부품 break out + 부싱 super glue 3방울
4. 0.5-1mm shim, 인두 타입별 mount STL 선택, 인서트 압입 온도
5. 인서트 실제 수량 34개 (웹 BOM 30개와 mismatch)

### v0.3.0에서 추가된 워크플로우 단계

- **Phase 1 Attached Resources Inventory** — 페이지 외부 링크를 4개 카테고리로 enumerate
- **Phase 1.5 신규 — PDF/YouTube/GitHub 분석** — 첨부 자료 자동 분석 + cross-check 보고
- **Phase 4 notes.md 5섹션 표준화** — 필라멘트/부품/조립/임포트/라이센스
- **매 실행 시 필수 사전 절차** — Bambu Studio 버전 + memory + 시스템 base 프리셋 cross-check
- **Phase 5 Coupon test 자동 생성** — 트리거 조건 충족 시 zip 번들에 lean process JSON 자동 포함

reference notes.md: `/Users/jackson/Hub/60_3D Print/Settings/stealth-press-1s/notes.md`

---

## v2 — 홈서버 자동 print outcome capture daemon

**목표:** H2S print 결과를 홈서버에서 자동 수집 → JSONL 로그 → 카이젠 스킬이 주 1회 읽어 references default 값 보정.

### 환경
- **호스트:** 홈서버 (macOS 아님, Linux 가정)
- **프린터:** Bambu Lab H2S
- **네트워크:** 동일 LAN

### 셋업 (예상)

1. Python 가상환경 + 의존성:
   ```bash
   python3 -m venv ~/.bambu-log-venv
   ~/.bambu-log-venv/bin/pip install bambulabs-api paho-mqtt
   ```

2. 입력 정보 (홈서버 환경변수 또는 config 파일):
   - `BAMBU_PRINTER_IP` (LAN 고정 권장)
   - `BAMBU_LAN_ACCESS_CODE` (Studio Settings에서 확인)
   - `BAMBU_SERIAL` (프린터 serial number)
   - `LOG_PATH` (예: `~/BambuLogs/prints.jsonl`)
   - `MEDIA_PATH` (예: `~/BambuLogs/media/`)

3. Daemon 스크립트 (`bambu_print_logger.py`):
   - MQTT TLS port 8883 connect, username `bblp`, password = LAN access code
   - `device/<serial>/report` subscribe
   - `gcode_state` 전환 감지 (`RUNNING` → `FINISH`/`FAILED`/`CANCELLED`)
   - 완료 시 JSONL 1줄 append: actual_time, success/fail, hms[], print_error, AMS, .gcode.3mf 헤더 파싱 (FTPS port 990으로 받음)
   - timelapse는 별도 downloader cron 또는 daemon 종료 시 snapshot

4. systemd 서비스 (홈서버 Linux):
   ```ini
   ~/.config/systemd/user/bambu-print-log.service
   [Unit]
   Description=Bambu Print Outcome Logger
   After=network-online.target

   [Service]
   ExecStart=/home/<user>/.bambu-log-venv/bin/python /home/<user>/bin/bambu_print_logger.py
   Restart=on-failure
   RestartSec=10s

   [Install]
   WantedBy=default.target
   ```
   `systemctl --user enable --now bambu-print-log` (또는 system-level service로 olarak)

5. **USB 스틱 필수** (H2S timelapse/recording은 USB 없으면 안 켜짐):
   - FAT32 또는 exFAT
   - write speed 10MB/s+
   - 프린터에 상시 꽂아둠

### 카이젠 통합

- `bambu-print-profile-kaizen` 스킬이 주 1회 다음 작업:
  - SFTP/SSH 또는 syncthing/rsync로 홈서버의 `prints.jsonl` 가져옴 (또는 클라이언트가 직접 mount)
  - 최근 1주 record에서:
    - 실패율 (성공/전체)
    - HMS error 빈도
    - 실제 시간 vs estimated 시간 편차
    - 소재별 평균 print time
    - seam/scarf 관련 user feedback (별도 채널)
  - references default 값 자동 보정 제안 (사용자 승인 후 commit)

### 알려진 caveat

- `bambulabs-api` PyPI 설명: "H2D printers have not been tested yet" — H2S/H2 계열 직접 검증 필요
- `gcode_state` 전환 edge case: cancel 후 `FAILED` 잔류 등 펌웨어별 차이
- LAN access code는 보안 정보 — git에 commit 금지, 홈서버 env로만

### 대안 검토 후보

- **Bambuddy** (https://github.com/maziggy/bambuddy): self-hosted, 이미 print log/archive/CSV export 다 있음. v1 대신 Bambuddy 깔고 그 DB/CSV를 카이젠 input으로 쓰는 게 더 가벼울 수도 있음. v2 착수 시 둘 다 PoC 비교 권장.

### 출처

- Codex research run: `a207bd8531800c43c` (2026-05-15)
- 로그 파일: `~/.claude/codex-research-log/2026-05.md` (2026-05-15T... — TODO: 이 entry는 로그에 아직 안 적힘, v2 시작 시 추가)

### 우선순위

**낮음** — 박스 오프너 + 추가 모델 몇 개로 SKILL.md v1 충분히 검증 후 진행. 손으로 feedback 채우는 방식이라도 카이젠 동작은 가능.

## Surface-first 후속 검증 (2026-05-16 v2)

> 출처: Codex run `a25261e23b21252b2` 의 open questions. surface-first 정책 풀 적용 후 실측/문서 보강 필요 항목.

### (a) precise z-seam JSON 키 매핑

Bambu Studio 2.6+ UI에 "precise z-seam" 또는 동등 옵션이 보이는지, 그리고 해당 옵션이 어느 JSON 키에 매핑되는지 확인 필요. 현재 로컬 baseline에는 명시 필드 없음 — 2.6+에서 변경/제거되었거나 다른 키로 흡수되었을 가능성.

검증 방법:
1. Bambu Studio UI에서 Process → Seam 탭 옵션 enumerate
2. Studio에서 dummy preset 만든 후 "Edit in Place" → JSON export하여 키 추출
3. GitHub `src/libslic3r/PrintConfig.cpp` grep으로 `z_seam|precise_z` 키 검색
4. 발견 시 `references/bambu-fields-baseline.md` §3 (Seam/Scarf) 또는 §8.4 (Spiral / Seam Placement)에 추가

### (b) seam_slope_steps / seam_slope_entire_loop / seam_slope_inner_walls 누락 default 재확인

`references/bambu-fields-baseline.md` §8.5에 enumerate되어 있으나 로컬 `fdm_process_common.json`에 default 값 누락. 다음 중 어느 단계에서 default가 결정되는지 확인 필요:

1. PrintConfig.cpp 코드 default
2. fdm_process_single_common.json 또는 fdm_process_single_0.20.json 부모 단계
3. Bambu 시스템 정적 default (UI 보여주기 전 단계)

검증 방법:
- `grep -rn "seam_slope_steps\|seam_slope_entire_loop\|seam_slope_inner_walls" ~/Library/Application\ Support/BambuStudio/system/BBL/process/`
- 미발견 시 BambuStudio 소스 `src/libslic3r/PrintConfig.cpp` 직접 확인

### (c) Coupon 부족 소재 실측 — PLA Matte / PLA Silk / PC / ASA / PAHT-CF / TPU 중 최소 3종

기존 실측 사례 (`SKILL.md` Phase 5 + `seam-recipes.md` Real-world findings):
- ✅ PETG HF (vent pipe 회전체)
- ✅ PLA Basic (박스 오프너 dual-color)
- ✅ TPU 90A (sealing ring — scarf off 검증)

surface-first 정책 적용 후 coupon 검증이 필요한 소재 (`surface-recipes.md` §3·§5·§7 권장값 검증):
- **PLA Matte** — layer line 은폐 최강 가설 검증, ironing 과다 시 chalky 변색 가설
- **PLA Silk** — top ironing 광택 불일치 가설 (옆면과 매트 차이)
- **PC** — chamber 60°C + outer 20-30mm/s + topmost 소형 ironing 실험
- **ASA** — enclosure + brim + vapor smoothing 후가공 비교
- **PAHT-CF** — hardened nozzle + fiber 질감 한계 정량화
- **TPU** — surface-first 모드에서 ironing/scarf off의 표면 한계 측정

각 coupon은 30×30×35mm 회전체 + 평면 top 박스 2종 출력 후 `surface-recipes.md`에 Finding 추가.

### (d) PETG HF lot / 습도 의존성 비교 coupon

PETG HF는 lot별 흡습 + 습도 환경 의존성이 큼. 같은 surface-first preset으로 다음 3 조건 비교 출력:

1. 신품 봉인 PETG HF + AMS HT 65°C 8h 사전 건조 + continuous drying ON
2. 신품 봉인 PETG HF + AMS HT 사전 건조 X + continuous drying ON
3. 같은 lot의 1주일 개봉 노출 PETG HF + AMS HT 사전 건조 + continuous drying ON

평가 지표: stringing 개수 / blob 빈도 / outer wall 광택 균일도 / entire_loop scarf 흔적 노출 정도.

결과를 `surface-recipes.md` §6.5 (속도 무시 부작용) 또는 새 Finding으로 환류.

### 우선순위

**중간** — surface-first 정책이 default ON 가능하려면 (a)~(b) 문서 갭은 1-2주 내 보강 권장. (c)/(d) 실측은 3-6 모델 출력 후 점진 환류.
