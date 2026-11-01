#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MinerU v4 API 客户端 —— 批量上传 + 轮询 + 下载解压"""
import os, sys, json, time, zipfile, io
import urllib.request, urllib.error

TOKEN = os.environ.get("MINERU_TOKEN", "").strip()
BASE = "https://mineru.net/api/v4"


def _req(method, path, payload=None, timeout=120):
    url = path if path.startswith("http") else BASE + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "*/*")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", "replace")
            return r.status, json.loads(body) if body.strip().startswith(("{", "[")) else body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        return e.code, body
    except Exception as e:
        return -1, str(e)


def batch_upload_urls(file_names, opts=None):
    """申请预签名上传链接"""
    opts = opts or {}
    files = []
    for n in file_names:
        item = {"name": os.path.basename(n)}
        item.update(opts.get(os.path.basename(n), {}))
        files.append(item)
    payload = {
        "enable_formula": False,
        "enable_table": True,
        "model_version": "pipeline",
        "files": files,
    }
    payload.update(opts.get("_global", {}))
    return _req("POST", "/file-urls/batch", payload)


def put_file(url, path):
    """PUT 上传到预签名地址。

    关键坑：OSS 预签名的 StringToSign 里 Content-Type 为空，
    而 urllib 在带 data 时会自动补 application/x-www-form-urlencoded，
    导致 SignatureDoesNotMatch。必须显式置空，且不能带 Authorization 头。
    """
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        body = f.read()
    req = urllib.request.Request(url, data=body, method="PUT")
    req.add_header("Content-Type", "")
    req.add_header("Content-Length", str(size))
    try:
        with urllib.request.urlopen(req, timeout=3600) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:500]


def batch_status(batch_id):
    return _req("GET", "/extract-results/batch/" + batch_id)


def download(url, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    with urllib.request.urlopen(url, timeout=1800) as r:
        buf = r.read()
    with zipfile.ZipFile(io.BytesIO(buf)) as z:
        z.extractall(dest_dir)
    return dest_dir


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "ping"
    if cmd == "ping":
        print(_req("POST", "/file-urls/batch", {"files": [{"name": "probe.pdf"}]}))
