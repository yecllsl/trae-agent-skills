# AGENTS.md — Trae Agent Skills

本项目是作者在使用 [Trae CN IDE](https://www.trae.ai/) 和 Trae Work 过程中的经验总结与方法论实践。

## 项目组成

完整的 AI 辅助开发方法论，包括：

- **智能体定义**（`.trae/agents/`）：6 类专业智能体（产品经理、架构师、开发工程师、测试工程师、发布运维工程师、代码评审工程师）
- **自定义 Skills**（`.trae/skills/`）：覆盖软件开发全生命周期的 Skill（含方法论型和功能型）
- **规则体系**（`.trae/rules/`）：项目规则、安全规则、合规规则、质量规则、流程规则
- **协作规范**：指令手册、协作链路、Skills 协作规范、完整流程调用规范

## Repo structure

```
.trae/                          # 方法论体系（核心内容）
├── agents/                     # 智能体定义（6 类角色）
├── rules/                      # 规则体系
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
├── 指令手册.md                  # 智能体指令定义
├── 协作链路.md                  # 协作流程规范
├── Skills协作.md                # Skill 协作规范
└── 完整流程调用规范.md           # 完整流程调用规范

docs/                           # 开发文档
├── SKILL_DEVELOPMENT_GUIDE.md  # Skill 开发指南
└── SKILL_TEMPLATE.md           # Skill 模板

scripts/                        # 工具脚本
└── validate-skills.py          # Skill 验证脚本
```

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