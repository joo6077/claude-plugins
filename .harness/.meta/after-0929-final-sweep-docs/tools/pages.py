"""fs2 가 새로 만든 쪽 둘의 머리글 · 요점 카드. `gen.py` 가 읽는다."""

DESIGN = dict(ACCENT='#E8965A', ACCENT2='#F0B088', ACCENT_RGB='232,150,90',
              L_ACCENT='#9A4F1C', L_ACCENT2='#7C3F16', L_ACCENT_RGB='154,79,28')
REACT = dict(ACCENT='#38BDF8', ACCENT2='#7DD3FC', ACCENT_RGB='56,189,248',
             L_ACCENT='#0369A1', L_ACCENT2='#075985', L_ACCENT_RGB='3,105,161')


def badges(src, *extra):
    return ['원본 <code>%s</code>' % src] + list(extra)


STYLE_RULES = [
    ('<code>any</code>', '금지', '<code>@typescript-eslint/no-explicit-any</code>'),
    ('<code>as</code> 타입 단언', '<code>as const</code> 만', '제한'),
    ('<code>!</code> non-null 단언', '금지', '<code>@typescript-eslint/no-non-null-assertion</code>'),
    ('<code>export default</code>', '금지', '<code>no-default-export</code>'),
    ('<code>React.FC</code>', '경고', '<code>(props: Props) =&gt; JSX.Element</code> 또는 <code>forwardRef</code>'),
    ('<code>console.log</code>', 'production 경고', '<code>no-console</code>'),
    ('<code>throw new</code>', '<code>src/domain/</code> 에서 금지', 'Result 타입을 쓴다'),
    ('상대 경로 <code>\'../../../\'</code>', '금지', 'absolute <code>@/</code> 만'),
]

NAMING_RULES = [
    ('File', 'kebab-case', '<code>user-profile-card.tsx</code> · <code>use-drag.ts</code>'),
    ('Component', 'PascalCase', '<code>UserProfileCard</code>'),
    ('Hook', '<code>use</code> prefix', '<code>useDrag</code> · <code>useUser</code>'),
    ('Type', 'PascalCase', '<code>User</code> · <code>UserFailure</code>'),
    ('Zod schema', 'PascalCase + <code>Schema</code> suffix', '<code>UserSchema</code>'),
    ('Store', '<code>use&lt;Name&gt;Store</code>', '<code>useAuthStore</code>'),
]


def table(caption, heads, rows):
    out = ['<section class="section" aria-labelledby="%s">' % caption[0],
           '  <div class="section-label" id="%s">%s</div>' % caption,
           '  <div class="table-wrap">',
           '    <table>',
           '      <thead>',
           '        <tr>' + ''.join('<th>%s</th>' % h for h in heads) + '</tr>',
           '      </thead>',
           '      <tbody>']
    for row in rows:
        out.append('        <tr>')
        for cell in row:
            out.append('          <td>%s</td>' % cell)
        out.append('        </tr>')
    out += ['      </tbody>', '    </table>', '  </div>', '</section>']
    return '\n'.join(out)


def style_extra():
    return '\n\n'.join([
        table(('rules-at-a-glance', 'ESLint error 레벨 규칙 한눈에'), ['대상', '규칙', '근거 · 대신 쓸 것'], STYLE_RULES),
        table(('naming-at-a-glance', '이름 규칙 한눈에'), ['무엇', '형식', '예'], NAMING_RULES),
    ])


PAGES = [
    dict(
        src='docs/design/research-log.md', out='docs/design-kit/research-log.html', css=DESIGN, base='cacd9da3',
        kit='Design Kit', eyebrow='Design Kit · 연구 기록', title='design-kit 연구 기록',
        subtitle='design-kaizen 이 사이클마다 <strong>조사한 외부 출처와 채택 여부</strong>를 누적한 기록이다. 다음 사이클의 중복 조사를 막고, 개선 결정이 어느 출처에서 왔는지 되짚는 데 쓴다.',
        badges=badges('docs/design/research-log.md', '판 1.4.0', '마지막 갱신 2026-09-25', '사이클 절 넷'),
        cards=[
            ('2026-09-24 · Phase 6', '되말하기 · 관례 표 · 반영 판정. 처리 배정표 아홉 행과 러닝북 추가 과제를 규약 한 곳 정의 · 스킬 인용 구조로 묶었다.'),
            ('2026-08-13 · Phase 6', '글로벌 REJECT <code>UI-04</code> 와 신규 델타를 신호로 삼았다. 외부 근거는 증거 파일 하나로 고정했다.'),
            ('2026-07-27 · Phase 6', '시각 · 런타임 검증 신뢰 문제와 <code>UI-06</code> 을 신호로 DTCG alias 표기 오류를 바로잡았다.'),
            ('2026-04-12 · 첫 조사', '디자인 토큰 · 접근성 · 색상 과학 등 10 개 카테고리를 조사하고 11 개 확장 토픽을 보강했다.'),
        ],
    ),
    dict(
        src='react-kit/references/style-guide.md', out='docs/react-kit/style-guide.html', css=REACT, base='cacd9da3',
        kit='React Kit', eyebrow='React Kit · 참고 문서', title='Style Guide',
        subtitle='react-kit 이 생성하는 <strong>모든 코드가 지킬 스타일 규칙</strong>이다. strict TypeScript 설정 · ESLint 금지 사항 · 이름 규칙 · Prettier 설정을 정하고, <code>/react-audit</code> 가 이 규칙을 검증한다.',
        badges=badges('react-kit/references/style-guide.md', '금지 사항 여덟', '이름 규칙 여섯'),
        cards=[
            ('strict TypeScript', '<code>strict</code> 에 더해 <code>noUncheckedIndexedAccess</code> · <code>exactOptionalPropertyTypes</code> 를 켠다.'),
            ('ESLint error 레벨', '<code>any</code> · non-null 단언 · <code>export default</code> 를 막고 <code>as</code> 는 <code>as const</code> 만 둔다.'),
            ('이름 규칙', '파일은 kebab-case, 컴포넌트 · 타입은 PascalCase, 훅은 <code>use</code> 로 시작한다.'),
            ('설치본에서 읽을 때', '설치본 플러그인에는 <code>docs/react/</code> 가 없다 — 못 열면 저장소 원문 주소로 읽고, 그래도 못 읽으면 지어내지 않는다.'),
        ],
        extra=style_extra(),
    ),
]
