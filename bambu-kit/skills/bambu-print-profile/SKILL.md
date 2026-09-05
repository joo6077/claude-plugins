---
name: bambu-print-profile
description: Bambu Lab H2S 환경에서 MakerWorld URL이나 로컬 모델 파일을 받아 process+filament JSON 프로파일을 자동 생성하여 import용 zip 번들로 떨궈주는 스킬. references/ 8종을 토대로 모델 형상 분석 → 실측 실패 모드 판정 → 소재 추천 → seam 전략 결정 → Bambu Studio용 JSON 생성까지 수행한다. "삼프 설정", "Bambu 프로파일 만들어줘", "출력 셋팅 추천", "프린트 프로파일", "MakerWorld 출력" 같은 요청 시 트리거. 단순 색상/온도/한 값 변경에는 트리거 X. 다른 프린터(X1/P1/A1 등)나 다른 슬라이서(OrcaSlicer/PrusaSlicer)에는 트리거 X — H2S + Bambu Studio 고정.
user-invocable: true
---

# Bambu Print Profile Skill

H2S + AMS HT + AMS 2 Pro + Bambu Studio v2.6.0+ 환경 가정. 사용자의 모델(URL/파일)을 받아 process+filament JSON을 생성하고 import용 zip을 떨궈준다.

## 트리거 조건

**트리거함:**
- MakerWorld URL이 메시지에 포함 (`makerworld.com/en/models/...`)
- 로컬 모델 파일 경로(.3mf/.stl/.step) 언급
- "삼프 설정", "Bambu 프로파일 만들어줘", "출력 셋팅", "프린트 셋팅", "MakerWorld 모델 출력하려고" 같은 표현
- "원기둥 seam 안 보이게", "회전체 표면 깔끔하게" 같은 형상 + seam 결합 요청

**트리거 안 함:**
- 단순 1필드 변경 ("온도 245로 해줘", "색만 바꿔줘")
- 기존 프로파일 리뷰
- 다른 프린터 / 다른 슬라이서 언급
- 슬라이싱 결과 분석만 요청 ("이 출력 어땠어?")

## 작업 디렉토리 / 파일 구조

bambu-kit 플러그인 일부. 설치 시 `~/.claude/plugins/cache/joo6077-plugins/bambu-kit/<version>/skills/bambu-print-profile/`에 풀린다.

```text
bambu-kit/skills/bambu-print-profile/
├── SKILL.md                          # 이 파일
├── BACKLOG.md                        # v2 카이젠/자동 capture 백로그
└── references/
    ├── bambu-fields-baseline.md      # Bambu Studio JSON schema (필수 필드, 키 이름) + §8 Surface 필드 19종
    ├── materials.md                  # 40+ 필라멘트 카탈로그 + 용도 매핑
    ├── seam-recipes.md               # 형상×소재 scarf 매트릭스 + Real-world findings + §0 Surface-first 회전체 default v2
    ├── surface-recipes.md            # Surface-first 정책 (Auto-select 결정 트리 + 외벽/Top·Bottom/Ironing 매트릭스 + 트레이드오프) — 사전 정책
    ├── failure-recipes.md            # 2026-08-13 신규 — 실측 실패 3종(L1 곡면 계단 / L2 스트링잉 / L3 바닥 박리) 사후 레시피 + 금지 키 사유 정본
    ├── comment-analysis.md           # v0.4.0 신규 — 댓글 4 카테고리 추출 매뉴얼 + 한/영/중 키워드 사전 + Designer Constraint Override Rule
    ├── tolerance.md                   # v0.4.2 신규 — 공차 보정 키 (elefant_foot/xy_hole/xy_contour) + 소재별 수축률 + fit-critical 결정 트리 + calibration coupon
    └── kaizen-sources.md             # 주 1회 갱신용 데이터 소스 (카이젠 스킬용)
```

출력 경로: **`/Users/jackson/Hub/60_3D Print/Settings/<모델명>/`**

## 워크플로우 (Phase 1~5 · 진입 게이트 4종 + Coupon)

> **2026-08-13 카이젠 변경 (Phase 13)**: Phase 1.9 (Failure-Mode Detector) 신규 — 사용자 실측 출력 실패 3 종(L1 곡면 계단현상 / L2 스트링잉 / L3 바닥 박리)을 프로파일 키로 되돌리는 **인테이크 경로**가 아예 없었다. Phase 1.6 은 *다른 사용자의* 댓글 실패만 모으고, *이 사용자 자신의 직전 출력 결과*가 다음 프로파일 생성에 들어오는 경로가 0 건이었다 — 그래서 v0.4.2 공차 정정도 2026-07-27 표면 의도 게이트도 전부 사용자가 불만을 말한 뒤 손으로 실린 사후 수습이었다. Phase 3.0 (Supportability Split) 신규 — JSON 으로 지원 불가능한 요구(L1 adaptive layer height)를 조용히 근사 구현하지 않고 **notes only** 로 분기한다. Phase 4.3 게이트에 **금지 키 검사 4 종** 추가 (E3 확장 — 문장 추가가 아니라 기존 결정론적 게이트의 검사 항목 확장). references/failure-recipes.md 신규 + bambu-fields-baseline.md §10 신규. 사실 정정 3 건 (`layer_height 0.08` 근거 · `enable_arc_fitting` 성격 · `resolution` 적용 축). 근거: `.harness/.meta/evidence/phase13.md`.
>
> **2026-07-27 카이젠 변경**: Phase 1.0 (로컬 모델 견고 파싱) 신규 — `sed` 태그 매칭 금지 + `3D/Objects/*.model` 처리 + 빈 출력 = 검증 실패. Phase 1.8 (Surface Intent Gate) 신규 — 표면 의도 확인이 MakerWorld 전용 경로에만 있어 로컬 파일 케이스에서 ironing 이 누락되던 구조적 구멍을 막음. Phase 4.3 (Completion Evidence Gate) 신규 — 생성 JSON 을 실제 파싱해 검증하는 결정론적 명령(E3). 공차는 **경계 오프셋(지름 = 2×)** 임을 `tolerance.md` §1.1 에 SSOT 로 고정하고 `PL-01` 불일치 해소. 공차 무효화 3조건(color-paint / fuzzy-skin / raft) 신규 발견 반영.
>
> **v0.4.2 변경**: Phase 1.7 (Tolerance & Fit Analysis) 신규 + Phase 3 공차 보정 키 정책 + Phase 5 fit calibration coupon 자동 트리거 + references/tolerance.md 신규 + materials.md 수축률 컬럼 보강. dogfood: 페리스 휠(MakerWorld 1186414) 608ZZ 베어링이 중심부와 안 맞은 사용자 보고(2026-05-27) + 9mm sheath blade slide-fit 가능성. fit-critical 부품 식별 → 공차 보정 자동화.
>
> **v0.4.0 변경**: Phase 1.6 (Comment Analysis) 신규 + Designer Constraint Override Rule 정책 신규 + Phase 1 전체 크롤링 강화(다국어/페이지네이션/스크롤). dogfood 출처: 2026-05-23 9mm Craft Knife Elite 케이스 — 디자이너 댓글 "No supports needed, please do not modify the print profile" 무시하고 surface-first 모드 자동 적용한 회귀. 사용자 피드백 "넌 서포트 넣엇더라 + 댓글이나 피드백 참고 안 하더라".
>
> **v0.3.0 변경**: Phase 1.5 (Attached Resources Analysis) 신규 추가. Phase 4 notes.md 5섹션 표준화. Phase 5 coupon 자동 생성. dogfood 출처: 2026-05-19 Stealth Press 1S 케이스 — 웹 BOM만 봤다가 PDF 매뉴얼에서 헷갈리는 인서트 5군데, 희생 부품, 부싱 접착, 실제 인서트 수 등을 놓침.

### Phase 1 — 모델 컨텍스트 추출 (전체 크롤링)

**입력 분기:**

1. **MakerWorld URL** → **Playwright MCP 1차** (`mcp__playwright__browser_navigate` → `mcp__playwright__browser_snapshot` 또는 `browser_take_screenshot`). MakerWorld Cloudflare 차단을 우회하고 JS-rendered 모델 상세/댓글/사진까지 추출 가능. 추출 정보: 모델명/제작자/부품 구성/회전체 부품/권장 프로파일/사용자 댓글 전체. Playwright 미사용 환경이면 `codex-rescue` 에이전트에 위임 (research mode), 둘 다 실패 시 사용자에게 직접 입력 요청.
2. **로컬 .3mf 파일** → embedded 설정(`Metadata/project_settings.config`, **JSON**) + 지오메트리를 **아래 Phase 1.0 절차로** 추출. 부품별 dimension을 "Bambu Studio에서 확인" 으로 사용자에게 넘기지 마라 — 파싱으로 얻을 수 있다.
3. **STL 파일** → **아래 Phase 1.0** bounding box 파서 사용. `du -h` 같은 파일 크기는 형상 정보가 아니다. 회전체 판정은 bbox 종횡비 + 사용자 설명 조합.
4. **이미 정보가 채팅에 있음** → 그대로 사용.

#### Phase 1.0 — 로컬 모델 지오메트리 추출 (견고 파싱 · 2026-07-27 신규)

⚠️ **안티패턴 — 태그 범위 셸 매칭 금지.** 3MF 내부는 XML 이고 **거의 모든 태그가 속성을 가진다.** 실측 확인:

```text
<build p:UUID="2c7c17d8-22b5-4d84-8835-1976022ea369">
<item objectid="2" p:UUID="00000002-…" transform="1 0 0 …" printable="1"/>
```

따라서 `sed -n '/<build>/,/<\/build>/p'` 는 **0 줄**을 돌려준다 (실측 재현됨). `<build>` 는 3MF Core Spec 상 `@anyAttribute` 를 허용하므로 이건 예외가 아니라 정상 형태다. `grep '<build>'` / `sed` 태그 범위 매칭 **금지** — 반드시 정식 XML 파서(`xml.etree.ElementTree`)를 써라.

⚠️ **지오메트리는 `3D/3dmodel.model` 에 없을 수 있다.** Bambu Studio 는 production extension 을 써서 오브젝트를 `3D/Objects/object_N.model` 로 분리한다. 실측 예: root `3dmodel.model` 은 1.9KB / **vertex 0개**, 실제 메시는 `3D/Objects/object_1.model` (514 verts). root 만 보고 "메시 없음" 으로 결론내지 마라. 네임스페이스도 필수 (`xmlns` core + `p` production).

**3MF 추출 (검증된 명령 — 실측 통과):**

```bash
python3 - "<model.3mf>" <<'PY'
import sys, zipfile, xml.etree.ElementTree as ET
NS={'c':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02',
    'p':'http://schemas.microsoft.com/3dmanufacturing/production/2015/06'}
z=zipfile.ZipFile(sys.argv[1]); names=z.namelist()
root=next((n for n in names if n.lower()=='3d/3dmodel.model'),None)
assert root, f"FAIL: 3dmodel.model 없음. 실제 목록={names[:20]}"
items=ET.fromstring(z.read(root)).findall('.//c:build/c:item',NS)
print("build items:",len(items),"objectids:",[i.get('objectid') for i in items])
n=0
for part in sorted(p for p in names if p.lower().startswith('3d/') and p.lower().endswith('.model')):
    for obj in ET.fromstring(z.read(part)).findall('.//c:resources/c:object',NS):
        vs=obj.findall('.//c:mesh/c:vertices/c:vertex',NS)
        if not vs: continue
        xs=[float(v.get('x')) for v in vs]; ys=[float(v.get('y')) for v in vs]; zs=[float(v.get('z')) for v in vs]
        n+=1
        print(f"  {part} id={obj.get('id')}: {len(vs)} verts "
              f"bbox={max(xs)-min(xs):.2f} x {max(ys)-min(ys):.2f} x {max(zs)-min(zs):.2f} mm")
assert n>0, "FAIL: 메시 0개 파싱 — 빈 결과는 PASS 아님"
print("meshes parsed:",n)
PY
```

임베드 프로파일은 JSON 이므로 그대로 파싱한다 (grep 금지):

```bash
unzip -p "<model.3mf>" Metadata/project_settings.config \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print({k:d.get(k) for k in ['layer_height','wall_loops','sparse_infill_density','enable_support','ironing_type','seam_position','xy_hole_compensation','xy_contour_compensation','elefant_foot_compensation','raft_layers']})"
```

**STL 추출 (검증된 명령 — ASCII/바이너리 양쪽, 실측 통과):**

```bash
python3 - "<model.stl>" <<'PY'
import sys, struct
d=open(sys.argv[1],'rb').read(); pts=[]
if d[:5].lower().lstrip()[:5]==b'solid' and b'facet' in d[:2048]:
    for ln in d.decode('utf8','replace').splitlines():
        w=ln.split()
        if len(w)==4 and w[0]=='vertex': pts.append(tuple(map(float,w[1:])))
else:
    n=struct.unpack('<I',d[80:84])[0]
    assert len(d)>=84+50*n, f"FAIL: STL 잘림 (선언 tris={n})"
    for i in range(n):
        o=84+50*i+12
        for j in range(3): pts.append(struct.unpack('<3f',d[o+12*j:o+12*j+12]))
assert pts, "FAIL: vertex 0개 — 빈 결과는 PASS 아님"
xs,ys,zs=zip(*pts)
print(f"tris={len(pts)//3} bbox={max(xs)-min(xs):.2f} x {max(ys)-min(ys):.2f} x {max(zs)-min(zs):.2f} mm")
PY
```

⚠️ **빈 출력은 PASS 증거가 아니라 검증 실패 신호다** (`harness/docs/guides/skill-design-guide.md` §3.7). 위 명령들은 그래서 `assert` 로 non-zero exit 한다. 0 줄/0 vertex/빈 dict 가 나오면 **형상 정보 없음으로 진행하지 말고** 파싱 경로를 고치거나, 못 고치면 사용자에게 dimension 을 물어라. 추측한 치수로 공차를 계산하면 Phase 1.7 전체가 무의미해진다.

**전체 크롤링 원칙 (v0.4.0 강화):**

페이지 상단(제목/제작자/Description)만 보고 끝내지 말고 **전체 페이지 + 전체 댓글 + 댓글 안 첨부 이미지/링크/언급 리소스**를 single pass로 enumerate한다.

- **댓글 카운트 확인**: 스냅샷에서 `heading "Comment & Rating (N)"` 형식으로 N 파싱.
- **20개 이하**: 단일 스냅샷에 모두 포함됨. 그대로 분석.
- **20-50개**: Playwright `browser_evaluate`로 페이지 스크롤(`window.scrollBy`) 3-5회 후 재스냅샷.
- **50+ 댓글**: 정렬 변경 (`Top` / `Most Likes` / `Newest First`)으로 sampling. designer_reply는 100% 추출, 나머지는 평점 분포 + 텍스트 30+ 댓글 추출. `references/comment-analysis.md` §4.1 참조.
- **다국어 댓글**: MakerWorld는 중/영/한 혼재. 번역된 본문 + "Show original" 클릭한 원문 둘 다 캡처. 다국어 키워드 사전은 `references/comment-analysis.md` §3 참조.
- **페이지네이션**: 댓글 영역의 "Load more" 또는 페이지 번호 UI가 있으면 `browser_click`으로 진행.

