# Kaizen Data Sources (주 1회 갱신용)

> Last updated: 2026-05-15
> Source: Codex research run `ab679b7fbc81fa7b6` (score 24/25)

`bambu-print-profile-kaizen` 스킬이 주 1회 cron으로 돌면서 references/ 3개 문서(`bambu-fields-baseline.md`, `materials.md`, `seam-recipes.md`)를 갱신할 때 폴링할 데이터 소스 매핑.

전략: 공식 피드/API를 1차로 잡고, 빠른 현장 신호는 Reddit/Discourse/YouTube로 보강.

## 1. 카테고리별 소스

### A. Bambu Studio 새 버전 릴리스

| 소스 | URL / endpoint | 폴링 가능성 | 추천 주기 | 비고 |
|------|---------------|------------|----------|------|
| **GitHub Releases** | https://github.com/bambulab/BambuStudio/releases<br>Atom: `.../releases.atom`<br>JSON: `https://api.github.com/repos/bambulab/BambuStudio/releases` | JSON / Atom | 일 1회 | 공식 릴리스 1순위. unauth 60/h |
| GitHub tags | `https://api.github.com/repos/bambulab/BambuStudio/tags` | JSON | 주 1회 | prerelease/tag 보조. 노이즈 ↑ |
| Wiki changelog | https://wiki.bambulab.com/en/software/bambu-studio/release/ | RSS 미확인, 스크래핑 필요 | 주 1회 | GitHub 릴리스가 "full notes are on Wiki"로 안내하는 경우 있음 |
| Bambu Blog | https://blog.bambulab.com/<br>RSS 후보: `/rss/` | Ghost 기반 | 주 1회 | 공식 발표/제품. Studio patch 누락 가능 |
| Software forum | https://forum.bambulab.com/c/bambu-lab-software/7<br>RSS: `/c/bambu-lab-software/7.rss`, JSON: `.json` | Discourse | 주 1회 | 릴리스 후 회귀/다운로드 문제 빠르게 포착 |

### B. Bambu Lab 신소재 출시 / 단종

| 소스 | URL / endpoint | 폴링 | 추천 주기 | 비고 |
|------|---------------|-----|----------|------|
| **공식 스토어 filament collection** | https://us.store.bambulab.com/collections/bambu-lab-3d-printer-filament<br>Atom: `.atom`, JSON: `/products.json?limit=250` | Shopify HTML/Atom/JSON | 주 1회 | 신제품/단종/가격/품절 1순위. 지역별 분리 |
| PLA collection 예시 | https://us.store.bambulab.com/collections/pla | Shopify | 주 1회 | 카테고리별 신규 SKU. 재고 노이즈 ↑ |
| Filament Guide PDF | https://cdn1.bambulab.com/filament/filament-guide/241213/filament-guide-us.pdf | PDF 해시 비교 | 월 1회 | 공식 라인업/조건 변화. 정확도 ↑ |
| Filament forum | https://forum.bambulab.com/c/bambu-filament-and-accesories/9<br>RSS: `/c/bambu-filament-and-accesories/9.rss` | Discourse | 주 1회 | 실사용 신호 빠름. 노이즈 ↑ |
| Blog company-news | https://blog.bambulab.com/tag/company-news/<br>RSS 후보: `.../rss/` | HTML/RSS | 주 1회 | EOL/제품 발표 강함. SKU는 놓칠 수 있음 |
| bbltracker | https://bbltracker.com/ | 사이트 + 공개 DuckDB 언급 (URL 재확인 필요) | 주/일 | 비공식. 2차 소스로 |

### C. MakerWorld 트렌드 / 인기 모델

