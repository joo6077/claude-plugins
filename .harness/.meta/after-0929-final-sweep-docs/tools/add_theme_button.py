"""어두운 테마만 있던 쪽에 테마 단추와 단추 · 저장 · 복원 스크립트를 넣는다.

`python3 add_theme_button.py <docs 가 든 폴더> <쪽 목록 파일>` — 목록의 쪽마다 `<body…>` 바로 뒤에 붙인다.
이미 `class="dk-theme-btn"` 이 있는 쪽은 건너뛴다. 색은 `docs/assets/site.css` 가 준다.
"""
import re
import sys
from pathlib import Path

SNIPPET = """<button id="theme-btn" class="dk-theme-btn" type="button" aria-label="밝은 테마와 어두운 테마 바꾸기">◐</button>
<script>
// 저장 키는 dk-theme — 저장값이 없으면 브라우저 색 설정을 따른다 (docs-site Gotcha 13)
(function () {
  var root = document.documentElement;
  var button = document.getElementById('theme-btn');
  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    button.setAttribute('aria-pressed', String(theme === 'light'));
  }
  var saved = null;
  try { saved = localStorage.getItem('dk-theme'); } catch (err) { /* 저장소를 막은 브라우저 */ }
  applyTheme(saved === 'light' || saved === 'dark' ? saved
    : (matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'));
  button.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    try { localStorage.setItem('dk-theme', next); } catch (err) { /* 저장소를 막은 브라우저 */ }
    applyTheme(next);
  });
})();
</script>
"""


def main(root, listing):
    done = 0
    for rel in Path(listing).read_text(encoding="utf-8").split():
        page = Path(root) / rel
        h = page.read_text(encoding="utf-8")
        if 'class="dk-theme-btn"' in h:
            continue
        m = re.search(r"<body\b[^>]*>\n?", h)
        if not m:
            raise SystemExit(f"<body> 없음: {rel}")
        page.write_text(h[:m.end()] + SNIPPET + h[m.end():], encoding="utf-8")
        done += 1
    print(f"단추를 넣은 쪽 {done}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
