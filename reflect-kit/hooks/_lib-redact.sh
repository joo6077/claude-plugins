#!/usr/bin/env bash
# 민감 패턴 redaction 헬퍼.
# 사용: redacted=$(redact_sensitive "$raw_text")
# 시크릿 prefix, JWT, env 대입, private key 블록, Bearer 토큰을 [REDACTED-*]로 치환.
# macOS/GNU sed 모두에서 동작하는 ERE만 사용.

redact_sensitive() {
  local input="$1"
  [ -z "$input" ] && { printf ''; return 0; }

  # 1) private key 블록을 먼저 awk로 축약 (멀티라인)
  printf '%s' "$input" | awk '
    /-----BEGIN[[:space:]]+[A-Z ]*PRIVATE KEY-----/ {
      in_key=1
      print "[REDACTED-PRIVATE-KEY-BLOCK]"
      next
    }
    /-----END[[:space:]]+[A-Z ]*PRIVATE KEY-----/ { in_key=0; next }
    in_key==1 { next }
    { print }
  ' | sed -E \
    -e 's/sk-ant-[A-Za-z0-9_-]{10,}/[REDACTED-ANTHROPIC-KEY]/g' \
    -e 's/sk-proj-[A-Za-z0-9_-]{10,}/[REDACTED-OPENAI-KEY]/g' \
    -e 's/sk-[A-Za-z0-9]{20,}/[REDACTED-API-KEY]/g' \
    -e 's/github_pat_[A-Za-z0-9_]{20,}/[REDACTED-GH-PAT]/g' \
    -e 's/ghp_[A-Za-z0-9]{20,}/[REDACTED-GH-TOKEN]/g' \
    -e 's/gho_[A-Za-z0-9]{20,}/[REDACTED-GH-OAUTH]/g' \
    -e 's/ghu_[A-Za-z0-9]{20,}/[REDACTED-GH-USER]/g' \
    -e 's/ghs_[A-Za-z0-9]{20,}/[REDACTED-GH-SERVER]/g' \
    -e 's/ghr_[A-Za-z0-9]{20,}/[REDACTED-GH-REFRESH]/g' \
    -e 's/xox[abprs]-[A-Za-z0-9-]{10,}/[REDACTED-SLACK]/g' \
    -e 's/AKIA[0-9A-Z]{16}/[REDACTED-AWS-ACCESS-KEY]/g' \
    -e 's/AIza[A-Za-z0-9_-]{30,}/[REDACTED-GOOGLE-KEY]/g' \
    -e 's/eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_.+-]+/[REDACTED-JWT]/g' \
    -e 's/([Bb]earer[[:space:]]+)[A-Za-z0-9._~+/=-]{20,}/\1[REDACTED]/g' \
    -e 's/([A-Z_]*(API|AUTH|ACCESS|PRIVATE|SECRET|TOKEN|KEY|PASSWORD|PASS|PWD)[A-Z_]*[[:space:]]*[=:][[:space:]]*)["'"'"']?[A-Za-z0-9+/=_.~-]{8,}["'"'"']?/\1[REDACTED]/g' \
    -e 's/("[A-Z_]*(API|AUTH|ACCESS|PRIVATE|SECRET|TOKEN|KEY|PASSWORD|PASS|PWD)[A-Z_]*"[[:space:]]*:[[:space:]]*")[^"]{4,}"/\1[REDACTED]"/g'
}
