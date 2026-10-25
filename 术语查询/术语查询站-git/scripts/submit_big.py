#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""提交梅德明百科全书 4 个分段到 MinerU"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mineru_client import _req, put_file

OUT = r"D:\WorkBuddy工作区\02-语言学站点\术语查询站"
RAW = os.path.join(OUT, "raw")

with open(os.path.join(RAW, "meidemin_parts.json"), encoding="utf-8") as f:
    parts = json.load(f)

files = []
for i, p in enumerate(parts, 1):
    files.append({
        "name": f"meidemin_part{i}.pdf",
        "is_ocr": True,
        "data_id": f"meidemin_p{i}",
        "language": "ch",
    })

payload = {
    "enable_formula": False,
    "enable_table": True,
    "model_version": "pipeline",
    "files": files,
}

code, resp = _req("POST", "/file-urls/batch", payload)
print("apply:", code, json.dumps(resp, ensure_ascii=False)[:300])
if code != 200 or resp.get("code") != 0:
    sys.exit(1)

batch_id = resp["data"]["batch_id"]
urls = resp["data"]["file_urls"]

ok = True
for p, f_meta, u in zip(parts, files, urls):
    path = p["file"]
    print("uploading", f_meta["name"], f"{p['mb']}MB", flush=True)
    r = put_file(u, path)
    print("  ->", r, flush=True)
    if r != 200:
        ok = False

state = {"batch_id": batch_id, "jobs": [{"name": f["name"], "key": f["data_id"]} for f in files],
         "parts": parts}
with open(os.path.join(OUT, "batch_big.json"), "w", encoding="utf-8") as fp:
    json.dump(state, fp, ensure_ascii=False, indent=2)
print("BATCH_ID:", batch_id, "all_ok:", ok)
