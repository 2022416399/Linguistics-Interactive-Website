# -*- coding: utf-8 -*-
"""发布站点全量验证：链接可达、无中文文件名残留、零外部依赖、标签配对、脚本可提取。"""
import os
import re
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "发布站点")
files = sorted(f for f in os.listdir(OUT) if f.endswith(".html"))
errors = []

# 1) href 目标核验 + 中文文件名残留
CN_RESIDUE = re.compile(r"认知语言学与汉语名词短语-(?:\d|第[一二三四五六七八]章)")
all_targets = set()
for f in files:
    p = os.path.join(OUT, f)
    html = open(p, encoding="utf-8").read()
    if CN_RESIDUE.search(html):
        errors.append("%s: 残留中文文件名" % f)
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith(("http://", "https://", "mailto:", "#", "data:")):
            continue
        if href.endswith(".html"):
            all_targets.add((f, href))
            if not os.path.isfile(os.path.join(OUT, href)):
                errors.append("%s: 死链 -> %s" % (f, href))
    for src in re.findall(r'src="([^"]+)"', html):
        if src.startswith(("http://", "https://", "data:")):
            errors.append("%s: 外部 src -> %s" % (f, src))

# 2) 外部依赖
for f in files:
    html = open(os.path.join(OUT, f), encoding="utf-8").read()
    for pat in (r'src="https?://', r'href="https?://', r'@import', r'url\(https?://', r'<link[^>]+href="https?://'):
        if re.search(pat, html):
            errors.append("%s: 外部依赖 %s" % (f, pat))

# 3) 标签配对
VOID = {"meta", "link", "br", "hr", "img", "input", "source", "col", "area", "base", "wbr", "embed", "track", "param"}
for f in files:
    html = open(os.path.join(OUT, f), encoding="utf-8").read()
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.S | re.I)
    stack = []
    for m in re.finditer(r"<(/?)([a-zA-Z][a-zA-Z0-9-]*)([^>]*?)(/?)>", html):
        closing, tag, attrs, selfclose = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if tag in VOID or selfclose:
            continue
        if closing:
            if not stack:
                errors.append("%s: 多余闭标签 </%s>" % (f, tag))
            elif stack[-1] != tag:
                errors.append("%s: 标签交叉 <%s> vs </%s>" % (f, stack[-1], tag))
                stack.pop()
            else:
                stack.pop()
        else:
            stack.append(tag)
    if stack:
        errors.append("%s: 未闭合标签 %s" % (f, stack[:8]))

# 4) 脚本可提取（交 node --check）
os.makedirs("_verify", exist_ok=True)
js_files = []
for f in files:
    html = open(os.path.join(OUT, f), encoding="utf-8").read()
    for i, m in enumerate(re.finditer(r"<script[^>]*>(.*?)</script>", html, flags=re.S)):
        code = m.group(1)
        if not code.strip():
            continue
        jf = os.path.join("_verify", "%s.%d.js" % (f.replace(".html", ""), i))
        open(jf, "w", encoding="utf-8").write(code)
        js_files.append(jf)

print("HTML 文件: %d" % len(files))
print("链接条目（源 -> 目标）: %d 条，全部目标存在" % len(all_targets))
print("提取脚本: %d 个" % len(js_files))
print("")
if errors:
    print("!! 发现 %d 个问题:" % len(errors))
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("== 静态核验全部通过 ==")
for f in files:
    print("  OK", f)
print("JS_LIST:" + "|".join(js_files))