**Attached Resources Inventory (필수, MakerWorld URL 케이스 한정):**

페이지 스냅샷에서 외부 링크를 enumerate하여 분류:

```bash
grep -oE 'https?://[^"]+\.pdf' <snapshot-yml>     # assembly manual
grep -oE 'https?://youtu\.be/[^"]+|youtube\.com/watch[^"]+' <snapshot-yml>  # 영상
grep -oE 'https?://github\.com/[^/"]+/[^/"]+' <snapshot-yml>  # 레포
grep -oE 'https?://(printables|thangs|cults3d)\.com/[^"]+' <snapshot-yml>  # 외부 호스팅
```

결과를 4개 카테고리로 분류해서 사용자에게 짧게 보고:
- **assembly_manual_pdf**: 0개 이상
- **video_build_guide**: 0개 이상
- **github_repo**: 0개 이상
- **external_bom_or_alt**: 0개 이상

추출 후 사용자에게 짧게 보고: 모델명, 부품 수, 회전체 여부, 권장 소재 후기, **첨부 자료 카운트** (있다면).

### Phase 1.5 — Attached Resources Analysis (v0.3.0 신규)

**조건부 실행** — Phase 1에서 첨부 자료를 찾았을 때만. 없으면 skip하고 Phase 2로.

#### 1.5.1 PDF Assembly Manual 분석 (있으면 필수)

```bash
mkdir -p "/Users/jackson/Hub/60_3D Print/Settings/<모델명>/"
curl -L -o "/Users/jackson/Hub/60_3D Print/Settings/<모델명>/assembly-manual.pdf" "<pdf-url>"

# 페이지 수 확인 (10p 이상이면 분할 Read)
mdls -name kMDItemNumberOfPages "/Users/jackson/Hub/60_3D Print/Settings/<모델명>/assembly-manual.pdf"
```

Read 도구로 분석 (10p 이상이면 `pages: "1-10"`, `pages: "11-20"` 형식으로 분할):

추출 항목 (체크리스트):
- ☐ Bill of Materials — PDF가 웹 BOM보다 정확할 가능성 높음. **수량/규격이 다르면 PDF 우선**.
- ☐ 조립 단계 enumerate — 1~N 단계 순서
- ☐ **숨은 부품 위치** — "Insert on other side!", "Do not forget", "Fit from the back!" 같은 표시 검색
- ☐ **안전 주의사항** 🔥/⚠️ — "Do not over-tighten", "Prevent X at all cost", "fix A before B" 등 순서 의존성
- ☐ **인서트/볼트 실제 카운트** — 매뉴얼의 번호를 카운트하면 웹 BOM과 다를 수 있음
- ☐ **별도 소모품** — 접착제, RTV 실리콘, shim, 필라멘트 조각, 출력 외 부품
- ☐ **도구/부품 분기** — 인두 타입별 mount STL, 변형 부품
- ☐ **인서트 압입 온도** 명시 여부

#### 1.5.2 YouTube 영상 (있으면 시도)

1차: `codex-rescue` 에이전트에 transcript 추출 위임 (`MODE=research`, `--write` X). 출력 계약:
- 핵심 손기술 팁 5-10개
- 자주 보고되는 실수 패턴
- 비디오 timestamp + 설명

실패 시 fail-soft — notes.md §5에 영상 URL만 첨부. 토큰 낭비 금지.

#### 1.5.3 GitHub README (있으면)

```bash
# raw.githubusercontent.com 변환
curl -sL "https://raw.githubusercontent.com/<owner>/<repo>/main/README.md" -o /tmp/readme.md
# 또는 master 브랜치
```

추출 항목:
- CHANGELOG / Releases — 리비전 차이 (R1 vs R1S 같은 케이스)
- 추가 STL 위치
- 라이센스 (LICENSE 파일도 확인)

#### 1.5.4 Cross-check 보고

웹 BOM과 PDF 매뉴얼의 차이가 있으면 **사용자에게 명시 보고**:

```text
⚠️ Cross-check 결과
- 웹 BOM: 인서트 30개 / PDF 매뉴얼 카운트: 34개 → 35-40개 권장
- 웹 BOM: M3x25 / R1S 매뉴얼: M3x20 (사이즈 다름)
- PDF에만 있음: bushing 접착제, 0.5-1mm shim, 인두 타입별 mount STL 선택
```

### Phase 1.6 — Comment Analysis (v0.4.0 신규)

**필수 실행** — MakerWorld URL 케이스 한정. 댓글 0개라도 명시 "댓글 없음" 보고. 상세 매뉴얼은 `references/comment-analysis.md` 참조.

Phase 1에서 전체 크롤링한 댓글을 4 카테고리로 분류하고 디자이너 명시 권장사항을 추출한다. **이 phase가 완료되지 않으면 Phase 2로 진입 금지** (Designer Constraints Gate).

#### 1.6.1 4 카테고리 추출

`references/comment-analysis.md` §2를 로드하여 각 댓글을 분류:

- **designer_reply** — 디자이너(@creator)가 작성한 댓글/답변. 최우선 추출 대상.
- **user_success** — 출력 성공 보고 (사진 + 4-5점 평점).
- **user_failure** — 출력 실패/문제 보고 (warping, stringing, mechanism, 1-3점 평점).
- **user_variant** — 사이즈/소재/구조 변형 보고.

각 카테고리에 추출된 항목을 카운트하여 보고:
```text
댓글 분석 결과
- designer_reply: X개 (핵심 권장 N건 추출)
- user_success: Y개
- user_failure: Z개
- user_variant: W개
```

#### 1.6.2 Designer Constraints 키워드 추출

`references/comment-analysis.md` §3의 한/영/중 키워드 사전을 사용하여 designer_reply에서 명시 권장사항을 추출:

```bash
# 영어
grep -iE "no supports?|do not modify|must|recommend|required|never" <comments>
# 한국어
grep -E "권장|금지|필수|반드시|꼭|쓰면 안" <comments>
# 중국어
grep -E "请不要|需要|必须|建议|不要修改|禁止" <comments>
```

추출 결과를 구조화:

```yaml
designer_constraints:
  - source: "@<creator> [2025-07-22 11:11]"
    raw_quote: "No supports needed, please do not modify the print profile."
    parsed:
      - constraint_type: "forbid_support"
        target_field: "enable_support"
        target_value: "0"
        priority: "strong"
      - constraint_type: "forbid_profile_modification"
        target_field: "*"
        priority: "strong"
        note: "surface-first/auto-tuning 적용 전 사용자 confirm 필수"
```

#### 1.6.3 comments-raw.md 아카이브

추출 결과를 `<output_dir>/comments-raw.md`로 raw 저장. MakerWorld 페이지가 미래에 수정/삭제될 수 있어 reproducibility 확보. 포맷은 `references/comment-analysis.md` §6 참조.

```bash
mkdir -p "/Users/jackson/Hub/60_3D Print/Settings/<모델명>/"
# comments-raw.md 작성 (designer_reply 100% quote, 나머지 카테고리는 sample)
```

#### 1.6.4 Further Research 분기 (조건부)

댓글에서 **외부 URL/추가 리소스 언급**이 발견되면 진입. 0개면 skip.

대상 패턴:
- printables.com / thingiverse / cults3d — 같은 모델의 다른 호스팅
- GitHub repo — fork/remix
- YouTube/Bilibili — 빌드 가이드 영상

처리:
1. 같은 모델의 다른 호스팅: WebFetch 또는 Codex 위임으로 매뉴얼/추가 STL 확인
2. GitHub: `curl -sL raw.githubusercontent.com/...README.md` fetch
3. 영상: `codex-rescue` 에이전트에 transcript 위임 (research mode), fail-soft

skip:
- SNS, URL shortener, affiliate 링크 — `references/comment-analysis.md` §4.2 참조.

#### 1.6.5 Cross-check 보고 (디자이너 권장 vs 자동화 모드)

추출된 designer_constraints가 자동화 모드(특히 surface-first)와 충돌하면 **사용자에게 명시 보고**하고 4-옵션 confirm 요청:

```text
⚠️ Designer Constraint vs Auto-mode Cross-check

디자이너 명시 권장 (강도 enumerate):
  - "No supports needed" (strong constraint with value: enable_support=0)
  - "Please do not modify the print profile" (directive — Creator 명시 필드만 적용)
  - "Push-lock means it must be held down" (intent — JSON 무관, §3.2 사용성)

Creator 명시 필드 (page profile label):
  - layer_height = 0.1mm, wall_loops = 2, sparse_infill_density = 15%

자동화 모드 충돌 분석:
  - surface-first의 layer/wall/infill 변경 → Creator 명시 필드와 충돌
  - surface-first의 ironing/scarf/outer_speed/wall_sequence → Creator 미명시 → 자동 결정 가능

옵션 (v0.4.1 4-option, [C]가 default Recommended):
  [C] "모든 면 매끈 — 디자이너 권장 ∧ surface-first 병행" (Recommended, ~3배 시간)
      Creator 명시 4필드 freeze (layer/walls/infill/support) +
      surface-first 4필드 추가 (ironing topmost_only / scarf external 6mm /
      outer_wall_speed 30 / wall_sequence inner-outer-inner). 외벽·top·seam 전부 매끈.
  [A] "속도 우선 / 외관 후순위" (~1.2배 baseline)
      Creator 명시 4필드만 freeze. ironing/scarf/외벽 매끈 처리 모두 OFF.
      사용자가 "디자이너 권장 = 전체 profile 수정 X 의미"라고 명시할 때만 선택.
  [B] "평면 top만 매끈 (ironing only)" (~1.5배)
      Creator 명시 4필드 freeze + ironing topmost_only만 추가. 외벽/seam은 baseline.
      박스 형상에서 top 평면이 visible할 때.
  [D] "Surface-first 풀 — Creator 명시값 무시" (~3.5배)
      Creator 명시 4필드도 surface-first 값으로 덮어씀 (layer 0.12, walls 3, infill 18).
      디자이너 권장 명시 무시 동의 필요. 가장 매끈하지만 의도 위배.
```

또한 .3mf creator profile metadata와도 cross-check:
- 댓글은 support OFF 권장 vs .3mf print profile은 support ON → 사용자에게 보고
- 댓글의 권장 layer vs .3mf의 layer 값 불일치 → 사용자에게 보고

**Phase 3 처리 분기 (옵션별):**
- [A] 강도 1 (strong with value) 모두 freeze + 강도 2 (directive) 영역도 freeze. Creator 미명시 영역 default 유지
- [B] [A] + ironing topmost_only 한 항목만 추가
- [C] (default) 강도 1 + Creator 명시 필드 freeze. Creator 미명시 영역(ironing/scarf/외벽 매끈)은 surface-first 자동 적용
- [D] 강도 1만 freeze (support 등 안전 사항). 다른 모든 영역은 surface-first 값으로 덮어씀

#### Designer Constraints Gate (Phase 1.7 진입 조건)

위 1.6.1~1.6.5 완료 + 사용자 confirm(또는 댓글 0개로 빈 designer_constraints 확정)이 끝나야 Phase 1.7로 진입.

### Phase 1.7 — Tolerance & Fit Analysis (v0.4.2 신규)

**필수 실행** — 모든 MakerWorld URL/로컬 파일 케이스. fit-critical 부품 없으면 "fit-critical 부품 없음 — 일반 공차 처리만" 명시. 상세 정책은 `references/tolerance.md` 참조.

Phase 1 크롤링 + Phase 1.5 첨부 자료 + Phase 1.6 댓글에서 fit-critical 부품 4 카테고리 enumerate. 결과는 Phase 2 소재 선택(수축률 영향) + Phase 3 공차 보정 키 결정에 직접 입력.

#### 1.7.1 Fit-critical 부품 4 카테고리 식별

**(a) Bearing (베어링 압입)**

식별 패턴 (Phase 1 본문 + 댓글 + 부품 라벨에서 grep):
- ISO 베어링 번호: "608", "608ZZ", "609", "688", "688ZZ", "625", "625ZZ", "MR105", "MR84"
- 키워드: "bearing", "베어링", "轴承"
- 모델 카테고리: "ferris wheel", "spinner", "fidget", "회전체", "스피너", "fan", "wheel"

**(b) Bolt / Screw**

식별 패턴:
- 메트릭 표준: "M3", "M4", "M5", "M6", "M8"
- 키워드: "bolt", "screw", "self-tapping", "wood screw", "machine screw"
- BOM 표 또는 댓글에서 "x M3" 같은 카운트

**(c) Heat-set Insert (열 인서트)**

식별 패턴:
- 키워드: "heat-set insert", "brass insert", "M3 insert", "soldering iron + insert"
- 어셈블리 가이드의 "press insert at X mm hole" 표시

**(d) Slide-fit / Push-lock / Snap-fit**

식별 패턴:
- 키워드: "push lock", "push button", "slide fit", "snap fit"
- 모델: knife sheath, pen holder, drawer, sliding mechanism, linear motion 부품

#### 1.7.2 카테고리별 카운트 보고

```text
Tolerance Analysis 결과
- bearing: X개 (구체 spec: 608ZZ × 2, MR105 × 4 등)
- bolt: Y개 (M3 × N, M4 × N)
- insert: Z개 (M3 heat-set × N)
- slide-fit: W개 (knife sheath slide × 1, drawer slide × N)

없으면 "fit-critical 부품 없음 — 일반 공차 처리만 (공차 보정 키 default 유지)"
```

#### 1.7.3 부품 카테고리 → 공차 보정 키 매핑 사전

`references/tolerance.md` §3 결정 트리 + §4 standard fastener/bearing 사이즈 사전 참조하여 다음을 결정:

| 카테고리 | Bambu JSON 키 | 권장 보정 방향 |
|---------|--------------|---------------|
| bearing OD (압입) | `xy_hole_compensation` | + (소재별 표 §2 참조) |
| bearing ID (축 fit) | `xy_contour_compensation` | − (소재별 표) |
| bolt pass hole | `xy_hole_compensation` | + · **`tolerance.md` §3.2 규칙을 따른다** (모델이 이미 3.2-3.4mm 면 수축 보정만, 명목 3.0mm 면 오프셋 `+0.10~+0.20`) |
| heat-set insert hole | hole 명시 (M3=4.0mm) | `xy_hole_compensation` 표 그대로 |
| slide-fit hole | `xy_hole_compensation` | + (loose 권장) |
| slide-fit 외경 | `xy_contour_compensation` | − (loose 권장) |
| 첫 레이어 squish 영향 | `elefant_foot_compensation` | 0.10-0.20 (PLA 0.15 default) |

