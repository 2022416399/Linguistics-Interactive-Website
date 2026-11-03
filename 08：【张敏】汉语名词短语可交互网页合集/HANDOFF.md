# HANDOFF · 张敏《认知语言学与汉语名词短语》交互研读页合集

> **新会话第一句请说：「请先读取 HANDOFF.md，了解项目上下文，再继续推进。」**
> 本文档写给**完全无上下文**的新会话。所有路径、行号、契约、代码标记均已于 **2026-10-28** 逐项磁盘核验，照 §5 执行即可，不必重新取证。
> 本文档在两地各存一份（内容相同）：`02：安装skill\HANDOFF.md`（主）与 `02：安装skill\Linguistics Interactive Website【2026.10.25】\汉语名词短语可交互网页合集\HANDOFF.md`（副本）。改内容请以主文档为准，并同步副本。

---

## 0. 三十秒速览

- **任务**：把张敏《认知语言学与汉语名词短语》做成「单文件、零外部依赖、可离线双击打开」的 HTML 交互研读页系列（深读页），外加一份总导览 `index.html`。
- **用户最高指示（当前有效口径）**：「**如果内容不缺少，就直接输出最终产物，风格不重要**」——内容齐备时直接交付，不要为风格返工。
- **已完成**：新版深读页 8 个文件正文全部生成；其中 **07 页只剩尾部未写**；旧版 10.24 简版 8 页完好。
- **卡点**：① 07 页尾部（quiz/series/footer/pop/backBtn/script/闭合标签）未写；② `index.html` 仍是旧版、只链到 06 一页；③ 05 页 series 链向**不存在**的 08 页（断链待决策）。
- **下一步**：§5.1 落 07 尾部 → §5.2 重写 index → §5.3 验证 → 全过后 `present_files` 交付并报告「任务做完」。另有暂缓的教程线见 §7。

---

## 1. 任务是什么

### 1.1 用户原话演进史（决定最终形态，**不可违背**）

1. 「@…认知语言学与汉语名词短语_张敏_研读底本md 继续，重新生成张敏这本书 @skill:pdf-to-interactive-web」——以研读底本 md 为素材重做全书交互页。
2. 多轮「继续输出 / 继续执行任务 / 继续，输出完告诉我」——逐章生成深读页。
3. 「修复残缺的两个半成品，再生成一份完整的导览页面，包含10.25日和10.27日的html文件」——半成品（05/06 曾残缺）已修复，导览待重做。
4. 「修复残缺和导览，任务做完告诉我」。
5. 「张敏的书，还剩多少没有输出」「张敏《认知语言学与汉语名词短语》（共 8 章）以及索引的html文件是否都输出完成，缺少的部分继续进行」。
6. **「如果内容不缺少，就直接输出最终产物，风格不重要」** ← 交付口径。

### 1.2 成品形态约定（唯一有效方案）

- 单文件 HTML，无外部 CSS/JS/字体/图片依赖，双击可开、可离线。
- 每页结构（以 05 页为标准骨架）：
  `header.top`（品牌＋四钮：`#resumeBtn`「回到进度」/`#fontDown`「字−」/`#fontUp`「字+」/`#themeBtn`「暗色」，均 `type="button"`）→ `main.wrap` → `section.hero[data-hero]` → 若干 `section.scene[data-scene]`（场景：kicker＋h2＋正文 P＋guess/lab 交互件）→ `section.quiz[data-quiz]`（自测）→ series 导航＋footer → `div#pop`（出处弹窗）→ `button#backBtn` → `details.src`（出处清单）→ `<script>`。
- 引文角标：正文 `<sup class="cite" data-cite="键名"></sup>`，点击弹 `#pop` 显示 quote / page / zh 三段；SOURCES 字典定义在 script 内。
- 读者设置走 localStorage：字号、主题、滚动位置（回到进度）。
- **07 页特有**：CSS 已备 `details.src` 全套规则（L71–79），而 05/06 都没写此块——判定为 07 原设计漏写，**07 必须补写出处清单**。

---

## 2. 项目地图（绝对路径，均已核验）

