#!/usr/bin/env python3
"""中药饮片命令行查询工具"""
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
        if (keyword in h["name"].lower() or
            keyword in h["pinyin"].lower() or
            keyword in h["category"].lower() or
            keyword in h["effects"].lower() or
            keyword in h["meridian"].lower()):
            results.append(h)
    return results

def print_herb(h):
    print(f"\n{'='*50}")
    print(f"  {h['name']}（{h['pinyin']}）")
    print(f"{'='*50}")
    print(f"  分类：{h['category']}")
    print(f"  性味：{h['properties']}")
    print(f"  归经：{h['meridian']}")
    print(f"  功效：{h['effects']}")
    print(f"  用量：{h['usage']}")
    print(f"  禁忌：{h['contraindications']}")
    if h["related"]:
        print(f"  配伍：{'、'.join(h['related'])}")

def list_categories(herbs):
    cats = {}
    for h in herbs:
        cats.setdefault(h["category"], []).append(h["name"])
    print("\n📂 按分类浏览：")
    for cat, names in sorted(cats.items()):
        print(f"\n  {cat}（{len(names)}味）")
        for n in names:
            print(f"    - {n}")

def main():
    herbs = load_data()
    if len(sys.argv) < 2:
        print("用法：")
        print("  python query.py <关键词>     # 搜索药材")
        print("  python query.py --list       # 按分类浏览")
        print("  python query.py --all        # 列出全部")
        return

    arg = sys.argv[1]
    if arg == "--list":
        list_categories(herbs)
    elif arg == "--all":
        for h in herbs:
            print_herb(h)
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
