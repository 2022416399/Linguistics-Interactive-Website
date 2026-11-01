const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf-8');
const payloadMatch = html.match(/id="payload"[^>]*type="application\/json">([\s\S]*?)<\/script>/);
const mainMatch = html.match(/<script>\s*\(function\(\)\{([\s\S]*?)\}\)\(\);\s*<\/script>\s*<\/body>/);
if (!mainMatch || !payloadMatch) { console.error('脚本或 payload 提取失败'); process.exit(1); }
const payloadJson = payloadMatch[1].trim();
let js = '(function(){' + mainMatch[1] + '})();';
// 注入 payload 文本到 mock element
js = js.replace('document.getElementById(\'payload\').textContent', JSON.stringify(payloadJson));

// Minimal DOM mock
class FakeEl {
  constructor(tag) {
    this.tagName = tag;
    this.children = [];
    this.style = {};
    this.dataset = {};
    this._html = '';
    this._text = '';
    this.value = '';
    this.className = '';
    this.textContent = '';
    this.onclick = null;
  }
  get innerHTML() { return this._html; }
  set innerHTML(v) { this._html = v; }
  get innerText() { return this._text; }
  set textContent(v) { this._text = v; }
  setAttribute(k, v) { this[k] = v; }
  getAttribute(k) { return this[k]; }
  appendChild(c) { this.children.push(c); return c; }
  querySelector() { return new FakeEl('div'); }
  querySelectorAll() { return []; }
  addEventListener() {}
  focus() {}
  blur() {}
}

global.document = {
  getElementById: (id) => {
    if (!global._els) global._els = {};
    if (!global._els[id]) {
      const el = new FakeEl('div');
      el.id = id;
      if (id === 'q') el.value = '';
      if (id === 'chips') el.children = [];
      global._els[id] = el;
    }
    return global._els[id];
  },
  documentElement: { setAttribute() {}, getAttribute() { return 'light'; } },
  querySelectorAll: () => [],
  createElement: (tag) => new FakeEl(tag),
  createDocumentFragment: () => ({ children: [], appendChild(c) { this.children.push(c); } }),
  addEventListener() {}
};
global.localStorage = {
  store: {},
  getItem(k) { return this.store[k] || null; },
  setItem(k, v) { this.store[k] = v; }
};
global.URL = { createObjectURL() { return 'blob://x'; }, revokeObjectURL() {} };

eval(js);
console.log('smoke ok, cards rendered:', global._els.result.children.length);
