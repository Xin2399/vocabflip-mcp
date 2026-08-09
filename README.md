# vocabflip

专业英语词汇学习小站，为涉外知产从业者打造，也适用于任何需要系统学习领域词汇的场景。

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey) ![License](https://img.shields.io/badge/License-MIT-green)

## 功能

- **翻卡片学词** — 正面英文，翻面显示中文释义、音标和例句，一键标记"已掌握"或"需复习"
- **实战例句** — 来自真实官方文件的原句，关键词高亮展示
- **阅读练习** — PCT/知产真实语料，配套阅读理解题
- **知识测验** — 选择题，即时反馈，查漏补缺
- **学习统计** — 每日进度、批次管理、完成率一览
- **MCP 工具接入** — AI 助手可直接查询今日进度、添加词汇、查看整体进度
- **背景持久化** — 上传自定义背景图，刷新不丢失
- **主题切换** — 浅色 / 深色 / 黑白三种主题

## 技术栈

- 后端：Python / Flask / SQLite
- 前端：原生 HTML + CSS + JS（无框架，移动端友好）
- MCP：[FastMCP](https://github.com/jlowin/fastmcp)

## 快速开始

```bash
git clone https://github.com/Nixie0/vocabflip.git
cd vocabflip
pip install flask fastmcp

# 启动 Web（端口 5002）
python app.py

# 启动 MCP 服务（端口 8771，可选）
python mcp_server.py
```

浏览器打开 `http://localhost:5002` 即可使用。

## MCP 工具列表

| 工具名 | 功能 |
|--------|------|
| `vocab_check_today` | 查看今日学习情况 |
| `vocab_add_words` | 批量添加新词（JSON 格式） |
| `vocab_get_all_progress` | 查询所有批次的整体进度 |

MCP 服务使用 SSE 传输，默认端口 `8771`。

## 添加自己的词汇

通过 `vocab_add_words` 传入 JSON 数组：

```json
[
  {
    "word": "prior art",
    "phonetic": "/ˈpraɪər ɑːrt/",
    "meaning": "现有技术",
    "example": "The invention must be novel over the prior art."
  }
]
```

也可以直接操作 `vocab.db` 写入 SQLite 数据库。

## License

MIT