根目录：`D:\WorkBuddy工作区\04-工具与技能\02：安装skill\`
（目录名含全角冒号「：」，bash 里所有路径必须加双引号）

| 内容 | 路径 |
|---|---|
| 研读底本 md（4278 行，OCR 转录，无原书页码；角标「底本 Lx」= 该行在 md 中的行号） | `1-2：研读底本md\认知语言学与汉语名词短语_张敏_研读底本.md` |
| 合集目录（本任务主战场） | `Linguistics Interactive Website【2026.10.25】\汉语名词短语可交互网页合集\` |
| 事实账本 | 合集内 `_事实账本\ch3.md`、`ch6.md` |
| 旧版备份 | 合集内 `_旧版备份\` |
| 教程线（另一任务，暂缓） | `Linguistics Interactive Website【2026.10.25】\现代汉语语法研究教程交互页\`（自带 HANDOFF.md） |

### 2.1 合集文件清单与状态（2026-10-28 核验）

**新版深读页（10.27–10.28 生成）：**

| 文件 | 大小/行数 | 状态 |
|---|---|---|
| `认知语言学与汉语名词短语-01深读-理论主张.html` | 58KB | ✅ 完整（series 只列到 01） |
| `认知语言学与汉语名词短语-02深读-范畴化.html` | 57KB | ✅ 完整（series 列到 02） |
| `认知语言学与汉语名词短语-03深读-句法的象似性.html` | 135KB / 1374 行 | ✅ 完整，但**无 series nav**（独立加页，index 收录时注意） |
| `认知语言学与汉语名词短语-03深读-重叠动因.html` | 53KB | ✅ 完整（series 链中 03＝重叠动因） |
| `认知语言学与汉语名词短语-04深读-下篇概述.html` | 46KB | ✅ 完整（series 列到 04） |
| `认知语言学与汉语名词短语-05深读-距离动因.html` | 80KB | ✅ 完整，**05 是 07 的逐字样板**；series 列全链 01–08（含不存在的 08） |
| `认知语言学与汉语名词短语-06深读-的字隐现.html` | 100KB | ✅ 完整，但**另一套交互约定**（`data-ok`/`.exp`/veil），series 只有 index 链接；**不能当 07 样板** |
| `认知语言学与汉语名词短语-07深读-领属结构.html` | 41KB / 383 行 | ⚠️ **正文 6 场景完好，尾部全缺** ← 当前卡点 |
| `认知语言学与汉语名词短语-08深读-定语语序.html` | — | ❌ 不存在（素材：md 第八章 L3603–4278） |

**旧版 10.24 简版 8 页（15–16KB 小文件，完好，index 要收录并标「已上线」）：**
`认知语言学与汉语名词短语-第一章-理论主张.html`、`-第二章-经验基础.html`、`-第三章-句法的象似性.html`、`-第四章-下篇概述.html`、`-第五章-距离动因与DN、DdN语义差别.html`、`-第六章-的字隐现的一般规律.html`、`-第七章-领属结构的的与语言共性.html`、`-第八章-多项定语的语序规律.html`

**导览：** `index.html`（39KB 旧版，**只链到 06 一页**，待重写 = Task #71）

---

## 3. 07 页现状明细（写尾部前必读）

- **383 行，止于场景六 `.vs` 双卡 `</section>`，其后全空**。前 383 行一个字都不要动。
- 文档骨架（实测）：`<!DOCTYPE html>` / `<html lang="zh-CN" data-theme="light">` / head（charset、viewport、title「第七章 领属结构 · 认知语言学与汉语名词短语 深读」、`<style>`）/ body / `header.top>div.wrap.nav`（`.brand`「名词短语深读 · **领属结构**」＋`.tools` 四钮）/ `<main class="wrap">`（L125 起，**无 `</main>`**）/ `section.hero[data-hero]`（L127）。
- 正文 6 场景（`data-scene` 1–6）已定稿：场景五「代词作定语·PdN 与 PN」、场景六「为什么偏偏是我哥哥·两步理据」（含 Silverstein 十级阶梯 `.ladder` Ⅰ–Ⅹ、Deane 前后置对比 `.vs` 双卡）；场景一至四覆盖「的」字三条件、指称/分类之别、显著度、双层假说等（键名见 §5.1.4）。
- 交互件：guess 块（`.guess[data-guess]` 内 `.opts[data-correct]`＋4 个 `button[data-ans]`，**无 `data-q`**，判定句在 `.why[hidden]`）；lab 块 3 个（`data-pool`/`data-out`，键为 proto/class/pdn）。
- **15 处 `data-cite`，13 个唯一键**：`silverstein`×2、`PN-motivation`×2，其余 `two-layer`、`salience`、`reciprocal`、`plural-test`、`pdN-pN`、`institution`、`identification-class`、`ident-vs-class`、`ego`、`condition-order`、`adjacency` 各 ×1。
- CSS 已全部就位（quiz/series/footer/details.src/pop/backBtn/sup.cite 全套），契约见 §5.1.2。

---

## 4. 当前卡点（按优先级）

1. **Task #70**：07 页尾部未写。缺：`section.quiz`、series 导航、footer、`</main>`、`div#pop`、`#backBtn`、`details.src`、`<script>` 全量、`</body></html>`。
2. **Task #71**：`index.html` 重写（收录全部深读页＋旧版 8 页，全部标「已上线」可点击）。
3. **Task #72**：完整性验证未跑（闭合标签、`node --check`、场景数、角标键全覆盖、index 链接可达）。
4. **断链决策**：05 页 series 链向 `认知语言学与汉语名词短语-08深读-定语语序.html`（不存在）。两条路：补生成 08 页，或改 05 链接。**建议补页**——用户专门问过「还剩多少没有输出」，且 md 第八章素材充足（L3603–4278，余论：多项定语的语序规律）。
5. 暂缓线：教程章节版 `_body-3/_body-4`（见 §7），用户未催。

