"""봉인 전 알려진 답 대조용 — scratch 복제본에 네 규칙을 최소로 넣는다. 인자: 복제본 경로."""
import sys
from pathlib import Path

R = Path(sys.argv[1])
Q = dict(
    RFC="All times expressed have a stated relationship (offset) to Coordinated Universal Time (UTC).",
    ISO="September 27, 2022 at 6 p.m. is represented as 2022-09-27 18:00:00.000.",
    ATL="A product requirements document (PRD) defines the purpose, features, and behavior of a product, aligning stakeholders and guiding development.",
    ADR="An Architectural Decision Record (ADR) captures a single AD and its rationale.",
    NYG="Each record describes a set of forces and a single decision in response to those forces.",
    SA1="We recommend that you avoid using service account keys whenever possible.",
    SA2="Use Workload Identity Federation whenever an application needs to access Google Cloud and has access to ambient credentials.",
    SA3="this way of initializing the SDK is strongly recommended for applications running in Google environments",
    SA4="For client-side applications such as tools, desktop programs, or mobile apps, don't use service accounts.",
)
SHAPE_MD = "벽시계는 `YYYY-MM-DDTHH:mm:ss[.fraction]` 을 `type: string` · `pattern` · `example` 로 명세한다 — 이 킷이 고른 형식이다."
ORDER = "① Google Cloud 안: ADC 와 연결된 서비스 계정 ② GKE: Workload Identity Federation for GKE ③ 혼자 쓰는 개발 환경: 사용자 자격 증명 또는 서비스 계정 가장 ④ Google Cloud 밖 외부 신원 제공자: Workload Identity Federation ⑤ 대안이 없을 때만: 서비스 계정 키"


def edit(path, old, new, count=1):
    p = R / path
    t = p.read_text(encoding="utf-8")
    assert t.count(old) >= 1, (path, old[:40])
    p.write_text(t.replace(old, new, count), encoding="utf-8")


def insert_after_line(path, head, new):
    p = R / path
    lines = p.read_text(encoding="utf-8").split("\n")
    i = next(k for k, l in enumerate(lines) if l.startswith(head))
    lines.insert(i + 1, new)
    p.write_text("\n".join(lines), encoding="utf-8")


def append_to_line(path, head, extra):
    p = R / path
    lines = p.read_text(encoding="utf-8").split("\n")
    i = next(k for k, l in enumerate(lines) if l.startswith(head))
    lines[i] += extra
    p.write_text("\n".join(lines), encoding="utf-8")


append_to_line("backend-kit/skills/backend-system/SKILL.md", "15. **timestamp", " " + SHAPE_MD)
edit("backend-kit/skills/backend-audit/references/audit-criteria.md", "벽시계 필드(반복 일정·영업시간·알림 시각)의 저장은",
     SHAPE_MD + " 벽시계 필드(반복 일정·영업시간·알림 시각)의 저장은")
edit("docs/backend/fundamentals/database.md", "은 `date-time` 이 아니다.\n",
     f"은 `date-time` 이 아니다.\n- {SHAPE_MD} RFC 3339: 「{Q['RFC']}」 ISO: 「{Q['ISO']}」\n")
edit("docs/backend-kit/database.html", "</code> 은 <code>date-time</code> 이 아니다.",
     f"</code> 은 <code>date-time</code> 이 아니다. 벽시계는 <code>YYYY-MM-DDTHH:mm:ss[.fraction]</code> 을 <code>type: string</code> · <code>pattern</code> · <code>example</code> 로 명세한다 — 이 킷이 고른 형식이다. 「{Q['RFC']}」 「{Q['ISO']}」")
insert_after_line("planning-kit/skills/plan-prd/SKILL.md", "14. **",
                  "15. **PRD 와 ADR 경계** — 제품 비범위는 PRD 에, 구조 결정은 ADR 에. 원문에 직접 근거가 없는 추론이다. `docs/planning/prd-patterns.md`")
edit("docs/planning/prd-patterns.md", "## 참고 링크 (전체)",
     f"### PRD 와 설계 결정 기록(ADR)의 경계\n\n「{Q['ATL']}」 「{Q['ADR']}」 「{Q['NYG']}」 원문에 직접 근거가 없는 추론이다.\n\n## 참고 링크 (전체)")
edit("docs/planning-kit/prd-patterns.html", "<!-- 03 다섯 블록 -->",
     f"<section><p>「{Q['ATL']}」 「{Q['ADR']}」 「{Q['NYG']}」 원문에 직접 근거가 없는 추론이다.</p></section>\n  <!-- 03 다섯 블록 -->")
S = "onboarding-kit/skills/setup-guide/SKILL.md"
insert_after_line(S, "\"그 시점 최신 정보 기준\"",
                  "\n조회일과 원문의 Last updated 를 따로 적는다. 갱신일만 보고 본문을 다시 확인하지 않았으면 조회일을 바꾸지 않는다. 이 킷의 규칙이다.")
edit(S, "## Process\n",
     f"### Gotcha 10: 서비스 계정 선택 순서\n\n{ORDER}. 「{Q['SA1']}」 「{Q['SA2']}」 「{Q['SA3']}」 「{Q['SA4']}」 (조회 2026-09-28 · Last updated 2026-09-24 UTC)\n\n## Process\n")
edit("onboarding-kit/skills/setup-guide/references/format-checklist.md", "— 조회 YYYY-MM-DD>",
     "— 조회 YYYY-MM-DD · Last updated YYYY-MM-DD UTC>")
H = "docs/onboarding-kit/setup-guide.html"
edit(H, "반복 실패를 막는 9개 체크다.", "반복 실패를 막는 10개 체크다.")
edit(H, "재검증 명령)을 적는다.</div></li>\n    </ul>",
     f"재검증 명령)을 적는다.</div></li>\n      <li><span class=\"check\">10</span><div>{ORDER}. 「{Q['SA1']}」</div></li>\n    </ul>")
edit(H, "<h3>ENV 마커를 인정받는 네 가지 근거</h3>",
     "<p>조회일과 원문의 Last updated 를 따로 적는다. 본문을 다시 확인하지 않았으면 조회일을 바꾸지 않는다. 이 킷의 규칙이다.</p>\n    <h3>ENV 마커를 인정받는 네 가지 근거</h3>")
edit(H, "<li><span class=\"check\">✓</span><div>막는 요구마다",
     "<li><span class=\"check\">✓</span><div>서비스 계정 키는 맨 끝, 출처마다 조회일과 Last updated 를 따로 적었다.</div></li>\n      <li><span class=\"check\">✓</span><div>막는 요구마다")
edit("docs/onboarding-kit/format-checklist.html", "— 조회 YYYY-MM-DD&gt;", "— 조회 YYYY-MM-DD · Last updated YYYY-MM-DD UTC&gt;")
print("applied")
