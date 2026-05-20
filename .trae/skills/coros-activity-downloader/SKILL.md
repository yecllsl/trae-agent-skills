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
  - name: Chrome DevTools MCP
    optional: false
enabled_tools:
  - mcp_Chrome_DevTools_MCP_navigate_page
  - mcp_Chrome_DevTools_MCP_evaluate_script
---

# Coros活动数据下载技能

## Purpose

从 COROS Training Hub 自动下载跑步活动记录（FIT 格式），支持智能去重和增量同步，适用于：

- 定期备份运动数据
- 批量导出活动记录
- 自动化数据同步任务

## Prerequisites

1. **COROS 账户**：已登录 COROS Training Hub（<https://t.coros.com>）
2. **Chrome DevTools MCP**：已配置 Chrome DevTools MCP 连接器，确保浏览器已登录 COROS 账户
3. **Python 环境**：Python 3.6+（用于辅助脚本）
4. **配置文件**：`config.json` 中设置正确的 `downloadDir`

## Usage

### 自动化任务调用

```
调用 coros-activity-downloader 技能，下载最新的不重复的跑步记录
```

### 执行步骤

1. 使用 `mcp_Chrome_DevTools_MCP_navigate_page` 访问活动列表页面 `https://t.coros.com/admin/views/activities`
2. 使用 `mcp_Chrome_DevTools_MCP_evaluate_script` 执行 JavaScript 提取活动列表数据（labelId、name、sportType）
3. 筛选 `sportType=100` 的跑步活动
4. 扫描下载目录，基于 labelId 去重
5. 将未下载的活动列表作为 `--activities-json` 参数传入 Python 脚本
6. 脚本通过 HTTP 直接请求 COROS CDN 下载 FIT 文件
7. 保存到配置的下载目录

### 命令行脚本

```bash
# 使用 Chrome DevTools MCP 获取活动后，通过脚本下载
python scripts/download_coros.py --count 15 --activities-json '<JSON>'

# 指定下载目录
python scripts/download_coros.py --download-dir "D:\COROS_Backup" --activities-json '<JSON>'

# 仅验证现有文件
python scripts/download_coros.py --validate-only

# JSON 输出模式（便于程序化调用）
python scripts/download_coros.py --json-output --activities-json '<JSON>'
```

### 参数说明

| 参数                  | 类型     | 默认值             | 说明           |
| ------------------- | ------ | --------------- | ------------ |
| `--count`           | int    | 10              | 下载数量         |
| `--activities-json` | string | -               | 活动列表 JSON 字符串 |
| `--label-ids`       | string | -               | 直接指定 labelId（逗号分隔） |
| `--user-id`         | string | config.json 配置值 | COROS 用户 ID   |
| `--download-dir`    | string | config.json 配置值 | 下载目录         |
| `--sport-type`      | int    | 100             | 运动类型（100=跑步） |
| `--validate-only`   | flag   | false           | 仅验证，不下载      |
| `--json-output`     | flag   | false           | JSON 格式输出    |
| `--show-config`     | flag   | false           | 显示当前配置并退出 |

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          执行流程                                        │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. 访问活动页面                                                          │
│     navigate_page(url="https://t.coros.com/admin/views/activities")       │
│            │                                                             │
│            ▼                                                             │
│  2. 提取活动数据                                                          │
│     evaluate_script(提取 labelId + name + sportType)                      │
│            │                                                             │
│            ▼                                                             │
│  3. 筛选跑步活动                                                          │
│     filter(sportType === 100)                                            │
│            │                                                             │
│            ▼                                                             │
│  4. 去重检查                                                              │
│     scan(downloadDir) → existing labelIds                                │
│            │                                                             │
│            ▼                                                             │
│  5. 传入 Python 脚本                                                      │
│     --activities-json '<新活动JSON>'                                       │
│            │                                                             │
│            ▼                                                             │
│  6. 脚本通过 HTTP 请求 COROS CDN 下载 FIT                                  │
│     urllib → https://oss.coros.com/fit/{userId}/{labelId}.fit            │
│            │                                                             │
│            ▼                                                             │
│  7. 保存文件                                                              │
│     {name}_{labelId}.fit                                                 │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 文件结构

```
coros-activity-downloader/
├── SKILL.md           # 技能定义（本文件）
├── README.md          # 使用说明
├── CHANGELOG.md       # 更新日志
├── config.json        # 可选配置文件（不存在时使用脚本内默认值）
└── scripts/
    └── download_coros.py  # 下载脚本
```

### 运动类型代码

| sportType | 运动类型 |
| --------- | ---- |
| 100       | 跑步   |
| 101       | 骑行   |
| 102       | 游泳   |
| 103       | 徒步   |
| 104       | 健身   |

## Error Handling

| 错误类型      | 原因               | 解决方案                              |
| --------- | ---------------- | --------------------------------- |
| HTTP 404  | COROS CDN 返回 404，活动已删除或 userId 不正确 | 检查活动是否存在，验证 config.json 中的 userId |
| 文件大小为 0   | 网络中断或权限问题        | 重新执行，脚本会自动重试                      |
| 下载目录不存在   | 路径配置错误           | 检查 config.json 中的 downloadDir     |
| Chrome DevTools MCP 不可用 | 连接器未配置或浏览器未登录 | 检查 MCP 配置，确保浏览器已登录 COROS 账户 |
| 无新活动      | 所有活动已下载          | 正常情况，无需处理                         |
| JavaScript 执行失败 | 页面结构变化         | 检查页面 HTML 结构，更新提取脚本                |
| 未提供活动列表 | 未指定 `--activities-json` 或 `--label-ids` | 必须提供至少一种方式来指定要下载的活动 |

### 日志输出

脚本支持两种输出模式：

- **人类可读模式**（默认）：彩色输出，进度条，摘要统计
- **JSON 模式**（`--json-output`）：结构化输出，便于程序解析
