"""rest 묶음이 새로 만든 reflect-kit 쪽 둘. fs2 변환기 gen.py 의 render 를 그대로 불러 쓴다.

`python3 new-pages.py` — 레포 맨 위 폴더에서 부른다.
"""
import importlib.util
from pathlib import Path

TOOLS = Path(".harness/.meta/after-0929-final-sweep-docs/tools")
spec = importlib.util.spec_from_file_location("gen", TOOLS / "gen.py")
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

REFLECT = dict(ACCENT="#F43F5E", ACCENT2="#FDA4AF", ACCENT_RGB="244,63,94",
               L_ACCENT="#BE123C", L_ACCENT2="#9F1239", L_ACCENT_RGB="190,18,60")

GROUNDING_TABLE = """<section class="section" aria-labelledby="decide">
  <div class="section-label" id="decide">판정 한눈에 — 두 신호의 조합</div>
  <div class="table-wrap">
    <table>
      <thead>
        <tr><th>인간 신호</th><th>기계 신호</th><th>값</th><th>소비면에서</th></tr>
      </thead>
      <tbody>
        <tr>
          <td>있음</td>
          <td>있음</td>
          <td><code>mixed</code></td>
          <td>우선 주입</td>
        </tr>
        <tr>
          <td>있음</td>
          <td>없음</td>
          <td><code>user_correction</code></td>
          <td>우선 주입</td>
        </tr>
        <tr>
          <td>없음</td>
          <td>있음</td>
          <td><code>execution_evidence</code></td>
          <td>우선 주입</td>
        </tr>
        <tr>
          <td>없음</td>
          <td>없음</td>
          <td><code>self_inference</code></td>
          <td>제외하거나 명시 라벨 — 계약 PASS 근거로 쓰지 않는다</td>
        </tr>
        <tr>
          <td colspan="2">필드 없음</td>
          <td>미태깅</td>
          <td><code>self_inference</code> 와 다르다 — 4 값 밖 값은 집계에서 빼고 뺀 건수를 보고한다</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>"""

KAIZEN_TABLE = """<section class="section" aria-labelledby="verdicts">
  <div class="section-label" id="verdicts">post_freq 판정 한눈에</div>
  <div class="table-wrap">
    <table>
      <thead>
        <tr><th>조건</th><th>verdict</th><th>다음 행동</th></tr>
      </thead>
      <tbody>
        <tr>
          <td><code>post_freq == 0 AND risk_class == low</code></td>
          <td><code>demote-candidate</code></td>
          <td><code>/reflect-promote action=rollback</code> — 단 §0 이 low 면 <code>blocked-low-confidence</code></td>
        </tr>
        <tr>
          <td><code>post_freq &gt;= initial_freq</code> · 게이트(hook · CLAUDE.md)에 있음</td>
          <td><code>hook-coverage-audit</code></td>
          <td><code>/reflect-promote</code> §B-0 9 항 점검</td>
        </tr>
        <tr>
          <td><code>post_freq == 1</code></td>
          <td><code>prompt-revision</code></td>
          <td>문구 명확화 — 등급은 그대로</td>
        </tr>
        <tr>
          <td><code>post_freq &gt;= 2</code></td>
          <td><code>enforcement-escalation</code></td>
          <td>E2 · E3 로 등급 상향 — <code>/reflect-promote</code> §B</td>
        </tr>
        <tr>
          <td><code>post_freq &lt; initial_freq AND post_freq &lt;= 1</code></td>
          <td><code>keep</code></td>
          <td>효과 있음, 유지</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>"""

def neighbors(cards):
    out = ['<section class="section" aria-labelledby="rel-r">',
           '  <div class="section-label" id="rel-r">같은 킷의 이웃 문서</div>',
           '  <div class="glance">']
    for href, name, text in cards:
        out += ['    <div class="card glance-card">',
                '      <h3><a href="%s">%s</a></h3>' % (href, name),
                '      <p>%s</p>' % text,
                '    </div>']
    return '\n'.join(out + ['  </div>', '</section>'])


GROUNDING_NEAR = neighbors([
    ("reflect-promote.html", "/reflect-promote", "승격 파이프라인 — 규칙을 반영할 자리를 고르고 기록 파일에 남긴다."),
    ("reflect-digest.html", "/reflect-digest", "집계 파이프라인 — 반복 실수를 모아 승격 후보를 낸다."),
    ("schema.html", "기록 틀", "reflections · 승격 기록의 필드 정의."),
])

