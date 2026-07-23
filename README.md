# 中药饮片查询工具 🍃

基于《中国药典》2020年版的中药饮片信息查询系统，支持**性味归经、功效主治、炮制规范**多维度检索。

## 功能

- 🔍 **多维度查询** — 按名称、拼音、功效、归经、炮制品名称搜索
- 📖 **详情查看** — 每味药的性味归经、功效主治、用法用量、禁忌
- 🏗️ **炮制规范** — 净制、切制、饮片标准，以及不同炮制品的工艺与功效
- 🏷️ **分类浏览** — 按功效分类（补气药、清热药、活血化瘀药等）
- 🖥️ **命令行 + Web 双模式**

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动Web界面
python app.py
# 打开 http://127.0.0.1:5000

# 命令行查询
python query.py 黄芪
python query.py 炙黄芪           # 搜索炮制品
python query.py --list           # 按分类浏览
python query.py --all            # 全部列出（含炮制信息）
```

## 项目结构

```
chinese-herbal-medicine/
├── data/
│   └── herbs.json            # 药材数据（含炮制规范）
├── docs/
│   ├── processing-specifications.md  # 炮制规范全文（药典通则）
├── app.py                    # Web应用（Flask）
├── query.py                  # 命令行查询工具
├── build_data.py             # 数据生成脚本
├── requirements.txt
└── README.md
```

## 数据字段

`data/herbs.json` 每味药材包含：

| 字段 | 说明 |
|------|------|
| `name` | 名称 |
| `pinyin` | 拼音 |
| `category` | 分类 |
| `properties` | 性味 |
| `meridian` | 归经 |
| `effects` | 功效主治 |
| `usage` | 用法用量 |
| `contraindications` | 禁忌/注意事项 |
| `related` | 相关配伍 |
| `processing.净制` | 净制方法 |
| `processing.切制` | 切制规格 |
| `processing.standard` | 饮片标准描述 |
| `processing.processed_forms[]` | 炮制品列表（名称/炮制方法/功效） |
| `processing.notes` | 炮制备注 |

## 数据来源

- **炮制规范**：《中华人民共和国药典》2020年版四部通则 0213
- **药材数据**：基于《中国药典》及相关中医药典籍整理

> ⚠️ 仅供参考，不构成用药建议。实际应用以最新版《中国药典》及各省市炮制规范为准。

## 许可

MIT
