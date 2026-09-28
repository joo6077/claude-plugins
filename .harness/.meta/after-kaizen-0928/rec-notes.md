# rec 묶음 기록 — 지난 기록 줄 참조 · 기록 정정 (B20 · D6 · D8)

- 계약: `.harness/sprint-contract-after-0928-record-fixes.md` (23 조건, 봉인 커밋 `a6c1487`, 조건 지문 `sha256:eeed04ad09b3a423` · 측정 지문 `sha256:31aef57f8264fd42`)
- 기준 판 `e500a63`, 가지 `chore/ak3-rec`. 측정 도구 셋은 `.harness/.meta/after-kaizen-0928/rec/` 에 있다.
- QA 판정은 하지 않았다. 계약 `status` 는 `active` 그대로다.

## 항목별 결과

| 항목 | 한 일 | 커밋 |
| --- | --- | --- |
| B20 | 경고 정리 병합이 밀어 놓은 `.harness` 기록의 `파일:줄` 참조 1065 곳(기록 170 파일)을 기준 판 번호로 옮겼다. 계약 본문 311 곳과 리포트 · 개정 · notes 686 곳은 번호만 고쳤고 줄 수는 그대로다. 봉인된 조건 줄 31 곳 · 측정 줄 37 곳은 글자를 두고, 계약 옆 정정 파일(`sprint-lineref-*.md`) 60 개에 옛 참조 → 새 참조를 적었다. 본문 311 곳도 같은 정정 파일에 한 행씩 있다 | `a3bb518` |
| D6 | `docs/flutter/research-log.md` 20 행과 `docs/kaizen/flutter-research-log.md` 20 행의 「2.16 부터」 문장은 그대로 두고 바로 뒤에 「정정(2026-09-28): build_runner 원문 기준 2.7.0 부터 — 이 옵션은 이미 무시됐다」 와 근거 `.harness/.meta/after-kaizen-0926b/ex/EX-5.md` 를 붙였다. 두 파일 모두 짝 페이지가 없어 페이지는 만들지 않았다 | `a078903` |
| D8 | main 끝 `01b1cac` 까지의 커밋 1535 개 가운데 메시지에 쉬운 말 목록 낱말이 든 271 개에 `git notes` 메모(`refs/notes/commits`)를 달았다. 메모 본문은 `plain_words.py note <해시>` 출력 그대로다 — 머리 한 줄과 걸린 낱말마다 「낱말」 → 바꿔 쓸 말. 원격에는 올리지 않았다 | 커밋 없음 (메모 ref) |
| 도구 | 측정 도구 셋을 봉인 전 실측 때와 같은 글자로 커밋했다 | `b2a65df` |

## 올리기 (부모가 할 일)

```bash
git push origin refs/notes/commits
```

메모는 기본 fetch 에 딸려 오지 않는다. 다른 복제본에서 보려면 `git fetch origin refs/notes/commits:refs/notes/commits` 가 필요하다.

## 자기 측정 (TIP 기준, 2026-09-28)

- SK-01 · SK-02: 행 1 개, 옛 문장 · 정정 문자열 둘 각 1, 순서 1, 줄 수 BASE 와 같음(477 · 203). SK-03: 페이지 없음 · html 에 `2.16 부터` 0 · 짝 이름 `None` (양성 대조 md 2).
- SC-01: 목록 1065 행 · 지문 `2e65984b2b251b03`, 내용 대조 `SUMMARY moved=1021 changed=44 bad=0` 종료 코드 0.
- SC-02: `SUMMARY rows=1065 in_place=997 lineref_file=68 bad=0`. SC-04: `SUMMARY files_expected=60 files_found=60 bad=0`, 이름 집합 지문 `aae51cb9240e20ff`.
- SC-03: `SUMMARY scope_bad=0`. ER-01: 계약 231 개, 봉인 판정 차이 0 줄. ER-02: followup 파일 차이 없음, 원격 메모 0 · 원격 가지 0 (원격 조회 양성 대조 main 1).
- SC-05: 271 개 · 지문 `07bc82fc875822a0`, `SUMMARY commits=271 bad=0`, 메모 목록과 걸린 커밋 목록 차이 0 줄. 목록 파일 지문 `694f07858cf9016c` · 읽기 도구 지문 `793e5682f39120f3` 그대로.
- SC-06: `ci-local.sh` 25 단계 rc=0 · `feedback-agg-test SKIP (yq 없음)` 한 줄 (playwright 두 묶음 포함). CI 파일에만 있는 여섯 단계 전부 rc=0.
- AR-01 BAD 0 · AR-02 범위 밖 0 · 바뀐 경로 2 · AR-03 도구 지문 셋 일치 · AR-04 해시 빠짐 0. AP-03 · RE-01 · RE-02 · DG-01 기대값대로. DG-02: md 63 파일 경고 0.

