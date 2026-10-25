#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""构建离线单文件术语查询站（site/index.html）。

- 内嵌 entries.json（牛津/现代/百科）+ crystal_index.json（汉英对照）
- 全文模糊搜索 + 词典筛选 + 明暗主题 + 词条编辑（localStorage）
- 零外部依赖，双击即用，可离线打开
"""
import os, json, re, html, datetime

OUT = r"D:\WorkBuddy工作区\02-语言学站点\术语查询站"
DATA = os.path.join(OUT, "data")
SITE = os.path.join(OUT, "site")
os.makedirs(SITE, exist_ok=True)

# ---------------------------------------------------------------- 载入数据
entries = json.load(open(os.path.join(DATA, "entries.json"), encoding="utf-8"))
stats = json.load(open(os.path.join(DATA, "stats.json"), encoding="utf-8")) \
    if os.path.exists(os.path.join(DATA, "stats.json")) else []

try:
    pairs = json.load(open(os.path.join(DATA, "crystal_index.json"), encoding="utf-8"))
except Exception:
    pairs = []

# 汉英对照表并入可检索词条（中文词目为主键，英文为 sub）
idx_entries = []
for i, p in enumerate(pairs):
    cn = (p.get("cn") or "").strip()
    en = (p.get("en") or "").strip()
    if not cn or not en:
        continue
    idx_entries.append({
        "term": cn,
        "sub": en,
        "text": "英文术语：" + en,
        "src": "crystal_index",
        "id": f"cidx-{i}",
        "page": p.get("page"),
    })

all_entries = entries + idx_entries

# 来源标签
SRC_LABEL = {
    "oxford": "牛津语言学词典",
    "crystal": "现代语言学词典（英汉）",
    "meidemin": "语言学百科全书",
    "crystal_index": "现代词典·汉英对照",
}
# 预计算小写检索串 + 来源中文标签
for e in all_entries:
    e["src_label"] = SRC_LABEL.get(e.get("src", ""), e.get("src", ""))
    hay = " ".join([e.get("term", ""), e.get("sub", ""), e.get("text", "")]).lower()
    e["_h"] = re.sub(r"[^0-9a-z\u4e00-\u9fff]+", " ", hay).strip()

n_by_src = {}
for e in all_entries:
    n_by_src[e["src"]] = n_by_src.get(e["src"], 0) + 1

print("总词条:", len(all_entries))
print("按来源:", n_by_src)

payload = {
    "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    "entries": [{k: v for k, v in e.items() if not k.startswith("_")} | {"src_label": e["src_label"]}
                for e in all_entries],
    "src_label": SRC_LABEL,
}

data_js = json.dumps(payload, ensure_ascii=False)

# ---------------------------------------------------------------- HTML 模板
HTML = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>语言学工具书 · 术语查询站（离线版）</title>
<style>
:root{
  --bg:#f6f7f9; --bg2:#ffffff; --ink:#1a1d24; --muted:#6b7280; --line:#e6e8ec;
  --brand:#4f46e5; --brand2:#7c3aed; --chip:#eef0f4; --chip-on:#4f46e5;
  --card:#ffffff; --shadow:0 1px 3px rgba(16,24,40,.08),0 8px 24px rgba(16,24,40,.06);
  --hi:#fff3bf; --danger:#ef4444; --ok:#10b981;
}
[data-theme="dark"]{
  --bg:#0d1017; --bg2:#11151f; --ink:#e8ebf2; --muted:#9aa3b2; --line:#222838;
  --brand:#818cf8; --brand2:#a78bfa; --chip:#1b2030; --chip-on:#818cf8;
  --card:#151a26; --shadow:0 1px 2px rgba(0,0,0,.4),0 12px 30px rgba(0,0,0,.35);
  --hi:#3b3410; --danger:#f87171; --ok:#34d399;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",Roboto,Helvetica,Arial,sans-serif;
  background:radial-gradient(1200px 600px at 80% -10%, color-mix(in srgb,var(--brand) 12%, transparent), transparent 60%),
             radial-gradient(900px 500px at -10% 0%, color-mix(in srgb,var(--brand2) 10%, transparent), transparent 55%),
             var(--bg);
  color:var(--ink); min-height:100vh; -webkit-font-smoothing:antialiased;
  transition:background .35s ease, color .35s ease;
}
.wrap{max-width:1040px;margin:0 auto;padding:0 18px 80px}
header.top{padding:30px 0 14px}
.brand{display:flex;align-items:center;gap:12px;justify-content:space-between}
.logo{display:flex;align-items:center;gap:12px}
.logo .mark{width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,var(--brand),var(--brand2));
  display:grid;place-items:center;color:#fff;font-weight:800;font-size:18px;box-shadow:var(--shadow)}
.logo h1{font-size:20px;margin:0;letter-spacing:.3px}
.logo p{margin:2px 0 0;font-size:12.5px;color:var(--muted)}
.top-actions{display:flex;align-items:center;gap:8px}
.theme-btn{cursor:pointer;border:1px solid var(--line);background:var(--bg2);color:var(--ink);
  width:42px;height:42px;border-radius:12px;font-size:18px;display:grid;place-items:center;transition:.2s}
.theme-btn:hover{transform:translateY(-2px);box-shadow:var(--shadow)}
.searchbox{position:sticky;top:12px;z-index:20;margin:14px 0 14px}
.searchbar{display:flex;align-items:center;gap:10px;background:var(--bg2);border:1px solid var(--line);
  border-radius:16px;padding:12px 16px;box-shadow:var(--shadow);transition:.2s}
.searchbar:focus-within{border-color:var(--brand);box-shadow:0 0 0 4px color-mix(in srgb,var(--brand) 18%,transparent)}
.searchbar svg{flex:none;opacity:.6}
.searchbar input{flex:1;border:0;outline:0;background:transparent;color:var(--ink);font-size:16px}
.searchbar .kbd{font-size:11px;color:var(--muted);border:1px solid var(--line);border-radius:6px;padding:2px 7px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:4px 0 6px}
.chip{cursor:pointer;border:1px solid var(--line);background:var(--chip);color:var(--ink);
  padding:7px 13px;border-radius:999px;font-size:13px;transition:.18s;user-select:none}
.chip:hover{transform:translateY(-1px)}
.chip.on{background:var(--chip-on);color:#fff;border-color:var(--chip-on)}
.chip .n{opacity:.7;margin-left:5px;font-size:11px}
.meta{display:flex;align-items:center;gap:12px;font-size:12.5px;color:var(--muted);margin:2px 2px 14px;flex-wrap:wrap}
.meta .link{cursor:pointer;color:var(--brand);text-decoration:underline}
.meta .link:hover{opacity:.8}
.result{display:grid;gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 18px;
  box-shadow:var(--shadow);transition:.18s;animation:rise .35s ease both;position:relative}
.card:hover{transform:translateY(-2px);border-color:color-mix(in srgb,var(--brand) 40%,var(--line))}
.card.edited{border-left:4px solid var(--ok)}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.card h3{margin:0;font-size:18px;letter-spacing:.2px;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.card .sub{font-size:13px;color:var(--brand);font-weight:600}
.card .meta-row{margin-left:auto;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.card .src{font-size:11.5px;color:var(--muted);border:1px solid var(--line);
  padding:2px 9px;border-radius:999px;white-space:nowrap}
.card .page{font-size:12px;color:var(--brand);font-weight:600;white-space:nowrap}
.card .edit-btn{font-size:12px;color:var(--muted);cursor:pointer;opacity:0;transition:.15s}
.card:hover .edit-btn{opacity:1}
.card .edit-btn:hover{color:var(--brand)}
.card .body{margin-top:9px;font-size:14.5px;line-height:1.75;color:var(--ink);opacity:.92;
  white-space:pre-wrap;word-break:break-word}
.card .body.collapsed{max-height:5.4em;overflow:hidden;position:relative}
.card .more{cursor:pointer;color:var(--brand);font-size:12.5px;margin-top:6px;display:inline-block}
mark{background:var(--hi);color:inherit;border-radius:3px;padding:0 1px}
.empty{text-align:center;color:var(--muted);padding:60px 20px;font-size:15px}
footer{margin-top:40px;text-align:center;font-size:12px;color:var(--muted)}
footer a{color:var(--brand);text-decoration:none}
.edit-form{display:grid;gap:10px;margin-top:10px}
.edit-form input,.edit-form textarea,.edit-form select{
  font:inherit;padding:8px 10px;border-radius:10px;border:1px solid var(--line);background:var(--bg2);color:var(--ink)}
.edit-form textarea{min-height:90px;resize:vertical;line-height:1.6;white-space:pre-wrap}
.edit-form .row{display:flex;gap:10px;flex-wrap:wrap}
.edit-form .row input,.edit-form .row select{flex:1;min-width:120px}
.edit-actions{display:flex;gap:8px;justify-content:flex-end}
.edit-actions button{cursor:pointer;border:0;border-radius:8px;padding:7px 14px;font-size:13px}
.edit-actions .save{background:var(--brand);color:#fff}
.edit-actions .cancel{background:var(--chip);color:var(--ink)}
.edit-actions .reset{background:var(--danger);color:#fff}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%);background:var(--ink);color:#fff;
  padding:9px 18px;border-radius:10px;font-size:13px;box-shadow:var(--shadow);opacity:0;transition:.25s;pointer-events:none;z-index:100}
.toast.show{opacity:1}
@media (max-width:640px){
  .card .edit-btn{opacity:1}
  .meta-row{margin-left:0!important;width:100%;justify-content:flex-end}
}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div class="brand">
      <div class="logo">
        <div class="mark">语</div>
        <div>
          <h1>语言学工具书 · 术语查询站</h1>
          <p>牛津语言学词典 · 现代语言学词典 · 语言学百科全书 · 离线可检索</p>
        </div>
      </div>
      <div class="top-actions">
        <button class="theme-btn" id="theme" title="切换明暗主题">🌙</button>
      </div>
    </div>
  </header>

  <div class="searchbox">
    <div class="searchbar">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
      <input id="q" type="text" placeholder="搜索术语、英文、释义…（按 / 聚焦）" autocomplete="off" spellcheck="false">
      <span class="kbd">/</span>
    </div>
    <div class="chips" id="chips"></div>
    <div class="meta" id="meta"></div>
  </div>

  <div class="result" id="result"></div>

  <footer>
    共 <span id="total">0</span> 条术语 · 数据由 MinerU OCR 解析自三本工具书 · 本页为完全离线单文件，可随意复制分发
  </footer>
</div>
<div class="toast" id="toast"></div>

<script id="payload" type="application/json">__DATA__</script>
<script>
(function(){
  const PAYLOAD = JSON.parse(document.getElementById('payload').textContent);
  const SRC_LABEL = PAYLOAD.src_label;
  const $ = id => document.getElementById(id);

  const LS_KEY = 'ling-edits-v1';
  let edits = {};
  try{ const raw = localStorage.getItem(LS_KEY); if(raw) edits = JSON.parse(raw); }catch(e){}

  // 应用编辑覆盖
  const ENTRIES = PAYLOAD.entries.map(e => {
    const ov = edits[e.id];
    return ov ? {...e, ...ov, _edited:true} : e;
  });
  ENTRIES.forEach(e => { e.h = norm((e.term||'')+' '+(e.sub||'')+' '+(e.text||'')); });

  // 主题
  const root = document.documentElement;
  const themeBtn = $('theme');
  function applyTheme(t){
    root.setAttribute('data-theme', t);
    themeBtn.textContent = t === 'dark' ? '☀️' : '🌙';
    try{ localStorage.setItem('ling-theme', t); }catch(e){}
  }
  try{ const saved = localStorage.getItem('ling-theme'); if(saved) applyTheme(saved); }catch(e){}
  themeBtn.onclick = () => applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');

  // 来源筛选 chips
  const counts = {};
  ENTRIES.forEach(e => counts[e.src] = (counts[e.src]||0)+1);
  let active = 'all';
  const chipWrap = $('chips');
  const defs = [['all','全部',ENTRIES.length]].concat(
    Object.keys(SRC_LABEL).filter(k=>counts[k]).map(k=>[k,SRC_LABEL[k],counts[k]]));
  defs.forEach(([key,label,n])=>{
    const c = document.createElement('div');
    c.className = 'chip' + (key==='all'?' on':'');
    c.dataset.k = key;
    c.innerHTML = label + '<span class="n">'+n+'</span>';
    c.onclick = ()=>{ active = key; document.querySelectorAll('.chip').forEach(x=>x.classList.remove('on')); c.classList.add('on'); render(); };
    chipWrap.appendChild(c);
  });

  $('total').textContent = ENTRIES.length;

  // 搜索索引
  function norm(s){ return (s||'').toLowerCase().replace(/[^0-9a-z\\u4e00-\\u9fff]+/g,' ').trim(); }
  const qEl = $('q'), resEl = $('result'), metaEl = $('meta');
  let timer=null;

  function escapeHtml(s){ return (s||'').replace(/[&<>]/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m])); }
  function hl(text, q){
    if(!q) return escapeHtml(text);
    const safe = escapeHtml(text);
    try{
      const re = new RegExp('('+q.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')+')','ig');
      return safe.replace(re, '<mark>$1</mark>');
    }catch(e){ return safe; }
  }

  function toast(msg){
    const t = $('toast'); t.textContent = msg; t.classList.add('show');
    setTimeout(()=>t.classList.remove('show'), 2200);
  }

  function saveEdits(){
    try{ localStorage.setItem(LS_KEY, JSON.stringify(edits)); }catch(e){ toast('保存失败：存储空间不足'); }
  }

  function exportEdits(){
    const blob = new Blob([JSON.stringify(edits, null, 2)], {type:'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'terminology-edits-'+new Date().toISOString().slice(0,10)+'.json';
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function makeEditForm(card, e){
    card.innerHTML = '';
    card.classList.add('editing');
    const form = document.createElement('div');
    form.className = 'edit-form';
    const termIn = document.createElement('input'); termIn.value = e.term || '';
    termIn.placeholder = '词目 / Term';
    const subIn = document.createElement('input'); subIn.value = e.sub || '';
    subIn.placeholder = '副标题 / 英文 / Sub';
    const row = document.createElement('div'); row.className = 'row';
    const pageIn = document.createElement('input'); pageIn.type='text'; pageIn.value = e.page || ''; pageIn.placeholder='页码 p.';
    const srcSel = document.createElement('select');
    Object.keys(SRC_LABEL).forEach(k=>{ const o=document.createElement('option'); o.value=k; o.textContent=SRC_LABEL[k]; if(k===e.src)o.selected=true; srcSel.appendChild(o); });
    row.appendChild(pageIn); row.appendChild(srcSel);
    const textIn = document.createElement('textarea'); textIn.value = e.text || ''; textIn.placeholder = '释义 / 正文';
    const actions = document.createElement('div'); actions.className = 'edit-actions';
    const saveBtn = document.createElement('button'); saveBtn.className='save'; saveBtn.textContent='保存';
    const cancelBtn = document.createElement('button'); cancelBtn.className='cancel'; cancelBtn.textContent='取消';
    const resetBtn = document.createElement('button'); resetBtn.className='reset'; resetBtn.textContent='恢复原始';
    actions.appendChild(saveBtn); actions.appendChild(cancelBtn); actions.appendChild(resetBtn);
    form.appendChild(termIn); form.appendChild(subIn); form.appendChild(row); form.appendChild(textIn); form.appendChild(actions);
    card.appendChild(form);

    saveBtn.onclick = ()=>{
      const patch = {
        term: termIn.value.trim(),
        sub: subIn.value.trim(),
        text: textIn.value.trim(),
        page: pageIn.value.trim(),
        src: srcSel.value,
        src_label: SRC_LABEL[srcSel.value] || srcSel.value
      };
      Object.assign(e, patch, {_edited:true});
      edits[e.id] = patch;
      saveEdits();
      toast('已保存到本地浏览器');
      render();
    };
    cancelBtn.onclick = ()=> render();
    resetBtn.onclick = ()=>{
      delete edits[e.id];
      saveEdits();
      // 恢复原始数据
      const orig = PAYLOAD.entries.find(x=>x.id===e.id) || e;
      Object.assign(e, orig, {_edited:false});
      toast('已恢复原始词条');
      render();
    };
  }

  function renderCard(e, raw, q){
    const card = document.createElement('div');
    card.className = 'card' + (e._edited?' edited':'');
    const sub = e.sub ? '<span class="sub">'+escapeHtml(e.sub)+'</span>' : '';
    const text = e.text || '';
    const collapsed = text.length > 120 ? ' collapsed' : '';
    const pageTag = e.page ? '<span class="page">p.'+escapeHtml(String(e.page))+'</span>' : '';
    card.innerHTML =
      '<h3>'+hl(e.term,'')+sub+
      '<span class="meta-row"><span class="src">'+escapeHtml(e.src_label||'')+'</span>'+pageTag+'<span class="edit-btn" title="编辑">✎ 编辑</span></span></h3>'+
      '<div class="body'+collapsed+'">'+hl(text, raw)+'</div>'+
      (collapsed?'<span class="more">展开全文 ▾</span>':'');
    card.querySelector('.edit-btn').onclick = ()=> makeEditForm(card, e);
    if(collapsed){
      const body = card.querySelector('.body'), more = card.querySelector('.more');
      more.onclick = ()=>{ if(body.classList.contains('collapsed')){body.classList.remove('collapsed');more.textContent='收起 ▴';} else {body.classList.add('collapsed');more.textContent='展开全文 ▾';} };
    }
    return card;
  }

  function render(){
    const raw = qEl.value.trim();
    const q = norm(raw);
    let list = ENTRIES;
    if(active!=='all') list = list.filter(e=>e.src===active);
    if(q){
      const parts = q.split(' ').filter(Boolean);
      list = list.filter(e=>{
        const h = e.h || norm(e.term+' '+e.sub+' '+e.text);
        return parts.every(p=>h.includes(p));
      });
      list = list.slice().sort((a,b)=>{
        const at = norm(a.term).includes(q)?0:1, bt = norm(b.term).includes(q)?0:1;
        return at-bt;
      });
    }
    const MAX = 300;
    const shown = list.slice(0, MAX);
    const editedCount = Object.keys(edits).length;
    let metaText = raw? ('匹配 '+list.length+' 条'+(list.length>MAX?'（仅显示前 '+MAX+' 条，请缩小关键词）':'')) : (active==='all'?'显示全部词条':'当前词典共 '+list.length+' 条');
    if(editedCount){
      metaText += ' · 你已本地修改 ' + editedCount + ' 条';
      const exportLink = document.createElement('span');
      exportLink.className = 'link'; exportLink.textContent = '[导出修改]';
      exportLink.onclick = exportEdits;
      metaEl.innerHTML = metaText.replace(' · 你已本地修改 ', ' · ');
      metaEl.appendChild(document.createTextNode(' 你已本地修改 ' + editedCount + ' 条 '));
      metaEl.appendChild(exportLink);
    } else {
      metaEl.textContent = metaText;
    }
    if(!shown.length){
      resEl.innerHTML = '<div class="empty">没有找到匹配的术语 😶<br>试试更换关键词，或切换上方词典筛选</div>';
      return;
    }
    const frag = document.createDocumentFragment();
    shown.forEach(e=> frag.appendChild(renderCard(e, raw, q)));
    resEl.innerHTML = '';
    resEl.appendChild(frag);
  }

  qEl.addEventListener('input', ()=>{ clearTimeout(timer); timer=setTimeout(render, 70); });
  document.addEventListener('keydown', ev=>{
    if(ev.key==='/' && document.activeElement!==qEl){ ev.preventDefault(); qEl.focus(); }
    if(ev.key==='Escape'){ qEl.value=''; render(); qEl.blur(); }
  });
  render();
})();
</script>
</body>
</html>
"""

out = HTML.replace("__DATA__", data_js)
dest = os.path.join(SITE, "index.html")
with open(dest, "w", encoding="utf-8") as f:
    f.write(out)
mb = os.path.getsize(dest) / 1024 / 1024
print(f"已生成 {dest}  ({mb:.2f} MB)")
