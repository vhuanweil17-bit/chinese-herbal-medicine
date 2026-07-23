#!/usr/bin/env python3
"""中药饮片查询 - Web界面（含炮制规范）"""
import json
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

data_file = Path(__file__).parent / "data" / "herbs.json"
with open(data_file, "r", encoding="utf-8") as f:
    herbs = json.load(f)

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>中药饮片查询 | 炮制规范</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f0f4f0;color:#333}
header{background:linear-gradient(135deg,#2d5a27,#4a8c42);color:#fff;padding:2rem 1rem;text-align:center}
header h1{font-size:1.8rem;margin-bottom:.3rem}
header p{opacity:.9;font-size:.95rem}
.container{max-width:1100px;margin:0 auto;padding:1rem}
.search-box{display:flex;gap:.5rem;margin:1.5rem 0}
.search-box input{flex:1;padding:.8rem 1rem;border:2px solid #c8dcc8;border-radius:8px;font-size:1rem;outline:none}
.search-box input:focus{border-color:#4a8c42}
.search-box button{padding:.8rem 1.5rem;background:#4a8c42;color:#fff;border:none;border-radius:8px;font-size:1rem;cursor:pointer}
.search-box button:hover{background:#3a7533}
.filters{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:1rem}
.filter-btn{padding:.4rem 1rem;background:#fff;border:1px solid #c8dcc8;border-radius:20px;cursor:pointer;font-size:.85rem;color:#555}
.filter-btn.active{background:#4a8c42;color:#fff;border-color:#4a8c42}
.result-card{background:#fff;border-radius:10px;padding:1.2rem;margin-bottom:.8rem;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.result-card h3{color:#2d5a27;margin-bottom:.2rem;font-size:1.15rem}
.result-card .pinyin{color:#888;font-size:.85rem;margin-bottom:.5rem}
.result-card .tags{margin-bottom:.5rem}
.result-card .tag{display:inline-block;background:#e8f2e8;color:#2d5a27;padding:.15rem .6rem;border-radius:4px;font-size:.78rem;margin-right:.3rem}
.result-card .section{margin-top:.8rem;padding-top:.6rem;border-top:1px solid #eef3ee}
.result-card .section-title{font-weight:600;color:#2d5a27;font-size:.9rem;margin-bottom:.3rem}
.result-card p{margin:.2rem 0;font-size:.9rem;line-height:1.5}
.result-card .label{color:#888;font-size:.82rem}
.result-card .form-item{background:#f8faf8;border-radius:6px;padding:.6rem .8rem;margin:.4rem 0}
.result-card .form-name{font-weight:600;color:#4a8c42;font-size:.9rem}
.result-card .form-detail{font-size:.85rem;color:#555;margin-top:.2rem}
.count{color:#888;font-size:.9rem;margin-bottom:.5rem}
.nav-links{text-align:center;margin:.8rem 0}
.nav-links a{color:#4a8c42;font-size:.9rem;text-decoration:none;margin:0 .5rem}
.nav-links a:hover{text-decoration:underline}
</style>
</head>
<body>
<header>
<h1>🌿 中药饮片查询</h1>
<p>含炮制规范 · 数据依据《中国药典》2020年版</p>
</header>
<div class="container">
<div class="search-box">
<input id="search" placeholder="输入药材名称、功效、归经..." onkeyup="searchHerb()">
<button onclick="searchHerb()">搜索</button>
</div>
<div class="nav-links">
<a href="https://github.com/vhuanweil17-bit/chinese-herbal-medicine/blob/main/docs/processing-specifications.md" target="_blank">📖 炮制规范全文</a>
<a href="https://github.com/vhuanweil17-bit/chinese-herbal-medicine" target="_blank">🐙 GitHub</a>
</div>
<div class="filters" id="filters"></div>
<div id="count" class="count"></div>
<div id="results"></div>
</div>
<script>
const herbs = {{HERBS}};
const categories = [...new Set(herbs.map(h=>h.category))];
const filterDiv = document.getElementById('filters');
let activeCategory = '';

categories.forEach(c => {
    const btn = document.createElement('button');
    btn.className = 'filter-btn';
    btn.textContent = c;
    btn.onclick = () => {
        document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
        btn.classList.add('active');
        activeCategory = activeCategory === c ? '' : c;
        if (!activeCategory) btn.classList.remove('active');
        searchHerb();
    };
    filterDiv.appendChild(btn);
});

function renderProcessing(p) {
    if (!p) return '';
    let html = '<div class="section"><div class="section-title">📋 炮制规范</div>';
    html += '<p><span class="label">净制：</span>' + (p['\u51c0\u5236'] || p['\u51c0\u5236'] || '') + '</p>';
    html += '<p><span class="label">切制：</span>' + (p['\u5207\u5236'] || '') + '</p>';
    html += '<p><span class="label">饮片标准：</span>' + (p.standard || '') + '</p>';
    if (p.processed_forms && p.processed_forms.length) {
        html += '<div style="margin-top:.6rem"><span class="label">炮制品：</span>';
        p.processed_forms.forEach(f => {
            html += '<div class="form-item"><div class="form-name">' + f.name + '</div>';
            html += '<div class="form-detail">' + f.method + '</div>';
            html += '<div class="form-detail" style="color:#2d5a27">' + f.effects + '</div>';
            if (f.usage) html += '<div class="form-detail"><span class="label">用量：</span>' + f.usage + '</div>';
            html += '</div>';
        });
        html += '</div>';
    }
    if (p.notes) html += '<p style="margin-top:.4rem"><span class="label">备注：</span>' + p.notes + '</p>';
    html += '</div>';
    return html;
}

function searchHerb() {
    const q = document.getElementById('search').value.trim().toLowerCase();
    const results = herbs.filter(h => {
        if (activeCategory && h.category !== activeCategory) return false;
        if (!q) return true;
        const fields = [h.name, h.pinyin, h.effects, h.meridian, h.category];
        if (h.processing) {
            if (h.processing.standard) fields.push(h.processing.standard);
            if (h.processing.processed_forms) {
                h.processing.processed_forms.forEach(f => fields.push(f.name, f.method, f.effects));
            }
            if (h.processing.notes) fields.push(h.processing.notes);
        }
        return fields.some(f => f && f.toLowerCase().includes(q));
    });
    document.getElementById('count').textContent = '共 ' + results.length + ' 味药材';
    const div = document.getElementById('results');
    div.innerHTML = results.map(h => {
        let tags = '<span class="tag">' + h.category + '</span><span class="tag">' + h.properties + '</span><span class="tag">' + h.meridian + '</span>';
        if (h.processing && h.processing.processed_forms) {
            h.processing.processed_forms.forEach(f => tags += '<span class="tag" style="background:#fff3e0;color:#b87333">' + f.name + '</span>');
        }
        return '<div class="result-card"><h3>' + h.name + '</h3>' +
            '<div class="pinyin">' + h.pinyin + '</div>' +
            '<div class="tags">' + tags + '</div>' +
            '<p><span class="label">功效：</span>' + h.effects + '</p>' +
            '<p><span class="label">用量：</span>' + h.usage + '</p>' +
            '<p><span class="label">禁忌：</span>' + h.contraindications + '</p>' +
            (h.related ? '<p><span class="label">配伍：</span>' + h.related.join('、') + '</p>' : '') +
            renderProcessing(h.processing) +
            '</div>';
    }).join('');
}
searchHerb();
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, HERBS=json.dumps(herbs, ensure_ascii=False))

@app.route("/api/herbs")
def api_herbs():
    q = request.args.get("q", "").lower()
    cat = request.args.get("category", "")
    results = herbs
    if cat:
        results = [h for h in results if h["category"] == cat]
    if q:
        results = [h for h in results if any(q in (h.get(f,"") or "").lower() for f in ["name","pinyin","effects","meridian","category"])]
    return jsonify(results)

@app.route("/api/herbs/<name>")
def api_herb_detail(name):
    for h in herbs:
        if h["name"] == name:
            return jsonify(h)
    return jsonify({"error": "not found"}), 404

@app.route("/api/categories")
def api_categories():
    cats = {}
    for h in herbs:
        cats.setdefault(h["category"], []).append(h["name"])
    return jsonify(cats)

if __name__ == "__main__":
    print("🌿 中药饮片查询工具（含炮制规范）")
    print("打开 http://127.0.0.1:5000 使用")
    print("数据依据《中国药典》2020年版")
    app.run(debug=True, host="0.0.0.0", port=5000)
