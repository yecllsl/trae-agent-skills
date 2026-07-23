# 贡献指南

感谢你对 Trae 敏捷开发规范与工作流项目的兴趣！本文档将帮助你了解如何为项目做出贡献。

## 🎯 项目定位

本项目是一套**针对 Trae CN IDE 的 Agentic AI 编程敏捷开发规范与工作流定义**，贡献方向包括：

- 完善工作流规范（`.trae/开发流程规范.md`）
- 新增/改进 BMAD 智能体（`.trae/agents/`）
- 新增/改进快捷命令（`.trae/commands/`）
- 新增方法论 Skill（`.trae/skills/`）
- 完善规则体系（`.trae/rules/`）
- 改进文档

## 📋 贡献方式

### 1. 报告问题

通过 [GitHub Issues](../../issues) 提交，包含：
- 问题描述（规范漏洞、Agent 行为异常、命令流程问题）
- 复现步骤
- 期望行为 vs 实际行为
- 环境信息（Trae 版本、模型）

### 2. 改进规范

规范类贡献（工作流、门控、异常处理）：

1. **Fork 仓库** 并创建分支 `docs/improve-<topic>`
2. **修改** `.trae/开发流程规范.md` 或相关文档
3. **提交 PR**，说明改进点和理由

### 3. 新增/改进智能体

智能体定义贡献：

1. **Fork 仓库** 并创建分支 `agent/<role-name>`
2. **修改或新建** `.trae/agents/bmad-<role>.md`
3. **遵循 Agent 定义规范**（见下方）
4. **提交 PR**

### 4. 新增方法论 Skill

1. **Fork 仓库** 并创建分支 `skill/<skill-name>`
2. **复制模板** 从 `docs/SKILL_TEMPLATE.md`
3. **开发 Skill** 遵循规范
4. **运行验证** `python scripts/validate-skills.py -s <skill-name>`
5. **提交 PR**

### 5. 新增快捷命令

1. **Fork 仓库** 并创建分支 `cmd/<command-name>`
2. **新建** `.trae/commands/<command>.md`
3. **遵循命令格式**（`## Usage` / `## Context` / `## Your Role` / `## Execution Flow`）
4. **提交 PR**

## 📐 Agent 定义规范

### 目录结构

```
.trae/agents/
└── bmad-<role>.md      # 一个文件定义一个 Agent
```

### YAML frontmatter 必需字段

```yaml
---
name: bmad-<role>              # 必需，唯一标识
description: <场景描述>         # 必需，SOLO Agent 据此判断何时调用
model: <modelName>             # 可选，指定模型
tools: <tool1>, <tool2>        # 可选，限制可用工具
disallowedTools: <tool>        # 可选，禁止使用的工具
mcpServers:                    # 可选，允许调用的 MCP Server
  - <mcpServerName>
---
```

### 模型选择策略

| 任务复杂度 | 推荐模型 | 典型场景 |
|-----------|---------|---------|
| 机械实现 | 快速模型（Doubao-Seed-2.1-Turbo） | CRUD、数据模型 |
| 集成判断 | 标准模型（GLM-5.2） | API 集成、组件交互 |
| 架构设计 | 最强模型（Doubao-Seed-2.1-Pro） | 架构决策、Review、调试 |

### 权限隔离原则

- 产出文档的角色（Architect、Review）应禁用 `Edit`，防止越权修改代码
- 只读角色（Orchestrator）应禁用 `Edit` + `DeleteFile`
- 需要 E2E 测试的角色（QA）应启用 `mcp_Playwright`

## 📐 Skill 开发规范

### 目录结构

```
.trae/skills/<skill-name>/
├── SKILL.md           # Skill 定义（必需）
├── README.md          # 用户文档（推荐）
├── CHANGELOG.md       # 版本历史（推荐）
└── scripts/           # 执行脚本（至少一个）
    └── script.py
```

### 命名规范

- **Skill 目录名**：kebab-case（如 `test-driven-development`）
- **脚本文件名**：snake_case（如 `validate_skills.py`）
- **函数名**：snake_case

### SKILL.md 规范

必须包含 frontmatter：

```yaml
---
name: "skill-name"
description: "简短描述，50字以内"
---
```

