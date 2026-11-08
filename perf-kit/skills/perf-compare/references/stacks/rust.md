# 스택: Rust

감지: `Cargo.toml` 이 있다. 서버 바이너리의 API 비교는 `server.md` 를 함께 읽는다.

## 함정

- **표본 하나는 프로세스 실행 하나다** — criterion 은 한 프로세스 안에서 여러 번 재고 자체 비교(변화율 · p 값)를 낸다. 두 커밋 비교에서는 `cargo bench` 를 A · B 번갈아 여러 번 돌리고, 회마다 criterion 이 낸 중앙값 하나를 표본으로 쓴다. criterion 의 `change` 판정을 그대로 옮기지 않는다 — 순서와 대조 지표를 이 스킬이 맞춘다
- **최적화 빌드끼리 비교한다** — `cargo bench` 는 `bench` 프로필, 바이너리 비교는 `--release` 다. 두 쪽 프로필 · 기능 플래그(`--features`) · 툴체인이 같은지 `fixed` 에 적는다
- **hyperfine 은 명령을 입력 순서대로 잰다** — README 는 "Commands run and appear in input order" 라고만 적는다. 라운드마다 순서를 섞으려면 라운드마다 hyperfine 을 따로 부르고 결과를 합친다
- **criterion 의 JSON 파일은 읽지 않는다** — 공식 문서가 `estimates.json` 같은 JSON 을 "private implementation details" 이고 예고 없이 바뀐다고 적는다. 기계가 읽을 출력은 `cargo-criterion --message-format=json` 을 쓰라고 권한다

## 지표별 경로

| 지표 | 경로 | 표본 |
| --- | --- | --- |
| 함수 · 크레이트 단위 시간 | criterion `cargo bench` | 회마다 표본별 반복당 시간(ns)의 중앙값 |
| 명령줄 실행 시간 | hyperfine | 회마다 JSON 내보내기의 실행 시간 (초) |
| 최대 메모리 | `/usr/bin/time` | 회마다 최대 상주 메모리 |
| 바이너리 크기 | `stat` | 결정값 — 쪽마다 2 회 |

## criterion

공식 권장 경로는 `cargo-criterion --message-format=json` 이다. 출력 줄 형식은 External Tools 문서를 보고 첫 회에 중앙값 필드를 정한 뒤 알려진 답 대조를 한다.

`raw.csv` 는 형식이 문서화돼 있어 바로 쓸 수 있다. 다만 공식 문서가 CSV 출력을 없애는 중이고 0.4.0 부터 선택 기능이 된다고 적는다. 쓰는 판에서 `target/criterion/{벤치}/new/raw.csv` 가 생기는지 첫 회에 확인한다.

```bash
# 한 회: 벤치를 돌리고 표본마다 반복당 시간 = sample_measured_value / iteration_count 의 중앙값(ns)을 낸다
cargo bench --bench {벤치 파일} -- '{벤치 이름}'
python3 -c '
import csv, statistics, sys
rows = list(csv.DictReader(open(sys.argv[1])))
assert rows and rows[0]["unit"] == "ns", rows[:1]
print(statistics.median(float(r["sample_measured_value"]) / float(r["iteration_count"]) for r in rows))
' "target/criterion/{벤치}/new/raw.csv"
```

- 알려진 답 대조: `sample_measured_value` 2000 · 4000 · 9000 에 `iteration_count` 가 모두 10 인 세 줄짜리 사본이면 400 이 나와야 한다. 나누기를 빼먹으면 4000 이 나온다
- criterion 은 기본으로 앞 회 측정과 비교한 결과를 출력한다. 표본은 `new/` 만 읽으므로 그 비교 출력은 쓰지 않는다
- 커밋을 오가며 재려면 `git worktree` 로 A · B 를 따로 꺼내 두고 각 폴더에서 돌린다. 빌드 산출물을 나누려면 `CARGO_TARGET_DIR` 을 쪽마다 따로 둔다

## hyperfine

```bash
# 한 라운드: 예열 후 1 회씩. 라운드 순서는 experiment-design.md §순서 대로 섞는다
hyperfine --warmup 3 --runs 1 --export-json round-03-a.json './a/target/release/app input.txt'
python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["results"][0]["times"][0])' round-03-a.json
```

- JSON 내보내기는 예열 실행을 뺀 실행마다 값을 담는다. 키 구조(`results[].times`)는 README 에 설명이 없어 첫 회에 파일을 열어 확인한다
- `--runs` 를 늘려 한 번에 여러 표본을 얻을 수도 있다. 그때 순서는 `blocked` 로 기록한다

## 최대 메모리

```bash
/usr/bin/time -l ./target/release/app input.txt 2> time.txt   # macOS: "maximum resident set size" (bytes)
/usr/bin/time -v ./target/release/app input.txt 2> time.txt   # Linux: "Maximum resident set size (kbytes)"
```

macOS 와 Linux 의 단위가 다르다. `unit` 에 실제 단위를 적는다.

## 바이너리 크기

```bash
stat -f %z target/release/app 2>/dev/null || stat -c %s target/release/app
```

## 출처

- criterion — CSV 출력(열 정의 · JSON 은 내부 구현 · CSV 단계적 폐지): <https://bheisler.github.io/criterion.rs/book/user_guide/csv_output.html>
- criterion — 명령줄 옵션(`--save-baseline` · `--baseline`): <https://bheisler.github.io/criterion.rs/book/user_guide/command_line_options.html>
- hyperfine README(`--warmup` · `--runs` · 입력 순서 · JSON 내보내기): <https://github.com/sharkdp/hyperfine>
