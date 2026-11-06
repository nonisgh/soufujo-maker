# Copy the AI prompt (the part after the paste marker in prompt.md) into index.html,
# so the page can copy/download it without fetching. Run after editing prompt.md.
import re, sys, pathlib
html_path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
md_path = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "prompt.md")
md = md_path.read_text(encoding="utf-8")
marker = "---------- ここから下をAIに貼りつける ----------"
rules = md.split(marker, 1)[1].strip() + "\n"
assert "</script" not in rules.lower()
html = html_path.read_text(encoding="utf-8")
block = '<!-- AI_RULES_START -->\n<script type="text/plain" id="aiRules">\n' + rules + '</script>\n<!-- AI_RULES_END -->'
html, n = re.subn(r"<!-- AI_RULES_START -->.*?<!-- AI_RULES_END -->", lambda m: block, html, flags=re.S)
assert n == 1
html_path.write_text(html, encoding="utf-8")
print("embedded", len(rules), "chars")
