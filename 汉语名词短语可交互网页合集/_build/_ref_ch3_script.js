
(function(){
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const SOURCES={
 bookInfo:{page:'书目信息',quote:'第三章 句法的象似性',zh:'本页材料范围。'},
 iconDef:{page:'3.2',quote:'象似性指语言形式和内容之间的联系有着非任意、有理据、可论证的一面。',zh:'象似性不是纯任意约定。'},
 disputeOld:{page:'3.1',quote:'象似性研究长期受到冷落，部分源于把它局限于拟声词和语音象征。',zh:'研究史上的任意性—象似性之争。'},
 saussureArb:{page:'3.1',quote:'符号可能是相对地可以论证的；绝对的任意性主要是不可再分析的词汇的属性，相对的可论证性则是语法的属性。',zh:'索绪尔区分绝对任意与相对可论证。'},
 peirceIcon:{page:'3.1',quote:'在每一语言的句法里，都存在着合乎逻辑的象似符。',zh:'皮尔士强调句法中的象似关系。'},
 chomskyInnate:{page:'3.1',quote:'语言形式不直接反映外部世界的形式。',zh:'形式主义立场的概括。'},
 jakobsonVeni:{page:'3.1',quote:'veni, vidi, vici 的子句语序对应事件时序。',zh:'语序可平行于事件顺序。'},
 cooperRoss:{page:'3.1',quote:'Haiman 提出自然句法，认知功能学派从形式与意义的对应研究象似性。',zh:'现代象似性研究。'},
 taiTime:{page:'3.5',quote:'语言中的事件次序往往平行于事件发生的次序。',zh:'时间顺序原则。'},
 haimanDef:{page:'3.2',quote:'当表达式在外形、长度、复杂性及成分关系上平行于它所编码的概念、经验或交际策略，它就具有象似性质。',zh:'Haiman 的象似性定义。'},
 peirce3sign:{page:'3.2',quote:'符号可按与对象的关系分为象似符、引得符和标志符。',zh:'皮尔士符号三分。'},
 peirceMind:{page:'3.2',quote:'相似性是心理事实；没有一种象似符与所指完全相像。',zh:'象似性是程度性的心理关系。'},
 peirceSub:{page:'3.2',quote:'象似符可分为影像、图样和隐喻。',zh:'象似符的三个次类。'},
 motivationList:{page:'3.2',quote:'句法象似动因包括复杂性、独立性、次序、对称、重叠和范畴化。',zh:'六类句法象似动因。'},
 rise3:{page:'3.1',quote:'功能学派崛起、类型学与共性研究积累，以及认知语言学的发展推动了象似性研究复兴。',zh:'象似性研究复兴的原因。'},
 notDenyArb:{page:'3.1',quote:'各种象似原则只是促动，而非决定语言形式。',zh:'象似性不是绝对决定因素。'},
 imagicDiagram:{page:'3.2',quote:'自然语言里的象似符主要是图样，成分之间的关系像指称对象成分之间的关系。',zh:'语言象似性的图样性质。'},
 langDiagram:{page:'3.2',quote:'单个词语可以是任意的，但词语的组织方式能够具有象似性。',zh:'语法组织可具有象似性。'},
 numeral:{page:'3.2',quote:'数字系统和门牌号码可以显示形式排列与空间排列之间的对应。',zh:'数字序列的图样象似。'},
 isoDef:{page:'3.2',quote:'同构是能指与所指结构之间的对应关系。',zh:'同构定义。'},
 isoHypo:{page:'3.2',quote:'形式不同，往往蕴含意义或交际功能的不同；形式相同，往往反映感知到的意义相似。',zh:'同构假说。'},
 automorphism:{page:'3.2',quote:'若对应关系存在于同一系统的两个或多个部分之间，则可称为自同构。',zh:'自同构定义。'},
 isoTypes:{page:'3.2',quote:'图样象似性可分同构、自同构和动因。',zh:'图样象似性的三类。'},
 overlapDef:{page:'3.7',quote:'形式上的重叠可以对应意义上的重叠。',zh:'重叠象似动因。'},
 competition:{page:'3.9',quote:'象似性只是促动语言形式的因素之一，经济性、语法化和规约化都可能使象似性减损。',zh:'动因竞争与象似性减损。'},
 inverse:{page:'3.9',quote:'象似原则与经济原则相互竞争，竞争结果可能导致象似性的减损。',zh:'本章总括。'}
};
// 修正 OCR/复制造成的不可见字符键
SOURCES.cooperRoss=SOURCES['cooperRoss']; delete SOURCES['cooperRoss'];
const citeEls=$$('.cite'); citeEls.forEach((e,i)=>{e.textContent=i+1;e.dataset.n=i+1;e.addEventListener('click',()=>{const s=SOURCES[e.dataset.cite];if(!s)return;$('#citeLoc').textContent='第'+s.page+'节';$('#citeQuote').textContent='“'+s.quote+'”';$('#citeZh').textContent=s.zh;$('#citePop').hidden=false;});});
$('#citeClose').addEventListener('click',()=>$('#citePop').hidden=true);$('#citePop').addEventListener('click',e=>{if(e.target.id==='citePop')$('#citePop').hidden=true;});
const tl={1:'古希腊已讨论名称来自性质还是约定。',2:'索绪尔承认相对可论证性，但强调任意性原则。',3:'皮尔士把句法中的合理对应称为象似符。',4:'生成语法传统倾向于把句法看成自主系统。',5:'功能语言学用事件顺序解释语序。',6:'认知功能研究把象似性推广到自然句法和汉语。'};$$('[data-t]').forEach(b=>b.addEventListener('click',()=>{$$('[data-t]').forEach(x=>x.classList.remove('sel'));b.classList.add('sel');$('#tlTxt').textContent=tl[b.dataset.t];$('#tlBox').hidden=false;}));
$('#sauOpts').addEventListener('click',e=>{if(!e.target.dataset.o)return;$('#sauRev').hidden=false;$$('#sauOpts .btn').forEach(x=>x.classList.toggle('sel',x===e.target));});
const signs={icon:'象似符：依靠性质相似，如地图与地形。',index:'引得符：依靠时空相邻或因果关联，如水兵服与水兵。',symbol:'标志符：依靠社会规约，如 book 与“书”。'};$$('[data-k]').forEach(b=>b.addEventListener('click',()=>{$('#signTxt').textContent=signs[b.dataset.k];$('#signBox').hidden=false;}));
$('#signQuiz').addEventListener('click',e=>{if(e.target.dataset.o){$('#signRev').hidden=false;e.target.classList.add('sel');}});
const nums={1:'契刻计数把数量直接留下痕迹，形式与数量有近似关系。',2:'罗马数字仍保留较强的图形特征，但系统性增加。',3:'阿拉伯数字进入门牌系统后，序列位置可以映射街道位置。'};$$('#numBtns .btn').forEach(b=>b.addEventListener('click',()=>{$('#numTxt').textContent=nums[b.dataset.n];$('#numBox').hidden=false;$('#numFb').textContent='已选择：'+b.textContent;}));
const ex={1:'空语素：形式位置存在，但没有明显的语音材料。',2:'零语素：没有可听形式，却由语法位置承载意义。',3:'同义现象：不同形式可能在某些语境中实现相近功能。',4:'同形/多义：相同形式可以因概念关联形成多个意义。'};$$('[data-e]').forEach(b=>b.addEventListener('click',()=>{$('#excTxt').textContent=ex[b.dataset.e];$('#excBox').hidden=false;}));
const mot={complex:'复杂性：表达越复杂的概念，形式往往也越复杂；更多形式可承载更多意义。',independent:'独立性：概念上彼此独立的成分倾向于用形式上更独立的成分表达。',order:'次序：语言成分的顺序可模拟事件或概念展开的顺序。',symmetry:'对称：概念结构中的对称关系可映射为形式上的对称排列。',overlap:'重叠：形式重复或重叠可对应意义上的重复或重叠。',category:'范畴化：形式标记的有无或强弱可对应成员的范畴地位。'};$$('[data-m]').forEach(b=>b.addEventListener('click',()=>{$('#motiveTxt').textContent=mot[b.dataset.m];$$('[data-m]').forEach(x=>x.classList.toggle('sel',x===b));}));
const oq={a:'次序：语言顺序平行于事件顺序。',b:'对称：形式重复对应概念成员的对称分组。',c:'重叠：重复形式对应程度或过程的重叠。'};$$('#orderBtns .btn').forEach(b=>b.addEventListener('click',()=>{$('#orderTxt').textContent=oq[b.dataset.o];$('#orderBox').hidden=false;}));$('#orderReveal').addEventListener('click',()=>$('#orderRev').hidden=false);
let gameDone=false;$('#gameBtns').addEventListener('click',e=>{if(!e.target.dataset.g)return;$('#gameFb').innerHTML=e.target.dataset.g==='order'?'<span class="v-ok">✓</span>正确：这是次序象似。':'<span class="v-no">△</span>再想想：关键是事件先后。';$('#gameNext').hidden=false;});$('#gameNext').addEventListener('click',()=>{$('#gameQ').textContent='2. “大家齐声喊：走走走！”';$('#gameFb').textContent='';$('#gameNext').hidden=true;});
$('#balance').addEventListener('input',e=>{const v=+e.target.value;$('#balLabel').textContent='象似 '+v+' / 经济 '+(100-v);$('#balFb').textContent=v>70?'象似性占优：形式更透明。':v<30?'经济性占优：形式更压缩。':'两种动因暂时平衡。';});$$('[data-b]').forEach(b=>b.addEventListener('click',()=>$('#balRev').hidden=false));
$$('#q1 .btn').forEach(b=>b.addEventListener('click',()=>{$('#q1fb').textContent=b.dataset.q==='b'?'✓ 正确：象似性与任意性是程度关系。':'△ 不是二选一。';}));$$('#q2 .btn').forEach(b=>b.addEventListener('click',()=>{$('#q2fb').textContent=b.dataset.q==='a'?'✓ 正确。':'△ 再想想事件顺序。';}));
const scenes=['s1','s2','s3','s4','s5','s6','s7','quiz'];function jump(id){const e=document.getElementById(id);if(e)e.scrollIntoView({behavior:'smooth'});history.pushState({id},'',location.pathname+'#'+id);}$$('[data-jump]').forEach(b=>b.addEventListener('click',()=>jump(b.dataset.jump)));let idx=0;document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){idx=Math.min(idx+1,scenes.length-1);jump(scenes[idx]);}if(e.key==='ArrowLeft'){idx=Math.max(idx-1,0);jump(scenes[idx]);}});
$('#themeBtn').addEventListener('click',()=>{const r=document.documentElement;r.dataset.theme=r.dataset.theme==='dark'?'light':'dark';localStorage.setItem('np3theme',r.dataset.theme);});if(localStorage.np3theme)document.documentElement.dataset.theme=localStorage.np3theme;let fs=17;$('#fontUp').addEventListener('click',()=>{fs=Math.min(20,fs+1);document.documentElement.style.setProperty('--fs',fs+'px');});$('#fontDown').addEventListener('click',()=>{fs=Math.max(15,fs-1);document.documentElement.style.setProperty('--fs',fs+'px');});
const key='np3progress';const obs=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting&&x.target.id){localStorage.setItem(key,x.target.id);}}),{threshold:.25});$$('[data-scene]').forEach(s=>obs.observe(s));
})();
