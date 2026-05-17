# Everything Claude Code — 中文仪表盘版

<p align="center">
  <img src="assets/hero.png" alt="ECC Dashboard" width="600"/>
</p>

<p align="center">
  <b>ECC 中文仪表盘 · 一站式 Claude Code 插件管理</b><br/>
  <sub>基于 <a href="https://github.com/afffaan-m/everything-claude-code">everything-claude-code</a> 增强的中文版本</sub>
</p>

<p align="center">
  <a href="https://github.com/afffaan-m/everything-claude-code"><img src="https://img.shields.io/badge/上游-ECC_原项目-blue" alt="Upstream"/></a>
  <a href="https://github.com/LiHuaInCh/everything-claude-code-/blob/main/ECL-2.0.md"><img src="https://img.shields.io/badge/license-ECL_2.0-green" alt="License"/></a>
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform"/>
</p>

> 本项目是 [everything-claude-code](https://github.com/afffaan-m/everything-claude-code) 的 Fork，核心改动是新增 **ECC 中文仪表盘**（`ecc_dashboard.py`），将所有 Agent、Skill、Command、Rule 翻译为中文，方便中文用户浏览和管理。

## 中文仪表盘

```
python ecc_dashboard.py
```

启动后是一个 TkInter 图形界面，包含 5 个标签页：

| 标签 | 内容 |
|------|------|
| **智能体** | 80+ 个 Agent，名称和用途全部翻译为中文 |
| **技能** | 400+ 个 Skill，按类别分组，中文名称 + 原文对照 |
| **命令** | 所有 Slash 命令，中文说明 |
| **规则** | 语言/框架专属规则，分类浏览 |
| **设置** | ECC 配置管理 |

### 仪表盘功能

- **全文搜索** — 搜索所有 Agent、Skill、Command、Rule
- **中文翻译** — Agent 名称、描述、使用场景全部中文化
- **分类筛选** — 按语言/框架/用途分类浏览
- **一键打开** — 点击即可在编辑器中打开对应文件
- **Agent 详情** — 查看每个 Agent 的工具列表、适用场景

### 翻译示例

| 英文原文 | 中文翻译 |
|----------|----------|
| code-reviewer | 代码审查 |
| tdd-guide | TDD 指南 |
| security-reviewer | 安全审查 |
| architect | 软件架构师 |
| planner | 规划器 |

## 安装

```bash
git clone https://github.com/LiHuaInCh/everything-claude-code-.git
cd everything-claude-code-
./install.sh   # 或 install.bat (Windows)
```

## 与原项目的区别

| | 原版 ECC | 中文仪表盘版 |
|---|---|---|
| Agent 名称 | 英文 | 中文 + 英文原文 |
| Skill 名称 | 英文 | 中文 + 英文原文 |
| GUI 管理 | 无 | TkInter 图形仪表盘 |
| 搜索功能 | 命令行 | 图形界面全文搜索 |
| 原项目功能 | 全部保留 | 全部保留 |

## 项目结构

```
├── ecc_dashboard.py      # 中文仪表盘（新增）
├── agents/               # 80+ AI Agent 定义
├── skills/               # 400+ 技能定义
├── commands/             # Slash 命令
├── rules/                # 语言/框架规则
├── hooks/                # 自动化钩子
└── mcp-configs/          # MCP 服务器配置
```

## License

ECL 2.0 © [afffaan-m](https://github.com/afffaan-m)

---

> 中文仪表盘由 [LiHuaInCh](https://github.com/LiHuaInCh) 开发
