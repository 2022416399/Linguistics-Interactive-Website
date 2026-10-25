#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""轮询 submit_state.json 里所有 batch，完成即下载解压（断点续传）"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mineru_client import batch_status, download

OUT = r"D:\WorkBuddy工作区\02-语言学站点\术语查询站"
RESULT = os.path.join(OUT, "result")
STATE = os.path.join(OUT, "submit_state.json")
MARK = os.path.join(OUT, "downloaded.json")
os.makedirs(RESULT, exist_ok=True)

downloaded = {}
if os.path.exists(MARK):
    with open(MARK, encoding="utf-8") as f:
        downloaded = json.load(f)

MAX_WAIT = int(os.environ.get("MAX_WAIT", 4 * 3600))
t0 = time.time()

while time.time() - t0 < MAX_WAIT:
    with open(STATE, encoding="utf-8") as f:
        st = json.load(f)
    expected = set(st["submitted"].keys())
    batches = st["batches"]

    all_done = True
    seen = set()
    for bid in batches:
        code, resp = batch_status(bid)
        if code != 200 or not isinstance(resp, dict) or resp.get("code") != 0:
            print(f"[{bid[:8]}] err {code} {str(resp)[:150]}", flush=True)
            all_done = False
            continue
        for r in resp["data"].get("extract_result", []):
            name = r.get("file_name") or (r.get("data_id", "") + ".pdf")
            seen.add(name)
            stt = r.get("state")
            if stt == "done":
                if name in downloaded:
                    continue
                dest = os.path.join(RESULT, os.path.splitext(name)[0])
                print(f"  ↓ {name}", flush=True)
                try:
                    download(r["full_zip_url"], dest)
                    downloaded[name] = dest
                    with open(MARK, "w", encoding="utf-8") as f:
                        json.dump(downloaded, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    print(f"  ! download fail {name}: {e}", flush=True)
                    all_done = False
            elif stt == "failed":
                print(f"  ✗ {name} FAILED: {r.get('err_msg')}", flush=True)
                downloaded[name] = None
            else:
                p = r.get("extract_progress") or {}
                ex, tp = p.get("extracted_pages"), p.get("total_pages")
                print(f"  · {name}: {stt}" + (f" {ex}/{tp}p" if ex is not None else ""), flush=True)
                all_done = False

    missing = expected - seen
    if missing:
        print("  ? not yet listed:", sorted(missing), flush=True)
        all_done = False

    ok = sum(1 for v in downloaded.values() if v)
    print(f"--- done {ok}/{len(expected)} ---", flush=True)
    if all_done:
        print("ALL DONE", flush=True)
        break
    time.sleep(45)
else:
    print("TIMEOUT", flush=True)