| 소스 | URL / endpoint | 폴링 | 추천 주기 | 비고 |
|------|---------------|-----|----------|------|
| Search trending | https://makerworld.com/en/search/models | RSS/API 미확인, 스크래핑 | 주 1회 | Trending/Boosts/Newest/Downloads/Likes 정렬. DOM 변경 리스크 |
| Categories trending | https://makerworld.com/en/models/categories?categories=1 | 스크래핑 | 주 1회 | 트렌드 포착 적합. AI/스팸 노이즈 |
| Bambu Forum MakerWorld | https://forum.bambulab.com/c/makerworld/144<br>RSS: `.../144.rss` | Discourse | 주 1회 | 정책/저작권/랭킹 변화. 모델 자체보단 플랫폼 변화 감지 |
| Makrs aggregator | https://makrs.co/ | HTML 스크래핑 | 주 1회 | 다중 플랫폼 집계. 정확성 검증 필요 |

### D. H2S / AMS HT / AMS 2 Pro 검증 findings

| 소스 | URL / endpoint | 폴링 | 추천 주기 | 비고 |
|------|---------------|-----|----------|------|
| **AMS forum** | https://forum.bambulab.com/c/bambu-lab-ams/6<br>RSS: `/c/bambu-lab-ams/6.rss` | Discourse | 주 1회 | AMS HT/AMS 2 Pro 실사용 문제·해결 |
| **H2S forum** | https://forum.bambulab.com/c/bambu-lab-h2-series/bambu-lab-h2s/175<br>RSS: `.../175.rss` | Discourse | 주 1회 | H2S 전용. 구조화된 사례 |
| Reddit r/BambuLab top | `https://www.reddit.com/r/BambuLab/top/.rss?t=week`<br>JSON: `.json?t=week` | RSS/JSON | 주 1회 | 빠른 집단 신호. UA 지정 + 백오프 필요 |
| Reddit search | `.../r/BambuLab/search.rss?q="AMS HT" OR "AMS 2 Pro" OR H2S&restrict_sr=1&sort=new` | RSS (안정성 ↓) | 주 1회 | 키워드 타깃. 노이즈 ↑ |
| AMS HT 공식 PDF | https://cdn1.bambulab.com/documentation/h2d/en/AMS_HT_20250109.pdf | 해시 비교 | 월 1회 | 공식 호환/온도/절차 |
| Bambu YouTube | `https://www.youtube.com/feeds/videos.xml?channel_id=UCDF3Sd2LNAsa-nKD17Jq3mw` | RSS | 주 1회 | 공식 발표 |
| Maker's Muse | `.../channel_id=UCxQbYGpbdrh-b2ND-AfIybg` | RSS | 주 1회 | 검증 채널 |
| Teaching Tech | `.../channel_id=UCbgBDBrwsikmtoLqtpc59Bw` | RSS | 주 1회 | slicer/print quality 검증 강함 |

### E. Scarf seam / 신규 slicer 기능

| 소스 | URL / endpoint | 폴링 | 추천 주기 | 비고 |
|------|---------------|-----|----------|------|
| **GitHub issues search** | `https://api.github.com/search/issues?q=repo:bambulab/BambuStudio+"scarf+seam"` | JSON, 60/h | 주 1회 | 버그/회귀/설정 변화 가장 빠름 |
| Studio forum | https://forum.bambulab.com/c/bambu-lab-software/bambu-studio/8<br>RSS: `.../8.rss` | Discourse | 주 1회 | 실제 출력 결과 + 설정 조합 |
| OrcaSlicer seam wiki | https://github.com/OrcaSlicer/OrcaSlicer/wiki/quality_settings_seam | HTML 스크래핑 | 주 1회 | scarf 패턴은 Orca에서 먼저 정리되는 경우 多 |
| OrcaSlicer discussions | https://github.com/SoftFever/OrcaSlicer/discussions/4325 | HTML/일부 API | 월 1회 | deep-dive 토론. 노이즈 ↑ |
| Reddit scarf search | `.../r/BambuLab/search.rss?q="scarf seam"&restrict_sr=1&sort=new` | RSS (안정성 ↓) | 주 1회 | "PETG에서 된다/안 된다" 같은 현장 신호 |

