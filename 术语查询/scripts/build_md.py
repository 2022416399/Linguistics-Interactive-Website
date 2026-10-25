#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把各分段 full.md 按顺序拼成整本书的 Markdown"""
import os, json, re, sys

OUT = r"D:\WorkBuddy工作区\02-语言学站点\术语查询站"
RESULT = os.path.join(OUT, "result")
MD = os.path.join(OUT, "md")
os.makedirs(MD, exist_ok=True)

with open(os.path.join(OUT, "raw", "manifest.json"), encoding="utf-8") as f:
    manifest = json.load(f)

books = {}
for m in manifest:
    books.setdefault(m["book"], {"title": m["title"], "author": m["author"],
                                 "lang": m["lang"], "chunks": []})
    books[m["book"]]["chunks"].append(m)

summary = []
for key, b in books.items():
    b["chunks"].sort(key=lambda x: x["seq"])
    parts, missing, total_pages = [], [], 0
    for c in b["chunks"]:
        p = os.path.join(RESULT, c["name"].replace(".pdf", ""), "full.md")
        if not os.path.exists(p):
            missing.append(c["name"])
            continue
        txt = open(p, encoding="utf-8").read()
        parts.append(f"\n\n<!--CHUNK seq={c['seq']} pages={c['page_start']}-{c['page_end']}-->\n\n" + txt)
        total_pages += c["page_end"] - c["page_start"] + 1
    body = "".join(parts)
    header = (f"---\ntitle: {b['title']}\nauthor: {b['author']}\n"
              f"lang: {b['lang']}\npages: {total_pages}\nsource: MinerU OCR\n---\n")
    dest = os.path.join(MD, f"{key}.md")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(header + body)
    mb = os.path.getsize(dest) / 1024 / 1024
    summary.append({"book": key, "title": b["title"], "chars": len(body),
                    "mb": round(mb, 2), "pages": total_pages, "missing": missing})
    print(f"{key}: {len(body):,} chars, {mb:.2f}MB, {total_pages}p"
          + (f"  MISSING {missing}" if missing else ""))

with open(os.path.join(MD, "_summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