---

## 5. 下一步施工图

### 5.1 落 07 尾部（Task #70）

#### 5.1.1 写入顺序（严格照 05 骨架，`cat` 追加，勿动前 383 行）

1. `<section class="quiz" data-quiz>`：`<h2>你答得上来吗</h2>`＋3 个 `<div class="qitem">`。每题：`<p class="q"><b>1.</b>题干</p>`＋`<div class="opts" data-correct="b">`（3 个 `button[data-ans]`，**不带 `data-q`**）＋`<p class="why" hidden>答案：b。…</p>`。题目建议：①「的」字三条件的次序（引 `condition-order`）；② PN 只表单数指称（引 `plural-test`）；③ 脚色稳固性/双向领属（引 `PN-motivation`/`reciprocal`）。
2. `<section>` 包 `<nav class="series">`（说明 span「系列深读页：」＋`↖ 索引`＋01–08 八链，07 标 `class="cur"`）＋`<footer>` 两段（第一段：本页范围＝底本第七章 L3240–L3602＋行号口径说明；第二段：未覆盖第八章多项定语语序＋原书信息）→ `</section>`。
3. `</main>`（单独一行）。
4. `<div class="pop" id="pop" hidden role="dialog" aria-modal="true" aria-label="出处">`：`<button class="x" id="popClose" aria-label="关闭">✕</button>`＋`<p class="q" id="popQuote"></p>`＋`<p class="meta" id="popMeta"></p>`＋`<p class="zh" id="popZh"></p>`＋`</div>`；紧随 `<button id="backBtn" hidden>↩ 回到刚才的位置</button>`。
5. `<details class="src">`：`<summary>出处清单 · 本页角标共 13 条</summary>`＋`<ol>` 13 条 `<li>`，每条 `<code>键名</code>`＋page＋quote＋zh。
6. `<script>` 全量 → `</script></body></html>`。

**组装命令**（在合集目录）：
```bash
cat _c7_tail.html >> 认知语言学与汉语名词短语-07深读-领属结构.html
```

#### 5.1.2 CSS 契约（07 页实测行号，尾部落笔直接对照）

