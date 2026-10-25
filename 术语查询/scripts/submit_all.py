#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""按 manifest 分批提交全部分段到 MinerU（支持断点续传）"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mineru_client import _req, put_file

OUT = r"D:\WorkBuddy工作区\02-语言学站点\术语查询站"
RAW = os.path.join(OUT, "raw")
STATE = os.path.join(OUT, "submit_state.json")
GROUP = int(os.environ.get("GROUP_SIZE", "5"))

with open(os.path.join(RAW, "manifest.json"), encoding="utf-8") as f:
    manifest = json.load(f)

state = {"batches": [], "submitted": {}}
if os.path.exists(STATE):
    with open(STATE, encoding="utf-8") as f:
        state = json.load(f)

pending = [m for m in manifest if m["name"] not in state["submitted"]]
print(f"pending {len(pending)} / total {len(manifest)}", flush=True)

for i in range(0, len(pending), GROUP):
    grp = pending[i:i + GROUP]
    files = [{
        "name": m["name"],
        "is_ocr": True,
        "data_id": m["name"].replace(".pdf", ""),
        "language": m["lang"],
    } for m in grp]
    payload = {
        "enable_formula": False,
        "enable_table": True,
        "model_version": "pipeline",
        "files": files,
    }
    code, resp = _req("POST", "/file-urls/batch", payload)
    if code != 200 or resp.get("code") != 0:
        print("apply FAIL", code, str(resp)[:300], flush=True)
        break
    bid = resp["data"]["batch_id"]
    urls = resp["data"]["file_urls"]
    print(f"batch {bid} <- {[m['name'] for m in grp]}", flush=True)
    okall = True
    for m, u in zip(grp, urls):
        r = put_file(u, m["file"])
        print(f"  upload {m['name']} ({m['mb']}MB) -> {r}", flush=True)
        if r == 200:
            state["submitted"][m["name"]] = {"batch_id": bid, "book": m["book"],
                                             "seq": m["seq"], "page_start": m["page_start"],
                                             "page_end": m["page_end"]}
        else:
            okall = False
    if bid not in state["batches"]:
        state["batches"].append(bid)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    if not okall:
        print("some uploads failed in this group", flush=True)

print("submitted total:", len(state["submitted"]), flush=True)
print("batches:", state["batches"], flush=True)
