---
name: 스킬/에이전트 생성 시 create-skill, create-agent 스킬 사용 필수
description: 새 스킬이나 에이전트를 만들 때 반드시 harness의 create-skill, create-agent 스킬을 통해 생성해야 함
type: feedback
---

스킬이나 에이전트를 새로 만들 때 반드시 `/create-skill` 또는 `/create-agent` 스킬을 통해 생성할 것.

**Why:** 직접 작성하면 skill-design-guide.md의 9가지 아키타입 체크, Gotchas 패턴, 폴더 구조, description 트리거/비트리거 조건 등 설계 가이드를 놓치게 됨. docs-site 스킬을 직접 만들었더니 page-template.html 누락, 추측성 Gotchas 등 품질 이슈 발생.

**How to apply:** 사용자가 "스킬 만들어줘", "에이전트 추가해줘" 등 요청 시 항상 `/create-skill` 또는 `/create-agent`를 먼저 호출하고, 해당 스킬의 프로세스를 따라 생성한다. 시간 효율을 위해 직접 작성하지 않는다.
