// 놀이터를 실제 구글 크롬으로 띄워 조작하고 판정한다. 사용: node web_check.js <주소> <캡처 폴더>
// 화면 글자는 접근성 트리(Flutter 시맨틱)로 찾는다 — 진입 파일이 시맨틱을 켠다.
const { chromium } = require('playwright-core');
const exe = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const [url, out] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({ executablePath: exe });
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  p.on('pageerror', (e) => errs.push(String(e)));
  p.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
  const steps = [];
  const has = async (t) => (await p.getByText(t, { exact: false }).count()) > 0;
  const step = async (name, ok) => { steps.push([name, ok]); console.log(`${ok ? 'OK' : 'NG'} ${name}`); };
  await p.goto(url); await p.waitForTimeout(7000);
  await p.screenshot({ path: `${out}/1-first.png` });
  await step('첫 화면에 위젯 목록(IFButton)과 종류 칸이 보인다', (await has('IFButton')) && (await has('종류')));
  await step('코드 칸이 없다', (await p.getByText('Code', { exact: true }).count()) === 0 && (await p.getByText('코드', { exact: true }).count()) === 0);
  // 열린 위젯 제목은 「<클래스>.<종류>」 모양이다. 누르기 전에는 IFMiniButton. 으로 시작하는 제목이 없어야 한다
  const title = async (re) => p.getByText(re).count();
  const before = await title(/^IFMiniButton\./);
  await p.getByText('IFMiniButton', { exact: true }).first().click(); await p.waitForTimeout(1500);
  await p.screenshot({ path: `${out}/2-widget.png` });
  const after = await title(/^IFMiniButton\./);
  console.log(`  IFMiniButton 제목 수 ${before} → ${after}`);
  await step('목록에서 IFMiniButton 을 누르면 그 위젯이 열린다', before === 0 && after >= 1);
  await p.getByRole('button', { name: /종류/ }).first().click(); await p.waitForTimeout(800);
  await p.getByText('secondary', { exact: true }).last().click(); await p.waitForTimeout(1200);
  await p.screenshot({ path: `${out}/3-variant.png` });
  await step('종류 드롭다운에서 secondary 를 고르면 IFMiniButton.secondary 가 된다', await has('IFMiniButton.secondary'));
  await p.getByRole('switch', { name: /held/ }).first().click(); await p.waitForTimeout(1000);
  await p.screenshot({ path: `${out}/4-prop.png` });
  await step('속성 held 를 바꾸면 기본값으로 되돌리기가 생긴다', (await p.getByRole('button', { name: /기본값으로/ }).count()) >= 1);
  // IFMiniButton 은 목록에서 content 보기로 열린다. 휴대폰 화면으로 바꾸면 크기 글자의 가로가 휴대폰 폭(320·375·390·430)이 된다
  const sizes = async () => (await p.getByText(/^\d+ × \d+$/).allInnerTexts()).map((t) => t.trim());
  const s0 = await sizes();
  await p.getByRole('button', { name: /휴대폰 화면/ }).first().click(); await p.waitForTimeout(1200);
  await p.screenshot({ path: `${out}/5-view.png` });
  const s1 = await sizes();
  console.log(`  크기 글자 ${JSON.stringify(s0)} → ${JSON.stringify(s1)}`);
  const phone = s1.some((t) => /^(320|375|390|430) × \d+$/.test(t));
  await step('보기를 휴대폰 화면으로 바꾸면 영역 크기 숫자(가로 × 세로)의 가로가 휴대폰 폭이 된다', phone && JSON.stringify(s0) !== JSON.stringify(s1));
  const failed = steps.filter((s) => !s[1]).length;
  console.log(`errors ${errs.length}`); errs.slice(0, 5).forEach((e) => console.log('  ' + e.slice(0, 200)));
  console.log(`steps ${steps.length} failed ${failed}`);
  const ok = failed === 0 && steps.length === 6 && errs.length === 0;
  console.log(ok ? 'VERDICT PASS' : 'VERDICT FAIL 단계 또는 화면 오류');
  await b.close();
})().catch((e) => { console.log('VERDICT FAIL 실행 오류 ' + e); process.exit(0); });