必须包含以下 H2 章节（按顺序）：
1. `## Purpose` — 功能目的
2. `## Prerequisites` — 依赖要求
3. `## Usage` — 使用方法
4. `## Architecture` — 架构说明
5. `## Error Handling` — 错误处理

### 代码规范

- Python 3.6+ 语法，PEP 8 风格
- 复杂逻辑添加中文注释
- CLI 脚本应支持人类可读和 `--json-output` 两种模式
- 禁止硬编码敏感信息

## 📐 命令定义规范

`.trae/commands/<command>.md` 必须包含：

```markdown
## Usage
`/<command> <ARGUMENTS> [OPTIONS]`

### Options
- `--flag`: 说明

## Context
- 输入：$ARGUMENTS
- 关键上下文说明

## Your Role
Coordinator 角色与职责描述

## Execution Flow
### Step 0: ...
### Step 1: ...
...
```

## 🔍 提交前检查清单

### 通用检查

- [ ] 修改不破坏现有工作流
- [ ] 已更新相关文档（AGENTS.md / README.md / CODE_WIKI.md）
- [ ] 已更新 CHANGELOG.md
- [ ] 没有硬编码的敏感信息

### Agent 检查

- [ ] YAML frontmatter 字段完整（name + description）
- [ ] model 字段符合模型选择策略
- [ ] 权限隔离合理（文档角色禁用 Edit，只读角色禁用 Edit+DeleteFile）
- [ ] 职责描述与 [开发流程规范.md](file:///d:/yecll/Documents/LocalCode/testskills/.trae/开发流程规范.md) 一致

### Skill 检查

- [ ] 已运行 `python scripts/validate-skills.py -s <skill-name>` 并通过
- [ ] SKILL.md 含 frontmatter + 5 个必需章节
- [ ] scripts/ 目录含至少一个可执行脚本

### 命令检查

- [ ] 含 Usage / Context / Your Role / Execution Flow 四个部分
- [ ] 引用的 Agent 已存在
- [ ] 引用的规范章节准确
- [ ] 🛑 STOP POINT 标记清晰

## 📝 Pull Request 流程

1. **创建分支**

   ```bash
   # 规范类
   git checkout -b docs/improve-workflow

   # Agent 类
   git checkout -b agent/bmad-new-role

   # Skill 类
   git checkout -b skill/new-skill-name

   # 命令类
   git checkout -b cmd/new-command
   ```

2. **提交更改**

   ```bash
   git add <specific-files>
   git commit -m "docs: 完善六阶段工作流门控"
   # 或
   git commit -m "Add agent: bmad-new-role v1.0.0"
   # 或
   git commit -m "Add skill: new-skill-name v1.0.0"
   ```

3. **推送到你的 Fork**

   ```bash
   git push origin <branch-name>
   ```

4. **创建 Pull Request**
   - 标题格式：`<type>: <description>`（如 `docs: 完善门控体系`）
   - 描述中包含变更说明
   - 关联相关 Issue（如有）

### Commit 类型约定

| 类型 | 用途 | 示例 |
|------|------|------|
| `docs` | 文档/规范改进 | `docs: 完善六阶段门控` |
| `Add agent` | 新增 Agent | `Add agent: bmad-new-role v1.0.0` |
| `Add skill` | 新增 Skill | `Add skill: new-skill v1.0.0` |
| `Add cmd` | 新增命令 | `Add cmd: bmad-deploy v1.0.0` |
| `fix` | 修复规范漏洞 | `fix: 修正架构审批 STOP POINT` |
| `refactor` | 重构 | `refactor: 合并指令手册到流程规范` |

## 💬 沟通指南

- 保持友善和尊重
- 提供建设性的反馈
- 接受不同的观点
- 专注于技术讨论

## 📞 获取帮助

1. 查看 [CODE_WIKI.md](file:///d:/yecll/Documents/LocalCode/testskills/CODE_WIKI.md) — 架构级 Wiki
2. 查看 [.trae/开发流程规范.md](file:///d:/yecll/Documents/LocalCode/testskills/.trae/开发流程规范.md) — 流程权威定义
3. 参考 [Skill 开发指南](file:///d:/yecll/Documents/LocalCode/testskills/docs/SKILL_DEVELOPMENT_GUIDE.md)
4. 在 Issue 中提问

再次感谢你的贡献！
