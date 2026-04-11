---
created: 2026-04-11
tool: scripts/validate-plugin.py
scope: 7개 킷 전체 (harness, flutter-toolkit, design-kit, backend-kit, infra-kit, rust-kit, react-kit)
status: 기록만 — 이 세션에서 fix 하지 않음
---

# 플러그인 검증 발견 사항 (2026-04-11)

`python3 scripts/validate-plugin.py` 첫 실행 결과 요약.
가이드: `harness/docs/guides/plugin-validation-guide.md`

---

## 전체 요약

| 킷 | V1 | V2 | V3 | V4 | V5 | V6 | V7 | 판정 |
|----|----|----|----|----|----|----|-----|------|
| harness | OK | OK | OK | WARN | FAIL | FAIL | OK | ERROR |
| flutter-toolkit | FAIL | SKIP | OK | WARN | OK | FAIL | OK | ERROR |
| design-kit | OK | SKIP | OK | OK | OK | FAIL | OK | ERROR |
| backend-kit | OK | SKIP | OK | OK | OK | OK | OK | **OK** |
| infra-kit | OK | SKIP | OK | OK | OK | FAIL | OK | ERROR |
| rust-kit | OK | SKIP | OK | WARN | FAIL | FAIL | OK | ERROR |
| react-kit | OK | OK | OK | WARN | OK | FAIL | OK | ERROR |

- **총 이슈**: 6개 킷 ERROR, 1개 킷 OK (backend-kit)
- **V6 code-fence**: 전 킷 공통 — 57건 총합
- **V5 placeholders**: harness 1건, rust-kit 7건
- **V1 frontmatter**: flutter-toolkit 1건
- **V4 triggers**: flutter-toolkit·rust-kit·react-kit 킷 간 공통 키워드 다수 (설계 의도 가능)
- **V2/V3/V7**: 전 킷 이상 없음

---

## 킷별 상세

### harness

**V5 — placeholder 1건 (ERROR)**

```text
harness/agents/qa-evaluator.md:42
"6. **주석은 증거가 아니다** — 구현자가 작성한 주석, TODO, 커밋 메시지..."
```

분석: `TODO` 가 문장 맥락에서 체크 항목 이름으로 사용됨. 의미상 교체가 필요하지 않을 수 있으나 V5 기준상 FAIL.

수정 방향:
- `--fix` 자동 수정 가능 (단, 문장 의미가 바뀔 수 있으므로 수동 검토 권장)
- 대안: `"주석"` 이라는 표현으로 교체하여 TODO 단어 제거

**V6 — bare code fence 8건 (ERROR)**

대상 파일: `README.md` 5건, `agents/qa-evaluator.md` 1건, `skills/create-skill/SKILL.md` 1건, `skills/init/SKILL.md` 1건

수정 방향: `--fix` 자동 수정 가능 (모두 ` ```text ` 으로 교체)

**V4 — cross-kit WARN 2건 (WARNING)**

"화면 추가" 키워드가 harness·flutter-toolkit·react-kit 에 동시 존재.
harness 의 sprint-contract description 에 포함된 예시 문구로 보임. 킷 간 트리거 경쟁 우려 낮음.

---

### flutter-toolkit

**V1 — frontmatter 누락 1건 (ERROR)**

```text
flutter-toolkit/skills/flutter-hooks/SKILL.md: 누락 필드 ['user-invocable']
```

수정 방향: SKILL.md frontmatter 에 `user-invocable: true` 추가 (1줄 수정)

**V6 — bare code fence 26건 (ERROR)**

가장 많은 킷. 대상 파일:
- `agents/widget-inspector.md` 2건
- `references/project-detection.md` 1건
- `skills/flutter-api/SKILL.md` 4건
- `skills/flutter-audit/SKILL.md` 5건
- `skills/flutter-build/SKILL.md` 2건
- `skills/flutter-error/SKILL.md` 1건
- `skills/flutter-extract/SKILL.md` 1건
- `skills/flutter-feature/SKILL.md` 3건
- `skills/flutter-hooks/SKILL.md` 1건
- `skills/flutter-kaizen/SKILL.md` 1건
- `skills/flutter-preflight/SKILL.md` 2건
- `skills/flutter-run/SKILL.md` 2건
- `skills/flutter-skeleton/SKILL.md` 1건

수정 방향: `--fix` 자동 수정 가능 (전체 ` ```text ` 로 교체, 이후 각 fence에 맞는 언어 수동 확인 권장)

**V4 — cross-kit WARN 56건 (WARNING)**

flutter-toolkit ↔ rust-kit / react-kit 간 공통 키워드. "빌드해줘", "에러 처리", "pre-commit", "preflight" 등 기능 카테고리 동사류. Flutter/Rust/React 는 스택이 달라 실제 트리거 경쟁은 낮으나 Claude 가 "현재 프로젝트 스택"을 인식 못할 경우 혼동 가능.

수정 방향: 카이젠 위임 — 스택별 구별자를 키워드에 추가하거나 description 에서 스택 명시 강화.

---

### design-kit

**V6 — bare code fence 10건 (ERROR)**

대상 파일: `README.md` 1건, `agents/design-reviewer.md` 2건, 스킬 7건 (design-audit, design-component ×2, design-guide, design-mockup, design-system ×2)

수정 방향: `--fix` 자동 수정 가능

---

### backend-kit

이슈 없음. 전 체크 PASS.

---

### infra-kit

**V6 — bare code fence 1건 (ERROR)**

```text
infra-kit/skills/infra-init/SKILL.md:51
```

수정 방향: `--fix` 자동 수정 가능

---

### rust-kit