| 行号 | 规则 | 对尾部的要求 |
|---|---|---|
| L19 | `.tools button,.quiz button,.lab button,.guess button,.pop button,#backBtn{…}` | 按钮无需另写样式 |
| L43–49 | `.opts{flex,wrap}`、`.opts button.right{border/color=red}`、`.opts button.wrong{opacity:.55}`、`.why{display:none}`、**`.why.show{display:block}`**、`.why b{color:red}` | 判定后必须 `why.hidden=false` **且** `why.classList.add("show")` 双保险 |
| L50–55 | `.lab .cap`、`.pool{flex}`、`.result{…min-height:2.2em}`、**`.result b{color:red}`**、**`.result b.ok{color:blue}`** | lab 输出必须走 `innerHTML`＋`<b>`/`<b class="ok">` |
| L80–89 | `.quiz{margin-top:46px;border-top:2px solid red}`、`.quiz h2{22px}`、**`.quiz .qitem{margin:18px 0}`**、`.quiz .q{16.5px}`、**`.quiz .q b{color:gold;margin-right:8px}`**、`.series{…}`、`.series a{…}`、`.series a:hover`、`.series a.cur{红}$` | quiz 每题用 `.qitem`；题号用 `<b>1.</b>`；当前页 series 链标 `a.cur` |
| L71–79 | `details.src{…}`、`summary`（`▸/▾` 伪元素）、`details.src ol/li`、`details.src li code{红色等宽}` | 出处清单 13 条 `li`，键名放 `<code>` |
| L90 | `footer{border-top;margin-top:40px;…}` | footer 两段 `<p>` |
| L91 | `#backBtn{position:fixed;right:18px;bottom:18px;z-index:20}` | 直接抄 05 |
| L103–112 | `.pop{position:absolute;…max-width:min(430px,92vw)}`、`.pop[hidden]{display:none}`、`.pop .q`（楷体左边框）、`.pop .meta`、`.pop .zh`、`.pop .x`、`@media(max-width:640px)` 改 fixed、`sup.cite{color:red;cursor:pointer}` | pop 结构照抄 05；锚定定位 JS 见 5.1.3 |

#### 5.1.3 05 页 script 逐字样板（L455–697，照抄后按 5.1.5 改）

关键片段（05 页实测）：

```js
const SOURCES = { "three-props": { page:"底本 L2278-2286", quote:"…", zh:"…" }, … };
const store = { get(k){ try{ return localStorage.getItem(k); }catch{ return null; } },
                set(k,v){ try{ localStorage.setItem(k,v); }catch{} } };
const motionOK = () => !matchMedia("(prefers-reduced-motion: reduce)").matches;

function openPop(id, anchor){ const s = SOURCES[id]; if(!s) return; lastCite = anchor;
  popQuote.textContent = "「" + s.quote + "」";
  popMeta.textContent = "出处：" + s.page + "（《认知语言学与汉语名词短语》研读底本）";
  popZh.textContent = "转述：" + s.zh; pop.hidden = false;
  const r = anchor.getBoundingClientRect();
  if (innerWidth > 640){ pop.style.top = (scrollY + r.bottom + 8) + "px";
    pop.style.left = Math.min(scrollX + r.left - 160, scrollY + innerWidth - 450) + "px"; }
  else { pop.style.top = ""; pop.style.left = ""; } }
function closePop(){ pop.hidden = true; }
document.addEventListener("click", e => { const c = e.target.closest("sup.cite");
  if (c){ openPop(c.dataset.cite, c); e.stopPropagation(); return; }
  if (!e.target.closest("#pop")) closePop(); });
document.getElementById("popClose").onclick = closePop;
// popstate + backBtn.onclick → 回到 lastCite（或收起）
```

- `.guess .opts` 判定：`correct = group.dataset.correct || group.querySelector("button").dataset.ans`；命中 `x.classList.add("right")`、未命中 `b.classList.add("wrong")`、全部 `disabled`、`group.nextElementSibling.hidden = false`。
- `.quiz .opts` 判定：`q = group.closest(".q")`（07 改用 `.qitem`）→ `q.querySelector(".why").hidden = false`。
- 滚动：400ms throttle → `store.set("you-scroll", String(scrollY))`；`savedY>240` 才 `resumeBtn.style.display="inline-block"`。
- 键盘：`Escape` 关 pop；`←/→` 在 `[...document.querySelectorAll("[data-scene],[data-hero],[data-quiz]")]` 间跳转（`cur=scenes.findIndex(s=>s.getBoundingClientRect().top>-80)`、`next=scenes[Math.min(len-1,Math.max(0,idx±1))]`、`scrollIntoView`）。

#### 5.1.4 13 键 SOURCES 与取证命令

键 → md 行号（page 字段写「底本 Lxxxx-yyyy」）；引文用 `sed -n 'a,bp'` 从底本 md 取**逐字原文**（勿凭记忆改写）：

