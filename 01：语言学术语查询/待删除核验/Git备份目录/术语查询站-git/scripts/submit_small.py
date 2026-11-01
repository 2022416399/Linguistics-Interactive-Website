#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""提交两本小词典到 MinerU"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mineru_client import _req, put_file

BASE_DIR = r"C:\Users\HUAWEI\Desktop\陈昌来老师书单\5、百科全书检索"
OUT = r"D:\WorkBuddy工作区\02-语言学站点\术语查询站"

JOBS = [
    {
        "path": os.path.join(BASE_DIR, "牛津语言学词典 英文本 (（英）马修斯（MatthewsP.H.）编 etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"),
        "name": "oxford_concise_linguistics.pdf",
        "language": "en",
        "key": "oxford",
    },
    {
        "path": os.path.join(BASE_DIR, "现代语言学词典 (（英）戴维·克里斯特尔（David Crystal）编；沈家煊译 etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf"),
        "name": "crystal_modern_linguistics_cn.pdf",
        "language": "ch",
        "key": "crystal",
    },
]

payload = {
    "enable_formula": False,
    "enable_table": True,
    "model_version": "pipeline",
    "files": [{"name": j["name"], "is_ocr": True, "data_id": j["key"], "language": j["language"]} for j in JOBS],
}

code, resp = _req("POST", "/file-urls/batch", payload)
print("apply:", code, json.dumps(resp, ensure_ascii=False)[:400])
if code != 200 or resp.get("code") != 0:
    sys.exit(1)

batch_id = resp["data"]["batch_id"]
urls = resp["data"]["file_urls"]

for j, u in zip(JOBS, urls):
    print("uploading", j["name"], os.path.getsize(j["path"]) / 1024 / 1024, "MB")
    r = put_file(u, j["path"])
    print("  ->", r)

state = {"batch_id": batch_id, "jobs": [{"name": j["name"], "key": j["key"]} for j in JOBS]}
with open(os.path.join(OUT, "batch_small.json"), "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print("BATCH_ID:", batch_id)
