# AGENTS.md — Trae 生产级工程技能

本项目是一套**适用于 TRAE AI coding Agent 的生产级工程技能**。这些技能规范了软件构建过程中高级工程师所使用的流程、质量控制标准以及最佳实践，并被整合到 Agent 中，以便其在开发的每个阶段都能一致地遵循这些规范。

具体落地为：将软件工程六阶段（需求、设计、开发、测试、部署、维护）封装为可执行流水线，由 Coordinator 编排专业 Subagent 协作完成，全程质量门控。

## 项目定位

| 维度       | 说明                                                                 |
| -------- | ------------------------------------------------------------------ |
| **目标**   | 为 TRAE AI coding Agent 提供生产级工程技能，使其在每个开发阶段一致遵循高级工程师的流程、质量控制标准与最佳实践 |
| **核心产物** | 工程技能规范（流程 + 质量标准 + 最佳实践）+ 角色体系 + 全流程工作流 + 质量门控 + 快捷命令              |
| **整合方式** | 规范整合到 Agent 定义与 Skill 中，由 Agent 在各阶段一致执行                           |
| **适用环境** | Trae CN IDE（SOLO Agent 模式）                                         |

## Repo structure

```
.trae/                              # 工程技能体系（核心内容）
├── agents/                         # 智能体定义（BMAD 7 角色）
│   ├── bmad-architect.md           # 架构师（最强模型，不编辑代码）
│   ├── bmad-dev.md                 # 开发工程师（TDD 实现）
│   ├── bmad-orchestrator.md        # 仓库扫描/上下文准备（只读）
│   ├── bmad-po.md                  # 产品经理（需求收集+PRD）
│   ├── bmad-qa.md                  # 测试工程师（Playwright 优先）
│   ├── bmad-review.md              # 代码审查（不修改代码）
│   └── bmad-sm.md                  # Scrum Master（Sprint 规划）
├── commands/                       # 快捷命令（6 阶段 + 1 组合）
│   ├── bmad-requirements.md        # 阶段1：需求分析
│   ├── bmad-design.md              # 阶段2：设计（架构+Sprint）
│   ├── bmad-development.md         # 阶段3：开发（TDD+Review）
│   ├── bmad-testing.md             # 阶段4：测试（QA+回归）
│   ├── bmad-deployment.md          # 阶段5：部署（版本+CI+Tag）
│   ├── bmad-maintenance.md         # 阶段6：维护（调试+修复）
│   └── bmad-pipeline.md            # 组合命令：编排阶段 1-5
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


scripts/                            # 工具脚本

```

## 智能体体系

主 Agent 承担 Coordinator 职责，编排 7 个 BMAD Subagent 协作完成全流程：

| Agent                                                                                                  | 模型                | 职责               | 权限约束                   |
| ------------------------------------------------------------------------------------------------------ | ----------------- | ---------------- | ---------------------- |
| **Coordinator**（主 Agent）                                                                               | —                 | 工作流编排、门控、异常回退    | 不直接编码                  |
| [bmad-orchestrator](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-orchestrator.md) | GLM-5.1           | 仓库扫描、上下文准备       | 只读（禁用 Edit/DeleteFile） |
| [bmad-po](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-po.md)                     | GLM-5.2           | 需求收集、PRD 编写、质量评分 | —                      |
| [bmad-architect](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-architect.md)       | DeepSeek-V4-Pro   | 架构设计、技术选型        | Prompt constraint (no code edits; .md allowed) |
| [bmad-sm](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-sm.md)                     | Qwen3.7-plus      | Sprint 规划、任务拆解   | —                      |
| [bmad-dev](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-dev.md)                   | Kimi-k2.7-code    | 功能实现、单元测试、Bug 修复 | —                      |
| [bmad-review](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-review.md)             | GLM-5.2           | 代码审查、需求合规检查      | Prompt constraint (no code edits; .md allowed) |
| [bmad-qa](file:///d:/yecll/Documents/LocalCode/testskills/.trae/agents/bmad-qa.md)                     | DeepSeek-V4-Flash | 测试策略、测试执行、回归     | 启用 mcp\_Playwright     |

## 工作流概览

六阶段大循环：**需求分析 → 设计 → 开发 → 测试 → 部署 → 维护**，详见 [开发流程规范.md](file:///d:/yecll/Documents/LocalCode/testskills/.trae/开发流程规范.md)。

三种执行策略（按复杂度）：

| 策略                    | 适用场景              | 交互频率       |
| --------------------- | ----------------- | ---------- |
| **Inline Execution**  | Bug 修复、单函数、配置变更   | 低（1-2 次确认） |
| **Standard Workflow** | 新功能、多文件变更         | 中（3-4 次确认） |
| **Full Workflow**     | 大型项目、多 Sprint、跨模块 | 高（6+ 次确认）  |

## 快捷命令

6 个阶段命令各自独立可执行（支持 refinement 复用），1 个组合命令编排完整流水线：

| 命令                        | 阶段     | 用途                            | 关键选项                                               |
| ------------------------- | ------ | ----------------------------- | -------------------------------------------------- |
| `/bmad-requirements <描述>` | 1 需求分析 | PRD 生成与精炼                     | `--feature` / `--skip-scan`                        |
| `/bmad-design`            | 2 设计   | 架构 + Sprint 计划                | `--feature` / `--direct-dev` / `--target`          |
| `/bmad-development`       | 3 开发   | TDD 实现 + Code Review          | `--feature` / `--skip-review` / `--max-iterations` |
| `/bmad-testing`           | 4 测试   | QA 测试 + 回归                    | `--feature` / `--skip-e2e` / `--skip-security`     |
| `/bmad-deployment`        | 5 部署   | 版本 + CI + Tag                 | `--feature` / `--version` / `--skip-ci`            |
| `/bmad-maintenance <Bug>` | 6 维护   | systematic-debugging + TDD 修复 | `--feature` / `--direct-fix` / `--skip-regression` |
| `/bmad-pipeline <描述>`     | 组合     | 编排阶段 1-5 完整流水线                | `--from` / `--to` / 透传各阶段选项                        |

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
- 命令文件：`bmad-<phase>.md`，含 Usage / Context / Your Role / Execution Flow 四部分
- Skill 目录：kebab-case（如 `test-driven-development`）
- 脚本文件名：snake\_case
- Python：PEP 8，snake\_case 函数，4 空格缩进，复杂逻辑中文注释
- Commit 格式：`Add skill: skill-name v1.0.0` / `docs: 更新流程规范`

## Environment

- Python 3.6+（`.venv/` 虚拟环境，gitignored）
- Playwright MCP（bmad-qa 启用，E2E 测试优先）
- `.trae/cache/`、`.trae/logs/` gitignored
- 敏感文件（`.env`、`*.pem`、`*.key`、`credentials.json`）gitignored

