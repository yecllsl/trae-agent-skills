# AGENTS.md — Trae 敏捷开发规范与工作流

本项目是一套**针对 Trae CN IDE（SOLO Agent 模式）的 Agentic AI 编程敏捷开发规范与工作流定义**，将软件工程六阶段（需求、设计、开发、测试、部署、维护）封装为可执行的流水线，由 Coordinator 编排专业 Subagent 协作完成。

## 项目定位

| 维度 | 说明 |
|------|------|
| **目标** | 在 Trae CN SOLO Agent 环境下，实现高效协作、快速迭代、质量可控的 Agentic AI 编程 |
| **核心产物** | 角色体系 + 全流程工作流 + 质量门控 + 快捷命令 + 方法论 Skill |
| **适用环境** | Trae CN IDE（SOLO Agent 模式） |

## Repo structure

```
.trae/                              # 方法论体系（核心内容）
├── agents/                         # 智能体定义（BMAD 7 角色）
│   ├── bmad-architect.md           # 架构师（最强模型，不编辑代码）
│   ├── bmad-dev.md                 # 开发工程师（TDD 实现）
│   ├── bmad-orchestrator.md        # 仓库扫描/上下文准备（只读）
│   ├── bmad-po.md                  # 产品经理（需求收集+PRD）
│   ├── bmad-qa.md                  # 测试工程师（Playwright 优先）
│   ├── bmad-review.md              # 代码审查（不修改代码）
│   └── bmad-sm.md                  # Scrum Master（Sprint 规划）
├── commands/                       # 快捷命令
│   ├── bmad-pilot.md               # 完整开发流程
│   ├── bmad-fix.md                 # Bug 修复流程
│   └── bmad-refine.md              # 单独精炼 PRD/架构/计划
├── rules/                          # 规则体系
│   ├── project-rules.md            # 项目规则（含 Coordinator 规则）
│   ├── security-rules.md           # 安全规则
│   ├── compliance-rules.md         # 合规规则
│   ├── quality-rules.md            # 质量规则
│   ├── process-rules.md            # 流程规则
│   └── ponytail.md                 # YAGNI / 简洁性原则
├── skills/                         # 方法论 Skill（14 个）
│   ├── brainstorming/              # 需求/方案探索
│   ├── writing-plans/              # 实施计划编写
│   ├── test-driven-development/    # TDD 铁律
│   ├── systematic-debugging/       # 根因定位四阶段
│   ├── subagent-driven-development/# 逐任务派发+Review
│   ├── dispatching-parallel-agents/# 并行任务派发
│   ├── executing-plans/            # 计划执行
│   ├── requesting-code-review/     # 代码审查请求
│   ├── receiving-code-review/      # 审查反馈处理
│   ├── verification-before-completion/ # 完成前强制验证
│   ├── using-git-worktrees/        # 工作区隔离
│   ├── finishing-a-development-branch/ # 分支完成与合并
│   ├── writing-skills/             # Skill 编写规范
│   └── using-superpowers/          # Skill 发现与使用
├── 开发流程规范.md                  # 统一流程手册（六阶段+门控+异常处理）
└── skill-config.json               # Skill 配置

docs/                               # 开发文档
├── SKILL_DEVELOPMENT_GUIDE.md      # Skill 开发指南
└── SKILL_TEMPLATE.md               # Skill 模板

scripts/                            # 工具脚本
└── validate-skills.py              # Skill 验证脚本
```

## 智能体体系

主 Agent 承担 Coordinator 职责，编排 7 个 BMAD Subagent 协作完成全流程：

| Agent | 模型 | 职责 | 权限约束 |
|-------|------|------|---------|
| **Coordinator**（主 Agent） | — | 工作流编排、门控、异常回退 | 不直接编码 |
| [bmad-orchestrator](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-orchestrator.md) | GLM-5.2 | 仓库扫描、上下文准备 | 只读（禁用 Edit/DeleteFile） |
| [bmad-po](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-po.md) | Doubao-Seed-2.1-Pro | 需求收集、PRD 编写、质量评分 | — |
| [bmad-architect](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-architect.md) | Doubao-Seed-2.1-Pro | 架构设计、技术选型 | 禁用 Edit（不直接改代码） |
| [bmad-sm](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-sm.md) | GLM-5.2 | Sprint 规划、任务拆解 | — |
| [bmad-dev](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-dev.md) | GLM-5.2 | 功能实现、单元测试、Bug 修复 | — |
| [bmad-review](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-review.md) | Doubao-Seed-2.1-Pro | 代码审查、需求合规检查 | 禁用 Edit（不修改代码） |
| [bmad-qa](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-qa.md) | GLM-5.2 | 测试策略、测试执行、回归 | 启用 mcp_Playwright |

## 工作流概览

六阶段大循环：**需求分析 → 设计 → 开发 → 测试 → 部署 → 维护**，详见 [开发流程规范.md](file:///d:/yecll/Documents/LocalCode/testskills/.trae/开发流程规范.md)。

三种执行策略（按复杂度）：

| 策略 | 适用场景 | 交互频率 |
|------|---------|---------|
| **Inline Execution** | Bug 修复、单函数、配置变更 | 低（1-2 次确认） |
| **Standard Workflow** | 新功能、多文件变更 | 中（3-4 次确认） |
| **Full Workflow** | 大型项目、多 Sprint、跨模块 | 高（6+ 次确认） |

## 快捷命令

| 命令 | 用途 |
|------|------|
| `/bmad-pilot <描述>` | 启动完整开发流程（支持 `--skip-tests` / `--direct-dev` / `--skip-scan`） |
| `/bmad-fix <Bug 描述>` | Bug 修复流程（systematic-debugging + TDD） |
| `/bmad-refine <target>` | 单独精炼 PRD / 架构 / Sprint 计划 |

## 质量门控

四道门控贯穿全流程：

1. **实现前** — 规格审批 + 计划审批 + 环境隔离
2. **实现中** — TDD 循环完成 + self-review 完成
3. **验证前** — 测试套件通过 + 构建成功 + Lint/TypeCheck 通过
4. **合并前** — 验证证据新鲜（<5min）+ Review 通过 + 安全扫描通过

## Validation

- `python scripts/validate-skills.py` — 检查所有 skills 结构
- `python scripts/validate-skills.py -s <skill-name>` — 检查单个 skill
- `python scripts/validate-skills.py -v` — 详细输出

## Style conventions

- Agent 文件：`bmad-<role>.md`，YAML frontmatter 含 name/description/model/权限字段
- Skill 目录：kebab-case（如 `test-driven-development`）
- 脚本文件名：snake_case
- Python：PEP 8，snake_case 函数，4 空格缩进，复杂逻辑中文注释
- Commit 格式：`Add skill: skill-name v1.0.0` / `docs: 更新流程规范`

## Environment

- Python 3.6+（`.venv/` 虚拟环境，gitignored）
- Playwright MCP（bmad-qa 启用，E2E 测试优先）
- `.trae/cache/`、`.trae/logs/` gitignored
- 敏感文件（`.env`、`*.pem`、`*.key`、`credentials.json`）gitignored