| 键 | md 行号 | 键 | md 行号 |
|---|---|---|---|
| `ident-vs-class` | L3252 | `institution` | L3442–3446 |
| `identification-class` | L3266–3268 | `PN-motivation` | L3496–3500 ＋ L3538–3546 |
| `salience` | L3282–3284 | `reciprocal` | L3544–3548 |
| `condition-order` | L3404–3408 | `ego` | L3556–3562 |
| `two-layer` | L3348–3356 | `silverstein` | L3565–3570 |
| `adjacency` | L3344–3346 | `pdN-pN` | L3410–3416 |
| `plural-test` | L3420–3440 | | |

取证命令示例：
```bash
cd "D:/WorkBuddy工作区/04-工具与技能/02：安装skill/1-2：研读底本md"
sed -n '3244,3290p' 认知语言学与汉语名词短语_张敏_研读底本.md   # 前三键
```
（注意：**读 07 页 HTML 的 L312–383 会被 Read 工具 withhold，读 HTML 一律用 `sed`**，读 md 用 Read 或 sed 均可。）

#### 5.1.5 07 专属适配（与 05 不同，**务必遵守**）

1. **字号**：07 的 `:root` **没有** `font-size` 声明（05 有 `16.5px`），且 07 `body{font-size:17px}` 是硬编码 → 只设 `document.documentElement.style.fontSize` **几乎无效**。必须：
   ```js
   const SIZES = ["15px","17px","19px"];           // 默认下标 1，与 CSS 17px 一致，首载无跳变
   function applyFs(){ document.documentElement.style.fontSize = SIZES[i];
                      document.body.style.fontSize = SIZES[i]; store.set("c7-fs", SIZES[i]); }
   ```
   绑 `#fontUp`/`#fontDown`。
2. **主题**：`applyTheme()` 用 `setAttribute("data-theme", v)`；`THEMES=["auto","light","dark"]`；键 `c7-theme`；绑 `#themeBtn`。
3. 07 **没有** `html{scroll-behavior:smooth}` → 键盘跳转写 `behavior: motionOK() ? "smooth" : "auto"`。
4. **不写** `jumpTo` / `data-go`（05 里是死码，05/07 的 HTML 均无 `data-go` 元素）。
5. `.why` 判定后 `hidden=false` ＋ `classList.add("show")` 双保险（CSS 是 `.why.show{display:block}`）。
6. lab 输出用 `innerHTML`，判定词包 `<b>`（说不通）或 `<b class="ok">`（说得通），写进 `[data-out]`。
7. quiz 的 why 查找：`group.closest(".qitem").querySelector(".why")`（07 用 `.qitem` 不用 `.q` 包裹）。
8. `details.src` 的 summary 文案建议「出处清单 · 本页角标共 13 条」。

#### 5.1.6 自检命令

```bash
# 1) 追加尾部后抽 JS 检查语法（临时文件用完即删）
sed -n '/<script>/,/<\/script>/p' 认知语言学与汉语名词短语-07深读-领属结构.html | sed '1d;$d' > _c7_check.js
node --check _c7_check.js && rm _c7_check.js
# 2) 闭合与计数
grep -c '</html>' 认知语言学与汉语名词短语-07深读-领属结构.html      # 期望 1
grep -c 'class="scene"' 认知语言学与汉语名词短语-07深读-领属结构.html # 期望 6
grep -o 'data-cite="[^"]*"' 认知语言学与汉语名词短语-07深读-领属结构.html | sort -u | wc -l  # 期望 13
```

### 5.2 重写 index.html（Task #71）

- 收录并全部标「**已上线**」可点击：新版深读 9 文件（01 理论主张 / 02 范畴化 / 03 句法的象似性 / 03 重叠动因 / 04 下篇概述 / 05 距离动因 / 06 的字隐现 / 07 领属结构 / 08 定语语序——08 若按 §4.4 补页则收，否则先不列并处理 05 的断链）＋旧版 10.24 简版 8 页。
- 分组陈列（「新版深读」/「10.24 简版」），每条注明对应章节与底本行号范围；旧版可注明「简版」。
- 风格从简——用户明确说过风格不重要；保持单文件、可离线、与深读页一致的视觉基调即可。
- 现状：旧 index 只链到 06，直接整体重写，不要打补丁。

### 5.3 完整性验证（Task #72）

