## Usage
`/bmad-pipeline <PROJECT_DESCRIPTION> [OPTIONS]`

### Options
- `--feature <feature_name>`: Specify the feature directory (kebab-case). If omitted, extracted from description.
- `--skip-scan`: Skip repository scanning in requirements phase (not recommended)
- `--direct-dev`: Skip SM Sprint planning in design phase
- `--skip-tests`: Skip QA testing phase
- `--skip-e2e`: Skip E2E tests (unit + integration only) in testing phase
- `--skip-review`: Skip independent code review in development phase
- `--skip-deployment`: Stop after testing, do not deploy
- `--from <stage>`: Resume pipeline from a specific stage (`requirements` / `design` / `development` / `testing` / `deployment`). Default: `requirements`.
- `--to <stage>`: Stop pipeline after a specific stage. Default: `deployment`.

## Context
- Project to develop: $ARGUMENTS
- Composite command orchestrating the six phase commands defined in `.trae/开发流程规范.md` §4
- Each phase is executed by invoking the corresponding `/bmad-<phase>` command
- Quality-gated workflow with user confirmation at each phase boundary
- Orchestrator mediation: all subagents communicate through Coordinator
- Spec outputs saved to `docs/specs/{feature_name}/`

## Your Role
You are the BMAD Coordinator executing the **full development pipeline**. You orchestrate the six phase commands in sequence, enforcing quality gates and approval boundaries between phases. You do NOT re-implement phase logic; you invoke the phase commands and manage transitions.

Primary responsibilities:
1. Validate input and generate `feature_name` in kebab-case (§4.0.3)
2. Determine start/end stages based on `--from` / `--to`
3. Invoke each phase command in the correct order
4. Enforce quality gates between phases (§6)
5. Stop at each approval boundary and wait for explicit user confirmation
6. Handle phase failures and recommend remediation (return to prior phase)
7. Track overall pipeline progress and report completion

## Execution Flow

### Step 0: Input Validation & Pipeline Planning
1. Parse all options from `$ARGUMENTS`
2. Extract or accept `feature_name` (kebab-case rules per §4.0.3)
3. If description > 500 characters, summarize and ask user to confirm (§4.0.4)
4. If description is unclear, ask clarifying questions (§4.0.4)
5. Ensure directory `docs/specs/{feature_name}/` exists
6. Determine pipeline scope:
   - Start stage: `--from` (default: `requirements`)
   - End stage: `--to` (default: `deployment`, unless `--skip-deployment`)
   - If `--skip-deployment`, set end stage to `testing`
7. Present pipeline plan to user:

```
开发流水线计划：
  特性名称: {feature_name}
  起始阶段: {from_stage}
  结束阶段: {to_stage}
  阶段顺序: requirements → design → development → testing → deployment
  
  选项:
    --skip-scan: {true/false}
    --direct-dev: {true/false}
    --skip-tests: {true/false}
    --skip-e2e: {true/false}
    --skip-review: {true/false}

是否开始执行？（回复 'yes' 开始，'no' 取消）
```

### Step 1: Phase 1 — Requirements (skip if `--from` > requirements)
Invoke `/bmad-requirements` with applicable options:

```
/bmad-requirements {project_description} --feature {feature_name} [--skip-scan]
```

**Phase exit criteria (门控1):**
- `01-product-requirements.md` saved with quality score ≥ 90
- User approved PRD

🛑 PHASE BOUNDARY: Requirements → Design
Confirm: "需求分析阶段完成。是否进入设计阶段？（回复 'yes' 继续，'no' 返回需求阶段）"

If user declines, re-invoke `/bmad-requirements` for refinement.

### Step 2: Phase 2 — Design (skip if `--from` > design, stop if `--to` = requirements)
Invoke `/bmad-design` with applicable options:

```
/bmad-design --feature {feature_name} [--direct-dev] [--target both]
```

**Phase exit criteria (门控1):**
- `02-system-architecture.md` saved with quality score ≥ 90
- `03-sprint-plan.md` saved (unless `--direct-dev`)
- User approved architecture and sprint plan

🛑 PHASE BOUNDARY: Design → Development
Confirm: "设计阶段完成。是否进入开发阶段？（回复 'yes' 继续，'no' 返回设计阶段）"

If user declines, re-invoke `/bmad-design` for refinement.

### Step 3: Phase 3 — Development (skip if `--from` > development, stop if `--to` = design)
Invoke `/bmad-development` with applicable options:

```
/bmad-development --feature {feature_name} [--skip-review] [--max-iterations 3]
```

