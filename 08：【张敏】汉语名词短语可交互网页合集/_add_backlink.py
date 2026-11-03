# -*- coding: utf-8 -*-
"""给 8 个简版页插入悬浮「返回全书导览」按钮（零外部依赖、内联样式）。"""
import io, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))

LINK = ('<a href="index.html" title="返回全书导览" style="position:fixed;left:12px;bottom:14px;'
        'z-index:9999;display:inline-flex;align-items:center;gap:4px;font:13px/1.4 system-ui,'
        "'Microsoft YaHei',sans-serif;color:#5a5348;background:rgba(255,253,246,.94);"
        'border:1px solid #d8d1c2;border-radius:999px;padding:6px 13px;text-decoration:none;'
        'box-shadow:0 2px 10px rgba(35,32,28,.12);backdrop-filter:blur(2px)">'
        '\u2190 返回全书导览</a>')

FILES = [
    "认知语言学与汉语名词短语-第一章-理论主张.html",
    "认知语言学与汉语名词短语-第二章-经验基础.html",
    "认知语言学与汉语名词短语-第三章-句法的象似性.html",
    "认知语言学与汉语名词短语-第四章-下篇概述.html",
    "认知语言学与汉语名词短语-第五章-距离动因与DN、DdN语义差别.html",
    "认知语言学与汉语名词短语-第六章-的字隐现的一般规律.html",
    "认知语言学与汉语名词短语-第七章-领属结构的的与语言共性.html",
    "认知语言学与汉语名词短语-第八章-多项定语的语序规律.html",
]

def insert(path):
    with io.open(path, "r", encoding="utf-8") as f:
        html = f.read()
    if "返回全书导览" in html:
        return "SKIP(已有)"
    # 类型 B：body 与 topbar 同行
    if "<body><header" in html:
        new = html.replace("<body><header", "<body>" + LINK + "<header", 1)
    # 类型 A：body 独立成行
    elif "<body>\n" in html:
        new = html.replace("<body>\n", "<body>\n" + LINK + "\n", 1)
    else:
        # 兜底：body 后无换行
        i = html.find("<body>")
        if i < 0:
            return "FAIL(无 body)"
        new = html[:i+6] + "\n" + LINK + "\n" + html[i+6:]
    if new == html:
        return "FAIL(未变化)"
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    return "OK"

for name in FILES:
    p = os.path.join(BASE, name)
    print(name, "->", insert(p))