**V5 — placeholder 7건 (ERROR)**

```text
rust-kit/skills/rust-api/SKILL.md:108  — todo!()
rust-kit/skills/rust-api/SKILL.md:112  — todo!()
rust-kit/skills/rust-auth/SKILL.md:127 — todo!("refresh_token_store 연동 필요")
rust-kit/skills/rust-auth/SKILL.md:131 — todo!("refresh_token_store 연동 필요")
rust-kit/skills/rust-auth/SKILL.md:135 — todo!("refresh_token_store 연동 필요")
rust-kit/skills/rust-l10n/SKILL.md:161 — # TODO: 번역 필요
rust-kit/skills/rust-l10n/SKILL.md:199 — 3. TODO 주석이 있는 로케일...
```

분석:
- `todo!()` / `todo!("...")`: Rust 코드 예시 템플릿에 미완성 구현 마커. 사용자에게 노출되는 코드 스니펫이므로 실제 구현 예시로 교체해야 함.
- `# TODO: 번역 필요`: 실제 번역 미완성 마커. 한국어 번역 내용으로 교체 필요.
- `rust-l10n/SKILL.md:199`: "TODO 주석이 있는 로케일" 이라는 설명 텍스트로 V5 패턴 매칭. 단어 자체가 설명에 사용된 경우이므로 예외 처리 검토 가능.

수정 방향:
- `rust-api`, `rust-auth`: 수동 수정 — `todo!()` 를 실제 Rust 코드 예시로 교체
- `rust-l10n:161`: 수동 수정 — `# TODO: 번역 필요` → 실제 한국어 번역 또는 명시적 예시로 교체
- `rust-l10n:199`: 가이드 V5 예외 조건 추가 검토 (설명 문맥에서의 `TODO` 단어)
- `--fix` 자동 수정도 가능하지만 의미가 손실될 수 있어 수동 검토 권장

**V6 — bare code fence 11건 (ERROR)**

대상 파일: rust-audit, rust-auth, rust-docker, rust-error ×2, rust-feature ×3, rust-init ×3

수정 방향: `--fix` 자동 수정 가능

**V4 — cross-kit WARN 29건 (WARNING)**

rust-kit ↔ flutter-toolkit / react-kit 간 공통 키워드. flutter-toolkit 과 동일한 성격.

---

### react-kit

**V6 — bare code fence 1건 (ERROR)**

```text
react-kit/README.md:76
```

수정 방향: `--fix` 자동 수정 가능

**V4 — cross-kit WARN 50건 (WARNING)**

react-kit ↔ flutter-toolkit / rust-kit 간 공통 키워드. 동일 성격.

---

## 우선순위 정리

### P0 — 즉시 수동 수정 (스킬 동작에 직접 영향)

| 킷 | 체크 | 파일 | 내용 |
|----|------|------|------|
| flutter-toolkit | V1 | skills/flutter-hooks/SKILL.md | `user-invocable` 필드 누락 — 스킬이 인식 안 될 수 있음 |
| rust-kit | V5 | skills/rust-api/SKILL.md | `todo!()` 미완성 코드 예시 2건 |
| rust-kit | V5 | skills/rust-auth/SKILL.md | `todo!("refresh_token_store 연동 필요")` 3건 |
| rust-kit | V5 | skills/rust-l10n/SKILL.md | `# TODO: 번역 필요` 실제 번역 누락 |

### P1 — --fix 자동 수정 가능 (품질 개선, 기능 영향 없음)

| 킷 | 체크 | 건수 |
|----|------|------|
| harness | V5 | 1건 (수동 검토 권장) |
| harness | V6 | 8건 |
| flutter-toolkit | V6 | 26건 |
| design-kit | V6 | 10건 |
| infra-kit | V6 | 1건 |
| rust-kit | V6 | 11건 |
| react-kit | V6 | 1건 |

총 V6 자동 수정 대상: **57건**

자동 수정 명령:
```bash
python3 scripts/validate-plugin.py --fix
```

### P2 — 카이젠 위임 (설계 수준 재검토)

| 킷들 | 체크 | 내용 |
|------|------|------|
| flutter-toolkit, rust-kit, react-kit | V4 | 킷 간 트리거 키워드 중복 135건. `flutter-kaizen`, `rust-kaizen`, `react-kaizen` 에서 description 키워드 전략 재검토 |

---

## 향후 작업 (다음 세션)

1. `python3 scripts/validate-plugin.py --fix` 실행 → V5/V6 자동 수정
2. flutter-toolkit V1: `flutter-hooks/SKILL.md` 에 `user-invocable: true` 추가
3. rust-kit V5: `rust-api`, `rust-auth` `todo!()` 실제 코드로 교체, `rust-l10n` 번역 완성
4. V4 cross-kit 키워드 전략: 각 카이젠 스킬 실행 시 description 개선 포함

---

## 참고: --fix 실행 예상 결과

`--fix` 는 V5(placeholders)와 V6(bare fence)만 수정한다. 실행 후 예상 상태:

| 킷 | V5 after fix | V6 after fix |
|----|-------------|-------------|
| harness | WARN(fixed) | WARN(fixed) |
| flutter-toolkit | OK | WARN(fixed) |
| design-kit | OK | WARN(fixed) |
| backend-kit | OK | OK |
| infra-kit | OK | WARN(fixed) |
| rust-kit | FAIL(수동 필요) | WARN(fixed) |
| react-kit | OK | WARN(fixed) |

rust-kit V5 의 `todo!()` 는 `--fix` 로 `<설명 필요>()` 형태로 교체되지만 Rust 문법을 깨뜨리므로 수동 수정이 바람직하다.