## 2. 주 1회 cron 우선순위 Top 10

가성비 기준 (유지보수 비용 vs 신호 정확도):

1. `https://api.github.com/repos/bambulab/BambuStudio/releases` — JSON. **공식 Studio 릴리스 1순위**. 60/h 충분.
2. `https://api.github.com/search/issues?q=repo:bambulab/BambuStudio+scarf+seam+OR+slicer+updated:>=YYYY-MM-DD` — JSON. 신규 기능/회귀 감지. ETag 권장.
3. `https://blog.bambulab.com/rss/` — RSS 후보. 제품/EOL/정책. 첫 cron에서 200/XML 검증.
4. `https://forum.bambulab.com/c/bambu-lab-software/bambu-studio/8.rss` — Discourse. 릴리스 후 실사용 회귀.
5. `https://forum.bambulab.com/c/bambu-lab-ams/6.rss` — Discourse. AMS HT/AMS 2 Pro 패턴.
6. `https://forum.bambulab.com/c/bambu-lab-h2-series/bambu-lab-h2s/175.rss` — Discourse. H2S 실사용.
7. `https://us.store.bambulab.com/collections/bambu-lab-3d-printer-filament` — Shopify JSON. 신소재/단종/이름 변화. 실패 시 collection HTML/Atom fallback.
8. `https://www.reddit.com/r/BambuLab/top/.rss?t=week` — RSS. 상위 신호만 (노이즈 억제).
9. `https://makerworld.com/en/search/models` 또는 `.../categories?categories=1` — 스크래핑. trending 캡처. API 확인 전까지 낮은 빈도.
10. `https://github.com/OrcaSlicer/OrcaSlicer/wiki/quality_settings_seam` — HTML 스크래핑. scarf best practice 진화.

## 3. 주기 / 정확성 / Rate limit 트레이드오프

- **주 1회 cron**: 공식 릴리스/문서/포럼 요약에는 충분. 스토어 재고나 신규 SKU는 놓칠 수 있음.
  - "신소재 출시"만 보면 주 1회
  - "재고/단종 조짐"까지 보면 일 1회

- **정확성 순서**: GitHub releases > Bambu Blog/Wiki/PDF > Discourse forum > Reddit/YouTube > MakerWorld scraping/aggregator

- **Reddit/YouTube**: 빠르지만 references 갱신에는 "반복 출현 + 공식 문서/포럼 교차확인" 조건 권장.

- **GitHub rate limit**: unauth REST 60/h — 본 용도엔 충분. 단 `ETag`, `If-None-Match`, `since`/`updated:>=` 쿼리로 변동분만 가져오는 편 권장.
  - 출처: https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api

- **Reddit RSS**: 공개 RSS 가능하나 최근 403/제한 사례. User-Agent 지정 + 요청 간격 완화 + 실패 시 JSON/API 또는 수동 fallback 필요.

- **MakerWorld**: 공식 RSS/API 미확인. 스크래핑은 정렬 파라미터/렌더링 구조 변경 시 깨질 수 있음. **kaizen reference 핵심 소스보다는 "트렌드 후보 수집"으로 제한**.

## 4. 미해결 / 검증 필요

1. **Bambu Blog RSS** — Ghost 기반이라 `/rss/` 가능성 높지만 첫 자동화에서 실제 XML 응답 검증 필요.
2. **Bambu Store Shopify endpoint** — 지역 스토어별 노출/차단 다를 수 있음. US/EU/JP/KR 중 기준 지역 결정 필요.
3. **MakerWorld** — 공개 API/RSS 미확인. 스크래핑 또는 비공식 reverse-engineered endpoint 의존. 장기 자동화 안정성 ↓.
4. **Discord 채널** — 빠른 신호 ↑, 공개 RSS/API ✗, 권한/초대/검색 문제. 자동 reference 갱신 소스로 비추천. 수동 검증 채널로.