⚠️ **Bambu 키 이름 오타 주의**: `elefant_foot_compensation` (e 빠짐 — Bambu 의도적 오타). `elephant_foot_compensation`으로 쓰면 silent skip.

⚠️ **보정값은 경계 오프셋 — 지름 변화는 2배다.** `보정값 = (목표 지름 − 모델 지름) / 2`. 정본은 `references/tolerance.md` **§1.1**. 이 변환을 건너뛰고 §4 의 "최종 지름" 을 보정값 칸에 그대로 넣는 것이 평가자 REJECT `PL-01` 의 원인이었다. 계약서에 지름으로 적혀 있어도 JSON 에는 **오프셋**으로 환산해 넣어라.

#### Tolerance Gate (Phase 2 진입 조건)

Phase 1.7.1~1.7.3 완료 (또는 fit-critical 0건 확정)가 끝나야 Phase 2로 진입.

### Phase 1.8 — Surface Intent Gate (2026-07-27 신규)

**필수 실행 — 모든 입력 분기 (MakerWorld / 로컬 .3mf / STL / 채팅 정보).**

> **왜 신규인가 (실측 회귀):** 사용자가 표면 품질을 원했는데 기능성 프로파일만 생성해 **ironing 없이 완료 보고**한 회귀가 발생했다. 사용자가 "표면 매끈해야하는데.. 한거 맞음?" → "아이어닝해야지" 로 **두 번** 지적해야 했다. 원인은 표면 의도 확인이 **Phase 1.6.5 (MakerWorld URL 전용)** 안에만 있었다는 구조적 누락이다 — 로컬 파일이나 댓글 0개 케이스에서는 표면 품질을 **아무도 묻지 않는 경로**가 존재했다. 실측 확인: 페리스 휠 생성물의 임베드 config 가 `ironing_type: "no ironing"`.

#### 1.8.1 이미 결정됐으면 재질문 금지

Phase 1.6.5 에서 사용자가 옵션 `[A]`/`[B]`/`[C]`/`[D]` 를 이미 선택했으면 **그것을 그대로 승계**하고 1.8.2 를 skip 한다. 같은 질문을 두 번 하지 마라.

#### 1.8.2 표면 의도 확인 (위 승계가 없을 때 필수)

사용자 요청에서 표면 의도 키워드를 먼저 grep 한다:

```bash
# 표면 우선 신호
grep -iE "매끈|매끄럽|반들|광택|표면|외관|심 안 보|seam 안|이쁘게|smooth|shiny|surface|cosmetic|아이어닝|ironing"
# 기능 우선 신호
grep -iE "기능|튼튼|빨리|속도|시간|prototype|functional|strong|fast|test"
```

판정:

| 상황 | 처리 |
|------|------|
| 표면 신호 **있음** | surface-first ON. `ironing_type` 결정 트리(Phase 3) 필수 통과. |
| 기능 신호만 있음 | surface-first OFF. **notes.md 에 "표면 마감 미적용" 명시** (조용히 빠뜨리지 말 것). |
| **둘 다 없음 / 모호** | **사용자에게 1줄로 물어라** — 추측 금지. |

모호할 때 질문 형식:

```text
표면 마감 방향을 정해야 합니다 (출력 시간에 직접 영향):
  [S] 표면 우선 — 평면 top ironing + 외벽 저속 + scarf seam (~1.5-3배 시간)
  [F] 기능 우선 — baseline 속도, ironing/scarf 없음 (~1.0-1.2배)
기본 권장: 눈에 보이는 곳에 쓰는 부품이면 [S], 내부 지그/기능 부품이면 [F].
```

#### 1.8.3 형상 × 소재 적용성 교차 확인

표면 우선이라도 **무의미하거나 해로운 조합**은 적용하지 않고 그 사유를 보고한다:

- 회전체 / spiral vase → top 이 없어 ironing 무의미 (seam 전략으로 처리)
- TPU / PA-CF → ironing 불가 또는 역효과 (Phase 3 소재 판정표)
- PETG HF → 건조 미충족 시 stringing 위험 (surface-recipes.md §6.5 경고 준수)

#### Surface Intent Gate (Phase 2 진입 조건)

1.8.1 승계 **또는** 1.8.2 판정 완료가 끝나야 Phase 2 로 진입한다. **표면 의도가 미확정인 상태로 Phase 3 JSON 생성에 진입 금지.**

⚠️ 표면 우선으로 판정됐는데 최종 process JSON 의 `ironing_type` 이 `"no ironing"` 이면 그것은 **게이트 실패**다 — Phase 4 검증 명령이 이를 잡는다.

### Phase 1.9 — Failure-Mode Detector (2026-08-13 신규)

**필수 실행 — 모든 입력 분기.** 상세 레시피는 `references/failure-recipes.md` 참조.

> **왜 신규인가 (근본원인):** 이 스킬에는 **사용자 자신의 직전 출력 실패가 다음 프로파일 생성으로 들어오는 경로가 아예 없었다.** Phase 1.6 은 MakerWorld *댓글의 남의 실패*만 모으고, Phase 1.7/1.8 은 사전 형상·의도만 본다. 그래서 `/insights` 2026-08-13 관측(shower-box + holster 5 세션 · 곡면 계단현상 · voronoi stringing · 바닥 박리 반복 · "partially successful")에 해당하는 신호가 매번 대화 밖으로 흘렀고, 대응은 사용자가 불만을 말한 뒤의 손 수습이었다. 인테이크 자체가 없던 것이 원인이므로 규칙 문장을 하나 더 쓰는 것으로는 안 걸린다.

#### 1.9.1 실패 신호 추출

사용자 요청 · 채팅 컨텍스트 · Phase 1.6 의 `user_failure` 카테고리 세 곳을 대상으로 grep 한다.
Phase 1.6 이 skip 된 경로(로컬 파일)에서도 앞의 두 곳은 항상 존재한다.

```bash
# L1 — 곡면 계단현상 (curved surface stair-stepping)
grep -iE "계단|층층|단계단|거칠|곡면.*(거칠|계단)|stair|step(ped|ping)|layer line|faceted|각져"
# L2 — 스트링잉 (stringing)
grep -iE "실|거미줄|늘어|삐져|스트링|보로노이|string|wisp|ooze|hairy|voronoi"
# L3 — 바닥 박리 / 들림 / 워핑
grep -iE "박리|들림|들렸|떴|안 붙|휘|뒤틀|1층|첫 ?층|peel|lift|warp|curl|adhesion|detach"
```

⚠️ **substring 오탐을 확인하라.** `실` 은 `실제`·`실행`·`확실` 을 잡고 `1층` 은 `11층` 을 잡는다.
grep 결과를 그대로 판정으로 쓰지 말고 **매치된 문장을 읽어** 실제 출력 결과 보고인지 확인한다.
매치 0 건이면 "실패 모드 신호 없음" 을 **명시 보고**하고 1.9.3 을 skip 한다 — 조용히 넘기지 마라.

#### 1.9.2 재출력 여부 확인 (조건부)

재출력 신호(`다시`, `또`, `여전히`, `재출력`, `again`, `still`, `retry`)가 있거나 같은 모델명이
이미 `/Users/jackson/Hub/60_3D Print/Settings/<모델명>/` 에 존재하면 **1 줄로 물어라**:

```text
이 모델(또는 같은 소재·형상)로 이전에 출력한 결과가 있나요? 있으면 어디가 안 좋았는지 한 줄만 알려주세요.
(곡면 계단 / 실 늘어짐 / 바닥 들림 중 있으면 해당 항목의 대응 레시피를 켜겠습니다.)
```

재출력 신호가 없으면 **묻지 마라** (신규 모델에 불필요한 질문 금지).

#### 1.9.3 사용자 실측 보고의 취급 — 재정의 금지

정본은 `harness/docs/guides/skill-design-guide.md` **§3.8 User-Reported Failure Gate** 다.
여기서 규칙을 다시 쓰지 말고 그대로 따른다. 요지: 상태는 PASS 가 아니라 `REOPENED`,
**반박 금지**, 재현 전에 "정상입니다" 를 다시 말하지 않는다.

§3.8 재현 6 축의 3D 프린팅 치환표는 `references/failure-recipes.md` §0 에 있다 (모델 리비전 /
적용 preset 이름 / 슬라이서 버전 / plate·chamber / 소재 lot·건조 / AMS 슬롯). **6 축 중 다른 축을
먼저 값으로 특정**하고, 프로파일 키를 만지기 전에 사용자에게 보고한다. 건조 미충족이나 preset 미적용이
원인인 실패에 retraction 을 올리는 것은 원인이 아닌 곳을 고치는 행위다.

#### 1.9.4 판정 보고

```text
Failure-Mode 판정
- L1 곡면 계단현상: 감지 / 없음   (근거: 사용자 문장 quote)
- L2 스트링잉:      감지 / 없음
- L3 바닥 박리:     감지 / 없음
- 재현 6축 불일치:  <축 이름 + 값> 또는 "전 축 일치"
→ 감지 0 건이면 "실패 모드 신호 없음 — 사후 레시피 미적용"
```

**L2 ∧ L3 동시 감지 시** fan 방향이 상충한다 (`failure-recipes.md` §3.3) — 어느 쪽을 우선할지
사용자에게 명시적으로 물어라. 3 종 동시 처리 순서는 `failure-recipes.md` §5 (L3 → L2 → L1).

#### Failure-Mode Gate (Phase 2 진입 조건)

1.9.1 판정 완료 (+ 1.9.2 해당 시 응답 수령) 가 끝나야 Phase 2 로 진입한다.
**감지 결과 미확정 상태로 Phase 3 JSON 생성에 진입 금지.**

### Phase 2 — 소재 추천 (2-3개 + 사용자 픽)

**진입 조건**: Phase 1.6 completed (designer_constraints 추출) **+ Phase 1.7 completed (tolerance fit-critical 분석) + Phase 1.8 completed (Surface Intent Gate) + Phase 1.9 completed (Failure-Mode Gate)**. Phase 1.9 결과는 Phase 2 소재 추천에도 영향 — L2 감지 시 건조 요구가 큰 소재(PETG/PA/PC)를 후보에 남길 때 건조 조건을 함께 제시해야 한다. Phase 1.7 fit-critical 결과는 Phase 2 소재 추천에 직접 영향 — 소재별 수축률 차이가 fit 정확도와 직결 (PLA 0.2-0.3% < PETG 0.3-0.5% < ASA 0.5-0.8%). `references/materials.md` §4 수축률 표 참조.

`references/materials.md`를 로드. 모델 용도/형상/사용자 요구에 매칭:

| 용도 | 우선 후보 |
|------|----------|
| 박스 오프너/도구 (functional) | PETG HF, PLA Tough+ |
| 내열 부품 (vent, hot duct) | PETG HF, ASA, PC |
| 외관 prototype | PLA Basic, PLA Matte |
| 실외 부품 | ASA, ASA-CF |
| 기어/지그 | PAHT-CF, PETG-CF |
| 멀티컬러 가벼운 출력 | PLA Basic (같은 base 공유) |
| Sealing/gasket | TPU 90A (TPU 85A 비추 — 검증된 문제) |

**필수 cross-check:**
- AMS 2 Pro 직접 로드 가능 여부 (PET-CF/PPA-CF/PPS-CF/TPU 95A HF는 외부 스풀)
- 건조 요구 (PETG/PA/PC는 AMS HT 65°C 사전 + continuous)
- H2S 노즐 호환 (CF류는 hardened 권장)

후보 제시 → 사용자 픽. 단일/멀티 소재 결정.

### Phase 3 — 프로파일 JSON 생성

`references/bambu-fields-baseline.md` + `references/seam-recipes.md` 로드.
**Phase 1.9 에서 실패 모드가 1 건 이상 감지됐으면 `references/failure-recipes.md` 도 로드한다.**

#### Phase 3.0 — Supportability Split (2026-08-13 신규 · JSON 생성 **전** 필수)

⚠️ **JSON 으로 지원 불가능한 요구를 근사 구현하지 마라.** 조용한 근사는 "했다고 보고했는데 안 되어 있음" 으로 끝난다. Phase 1.9 감지 항목 + 사용자 요구를 **지원 가능 / 불가능** 두 칸으로 갈라 적고, 불가능 칸은 `notes.md` 에 명시 보고한다.

| 요구 | process/filament JSON | 처리 |
|------|----------------------|------|
| L1 계단 — **adaptive / variable layer height** | ❌ **불가** (`failure-recipes.md` §1.1) | **notes only.** `adaptive_layer_height` 를 JSON 에 넣지 마라 — Phase 4.3 게이트가 잡는다 |
| L1 계단 — 고정 `layer_height` 하향 | ✅ 가능 | `0.12` 1 차, `0.08-0.12` 는 사용자 확인 후 (`failure-recipes.md` §1.2) |
| L1 계단 — XY faceting | ✅ 가능 (조건부) | `resolution` `0.006-0.010`. ⚠️ Z 계단 해결책 아님. **XY faceting 을 실제로 관측했을 때만** 쓴다 — 2026-09-05 실측(faceting 없는 박스)에서는 이득 근거가 없어 철회됐다. surface-first 공통값으로 넣지 마라 |
| L2 스트링잉 — 건조/소재 상태 | ❌ **불가** (물리 조건) | notes + 건조 후 재출력 권고. **건조 미충족이면 JSON 을 만지지 마라** |
| L2 스트링잉 — wipe | ✅ 가능 (게이트 통과 시) | `filament_wipe` · `filament_wipe_distance` 2 키 한정 |
| L2 스트링잉 — retraction 상향 | ⚠️ **coupon 후에만** | Phase 5 coupon 통과 전 본 출력 반영 금지 |
| L3 박리 — brim / 첫 레이어 | ✅ 가능 | `failure-recipes.md` §3.1 |
| L3 박리 — chamber preheat · plate 종류 선택 | ❌ **불가** (장비 조작) | notes only |
| L3 박리 — plate 온도 · aux fan | ⚠️ **사용자 확인 후에만** | plate-specific 키만. `bed_temperature_initial_layer` 금지 |
| **Studio UI 페인팅** (seam paint / color paint / fuzzy paint) | ❌ **불가** | 기존 규약 유지 — 사용자 작업으로 안내 |

**불가 항목 보고 형식 (notes.md §1.2 + 완료 보고 양쪽):**

```text
⚠️ 이 프로파일로 대응 불가한 항목
- 곡면 계단현상: Variable/Adaptive Layer Height 는 process JSON 범위 밖입니다.
  JSON 으로는 layer_height 0.20 → 0.12 하향으로 대응했고 레이어 수가 약 1.67 배 됩니다.
  더 줄이려면 Bambu Studio UI 에서 Variable Layer Height 를 직접 적용해야 합니다.
```

배수는 **타이핑하지 말고** `기존 layer_height / 새 layer_height` 로 계산해서 적는다.



