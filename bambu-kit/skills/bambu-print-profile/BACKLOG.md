# TODO — bambu-print-profile 스킬

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
   ```
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
