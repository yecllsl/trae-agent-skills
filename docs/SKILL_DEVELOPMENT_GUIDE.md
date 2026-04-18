# Skill 开发指南

本文档介绍如何为 Trae Agent Skills 项目开发新的 Skill。

## 目录

1. [Skill 概述](#skill-概述)
2. [开发环境准备](#开发环境准备)
3. [Skill 结构](#skill-结构)
4. [SKILL.md 规范](#skillmd-规范)
5. [脚本开发](#脚本开发)
6. [测试和验证](#测试和验证)
7. [提交和发布](#提交和发布)

## Skill 概述

### 什么是 Skill？

Skill 是 Trae IDE 的 Agent 能力扩展，通过预定义的指令和脚本，让 AI 助手能够执行特定任务。

### Skill 的组成部分

- **SKILL.md**: Skill 的定义文档，包含元数据、使用说明、架构描述
- **脚本**: 实际执行任务的代码（Python、JavaScript 等）
- **README.md**: 面向用户的文档
- **可选**: 测试、示例、详细文档

## 开发环境准备

### 基本要求

- Trae IDE 安装并配置
- Python 3.6+（如果开发 Python Skill）
- Git 用于版本控制

### 项目设置

1. Fork 或克隆本项目
   ```bash
   git clone https://github.com/你的用户名/trae-agent-skills.git
   cd trae-agent-skills
   ```

2. 创建新的 Skill 目录
   ```bash
   mkdir skills/my-new-skill
   cd skills/my-new-skill
   ```

## Skill 结构

标准的 Skill 目录结构：

```
my-new-skill/
├── README.md              # 用户文档（必需）
├── SKILL.md               # Skill 定义（必需）
├── CHANGELOG.md           # 版本历史（推荐）
├── scripts/               # 执行脚本
│   └── main.py
├── docs/                  # 详细文档（可选）
│   └── advanced-usage.md
└── tests/                 # 测试文件（可选）
    └── test_main.py
```

### 文件说明

#### README.md

面向最终用户的文档，应包含：
- 功能简介
- 使用方法
- 参数说明
- 示例
- 常见问题

#### SKILL.md

Trae Agent 使用的技术文档，必须包含：
- Frontmatter（元数据）
- Purpose（目的）
- Prerequisites（依赖）
- Usage（使用方式）
- Architecture（架构）
- Error Handling（错误处理）

#### scripts/

存放执行脚本，支持多种语言：
- Python（推荐）
- JavaScript/Node.js
- PowerShell
- Shell

## SKILL.md 规范

### Frontmatter

每个 SKILL.md 必须以 YAML frontmatter 开头：

```yaml
---
name: "skill-name"
description: "简短描述，50字以内"
---
```

### 必需章节

#### 1. Purpose

描述 Skill 的功能目的：

```markdown
## Purpose

This skill enables automated downloading of running activity records from the COROS Training Hub platform.
```

#### 2. Prerequisites and Dependencies

列出所有依赖：

```markdown
## Prerequisites and Dependencies

### System Requirements
- **Operating System**: Windows 10/11
- **Python**: Python 3.6+
- **Browser**: Chrome browser

### Authentication Requirements
- Valid COROS account
```

#### 3. Usage

提供使用示例：

```markdown
## Quick Start

### Step 1: Do something
```
command here
```

### Step 2: Do another thing
```
```

#### 4. Architecture

描述架构和数据流：

```markdown
## Architecture Overview

```
[Architecture diagram]
```
```

#### 5. Error Handling

列出常见错误和解决方案：

```markdown
## Error Handling

### Common Issues

#### 1. Error Name
Description and solution.
```

## 脚本开发

### Python 脚本规范

#### 文件头

```python
#!/usr/bin/env python3
"""
Skill Name

Brief description of what this script does.

Usage:
    python script.py --arg1 value1
    python script.py --help
"""
```

#### 代码风格

- 使用 4 空格缩进
- 函数和变量使用 snake_case
- 类使用 PascalCase
- 常量使用 UPPER_CASE
- 添加中文注释解释复杂逻辑

#### 示例结构

```python
import argparse
import json

# 配置常量
DEFAULT_TIMEOUT = 30


def main_function():
    """主功能函数的中文说明"""
    pass


def helper_function():
    """辅助函数的中文说明"""
    pass


def main():
    """CLI入口点"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--arg', help='参数说明')
    args = parser.parse_args()
    
    # 执行主逻辑
    result = main_function()
    print(json.dumps(result))


if __name__ == '__main__':
    main()
```

### 错误处理

```python
try:
    result = risky_operation()
except SpecificError as e:
    # 处理特定错误
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    # 处理未知错误
    print(f"Unexpected error: {e}", file=sys.stderr)
    sys.exit(1)
```

### 输出格式

支持两种输出模式：

1. **人类可读模式**（默认）：
   ```
   Downloading: 活动名称... OK (95.76 KB)
   ```

2. **JSON 模式**（用于程序化调用）：
   ```bash
   python script.py --json-output
   ```
   
   输出：
   ```json
   {
     "success": true,
     "data": {...}
   }
   ```

## 测试和验证

### 本地测试

在提交前，确保：

1. **功能测试**
   ```bash
   python scripts/your_script.py --test
   ```

2. **验证脚本检查**
   ```bash
   python scripts/validate-skills.py
   ```

3. **Trae IDE 测试**
   - 将 Skill 复制到 `~/.trae/skills/`
   - 在 Trae 中测试调用

### 验证清单

- [ ] SKILL.md 包含所有必需章节
- [ ] README.md 清晰易懂
- [ ] 脚本可以独立运行
- [ ] 错误处理完善
- [ ] 没有硬编码的敏感信息
- [ ] 代码有适当的中文注释

## 提交和发布

### 提交前准备

1. 更新 CHANGELOG.md
2. 运行验证脚本
3. 检查代码风格

### 提交信息格式

```
Add skill: skill-name v1.0.0

- Brief description of the skill
- Key features
- Any special notes
```

### Pull Request 流程

1. 创建功能分支
   ```bash
   git checkout -b feature/my-skill
   ```

2. 提交更改
   ```bash
   git add .
   git commit -m "Add skill: my-skill v1.0.0"
   ```

3. 推送到 GitHub
   ```bash
   git push origin feature/my-skill
   ```

4. 创建 Pull Request
   - 标题：`Add skill: my-skill v1.0.0`
   - 描述：包含功能说明和使用示例

## 最佳实践

### DO（推荐）

- ✅ 使用清晰的命名
- ✅ 添加详细的中文注释
- ✅ 处理边界情况
- ✅ 提供 JSON 输出模式
- ✅ 验证输入参数
- ✅ 使用标准库（减少依赖）

### DON'T（避免）

- ❌ 硬编码敏感信息
- ❌ 忽略错误处理
- ❌ 使用平台特定代码（除非必要）
- ❌ 添加不必要的依赖
- ❌ 混合多种语言（除非必要）

## 示例 Skill

参考现有的 Skill：

- [coros-activity-downloader](../skills/coros-activity-downloader/) - 完整的 Python Skill 示例

## 获取帮助

- 查看现有 Skill 的实现
- 阅读 [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md)
- 在 Issue 中提问

---

祝你开发愉快！
