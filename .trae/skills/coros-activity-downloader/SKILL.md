---
name: "coros-activity-downloader"
description: "下载COROS跑步活动FIT文件，支持去重"
version: "2.1.0"
author: "nanobot-runner"
tags:
  - coros
  - activity
  - download
  - fit
dependencies:
  - name: coros
    optional: false
enabled_tools:
  - mcp_coros_download_activity
  - mcp_coros_list_activities
---

# Coros活动数据下载技能

## Purpose

从 COROS Training Hub 自动下载跑步活动记录（FIT 格式），支持智能去重和增量同步，适用于：
- 定期备份运动数据
- 批量导出活动记录
- 自动化数据同步任务

## Prerequisites

1. **COROS 账户**：已登录 COROS Training Hub (https://t.coros.com)
2. **MCP 工具**：已配置 `coros` MCP 连接器
3. **Python 环境**：Python 3.6+（用于辅助脚本）
4. **配置文件**：`config.json` 中设置正确的 `userId` 和 `downloadDir`

## Usage

### 自动化任务调用

```
调用 coros-activity-downloader 技能，下载最新的不重复的跑步记录
```

### 执行步骤

1. 使用 `mcp_coros_list_activities` 获取活动列表
2. 筛选 `sportType=100` 的跑步活动
3. 扫描下载目录，基于 labelId 去重
4. 使用 `mcp_coros_download_activity` 下载新活动
5. 保存到配置的下载目录

### 命令行脚本

```bash
# 使用 MCP 工具获取活动后，通过脚本下载
python scripts/download_coros.py --count 15 --activities-json '<JSON>'

# 指定下载目录
python scripts/download_coros.py --download-dir "D:\COROS_Backup" --activities-json '<JSON>'

# 仅验证现有文件
python scripts/download_coros.py --validate-only

# JSON 输出模式（便于程序化调用）
python scripts/download_coros.py --json-output --activities-json '<JSON>'
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--count` | int | 10 | 下载数量 |
| `--activities-json` | string | - | 活动列表 JSON |
| `--download-dir` | string | 见 config.json | 下载目录 |
| `--sport-type` | int | 100 | 运动类型（100=跑步） |
| `--validate-only` | flag | false | 仅验证，不下载 |
| `--json-output` | flag | false | JSON 格式输出 |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    执行流程                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 获取活动列表                                         │
│     mcp_coros_list_activities()                         │
│            │                                            │
│            ▼                                            │
│  2. 筛选跑步活动                                         │
│     filter(sportType === 100)                           │
│            │                                            │
│            ▼                                            │
│  3. 去重检查                                             │
│     scan(downloadDir) → existing labelIds               │
│            │                                            │
│            ▼                                            │
│  4. 下载新活动                                           │
│     mcp_coros_download_activity(labelId)                │
│            │                                            │
│            ▼                                            │
│  5. 保存文件                                             │
│     {name}_{labelId}.fit                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 文件结构

```
coros-activity-downloader/
├── SKILL.md           # 技能定义（本文件）
├── README.md          # 使用说明
├── CHANGELOG.md       # 更新日志
├── config.json        # 配置文件
└── scripts/
    └── download_coros.py  # 下载脚本
```

### 运动类型代码

| sportType | 运动类型 |
|-----------|---------|
| 100 | 跑步 |
| 101 | 骑行 |
| 102 | 游泳 |
| 103 | 徒步 |
| 104 | 健身 |

## Error Handling

| 错误类型 | 原因 | 解决方案 |
|---------|------|---------|
| HTTP 404 | 活动已删除或 userId 错误 | 检查活动是否存在，验证 config.json 中的 userId |
| 文件大小为 0 | 网络中断或权限问题 | 重新执行，脚本会自动重试 |
| 下载目录不存在 | 路径配置错误 | 检查 config.json 中的 downloadDir |
| MCP 工具不可用 | coros 连接器未配置 | 检查 MCP 配置并重新连接 |
| 无新活动 | 所有活动已下载 | 正常情况，无需处理 |

### 日志输出

脚本支持两种输出模式：
- **人类可读模式**（默认）：彩色输出，进度条，摘要统计
- **JSON 模式**（`--json-output`）：结构化输出，便于程序解析
