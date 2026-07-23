#!/usr/bin/env python3
"""中药饮片命令行查询工具（含炮制规范）"""
import json
import sys
from pathlib import Path

def load_data():
    data_file = Path(__file__).parent / "data" / "herbs.json"
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)

def search(herbs, keyword):
    results = []
    keyword = keyword.lower()
    for h in herbs:
        fields = [h["name"], h["pinyin"], h["category"], h["effects"], h["meridian"]]
        if h.get("processing"):
            p = h["processing"]
            if p.get("standard"): fields.append(p["standard"])
            if p.get("processed_forms"):
                for f in p["processed_forms"]:
                    fields.extend([f["name"], f["method"], f["effects"]])
            if p.get("notes"): fields.append(p["notes"])
        if any(keyword in (f or "").lower() for f in fields):
            results.append(h)
    return results

def print_herb(h):
    print(f"\n{'='*55}")
    print(f"  {h['name']}（{h['pinyin']}）")
    print(f"{'='*55}")
    print(f"  分类：{h['category']}")
    print(f"  性味：{h['properties']}")
    print(f"  归经：{h['meridian']}")
    print(f"  功效：{h['effects']}")
    print(f"  用量：{h['usage']}")
    print(f"  禁忌：{h['contraindications']}")
    if h.get("related"):
        print(f"  配伍：{'、'.join(h['related'])}")

    p = h.get("processing")
    if p:
        print(f"\n  ── 炮制规范 ──")
        print(f"  净制：{p.get('净制', '')}")
        print(f"  切制：{p.get('切制', '')}")
        print(f"  饮片：{p.get('standard', '')}")
        if p.get("processed_forms"):
            print(f"\n  炮制品：")
            for f in p["processed_forms"]:
                print(f"    ● {f['name']}")
                print(f"      炮制：{f['method']}")
                print(f"      功效：{f['effects']}")
                if f.get("usage"):
                    print(f"      用量：{f['usage']}")
        if p.get("notes"):
            print(f"\n  备注：{p['notes']}")

def list_categories(herbs):
    cats = {}
    for h in herbs:
        cats.setdefault(h["category"], []).append(h["name"])
    print("\n📂 按分类浏览：")
    for cat, names in sorted(cats.items()):
        print(f"\n  {cat}（{len(names)}味）")
        for n in names:
            forms = ""
            for h in herbs:
                if h["name"] == n and h.get("processing",{}).get("processed_forms"):
                    forms = " [" + ", ".join(f["name"] for f in h["processing"]["processed_forms"]) + "]"
                    break
            print(f"    - {n}{forms}")

def main():
    herbs = load_data()
    if len(sys.argv) < 2:
        print("用法：")
        print("  python query.py <关键词>     # 搜索药材（支持名称/功效/炮制品）")
        print("  python query.py --list       # 按分类浏览")
        print("  python query.py --all        # 列出全部（含炮制信息）")
        print("  python query.py proc         # 查看炮制规范文档路径")
        return

    arg = sys.argv[1]
    if arg == "--list":
        list_categories(herbs)
    elif arg == "--all":
        for h in herbs:
            print_herb(h)
    elif arg == "proc":
        print("\n📖 炮制规范全文：docs/processing-specifications.md")
        print("   打开 docs/ 目录下的 processing-specifications.md 查看完整炮制通则")
    else:
        results = search(herbs, arg)
        if results:
            print(f"\n🔍 找到 {len(results)} 味药材：")
            for h in results:
                print_herb(h)
        else:
            print(f"未找到与「{arg}」相关的药材")

if __name__ == "__main__":
    main()
