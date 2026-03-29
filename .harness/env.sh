# ── 하네스 환경 변수 템플릿 ──
# 프로젝트의 .harness/env.sh에 복사하여 수정한다.
# env hooks 스크립트들이 source하여 사용한다.

# ── SDK 래퍼 명령 ──
# SDK 래퍼를 사용하지 않으면 비워둔다.
SDK_CMD_NAME=""           # 예: "fvm", "nvm", "rbenv"
SDK_CMD_WINDOWS=""        # Windows용 명령 예: "fvm.bat"
SDK_CMD_UNIX=""           # macOS/Linux용 명령 예: "fvm"
SDK_GUARD_MSG=""          # 차단 시 표시할 메시지

# ── 필수 파일 ──
# 배열 인덱스를 맞춰야 한다 (FILES[0] ↔ MSG[0] ↔ RESOLVE[0])
REQUIRED_FILES=()         # 예: (".env" ".dart_defines.json")
REQUIRED_FILES_MSG=()     # 예: (".env 파일이 필요합니다" ".dart_defines.json이 없습니다")
REQUIRED_FILES_RESOLVE=() # 예: ("cp .env.example .env" "bash scripts/setup.sh")

# ── 필수 CLI 명령 ──
REQUIRED_COMMANDS=()      # 예: ("cargo" "docker")

# ── Run 가드 ──
# 형식: "명령패턴|필수플래그|필수파일|경고메시지"
# 특정 명령 실행 시 필수 조건 체크. 비어두면 가드 없음.
RUN_GUARDS=()
# 예: ("flutter run|dart-define-from-file|.dart_defines.json|환경 변수 누락")

# ── 외부 도구 (선택) ──
EXTERNAL_TOOLS_NAME=()              # 예: ("adb" "docker")
EXTERNAL_TOOLS_WINDOWS_FALLBACK=()  # 예: ("\$LOCALAPPDATA/Android/Sdk/...")
EXTERNAL_TOOLS_OPTIONAL=()          # 예: (true false)
