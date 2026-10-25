#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把梅德明百科全书拆成若干段，每段 <= 450 页且 <= 190MB"""
import os, sys
from pypdf import PdfReader, PdfWriter

SRC = r"C:\Users\HUAWEI\Desktop\陈昌来老师书单\5、百科全书检索\语言学百科全书（梅德明）正文部分.pdf"
OUT = r"D:\WorkBuddy工作区\02-语言学站点\术语查询站\raw"
CHUNK = 350  # 页/段，控制体积

os.makedirs(OUT, exist_ok=True)
reader = PdfReader(SRC)
n = len(reader.pages)
print("total pages:", n)

parts = []
idx = 0
start = 0
while start < n:
    end = min(start + CHUNK, n)
    idx += 1
    w = PdfWriter()
    for i in range(start, end):
        w.add_page(reader.pages[i])
    out = os.path.join(OUT, f"meidemin_part{idx}.pdf")
    with open(out, "wb") as f:
        w.write(f)
    mb = os.path.getsize(out) / 1024 / 1024
    print(f"part{idx}: pages {start+1}-{end} -> {mb:.1f} MB  {out}")
    parts.append({"file": out, "start": start + 1, "end": end, "mb": round(mb, 1)})
    start = end

import json
with open(os.path.join(OUT, "meidemin_parts.json"), "w", encoding="utf-8") as f:
    json.dump(parts, f, ensure_ascii=False, indent=2)
print("DONE", len(parts), "parts")
