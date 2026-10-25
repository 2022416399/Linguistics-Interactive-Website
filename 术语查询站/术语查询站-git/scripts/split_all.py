#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""按 180 页/段拆分全部三本书（MinerU 账户限制 200 页/文件）"""
import os, json
from pypdf import PdfReader, PdfWriter

BASE = r"C:\Users\HUAWEI\Desktop\陈昌来老师书单\5、百科全书检索"
OUT = r"D:\WorkBuddy工作区\02-语言学站点\术语查询站\raw"
CHUNK = 180

BOOKS = [
    {
        "key": "oxford",
        "title": "牛津语言学词典（英文本）",
        "author": "P. H. Matthews",
        "lang": "en",
        "src": os.path.join(BASE, "牛津语言学词典 英文本 (（英）马修斯（MatthewsP.H.）编 etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"),
    },
    {
        "key": "crystal",
        "title": "现代语言学词典",
        "author": "David Crystal 著 / 沈家煊 译",
        "lang": "ch",
        "src": os.path.join(BASE, "现代语言学词典 (（英）戴维·克里斯特尔（David Crystal）编；沈家煊译 etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"),
    },
    {
        "key": "meidemin",
        "title": "语言学与应用语言学百科全书",
        "author": "梅德明 主编",
        "lang": "ch",
        "src": os.path.join(BASE, "语言学百科全书（梅德明）正文部分.pdf"),
    },
]

os.makedirs(OUT, exist_ok=True)
manifest = []

for b in BOOKS:
    reader = PdfReader(b["src"])
    n = len(reader.pages)
    print(f"== {b['key']}: {n} pages", flush=True)
    idx = 0
    start = 0
    while start < n:
        end = min(start + CHUNK, n)
        idx += 1
        w = PdfWriter()
        for i in range(start, end):
            w.add_page(reader.pages[i])
        name = f"{b['key']}_p{idx:02d}.pdf"
        out = os.path.join(OUT, name)
        with open(out, "wb") as f:
            w.write(f)
        mb = os.path.getsize(out) / 1024 / 1024
        print(f"   {name}: {start+1}-{end} ({end-start}p, {mb:.1f}MB)", flush=True)
        manifest.append({
            "book": b["key"], "title": b["title"], "author": b["author"],
            "lang": b["lang"], "name": name, "file": out,
            "seq": idx, "page_start": start + 1, "page_end": end, "mb": round(mb, 1),
        })
        start = end

with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print("TOTAL CHUNKS:", len(manifest))
print("TOTAL PAGES:", sum(m["page_end"] - m["page_start"] + 1 for m in manifest))