逐项过：
1. 每页 `</html>`、`</main>`、`</script>` 齐全（07 重点）。
2. 07 的 JS `node --check` 通过（临时 `_c7_check.js` 用完删除）。
3. 07 场景数 6；15 处 `data-cite` 的键全部落在 SOURCES 13 键内（`sort -u` 比对）。
4. index.html 所有 `href` 指向的文件**真实存在**（防再出现 05→08 式断链）。
5. 弹出件可用：点角标出 pop、点窗外关、Esc 关、←→ 跳场景。
6. 全过 → `present_files`（index.html 优先，其次 07 页）→ 文字报告「**任务做完**」并简述改动文件。

### 5.4 08 页（建议补，Task 附赠）

- 素材：md L3603–4278（第八章 余论：多项定语的语序规律；戴浩一「时间顺序原则」、朱德熙(1957) 三条语序规则、陆丙甫等）。
- 结构照 05；页名 `认知语言学与汉语名词短语-08深读-定语语序.html`；series 链落地；index 收录。
- 若决定不补：把 05 页 series 里 08 那条链删掉或改为旧版第八章链接，并在 index 说明。

---

## 6. 坑（绝对不要再踩）

1. **Read 工具读 07 页 L312–383 会返回 `[SENSITIVE_CONTENT_UNAVAILABLE]`** → 读该文件一律 `sed -n 'a,bp'` 小批量来，有效。
2. 07 页角标属性是 `data-cite`，**不是** `data-src`（曾搞错）。
3. 07 `:root` 无 `font-size`、`body` 硬编码 17px → 只设 html 的 fontSize 会让字号按钮**几乎失效**；必须 html/body 双设（见 5.1.5-1）。
4. 05 脚本里的 `jumpTo` / `[data-go]` / popstate 部分是**死码**（05/07 HTML 均无 `data-go`），07 不写。
5. `details.src` 不是「05/06 都没写所以不写」——07 的 CSS 专为此备了 L71–79 全套，是原设计漏写，**要补**。
6. 07 没有 `html{scroll-behavior:smooth}` → 平滑滚动靠 JS `motionOK()` 判断。
7. **06 页不能当样板**：它用另一套交互约定（`data-ok`/`.exp`/veil），series 也只有 index 链接。样板只用 **05**。
8. 01/02/04 的 series nav 只列到自己序号；05 列全链 01–08。07 按 05 的全链形态写（并留意 08 断链）。
9. `file` 命令不存在（exit 127）；`python -c` 用 `re` 必须显式 `import re`。
10. 临时文件（`_c7_tail.html`、`_c7_check.js`）用完即删，别留在合集目录。
11. 路径口径：单 Bud `D:\WorkBuddy工作区\04-工具与技能\02：安装skill\...`；目录名含全角冒号「：」和方括号【】，bash 必须引号包裹。
12. `.workbuddy` 目录是项目数据，**不要删**；workspace memory 的 `MEMORY.md` 不存在，历史读 `.workbuddy\memory\` 日期日志。
13. Silverstein 层级是 **10 级（Ⅰ–Ⅹ）**（咱们 / 我·我们 / 你·你们 / 他·他们 / 专名 / 亲属词 / 地位词 / 有生名词 / 离散实体 / 抽象事物），不是 8 级。
14. 用户已豁免「2500 可见汉字」上限（教程线口径）；张敏线同样不压字数，内容优先。
15. quiz 题号必须 `<b>1.</b>`（CSS `.quiz .q b` 金色样式在），不要裸文本。
16. 曾把 `03深读-句法的象似性.html`（无 series nav 的独立加页）和 `03深读-重叠动因.html`（series 链中的 03）搞混——这是两个不同文件，index 都要收。

---

## 7. 另一条线（暂缓，用户未催）

《现代汉语语法研究教程》15 章章节版：`Lingustics Interactive Website【2026.10.25】\现代汉语语法研究教程交互页\`（正确路径：`Linguistics Interactive Website【2026.10.25】\现代汉语语法研究教程交互页\`），已有独立 HANDOFF.md。状态：`_head.html`/`_tail.html`/`_body-1/2a/2b` 就绪；`_body-3.html`（ch8–11）、`_body-4.html`（ch12–14＋自测＋footer＋pop）未写；92 个 cite id 只登记 31 条 SOURCES。张敏线不依赖它。

---

## 8. 交付口径

- 全部完成后：`present_files`（`index.html` 第一、07 页第二）→ 文字报告「**任务做完**」＋简述改了哪些文件。
- 复述用户偏好：**内容不缺少就直接输出最终产物，风格不重要**；不要在风格上反复返工。
