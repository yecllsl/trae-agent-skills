# AGENTS.md — Trae Agent Skills

本项目是作者在使用 [Trae CN IDE](https://www.trae.ai/) 和 Trae Work 过程中的经验总结与方法论实践。

## 项目组成

完整的 AI 辅助开发方法论，包括：

- **智能体定义**（`.trae/agents/`）：8 类专业智能体（产品经理、架构师、开发工程师、调试工程师、代码评审工程师、测试工程师、发布运维、代码探索员）
- **自定义 Skills**（`.trae/skills/`）：覆盖软件开发全生命周期的 Skill（含方法论型和功能型）
- **规则体系**（`.trae/rules/`）：项目规则、安全规则、合规规则、质量规则、流程规则
- **协作规范**：开发流程规范（统一手册，合并原指令手册、协作链路、Skills协作、完整流程调用规范）

## Repo structure

```
.trae/                          # 方法论体系（核心内容）
├── agents/                     # 智能体定义（8 类角色）
│   ├── Architect.md            # 架构师（最强模型，设计+规划）
│   ├── Developer.md            # 开发工程师（单任务生命周期+TDD）
│   ├── Debugger.md             # 调试工程师（构建修复+根因定位+TDD指导）
│   ├── CR-Engineer.md          # 代码评审工程师（三级严重度+安全审计）
│   ├── Test-Engineer.md        # 测试工程师（策略+执行+回归）
│   ├── DevOps.md               # 发布运维（CICD+发布+知识沉淀）
│   ├── Code-Explorer.md        # 代码探索员（只读，轻量模型）
│   └── Product-Manager.md      # 产品经理
├── rules/                      # 规则体系
│   ├── project-rules.md        # 项目规则（含Coordinator规则）
│   ├── security-rules.md       # 安全规则
│   ├── compliance-rules.md     # 合规规则
│   ├── quality-rules.md        # 质量规则
│   └── process-rules.md        # 流程规则
├── skills/                     # 自定义 Skills（方法论型 + 功能型）
│   ├── 产品规划/                # 方法论型 Skill
│   ├── 需求分析/
│   ├── ...
│   └── coros-activity-downloader/  # 功能型 Skill 示例
│       ├── SKILL.md
│       ├── README.md
│       ├── CHANGELOG.md
│       └── scripts/
│           └── download_coros.py
├── 开发流程规范.md               # 统一流程手册（合并4份文档）
└── skill-config.json           # Skill 配置

docs/                           # 开发文档
├── SKILL_DEVELOPMENT_GUIDE.md  # Skill 开发指南
└── SKILL_TEMPLATE.md           # Skill 模板

scripts/                        # 工具脚本
└── validate-skills.py          # Skill 验证脚本
```

## 智能体体系

| Agent | 职责 | 关键特征 |
|-------|------|---------|
| **Architect** | 需求分析+架构设计+任务拆解+方案评审 | 最强模型，不编辑代码，自我审查checklist |
| **Developer** | 功能开发+单元测试+Bug修复 | 单任务生命周期，4种状态管理，TDD铁律 |
| **Debugger** 🆕 | 构建修复+TDD指导+根因定位 | 最小改动原则，只Edit不Write，systematic-debugging |
| **Code-Reviewer** | 代码评审+安全审计+性能检查 | 三级严重度(CRITICAL/IMPORTANT/SUGGESTION) |
| **Test-Engineer** | 测试策略+测试执行+回归测试 | 上线门禁管控，Playwright优先 |
| **DevOps** | CICD+发布+FIX-CI+知识沉淀 | 发布门禁，知识沉淀OPS-06 |
| **Code-Explorer** 🆕 | 代码搜索+依赖追踪+上下文收集 | 只读权限，轻量模型，结构化输出 |
| **Product-Manager** | 产品规划+价值验收 | 业务方向 |

> 主Agent承担Coordinator职责：工作流编排、阶段转换决策、质量门控检查、异常回退处理。

## Validation

- Run `python scripts/validate-skills.py` to check all skills.
- Run `python scripts/validate-skills.py -s <skill-name>` for a single skill.
- Run `python scripts/validate-skills.py -v` for verbose output.
- Validates: required files, SKILL.md frontmatter (name + description fields), required sections (Purpose, Prerequisites, Usage, Architecture, Error Handling), scripts/ presence.

## SKILL.md requirements

Must start with:
```yaml
---
name: "skill-name"
description: "short desc (50 chars max)"
---
```
Then contain exactly these H2 sections: `## Purpose`, `## Prerequisites`, `## Usage`, `## Architecture`, `## Error Handling`.

## Style conventions

- Skill dirs: kebab-case (e.g., `coros-activity-downloader`)
- Script filenames: snake_case (e.g., `download_coros.py`)
- Python: PEP 8, snake_case functions, 4-space indent, Chinese comments for complex logic
- PR title format: `Add skill: skill-name vX.X.X`
- Commit format: `Add skill: skill-name v1.0.0`
- CLI scripts should support both human-readable and `--json-output` modes where applicable.

## Environment

- Python 3.6+ for Python skills (`.venv/` virtual env in root, gitignored)
- Chrome DevTools MCP configured in `.trae/mcp.json` (disabled by default)
- `.trae/cache/`, `.trae/logs/` are gitignored
- Sensitive files (`.env`, `*.pem`, `*.key`, `credentials.json`) are gitignored
- Downloaded data formats (`.fit`, `.gpx`, `.tcx`) and `download/`, `backup/` dirs are gitignored