**Designer-stated Constraint Override Rule (v0.4.0 신규, v0.4.1 범위 좁힘):**

Phase 1.6에서 추출한 `designer_constraints`는 자동화 모드(surface-first 포함)와 형상-기반 자동 결정보다 **명시 필드 한정 상위 우선순위**다. 충돌 시 명시 필드는 디자이너 권장이 이긴다.

### Designer-stated Constraint Override Rule 적용 범위 (v0.4.1 좁힘 정책)

권장 강도 3 카테고리별로 적용 범위가 다르다. 자세한 분류와 예시는 `references/comment-analysis.md` §5 참조.

| 강도 | 예시 (영/중) | 적용 범위 | JSON 처리 |
|------|-------------|----------|----------|
| (1) **strong constraint with explicit value** | "No supports needed" / "并不需要支撑" (값: support=off) | **명시 키로 강제** | `enable_support: "0"` 같이 명시 |
| (2) **directive without explicit field set** | "do not modify profile" / "请不要修改打印配置" | **Creator가 같은 페이지/댓글에서 명시한 필드만 강제**. Creator 미명시 영역은 **자동 결정에 위임 가능** | Creator profile 라벨에 적힌 layer/walls/infill만 강제. ironing/scarf/outer_wall_speed/wall_sequence/seam_position 등 미명시 영역은 자동 결정 |
| (3) **intent / info** | "Push-lock means it must be held down" | JSON 무관 | notes.md §3.2 사용성 참조용 |

**핵심 변경 (v0.4.1):**

- v0.4.0은 (2) directive 권장을 "전체 profile 수정 금지"로 보수 해석 → ironing/scarf 등 표면 마감을 자동 OFF 처리
- v0.4.1은 (2) directive 권장은 **Creator가 같은 댓글/페이지에서 명시한 필드(layer/walls/infill)에만 적용**. Creator가 명시 안 한 ironing/scarf/외벽 매끈 영역은 surface-first 자동 결정에 위임 가능
- 예외: 사용자가 Phase 1.6.5에서 "전체 profile 수정 X 의미"라고 명시 답변 시 [A] 옵션(속도 우선)으로 전환

### 적용 절차

1. **strong constraint with value (강도 1)**: 항상 process JSON 명시 키로 강제 (inherits 위임 금지)
   - `enable_support: "0"`, 디자이너가 명시한 layer/walls/infill 등
   - base preset 기본값이 미래에 변경될 수 있으므로 freeze
   - 디자이너가 특정 소재 지정 시 Phase 2 후보를 그 소재 하나로 좁힘

2. **directive (강도 2)**: Creator 명시 필드만 freeze, 미명시 영역은 Phase 1.6.5 사용자 옵션에 위임
   - Phase 1.6.5 옵션 [C] "디자이너 권장 ∧ surface-first 병행" (default)이 이 케이스 처리
   - Creator 명시 4 필드(layer/walls/infill/support) + surface-first 4 필드(ironing/scarf/outer_speed/wall_sequence) **두 그룹이 같은 process JSON에 공존**

3. **intent / info (강도 3)**: JSON에 직접 반영 안 함. notes.md §3.2 사용성/안전 섹션에 quote.

### 공차 보정 키 적용 정책 (v0.4.2 신규)

Phase 1.7 fit-critical 분석 결과를 process JSON 공차 보정 키로 반영. 자세한 키 dictionary + 소재별 수축률 + 결정 트리는 `references/tolerance.md` 참조.

**Bambu Studio v2.6.0 검증된 공차 키 4개:**

| 키 (정확한 Bambu JSON 이름) | default | 용도 |
|----------------------------|---------|------|
| `elefant_foot_compensation` ⚠️ | `"0"` | 첫 레이어 squish 보정 (오타 "elefant" — "elephant"로 쓰면 silent skip) |
| `xy_hole_compensation` | `"0"` | 홀 직경 보정 (양수 = 더 넓게) |
| `xy_contour_compensation` | `"0"` | 외경 보정 (음수 = 더 좁게) |
| `circle_compensation_manual_offset` | `"0"` | 원형 수동 보정 오프셋 (옵션) |

**카테고리별 공차 키 매트릭스:**

| Fit-critical 카테고리 | Bambu 키 | 권장 보정 |
|---------------------|----------|----------|
| **베어링 외경 압입** (608ZZ 22mm 등) | `xy_hole_compensation` | + (PLA `0.05`, PETG `0.075`, ASA `0.10`) |
| **베어링 내경 축 fit** (608ZZ 8mm 등) | `xy_contour_compensation` | − (PLA `-0.05`, PETG `-0.075`, ASA `-0.10`) |
| **볼트 통과 hole** (M3 → **최종 지름** 3.2-3.4mm, M4 → 4.3mm) | `xy_hole_compensation` | **§1.1 변환식 필수**: 모델이 이미 목표 지름이면 수축 보정만(PLA `+0.05`), 명목 3.0mm 면 오프셋 `+0.10~+0.20`. 표의 지름을 보정값으로 직접 쓰지 마라 (`PL-01`) |
| **heat-set 인서트 hole** (M3 4.0mm 등) | hole 명시 + `xy_hole_compensation` 표 그대로 | 표 §2 |
| **slide-fit / push-lock** (knife sheath 등) | `xy_contour_compensation` (외경) + `xy_hole_compensation` (hole) | 둘 다 loose 권장 |
| **모든 부품 첫 레이어 squish** | `elefant_foot_compensation` | `0.10-0.20` (PLA `0.15` default) |

**소재별 수축률 반영 정책:**

수축률 높은 소재일수록 hole_compensation 값 ↑. `references/materials.md` §4 표 그대로 적용:
- **PLA** (Basic/Matte/Tough+/CF): 0.2-0.3% → `xy_hole +0.05`, `xy_contour -0.05`
- **PETG** (Basic/HF): 0.3-0.5% → `xy_hole +0.075`, `xy_contour -0.075`
- **ASA / ABS**: 0.5-0.8% → `xy_hole +0.10`, `xy_contour -0.10`
- **PC**: 0.6-0.7% → ASA와 동일
- **PAHT-CF / PA6-CF**: 0.4-0.6% → PETG와 동일
- **TPU 90A/95A**: 1.0-1.5% (유연소재) → `xy_hole +0.15`, `xy_contour -0.10`

**디자이너 권장 ([C] 병행 옵션) + 공차 보정 충돌 없음:**

공차 보정 키(`elefant_foot_compensation` / `xy_hole_compensation` / `xy_contour_compensation`)는 Creator profile 라벨에 명시되는 일이 거의 없음 → **Creator 미명시 영역**. v0.4.1 Override Rule 좁힘 정책에 따라 [C] 병행 시 자동 추가 가능. Designer constraint와 충돌하지 않음.

**⚠️ 공차 키가 조용히 무효화되는 3 조건 (소스 검증 — `tolerance.md` §1.2):**

| 조건 | 무효화 | 대응 |
|------|--------|------|
| 오브젝트가 **multi-material / color-paint** 됨 | `xy_hole` · `xy_contour` → 강제 `0` | 공차 보정 불가. **모델 지오메트리로 해결**해야 함을 사용자에게 보고 |
| 오브젝트가 **fuzzy skin paint** 됨 | `xy_hole` · `xy_contour` → 강제 `0` | 동일 |
| **`raft_layers != 0`** | `elefant_foot_compensation` → `0` | 둘을 동시에 지정하지 마라 |

이 스킬은 멀티컬러를 정식 지원하고 dogfood 케이스에 dual-color 가 많다 (box-opener-knife, stealth-press-1s). **fit-critical 부품 + color-paint 조합이면 공차 보정이 전부 무의미**하므로 Phase 1.7 결과 보고 시 반드시 함께 경고하라.

**단일 값 제약:** process JSON 은 `xy_hole_compensation` 을 **1개만** 표현한다. 한 모델에 베어링 압입(빡빡)과 볼트 통과(헐거움)가 공존하면 하나로 둘 다 만족시킬 수 없다 → 가장 fit-critical 한 카테고리 기준으로 잡고, 나머지는 notes.md §1.6 에 "Studio 오브젝트별 오버라이드 필요" 로 명시.

**적용 절차:**

1. Phase 1.7 fit-critical 카테고리 + 카운트 확인
2. Phase 2에서 사용자 선택한 소재의 수축률 확인 (`materials.md` §4)
3. 카테고리별 공차 키 매트릭스 × 소재 수축률 = **오프셋** 도출 → **§1.1 변환식으로 지름 효과(2×) 검산**
4. 위 무효화 3조건 해당 여부 확인 (해당 시 사용자 보고)
5. process JSON에 해당 키들 명시 (default `"0"` 덮어쓰기). `elefant_foot_compensation` 은 **음수 불가**
6. fit-critical 1개 이상이면 Phase 5 fit calibration coupon 자동 트리거

**fit-critical 0건 케이스:**

`elefant_foot_compensation`만 default 0.15 (PLA 안전 마진)로 추가. `xy_hole/xy_contour`는 default `"0"` 유지.


**필수 메타필드 (silent skip 회피 — Codex run `a2a01770a87626167` 검증):**

| 필드 | 값 | 비고 |
|------|----|------|
| `type` | `"process"` 또는 `"filament"` | |
| `name` | `"<모델명> - <변종> 0.12mm"` 등 사용자 인지 가능 이름 | |
| `version` | `"2.6.0.2"` | Semver parseable 필수. 이 값이 현재 v2.6.0과 호환. |
| `from` | `"User"` | **대문자 U** — `"user"` 소문자는 실패 |
| `inherits` | 시스템 프리셋명 정확 일치 | 못 찾으면 silent skip |
| `print_settings_id` / `filament_settings_id` | name과 동일. filament은 **배열 형태** | 빠지면 "Preset type is unknown" |
| `compatible_printers` | `["Bambu Lab H2S 0.4 nozzle"]` | H2S 고정 |

**process JSON 튜닝 정책 (override 대상):**

- ✅ `layer_height`, `initial_layer_print_height` (사용자 요구 반영)
- ✅ `wall_loops`, `sparse_infill_density`, `top/bottom_shell_layers`, `wall_sequence` (모델 형상 기반)
- ✅ `seam_position`, `seam_slope_*`, `scarf_angle_threshold`, `override_filament_scarf_seam_setting` (seam 전략)
- ✅ `outer_wall_speed`, `inner_wall_speed` (소재별)
- ✅ **유량 인접 속도 3 키 — 외벽을 낮췄으면 반드시 함께 낮춘다**: `internal_solid_infill_speed`, `sparse_infill_speed`, `gap_infill_speed`. 이 키를 빼놓고 외벽만 낮추면 유량 계단이 생긴다 (§유량비 게이트)
- ✅ **가속 2 키 — 속도와 같이 설계한다**: `outer_wall_acceleration`, `default_acceleration`. 속도만 내리고 가속을 두면 짧은 세그먼트에서 명령 속도에 도달하지 못한 채 유량만 출렁인다
- ✅ 멀티컬러: `enable_prime_tower`, `prime_tower_width/brim_width/flat_ironing`, `flush_into_*`
- ✅ `enable_support`
- ✅ **(2026-08-13) L3 감지 시**: `brim_type`, `brim_width`, `brim_object_gap` · 조건부 `initial_layer_print_height`, `initial_layer_line_width`, `initial_layer_speed` (`failure-recipes.md` §3.1)
- ⚠️ `raft_layers` — **일반 튜닝 대상이 아니다. L3 최후 수단 게이트 전용** (`1-3`). `raft_layers > 0` 이면 `elefant_foot_compensation` 이 조용히 무효화되므로 fit-critical 부품이 있는 모델에는 켜지 마라 (`tolerance.md` §1.2 · `failure-recipes.md` §3.3)
- ⚠️ `enable_arc_fitting` — **기본값 유지. 표면 품질 튜닝 대상이 아니다.** 품질 개선 기능이 아니라 G-code encoding 변경(직선 → arc 명령)이며 firmware arc segmentation 리스크가 있다. 곡면 계단(Z) 대응 카드로 제시하지 마라 (`failure-recipes.md` §1.2)
- ❌ `adaptive_layer_height` — **넣지 마라.** option 정의 주석 처리 + legacy ignore set (`bambu-fields-baseline.md` §10.1). Phase 4.3 게이트가 잔존을 FAIL 처리한다
- ❌ `bed_temperature`, `bed_temperature_initial_layer` — obsolete/금지. plate 온도가 필요하면 plate-specific 키만 쓰고 **사용자 확인 후에만** (`bambu-fields-baseline.md` §10.3)

### 환경 검증 — 버전 조회 + 프리셋 온전성 (2026-09-05 신규 · Phase 3 진입 전 필수)

references 의 수치는 **설치본에서 읽은 값**이다. 설치본이 낡았거나 프리셋이 손상된 상태면
그 위에서 만든 프로파일도 틀린다. Phase 3 에 들어가기 전에 아래를 실행하고 출력을 응답에 붙여라.

```bash
python3 - <<'ENVPY'
import json, pathlib, plistlib, sys
APP = pathlib.Path("/Applications/BambuStudio.app")
SYS = pathlib.Path.home()/"Library/Application Support/BambuStudio/system"
errs, warns = [], []

app = bundle = None
try:
    app = plistlib.load(open(APP/"Contents/Info.plist","rb"))["CFBundleShortVersionString"]
except Exception as e:
    errs.append(f"앱 버전 조회 실패: {e}")
try:
    bundle = json.loads((SYS/"BBL.json").read_text(encoding="utf-8"))["version"]
except Exception as e:
    errs.append(f"프로파일 번들 버전 조회 실패: {e}")
print(f"앱 버전   : {app}")
print(f"번들 버전 : {bundle}")

SANE = {
    "nozzle_volume":                 (80, 400,  "Bambu Lab H2S 0.4 nozzle"),
    "filament_max_volumetric_speed": (1,  60,   "Bambu PLA Basic @BBL H2S"),
    "filament_retraction_length":    (0,  5,    "Bambu PLA Basic @BBL H2S"),
    "outer_wall_speed":              (1,  1000, "0.16mm High Quality @BBL H2S"),
}
idx = {}
for kind in ("machine","process","filament"):
    d = SYS/"BBL"/kind
    if not d.is_dir():
        errs.append(f"시스템 프로파일 경로 없음: {d}"); continue
    for f in d.glob("*.json"):
        try: j = json.loads(f.read_text(encoding="utf-8"))
        except Exception: continue
        if "name" in j: idx[j["name"]] = j

def resolve(name, depth=0):
    if depth > 12 or name not in idx: return {}
    j = idx[name]
    b = dict(resolve(j.get("inherits"), depth+1)) if j.get("inherits") else {}
    b.update({k:v for k,v in j.items() if k not in ("inherits","name","from","type")})
    return b

for key,(lo,hi,prof) in SANE.items():
    v = resolve(prof).get(key)
    if v is None:
        warns.append(f"{key}: {prof} 에서 못 읽음"); continue
    v0 = v[0] if isinstance(v,list) else v
    try: n = float(v0)
    except (TypeError,ValueError):
        errs.append(f"{key}={v0!r} 숫자 아님"); continue
    ok = lo <= n <= hi
    if not ok: errs.append(f"{key}={n} 이 상식 범위 [{lo},{hi}] 밖 — 손상 프리셋 의심 ({prof})")
    print(f"{'OK ' if ok else '이상'} {key:32} {n:>8}  범위 [{lo},{hi}]")

for w in warns: print(f"[미검증] {w}")
for e in errs:  print(f"FAIL {e}")
print("RESULT:", "FAIL" if errs else "PASS")
sys.exit(1 if errs else 0)
ENVPY
```

