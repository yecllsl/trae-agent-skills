# Trae Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills Count](https://img.shields.io/badge/skills-18-blue.svg)]()

本项目是作者在使用 [Trae CN IDE](https://www.trae.ai/) 和 Trae Work 过程中的经验总结与方法论实践，包含一套完整的 AI 辅助开发工作流体系。

## 项目定位

本项目包含完整的 AI 辅助开发方法论体系：

1. **方法论体系**（`.trae/` 目录）：完整的 AI 辅助开发方法论，包括智能体协作规范、Skills 协作规范、规则体系等
2. **自定义 Skills**（`.trae/skills/` 目录）：覆盖软件开发全生命周期的 Skill，包含方法论型和功能型两类

## 核心内容

### 方法论体系（`.trae/` 目录）

所有方法论内容存放于 `.trae/` 目录，包含：

#### 智能体定义（`.trae/agents/`）

定义六类专业智能体的角色职责和执行规范：

| 智能体 | 职责 | 核心交付物 |
|--------|------|-----------|
| 产品经理 | 产品规划 | 产品规划方案 |
| 架构师 | 需求分析、架构设计、任务拆解 | 需求规格说明书、架构设计方案、任务清单 |
| 开发工程师 | 功能开发、单元测试、Bug修复 | 功能代码、单元测试、开发交付报告 |
| 测试工程师 | 测试策略、测试执行、质量评估 | 测试用例、测试报告、Bug清单 |
| 发布运维工程师 | CICD、自动化发布、文档管理 | 流水线配置、发布报告 |
| 代码评审工程师 | 代码质量评审、安全审计 | 代码评审报告 |

#### 自定义 Skills（`.trae/skills/`）

包含方法论型和功能型两类 Skill，覆盖软件开发全生命周期：

**产品与需求阶段**
- `产品规划` - 定义产品愿景和路线图
- `需求分析` - 拆解业务诉求为功能点

**架构与设计阶段**
- `架构设计` - 设计系统架构和技术方案
- `架构评审` - 评审架构方案可行性
- `任务拆解` - 将架构方案拆解为开发任务

**开发阶段**
- `功能开发` - 完成代码开发与单元测试
- `Bug修复` - 修复 Bug 并更新测试
- `代码优化` - 优化代码结构与性能

**评审与测试阶段**
- `代码评审` - 评审代码质量与架构一致性
- `测试策略` - 制定测试策略与门禁规则
- `测试执行` - 执行测试并输出报告
- `回归测试` - 验证 Bug 修复并给出上线结论

**发布与运维阶段**
- `文档更新` - 更新用户文档和全局文档
- `CICD验证` - 验证流水线正常执行
- `单人自动化发布` - 执行版本发布
- `FIX-CI` - 自动诊断并修复 CI 流水线问题
- `文档归档` - 归档版本相关文档

**功能型 Skill**
- `coros-activity-downloader` - 从 COROS Training Hub 下载跑步活动记录

#### 规则体系（`.trae/rules/`）

定义开发过程中的各类约束和规范：

- `project-rules.md` - 项目总规则、协同黄金法则
- `security-rules.md` - 安全规则（输入验证/敏感数据/访问控制）
- `compliance-rules.md` - 合规规则（代码审计/许可证/数据隐私）
- `quality-rules.md` - 质量规则（测试覆盖/代码规范/文档完整）
- `process-rules.md` - 流程规则（开发过程/分支策略/审批流程）
- `ponytail.md` - YAGNI 原则与代码简洁性规范

#### 协作规范文档

- `指令手册.md` - 六类智能体的核心执行指令定义（查表型速查）
- `协作链路.md` - 版本迭代全流程协作规范（流程型操作手册）
- `Skills协作.md` - 全局 Skill 与项目 Skill 协作规范（决策型方法论）
- `完整流程调用规范.md` - 完整开发流程的 Skill 调用规范

### 功能型 Skill 示例（`.trae/skills/coros-activity-downloader/`）

从 COROS Training Hub 自动下载跑步活动记录（FIT 格式），支持智能去重和增量同步。

**功能特性**
- 自动登录 COROS Training Hub
- 智能筛选跑步活动（sportType=100）
- 基于 labelId 去重，避免重复下载
- 支持批量下载和增量同步
- 提供人类可读和 JSON 两种输出模式

**使用方法**

```bash
# 下载最新 10 条跑步记录
python .trae/skills/coros-activity-downloader/scripts/download_coros.py --count 10

# 指定下载目录
python .trae/skills/coros-activity-downloader/scripts/download_coros.py --download-dir "D:\COROS_Backup"

# JSON 输出模式（便于程序化调用）
python .trae/skills/coros-activity-downloader/scripts/download_coros.py --json-output
```

**依赖要求**
- Python 3.6+
- Chrome DevTools MCP（已在 `.trae/mcp.json` 配置）
- COROS 账户（需已登录）

## 项目结构

```
trae-agent-skills/
├── .trae/                          # 方法论体系（核心内容）
│   ├── agents/                     # 智能体定义（6 类角色）
│   │   ├── 产品经理.md
│   │   ├── 架构师.md
│   │   ├── 开发工程师.md
│   │   ├── 测试工程师.md
│   │   ├── 运维发布工程师.md
│   │   └── 代码评审工程师.md
│   ├── rules/                      # 规则体系
│   │   ├── project-rules.md        # 项目总规则
│   │   ├── security-rules.md       # 安全规则
│   │   ├── compliance-rules.md     # 合规规则
│   │   ├── quality-rules.md        # 质量规则
│   │   ├── process-rules.md        # 流程规则
│   │   └── ponytail.md             # YAGNI 原则
│   ├── skills/                     # 自定义 Skills（方法论型 + 功能型）
│   │   ├── 产品规划/
│   │   ├── 需求分析/
│   │   ├── 架构设计/
│   │   ├── 架构评审/
│   │   ├── 任务拆解/
│   │   ├── 功能开发/
│   │   ├── Bug修复/
│   │   ├── 代码优化/
│   │   ├── 代码评审/
│   │   ├── 测试策略/
│   │   ├── 测试执行/
│   │   ├── 回归测试/
│   │   ├── 文档更新/
│   │   ├── CICD验证/
│   │   ├── 单人自动化发布/
│   │   ├── FIX-CI/
│   │   ├── 文档归档/
│   │   └── coros-activity-downloader/  # 功能型 Skill 示例
│   ├── 指令手册.md                  # 智能体指令定义
│   ├── 协作链路.md                  # 协作流程规范
│   ├── Skills协作.md                # Skill 协作规范
│   ├── 完整流程调用规范.md           # 完整流程调用规范
│   ├── mcp.json                    # MCP 配置
│   └── skill-config.json           # Skill 配置
├── docs/                           # 开发文档
│   ├── SKILL_DEVELOPMENT_GUIDE.md  # Skill 开发指南
│   └── SKILL_TEMPLATE.md           # Skill 模板
├── scripts/                        # 工具脚本
│   └── validate-skills.py          # Skill 验证脚本
├── .github/                        # GitHub 配置
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── AGENTS.md                       # 项目说明（GitHub 自动渲染）
├── CONTRIBUTING.md                 # 贡献指南
├── CHANGELOG.md                    # 项目更新日志
├── LICENSE                         # MIT 许可证
└── README.md                       # 本文件
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yecllsl/trae-agent-skills.git
cd trae-agent-skills
```

### 2. 了解方法论体系

阅读 `.trae/` 目录下的文档，了解完整的 AI 辅助开发方法论：

**建议阅读顺序**：
1. `.trae/指令手册.md` - 了解六类智能体的指令定义
2. `.trae/协作链路.md` - 了解版本迭代全流程
3. `.trae/Skills协作.md` - 了解全局 Skill 与项目 Skill 的协作规范
4. `.trae/完整流程调用规范.md` - 了解完整开发流程的 Skill 调用方式

### 3. 使用自定义 Skills

将 `.trae/skills/` 目录下的 Skill 复制到你的 Trae 配置目录：

```bash
# Windows
xcopy /E /I .trae\skills\* %USERPROFILE%\.trae\skills\

# 或手动复制单个 Skill
cp -r .trae/skills/功能开发 ~/.trae/skills/
```

### 4. 运行功能型 Skill 示例

```bash
# 验证 Skill 结构
python scripts/validate-skills.py

# 运行 COROS 下载器示例
python .trae/skills/coros-activity-downloader/scripts/download_coros.py --count 10
```

## 开发新 Skill

查看 [Skill 开发指南](docs/SKILL_DEVELOPMENT_GUIDE.md) 了解如何创建自定义 Skill。

### Skill 基本要求

每个 Skill 必须包含：

```
your-skill-name/
├── SKILL.md       # Skill 定义（必需）
├── README.md      # 用户文档（必需）
└── scripts/       # 执行脚本（至少一个）
    └── main.py
```

### SKILL.md 规范

必须以 YAML frontmatter 开头：

```yaml
---
name: "skill-name"
description: "简短描述，50字以内"
---
```

必须包含以下章节：
- `## Purpose` - 功能目的
- `## Prerequisites` - 依赖要求
- `## Usage` - 使用方法
- `## Architecture` - 架构说明
- `## Error Handling` - 错误处理

## 方法论核心概念

### 两类 Skills 的协作

本项目定义了两种类型的 Skills：

**全局 Skills**（方法论）
- 位于 `~/.trae-cn/skills/`（Trae CN 内置）
- 提供通用方法论，如 brainstorming、TDD、systematic-debugging
- 与具体项目无关，可迁移到任何项目

**项目 Skills**（执行器）
- 位于 `.trae/skills/`（本项目自定义）
- 绑定当前项目，包含项目特定的业务知识
- 按标准化流程交付，输出标准化文档

### 协作黄金法则

1. **方法论先行** - 全局 Skill 决定"怎么想"，项目 Skill 决定"怎么做"
2. **串联叠加** - 两类 Skill 是串联叠加关系，不是互斥替代
3. **准入门槛** - 项目 Skill 有前置条件，不满足时先回退到上游全局 Skill

### 完整开发流程

```
产品规划 → 需求分析 → 架构设计 → 架构评审 → 任务拆解
    ↓
功能开发 → 代码评审 → 测试策略 → 测试执行
    ↓
Bug修复 → 回归测试 → 文档更新 → CICD验证 → 自动化发布
```

每个阶段都有明确的准入准出规则和验证检查点。

## 贡献

欢迎提交 Issue 和 Pull Request！

查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

## 许可证

[MIT](LICENSE) (c) 2026

## 免责声明

本项目中的 Skills 和方法论仅供个人学习和参考。使用这些 Skills 时，请确保遵守相关服务的使用条款。

## 相关链接

- [Trae IDE 官网](https://www.trae.ai/)
- [Skill 开发指南](docs/SKILL_DEVELOPMENT_GUIDE.md)
- [贡献指南](CONTRIBUTING.md)
