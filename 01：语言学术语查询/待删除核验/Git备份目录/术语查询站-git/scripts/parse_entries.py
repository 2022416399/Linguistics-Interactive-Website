#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""从 OCR Markdown 中切分术语词条，输出结构化 JSON

三本书版式各异：
  oxford   : `headword [IPA]. 定义`            —— 英文，按字母序
  crystal  : `english 中文译名 释义`            —— 英汉对照，按英文字母序
  meidemin : `中文词目 English term 释义`       —— 中文百科，按拼音序

页码说明：MinerU 输出没有逐页标记，因此按段落在该 CHUNK 中的线性位置估算页码，
精度通常 ±1-2 页，足够核对原始扫描件。
"""
import os, re, json, sys, unicodedata

OUT = r"D:\WorkBuddy工作区\02-语言学站点\术语查询站"
MD = os.path.join(OUT, "md")
DATA = os.path.join(OUT, "data")
os.makedirs(DATA, exist_ok=True)

CJK = r"\u4e00-\u9fff"
IMG_RE = re.compile(r"!\[\]\([^)]*\)")
CHUNK_RE = re.compile(r"<!--CHUNK seq=(\d+) pages=(\d+)-(\d+)-->")

# OCR 常见误识：土耳其无点 ı 实为英文 i（crystal 625 处 / oxford 116 处）
OCR_FIX = str.maketrans({"ı": "i", "İ": "I", "ﬁ": "fi", "ﬂ": "fl",
                         "‚": ",", "―": "—", "\u00a0": " "})


# ---------------------------------------------------------------- 通用工具
def load_paras(book):
    """读入整本 md，切段并清洗噪声（图片/分块标记/书眉）。
    保留 __CHUNK__|page_start|page_end 标记，方便后续估算页码。"""
    txt = open(os.path.join(MD, f"{book}.md"), encoding="utf-8").read()
    txt = txt.split("---\n", 2)[-1].translate(OCR_FIX)
    # 把 CHUNK 注释换成不会与正文混淆的标记段
    txt = CHUNK_RE.sub(lambda m: f"\n\n__CHUNK__|{m.group(2)}|{m.group(3)}\n\n", txt)
    txt = IMG_RE.sub(" ", txt)
    raw = [p.strip() for p in re.split(r"\n\s*\n", txt)]
    raw = [re.sub(r"\s*\n\s*", " ", p).strip() for p in raw if p.strip()]

    paras = []
    for p in raw:
        if p.startswith("__CHUNK__|"):
            parts = p.split("|")
            paras.append({"t": p, "h": False, "chunk": True,
                          "page_start": int(parts[1]), "page_end": int(parts[2])})
        else:
            is_head = p.startswith("#")
            body = re.sub(r"^#+\s*", "", p).strip()
            if not body:
                continue
            paras.append({"t": body, "h": is_head})

    # 书眉去重：MinerU 会把页面天头的书眉识别成标题，它与紧随其后的正文首条重复
    keep = []
    for i, p in enumerate(paras):
        if p.get("chunk"):
            keep.append(p)
            continue
        if p["h"]:
            n = norm(p["t"])
            dup = False
            for j in range(i + 1, min(i + 6, len(paras))):
                if paras[j].get("chunk") or paras[j]["h"]:
                    continue
                nj = norm(paras[j]["t"])
                if nj.startswith(n) and len(n) >= 2:
                    dup = True
                    break
            if dup:
                continue
        keep.append(p)

    return [p["t"] for p in keep]


def get_chunks(paras):
    """从包含 __CHUNK__|A|B 标记的段落列表中提取 chunk 边界（段落下标）。"""
    chunks = []
    cur = None
    for i, p in enumerate(paras):
        if p.startswith("__CHUNK__|"):
            parts = p.split("|")
            if cur is not None:
                cur["end_idx"] = i
                chunks.append(cur)
            cur = {"start_idx": i + 1, "end_idx": None,
                   "page_start": int(parts[1]), "page_end": int(parts[2])}
    if cur is not None:
        cur["end_idx"] = len(paras)
        chunks.append(cur)
    return chunks


def estimate_page(para_idx, chunks):
    """根据段落下标估算原始页码。"""
    for c in chunks:
        if c["start_idx"] <= para_idx < c["end_idx"]:
            span = c["end_idx"] - c["start_idx"]
            if span <= 0:
                return c["page_start"]
            ratio = (para_idx - c["start_idx"]) / span
            return c["page_start"] + int(ratio * (c["page_end"] - c["page_start"]))
    return None


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]", "", s)


def sort_key(s):
    """英文排序键：去除音标/引号/标点后的字母数字串"""
    s = re.sub(r"\[[^\]]*\]|\{[^}]*\}", "", s)
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^0-9a-z ]", "", s).strip()


def lis_filter(keys):
    """最长非递减子序列 —— 词典按字母序排列，
    真词条的排序键必然单调不减；插图说明、跨页续段等噪声会打破单调性。
    """
    import bisect
    n = len(keys)
    tails, tails_idx, prev = [], [], [-1] * n
    for i, k in enumerate(keys):
        pos = bisect.bisect_right(tails, k)
        if pos == len(tails):
            tails.append(k)
            tails_idx.append(i)
        else:
            tails[pos] = k
            tails_idx[pos] = i
        prev[i] = tails_idx[pos - 1] if pos > 0 else -1
    res, cur = [], tails_idx[-1] if tails_idx else -1
    while cur != -1:
        res.append(cur)
        cur = prev[cur]
    return set(res)


# ---------------------------------------------------------------- 牛津（英）
OX_HEAD = re.compile(
    r"^(?P<hw>[‘'\"“]?[A-Za-z][A-Za-z0-9\u00c0-\u024f\-'’ ./()]{0,44}?[’'\"”]?)"
    r"\s*(?:\[[^\]]{0,70}\]|\{[^}]{0,70}\]|\([0-9]\))?"
    r"\s*(?P<sep>\.|=|,\s*(?=[A-Z])|\sSee\s)"
)


def parse_oxford(paras):
    cands = []
    for i, p in enumerate(paras):
        if p.startswith("__CHUNK__|"):
            continue
        m = OX_HEAD.match(p)
        if not m:
            continue
        hw = m.group("hw").strip(" .,")
        if not hw or len(hw) < 2:
            continue
        # headword 不应是完整句子
        if hw.count(" ") > 4:
            continue
        k = sort_key(hw)
        if not k:
            continue
        cands.append((i, hw, k))

    good = lis_filter([c[2] for c in cands])
    heads = {cands[j][0]: cands[j][1] for j in good}

    entries, cur = [], None
    for i, p in enumerate(paras):
        if p.startswith("__CHUNK__|"):
            continue
        if i in heads:
            if cur:
                entries.append(cur)
            hw = heads[i]
            body = p[len(hw):].lstrip(" .")
            ipa = ""
            mi = re.match(r"^\s*[\[{]([^\]}]{1,70})[\]}]\s*\.?\s*", body)
            if mi:
                ipa = mi.group(1).strip()
                body = body[mi.end():]
            cur = {"term": hw, "ipa": ipa, "body": [body.strip()], "_para_idx": i}
        elif cur:
            cur["body"].append(p)
    if cur:
        entries.append(cur)

    out = []
    for e in entries:
        text = "\n\n".join(x for x in e["body"] if x)
        if len(text) < 3:
            continue
        out.append({"term": e["term"], "sub": e["ipa"], "text": text,
                    "_para_idx": e["_para_idx"]})
    return out


# ---------------------------------------------------------------- 现代语言学词典（英汉）
CR_HEAD = re.compile(
    r"^(?P<en>[A-Za-z][A-Za-z0-9\-'’ /]{0,40}"
    r"(?:[（(][^）)]{0,40}[）)])?[A-Za-z0-9\-'’ /]{0,20})"
    r"\s*(?P<cn>[" + CJK + r"][^\s]{0,24})?"
)


# 对照表一行可能挤了多组「中文 english」，用 finditer 逐组切出
CR_PAIR_RE = re.compile(
    r"(?P<cn>[" + CJK + r"][" + CJK + r"0-9（）()，、·／/\-—]{0,24})\s*"
    r"(?P<en>[A-Za-z][A-Za-z0-9\-'’.]*"
    r"(?:[\s,，;；()（）/]+[A-Za-z0-9][A-Za-z0-9\-'’.]*)*)"
)


def split_crystal_index(paras):
    """现代语言学词典正文之后附有『汉英术语对照表』，
    可为英文词条反向补出中文检索入口。返回 (正文段落, 对照表条目)。
    """
    chunks = get_chunks(paras)
    cut = None
    for i, p in enumerate(paras):
        if p.startswith("__CHUNK__|"):
            continue
        if p.strip() in ("汉英术语对照表", "汉英术语对照") or (
                "汉英术语对照" in p[:20] and len(p) < 30):
            cut = i
            break
    if cut is None:
        return paras, []

    pairs, seen = [], set()
    for i, p in enumerate(paras[cut + 1:]):
        real_idx = cut + 1 + i
        if p.startswith("__CHUNK__|"):
            continue
        p = p.strip()
        if not p or len(p) < 3 or re.fullmatch(r"[A-Z]|\(.{0,12}\)", p):
            continue
        for m in CR_PAIR_RE.finditer(p):
            cn = m.group("cn").strip(" ，、")
            en = re.sub(r"\s+", " ", m.group("en")).strip(" ,.;，；")
            if len(cn) < 1 or len(en) < 2 or not re.search(r"[A-Za-z]{2}", en):
                continue
            k = (cn, en.lower())
            if k in seen:
                continue
            seen.add(k)
            pairs.append({"cn": cn, "en": en, "_para_idx": real_idx})
    return paras[:cut], pairs


def parse_crystal(paras):
    cands = []
    for i, p in enumerate(paras):
        if p.startswith("__CHUNK__|"):
            continue
        if not re.match(r"^[A-Za-z]", p):
            continue
        m = re.match(r"^([A-Za-z][A-Za-z0-9\-'’ /,.()（）]{0,60}?)(?=[" + CJK + r"])", p)
        if not m:
            continue
        en = m.group(1).strip(" ,.")
        if len(en) < 2 or en.count(" ") > 5:
            continue
        k = sort_key(en)
        if not k:
            continue
        cands.append((i, en, k, m.end()))

    good = lis_filter([c[2] for c in cands])
    heads = {cands[j][0]: cands[j] for j in good}

    entries, cur = [], None
    for i, p in enumerate(paras):
        if p.startswith("__CHUNK__|"):
            continue
        if i in heads:
            if cur:
                entries.append(cur)
            _, en, _, pos = heads[i]
            rest = p[pos:]
            # 中文译名：紧跟英文词条，以空格与释义分隔
            mc = re.match(r"^([" + CJK + r"][" + CJK + r"0-9a-zA-Z（）()·、／/\-]{0,23})(?=\s)", rest)
            cn = mc.group(1) if mc else ""
            body = rest[len(cn):].strip() if cn else rest.strip()
            cur = {"term": en, "cn": cn, "body": [body], "_para_idx": i}
        elif cur:
            cur["body"].append(p)
    if cur:
        entries.append(cur)

    out = []
    for e in entries:
        text = "\n\n".join(x for x in e["body"] if x)
        if len(text) < 3:
            continue
        out.append({"term": e["term"], "sub": e["cn"], "text": text,
                    "_para_idx": e["_para_idx"]})
    return out


# ---------------------------------------------------------------- 梅德明百科（中）
STOP_PREFIX = ("参见", "例如", "如上", "其中", "因此", "但是", "所以", "然而", "此外",
               "另外", "上述", "同时", "由于", "根据", "图", "表", "注",
               "前言", "凡例", "目录", "索引", "附录", "后记", "编者", "说明",
               "序", "导言", "缩写", "参考", "鸣谢", "致谢", "修订", "勘误",
               "词目", "音序", "部首", "笔画", "正文", "总", "编")

MD_HEAD = re.compile(
    r"^(?P<cn>[" + CJK + r"][" + CJK + r"0-9Ａ-Ｚａ-ｚ·—－\-]{0,13})"
    r"\s*(?P<en>[A-Za-z][A-Za-z0-9\-'’()（）\s;；,，:：./]{2,90}?)"
    r"(?=[" + CJK + r"]|$)"
)


def parse_meidemin(paras):
    entries, cur = [], None
    for i, p in enumerate(paras):
        if p.startswith("__CHUNK__|"):
            continue
        # 单字母分区标记
        if re.fullmatch(r"[A-Z]", p.strip()):
            continue
        m = MD_HEAD.match(p)
        ok = False
        if m:
            cn = m.group("cn").strip()
            en = m.group("en").strip(" ,.;；，、:：")
            letters = sum(c.isalpha() and c.isascii() for c in en)
            if (2 <= len(cn) <= 14 and len(en) >= 3 and letters >= 3
                    and letters / max(len(en), 1) > 0.55
                    and not cn.startswith(STOP_PREFIX)
                    and not re.search(r"[，。、；：？！“”（）]", cn)
                    and not re.fullmatch(r"[ivxlcdmIVXLCDM]+", en)):  # 过滤纯罗马数字页码
                ok = True
        if ok:
            if cur:
                entries.append(cur)
            en = m.group("en").strip(" ,.;；，、:：")
            body0 = p[m.end():].strip()
            # 修复英文词目被连字符折行：writ- / ing
            if en.endswith("-") and body0[:1].isascii() and body0[:1].islower():
                en = en[:-1] + body0[0]
                body0 = body0[1:].lstrip()
            cur = {"term": m.group("cn").strip(),
                   "en": en,
                   "body": [body0],
                   "_para_idx": i}
        elif cur:
            cur["body"].append(p)

    out = []
    for e in entries:
        text = "\n\n".join(x for x in e["body"] if x)
        if len(text) < 3:
            continue
        out.append({"term": e["term"], "sub": e["en"], "text": text,
                    "_para_idx": e["_para_idx"]})
    return out


# ---------------------------------------------------------------- 主流程
BOOKS = {
    "oxford": ("牛津语言学词典", "P. H. Matthews", "en", parse_oxford),
    "crystal": ("现代语言学词典", "David Crystal 著 / 沈家煊 译", "zh", parse_crystal),
    "meidemin": ("语言学与应用语言学百科全书", "梅德明 主编", "zh", parse_meidemin),
}

if __name__ == "__main__":
    only = sys.argv[1:] or list(BOOKS)
    all_entries, stats = [], []
    for key in only:
        if key not in BOOKS or not os.path.exists(os.path.join(MD, f"{key}.md")):
            print(f"skip {key}")
            continue
        title, author, lang, fn = BOOKS[key]
        paras = load_paras(key)
        chunks = get_chunks(paras)

        if key == "crystal":
            paras, pairs = split_crystal_index(paras)
            # 为汉英对照表条目估算页码
            for p in pairs:
                p["page"] = estimate_page(p.pop("_para_idx"), chunks)
            with open(os.path.join(DATA, "crystal_index.json"), "w", encoding="utf-8") as f:
                json.dump(pairs, f, ensure_ascii=False)
            print(f"  crystal 汉英对照表: {len(pairs)} 条")

        ents = fn(paras)
        for idx, e in enumerate(ents):
            e["id"] = f"{key}-{idx}"
            e["src"] = key
            e["page"] = estimate_page(e.pop("_para_idx"), chunks)
            all_entries.append(e)
        avg = sum(len(e["text"]) for e in ents) / max(len(ents), 1)
        stats.append({"book": key, "title": title, "paras": len(paras),
                      "entries": len(ents), "avg_len": round(avg)})
        print(f"{key}: {len(paras)} paras -> {len(ents)} entries (avg {avg:.0f} chars)")

    # 同词目去重：保留释义更长者（丢弃「参见…」短桩，避免查找时重复显示）
    best = {}
    for e in all_entries:
        k = (e["src"], e["term"])
        if k not in best or len(e["text"]) > len(best[k]["text"]):
            best[k] = e
    all_entries = list(best.values())

    with open(os.path.join(DATA, "entries.json"), "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False)
    with open(os.path.join(DATA, "stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print("TOTAL", len(all_entries), "entries")