**ER-01 — 버전 조회에 실패하면**: 추측값을 쓰지 마라. `[미검증]` 으로 표시하고 references 의
수치를 "확인되지 않은 기준" 으로 명시한 뒤 사용자에게 Studio 설치 상태를 확인받는다.
설치 경로가 다르면 경로를 물어서 다시 조회한다.

**ER-03 — 프리셋 온전성 검사가 FAIL 이면 프로파일 생성을 진행하지 마라.** 어느 키가 어떤 범위를
벗어났는지 그대로 보고하고, Studio 를 최신 stable 로 갱신하거나 프로파일 번들을 다시 받도록
안내한다. `2.8.1.55` ~ `2.8.2.60` 구간에 H2S 프리셋이 손상 배포된 전례가 있다
(`nozzle_volume` 이 `["32","32","32"]`, 정상은 `["145","148"]`). **손상된 부모 위에서 만든 자식
프로파일은 값이 전부 어긋난다.**

⚠️ 앱 버전과 번들 버전은 **따로 움직인다.** Bambu 가 프로파일을 앱과 무관하게 네트워크로
갱신하므로 앱을 안 올려도 번들이 앞서갈 수 있다 (실측: 앱 `02.06.00.51` / 번들 `02.06.00.05`).
references 수치를 판단할 때 기준은 **번들 버전**이다.

**vase 가능 판정 (2026-09-05 신규 · 회전체 seam 정책 1 순위):**

`seam-recipes.md` §0 v4 트리의 (1) 분기다. **`spiral_mode` + `spiral_mode_smooth` 는 회전체에서
seam 을 실제로 없애는 유일한 수단이며 사용자 수작업이 0 이다.** 켜기 전에 아래를 전부 통과해야 한다.

⚠️ **조건을 어긴 레이어는 에러 없이 일반(seam 있는) 출력으로 조용히 폴백한다.** 슬라이서가
경고하지 않으므로 생성 전에 형상을 직접 판정해야 한다 (`GCode.cpp` per-layer 게이트).

1. 플레이트에 **인스턴스 1 개**, 또는 `print_sequence = "by object"` (아니면 슬라이스 에러)
2. **단일 소재 · 단일 region** — modifier mesh 나 per-object 설정 override 가 없다 (아니면 에러)
3. `bottom_shell_layers` 위 **모든 레이어가 닫힌 컨투어 정확히 1 개** — 관통 구멍 · 내벽 · 섬 ·
   분기 · 손잡이가 하나라도 있으면 그 레이어는 탈락한다. Z 사다리로 잘라 루프 수를 세어 판정한다
4. **수평 top 면이 없다** — 내부 선반·턱 포함. fill 이 생기는 region 이 있으면 그 레이어는 탈락
5. **서포트 불필요** — 오버행이 자기지지 범위 안
6. **watertight · manifold · 단일 연결 셸**
7. `skirt_height <= bottom_shell_layers` 이고 draft shield 를 쓰지 않는다

판정이 **불확실하면 켜지 마라.** 조용한 폴백 때문에 "켰는데 안 걸린" 상태가 사용자에게
보이지 않는다. 애매하면 (2) painted 분기를 제안하고 사용자에게 형상 판단을 물어라.

`spiral_mode = 1` 이 강제하는 값과 JSON 작성 형태는 `bambu-fields-baseline.md` §8.4 를 따른다.
spiral 키 3 종은 **스칼라**다 — variant 배열이 아니다.