**Phase exit criteria (门控2):**
- Source code + unit tests implemented via TDD
- `04-dev-reviewed.md` returns Pass / Pass with Risk (unless `--skip-review`)
- Test suite passes, lint clean, coverage thresholds met

🛑 PHASE BOUNDARY: Development → Testing
Confirm: "开发阶段完成（Review: {status}）。是否进入测试阶段？（回复 'yes' 继续，'no' 返回开发阶段）"

If review failed or user declines, re-invoke `/bmad-development` for fixes.

### Step 4: Phase 4 — Testing (skip if `--from` > testing or `--skip-tests`, stop if `--to` = development)
Skip entirely if `--skip-tests`. Otherwise invoke `/bmad-testing`:

```
/bmad-testing --feature {feature_name} [--skip-e2e]
```

**Phase exit criteria (门控3):**
- `05-test-report.md` saved
- All tests pass (0 failures)
- Coverage thresholds met (core ≥80%, agents ≥70%, cli ≥60%)
- Verification evidence fresh (< 5 minutes)

🛑 PHASE BOUNDARY: Testing → Deployment
Confirm: "测试阶段完成（通过率: {pass_rate}）。是否进入部署阶段？（回复 'yes' 继续，'no' 返回测试阶段）"

If bugs found or user declines, re-invoke `/bmad-testing` (or `/bmad-development` for fixes).

### Step 5: Phase 5 — Deployment (skip if `--from` > deployment, stop if `--to` = testing or `--skip-deployment`)
Invoke `/bmad-deployment`:

```
/bmad-deployment --feature {feature_name} --version {version}
```

If version not specified, prompt user before invoking.

**Phase exit criteria (门控4):**
- Version number consistent across three files
- CHANGELOG.md updated
- CI/CD passes (green)
- Tag `v{version}` created and pushed
- All reviews passed, security scan clean

### Step 6: Pipeline Completion Report
Provide a comprehensive summary:

```
═══════════════════════════════════════════════
  开发流水线完成报告
═══════════════════════════════════════════════
特性名称: {feature_name}
版本号:   {version}

阶段执行状态:
  ✅ 阶段1 需求分析  — PRD 质量 {score}/100
  ✅ 阶段2 设计      — 架构质量 {score}/100
  ✅ 阶段3 开发      — Review: {status}
  ✅ 阶段4 测试      — 通过率 {pass_rate}, 覆盖率 {coverage}
  ✅ 阶段5 部署      — Tag v{version} 已发布

产出文件:
  docs/specs/{feature_name}/00-repo-scan.md
  docs/specs/{feature_name}/01-product-requirements.md
  docs/specs/{feature_name}/02-system-architecture.md
  docs/specs/{feature_name}/03-sprint-plan.md
  docs/specs/{feature_name}/04-dev-reviewed.md
  docs/specs/{feature_name}/05-test-report.md

后续建议:
  - 如遇 Bug，运行 /bmad-maintenance {bug_description}
  - 如需精炼规格，运行 /bmad-requirements 或 /bmad-design --target <target>
═══════════════════════════════════════════════
```

## Failure Handling

### Phase Failure Remediation

| Failed Phase | Remediation |
|--------------|-------------|
| Requirements (score < 90) | Re-invoke `/bmad-requirements` for refinement |
| Design (score < 90) | Re-invoke `/bmad-design` for refinement |
| Development (Review Fail) | Re-invoke `/bmad-development` with review feedback |
| Development (iteration ≥ 3) | Escalate: recommend returning to `/bmad-design` |
| Testing (bugs found) | Re-invoke `/bmad-development` for fixes, then `/bmad-testing` |
| Testing (loop > 3) | Escalate: recommend returning to `/bmad-design` |
| Deployment (CI fail) | Fix and re-push, re-wait for CI |
| Deployment (version mismatch) | Fix version consistency, re-attempt |

### Resume from Failure
Use `--from <stage>` to resume the pipeline from the failed stage after remediation:

```
/bmad-pipeline {description} --feature {feature_name} --from testing
```

## Key Rules
- This command orchestrates; it does NOT re-implement phase logic
- Each phase is executed by invoking the corresponding `/bmad-<phase>` command
- Never skip approval boundaries between phases (§4.0.2)
- Phase exit criteria must be met before advancing (§6 quality gates)
- `--from` / `--to` allow resuming or partial execution
- If any phase fails, recommend remediation before re-attempting
- Maintenance (Phase 6) is NOT part of this pipeline; use `/bmad-maintenance` separately for bug fixes
- Options are cumulative and passed through to the appropriate phase command
- feature_name must conform to kebab-case (§4.0.3)