## 킷 버전 판단

바뀐 파일은 `.harness` 기록과 `docs/flutter` · `docs/kaizen` 문서 둘뿐이다. 어느 킷 폴더도 건드리지 않아 올릴 킷 버전이 없다. 릴리스도 하지 않았다.

## 남은 것

- D8 메모 올리기 — 부모가 위 명령으로 올린다. 이 묶음은 원격에 아무것도 올리지 않았다(ER-02).
- B20 새 번호는 기준 판 `e500a63` 기준이다. 이 판 뒤에 다른 묶음(dz · h1 · h2 · k1 · orca · lt)이 대상 파일에 줄을 넣거나 빼면 다시 밀릴 수 있다. 그래서 정정 파일마다 새 참조 판을 적었다. 합친 뒤 `lineref.py` 를 새 기준 판으로 다시 돌릴지는 부모가 정한다.
- B20 에서 대상 줄 자체가 고쳐진 44 곳(`changed`)은 글자가 가장 닮은 새 줄로 보냈다. 줄 내용 대조(`content_check.py`)는 통과했지만 뜻까지 같은지는 사람이 보지 않았다.
- B20 은 경고 정리 병합이 만든 밀림만 다뤘다. 그 전부터 어긋나 있던 참조, 기준 판 뒤에 새로 쓰인 기록, `.harness` 밖 참조(`docs/superpowers/followup-2026-04-11-plugin-validation-findings.md` 등 — lt 묶음 몫)는 그대로다.
- 기록 가운데 「커밋 X 가 `파일:53` 을 고쳤다」 처럼 그때 번호를 적은 문장도 새 번호로 바뀌었다. 결정 B20 이 「리포트 · 기록은 직접 고친다」 여서 따랐다. 그때 번호가 필요하면 git 기록에서 찾는다.
- l4 notes 의 「520 곳」 과 이 묶음의 1065 곳은 세는 방식이 다르다. 이 묶음은 토큰마다 세고(같은 자리를 상대 · 절대 경로로 두 번 적으면 둘), 경고 정리 도중에 쓰인 기록도 센다.
- 측정 도구 셋은 CI 에 넣지 않았다. 고정된 옛 판의 줄별 작성 기록과 차이를 읽는데 CI 는 얕은 복제라 그 판이 없고, `plain_words.py` 는 저장소 밖 `~/.claude` 파일을 읽는다.
- D8 은 기계 판정을 그대로 따랐다. 「표면」 처럼 일상 뜻으로 쓴 커밋에도 메모가 달렸고, 메모 머리에 그 사실을 적었다.

## D8 메모를 단 커밋 (271 개)