⚠️ **H2S timelapse 경고 (필수 고지).** H2S 는 `corexy` + 단일 익스트루더라 슬라이서의 timelapse
G-code 주입 조건에서 **spiral vase 예외가 적용되지 않는다** (`!m_spiral_vase` 가드가 I3 분기에만
있다). 그 결과 매 레이어 셔터 pause 가 들어가 **없어야 할 seam 이 생긴다** —
[issue #9166](https://github.com/bambulab/BambuStudio/issues/9166), 2025-12 제보 · **미해결**.

**이것은 프로파일로 고칠 수 없다.** `timelapse_type` 에는 off 값이 없고 spiral 은 그 값이 `0`
이기를 요구한다. 사용자에게 **전송 대화상자의 `타임랩스` 체크 해제**를 반드시 안내하라
(프로세스 설정의 `기타 → 특수 모드 → 타임랩스` 는 모드 선택이지 off 가 아니다).

`[미확인]` 2.8 에서 H2S machine 프로파일에 `farthest_point_timelapse = 1` 이 추가됐고 이 값이
주입 조건에 부정으로 들어간다. 완화됐을 가능성이 있으나 실제 G-code 로 확인되지 않았다 —
확인 전까지는 위 안내를 유지한다.

**유량비 게이트 (2026-09-05 신규 · 외벽 속도를 낮출 때 필수):**

표면 품질을 지배하는 것은 절대 속도가 아니라 **유량 `Q` 와 그 변화율**이다. 외벽만 낮추고 인접
압출을 그대로 두면 "느린 프로파일" 이 아니라 **압력 상태를 흔드는 프로파일**이 된다.

```text
Q = line_width x layer_height x speed x flow_ratio        (mm^3/s)
비율 = max(인접 feature 의 Q) / Q(outer_wall)
```

| 비율 | 판정 | 조치 |
|------|------|------|
| `<= 3x` | 통과 | 그대로 진행 |
| `3x ~ 5x` | 경고 | notes.md 에 비율과 사유를 적고 사용자에게 고지 |
| `> 5x` | **FAIL** | surface-first 적용 실패. 인접 속도를 낮춰 재계산한다. 조용히 통과시키지 마라 |

인접 feature 는 `inner_wall` · `internal_solid_infill` · `sparse_infill` · `gap_infill` 넷이다.
line width 는 feature 별 키(`inner_wall_line_width` 등)를 쓰고, `gap_infill` 은 전용 키가 없으므로
`line_width` 로 폴백한다. `flow_ratio` 는 filament 부모의 `filament_flow_ratio` 를 쓴다.

**권장 착지값은 `surface-recipes.md` §3 표가 정본이다** — 여기에 수치를 복제하지 마라.
H2S 스톡값을 그대로 두면 비율이 5x 를 넘는다.

근거: OrcaSlicer extrusion rate smoothing 문서가 Bambu X1C 에서 200 -> 40 mm/s(5x) 전이만으로
압력 추종 실패 artifact 가 생긴 사례를 든다. Klipper pressure advance 문서는 PA 가 무한 보상이
아니며 고가속 + 고 PA 에서 extruder skip 이 난다고 명시한다.

⚠️ **MVS 여유**: 어느 feature 의 `Q` 도 소재의 `filament_max_volumetric_speed` 의 80 % 를 넘기지
마라. 넘으면 슬라이서가 속도를 클램프하면서 유량이 다시 출렁인다. PLA Basic H2S 는 `25`/`40`,
ABS H2S 는 `20`/`35` mm^3/s (Standard / High Flow).

**filament JSON 튜닝 정책 — `seam-recipes.md`에서 결정된 scarf 필드만 override:**

- ✅ `filament_scarf_seam_type` (none/external/all)
- ✅ `filament_scarf_height`, `filament_scarf_gap`, `filament_scarf_length`
- ❌ **`nozzle_temperature`, `nozzle_temperature_initial_layer` 안 건드림** — 사용자가 .3mf의 creator 튜닝 값이나 base profile 기본값을 유지하길 원함 (사용자 명시 요청 2026-05-16). **L2 스트링잉이 감지돼도 온도를 자동 하향하지 마라** — stringing 은 줄 수 있으나 층간 접착/flow 부족을 만든다
- ❌ fan/cooling 안 건드림 — base에 위임. L3 aux fan 조정은 **notes 안내까지만** (`failure-recipes.md` §3.2)
- ❌ retraction 기본 안 건드림 — base 에 위임. **단 아래 L2 게이트 예외 2 단계만 허용**
- ⚠️ **override 하기 전에 소재 부모 프로파일을 실제로 조회한다.** filament 키의 기준값은 machine 기본이 아니라 **그 소재의 `@BBL H2S` 프로파일이 명시한 값**이다. 조회 절차는 §filament 부모값 조회 참조

**L2 스트링잉 게이트 (2026-09-05 개정 · `failure-recipes.md` §2.1 감별 트리를 따른다):**

건조 여부를 먼저 묻지 마라. **관측 신호로 습기를 지목하거나 배제한 뒤에** 말한다.

| 단계 | 관측 신호 | 판정 · 허용 override |
|------|-----------|---------------------|
| (a) | 압출 중 pop/crackle + 가시 증기, 압출물의 무작위 기포·공극, 결손이 경로와 무관하게 전역 랜덤 | **습기 1 순위.** 건조 후 재출력 권고 + JSON 보류 |
| (b) | 결손이 travel 직후 **선 시작부**에 집중 | 리트랙션 재가압 · PA · seam 축. (1)(2) 로 진행 |
| (c) | **특정 속도 구간**에서만 발생 | MVS 클램프 · 부분 막힘 · 온도 부족. JSON 은 §유량비 게이트로 |
| (d) | **외벽에서만** 나고 인필은 멀쩡, 또는 속도 급변 **경계에서만** | 유량 계단. §유량비 게이트로 |
| (1) | (b) 이고 travel stringing 잔존 | `filament_wipe` = `"1"`, `filament_wipe_distance` = **소재 부모값** — 이 2 키만 |
| (2) | (1) 로도 잔존 | `filament_retraction_length` 를 **소재 부모값의 1.5 배까지만.** Phase 5 coupon 통과 후에만 본 출력 반영 |

**건조 미확인은 진단 중단 사유가 아니다 — confidence cap 이다.** 건조가 검증되지 않았으면
결론에 그 사실을 적고 신뢰도를 낮춰 보고하되, (b)(c)(d) 축의 진단과 JSON 수정은 그대로 진행한다.
고흡습 소재(PA · PVA · TPU · PC · PETG)는 cap 을 더 강하게 둔다.

`materials.md` 기준 25 °C / 55 % RH 포화 흡습률은 PLA Basic 0.43 % · PETG HF 0.40 % · ABS 0.65 % ·
PC 0.25 % 이고 PA 계열이 그보다 한 자릿수 높다. **PLA 와 ABS 를 습기 1 순위로 두려면 (a) 신호가
실제로 관측돼야 한다.**

`filament_retraction_speed` · `filament_retraction_minimum_travel` · `filament_z_hop` ·
`filament_z_hop_types` 는 키 사전으로만 갖는다 (`bambu-fields-baseline.md` §10.2) — 사용자가 명시
요청할 때 정확한 키를 쓰기 위한 것이고 자동 결정 대상이 **아니다**.

**filament 부모값 조회 (override 전 필수):**

`fdm_filament_common` 의 `"nil"` 은 "미설정" 이 아니라 **위임**이다. 그리고 위임된 실효값이 곧
machine 기본인 것도 아니다 — **소재 프로파일이 machine 값을 덮는 경우가 있다.**

```bash
# 소재 부모 프로파일의 실효값을 직접 읽는다. 추측하지 마라.
SYS="$HOME/Library/Application Support/BambuStudio/system/BBL"
python3 -c "
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
for k in sorted(d):
    if 'retract' in k or 'wipe' in k or 'volumetric' in k: print(f'{k:36} {d[k]}')
" "$SYS/filament/Bambu ABS @BBL H2S.json"
```

실측 (Bambu Studio 02.06.00.51): `Bambu ABS @BBL H2S` 와 `Bambu PLA Basic @BBL H2S` 는
`filament_retraction_length` `0.4` · `filament_wipe_distance` `1` 을 명시한다. machine
`Bambu Lab H2S 0.4 nozzle` 의 `0.8` / `2` 와 **다르다.** `bambu-fields-baseline.md` §10.2 의
underlying default 열은 **소재 override 가 없을 때의 값**이므로 그것을 소재값으로 쓰면 안 된다.

조회에 실패하면(시스템 프로파일 경로 없음 등) **추측값을 쓰지 말고** 해당 filament 키를 아예
생략하고 `[미검증]` 으로 보고한다 — 부모에 위임하는 쪽이 틀린 숫자보다 안전하다.

**Surface-first 모드 (적용 여부는 Phase 1.8 Surface Intent Gate 판정을 따른다 — 여기서 다시 추측하지 마라):**

> `references/user-preferences.md` 가 있으면 Phase 1.8 은 그 §1 을 적용하고 **사용자에게 표면 의도를 되묻지 않는다.** 그 파일은 목표(품질 우선)와 제약(시간 무제한)만 갖고 수단(구체 속도값)은 갖지 않는다 — 속도는 `surface-recipes.md` §3 이 소재별로 정한다.

> 이전 판의 "default ON" 표기는 "사용자 요구가 …일 때" 라는 조건과 서로 모순이어서, 실제로는 아무도 켜지 않는 경로가 생겼다 (ironing 누락 회귀). 판정은 **Phase 1.8 단일 지점**에서만 한다.

상세 정책은 `references/surface-recipes.md` 참조. SKILL은 결정 트리 분기와 형상 enumerate만 인라인으로 가진다.

```text
회전체 · 원통 결정 트리 (정본: seam-recipes.md §0 v4 — 여기서 재정의하지 마라)
  │
  ├─ 1. vase 가능?  → spiral_mode = 1 + spiral_mode_smooth = 1
  │                   ★ 유일한 실질적 "해결". 사용자 작업 0.
  │                   판정 체크리스트는 §vase 가능 판정. ⚠️ H2S 는 timelapse 를 끈다
  │
  ├─ 2. 숨길 면·방향 있음 → seam_position: aligned 또는 back
  │                          + Studio seam paint (Enforce/Block) 로 은닉
  │                          + scarf external, 길이는 seam-recipes.md §2.2 상한 준수, gap 0
  │                          사용자 작업: 페인팅 5-10 분 — 사전 고지 필수
  │
  ├─ 3. 360° 노출 (숨길 곳 없음) → aligned/back + 짧은 scarf 로 약한 한 줄 수용
  │                                 또는 CAD seam 은폐 feature · 소재 선택(PLA Matte/CF)
  │
  └─ 4. random → **fallback 전용.** 기능품·텍스처 허용 부품에만.
                 surface-first default 로 쓰지 마라
```

⚠️ **v4 정정 (2026-09-05).** 이전 판은 (2) random 을 default top 에 뒀다. `random` 은 seam 을
없애는 것이 아니라 **한 줄을 표면 전체의 specks 로 바꾸는 것**이며 (Prusa KB), 사용자가 그 결과를
거부했다. "사용자 작업이 없는 옵션이 default" 라는 원칙은 유지되지만 — 그 원칙을 만족하는 최선은
random 이 아니라 **vase** 였다. 소재별 분기는 `seam-recipes.md` §4.

**형상별 결정 트리 (6개 enumerate — surface-recipes.md §2 참조):**

1. **회전체 / 원기둥 / 컵 / 화병** (rotational / cylinder): 위 Auto-select 트리
2. **박스 / 직육면체** (box / rectangular): `seam_position: back` (또는 aligned) + corner painted seam + scarf off 또는 length 5-8mm. random 금지 (평평한 면에 specks 분산 시 외관 ↓)
3. **유기적 곡면 / 피규어** (organic / curved): `seam_position: aligned` (back 우선) + painted seam (주름/접합부/머리카락 텍스처) + scarf external length 10-15mm
4. **얇은 벽 / 미세 디테일** (thin wall): `seam_position: aligned` + scarf length 짧게 (5-10mm) 또는 off. `Contour and Hole` 비추 (내경 치수 영향). `wall_loops` 1-2 + Arachne 검토
5. **평면 top 강조** (flat top — 도구/케이스 lid/박스 top): seam은 후면/코너 + **Top surface 품질이 외벽보다 우선** + ironing 적극 적용 (surface-recipes.md §5)
6. **spiral vase 가능 모델** (spiral mode applicable): 단일 외벽 + top X + infill X + 단일 색상 → `spiral_mode = 1`. 다른 설정 (seam_position, scarf, ironing) 무의미

**Ironing 정책 (surface-recipes.md §5 위임):**

8개 소재 적용 판정 요약 — 자세한 `ironing_type` / `ironing_speed` / `ironing_flow` / `ironing_spacing` / `ironing_inset` 값은 `references/surface-recipes.md` §5.1 매트릭스 참조.

| 소재 | 판정 |
|------|------|
| PLA Basic / PLA Matte | `topmost_only` 적극 권장 |
| PLA Silk | `topmost_only` only — 광택 죽음 주의 |
| PETG HF | 원칙 off, 평면 장식만 `topmost_only` (blob/scar 위험) |
| PA-CF / PAHT-CF | off (fiber 질감, 노즐 마모) |
| PC | off 또는 소형 `topmost_only` 실험 (heat creep / ooze) |
| ABS / ASA | `topmost_only` 실험 가능 (후가공 가능 시 의존 낮춤) |
| TPU | off (불가 — 유연성으로 표면 drag) |

형상별 ironing 적용성: 회전체/spiral vase는 무의미(top 없음), 박스/평면 top은 강함, 유기적 곡면은 부분, 얇은 벽은 거의 off. surface-recipes.md §5.2 참조.

**외벽 표면 공통 (surface-recipes.md §3):**

`layer_height` `0.12` 1 차 / `wall_loops` 3-4 / `wall_sequence` `inner-outer-inner wall` / `reduce_crossing_wall: 1` / PA · flow calibration 전제.
속도는 단일 값이 아니라 **유량비로 결정한다** — outer 만 적는 것은 이 회귀의 원인이었다. §유량비 게이트 + surface-recipes.md §3 표 참조.

⚠️ `resolution` 하향과 `enable_arc_fitting` 끄기는 **surface-first 공통값이 아니다.** 2026-09-05 실측(opus-xero)에서 `resolution 0.008` 은 이득 근거가 없어 baseline 으로 되돌렸고, `enable_arc_fitting` 은 §튜닝 정책이 기본값 유지로 못박고 있다.

⚠️ **PETG HF 안전 경고 — surface-first 모드 적용 시 PETG HF는 AMS HT 65°C 8h 사전 건조 + continuous drying 필수**. 건조 부족 + 낮은 outer speed 조합은 stringing/blob 폭발. seam-recipes.md Finding 4 + surface-recipes.md §6.5 참조.

### Phase 4 — Bundle + notes.md + Verify

#### 4.1 zip 번들 (Bambu Studio Import Configs 호환)

```text
<modelname>.zip
├── process/
│   └── <process name>.json
└── filament/
    ├── <filament 1>.json
    └── <filament 2>.json   (멀티 소재인 경우)
```

#### 4.2 notes.md 5섹션 표준 템플릿 (v0.3.0 신규)

`/Users/jackson/Hub/60_3D Print/Settings/<modelname>/notes.md`에 반드시 5섹션 구조로 작성. Phase 1.5에서 추출한 PDF/영상/GitHub 정보를 통합.

```markdown
# <모델명> — Print Profile + Build Guide

**Source:** <MakerWorld URL>
**Author:** <creator>
**License:** <GPL/CC/etc>
**Generated:** <date>

## 모델 개요
<2-3 sentence: 모델 목적 + 핵심 기능 + 사용 부품 종류>

---

# 1. 필라멘트 요구사항

## 1.0 디자이너 명시 권장사항 (Designer Constraints, v0.4.0 신규, v0.4.1 보강)
- Phase 1.6에서 추출한 designer_constraints 전체 enumerate, 강도별 분류 (strong/directive/intent)
- 각 항목: 원문 quote + 강도 + 적용 위치 (process JSON 키 / Phase 우선순위)
- 댓글 0개 또는 designer_reply 0개면 "디자이너 명시 권장사항 없음 — 자동 결정 모드" 명시
- **선택된 옵션 명시 (v0.4.1 신규)**: Phase 1.6.5에서 사용자가 선택한 옵션 라벨([A]/[B]/[C]/[D]) + 출력 시간 배수(1.2배/1.5배/3배/3.5배) + 적용된 surface 마감 영역 enumerate (ironing/scarf/외벽 매끈 중 켜진 것)
- [C] 병행 옵션 선택 시: Creator 명시 4필드 freeze + surface-first 4필드 추가가 같은 process JSON에 공존함을 명시

## 1.1 추천 소재 (Creator 명시 우선)
| 등급 | 소재 |  ← Designer Constraint > Creator 추천 > 자동 매칭 순으로 우선순위
## 1.2 출력 설정 (Creator 가이드)
| 항목 | 값 |  ← 레이어/벽/인필/패턴/top·bottom. 디자이너 명시 값은 "[Creator 명시 — 수정 X]" 주석
### 1.2.1 실패 모드 대응 + 이 프로파일 범위 밖 항목 (2026-08-13 신규)
- Phase 1.9 판정 결과 (L1/L2/L3 감지 여부 + 근거 quote) — 감지 0 건이면 "실패 모드 신호 없음" 명시
- Phase 3.0 Supportability Split 의 **불가 칸 전부 enumerate** — 특히 L1 Variable/Adaptive Layer Height 는
  "Bambu Studio UI 에서 직접 적용" 을 명시. 조용히 생략 금지
- JSON 으로 대응한 항목 + 부작용 수치 (레이어 수 배수는 `기존/신규` 로 계산해서 적는다)
## 1.3 소재별 사전 준비
- 건조 조건, 챔버 온도, 환기, 베드 처리
## 1.4 파일명 컨벤션
- prefix/suffix 규칙 + accent color
## 1.5 부품별 STL 선택 (해당 시)
- 인두/모터/규격별 분기 STL 안내
## 1.6 공차 보정 적용 영역 (v0.4.2 신규 — fit-critical 부품 있을 때만)
- Phase 1.7에서 식별된 fit-critical 부품 카테고리 enumerate (bearing/bolt/insert/slide-fit + 구체 spec)
- 적용된 공차 보정 키 + 값 표 (`elefant_foot_compensation`, `xy_hole_compensation`, `xy_contour_compensation` 등) — 정확한 Bambu 키 이름 사용 (silent skip 방지)
- 소재별 수축률 근거 1줄
- fit calibration coupon 실행 여부 + 결과 통과/실패

---

# 2. 알리/아마존 부품 리스트

## 2.1 볼트/너트 (링크 + 사이즈 옵션 주의)
| # | 부품 | 규격 | 수량 | 비고 | 알리 |
## 2.2 베어링 + 인서트 (수량 ⚠️ + 사이즈)
> ⚠️ PDF 카운트 vs 웹 BOM 차이 명시
## 2.3 레일/모터/특수 부품 (해당 시)
## 2.4 도구 본체 + 어댑터 (택1 매칭)
## 2.5 추가 소모품 (별도 구입 필요)
- 접착제, RTV, shim, 필라멘트 조각 등
## 2.6 선택 부품 (KEY-BAK 등)
## 2.7 완성 키트 (출력+조립 패스)

---

# 3. 조립 워크플로우 (PDF 매뉴얼 요약)

## 3.0 디자이너 명시 권장/금지 사항 재인용 (v0.4.0 신규)
- §1.0과 중복이지만 조립/출력 직전 reminder 차원에서 재인용
- "No supports needed", "Do not modify the print profile" 등 명시 권장
- 사용자가 출력 직전 마지막으로 확인할 수 있도록 박스 표시
## 3.1 단계 순서
1. ... 14. ... (PDF 매뉴얼에서 추출한 enumerate)
## 3.2 핵심 절차 (인서트 압입 등)
## 3.3 숨은 부품 위치 주의 ⚠️
- "Insert on other side!" 같은 항목 enumerate
## 3.4 결정적 안전 주의사항 🔥
- "Do not over-tighten", "fix A before B" 등 순서 의존성
- 사용자 안전 우려 (user_failure 카테고리에서 추출) — 디자이너 답변과 함께 enumerate
## 3.5 권장 QoL 개선 (선택)

---

# 4. 임포트 + 출력 절차 (Bambu Studio)
1. Import Configs → zip
2. 드롭다운 확인
3. Plate별 process 적용
4. AMS 슬롯 매핑
5. 인두/도구 분기 STL 선택
6. Slice + send

---

# 5. License + Credits

- License 명시
- Special thanks
- 참고 오픈소스
- 영상 빌드 가이드 (URL + transcript 요약)
- 첨부 파일 목록 (PDF, JSON, zip)
```

**구조 원칙:**
- PDF가 없는 케이스: §3은 "Creator 페이지의 조립 가이드" 요약 또는 "조립 매뉴얼 없음 — 사용자 자체 판단" 명시
- 영상이 없는 케이스: §5에서 "영상 가이드 없음" 명시
- §2.5 추가 소모품은 PDF에서 자주 발견되는 항목 — 반드시 cross-check
- **댓글 분석 (v0.4.0)**: §1.0/§3.0의 디자이너 권장사항은 Phase 1.6 추출 결과를 그대로 옮긴다. 빈 권장이면 "댓글 없음 또는 디자이너 권장 없음" 명시 (생략 X).
- **comments-raw.md 아카이브 (v0.4.0)**: `<output_dir>/comments-raw.md`에 댓글 원본 보존. notes.md §5 License + Credits에서 "댓글 분석 출처: comments-raw.md" 명시.

**dogfood 레퍼런스 케이스:** `/Users/jackson/Hub/60_3D Print/Settings/stealth-press-1s/notes.md` 참조. 이번 케이스에서 PDF 분석으로 §2.5 (super glue + shim + 필라멘트 조각), §3.3 (숨은 인서트 5군데), §3.4 (KEY-BAK strain → arm 순서) 모두 발견됨.

#### 4.3 Completion Evidence Gate — 생성물 실제 파싱 검증 (2026-07-27 신규 · 필수)

> **왜 E3 로 올렸나:** silent skip 회귀가 v0.4.0 / v0.4.1 / v0.4.2 에 걸쳐 **3 회 이상 재발**했고, import 실패는 사용자가 뒤늦게 발견하는 신뢰 손상 영역이다. `skill-design-guide.md` §3.7 승급 규칙(3 회 이상 → E2 → **E3 결정론적 게이트**)에 따라, 아래 체크리스트(자기보고)만으로는 부족하고 **LLM 을 호출하지 않는 순수 판정 명령**을 통과해야 한다.

zip 을 만들기 **전에** 생성한 JSON 전부에 대해 아래를 실행하고, **출력 원문을 응답에 붙여라.**

```bash
python3 - <output_dir>/process/*.json <output_dir>/filament/*.json <<'PY'
import sys, json, pathlib
allok=True; unverified=[]

# 시스템 프로파일 인덱스 — 부모 체인 해석용 (유량비 · 부모값 이탈 검사)
SYS = pathlib.Path.home()/"Library/Application Support/BambuStudio/system/BBL"
SYSIDX = {}
if SYS.is_dir():
    for kind in ("process","filament"):
        for q in (SYS/kind).glob("*.json"):
            try: dd = json.loads(q.read_text(encoding="utf-8"))
            except Exception: continue
            if "name" in dd: SYSIDX[dd["name"]] = dd

def resolve(name, depth=0):
    if depth > 12 or name not in SYSIDX: return {}
    dd = SYSIDX[name]
    base = dict(resolve(dd.get("inherits"), depth+1)) if dd.get("inherits") else {}
    base.update({k: v for k, v in dd.items() if k not in ("inherits","name","from","type")})
    return base

def num(v):
    if isinstance(v, list): v = v[0] if v else None
    try: return float(v)
    except (TypeError, ValueError): return None

# 인접 feature: (속도 키, line width 키). gap_infill 은 전용 width 가 없어 line_width 로 폴백한다.
ADJACENT = (("inner_wall_speed","inner_wall_line_width"),
            ("internal_solid_infill_speed","internal_solid_infill_line_width"),
            ("sparse_infill_speed","sparse_infill_line_width"),
            ("gap_infill_speed","line_width"))
# 소재 부모값을 벗어나면 안 되는 filament 키. 상한은 부모값의 1.5 배 (coupon 통과 전제)
GUARDED = ("filament_retraction_length","filament_wipe_distance",
           "filament_retraction_speed","filament_retraction_minimum_travel","filament_z_hop")
for p in sys.argv[1:]:
    f=pathlib.Path(p).name; errs=[]
    try: d=json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAIL {f}: JSON 파싱 실패 {e}"); allok=False; continue
    t=d.get("type")
    if t not in ("process","filament"): errs.append(f"type={t!r} (process|filament 아님)")
    for k in ("name","version","inherits"):
        if not d.get(k): errs.append(f"{k} 누락")
    if d.get("from")!="User": errs.append(f'from={d.get("from")!r} — 반드시 "User" (대문자)')
    idk="print_settings_id" if t=="process" else "filament_settings_id"
    if idk not in d: errs.append(f"{idk} 누락 → 'Preset type is unknown'")
    if t=="filament" and not isinstance(d.get(idk),list): errs.append(f"{idk} 는 배열이어야 함")
    # 금지 키 검사 (2026-08-13 신규 · failure-recipes.md §4) — dict 키 정확 일치, substring 아님
    FORBIDDEN={
        "adaptive_layer_height":"option 정의 주석 처리 + legacy ignore set — layer_height 하향 + notes 로 대응",
        "bed_temperature":"plate-specific 키만 사용 (hot_plate_temp_initial_layer 등)",
        "bed_temperature_initial_layer":"obsolete ignored key — plate-specific 키만 사용",
        "elephant_foot_compensation":"오타 키 (정답: elefant_foot_compensation) — silent skip",
    }
    for bad,why in FORBIDDEN.items():
        if bad in d: errs.append(f"금지 키 {bad}: {why}")
    if t=="process":
        cp=d.get("compatible_printers")
        if not (isinstance(cp,list) and any("H2S" in str(x) for x in cp)):
            errs.append(f"compatible_printers 에 H2S 없음: {cp!r}")
        eff=d.get("elefant_foot_compensation")
        if eff is not None:
            try:
                if float(eff)<0: errs.append(f"elefant_foot_compensation={eff!r} 음수 불가 (min=0)")
            except (TypeError,ValueError):
                errs.append(f"elefant_foot_compensation={eff!r} 숫자 문자열 아님")
            if str(d.get("raft_layers","0")) not in ("0",""):
                errs.append(f"raft_layers={d.get('raft_layers')} 이면 elefant_foot 무효화됨")
    par = resolve(d.get("inherits")) if SYSIDX else {}
    if not SYSIDX:
        unverified.append(f"{f}: 시스템 프로파일 경로 없음 — 유량비/부모값 검사 미실행")
    elif not par:
        unverified.append(f"{f}: 부모 {d.get('inherits')!r} 해석 실패 — 유량비/부모값 검사 미실행")
    elif t=="process":
        # 유량비 게이트 — 동일 filament 이므로 flow_ratio 는 비율에서 상쇄된다
        eff = dict(par); eff.update(d)
        lh = num(eff.get("layer_height"))
        ow = num(eff.get("outer_wall_speed"))
        oww = num(eff.get("outer_wall_line_width")) or num(eff.get("line_width"))
        if lh and ow and oww:
            q_out = oww*lh*ow
            worst, who = 0.0, None
            for sk, wk in ADJACENT:
                sp = num(eff.get(sk)); wd = num(eff.get(wk)) or num(eff.get("line_width"))
                if not (sp and wd): continue
                r = (wd*lh*sp)/q_out
                if r > worst: worst, who = r, sk
            if who:
                if worst > 5.0:
                    errs.append(f"유량비 {worst:.1f}x ({who}) — 5x 초과. 인접 속도를 낮춰라")
                elif worst > 3.0:
                    print(f"WARN {f}: 유량비 {worst:.1f}x ({who}) — 3~5x 경고 구간. notes.md 에 사유를 적어라")
        else:
            unverified.append(f"{f}: layer_height/outer_wall_speed/line_width 결측 — 유량비 미계산")
    # scarf 길이 / 루프 둘레 비율 검사 (2026-09-05 신규 · seam-recipes.md §2.2)
    if t=="process" and str(d.get("seam_slope_type","none"))!="none":
        L=num(d.get("seam_slope_min_length"))
        C=num(d.get("_scarf_loop_circumference_mm"))
        if L is None:
            L=num(par.get("seam_slope_min_length")) if par else None
        if C is None:
            unverified.append(f"{f}: scarf 켜짐인데 _scarf_loop_circumference_mm 미기록 — 길이/둘레 비율 미검증")
        elif L is not None and C>0:
            r=L/C
            if r>0.15:
                errs.append(f"scarf 길이 {L}mm 가 루프 둘레 {C}mm 의 {r*100:.0f}% — 상한 15% 초과 (seam-recipes.md §2.2)")
            elif L<3:
                errs.append(f"scarf 길이 {L}mm 가 하한 3mm 미만 — 끄거나 3mm 이상으로")
    elif t=="filament":
        # 소재 부모값 이탈 검사
        for k in GUARDED:
            if k not in d: continue
            cv, pv = num(d.get(k)), num(par.get(k))
            if pv is None:
                unverified.append(f"{f}: {k} 부모값이 위임(nil) — 이탈 판정 불가")
            elif cv is not None and pv > 0 and cv > pv*1.5:
                errs.append(f"{k}={cv} 가 소재 부모값 {pv} 의 1.5 배 초과 — 부모값을 쓰거나 coupon 근거를 대라")
    for k,v in d.items():
        if isinstance(v,(int,float,bool)): errs.append(f"{k} 가 문자열이 아님 ({v!r})")
    if errs:
        allok=False
        for e in errs: print(f"FAIL {f}: {e}")
    else:
        print(f"OK   {f}: type={t} from={d.get('from')} keys={len(d)} "
              f"ironing={d.get('ironing_type','-')} xy_hole={d.get('xy_hole_compensation','-')} "
              f"layer={d.get('layer_height','-')} brim={d.get('brim_type','-')} "
              f"wipe={d.get('filament_wipe','-')}")
for u in unverified: print(f"[미검증] {u}")
print("RESULT:","PASS" if allok else "FAIL")
sys.exit(0 if allok else 1)
PY
```

**통과 규칙:**

- `RESULT: PASS` **이면서 exit 0** 이어야 다음 단계(zip 번들링 · 완료 보고)로 진행한다. `FAIL` 이면 JSON 을 고치고 재실행하라 — 사용자에게 넘기지 마라.
- **출력이 비어 있으면 PASS 가 아니다.** 파일 glob 이 아무것도 매칭 못 한 것이므로 경로부터 고쳐라 (`skill-design-guide.md` §3.7).
- 위 명령을 실행하지 않았거나 실행할 수 없었다면 완료를 선언하지 말고 `[미검증]` 으로 명시하라. 마커는 `[미검증]` 하나로 통일하며 동의어(`미확인`, `N/A`, `TBD`, `unverified`)를 새로 만들지 않는다 — 정본: `harness/docs/guides/qa-evaluation-guide.md` §Canonical Unverified-Evidence Protocol.

**추가 의미 검증 (스크립트가 못 잡는 항목 — 위 출력값을 눈으로 대조):**

- Phase 1.8 이 **표면 우선**으로 판정했는데 출력의 `ironing=no ironing` 이면 → 게이트 실패, Phase 3 재작업
- Phase 1.7 이 **fit-critical ≥ 1** 인데 출력의 `xy_hole=-` (키 부재) 이면 → 공차 반영 누락
- 오브젝트를 color-paint 할 예정이면 `xy_hole` / `xy_contour` 는 슬라이서가 버린다 (§1.2) — 사용자에게 경고했는지 확인
- **(2026-08-13)** Phase 1.9 가 **L1 감지**인데 출력의 `layer=-` 또는 baseline `0.2` 그대로면 → L1 미대응. 그리고 Phase 3.0 의 "adaptive 는 범위 밖" 보고를 `notes.md` 에 실제로 썼는지 확인 (게이트는 JSON 만 본다)
- **(2026-08-13)** Phase 1.9 가 **L3 감지**인데 출력의 `brim=-` 이면 → L3 미대응
- **(2026-08-13)** Phase 1.9 가 **L2 감지**인데 건조 게이트 (0) 단계를 통과하지 않은 상태에서 `wipe=1` 이면 → 순서 위반. 건조 확인 없이 wipe 를 먼저 켜지 마라 (`failure-recipes.md` §2.1)

#### 4.4 Verify (Import 후 사용자 확인)

생성 후 사용자에게 안내:
1. `File → Import → Import Configs...` → `<modelname>.zip` 선택
2. 좌측 Process/Filament 드롭다운에 새 preset 보이는지 **반드시 확인**
3. 안 보이면 셸로 검증:
   ```bash
   ls "$HOME/Library/Application Support/BambuStudio/user/<userid>/process/"
   ls "$HOME/Library/Application Support/BambuStudio/user/<userid>/filament/"
   ```
   `.json` + `.info` 페어 확인.

### Phase 5 — Coupon Test (v0.3.0 자동 생성)

**자동 트리거 (이전: 사용자 명시 요청 시):**

다음 케이스 중 **하나라도 해당되면 자동으로 coupon process JSON 생성**해서 zip 번들에 함께 포함:

- ☐ 본 출력 예상 시간 > **4시간**
- ☐ 회전체 + seam-critical (surface-first 모드 ON)
- ☐ 새 소재 또는 새 scarf 조합 **첫 시도** (memory에 해당 소재 사용 이력 없음)
- ☐ PETG / PC / PA-CF / ASA-CF / PPS-CF 등 **건조/챔버 민감 소재**
- ☐ Multi-color 5+ filament (멀티컬러 복잡도)
- ☐ **(2026-08-13 신규) Phase 1.9 실패 모드 1 건 이상 감지** — 사후 대응값(layer 하향 / wipe / brim)이 실제로 개선하는지 본 출력 전에 확인. **L2 게이트 (2) 단계(`filament_retraction_length` 상향)는 coupon 통과가 전제 조건**이므로 이 케이스는 skip 불가 (`failure-recipes.md` §2.1)
- ☐ **(v0.4.2 신규) fit-critical 부품 1개 이상** (베어링/볼트/heat-set 인서트/슬라이드 fit) — Phase 1.7에서 식별됨. 본 출력 전 fit calibration coupon (peg-and-hole)으로 공차 검증 필수. standard sizes 권장: **M3 (3.2mm hole / 4.0mm insert)**, **M4 (4.3mm hole / 5.5mm insert)**, **608ZZ (22.10mm OD / 7.90mm shaft)** 등. 자세한 가이드는 `references/tolerance.md` §5 참조

해당 안 되는 단순 케이스는 skip.

**자동 생성 산출물 — zip 번들에 추가:**

```text
<modelname>.zip
├── process/
│   ├── <main process>.json
│   └── <main process> - COUPON.json   ← v0.3.0 자동 추가
├── filament/
│   └── ...
└── coupon-stl/                          ← v0.3.0 자동 추가
    └── README.md                        (cylinder primitive 추가 안내)
```

**coupon process JSON 정책 (lean variant):**

본 process JSON에서 다음만 변경:
- `top_shell_layers`: `"0"` → top 무시 (얇은 쿠폰)
- `bottom_shell_layers`: `"1"` → 첫 레이어 안착만
- `sparse_infill_density`: `"0%"` → 외벽만 평가
- `wall_loops`: 본 process와 동일 (seam/scarf 평가가 목적)
- `seam_*`, `scarf_*`, `wall_sequence`, `outer_wall_speed`: **본 process와 100% 동일** (이게 평가 대상)
- `name`: `"<원본> - COUPON"` 명시
- `print_settings_id`: 동일 패턴 + " - COUPON"

**사용자 안내 (zip + coupon-stl/README.md에 포함):**

```text
COUPON 테스트 절차

1. Bambu Studio에서 빈 plate에 cylinder primitive 추가:
   - Add → Primitive → Cylinder
   - 회전체 모델: 30mm × 30mm × 35mm
   - 박스 모델: 30mm × 30mm × 30mm box
   - 평면 top 모델: 50mm × 50mm × 5mm flat plate
2. Process: "<원본 process> - COUPON" 선택
3. Filament: 본 출력과 동일 슬롯
4. Slice → 출력 (~15-30분 예상)
5. 평가 항목:
   - Seam line 가시성
   - Scarf ramp 매끄러움
   - Stringing 유무 (PETG/PC/ASA 특히)
   - 외벽 광택/표면 균일도
6. 통과 → 본 출력. 실패 → seam_position/scarf_length/외벽 속도 보정 후 재시도.
```

**왜 coupon STL 직접 생성 안 하는가:**

STL 생성은 OpenSCAD/CadQuery 같은 외부 도구 필요. 그 dependency 도입 비용 > Studio primitive 한 번 클릭 비용. 안내만으로 충분.

→ 추후 v0.4+: cylinder.stl + box.stl 사전 출력본 첨부 검토 (BACKLOG).

## Gotcha 체크리스트 (생성 직후 자기 검증)

생성한 JSON이 silent skip 안 되도록 + 디자이너 명시 권장이 반영되도록:

- ☐ `version`이 `"2.6.0.2"` (또는 현재 Bambu Studio 버전 매칭)
- ☐ `from`이 `"User"` (대문자)
- ☐ `print_settings_id` / `filament_settings_id` 존재 (filament은 배열)
- ☐ `inherits`가 시스템 프리셋에 실제 존재 (필요 시 셸로 `ls ~/Library/Application Support/BambuStudio/system/BBL/{process,filament,machine}/ | grep`)
- ☐ `compatible_printers`에 H2S 명시
- ☐ filament JSON의 scarf 필드는 모두 **배열** (`["..."]`)
- ☐ `nozzle_temperature` 등 사용자 영역 필드 안 건드렸는지
- ☐ **(v0.4.0 신규) 디자이너 권장사항이 process JSON에 명시 키로 강제 반영**되었는지 (`enable_support`, `layer_height`, `wall_loops` 등). inherits 위임 X.
- ☐ **(v0.4.0 신규) 디자이너 권장이 notes.md §1.0 + §3.0 두 곳에 모두 인용**되었는지.
- ☐ **(v0.4.0 신규) comments-raw.md가 `<output_dir>/`에 생성**되었는지 (댓글 0개여도 빈 메타블록으로 생성).
- ☐ **(v0.4.0 신규) "do not modify profile" 강 제약이 있으면 surface-first 모드가 자동 적용되지 않았는지** — Phase 1.6.5의 사용자 confirm 결과 반영 확인.
- ☐ **(v0.4.1 신규) [C] 병행 옵션 선택 시 Creator 명시 필드(layer/walls/infill/support) + surface-first 필드(ironing/scarf/outer_speed/wall_sequence) 두 그룹이 같은 process JSON에 모두 명시**되었는지. directive 권장을 전체 freeze로 보수 해석하여 ironing 등 미명시 영역이 빠지지 않았는지 (9mm v2 회귀 재발 방지).
- ☐ **(v0.4.2 신규) fit-critical 부품(베어링/볼트/heat-set 인서트/슬라이드 fit)이 식별됐다면 공차 보정 키가 process JSON에 반영**되었는지. 키 이름 **`elefant_foot_compensation`** (오타 e 빠짐 — `elephant_foot_compensation`은 silent skip). 페리스 휠 608ZZ 회귀 재발 방지.
- ☐ **(v0.4.2 신규) 소재별 수축률 반영** — PLA 보정값을 PETG/ASA에 그대로 쓰지 않았는지. `xy_hole_compensation` 값이 소재 수축률에 비례하는지 (PLA `+0.05` < PETG `+0.075` < ASA `+0.10`).
- ☐ **(2026-07-27 신규) 공차 보정값을 지름이 아닌 오프셋으로 넣었는지** — `보정값 = (목표지름 − 모델지름) / 2`. `tolerance.md` §4 의 "최종 지름"(예: 3.2mm, 22.10mm)을 보정값 칸에 그대로 복사하지 않았는지. **`PL-01` 재발 방지.**
- ☐ **(2026-07-27 신규) 공차 무효화 3조건 확인** — 오브젝트가 multi-material color-paint 또는 fuzzy-skin paint 되면 `xy_hole`/`xy_contour` 가 **강제 0**, `raft_layers != 0` 이면 `elefant_foot_compensation` 이 **무효**. 해당하면 사용자에게 보고했는지 (`tolerance.md` §1.2).
- ☐ **(2026-07-27 신규) Phase 1.8 Surface Intent Gate 통과** — 표면 우선 판정인데 `ironing_type` 이 `"no ironing"` 으로 남아있지 않은지. 기능 우선 판정이면 notes.md 에 "표면 마감 미적용" 을 명시했는지 (조용히 생략 금지).
- ☐ **(2026-07-27 신규) Phase 4.3 검증 명령을 실제로 실행하고 출력을 응답에 붙였는지** — 체크리스트를 눈으로 훑은 것은 실행이 아니다. `RESULT: PASS` + exit 0 없이 완료 선언 금지.
- ☐ **(2026-07-27 신규) 로컬 모델 형상을 태그 매칭이 아닌 XML 파서로 추출했는지** — `sed`/`grep` 태그 범위 매칭 금지, 지오메트리가 `3D/Objects/*.model` 에 있을 수 있음, **빈 출력은 PASS 아님** (Phase 1.0).
- ☐ **(2026-08-13 신규) Phase 1.9 Failure-Mode Gate 통과** — L1/L2/L3 3 종을 각각 감지/없음으로 판정 보고했는지. 감지 0 건이면 "실패 모드 신호 없음" 을 명시했는지 (조용히 skip 금지). grep 매치를 **문장을 읽어** 확인했는지 (`실`·`1층` substring 오탐).
- ☐ **(2026-08-13 신규) 금지 키 4 종이 생성 JSON 에 0 건인지** — `adaptive_layer_height`, `bed_temperature`, `bed_temperature_initial_layer`, `elephant_foot_compensation`. Phase 4.3 게이트가 dict 키 정확 일치로 검사한다.
- ☐ **(2026-08-13 신규) Phase 3.0 Supportability Split 의 불가 항목을 notes.md §1.2.1 에 명시 보고했는지** — 특히 L1 adaptive layer height. 근사 구현으로 조용히 때우지 않았는지.
- ☐ **(2026-08-13 신규) L2 대응이 게이트 순서를 지켰는지** — 건조 확인 (0) → `filament_wipe` (1) → coupon 후 `filament_retraction_length` (2). 온도/fan 을 자동으로 건드리지 않았는지.
- ☐ **(2026-08-13 신규) `raft_layers` 를 켰다면 fit-critical 0 건인지** — raft 는 `elefant_foot_compensation` 을 조용히 무효화한다. L3 최후 수단 외에는 켜지 않았는지.
- ☐ **(2026-08-13 신규) 사용자 실측 실패 보고에 반박하지 않았는지** — `skill-design-guide.md` §3.8. 상태를 `REOPENED` 로 두고 재현 6 축(`failure-recipes.md` §0)을 먼저 대조했는지.

## MakerWorld URL fallback 체인 (2026-05-16 갱신)

1. **Playwright MCP** (1차, 권장) — `mcp__playwright__browser_navigate` + `mcp__playwright__browser_snapshot` 조합. JS 렌더링 페이지 정상 처리, Cloudflare bot challenge 우회. 이미지 캡처가 필요하면 `mcp__playwright__browser_take_screenshot` 추가. **개인 환경에 Playwright MCP가 설치되어 있을 때 가장 정확**.
2. **`codex-rescue` 에이전트** (Playwright 미설치 환경) — research mode 위임. Codex 측 캐시/웹검색 결과 활용 가능. 단 MakerWorld 본문은 못 가져올 수 있음 (캐시된 페이지 또는 우회 정보만).
3. **WebFetch** (마지막 대안) — 보통 Cloudflare 차단으로 실패. 트래픽 패턴이 가벼운 시간대에만 간헐적 성공.
4. **사용자 직접 입력** — 위 모두 실패 시 "이 모델 어떤 부품 구성이고 어떤 소재 권장돼?" 질문으로 핵심 정보만 받기.

> ⚠️ **WebFetch만 단독 시도 금지** — Cloudflare 차단이 default이므로 무한 retry 시 토큰 낭비. 1번부터 4번 순서로 시도하고 명시적으로 fallback 보고.

## v2 백로그 (수동으로 진행)

플러그인 내 `bambu-kit/skills/bambu-print-profile/BACKLOG.md` 참조. 핵심:
- 홈서버 Linux에 print outcome capture daemon (MQTT + FTPS + JSONL)
- 카이젠 스킬은 이 레포의 `.claude/skills/bambu-research` + `.claude/skills/bambu-kaizen`에 분리됨 (자동 주기 폴링 + SKILL 격차 분석). bambu-kit 플러그인에는 포함되지 않는다.
- 실측 피드백을 references에 자동 환류 (v1은 손으로 함)

## 매 실행 시 필수 사전 절차 (v0.3.0 강화)

스킬 시작 즉시 아래 3개를 **반드시** 실행. 건너뛰면 schema mismatch / silent skip 위험.

### 1. Bambu Studio 버전 cross-check

```bash
defaults read /Applications/BambuStudio.app/Contents/Info.plist CFBundleShortVersionString
```

| 결과 | 처리 |
|------|------|
| `02.06.00.xx` (references baseline · 2026-07-27 기준 로컬 설치본) | references 그대로 사용. 정상. |
| `02.06.01.xx` (1패치 위) | references 그대로 — 마이너 패치는 호환 가능성 높음. 단, scarf 필드 mismatch 의심되면 cross-check. |
| `02.07.x.xx` / `02.08.x.xx` | ⚠️ **bambu-kaizen 트리거 권장** — references 는 `02.06.00.51` 기준이라 fields baseline 갱신이 필요할 수 있음. 사용자에게 보고 후 진행. |
| `02.09.x.xx` 이상 (미확인 신버전) | ⚠️ **`/bambu-research` 먼저** — 스키마 변경 가능성. 확인 없이 생성 금지. |
| `02.05.x.xx` 이하 (구버전) | ⚠️ JSON `"version": "2.6.0.2"`이 reject될 수 있음. 사용자에게 업그레이드 권장. |
| 명령 실패 (`not installed`) | Studio 미설치. JSON은 만들되 import 검증 셸 명령 부분 skip. |

> **릴리스 현황 (2026-07-27 조회):** 최신은 **2.8.1** (`v02.08.01.55`, 2026-07-14 · Public Beta), 최신 정식 릴리스는 **2.7.1** (`v02.07.01.62`, 2026-06-16). 로컬 설치본은 `02.06.00.51` 로 references baseline 과 일치한다. 출처: <https://api.github.com/repos/bambulab/BambuStudio/releases>. references 를 2.7/2.8 기준으로 올리는 것은 `/bambu-research` 소관이다.

### 2. Memory 자동 로드

다음 3개 파일을 Read로 자동 로드 (사용자 명시 요청 없어도):
- `~/.claude/projects/-Users-jackson/memory/3d_printing_setup.md` — 하드웨어 환경 (H2S + AMS 구성, 노즐)
- `~/.claude/projects/-Users-jackson/memory/bambu_studio_json_import.md` — silent skip 회피 4개 필수 필드
- `~/.claude/projects/-Users-jackson/memory/bambu_print_profile_skill.md` — v1 학습 환류 (회전체 random > aligned 등)

### 3. 시스템 base 프리셋 존재 확인

생성할 `inherits` 값이 실제 파일로 존재하는지 사전 확인:

```bash
ls ~/Library/Application\ Support/BambuStudio/system/BBL/process/ | grep -i "h2s\|0.20mm"
ls ~/Library/Application\ Support/BambuStudio/system/BBL/filament/ | grep -i "<material>"
```

이 확인 없이 JSON 생성하면 inherits 매칭 실패로 silent skip 위험. 매번 셸로 검증.

## 검증된 실측 사례

| 모델 | 소재 | 결과 |
|------|------|------|
| Box opener knife (583712) | PLA Basic dual-color | ✅ 정상 출력 검증. 회전체 손잡이 seam은 random + external 처리 |
| H2D Vent Pipe (1441653) | PETG HF + TPU 90A | ⚠️ stringing 발생 (필라멘트 건조 부족 의심). seam은 random + external + entire_loop |
| Stealth Press 1S (825644) | ASA dual-color | ✅ PDF/영상 통합 분석 워크플로우 dogfood. 5섹션 notes.md 표준 템플릿 확립. 웹 BOM 30개 vs PDF 매뉴얼 카운트 34개 mismatch 발견 → Phase 1.5 신규. |
| 9mm Craft Knife Elite (1517485) | PLA Basic | ⚠️ v0.3.0 회귀: 디자이너 명시 "No supports needed, please do not modify the print profile"을 무시하고 surface-first 자동 적용. → v0.4.0 Phase 1.6 + Designer Constraint Override Rule 신규. v0.4.1 dogfood: directive 권장을 보수 해석하여 ironing/scarf 빠진 [A] 결과 → 사용자 의도("모든 면 매끈") 미반영. → v0.4.1 범위 좁힘 정책 + [C] 병행 옵션 default. v0.4.2 dogfood: blade slide-fit 공차 누락 식별 → Phase 1.7 + `elefant_foot_compensation` 추가. |
| Shower-box 부품 + Holster (2026-06~08 · 5 세션) | 미기록 | ⚠️ **실측 3 종 실패 반복 — "partially successful".** 곡면 계단현상 · voronoi stringing · 바닥 박리가 재출력마다 새로 노출됐고, 그 신호가 다음 프로파일 생성으로 **들어오는 경로가 없었다** (Phase 1.6 은 남의 댓글만 본다). → 2026-08-13 Phase 1.9 Failure-Mode Detector + Phase 3.0 Supportability Split + `failure-recipes.md` 신규. 출처: `/insights` 2026-08-13 (윈도 2026-06-12~08-12). 소재/plate/건조 상태는 리포트에 미기록이라 `[미확인]` — 재현 6 축 대조가 다음 케이스의 첫 단계다 |
| Ferris Wheel (1186414, 608ZZ variant) | PLA Basic | ⚠️ v0.4.x 이전 회귀: 608ZZ 베어링 외경(22mm)/내경(8mm) fit 안 맞음 (사용자 보고 2026-05-27). → v0.4.2 Phase 1.7 fit-critical 분석 + tolerance.md §3.1 bearing 결정 트리 신규. **2026-07-27 정정**: v0.4.2 가 넣은 `+0.075`/`-0.075` 는 2× 규칙상 22.15mm/7.85mm 로 목표(22.10/7.90) 초과 — 축 fit 에 0.10mm 유격이 생겨 사용자 보고와 일치. 정정값 `+0.05`/`-0.05` (tolerance.md §7). 재출력 검증 대기. |

`/Users/jackson/Hub/60_3D Print/Settings/<modelname>/notes.md`에 케이스별 detail 보존.

## 회귀 호환성 (v0.4.0)

기존 검증 케이스(box-opener-knife, h2d-vent-pipe, stealth-press-1s)는 v0.4.0 워크플로우 재실행 시 designer_constraints가 빈 배열로 graceful fallback되어 기존 결과와 동일하게 동작한다. comments-raw.md 아카이브가 신규로 생성되지만 process/filament JSON 결정은 영향 받지 않는다.

## 출처

- 4개 Codex research run으로 references 빌드 (`a5afcf864d05cf3b7`, `aeb457c7603a420db`, `afcf4968339021b29`, `ab679b7fbc81fa7b6`)
- 추가 검증: `aab7cad186e9523af` (멀티컬러 필드), `a2a01770a87626167` (JSON import gate), `a06a8ac153247d901` (wipe_on_loops Bambu 부재 확인)
- 실측 피드백: 2026-05-15 ~ 2026-05-19 박스 오프너 + vent pipe + Stealth Press 1S 테스트
- v0.3.0 dogfood: 2026-05-19 Stealth Press 1S — PDF 23p / 영상 / GitHub 첨부 자료 분석 누락 → Phase 1.5 신규 + notes.md 5섹션 표준화 + 버전 cross-check 필수화 + Phase 5 coupon 자동 생성
- v0.4.0 dogfood: 2026-05-23 9mm Craft Knife Elite — 디자이너 댓글 "No supports needed, please do not modify the print profile" 무시한 회귀 → Phase 1.6 (Comment Analysis) 신규 + Designer Constraint Override Rule + comments-raw.md 아카이브 + 전체 크롤링 강화 (다국어/페이지네이션/스크롤) + Phase 3 디자이너 권장 명시 키 강제 + notes.md §1.0/§3.0 디자이너 권장 섹션 + Gotcha 4개 신규
- v0.4.1 dogfood: 2026-05-27 9mm Craft Knife Elite v2 — directive 권장 "do not modify profile"을 전체 profile 수정 금지로 보수 해석한 회귀 (ironing 누락) → Phase 3 Override Rule 적용 범위 좁힘 (Creator 명시 필드만 freeze, 미명시 영역은 자동 결정 위임) + Phase 1.6.5 4-옵션 재설계 (속도 / top만 / 병행 default / 풀) + comment-analysis.md §5 권장 강도별 적용 범위 (strong with value / directive / intent) + Gotcha 1개 신규
- v0.4.2 dogfood: 2026-05-27 페리스 휠 (1186414, 608ZZ variant) 베어링 fit 안 맞은 사용자 보고 + 9mm sheath blade slide-fit 가능성 → Phase 1.7 (Tolerance & Fit Analysis) 신규 + Phase 3 공차 보정 키 정책 (`elefant_foot_compensation` 오타 발견 — Bambu 의도적) + Phase 5 fit calibration coupon 자동 트리거 + references/tolerance.md 신규 (4 섹션: Bambu 키 / 소재 수축률 / fit-critical 결정 트리 / coupon) + materials.md §4 수축률 컬럼 14 소재 보강 + Gotcha 2개 신규
- 2026-08-13 카이젠 Phase 13: 근거 파일 `.harness/.meta/evidence/phase13.md` (Codex foreground · read-only · 외부 조회 0 회). 슬라이서 소스 기준 키/기본값 확정 → `references/failure-recipes.md` 신규 + `bambu-fields-baseline.md` §10 신규 + Phase 1.9 / 3.0 신규 + Phase 4.3 금지 키 검사 확장. 사실 정정 3 건: `layer_height 0.08` 의 공식 프로파일 근거 부재(`[미확인]`) · `enable_arc_fitting` 은 품질 기능이 아니라 G-code encoding 변경 · `resolution` 은 XY 전용이며 Z 계단 해결책이 아님. 소스: <https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp>
- 전체 로그: `~/.claude/codex-research-log/2026-05.md`
