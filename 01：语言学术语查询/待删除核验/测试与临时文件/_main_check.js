
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
