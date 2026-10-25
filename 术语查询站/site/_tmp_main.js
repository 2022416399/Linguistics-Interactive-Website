
(function(){
  const PAYLOAD = JSON.parse(document.getElementById('payload').textContent);
  const ENTRIES = PAYLOAD.entries;
  const SRC_LABEL = PAYLOAD.src_label;
  const $ = id => document.getElementById(id);
  // 前端现算检索串（避免内嵌重复数据）
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
  function norm(s){ return (s||'').toLowerCase().replace(/[^0-9a-z\u4e00-\u9fff]+/g,' ').trim(); }
  const qEl = $('q'), resEl = $('result'), metaEl = $('meta');
  let timer=null;

  function escapeHtml(s){ return (s||'').replace(/[&<>]/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m])); }
  function hl(text, q){
    if(!q) return escapeHtml(text);
    const safe = escapeHtml(text);
    try{
      const re = new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig');
      return safe.replace(re, '<mark>$1</mark>');
    }catch(e){ return safe; }
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
      // 排序：term 命中优先
      list = list.slice().sort((a,b)=>{
        const at = norm(a.term).includes(q)?0:1, bt = norm(b.term).includes(q)?0:1;
        return at-bt;
      });
    }
    // 限制渲染数量，保证流畅
    const MAX = 300;
    const shown = list.slice(0, MAX);
    metaEl.textContent = (raw? ('匹配 '+list.length+' 条'+(list.length>MAX?'（仅显示前 '+MAX+' 条，请缩小关键词）':'')) : (active==='all'?'显示全部词条':'当前词典共 '+list.length+' 条'));
    if(!shown.length){
      resEl.innerHTML = '<div class="empty">没有找到匹配的术语 😶<br>试试更换关键词，或切换上方词典筛选</div>';
      return;
    }
    const frag = document.createDocumentFragment();
    shown.forEach(e=>{
      const card = document.createElement('div');
      card.className = 'card';
      const sub = e.sub ? '<span class="sub">'+escapeHtml(e.sub)+'</span>' : '';
      const text = e.text || '';
      const collapsed = text.length > 120 ? ' collapsed' : '';
      card.innerHTML =
        '<h3>'+hl(e.term,'')+sub+'<span class="src">'+escapeHtml(e.src_label||'')+'</span></h3>'+
        '<div class="body'+collapsed+'">'+hl(text, raw)+'</div>'+
        (collapsed?'<span class="more">展开全文 ▾</span>':'');
      if(collapsed){
        const body = card.querySelector('.body'), more = card.querySelector('.more');
        more.onclick = ()=>{ if(body.classList.contains('collapsed')){body.classList.remove('collapsed');more.textContent='收起 ▴';} else {body.classList.add('collapsed');more.textContent='展开全文 ▾';} };
      }
      frag.appendChild(card);
    });
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
