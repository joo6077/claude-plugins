---
name: bambu-model
description: 출력할 부품을 새로 그리거나 원본 설계 파일(f3d)의 치수를 바꿔 STL 을 만든다. 새 부품은 전역 python3 의 CadQuery 로 코드로 그리고 그림으로 모양을 확인한다. 원본 f3d 는 퓨전 360 추가 기능을 잠깐 깔아 매개변수를 바꾸고 몸체마다 STL 과 구멍 크기 보고를 낸다. 끝나면 출력 설정은 /bambu-print-profile 로 넘긴다. "부품 모델링", "STL 만들어줘", "부품 새로 그려줘", "f3d 치수 바꿔줘", "퓨전 원본 수정", "CadQuery" 같은 요청 시 트리거. 출력 설정(process · filament JSON)만 필요하면 트리거 X — /bambu-print-profile 을 쓴다.
user-invocable: true
---

# Bambu Model

출력할 부품을 코드로 만든다. 두 갈래다 — 없는 부품을 새로 그리기(CadQuery), 있는 원본 설계 파일의 치수 바꾸기(퓨전 360).
결과는 STL 이고, 출력 설정은 이 스킬이 만들지 않는다.

## Gotchas

1. **퓨전은 화면 프로그램이라 못 다룬다고 결론 내지 마라.** 명령줄로는 못 부르지만 켜질 때 저절로 도는 추가 기능으로 다룬다.
   `scripts/fusion-job.sh` 가 깔고, 퓨전을 다시 켜고, 끝나면 걷어 낸다. 실측(2026-11-01): 다른 세션이 이걸 몰라 원본 치수를 못 바꿨다.
2. **CadQuery 를 가상 환경이나 세션 임시 폴더에 따로 깔지 마라.** 전역 python3 에 깔고, 있으면 그대로 쓴다.
   임시 폴더에 깔면 다음 세션이 못 찾는다.
3. **CadQuery 를 `python3 -I`(격리 모드)로 부르지 마라.** 의존 패키지(fontTools)가 사용자 폴더 `~/.local` 에만 있으면
   `No module named 'fontTools'` 로 죽는다 (2026-11-01 실측).
4. **퓨전이 안 꺼지면 강제로 끄지 마라.** 저장 안 한 문서가 있으면 퓨전이 확인 창을 띄운 채 남는다.
   `fusion-job.sh` 는 종료 코드 4 로 멈추고, 사용자에게 퓨전을 직접 끄게 한다.
5. **모양은 그림으로 확인한 뒤 사용자에게 보인다.** 크기 숫자만 보고 「됐다」 하지 마라 — 신발 걸이 시안은 숫자가 맞는데도
   사용자가 원한 모양과 달라 다섯 번 고쳤다. 사용자가 고른 시안을 기준으로 작게 고쳐 간다.
6. **AddIns 폴더에 다른 추가 기능이 있으면 먼저 치워라.** manifest 의 `runOnStartup` 을 `false` 로 바꿔도 퓨전은 자기 목록대로 계속 켤 때마다 돌린다.
   두 추가 기능이 같이 돌면 이 킷의 작업 신호가 처리되지 않아 시간 초과(종료 코드 3)로 끝난다 — 실측(2026-11-01): 옛 추가 기능을 지우자 15 초 만에 끝났다.
   지원 운영체제 값은 `windows|mac` 이다. 다른 값을 쓰면 퓨전이 추가 기능을 조용히 건너뛴다.
7. **원본 부품의 구멍 · 결합부를 새 부품에 맞출 땐 원본에서 재라.** 짐작한 나사 지름을 쓰지 마라 —
   `report.txt` 의 `HOLE` 줄이 원본의 실제 구멍 지름이다.

## Process

### 1. 도구 확인

```bash
bash "<이 스킬 폴더>/scripts/ensure-cadquery.sh"
```