KAIZEN_NEAR = neighbors([
    ("reflect-promote.html", "/reflect-promote", "되돌리기 · 등급 상향을 실제로 수행한다. 이 스킬은 후보만 낸다."),
    ("tag-canonicalization.html", "태그 정규화", "파편화 지표와 canonical · alias · family 규약의 정의처."),
    ("design.html", "설계", "Precedence Table 과 임계값 hypothesis 원본."),
])

PAGES = [
    dict(
        src="reflect-kit/references/memory-grounding.md", out="docs/reflect-kit/memory-grounding.html",
        css=REFLECT, base="ca1f5f4a",
        kit="Reflect Kit", eyebrow="Reflect Kit · 참고 문서", title="memory grounding",
        subtitle="메모리의 <code>feedback</code> 엔트리를 <strong>누가 썼느냐가 아니라 무엇이 그 교훈을 뒷받침하느냐</strong>로 가르는 "
                 "<code>grounding</code> 4 값의 유일한 정의처다. 아무도 확인하지 않은 자기추론이 영속 규칙으로 굳는 것을 막는다.",
        badges=["원본 <code>reflect-kit/references/memory-grounding.md</code>", "값 넷", "경계 사례 여섯"],
        cards=[
            ("<code>user_correction</code>", "외부 인간 신호 — 사용자의 교정 · 지시 · 불만 발화가 근거다."),
            ("<code>execution_evidence</code>", "외부 기계 신호 — QA verdict · 명령 출력 · 로그 · 실측 수치가 근거다."),
            ("<code>mixed</code>", "인간 신호와 기계 신호가 둘 다 근거로 적혀 있다."),
            ("<code>self_inference</code>", "외부 검증 없음 — 결함 라벨이 아니라 오염 후보 표시다. 소비면이 가중치를 낮춘다."),
        ],
        extra=GROUNDING_TABLE + '\n\n' + GROUNDING_NEAR,
    ),
    dict(
        src="reflect-kit/skills/reflect-kaizen/SKILL.md", out="docs/reflect-kit/reflect-kaizen.html",
        css=REFLECT, base="3ac3f737",
        kit="Reflect Kit", eyebrow="Reflect Kit · 스킬", title="/reflect-kaizen",
        subtitle="reflect-kit 파이프라인 자체를 <strong>월 1 회 측정 · 보정</strong>한다. 다른 모델로 재분류해 일치도를 재고, "
                 "승격 규칙의 30 일 뒤 재발 수(<code>post_freq</code>)로 효과를 판정하고, 승격 임계값을 재발률로 다시 맞춘다.",
        badges=["원본 <code>reflect-kit/skills/reflect-kaizen/SKILL.md</code>", "Gotcha 열둘", "리포트 절 여섯"],
        cards=[
            ("§0 파편화 게이트", "<code>singleton_share &gt; 0.70</code> 이거나 selftest · 수집이 멈추면 <code>calibration_confidence: low</code> — 되돌리기 후보를 낼 수 없다."),
            ("LLM-as-judge", "다른 모델(Haiku 권장)이 태그 어휘 없이 재분류한다. <code>primary_category</code> 일치 70% 미만이면 프롬프트 개선 후보다."),
            ("30 일 calibration", "<code>post_freq</code> 는 canonical 과 aliases 를 합친 클러스터로 센다. 재발하면 등급 상향, 게이트가 있는데 재발하면 게이트 점검."),
            ("임계값 재평가", "60 일 이상 데이터가 있어야 freq 2 · 3 임계 변경을 제안한다. 자동 저장하지 않고 diff 로 보인다."),
        ],
        extra=KAIZEN_TABLE + '\n\n' + KAIZEN_NEAR,
    ),
]

if __name__ == "__main__":
    css = (TOOLS / "page.css").read_text(encoding="utf-8")
    for cfg in PAGES:
        src = Path(cfg["src"]).read_text(encoding="utf-8")
        Path(cfg["out"]).write_text(gen.render(cfg, src, css), encoding="utf-8")
        print("wrote", cfg["out"])
