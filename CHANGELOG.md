# 更新日志

所有重要的更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

## [2.0.0] - 2026-07-23

### 变更（破坏性）

- **项目定位重构**：从"Trae Agent Skills 集合仓库"转向"针对 Trae 的敏捷开发规范与工作流定义"
- **智能体体系重命名**：从中文命名（Architect.md / Developer.md 等 8 个）迁移到 BMAD 命名体系（bmad-architect.md 等 7 个）
- **文档体系重写**：AGENTS.md / README.md / CODE_WIKI.md / CONTRIBUTING.md 全部按新定位重写
- **CODE_WIKI.md 重构**：删除 coros-activity-downloader 逐函数详解，重写为工作流架构 Wiki

### 新增

- **开发流程规范.md v1.1**：补充 §4.0 通用约定（Orchestrator 中介模式、文件保存时机策略、feature_name 命名规范、输入预处理）；§4.1~4.3 补充 STOP POINT 标记；§5.3 展开命令选项说明；§8.2 补充 Task tool 调用模板
- **7 个 BMAD Agent**：bmad-orchestrator / bmad-po / bmad-architect / bmad-sm / bmad-dev / bmad-review / bmad-qa
  - 按 §2.2 规范补充 model 字段（GLM-5.2 / Doubao-Seed-2.1-Pro）
  - 按角色性质配置权限（Architect/Review 禁用 Edit，Orchestrator 禁用 Edit+DeleteFile，QA 启用 mcp_Playwright）
- **3 个快捷命令**：
  - `bmad-pilot.md` — 完整开发流程（支持 `--skip-tests` / `--direct-dev` / `--skip-scan`）
  - `bmad-fix.md` — Bug 修复流程（systematic-debugging + TDD）
  - `bmad-refine.md` — 精炼 PRD / 架构 / Sprint 计划
- **14 个方法论 Skill**：brainstorming / writing-plans / test-driven-development / systematic-debugging / subagent-driven-development / dispatching-parallel-agents / executing-plans / requesting-code-review / receiving-code-review / verification-before-completion / using-git-worktrees / finishing-a-development-branch / writing-skills / using-superpowers

### 移除

- 旧的中文命名智能体定义（Architect.md / Developer.md / Debugger.md / CR-Engineer.md / Test-Engineer.md / DevOps.md / Code-Explorer.md / Product-Manager.md）
- 旧的中文方法论 Skill 目录（产品规划/ 需求分析/ 架构设计/ 等 18 个）
- 旧协作规范文档（指令手册.md / 协作链路.md / Skills协作.md / 完整流程调用规范.md，已合并入开发流程规范.md）
- coros-activity-downloader 相关内容从主文档移除（CODE_WIKI 不再含其逐函数详解）

## [1.0.0] - 2026-04-18

### 新增

- 项目初始化
- 添加第一个 Skill：`coros-activity-downloader` v2.0.0
  - 支持从 COROS Training Hub 下载跑步活动记录
  - 智能重复检测（基于 labelId）
  - 文件完整性验证
  - 支持中文文件名
  - JSON 输出模式
- 添加项目文档
  - README.md
  - CONTRIBUTING.md
  - SKILL_DEVELOPMENT_GUIDE.md
  - Skill 验证脚本

[未发布]: https://github.com/yecllsl/trae-agent-skills/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/yecllsl/trae-agent-skills/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/yecllsl/trae-agent-skills/releases/tag/v1.0.0