`있음: CadQuery <판>` 이면 그대로 쓰고, 없으면 이 스크립트가 `python3 -m pip install` 로 깐다. 종료 코드 1 이면 출력된 import 오류를 사용자에게 보인다.

### 2. 새 부품 그리기 (CadQuery)

1. 결합 치수(막대 지름 · 구멍 · 벽 두께)를 먼저 확정한다. 원본과 맞물리면 3 단계 보고에서 잰 값을 쓴다.
2. 부품 코드를 `.py` 하나로 쓰고, 바뀔 치수는 인자로 받는다. 결과는 `cq.exporters.export(part, "<이름>.stl")`.
3. 그림으로 모양을 확인한다. 각도를 바꿔 두세 장 찍는다.

   ```bash
   python3 "<이 스킬 폴더>/scripts/render.py" <이름>.stl <이름>-front.png 10 -90
   python3 "<이 스킬 폴더>/scripts/render.py" <이름>.stl <이름>-iso.png 25 -55
   ```

4. 그림과 크기(그림 제목에 나온다)를 사용자에게 보이고 고칠 점을 받는다. 코드와 STL 은 사용자 작업 폴더에 둔다.

### 3. 원본 f3d 치수 바꾸기 (퓨전 360)

1. 작업 파일을 쓴다.

   ```json
   {"source": "/abs/path/model.f3d", "out_dir": "/abs/path/out", "params": {"dowel_size": "32 mm"}, "holes_under_mm": 40}
   ```

   매개변수 이름을 모르면 `params` 를 비워 한 번 돌려 `report.txt` 의 `BODY` · `HOLE` 줄로 원본을 먼저 잰다.
2. 사용자에게 퓨전이 한 번 꺼졌다 켜진다고 알리고 돌린다.

   ```bash
   bash "<이 스킬 폴더>/scripts/fusion-job.sh" job.json
   ```

3. 결과를 읽는다. `out_dir` 에 보이는 몸체마다 `<부품>__<몸체>.stl` 이 생긴다. `report.txt` 에는 `PARAM`(바뀐 값) · `BODY`(크기 mm) · `HOLE`(원통 구멍 지름 · 길이 · 축) 줄이 있다.
4. 종료 코드별로 다음을 한다.

   | 코드 | 뜻 | 다음 |
   | --- | --- | --- |
   | 0 | 끝남 | 아래 3 번처럼 결과를 읽는다 |
   | 1 | 추가 기능이 실패 | 출력된 `fusion-job.log` 의 오류를 읽고 작업 파일을 고친다 |
   | 2 | 작업 파일 · 원본 경로 오류 | 경로를 고친다. 퓨전은 건드리지 않았다 |
   | 3 | 시간 초과(`BAMBU_FUSION_TIMEOUT`, 기본 600 초) | 퓨전이 로그인 창에서 멈췄는지 사용자에게 묻는다 |
   | 4 | 퓨전이 안 꺼짐 | 저장 안 한 문서를 사용자가 정리하고 퓨전을 직접 끈 뒤 다시 돌린다 |

### 4. 출력 설정으로 넘기기

STL 이 확정되면 `/bambu-print-profile` 로 출력 설정을 만든다. 부품 이름 · 크기 · 결합 치수(공차가 필요한 구멍)를 같이 넘긴다.

## References

- `scripts/ensure-cadquery.sh` — CadQuery · matplotlib · numpy-stl 확인 · 설치
- `scripts/render.py` — STL 을 음영 그림 PNG 로
- `scripts/fusion-job.sh` — 작업 파일대로 퓨전 추가 기능을 돌리고 걷어 낸다
- `scripts/fusion-addin/` — 퓨전 추가 기능 본보기 (`fusion-job.sh` 가 복사해 쓴다)
- 시험: `bambu-kit/evals/model-tools-test.sh` (`--fusion` 을 주면 진짜 퓨전으로 한 번 돈다)
