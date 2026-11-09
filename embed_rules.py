# Copy the AI prompts (the part after the paste marker) into index.html, so the page can copy/download them
# without fetching. Run after editing prompt.md or prompt_receipt.md.
#   prompt.md          -> <script id="aiRules">        between AI_RULES_START / AI_RULES_END
#   prompt_receipt.md  -> <script id="aiRulesReceipt"> between AI_RECEIPT_RULES_START / AI_RECEIPT_RULES_END
#   prompt_tegami.md   -> <script id="aiRulesTegami">  between AI_TEGAMI_RULES_START / AI_TEGAMI_RULES_END
import re, sys, pathlib
html_path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
marker = "---------- ここから下をAIに貼りつける ----------"
html = html_path.read_text(encoding="utf-8")
for md_name, tag, script_id in [("prompt.md", "AI_RULES", "aiRules"), ("prompt_receipt.md", "AI_RECEIPT_RULES", "aiRulesReceipt"), ("prompt_tegami.md", "AI_TEGAMI_RULES", "aiRulesTegami")]:
    md = pathlib.Path(md_name).read_text(encoding="utf-8")
    rules = md.split(marker, 1)[1].strip() + "\n"
    assert "</script" not in rules.lower()
    block = f'<!-- {tag}_START -->\n<script type="text/plain" id="{script_id}">\n' + rules + f'</script>\n<!-- {tag}_END -->'
    pattern = rf"<!-- {tag}_START -->.*?<!-- {tag}_END -->"
    if not re.search(pattern, html, flags=re.S):
        # first run for this prompt: add an empty slot right after the main rules block
        html = html.replace("<!-- AI_RULES_END -->", f"<!-- AI_RULES_END -->\n<!-- {tag}_START --><!-- {tag}_END -->", 1)
    html, n = re.subn(pattern, lambda m: block, html, flags=re.S)
    assert n == 1, tag
    print("embedded", md_name, len(rules), "chars")
html_path.write_text(html, encoding="utf-8")
