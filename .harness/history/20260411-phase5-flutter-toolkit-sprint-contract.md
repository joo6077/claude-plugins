# Sprint Contract — Phase 5 Flutter-toolkit Kaizen

Date: 2026-04-11
Sprint: kaizen-phase5-flutter-toolkit

## 목표

flutter-toolkit 스킬 품질 개선: V1/V6 validation 이슈 해결 + 실사용 인사이트 반영 + V4 disambiguation 보강

## 완료 조건

### V1 (필수)
- [ ] V1-01: `flutter-hooks/SKILL.md` frontmatter에 `user-invocable: true` 추가
- [ ] V1-02: `validate-plugin.py flutter-toolkit` V1 체크 결과 0 FAIL

### V6 (필수)
- [ ] V6-01: `validate-plugin.py flutter-toolkit --fix --check=code-fence` 실행하여 26건 bare fence 일괄 수정
- [ ] V6-02: V6 FAIL 건수가 수정 전 26건 → 수정 후 0건으로 감소

### 실사용 인사이트 반영 (필수)
- [ ] INS-01: `flutter-hooks/SKILL.md` Gotchas에 "@freezed Props + HookWidget enforce" 강화 항목 추가
  - apps 프로젝트 AR-01 사례: HookWidget + @freezed Props 패턴 enforce 규칙 구체화
- [ ] INS-02: `flutter-widget/SKILL.md` Gotchas에 "외부 라이브러리 위젯 wrapping 시 기본값 명시적 덮어쓰기" 추가
  - apps 프로젝트 UI-02 사례: html_editor_enhanced defaultToolbarButtons 완전 오버라이드 패턴

### V4 Cross-kit Disambiguation (선택적)
- [ ] DIS-01: 다수 flutter-toolkit 스킬 description에 Flutter 전용 컨텍스트 단어 보강 (HookWidget, Riverpod, GoRouter 등)
  - react-kit과의 혼동 방지 목적. 트리거 기능 코드는 수정 금지.

## 완료 기준 검증

- `validate-plugin.py flutter-toolkit` 최종 실행 → V1 0 FAIL, V6 0 FAIL 확인
- Gotchas 추가 내용이 실사용 사례 근거(apps/fit-pal feedback)와 연결됨을 확인