| 커밋 | 걸린 낱말 |
| --- | --- |
| `2a29cdf4b2dc1f0ee763b41284d68ba0ab399eed` | 스키마 |
| `2fe1a0db05159bf167167cd3fd3c2005202fa8c4` | 스키마 |
| `6ad234f593ed1745948ad4ad2e5cff089e742664` | 게이트 |
| `ee338799361f7583c610fda9d7833006ad73bf68` | 게이트 |
| `1cedfa899c2c68fe94d466feb59daead8b367edc` | API |
| `55b760b0522378b286d32710228e784634eb4854` | 스키마 |
| `d0357df73c9ccd2a09eddc9f0eb9f02bcba4ee8d` | 정본 |
| `c2844089d39002e461a160987c870908b0b13784` | 게이트 |
| `3224b42a96dacfe78e9f4287c01baf6e923a6328` | 정본 |
| `275e4fb6a5d6cfb5654b931a3cc8ea477039ea2a` | 정본 |
| `e5333b70c800bae49cc34a8de83a4f334a539123` | 정본 |
| `c08f56fb0a2ae061be418bb2df188f2d47baf4e6` | API |
| `2dbdf3fe6e574b32be4b2db38f7e8d4975cf9f57` | 스키마 |
| `f3083ed3b9a481c71a8483d38822416e3bbf4206` | 해시 |
| `538744a4257056197573f165b5f9baad56a53e36` | 엔드포인트 |
| `297df7c73a9bcc88f3aa7cf21e93e46bbaaa1d7c` | 원장 |
| `f07be350e6af01c4782ec7349e9280d2953282d2` | 엔드포인트 |
| `fe6539c2d82ca0447c88d125381f1565bfa8012b` | API |
| `28c50937e0737f2d4d2c14de0a2a527a075d56d9` | 게이트 |
| `87d08bc47e85260bf7dd5dc8caf4fe245dc4179a` | 정본 |
| `5a3277e9c03c187a853c8f3a7b4e76bfd89b535d` | API |
| `afb07b791d43859fd8e2efec200ca8007da93a2f` | baseline |
| `39516b76e459d4a84fb8dd6a3caf11a74e0a3b33` | 게이트 |
| `fe1a02e25803106e88adc4c8bac4a19b9445bdde` | 정본 |
| `5389a59ce0be3c761a002d67cf7492a20c8b41ce` | 정본 |
| `75210c06ff499af1bc853dbc6847e375e3c453d5` | relaxing |
| `bcb4b1b46ec422939cdc08c5875cde9666f11dae` | 정본 |
| `d213037103d329f2dc0d68721dfa2af1b0a83dca` | 게이트 |
| `a0dad4b7c6a442fbc00873ba1aa2676faca1ae7d` | 게이트 · 정본 |
| `875a6c202323b25119820e6bb80fa729647f26f2` | relaxing |
| `5ceca275f2df746bf2e3dcf0264bf0317706c261` | API |
| `48618f6af3d53c095fb0fc932d2984ed336dd5df` | 정본 |
| `39ddc1275f77faa66a0ceac6a1b07c2fb6310dda` | 캐시 |
| `3472bf5075cb088703f73599766b32c044d360a4` | 게이트 |
| `5dc249fa910364cf85debcf4f25add4bf185ef0d` | 게이트 |
| `7799a5a2ad745c8b58e9e469572a5913a534e1c2` | 파싱 |
| `2ca89421337bd52b29c9944af5e06d5323056df5` | API |
| `38b6076e5e0d4f1a468bf6585f959710b02ba5e5` | 게이트 |
| `870f1c1a280d5aaceb46c656ff8e72305cc9e760` | 스키마 |
| `77ed5bbda2fc9999c4b5b0a71b123595f7eed868` | 스키마 |
| `04e3591535f05900c8095df023649a6593c98eb0` | 게이트 |
| `c6850fee84c8d05c1f6ac8c63a7934d0e8fec4e0` | 앵커 |
| `65ea663cc27189ab2508fc518ca9399d50dc24ff` | amend_direction |
| `d12b7b6f2dd91a20557cf88d21b176fc8619098a` | baseline |
| `22cdca1dcfc01693791f40e4a46367485209c8fe` | 게이트 |
| `8163d6903c3eccec59f80bd71f16f6283b5afef0` | 원장 · 승격 |
| `3484855de4665f2b3cf1c8c79c0ee8a24c44b052` | 클러스터 |
| `83703911ce1599dddb435d970e84b6a820fe98b7` | amend_direction |
| `657c0110de582044b225e527a7e10c406517270c` | 게이트 |
| `1c7ed43c9bb7573853189dc0629c37de8ecde9d5` | 게이트 |
| `77dcb485d2e54d7b2cf812c2763c1fd8d179c43a` | 게이트 |
| `f7d1788217c1ef6960bc1c874fe092ce45e139fb` | 게이트 |
| `8b5dbfb96b186d02d6ef8788a10342ff850bde33` | API |
| `44b43675d836e93066c1f4a1e6c22cbe849839e3` | 스키마 |
| `8a7df325d8686215af734ed10a79d0b6f27970c2` | 앵커 |
| `176d9e47b11c007071207a33b1de6d334c014ceb` | 스키마 · 게이트 |
| `58c821bbc4754e06984706b447b1f359a7cb9530` | 원장 |
| `af93eabbbc15b61f147b8c5e142f349ba8cb071d` | 원장 |
| `ad7ab52f784205791adeba1c48430f752d30aced` | 앵커 |
| `6877d97b8ecc43a5d4748663dcee8c7bdebc5440` | 오라클 · 앵커 |
| `37ac75f67a93b054f8c274e055c9dfee0820f748` | 스키마 · 게이트 · 표면 |
| `d97944ca6892a4601ee02b5e8cefa93e9c69d6a1` | 게이트 |
| `306948c0a95d7172d4e53e4560e6996df81c1560` | 게이트 |
| `e4692cb43a1a05971374b65b0abffc41b7303b6b` | 스키마 |
| `5a96f7c7a0f7aa301aceae1024e1b2e010be0bf2` | 게이트 |
| `c97dd20e3fb6f25c83a6de93752dd8908b00cfc6` | 게이트 |
| `50dfd8608cd24f2e5735b167f43c29027a9e6c24` | 게이트 |
| `c012f2b48f4c7190a800461007c67001b37b5bc0` | 게이트 |
| `b2e661fea8a3c53a287f0c974206772c4e94ba30` | 게이트 · 원장 |
| `c0342a5f46cc0746401625e24ac8e3049c830dc5` | 정본 |
| `7b4618c68fe3233462a0a6c9813007c1398bf297` | 정본 |
| `c646472dd09a52710c58cdc8a0be66633a639e38` | 스키마 |
| `3e3ff0469de65141a77902acf46c72b79fc2b616` | 스키마 |
| `18b8ff03a857896274ae852476bbde5c551cd934` | 원장 |
| `5d411d44ef17d75ad726644d4c6eef8d6ac35330` | 캐시 |
| `04e49f6ca341f614f29d029b7a1e7200528f63a8` | relaxing |
| `57fdcb3133b2cd4e4e3b707ad828ae2a0cdfe43e` | 해시 |
| `e76983d145d85ff34974976d2cdec8d791e3d907` | 스테이징 |
| `2a185b4037ca09c86b535cda17e29f229948bd21` | 앵커 |
| `b3300bec04876257a9dbc43e7bc1577576aefec3` | relaxing · narrowing |
| `ac77cdce10a5b4b70978b052bc559ca6020cb79b` | 스키마 |
| `18ce9e2dbf1251c1a333161f3bf51103e657f11d` | 앵커 |
| `cb39d899c989adba8bb1529144ce5903719bec7e` | relaxing |
| `dbd7e6795aeac6aa9861e061225dc132d59553a7` | 정본 |
| `8c1407c30e8dafa3e92774176de44435a7049951` | relaxing |
| `5f97eceeffa097a0e8c194e31bfe030902ae2534` | 오라클 · 스키마 · 승격 |
| `b968867b78f18f73e672c96d3f485c0812c862e6` | baseline · 인덱스 · 사이드카 · amendment · relaxing · narrowing · 게이트 · 원장 |
| `21f6e33d774f83b9a86e79c5f9a05a10aa76125f` | false negative · 게이트 |
| `e9c508f12326a9112693d19aca0548d67aff8374` | 게이트 · 원장 |
| `c0f5b9f63ff1fb3afb391010b3859668e98670f4` | 엔드포인트 · 컨테이너 · 게이트 · 정본 · 승격 |
| `5b86a4b612b8e00d86448c9cc9f618639f92324a` | 엔드포인트 · 게이트 · 정본 · 승격 |
| `d84e034fbfde23e640a9d45e3382d8006aa7d5c4` | 오라클 · API · 사이드카 · relaxing · 아키타입 |
| `073d97844fb60376c3a06aa28601db7dac6999d7` | 오라클 · 사이드카 · 원장 · 정본 · 승격 |
| `5625a10109850034a7d0a0feee76ddaf33604a1e` | amendment |
| `50b31a7c5fda45520ced10e1604cda235d955a53` | 오라클 · 해시 · 사이드카 · amendment · relaxing · 앵커 · 게이트 · 원장 · 정본 |
| `540dfeec20f6dc6e9a134b69f9f64eb3cdc8ac2e` | 오라클 · 스키마 · amendment · amend_direction · relaxing · narrowing |
| `fc9e0af1a2c19a84213df5a3a639da8d884d115e` | 게이트 |
| `1587bae8671983e72d3d9ad0bf5f5fe29c5a278f` | 사이드카 · narrowing · 게이트 · 정본 |
| `becab71e4124c7a3c7bf5d4998b3fb47fb511355` | 파싱 |
| `8ab60499c8cae19649ecfe58d394a1ed3ce14b9a` | 게이트 |
| `8f41a6dd4a6fec0101ff27a270d36f238cc94132` | 게이트 |
| `f33b33aab655da3f0a86b67d768f307f802b55a4` | 게이트 |
| `b1ebfe516fc90f9807e14c8c40bddde10c52ee3e` | API · 게이트 |
| `3cd7dfe0d6fbcd744d0ee8854acb2d4a4b9804a4` | API · 게이트 |
| `51b3054c78b05047e0a8249ee50a5fb1cdeba496` | 파싱 · 게이트 |
| `e73429fab3ef800907691123e9bfe372bee3ec83` | 게이트 |
| `f2e1b34acaf9f6e501ccb1f3eb101014af2cde45` | 게이트 |
| `77cb66c666a6c7c05c226d7420cb67ee128752b3` | 게이트 |
| `c90d0606bdae651c0b3d7ff15d67e04f12dea7c4` | 게이트 |
| `d937aca0967a89b508f5a9b60acd7289b19dd391` | 게이트 · 승격 |
| `f3c73e6ecde08ec4c9e476d3abcd1f39001fc428` | 정본 · 표면 |
| `07573ee6ab451460504619c96d2389698a1b5887` | 앵커 · 게이트 · 표면 |
| `3ae2ea3eb020f0e592c9485f4f03e03b68897dd2` | 게이트 |
| `27f576462b9c1aa777323a4a073851de507c76d8` | 게이트 |
| `52ab5dc695a18da087bf73e362db3fffc6f9da1c` | 게이트 |
| `8b4dc4958d86ca0a85eaedb76938a726c4e055e9` | 컨테이너 · 게이트 · 정본 |
| `f0e4dd5abbcd09af1b7cceb157f8149877d4e6a7` | 오라클 · 게이트 |
| `6e1c967e3106cd76c1b24b7efb235464b1021408` | API |
| `fdce1a94f8d6ad8ed0a11491a76155c83fc5227a` | 오라클 · 게이트 |
| `a19e3bc8a76a8b2eae56ff6bcabf41f593b25c23` | 정본 |
| `9fb682ffd5378d4c806d7ee7d9c9819d0f3c1863` | 오라클 · 게이트 · 정본 |
| `c92fd9c35fdceeea55c76688d7a8301bfd2e7d9d` | API |
| `358f8e1de3fb4da2ded2fdc53b2ebff6d2f7f1e1` | API |
| `80daceb331e6b3b66f15715bd23e77cceec53bb3` | 게이트 |
| `6c9500fdfbc82fea7d7ea125c295fe5362c761b1` | 게이트 |
| `ddea1464935e50c74f43bce417dedb92f302f4d0` | API · 컨테이너 · 게이트 · 표면 |
| `6e3976f7cdc678ec9a3abe823854e5a0f1759579` | 오라클 · 승격 |
| `9d151340ea6b1fee11ed3297e5e84acccab0dbb9` | 오라클 · fail-open · false negative · 페이로드 · 파싱 · 사이드카 · relaxing · narrowing · 앵커 · 게이트 · 승격 |
| `70a44ccfc6ce7647ac1bfaf88ab1bb899a400349` | 오라클 · 스키마 · 해시 |
| `8192e1109d41a90cf148c9643be8f90045503c16` | 사이드카 · relaxing · 앵커 |
| `6978e8cd918a0ce72efe699ad19bc3f8c8534b9e` | 스키마 · 사이드카 · amend_direction · relaxing · 앵커 |
| `ca1f5f4a3f279de8358e93619422350825b507bb` | baseline · amendment · 측정문 · 승격 |
| `3f4a2b5fcd1507e99d0080047271fee54488b62c` | 오라클 |
| `87b999e356fc96a2310444694d9b6696f84c1103` | 정본 |
| `6760e8dee6c2052f54b64da52759f60cdc9883ce` | 엔드포인트 · 인증 · 마이그레이션 · 캐시 · 측정문 · 정본 · 표면 |
| `2db4007b8c65e9faf83db08b4ced7605c68eb8ea` | 스키마 · 측정문 · 앵커 · 승격 |
| `c3cc5d89ca3c164c25df624a44963d39ce69f3b7` | 오라클 |
| `36b3e86674ba1c673442e0db0411d7a5b3bd9d0b` | 오라클 · 승격 |
| `84128c7241ea8139f5cf149d2b3184de679f0671` | 측정문 |
| `ba02734430dc228f05e7e3a54b5e70dd1d6f075e` | 클러스터 · 측정문 · 앵커 |
| `033a6ab2ccba3a1aa3c2d32719ac4481286971cf` | 오라클 · 파싱 · 해시 · 측정문 · 앵커 |
| `834ab9a9b735005b32db5d9579a942d622f8d9a1` | 측정문 |
| `47f4d0574a1b4ecc0412bb1ac69b56c3e32fce91` | 측정문 |
| `05ccddb56b44551ca4edaeafd20e997c54249bdb` | 측정문 · 앵커 |
| `4a71207d07eaff1b0e1bbfeb0eb230d2801050b9` | 표면 |
| `b52c8bf9060d597f57111ccae4304133badda584` | 오라클 · 사이드카 · 게이트 · 원장 · 정본 |
| `f62691f645c79d77b6c2c2f730cc8a24247fcc97` | 사이드카 |
| `ffc0a8442a5c9446243137825050e7cafa60d810` | 오라클 · 스키마 · 사이드카 · relaxing · 측정문 · 게이트 · 표면 |
| `04641f709e1cb524e2ca589684bc82c52fa25153` | 사이드카 · 측정문 · 게이트 · 정본 |
| `175ef8709822aee52cf6b71d19c31c5af73b62cd` | 오라클 · 스키마 · 파싱 · 사이드카 · 측정문 · 앵커 · 게이트 |
| `409c780d4b9355dfb8d174bc6c6b2461141ae3c7` | 오라클 · 사이드카 · 측정문 · 정본 · 표면 |
| `a137055790f84d164bdb7dcbf0a208f0840efffe` | fail-open · 캐시 · 클러스터 · 측정문 · 게이트 · 표면 |
| `b17fef3ad7ceee363f6cd707ce54e62c24406906` | 오라클 · 트랜잭션 · 사이드카 · relaxing · 측정문 · 게이트 · 정본 · 표면 |
| `0fe357a340680c25d7645bed79430694869f854c` | 클러스터 · 사이드카 · 게이트 |
| `1ba6059aa5f1d76821c9738bd2c5cfa890622b6b` | REST · 정본 |
| `965af485e3f5609b6afee2264b6479804dec57d4` | 스키마 · 게이트 |
| `73ef4e7d5c7ccc204d916a118bdfe2899b5fb91c` | 오라클 · 게이트 · 표면 · 승격 |
| `cbc9d3269d3bdd7ab4b5f7346296dd0d10e47e6c` | 오라클 · 트랜잭션 · 롤백 · 게이트 · 표면 |
| `a90448aa83d01867a0ad395c43cfb9bb31cfe1b6` | 오라클 · amendment · relaxing · 측정문 · 표면 |
| `e7b950823f4184b81d695dd4377837e6e7306d42` | baseline · 표면 |
| `a35e5cc01a95fa24d09cd09dab722c3fd5b49874` | 오라클 · 게이트 · 정본 · 표면 · 승격 |
| `da69b58646e0cd3e9bc8ef891ab8599b18dbc72d` | 오라클 · false negative · 파싱 · 사이드카 · relaxing · 측정문 · 게이트 |
| `598a5c332dff0186175355915189ef736446dba4` | 스키마 · 사이드카 · relaxing · 측정문 · 앵커 · 게이트 |
| `b161d804a73b853b9d88db7351e4aace66cbce64` | 오라클 · 사이드카 · amendment · 앵커 |
| `e987a0e5dfde99a433b741e3f9d8fc0ba42ce235` | 사이드카 · amend_direction · relaxing · 측정문 · 표면 |
| `fb3489431c36e24eb09c7207173da69b14e4f248` | 사이드카 · amendment · amend_direction · relaxing · 앵커 · 표면 |
| `c3f95955d6cf7cb41f33f7654de06cad45d217d7` | 오라클 · 스키마 · amendment · 앵커 · 게이트 · 원장 · 정본 |
| `b9e911f9a1c5ea4cff9b9cb5119c6268301c8292` | 오라클 · 사이드카 · amendment · relaxing · narrowing · 앵커 · 표면 |
| `d8df8d68cfd6808adc6a61e80c478bd831658bac` | 오라클 · 게이트 · 원장 · 아키타입 |
| `d4a2b321cfabaa74afcc89a3e3b8e8400932a3ff` | 오라클 · 승격 |
| `7ae05429c4633836c2dab74818518de903bf08b1` | 오라클 · 스키마 · 컨테이너 |
| `92bcfca2ec2a9f509677c9339dbfe253452cd1e4` | 게이트 |
| `41c29b3156ad90456a554f371a01ba0241b995d6` | 컨테이너 |
| `0438b9a5d2ddd82b905db800a09a189b2c598639` | 오라클 |
| `31abb42cb58d40ad306ded2f493b60159154bfc0` | API · 인증 · 파싱 |
| `fddc89fdb0915aa9f05c0817a464b3b5ae066a74` | 오라클 · 파싱 · 컨테이너 |
| `a40b4748dd07b57afa3061344af527c6161dfa8d` | 타임아웃 |
| `ef0a839dfd55fd73bba2977a714842bb4bd320a9` | 표면 |
| `93aecbd89d1f429a1ba4c0242c820b3922e6eec5` | 표면 |
| `c9a4cbe7bd2d76d32f297756fbbebb1b7a6d3d77` | allowlist · 마이그레이션 · 해시 · 사이드카 · amendment |
| `8384205f2162cc214cdb91e0b93fb8f183bbc846` | false negative · 게이트 |
| `cdfc9e4927bb138d7b47d8c5c3b4c9bdee7e7f9a` | 파싱 |
| `df83bb1d92c9b37ee753f04cc5310e48ed599eb5` | 파싱 |
| `01c2d2ee860af365bb907645eefcd1fca3b508f8` | 롤백 |
| `2592635e861e43c176376ae0b92dd8b703a0e887` | 스키마 · 게이트 |
| `d4879873259f0880685ca2779b5f613f60977ad7` | API |
| `4352398e85e8518ea75ac8daa4e792359739bed9` | fail-open · allowlist · regression · API · 스키마 · 파싱 · 클러스터 · 게이트 · 승격 |
| `928fd30cfd821e40b570f41587a675f9d2c8a085` | regression · baseline · 정본 |
| `437bc9785edf6cc55145f5c5200d55abab9de2ef` | regression · baseline · 파싱 · 게이트 · 표면 |
| `2c2a353ba2754e49283eb6e12efd0e7ad0f5a58c` | regression · API · 파싱 · 게이트 · 원장 |
| `e0427924578821653fab1718f593d814e6542df1` | regression · 앵커 · 정본 |
| `ac0c05047f3103dc6a29b9b9c70d9929c5044c8a` | 파싱 |
| `29b07ceb2a5838b59f81446582c5c95d2bfd16f9` | regression · 마이그레이션 · 캐시 · 스키마 |
| `4bd632f9765d8cd2a37afbb154f797239f5ddbf3` | regression · 앵커 · 게이트 |
| `f20ce31f0150631ce8640297b9739915e2f716e4` | regression · 마이그레이션 · 직렬화 · 앵커 |
| `ef451720b59360cebea00a7e6e3700bd44d005fc` | regression · baseline · 정본 |
| `3e238ea65656833623f67ee3662c12bce2fdd963` | regression |
| `6e45bcda7ea4e792d015f8b24133bd61a822df77` | 정본 |
| `6f8b83cccc225ff704bc0ecb2da3d4c9eba5ab12` | 승격 |
| `0184fae16ff1ccde8387b8824f69177a57b66596` | 파싱 · 게이트 · 승격 |
| `0bfa2689a2ca16829f275be9908fee2d73f16a5a` | 파싱 · 게이트 · 정본 · 승격 |
| `c5cdec93d7498db7f89f48f166909fd2eafd15d5` | baseline · 게이트 · 승격 |
| `6ce20e6ad7a732bd9a8e39856ef3a40ff47d40c6` | 스키마 · 직렬화 · 게이트 · 승격 |
| `2b9f8b2806f86be0ea58046c4c6970b53fd816af` | 게이트 |
| `562c53cab7b383d5d25aadd5ff702df8b1818a31` | 승격 |
| `644e2df2af134e580aa3944490dbd1070c865467` | 스캐폴딩 |
| `1def4cb0a42d54d27e8ae5dc835aa455c0d16699` | 스키마 · 스캐폴딩 |
| `03d2c033e59de94cff5d5fe7ea9666e3ad6455e1` | 승격 · 스캐폴딩 |
| `cf23bd527c47921fc7f328a9a68b2c67e4b0cbd1` | false positive |
| `f6a29b46d5dedf092821315c9ef58352fa51c287` | 승격 |
| `68e5e95a85dc27b167f5bc923a0332ff96febb16` | API |
| `ed20292f0cf513cba30de5ab514dbf16f677126e` | 표면 |
| `db81c1cb1e8fa70202a161dfa4337956907e2e6c` | 캐시 |
| `57763b9d9cc919f411b76560d69851a9a33355c8` | 폴링 · 게이트 |
| `a964abc29d216dbbfd58cecb85b1c29305ec04de` | 승격 |
| `7e3b69e1d3b8af9a5adb9565ddfccb6be9bf5b31` | 승격 |
| `3b980543eda7925759e1cea8e1493e0c9b089fe8` | API · 게이트 · 스캐폴딩 |
| `8f83528b5c39fde217462e1f3ef4ee125a0b7939` | sentinel · 파싱 |
| `f5a760f7c43438aeffbb22f03f65b7c92f89e803` | 승격 |
| `5b6a84448e6a3118a463adf6cc1303b910a2e6d5` | 마이그레이션 |
| `e6c692e28c5fe9ef61392bbca7ae4e4ed9cd31d7` | 스키마 |
| `4faaafec85ff88f7566b4cf0cde2d7f53b6a5cef` | 승격 |
| `f9a8c85db87ab15836c5e250f8cdabd3a2e60fa0` | regression · 멱등성 · 마이그레이션 · 해시 |
| `9c59a23567833490b9859b6d5f2833015b60027d` | 승격 |
| `201e8e235df700ad587ca6b51897e75772cae1fd` | regression |
| `9e4a42c4345159b2c0d8854ff30610cc26923f2b` | API · 인증 · 승격 |
| `1df7aa26d584c88d266fef9ba50c947ee0dc0699` | 마이그레이션 |
| `a0b83fbffa0a549145339bb40cdd5a48714cada8` | regression |
| `03f903cbe950aad182617a657fce2e2534c21c15` | 승격 |
| `7b73e7bfb66b51e8755c950d3d4e6c5bf3c35f26` | API |
| `aa8e1140714fd58fec4bb924708d0cf8a4d4a9ed` | API · 승격 |
| `1896c80362db94e4ed8d6e530bd27397cfc74455` | gRPC · REST · API |
| `929b3b115d2d6e1a4e2bebfb4ef5478290c2cf48` | baseline · 스키마 |
| `515b66a725b8bbef3cf864e8a54b385da4e24f5d` | regression |
| `f120396fb122234b90d184379bb96006b8c76497` | regression · false positive · baseline |
| `21203d83651b266575898f82fc9a9a7c519e35f5` | 파싱 |
| `ba2b8d951b3d1e022fadd31be80cca2e08e90cff` | 스키마 |
| `4587154007bd0c8cb3ff8bb5dfa0b354f4812c53` | 스키마 |
| `276ebeeade42d0367c74dde8ee5c43bdfb0fb412` | false positive |
| `a8840e42ef18d33d874324574e154e451d4c2180` | false positive |
| `ec00e20b3bdfa42280d284c0714d2eb0d80bfce7` | regression · false positive |
| `a45a7b73f39db4e58d887b6d19558c77fa90582e` | regression · 인덱스 |
| `31808d48ccc8c17f64a4f1f816fdb6ab02798302` | false positive |
| `21be3fa1499a222684d6149671b37cd96e001ffa` | 캐시 |
| `f1d7efe1c9090f6817e77a2b452603f3036750f6` | 파싱 |
| `0ea8da930358a04643b047bdd54356c64a53f213` | 오케스트레이션 |
| `5d9d1c53725197af17f13d1ca2f875325c1be770` | 게이트 |
| `3666e5a24e03f3bda0c4bbaf05a3164bb1b57977` | 게이트 |
| `fb41712cb9d6d8cae241a265030b2d143dddde6d` | 프리미티브 |
| `6df43f4d320bae1a2f1f2bfd26ef4652de36faa9` | blocklist |
| `2cc7ef79a2de4941580ffb05f8afc479388b28b9` | API · 스캐폴딩 |
| `bda15e3491ae7fadb14d33f687976b3da4a48974` | API |
| `6159b98720ec70c1eac69ff8b76147dc9a1b8d02` | API |
| `a8edc63bd8797d370b756dea5455897ca442c728` | 스캐폴딩 |
| `76fa1245ab90f51e747cd463f3146e6995fbfb1c` | API |
| `0e424cdd889e4d1b9086474061c900aa8c64422b` | API |
| `2d9b8894b450a2c428a3fdebcbfb063b1679845f` | gRPC · 마이그레이션 |
| `f659210021ff8b3b212cd7113fcbc70d43898aee` | 인증 |
| `e6286e197946b030047ae7c45bd2c1d647d0fefd` | gRPC · 인증 |
| `8c8009de2df44cc6fd84f778fc3a283a90a02c13` | 스캐폴딩 |
| `49ec681c1776407cde6cb3168c395c4322f4bc45` | 스캐폴딩 |
| `1628c9adea2dbdf3a6eae348272201098601e0f8` | 승격 |
| `7d003a055ec18a2252dcf8d94d6d3a171f4b00d4` | 스키마 |
| `1809965f1494a0818653e04ea1f8b092d5b10288` | regression |
| `e26b64cb14ea793b1e7f95b53b7fa4a19c4f54ec` | 오케스트레이션 |
| `988d7340ac1fa0ee3d33994330410430f31b33c5` | 스캐폴딩 |
| `fc510562ad8eba1ec95efc8a75212c0e2a6ef643` | 타임아웃 |
| `3862346bfde384426475c9982f857b5d01c6f4bb` | 아키타입 · 스캐폴딩 |
| `73810a950abcef7bdd7b805d8c76a26456092764` | API |
| `2b70a7d5e6ea141a0a73e34a5732b2372e180c78` | 마이그레이션 |
| `4b43f8f6171d3827bf89db035f3d982bbc52c3a2` | 마이그레이션 |
