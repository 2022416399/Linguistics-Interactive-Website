# 语言学工具书术语检索站 · Linguistics Terminology Search

基于三本语言学工具书的 OCR 文本，构建的**离线 / 在线术语检索站**。单文件 HTML，双击即用，无需服务器、无需联网即可检索。

## 📚 数据源（三本工具书）

| 缩写 | 书名 | 编者 | 页数 |
|------|------|------|------|
| `oxford` | 牛津语言学词典（英文本） | P. H. Matthews | 425 |
| `crystal` | 现代语言学词典 | David Crystal（沈家煊 译） | 459 |
| `meidemin` | 语言学百科全书（正文） | 梅德明 等 | 1363 |

三本均为扫描版 PDF，经 **MinerU** 云端 OCR 识别为 Markdown（`md/` 目录），再解析为结构化词条（`data/`）。

## ✨ 功能

- **全文模糊搜索**：中文词目 / 英文术语 / 释义内容 / 人物名均可搜（如「句法」「syntax」「转换生成语法」「赵元任」）。
- **词典筛选**：按来源（牛津 / 现代 / 百科 / 汉英对照）过滤。
- **页码标注**：每条结果标注原始页码（基于 OCR 段落位置估算，精度 ±1–2 页），方便翻书核查。
- **词条编辑**：可本地修改任意词条（词目 / 英文 / 页码 / 来源 / 释义），保存到浏览器 `localStorage`，支持导出修改 JSON 备份。
- **明暗主题**：内置明暗主题切换，记忆偏好。
- **快捷键**：`/` 聚焦搜索，`Esc` 清空，长释义可折叠展开，命中关键词高亮。

## 🚀 使用方式

### 1. 离线（推荐）
直接用浏览器打开 `离线网站/index.html` 或 `site/index.html`（单文件，零依赖，可拷到任意电脑 / U 盘使用）。

### 2. 在线分享
已部署到 CloudStudio，生成公开链接，任何人打开即可检索（数据内嵌，搜索在访客浏览器本地完成）：
`https://67fe987cd2f04d1cabe6dfd016b5acd4.gz1.agentos-app.net`

### 3. GitHub Pages（可选）
本仓库根目录已含 `index.html`。在仓库 **Settings → Pages** 选择 `main` 分支、`/ (root)` 目录，开启后即可通过 `https://<user>.github.io/linguistics-terminology/` 访问。

## 📂 目录结构

```
术语查询站/
├── scripts/                 # 处理脚本（MinerU 客户端 / 分段 / 提交 / 轮询 / 解析 / 构建网站）
│   ├── mineru_client.py     #   MinerU v4 API 客户端（预签名上传 + 轮询下载）
│   ├── split_all.py         #   按 180 页/段拆分 PDF（账户限 200 页/段）
│   ├── submit_all.py        #   分批提交 OCR 任务（断点续传）
│   ├── poll_all.py          #   轮询并下载 OCR 结果（断点续传）
│   ├── build_md.py          #   合并各段 full.md 为完整书 md
│   ├── parse_entries.py     #   解析词条（三本书各自版式 + 汉英对照表）
│   └── build_site.py        #   生成单文件离线网站 index.html
├── md/                      # MinerU 识别后合成的完整书（最终 Markdown）
│   ├── oxford.md
│   ├── crystal.md
│   ├── meidemin.md
│   └── _summary.json
├── data/                    # 结构化词条
│   ├── entries.json         #   主词条（约 1.3 万条）
│   ├── crystal_index.json   #   汉英术语对照表（约 3700 对）
│   └── stats.json
├── 离线网站/
│   └── index.html           # 可直接双击打开的单文件站点（带页码 + 编辑）
└── .gitignore
```

> 注：`raw/`（PDF 切片）、`result/`（逐段原始 OCR 产物，含插图，约 800MB）体积过大，未纳入本仓库。需要原始 OCR 产物可单独索取。

## 🔧 重新构建

```bash
pip install requests        # MinerU 客户端依赖
python scripts/build_md.py      # 重新合成三本完整 md
python scripts/parse_entries.py oxford crystal meidemin   # 重新解析词条
python scripts/build_site.py    # 重新生成 index.html
```

## 📊 数据规模

- 主词条：约 13,231 条（牛津 3,215 + 现代 1,783 + 百科 8,233，已去重）
- 汉英对照：3,704 对
- 检索入口合计：约 16,935 条

## ⚠️ 说明

- 三本工具书版权归原出版社所有，本项目仅作个人学术研究用途。
- 页码为依据 OCR 段落位置估算，可能存在 ±1–2 页偏差，请以原书为准。
- 词条释义为 OCR 识别结果，可能存在个别识别误差，建议结合原书核查。
