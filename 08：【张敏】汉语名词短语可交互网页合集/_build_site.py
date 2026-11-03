# -*- coding: utf-8 -*-
"""搭建「发布站点」：9 深读 + 8 简版 + index 共 18 个 HTML，ASCII 文件名，全站链接重映射，插入 favicon。"""
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "发布站点")

MAPPING = [
    # 深读九篇
    ("认知语言学与汉语名词短语-01深读-理论主张.html", "01-theory.html"),
    ("认知语言学与汉语名词短语-02深读-范畴化.html", "02-categorization.html"),
    ("认知语言学与汉语名词短语-03深读-句法的象似性.html", "03-iconicity.html"),
    ("认知语言学与汉语名词短语-03深读-重叠动因.html", "03-reduplication.html"),
    ("认知语言学与汉语名词短语-04深读-下篇概述.html", "04-part2-overview.html"),
    ("认知语言学与汉语名词短语-05深读-距离动因.html", "05-distance.html"),
    ("认知语言学与汉语名词短语-06深读-的字隐现.html", "06-de-particle.html"),
    ("认知语言学与汉语名词短语-07深读-领属结构.html", "07-possession.html"),
    ("认知语言学与汉语名词短语-08深读-定语语序.html", "08-attributive-order.html"),
    # 简版八章
    ("认知语言学与汉语名词短语-第一章-理论主张.html", "ch1-theory.html"),
    ("认知语言学与汉语名词短语-第二章-经验基础.html", "ch2-basis.html"),
    ("认知语言学与汉语名词短语-第三章-句法的象似性.html", "ch3-iconicity.html"),
    ("认知语言学与汉语名词短语-第四章-下篇概述.html", "ch4-overview.html"),
    ("认知语言学与汉语名词短语-第五章-距离动因与语义差别.html", "ch5-distance.html"),
    ("认知语言学与汉语名词短语-第六章-的字隐现.html", "ch6-de.html"),
    ("认知语言学与汉语名词短语-第七章-领属结构.html", "ch7-possession.html"),
    ("认知语言学与汉语名词短语-第八章-定语语序.html", "ch8-order.html"),
]
# 长名优先，避免前缀互吃
MAPPING.sort(key=lambda kv: len(kv[0]), reverse=True)

FAVICON = (
    b"<link rel=\"icon\" href=\"data:image/svg+xml,"
    b"%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
    b"%3Ccircle cx='32' cy='32' r='26' fill='none' stroke='%239e3b2e' stroke-width='6'/%3E"
    b"%3C/svg%3E\">"
)
ANCHORS = [b"<meta charset=\"utf-8\">", b"<meta charset=\"UTF-8\">"]

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

# 1) 拷贝并改名
for old, new in MAPPING:
    shutil.copyfile(os.path.join(ROOT, old), os.path.join(OUT, new))
shutil.copyfile(os.path.join(ROOT, "index.html"), os.path.join(OUT, "index.html"))

# 2) 链接重映射 + favicon（二进制级操作，保留原始字节与行尾）
files = ["index.html"] + [new for _, new in MAPPING]
print("%-24s %-10s %s" % ("file", "favicon", "links remapped"))
for name in files:
    p = os.path.join(OUT, name)
    with open(p, "rb") as f:
        data = f.read()
    remapped = []
    for old, new in MAPPING:
        ob, nb = old.encode("utf-8"), new.encode("utf-8")
        c = data.count(ob)
        if c:
            data = data.replace(ob, nb)
            remapped.append("%s->%s x%d" % (old.split("-", 1)[1][:12], new, c))
    if b'rel="icon"' in data:
        fav = "exists"
    else:
        fav = "NO-ANCHOR!"
        for anchor in ANCHORS:
            if anchor in data:
                data = data.replace(anchor, anchor + b"\n" + FAVICON, 1)
                fav = "inserted"
                break
    with open(p, "wb") as f:
        f.write(data)
    print("%-24s %-10s %s" % (name, fav, "; ".join(remapped) if remapped else "(none)"))

# 3) .nojekyll（空文件，阻止 GitHub Pages 走 Jekyll 处理）
with open(os.path.join(OUT, ".nojekyll"), "wb") as f:
    f.write(b"")

print("\nOUT:", OUT)
