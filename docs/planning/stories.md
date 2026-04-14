---
name: stories
description: 사용자 스토리, 예시 기반 명세, 수용 기준을 일관되게 작성하기 위한 패턴 정리
last_updated: 2026-04-14
version: 0.1.0
---

# Stories

## 개요
스토리 문서는 backlog를 예쁘게 적는 기술이 아니라, 팀이 작게 나누되 맥락은 잃지 않도록 만드는 언어 체계다. 잘못 쓰인 story는 단순 task 제목이 되고, 잘 쓰인 story는 가치, 맥락, 검증 기준을 함께 담는다.

이 영역에서는 INVEST, Gherkin(Given-When-Then), Story Mapping, Acceptance Criteria 패턴을 함께 보는 것이 중요하다. INVEST는 story의 품질을 가늠하고, Gherkin은 예시(examples)를 실행 가능 문법으로 바꾸며, Story Mapping은 전체 사용자 흐름 속 위치를 보여준다. Acceptance Criteria는 최종적으로 "완료"의 의미를 팀 간 계약으로 고정한다.

## 원칙/방법론별 섹션

### INVEST
**요약**: INVEST는 좋은 user story의 품질 체크리스트다. Independent, Negotiable, Valuable, Estimable, Small, Testable 여섯 조건으로 스토리를 점검한다. 핵심은 템플릿 문장보다 story가 iteration-friendly한 단위인지 확인하는 데 있다.

이 체크리스트는 backlog grooming에서 특히 유용하다. 이야기하기 쉬운 story와 만들기 쉬운 story는 다르므로, INVEST는 스토리를 지나치게 큰 요구사항이나 숨은 기술 task로부터 분리해 준다.

**핵심 질문/포맷/체크리스트**:
- Independent: 다른 story에 과도하게 묶여 있지 않은가?
- Negotiable: 솔루션이 아니라 대화 가능한 요구로 남아 있는가?
- Valuable: 사용자/비즈니스 가치가 설명되는가?
- Estimable: 팀이 대략 추정 가능한가?
- Small: 한 iteration/cycle 안에 소화 가능한가?
- Testable: 검증 가능한 조건이 있는가?

**적용 시점**: backlog refinement, epic 분해, sprint planning 직전 품질 점검.
**한계/주의사항**: INVEST는 story 품질 체크이지 우선순위 도구가 아니다. 각 항목이 형식적으로만 맞아도 실제로는 맥락 없는 story일 수 있다.
**출처**:
- https://agilealliance.org/glossary/invest/ [dated: 2015-12]

### Gherkin / Given-When-Then
**요약**: Gherkin은 executable specification을 위한 문법이며, Given-When-Then은 초기 맥락, 사건, 기대 결과를 분리한다. Cucumber 공식 문서는 이를 business rule을 예시(example)로 표현하는 언어로 정의한다.

좋은 Gherkin은 테스트 자동화보다 먼저 협업 도구다. UI 버튼 위치나 DB 상태가 아니라 사용자가 관찰 가능한 결과를 서술해야 한다. "상세 구현"이 아닌 "행동 규칙"에 집중할수록 문서와 테스트의 수명이 길어진다.

**핵심 질문/포맷/체크리스트**:
- Given: 시스템의 초기 상태/전제조건이 명확한가?
- When: 단일 사건 또는 행동이 드러나는가?
- Then: 관찰 가능한 결과를 검증하는가?
- Scenario 수는 많아도 각 시나리오는 3~5 step 안에 유지되는가?
- 구현 세부가 아닌 도메인 언어로 쓰였는가?

**적용 시점**: acceptance test 정의, QA/PM/DEV 협업 명세, business rule 문서화.
**한계/주의사항**: 모든 story를 Gherkin으로 써야 하는 것은 아니다. 낮은 수준 UI step을 남발하면 brittle test 문서가 된다.
**출처**:
- https://cucumber.io/docs/gherkin/
- https://cucumber.io/docs/gherkin/reference
- https://cucumber.io/docs

### Story Mapping (Jeff Patton)
**요약**: Story Mapping은 backlog를 납작한 우선순위 리스트가 아니라 사용자 활동 흐름에 따라 배치하는 방식이다. Jeff Patton은 이것이 전체 시스템이 무엇을 하도록 설계되었는지 이해하고, release를 가치 단위로 자르기 쉽게 만든다고 설명한다.

실무적으로 story map은 두 가지를 동시에 해결한다. 첫째, 사용자의 end-to-end 맥락을 유지한다. 둘째, release slicing을 더 현실적으로 만든다. 따라서 story map은 discovery와 delivery의 경계에서 특히 강하다.

**핵심 질문/포맷/체크리스트**:
- backbone activities가 사용자 여정 순서대로 놓였는가?
- 각 activity 아래의 세부 story가 충분히 분해되었는가?
- 첫 release slice가 "작지만 완결된 경험"인가?
- map을 보면 누락된 단계나 예외 흐름이 보이는가?
- 기능 논쟁보다 사용자 행동 흐름이 중심에 있는가?

**적용 시점**: epic 분해, MVP/release slicing, discovery 결과를 backlog로 연결할 때.
**한계/주의사항**: map이 상세화될수록 유지비가 커진다. workshop 산출물로만 남기지 말고 이후 backlog/roadmap과 연결해야 한다.
**출처**:
- https://jpattonassociates.com/story-mapping/
- https://jpattonassociates.com/user-story-mapping-presentation/ [dated: 2008-01]
- https://jpattonassociates.com/story-mapping-boot-camp/

### Acceptance Criteria 패턴
**요약**: Acceptance Criteria는 story가 "done"인지 판단하는 명시적 조건이다. 형식은 자유롭지만, 관찰 가능하고 테스트 가능해야 하며, 범위와 예외를 명확히 해야 한다. Gherkin이 한 패턴이라면, checklist/규칙형 criteria도 실무에서 흔하다.

좋은 acceptance criteria는 개발자에게 구현 힌트를 주되 구현을 강제하지 않는다. 또한 happy path만이 아니라 edge case, error state, 접근권한, 데이터 제약을 포함해야 한다.

**핵심 질문/포맷/체크리스트**:
- 완료 판단 기준이 "구현 완료"가 아니라 "행동/결과 확인" 기준인가?
- 성공 조건, 예외 조건, 권한/제약이 분리되어 있는가?
- 사용자/외부 시스템이 관찰 가능한 결과를 검증하는가?
- story 설명에 숨어 있던 암묵 요구가 criteria로 명시됐는가?

**적용 시점**: story ready 정의, QA handoff, refinement 종료 조건.
**한계/주의사항**: acceptance criteria를 세부 설계 문서로 만들면 협상 가능성이 사라진다. 반대로 너무 추상적이면 쓸모가 없다.
**출처**:
- https://cucumber.io/docs/gherkin/reference
- https://agilealliance.org/glossary/invest/ [dated: 2015-12]

## 참고 링크 (전체)
- https://agilealliance.org/glossary/invest/ [dated: 2015-12]
- https://cucumber.io/docs/gherkin/
- https://cucumber.io/docs/gherkin/reference
- https://cucumber.io/docs
- https://jpattonassociates.com/story-mapping/
- https://jpattonassociates.com/user-story-mapping-presentation/ [dated: 2008-01]
- https://jpattonassociates.com/story-mapping-boot-camp/
