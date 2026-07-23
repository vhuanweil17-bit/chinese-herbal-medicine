# 中药饮片查询工具 🍃

支持按名称、功效、归经、性味、禁忌等多维度查询中药饮片信息。

## 功能

- 🔍 **多维度查询** — 按名称、功效、归经、性味查询
- 📖 **详情查看** — 每味药的性味归经、功效主治、用法用量、禁忌
- 🏷️ **分类浏览** — 按功效分类（解表药、清热药、补益药等）

## 数据来源

药材数据基于《中国药典》及相关中医药典籍整理，仅供参考，不构成用药建议。

## 用法

```bash
# 安装依赖
pip install -r requirements.txt

# 启动Web服务
python app.py

# 或命令行查询
python query.py 黄芪
```

## 数据格式

`data/herbs.json` — JSON格式，每味药包含：
- `name` — 名称
- `pinyin` — 拼音
- `category` — 分类
- `properties` — 性味
- `meridian` — 归经
- `effects` — 功效主治
- `usage` — 用法用量
- `contraindications` — 禁忌/注意事项
- `related` — 相关配伍

## 许可

MIT
