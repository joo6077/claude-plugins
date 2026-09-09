# amend_direction 픽스처

`harness/references/contract-schema.md` §Amendment 사이드카 의 두 헬퍼를 실행으로 검증하는 입력이다.
서술 존재는 증거가 아니다 — 아래를 zsh·bash 양쪽에서 돌려 출력을 대조한다.

| 파일 | 무엇 | 기대 |
| --- | --- | --- |
| `measured-orig.txt` / `measured-amended.txt` | howto-kit A-01 실측 **측정 집합** — `git diff --name-only 4fb1382..37d50a7` (제외 2 pathspec) 와 `54fb3b3..37d50a7`. 39 → 37 경로 | `amend_direction_oracle` → `relaxing measured_removed=2 measured_added=0` |
| 같은 두 파일 | 허용 집합 헬퍼에 잘못 넣으면 | `amend_direction` → `narrowing added=0 removed=2` — **오라벨** (음성 대조) |
| `allow-3.txt` / `allow-5.txt` | 스키마 본문의 실측 위반 사례, **허용 집합** 3 → 5 | `amend_direction` → `relaxing added=2 removed=0` (회귀 기준) |
| `empty.txt` | 빈 입력 | `amend_direction_oracle` → `unknown measured_removed=0 measured_added=0` |
| (존재하지 않는 경로) | 결측 입력 | `amend_direction_oracle` → `unknown missing_input=<경로>`, stderr 없음 |

헬퍼는 스키마 코드 펜스에서 추출한다:

```bash
awk '/^amend_direction\(\) \{/{p=1} p{print} p&&/^\}$/{exit}'        harness/references/contract-schema.md >  /tmp/helper.sh
awk '/^amend_direction_oracle\(\) \{/{p=1} p{print} p&&/^\}$/{exit}' harness/references/contract-schema.md >> /tmp/helper.sh
bash -c '. /tmp/helper.sh; amend_direction_oracle harness/evals/amend-direction/measured-orig.txt harness/evals/amend-direction/measured-amended.txt'
```
