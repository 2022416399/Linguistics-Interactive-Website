#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""轮询 MinerU 批任务状态，完成即下载解压"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mineru_client import batch_status, download

OUT = r"D:\WorkBuddy工作区\02-语言学站点\术语查询站"
RESULT = os.path.join(OUT, "result")
os.makedirs(RESULT, exist_ok=True)

state_files = [f for f in sys.argv[1:]] or ["batch_small.json", "batch_big.json"]
batches = []
for sf in state_files:
    p = os.path.join(OUT, sf)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            batches.append((sf, json.load(f)))

done_marker = os.path.join(OUT, "downloaded.json")
downloaded = {}
if os.path.exists(done_marker):
    with open(done_marker, encoding="utf-8") as f:
        downloaded = json.load(f)

MAX_WAIT = 3 * 3600
t0 = time.time()

while time.time() - t0 < MAX_WAIT:
    all_done = True
    for sf, st in batches:
        bid = st["batch_id"]
        code, resp = batch_status(bid)
        if code != 200 or not isinstance(resp, dict) or resp.get("code") != 0:
            print(f"[{sf}] status err", code, str(resp)[:200], flush=True)
            all_done = False
            continue
        results = resp["data"].get("extract_result", [])
        for r in results:
            name = r.get("file_name") or r.get("data_id")
            stt = r.get("state")
            if stt == "done":
                key = f"{bid}::{name}"
                if key not in downloaded:
                    url = r.get("full_zip_url")
                    dest = os.path.join(RESULT, os.path.splitext(name)[0])
                    print(f"[{sf}] downloading {name} -> {dest}", flush=True)
                    try:
                        download(url, dest)
                        downloaded[key] = dest
                        with open(done_marker, "w", encoding="utf-8") as f:
                            json.dump(downloaded, f, ensure_ascii=False, indent=2)
                        print(f"[{sf}] OK {name}", flush=True)
                    except Exception as e:
                        print(f"[{sf}] download FAIL {name}: {e}", flush=True)
                        all_done = False
            elif stt in ("failed",):
                print(f"[{sf}] {name} FAILED: {r.get('err_msg')}", flush=True)
            else:
                prog = r.get("extract_progress") or {}
                ex = prog.get("extracted_pages")
                tp = prog.get("total_pages")
                extra = f" {ex}/{tp}p" if ex is not None else ""
                print(f"[{sf}] {name}: {stt}{extra}", flush=True)
                all_done = False
    if all_done:
        print("ALL DONE", flush=True)
        break
    print("--- waiting 60s ---", flush=True)
    time.sleep(60)
else:
    print("TIMEOUT", flush=True)
